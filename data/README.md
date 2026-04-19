# 🇱🇾 Libya Open Dataset

Updated automatically every Monday via GitHub Actions.

## Download

**Direct file:** [fact_libya_yearly_metrics.csv](fact_libya_yearly_metrics.csv)

**Raw URL (use in Python, Excel, R):**
https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv

## Data Dictionary

| Column | Type | Description | Source |
|---|---|---|---|
| `year` | Integer | Reference year (2000–2023) | All sources |
| `population_total` | Float | Total population of Libya | World Bank |
| `gdp_usd` | Float | GDP in current US dollars | World Bank |
| `gdp_per_capita_usd` | Float | GDP per capita in current USD | World Bank |
| `unemployment_rate` | Float | Unemployment % of labor force | World Bank |
| `inflation_rate` | Float | Annual consumer price inflation % | World Bank |
| `refugees_from_libya` | Float | People who fled Libya | UNHCR — Phase 2 |
| `asylum_seekers_count` | Float | Asylum seekers from Libya | UNHCR — Phase 2 |
| `gdp_per_person_calculated` | Float | Derived: GDP divided by population | Calculated |
| `population_yoy_change` | Float | Population change vs prior year | Calculated |
| `gdp_yoy_change_usd` | Float | GDP change vs prior year in USD | Calculated |
| `conflict_period_note` | String | Conflict period label for context | Categorical |
| `wb_source` | String | Source identifier | Metadata |
| `wb_ingested_at` | Timestamp | Last pipeline run timestamp | Metadata |

## Notes on Missing Values

Null values reflect genuine gaps in World Bank reporting during conflict periods:
- **2011**: Revolution — economic data partially unavailable
- **2014–2016**: Second civil war — some indicators unreported

Do not treat nulls as zero.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0)
