"""
extract_unhcr.py
Loads UNHCR refugee and displacement data for Libya.

STATUS: Phase 2 — not yet implemented.
In Phase 1, the mart table covers World Bank indicators only.

When implemented, this will:
1. Read the UNHCR CSV (downloaded from unhcr.org/refugee-statistics)
2. Filter to Libya as origin and asylum country
3. Return a clean DataFrame with refugee counts by year
4. This feeds the migration columns in fact_libya_yearly_metrics
"""

from ingestion.utils import get_logger

logger = get_logger(__name__)


def extract_unhcr() -> None:
    """Phase 2 placeholder. Returns None until implemented."""
    logger.info("UNHCR extraction — Phase 2, not yet implemented")
    return None