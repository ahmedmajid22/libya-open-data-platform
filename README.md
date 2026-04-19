# 🇱🇾 Libya Open Data Platform
![Pipeline Status](https://github.com/ahmedmajid22/libya-open-data-platform/actions/workflows/pipeline.yml/badge.svg)

An automated data pipeline that collects, transforms, and publishes open data about Libya.

## What This Does
- Extracts data from the World Bank API every Monday
- Transforms it using dbt (staging + mart layers)
- Runs 13 automated data quality tests
- Publishes a clean CSV to this repository

## Data
The public dataset is available in the `/data` folder:
- [fact_libya_yearly_metrics.csv](data/fact_libya_yearly_metrics.csv)

**Direct download URL:**
https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv

## Stack
- **Ingestion:** Python + World Bank API
- **Warehouse:** Google BigQuery
- **Transformation:** dbt (staging + mart)
- **Automation:** GitHub Actions (weekly)
- **Data:** World Bank Open Data, UNHCR (Phase 2)

## Project Structure
libya-open-data-platform/
├── ingestion/          # Python scripts to extract and load data
├── dbt_libya/          # dbt models, tests, and documentation
├── data/               # Public CSV exports
├── docs/               # Data dictionary and documentation
└── .github/workflows/  # Automated pipeline
