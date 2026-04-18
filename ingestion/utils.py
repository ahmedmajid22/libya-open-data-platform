"""
utils.py
Shared utilities for the Libya Open Data Platform pipeline.
Provides: logging setup, environment loading, BigQuery client, and data loading.
"""

import logging
import os
from datetime import datetime, timezone

import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery


# ── Environment ──────────────────────────────────────────────────────────────

def load_env() -> dict:
    """
    Load environment variables from .env file.
    Returns a dict with all required config values.
    Raises a clear error if any required variable is missing.
    """
    load_dotenv()

    required = [
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GCP_PROJECT_ID",
        "BQ_DATASET_RAW",
        "BQ_DATASET_STAGING",
        "BQ_DATASET_MART",
    ]

    config = {}
    missing = []

    for key in required:
        value = os.getenv(key)
        if value is None:
            missing.append(key)
        else:
            config[key] = value

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            f"Check your .env file."
        )

    return config


# ── Logging ───────────────────────────────────────────────────────────────────

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger.
    Format: timestamp | level | script_name | message
    Usage: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


# ── BigQuery Client ───────────────────────────────────────────────────────────

def get_bq_client(project_id: str) -> bigquery.Client:
    """
    Creates and returns an authenticated BigQuery client.
    Authentication uses GOOGLE_APPLICATION_CREDENTIALS from the environment.
    """
    return bigquery.Client(project=project_id)


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_dataframe_to_bigquery(
    df: pd.DataFrame,
    table_id: str,
    client: bigquery.Client,
    logger: logging.Logger,
) -> None:
    """
    Loads a pandas DataFrame into a BigQuery table.

    Args:
        df:       The DataFrame to load. Must not be empty.
        table_id: Full table path, e.g. 'project.dataset.table_name'
        client:   Authenticated BigQuery client
        logger:   Logger instance for output

    Behavior:
        - Uses WRITE_TRUNCATE: replaces the table on every run
        - This keeps storage small and avoids duplicates
        - Safe to run multiple times — idempotent
    """
    if df.empty:
        logger.warning(f"DataFrame is empty — skipping load to {table_id}")
        return

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    logger.info(f"Loading {len(df)} rows into {table_id}...")

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    table = client.get_table(table_id)
    logger.info(f"✓ Load complete — {table.num_rows} rows now in {table_id}")


# ── Timestamp ─────────────────────────────────────────────────────────────────

def now_utc() -> str:
    """Returns current UTC timestamp as ISO 8601 string for ingested_at columns."""
    return datetime.now(timezone.utc).isoformat()