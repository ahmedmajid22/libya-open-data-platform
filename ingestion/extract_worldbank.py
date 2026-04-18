"""
extract_worldbank.py
Extracts population, GDP, unemployment, and inflation data
from the World Bank Open Data API for Libya (country code: LY).

API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/898590
No API key required.
"""

import time

import pandas as pd
import requests

from ingestion.utils import get_logger, now_utc

logger = get_logger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

COUNTRY_CODE = "LY"
BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"

# Year range to pull — World Bank has data from 1960 but Libya coverage starts ~2000
START_YEAR = 2000
END_YEAR = 2023

# Indicators to pull with human-readable names
# Format: { "INDICATOR_CODE": "column_name_in_output" }
INDICATORS = {
    "SP.POP.TOTL":    "population_total",
    "NY.GDP.MKTP.CD": "gdp_usd",
    "NY.GDP.PCAP.CD": "gdp_per_capita_usd",
    "SL.UEM.TOTL.ZS": "unemployment_rate",
    "FP.CPI.TOTL.ZG": "inflation_rate",
}


# ── API Functions ─────────────────────────────────────────────────────────────

def fetch_indicator(indicator_code: str, column_name: str) -> pd.DataFrame:
    """
    Fetches all available yearly data for one World Bank indicator for Libya.

    Args:
        indicator_code: World Bank indicator code (e.g. 'SP.POP.TOTL')
        column_name:    What to name the value column in the output DataFrame

    Returns:
        DataFrame with columns: year, {column_name}, indicator_code, indicator_name

    Notes:
        - Handles pagination automatically (World Bank returns max 100 rows per page)
        - Filters to START_YEAR–END_YEAR range
        - Skips years where the API returns null (Libya has gaps in some indicators)
        - Adds a 0.5s delay between pages to be respectful to the API
    """
    url = BASE_URL.format(country=COUNTRY_CODE, indicator=indicator_code)
    params = {
        "format": "json",
        "per_page": 100,
        "mrv": END_YEAR - START_YEAR + 1,  # Most recent values, covers our range
        "date": f"{START_YEAR}:{END_YEAR}",
    }

    logger.info(f"Fetching indicator: {indicator_code} ({column_name})")

    all_records = []
    page = 1

    while True:
        params["page"] = page
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {indicator_code} page {page}: {e}")
            break

        data = response.json()

        # World Bank API returns [metadata, data] as a list
        if not isinstance(data, list) or len(data) < 2:
            logger.warning(f"Unexpected API response format for {indicator_code}")
            break

        metadata = data[0]
        records = data[1]

        if records is None:
            logger.warning(f"No data returned for {indicator_code}")
            break

        for record in records:
            # Skip null values — Libya has missing years for some indicators
            if record.get("value") is None:
                logger.debug(f"  Skipping null value for year {record.get('date')}")
                continue

            try:
                year = int(record["date"])
            except (ValueError, TypeError):
                continue

            # Filter to our year range
            if not (START_YEAR <= year <= END_YEAR):
                continue

            all_records.append({
                "year":           year,
                column_name:      float(record["value"]),
                "indicator_code": indicator_code,
                "indicator_name": record.get("indicator", {}).get("value", ""),
            })

        # Check if there are more pages
        total_pages = metadata.get("pages", 1)
        if page >= total_pages:
            break

        page += 1
        time.sleep(0.5)  # Be polite to the API

    df = pd.DataFrame(all_records)

    if df.empty:
        logger.warning(f"No data collected for {indicator_code}")
    else:
        logger.info(f"  ✓ {len(df)} years collected for {indicator_code}")

    return df


# ── Main Extract Function ─────────────────────────────────────────────────────

def extract_worldbank() -> pd.DataFrame:
    """
    Pulls all indicators for Libya and combines them into one wide DataFrame.

    Each indicator starts as a tall DataFrame (one row per year).
    We pivot so that the final output is one row per year with all indicators
    as separate columns. This is the clean format for loading into BigQuery.

    Returns:
        DataFrame with columns:
            year, population_total, gdp_usd, gdp_per_capita_usd,
            unemployment_rate, inflation_rate,
            country_code, country_name, source, ingested_at
    """
    logger.info("=" * 60)
    logger.info("Starting World Bank extraction for Libya")
    logger.info(f"Year range: {START_YEAR}–{END_YEAR}")
    logger.info(f"Indicators: {len(INDICATORS)}")
    logger.info("=" * 60)

    # Pull each indicator separately
    indicator_dfs = {}
    for code, column_name in INDICATORS.items():
        df = fetch_indicator(code, column_name)
        if not df.empty:
            # Keep only year and the value column
            indicator_dfs[column_name] = df[["year", column_name]].set_index("year")

    if not indicator_dfs:
        logger.error("No data collected from any indicator — check API connectivity")
        return pd.DataFrame()

    # Merge all indicators on year (outer join keeps years even if one indicator has gaps)
    combined = pd.DataFrame()
    for column_name, df in indicator_dfs.items():
        if combined.empty:
            combined = df
        else:
            combined = combined.join(df, how="outer")

    combined = combined.reset_index()  # year becomes a column again
    combined = combined.sort_values("year").reset_index(drop=True)

    # Add metadata columns
    combined["country_code"] = COUNTRY_CODE
    combined["country_name"] = "Libya"
    combined["source"] = "world_bank"
    combined["ingested_at"] = now_utc()

    # Ensure year is integer
    combined["year"] = combined["year"].astype(int)

    logger.info("=" * 60)
    logger.info(f"Extraction complete: {len(combined)} year-rows")
    logger.info(f"Year range in data: {combined['year'].min()}–{combined['year'].max()}")
    logger.info(f"Columns: {list(combined.columns)}")

    # Report any years with null values (expected for conflict years)
    null_report = combined.isnull().sum()
    null_cols = null_report[null_report > 0]
    if not null_cols.empty:
        logger.info("Years with missing values (expected for conflict periods):")
        for col, count in null_cols.items():
            logger.info(f"  {col}: {count} missing years")
    logger.info("=" * 60)

    return combined


# ── Standalone Test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = extract_worldbank()
    if not df.empty:
        print("\n--- Sample Output (first 5 rows) ---")
        print(df.head().to_string(index=False))
        print(f"\nShape: {df.shape}")
        print(f"Columns: {list(df.columns)}")