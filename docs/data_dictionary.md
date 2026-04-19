# Libya Open Data Platform — Data Dictionary

## Raw Layer (raw dataset in BigQuery)

### raw.raw_worldbank
Unmodified World Bank data as loaded by ingestion. Never modify this table.

| Column | Type | Description |
|---|---|---|
| `year` | INTEGER | Reference year |
| `population_total` | FLOAT | Total population |
| `gdp_usd` | FLOAT | GDP in current USD |
| `gdp_per_capita_usd` | FLOAT | GDP per capita USD |
| `unemployment_rate` | FLOAT | Unemployment % |
| `inflation_rate` | FLOAT | Inflation % |
| `country_code` | STRING | Always 'LY' |
| `country_name` | STRING | Always 'Libya' |
| `source` | STRING | Always 'world_bank' |
| `ingested_at` | TIMESTAMP | UTC time of ingestion |

## Staging Layer (staging dataset in BigQuery)

### staging.stg_worldbank
Cleaned and typed view of raw_worldbank. Filtered to LY, 2000-2023.

## Mart Layer (mart dataset in BigQuery)

### mart.fact_libya_yearly_metrics
Primary analytics table. One row per year. Feeds dashboard and public CSV.

| Column | Type | Nullable | Description |
|---|---|---|---|
| `year` | INT64 | No | Primary key |
| `population_total` | FLOAT64 | Yes | Total Libya population |
| `gdp_usd` | FLOAT64 | Yes | GDP current USD |
| `gdp_per_capita_usd` | FLOAT64 | Yes | GDP per capita |
| `unemployment_rate` | FLOAT64 | Yes | Unemployment % |
| `inflation_rate` | FLOAT64 | Yes | Annual inflation % |
| `refugees_from_libya` | FLOAT64 | Yes | Phase 2 — null now |
| `asylum_seekers_count` | FLOAT64 | Yes | Phase 2 — null now |
| `gdp_per_person_calculated` | FLOAT64 | Yes | gdp_usd / population_total |
| `population_yoy_change` | FLOAT64 | Yes | Population minus prior year |
| `gdp_yoy_change_usd` | FLOAT64 | Yes | GDP minus prior year |
| `conflict_period_note` | STRING | Yes | Conflict context label |
| `wb_source` | STRING | Yes | 'world_bank' |
| `wb_ingested_at` | TIMESTAMP | Yes | Last ingestion timestamp |

## Null Value Policy

Nulls are real data gaps, not errors. Do not replace with zero.
