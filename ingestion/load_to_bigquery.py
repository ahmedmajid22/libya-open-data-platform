"""
load_to_bigquery.py
Orchestrates the full ingestion pipeline.
Calls all extractors and loads results into the BigQuery raw layer.

Run this script to execute a full ingestion cycle:
    python -m ingestion.load_to_bigquery
"""

from ingestion.extract_worldbank import extract_worldbank
from ingestion.utils import get_bq_client, get_logger, load_dataframe_to_bigquery, load_env

logger = get_logger(__name__)


def run_ingestion() -> None:
    """
    Full ingestion pipeline:
    1. Load environment config
    2. Create BigQuery client
    3. Extract World Bank data
    4. Load into raw.raw_worldbank
    """
    logger.info("╔══════════════════════════════════════════╗")
    logger.info("║  Libya Data Platform — Ingestion Start   ║")
    logger.info("╚══════════════════════════════════════════╝")

    # ── Load config ───────────────────────────────────────────────
    config = load_env()
    project_id = config["GCP_PROJECT_ID"]
    raw_dataset = config["BQ_DATASET_RAW"]

    # ── Create BigQuery client ────────────────────────────────────
    logger.info("Connecting to BigQuery...")
    client = get_bq_client(project_id)
    logger.info(f"✓ Connected to project: {project_id}")

    # ── Extract: World Bank ───────────────────────────────────────
    logger.info("\n── Step 1: World Bank Extraction ──────────────")
    wb_df = extract_worldbank()

    if wb_df.empty:
        logger.error("World Bank extraction returned no data — aborting ingestion")
        raise RuntimeError("Empty DataFrame from World Bank extraction")

    # ── Load: World Bank → raw.raw_worldbank ──────────────────────
    logger.info("\n── Step 2: Load to BigQuery ────────────────────")
    table_id = f"{project_id}.{raw_dataset}.raw_worldbank"
    load_dataframe_to_bigquery(wb_df, table_id, client, logger)

    # ── Summary ───────────────────────────────────────────────────
    logger.info("\n╔══════════════════════════════════════════╗")
    logger.info("║  Ingestion Complete ✓                    ║")
    logger.info(f"║  Table: {raw_dataset}.raw_worldbank")
    logger.info(f"║  Rows:  {len(wb_df)}")
    logger.info("╚══════════════════════════════════════════╝")


if __name__ == "__main__":
    run_ingestion()