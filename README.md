<div align="center">

<img src="https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/docs/flag.png" width="80" alt="Libya Flag" />

# 🇱🇾 Libya Open Data Platform

**An end-to-end automated data engineering pipeline — built to make Libya's data accessible to the world.**

<br/>

[![Pipeline](https://github.com/ahmedmajid22/libya-open-data-platform/actions/workflows/pipeline.yml/badge.svg)](https://github.com/ahmedmajid22/libya-open-data-platform/actions/workflows/pipeline.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data: World Bank](https://img.shields.io/badge/Data-World%20Bank-blue)](https://data.worldbank.org)
[![Warehouse: BigQuery](https://img.shields.io/badge/Warehouse-BigQuery-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![Transform: dbt](https://img.shields.io/badge/Transform-dbt-FF694B?logo=dbt&logoColor=white)](https://www.getdbt.com)
[![Automation: GitHub Actions](https://img.shields.io/badge/Automation-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)

<br/>

*Every Monday at 06:00 UTC — data is extracted, transformed, tested, and published. Automatically. No human intervention.*

<br/>

[📥 Download Dataset](#-public-dataset) · [📊 View Dashboard](#-dashboard) · [🏗 Architecture](#-architecture) · [📖 Data Dictionary](#-data-dictionary)

---

</div>

## ✦ What Is This?

Open data about Libya is fragmented, hard to find, and rarely in a format you can actually use. This project changes that.

The **Libya Open Data Platform** is a production-grade data pipeline that:

- Automatically collects macroeconomic and demographic data from the **World Bank API** every week
- Cleans, types, and transforms it through a **dbt** staging + mart layer with full documentation
- Validates every run with **13 automated data quality tests** — bad data never reaches the public
- Publishes a clean, versioned **public CSV** to this repository every Monday
- Tracks **24 years of data** (2000–2023), including conflict periods and their data gaps

The result is a single, reliable, continuously-updated dataset that any researcher, analyst, or developer can use in seconds.

---

## 📥 Public Dataset

The dataset is available in two ways:

**1 — Direct file in this repo:**
[`data/fact_libya_yearly_metrics.csv`](data/fact_libya_yearly_metrics.csv)

**2 — Raw URL (use directly in Python, R, Excel):**
```
https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv
```

```python
import pandas as pd

url = "https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv"
df = pd.read_csv(url)
print(df[['year', 'population_total', 'gdp_usd', 'unemployment_rate']])
```

> The dataset is updated automatically every Monday. The commit message on this file shows the exact date of the last update.

---

## 📊 Dashboard

> 🔗 [Open Live Dashboard](https://datastudio.google.com/reporting/ca23d690-a8b4-4506-8a39-f980855fd765)

| Population Trends | Economic Indicators |
|---|---|
| ![Population Dashboard](docs/dashboard-population.png) | ![Economy Dashboard](docs/dashboard-economy.png) |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS  (every Monday 06:00 UTC)          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
          ┌────────────────────▼────────────────────┐
          │           EXTRACT + LOAD                 │
          │  Python → World Bank API → BigQuery raw  │
          └────────────────────┬────────────────────┘
                               │
          ┌────────────────────▼────────────────────┐
          │              TRANSFORM                   │
          │   dbt staging (view) → dbt mart (table)  │
          └────────────────────┬────────────────────┘
                               │
          ┌────────────────────▼────────────────────┐
          │                 TEST                     │
          │    13 data quality tests — must all pass │
          └────────────────────┬────────────────────┘
                               │
          ┌────────────────────▼────────────────────┐
          │               PUBLISH                    │
          │   CSV → /data  ·  Committed to GitHub    │
          └─────────────────────────────────────────┘
```

### BigQuery Layers

| Layer | Dataset | Object | Type | Purpose |
|---|---|---|---|---|
| Raw | `raw` | `raw_worldbank` | Table | Unmodified source data |
| Staging | `staging` | `stg_worldbank` | View | Cleaned, typed, filtered |
| Mart | `mart` | `fact_libya_yearly_metrics` | Table | Analytics-ready fact table |

---

## 📁 Project Structure

```
libya-open-data-platform/
│
├── .github/
│   └── workflows/
│       └── pipeline.yml          # Full automation — runs every Monday
│
├── ingestion/
│   ├── extract_worldbank.py      # Pulls data from World Bank API
│   ├── load_to_bigquery.py       # Loads DataFrame into BigQuery raw layer
│   ├── export_to_csv.py          # Exports mart table to /data CSV
│   └── utils.py                  # Shared helpers (logging, BQ client, env)
│
├── dbt_libya/
│   ├── models/
│   │   ├── sources.yml           # Declares raw BigQuery tables as sources
│   │   ├── staging/
│   │   │   ├── stg_worldbank.sql # Cleans and types raw data (BigQuery view)
│   │   │   └── schema.yml        # Column docs + 9 automated tests
│   │   └── mart/
│   │       ├── fact_libya_yearly_metrics.sql  # Final analytics table
│   │       └── schema.yml        # Column docs + 4 automated tests
│   ├── tests/
│   │   ├── assert_population_positive.sql     # Custom test: pop > 0
│   │   └── assert_gdp_positive.sql            # Custom test: gdp > 0
│   ├── macros/
│   │   └── generate_schema_name.sql           # Schema routing macro
│   └── dbt_project.yml
│
├── data/
│   ├── fact_libya_yearly_metrics.csv          # ← Public dataset (auto-updated)
│   └── README.md                              # Dataset documentation
│
├── docs/
│   └── data_dictionary.md                     # Full column reference
│
├── DISCLAIMER.md
├── LICENSE                                    # CC BY 4.0
├── requirements.txt
└── README.md
```

---

## 📖 Data Dictionary

Full reference: [`docs/data_dictionary.md`](docs/data_dictionary.md)

| Column | Type | Nullable | Source | Description |
|---|---|---|---|---|
| `year` | INT64 | No | All | Reference year — primary key (2000–2023) |
| `population_total` | FLOAT64 | Yes | World Bank | Total Libya population |
| `gdp_usd` | FLOAT64 | Yes | World Bank | GDP in current US dollars |
| `gdp_per_capita_usd` | FLOAT64 | Yes | World Bank | GDP per capita in current USD |
| `unemployment_rate` | FLOAT64 | Yes | World Bank | Unemployment as % of labor force |
| `inflation_rate` | FLOAT64 | Yes | World Bank | Annual consumer price inflation % |
| `refugees_from_libya` | FLOAT64 | Yes | UNHCR *(Phase 2)* | People registered as refugees |
| `asylum_seekers_count` | FLOAT64 | Yes | UNHCR *(Phase 2)* | Asylum seekers from Libya |
| `gdp_per_person_calculated` | FLOAT64 | Yes | Derived | `ROUND(gdp_usd / population_total, 2)` |
| `population_yoy_change` | FLOAT64 | Yes | Derived | Population minus prior year |
| `gdp_yoy_change_usd` | FLOAT64 | Yes | Derived | GDP minus prior year (USD) |
| `conflict_period_note` | STRING | Yes | Categorical | Context label for conflict years |
| `wb_source` | STRING | Yes | Metadata | Always `world_bank` |
| `wb_ingested_at` | TIMESTAMP | Yes | Metadata | Pipeline run timestamp |

### ⚠️ A note on null values

Nulls in this dataset are **real data gaps — not errors.** They reflect years where the World Bank did not publish data for Libya, most commonly during conflict periods:

- **2011** — Revolution. Economic reporting partially collapsed.
- **2014–2016** — Second civil war. Several indicators went unreported.

Do not replace nulls with zero. Zero and "no data" are different things.

---

## 🔬 Data Quality

Every pipeline run executes 13 automated tests before the CSV is published. If any test fails, the pipeline stops — no bad data reaches the public.

<details>
<summary>View all 13 tests</summary>

| Test | Model | Type |
|---|---|---|
| `not_null` on `year` | stg_worldbank | Generic |
| `unique` on `year` | stg_worldbank | Generic |
| `accepted_range` year 2000–2023 | stg_worldbank | dbt_utils |
| `not_null` on `country_code` | stg_worldbank | Generic |
| `accepted_values` country_code = LY | stg_worldbank | Generic |
| `not_null` on `country_name` | stg_worldbank | Generic |
| `not_null` on `source` | stg_worldbank | Generic |
| `accepted_values` source = world_bank | stg_worldbank | Generic |
| `not_null` on `ingested_at` | stg_worldbank | Generic |
| `not_null` on `year` | fact_libya_yearly_metrics | Generic |
| `unique` on `year` | fact_libya_yearly_metrics | Generic |
| `unique_combination_of_columns` [year] | fact_libya_yearly_metrics | dbt_utils |
| `assert_population_positive` | fact_libya_yearly_metrics | Custom |

</details>

---

## 🛠 Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Extraction | Python 3.11 | World Bank API + pandas |
| Storage | Google BigQuery | Scalable, serverless, free tier |
| Transformation | dbt 1.11 | SQL-first, testable, documented |
| Automation | GitHub Actions | Free, reliable, audit-logged |
| Data source | World Bank Open Data | CC BY 4.0, reliable, global |
| Future | UNHCR Refugee Statistics | Phase 2 — migration data |

---

## 🚀 Run It Locally

```bash
# Clone
git clone https://github.com/ahmedmajid22/libya-open-data-platform.git
cd libya-open-data-platform

# Install dependencies
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Set up environment
cp .env.example .env   # Add your GCP credentials

# Run ingestion
python -m ingestion.load_to_bigquery

# Run dbt
cd dbt_libya
dbt deps
dbt run
dbt test

# Export CSV
cd ..
python -m ingestion.export_to_csv
```

---

## 🗺 Roadmap

- [x] World Bank ingestion pipeline
- [x] BigQuery raw + staging + mart layers
- [x] 13 automated data quality tests
- [x] GitHub Actions weekly automation
- [x] Public CSV export
- [x] Looker Studio dashboard
- [ ] UNHCR refugee and displacement data (Phase 2)
- [ ] REST API endpoint for the dataset
- [ ] Data versioning and changelog
- [ ] Additional open data sources

---

## ⚖️ License & Attribution

This project is released under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)**.

You are free to use, share, and adapt this data for any purpose — including commercial use — as long as you provide attribution.

**Attribution:** Libya Open Data Platform — [github.com/ahmedmajid22/libya-open-data-platform](https://github.com/ahmedmajid22/libya-open-data-platform)

The underlying source data remains the property of:
- [World Bank Open Data](https://data.worldbank.org) — CC BY 4.0
- [UNHCR Refugee Statistics](https://www.unhcr.org/refugee-statistics) — CC BY 4.0

See [`DISCLAIMER.md`](DISCLAIMER.md) for full data source notes and limitations.

---

<div align="center">

**Built with care for open access to data about Libya.**

*If this is useful to you — give it a ⭐ and share it.*

</div>