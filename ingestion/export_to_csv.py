"""
export_to_csv.py
Exports the mart layer fact table to data/fact_libya_yearly_metrics.csv.
This file is committed to GitHub and becomes the public downloadable dataset.

Run after dbt models have been built:
    python -m ingestion.export_to_csv
"""

import os
from pathlib import Path

import pandas as pd

from ingestion.utils import get_bq_client, get_logger, load_env

logger = get_logger(__name__)

# Path to the output CSV — relative to project root
OUTPUT_PATH = Path("data") / "fact_libya_yearly_metrics.csv"


def export_mart_to_csv() -> None:
    """
    Reads the mart fact table from BigQuery and saves it as a CSV.

    Steps:
    1. Connect to BigQuery
    2. Query mart.fact_libya_yearly_metrics
    3. Save result to data/fact_libya_yearly_metrics.csv
    4. Log stats (rows, file size, path)
    """
    logger.info("╔══════════════════════════════════════════╗")
    logger.info("║  Libya Data Platform — CSV Export        ║")
    logger.info("╚══════════════════════════════════════════╝")

    # ── Load config ───────────────────────────────────────────────
    config = load_env()
    project_id = config["GCP_PROJECT_ID"]
    mart_dataset = config["BQ_DATASET_MART"]

    # ── Connect to BigQuery ───────────────────────────────────────
    logger.info("Connecting to BigQuery...")
    client = get_bq_client(project_id)
    logger.info(f"✓ Connected to project: {project_id}")

    # ── Query the mart table ──────────────────────────────────────
    table_ref = f"{project_id}.{mart_dataset}.fact_libya_yearly_metrics"
    query = f"""
        SELECT *
        FROM `{table_ref}`
        ORDER BY year ASC
    """

    logger.info(f"Querying: {table_ref}")

    try:
        df = client.query(query).to_dataframe(create_bqstorage_client=False)
    except Exception as e:
        logger.error(f"Failed to query mart table: {e}")
        logger.error("Make sure dbt models have been built first (dbt run)")
        raise

    if df.empty:
        logger.error("Mart table is empty — make sure dbt ran successfully")
        raise RuntimeError("Empty mart table")

    logger.info(f"✓ Retrieved {len(df)} rows from mart")

    # ── Ensure output directory exists ────────────────────────────
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # ── Save to CSV ───────────────────────────────────────────────
    df.to_csv(OUTPUT_PATH, index=False)

    file_size_kb = OUTPUT_PATH.stat().st_size / 1024

    logger.info("╔══════════════════════════════════════════╗")
    logger.info("║  Export Complete ✓                       ║")
    logger.info(f"║  File:  {OUTPUT_PATH}")
    logger.info(f"║  Rows:  {len(df)}")
    logger.info(f"║  Size:  {file_size_kb:.1f} KB")
    logger.info("╚══════════════════════════════════════════╝")

    # Preview first few rows
    logger.info("\nPreview of exported data:")
    logger.info(df.head(3).to_string(index=False))


if __name__ == "__main__":
    export_mart_to_csv()