<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:16213e,100:0f3460&height=200&section=header&text=🇱🇾%20Libya%20Open%20Data%20Platform&fontSize=38&fontColor=ffffff&fontAlignY=38&desc=Automated%20·%20Tested%20·%20Open%20Source&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3000&pause=800&color=4FC3F7&center=true&vCenter=true&multiline=true&width=650&height=90&lines=World+Bank+API+%E2%86%92+BigQuery+%E2%86%92+dbt+%E2%86%92+GitHub;Every+Monday+at+06%3A00+UTC+%C2%B7+Zero+manual+work;13%2F13+data+quality+tests+passing+%E2%9C%93" alt="Typing animation"/>

<br/><br/>

[![Pipeline](https://github.com/ahmedmajid22/libya-open-data-platform/actions/workflows/pipeline.yml/badge.svg?style=for-the-badge)](https://github.com/ahmedmajid22/libya-open-data-platform/actions)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-22c55e?style=for-the-badge)](LICENSE)
[![Data](https://img.shields.io/badge/Years-2000–2023-f59e0b?style=for-the-badge)](data/fact_libya_yearly_metrics.csv)
[![Tests](https://img.shields.io/badge/Tests-13%2F13%20Passing-22c55e?style=for-the-badge&logo=checkmarx&logoColor=white)](dbt_libya/models)

<br/>

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=flat-square&logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat-square&logo=dbt&logoColor=white)](https://getdbt.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Looker Studio](https://img.shields.io/badge/Looker%20Studio-4285F4?style=flat-square&logo=google&logoColor=white)](https://datastudio.google.com)

</div>

---

## ◈ The Problem

> Open data about Libya is fragmented, inconsistent, and buried across international databases.
> A researcher shouldn't need days to get a clean table of GDP and population figures.

This project solves that — once, permanently, automatically.

---

## ◈ What Happens Every Monday

```
  06:00 UTC — GitHub Actions wakes up
       │
       ▼
  ┌─────────────────────────────────────────────────────┐
  │  STEP 1 · EXTRACT                                   │
  │  Python calls the World Bank API                    │
  │  5 indicators × 24 years = 23 data rows             │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │  STEP 2 · LOAD                                      │
  │  Raw data lands in BigQuery  raw.raw_worldbank       │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │  STEP 3 · TRANSFORM                                 │
  │  dbt builds staging.stg_worldbank  (view)           │
  │  dbt builds mart.fact_libya_yearly_metrics (table)  │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │  STEP 4 · TEST                                      │
  │  13 data quality checks run                         │
  │  ✗ Any failure → pipeline stops. No bad data ships. │
  │  ✓ All pass  → continue                             │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │  STEP 5 · PUBLISH                                   │
  │  CSV exported → committed to /data with timestamp   │
  │  Anyone in the world can now download clean data    │
  └─────────────────────────────────────────────────────┘
```

---

## ◈ Data Warehouse Architecture

<div align="center">

| Layer | Dataset | Object | Type | Role |
|:---:|:---:|:---:|:---:|:---|
| 🥉 Raw | `raw` | `raw_worldbank` | **Table** | Unmodified source truth — never edited |
| 🥈 Staging | `staging` | `stg_worldbank` | **View** | Cleaned, typed, filtered to LY 2000–2023 |
| 🥇 Mart | `mart` | `fact_libya_yearly_metrics` | **Table** | Analytics-ready — feeds dashboard + CSV |

</div>

---

## ◈ Public Dataset

<div align="center">

### [`data/fact_libya_yearly_metrics.csv`](data/fact_libya_yearly_metrics.csv)

**Direct URL — paste into Python, R, or Excel:**

```
https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv
```

</div>

<details>
<summary><b>▶ Python — load in 2 lines</b></summary>

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv"
)

# GDP in billions, population in millions
df["gdp_billions"] = df["gdp_usd"] / 1e9
df["population_millions"] = df["population_total"] / 1e6

print(df[["year", "population_millions", "gdp_billions", "unemployment_rate"]])
```

</details>

<details>
<summary><b>▶ R — load in 1 line</b></summary>

```r
df <- read.csv("https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv")
head(df)
```

</details>

<details>
<summary><b>▶ Excel — no code needed</b></summary>

```
1. Open Excel
2. Data → From Web
3. Paste the URL above
4. Click Load
5. Click Refresh any time for latest data
```

</details>

---

## ◈ Data Dictionary

| Column | Type | Source | Description |
|:---|:---:|:---:|:---|
| `year` | INT64 | — | Primary key · 2000–2023 |
| `population_total` | FLOAT64 | World Bank | Total Libya population |
| `gdp_usd` | FLOAT64 | World Bank | GDP in current US dollars |
| `gdp_per_capita_usd` | FLOAT64 | World Bank | GDP per capita in current USD |
| `unemployment_rate` | FLOAT64 | World Bank | Unemployment % of labor force |
| `inflation_rate` | FLOAT64 | World Bank | Annual consumer price inflation % |
| `refugees_from_libya` | FLOAT64 | UNHCR* | People registered as refugees |
| `asylum_seekers_count` | FLOAT64 | UNHCR* | Asylum seekers from Libya |
| `gdp_per_person_calculated` | FLOAT64 | Derived | `ROUND(gdp_usd / population_total, 2)` |
| `population_yoy_change` | FLOAT64 | Derived | Population delta vs prior year |
| `gdp_yoy_change_usd` | FLOAT64 | Derived | GDP delta vs prior year (USD) |
| `conflict_period_note` | STRING | Categorical | Context label for conflict years |
| `wb_source` | STRING | Metadata | Always `world_bank` |
| `wb_ingested_at` | TIMESTAMP | Metadata | Last pipeline run timestamp |

> *UNHCR columns reserved for Phase 2 — currently `null`

> **On null values:** Nulls are real data gaps, not errors. The World Bank did not publish data for Libya during conflict years — particularly **2011** (revolution) and **2014–2016** (second civil war). Do not replace nulls with zero.

---

## ◈ Data Quality Tests

<details>
<summary><b>▶ See all 13 tests</b></summary>

| # | Test | Model | Type |
|:---:|:---|:---:|:---:|
| 1 | `year` is not null | stg_worldbank | Generic |
| 2 | `year` is unique | stg_worldbank | Generic |
| 3 | `year` between 2000 and 2023 | stg_worldbank | dbt_utils |
| 4 | `country_code` is not null | stg_worldbank | Generic |
| 5 | `country_code` = 'LY' only | stg_worldbank | Generic |
| 6 | `country_name` is not null | stg_worldbank | Generic |
| 7 | `source` is not null | stg_worldbank | Generic |
| 8 | `source` = 'world_bank' only | stg_worldbank | Generic |
| 9 | `ingested_at` is not null | stg_worldbank | Generic |
| 10 | `year` is not null | fact_libya_yearly_metrics | Generic |
| 11 | `year` is unique | fact_libya_yearly_metrics | Generic |
| 12 | `year` unique combination | fact_libya_yearly_metrics | dbt_utils |
| 13 | `population_total` > 0 when not null | fact_libya_yearly_metrics | Custom |

</details>

---

## ◈ Project Structure

```
libya-open-data-platform/
│
├── 📂 .github/workflows/
│   └── pipeline.yml                    ← Full automation (Monday 06:00 UTC)
│
├── 📂 ingestion/
│   ├── extract_worldbank.py            ← Pulls 5 indicators from World Bank API
│   ├── load_to_bigquery.py             ← Loads DataFrame → BigQuery raw layer
│   ├── export_to_csv.py                ← Exports mart table → /data CSV
│   └── utils.py                        ← BQ client, logger, env loader
│
├── 📂 dbt_libya/
│   ├── 📂 models/
│   │   ├── sources.yml                 ← Declares raw tables as dbt sources
│   │   ├── 📂 staging/
│   │   │   ├── stg_worldbank.sql       ← Cleans raw data (BigQuery view)
│   │   │   └── schema.yml             ← Docs + 9 tests
│   │   └── 📂 mart/
│   │       ├── fact_libya_yearly_metrics.sql  ← Final analytics table
│   │       └── schema.yml             ← Docs + 4 tests
│   ├── 📂 tests/
│   │   ├── assert_population_positive.sql
│   │   └── assert_gdp_positive.sql
│   ├── 📂 macros/
│   │   └── generate_schema_name.sql   ← Schema routing override
│   └── dbt_project.yml
│
├── 📂 data/
│   ├── fact_libya_yearly_metrics.csv  ← ✦ Public dataset (auto-updated weekly)
│   └── README.md
│
├── 📂 docs/
│   └── data_dictionary.md
│
├── DISCLAIMER.md
├── LICENSE                            ← CC BY 4.0
├── requirements.txt
└── README.md
```

---

## ◈ Run It Yourself

```bash
# 1 — Clone and set up
git clone https://github.com/ahmedmajid22/libya-open-data-platform.git
cd libya-open-data-platform
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2 — Add your GCP credentials to .env
echo "GCP_PROJECT_ID=your-project-id" >> .env
echo "BQ_DATASET_RAW=raw" >> .env
echo "BQ_DATASET_MART=mart" >> .env
echo "GOOGLE_APPLICATION_CREDENTIALS=gcp_key.json" >> .env

# 3 — Run the full pipeline
python -m ingestion.load_to_bigquery         # Extract + Load
cd dbt_libya && dbt deps && dbt run          # Transform
dbt test                                     # Validate
cd .. && python -m ingestion.export_to_csv   # Export
```

---

## ◈ Roadmap

- [x] World Bank ingestion pipeline
- [x] BigQuery 3-layer architecture (raw → staging → mart)
- [x] dbt transformation with full documentation
- [x] 13 automated data quality tests
- [x] GitHub Actions weekly automation
- [x] Public CSV with auto-commit
- [x] Looker Studio dashboard
- [ ] UNHCR refugee and displacement data
- [ ] Public REST API endpoint
- [ ] Data versioning and changelog
- [ ] Expanded source coverage

---

## ◈ License & Attribution

Released under **[Creative Commons Attribution 4.0 (CC BY 4.0)](LICENSE)** — free to use, share, and adapt for any purpose with attribution.

Underlying data © [World Bank Open Data](https://data.worldbank.org) · [UNHCR](https://www.unhcr.org/refugee-statistics) — both CC BY 4.0.

See [`DISCLAIMER.md`](DISCLAIMER.md) for full source notes.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f3460,50:16213e,100:1a1a2e&height=120&section=footer&animation=fadeIn" width="100%"/>

*Built to make data about Libya accessible — open, clean, and always up to date.*

**[⭐ Star this repo](https://github.com/ahmedmajid22/libya-open-data-platform) · [📥 Download the data](data/fact_libya_yearly_metrics.csv) · [📊 Open the dashboard](https://datastudio.google.com/reporting/ca23d690-a8b4-4506-8a39-f980855fd765)**

</div>