"""
extract_un.py
Loads UN Data population estimates for Libya.

STATUS: Phase 2 — not yet implemented.
In Phase 1, the World Bank API is the primary population source.

When implemented, this will:
1. Read the UN Data CSV (manually downloaded from data.un.org)
2. Filter to Libya rows
3. Return a clean DataFrame matching the raw_worldbank schema
4. This data will be used in stg_population_reconciliation.sql for cross-checking
"""

from ingestion.utils import get_logger

logger = get_logger(__name__)


def extract_un() -> None:
    """Phase 2 placeholder. Returns None until implemented."""
    logger.info("UN Data extraction — Phase 2, not yet implemented")
    return None