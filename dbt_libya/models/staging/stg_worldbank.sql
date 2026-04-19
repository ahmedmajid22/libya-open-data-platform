{{ config(
    schema='staging',
    materialized='view'
) }}

WITH source_data AS (

    SELECT * FROM {{ source('raw', 'raw_worldbank') }}

),

cleaned AS (

    SELECT

        -- ── Identity ─────────────────────────────────────────────
        CAST(year AS INT64) AS year,

        country_code,
        country_name,

        -- ── Metrics ──────────────────────────────────────────────
        CAST(population_total AS FLOAT64) AS population_total,
        CAST(gdp_usd AS FLOAT64) AS gdp_usd,
        CAST(gdp_per_capita_usd AS FLOAT64) AS gdp_per_capita_usd,
        CAST(unemployment_rate AS FLOAT64) AS unemployment_rate,
        CAST(inflation_rate AS FLOAT64) AS inflation_rate,

        CAST(source AS STRING) AS source,

        -- ── Lineage ───────────────────────────────────────────────
        CAST(ingested_at AS TIMESTAMP) AS ingested_at

    FROM source_data

    WHERE
        country_code = 'LY'

        AND CAST(year AS INT64) BETWEEN 2000 AND 2023

        AND NOT (
            population_total IS NULL AND
            gdp_usd IS NULL AND
            gdp_per_capita_usd IS NULL AND
            unemployment_rate IS NULL AND
            inflation_rate IS NULL
        )

)

SELECT *
FROM cleaned
ORDER BY year