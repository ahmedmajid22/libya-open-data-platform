/*
fact_libya_yearly_metrics.sql
Final analytics fact table — one row per year, all metrics combined.

This is the primary output of the Libya Open Data Platform.
It feeds:
  - Looker Studio dashboard (direct BigQuery connection)
  - Public CSV (exported by export_to_csv.py)
  - Future API endpoints

Design decisions:
  - One row per year (grain = year)
  - LEFT JOINs used so no years are dropped even if some sources are missing
  - Derived metrics calculated here, not in staging (business logic in mart)
  - SAFE_DIVIDE used instead of plain division to handle zero denominators
  - Column order: identifier → population → economy → migration → derived → metadata
*/

WITH worldbank AS (

    SELECT
        year,
        population_total,
        gdp_usd,
        gdp_per_capita_usd,
        unemployment_rate,
        inflation_rate,
        source            AS wb_source,
        ingested_at       AS wb_ingested_at
    FROM {{ ref('stg_worldbank') }}

),

/*
    Spine: generate one row per year from 2000 to 2023.
    This ensures ALL years appear in the output, even if
    some are completely missing from the source data.
    BigQuery's GENERATE_ARRAY is free to use.
*/
year_spine AS (

    SELECT year
    FROM UNNEST(GENERATE_ARRAY(2000, 2023)) AS year

),

joined AS (

    SELECT
        spine.year,
        wb.population_total,
        wb.gdp_usd,
        wb.gdp_per_capita_usd,
        wb.unemployment_rate,
        wb.inflation_rate,
        wb.wb_source,
        wb.wb_ingested_at

    FROM year_spine AS spine
    LEFT JOIN worldbank AS wb
        ON spine.year = wb.year

),

with_derived_metrics AS (

    SELECT
        -- ── Core identifier ───────────────────────────────────────
        year,

        -- ── Population ───────────────────────────────────────────
        population_total,

        -- ── Economy ──────────────────────────────────────────────
        gdp_usd,
        gdp_per_capita_usd,
        unemployment_rate,
        inflation_rate,

        -- ── Migration (Phase 2 — null until UNHCR data is added) ──
        CAST(NULL AS FLOAT64) AS refugees_from_libya,
        CAST(NULL AS FLOAT64) AS asylum_seekers_count,

        -- ── Derived metrics ───────────────────────────────────────
        -- GDP per person (our own calculation vs World Bank's official figure)
        -- Using SAFE_DIVIDE to handle years where population or GDP is null
        ROUND(
            SAFE_DIVIDE(gdp_usd, population_total),
            2
        ) AS gdp_per_person_calculated,

        -- Year-over-year population change
        population_total - LAG(population_total)
            OVER (ORDER BY year)
        AS population_yoy_change,

        -- Year-over-year GDP change
        gdp_usd - LAG(gdp_usd)
            OVER (ORDER BY year)
        AS gdp_yoy_change_usd,

        -- ── Conflict period flag (important context for analysts) ──
        CASE
            WHEN year = 2011
                THEN 'Revolution (2011 civil war)'
            WHEN year BETWEEN 2014 AND 2019
                THEN 'Second civil war period'
            ELSE NULL
        END AS conflict_period_note,

        -- ── Metadata ─────────────────────────────────────────────
        wb_source,
        wb_ingested_at

    FROM joined

)

SELECT * FROM with_derived_metrics
ORDER BY year ASC