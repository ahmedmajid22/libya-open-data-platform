# How to Use the Libya Open Dataset

The data is publicly available with no signup, no API key, and no download
required. Pick the method that fits your tool.

---

## Method 1 — Python (pandas)

This loads the latest data directly from GitHub into a pandas DataFrame.
The data refreshes automatically every Monday — you always get the latest version.

```python
import pandas as pd

# Load directly from GitHub — no download needed
URL = "https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv"

df = pd.read_csv(URL)

# See all columns
print(df.columns.tolist())

# See first 5 rows
print(df.head())

# Filter to a specific year
year_2020 = df[df['year'] == 2020]
print(year_2020[['year', 'population_total', 'gdp_usd', 'unemployment_rate']])

# Filter to conflict years only
conflict = df[df['conflict_period_note'].notna()]
print(conflict[['year', 'conflict_period_note', 'gdp_usd']])
```

### Plot population over time

```python
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv"
df = pd.read_csv(URL)

df_sorted = df.sort_values('year')

plt.figure(figsize=(12, 5))
plt.plot(df_sorted['year'], df_sorted['population_total'] / 1_000_000,
         marker='o', linewidth=2, color='#2563EB')
plt.title('Libya Population (2000–2023)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Population (millions)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Plot GDP and unemployment together

```python
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv"
df = pd.read_csv(URL).sort_values('year')

fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.bar(df['year'], df['gdp_usd'] / 1e9, color='#3B82F6', alpha=0.7, label='GDP (billions USD)')
ax1.set_xlabel('Year')
ax1.set_ylabel('GDP (billions USD)', color='#3B82F6')

ax2 = ax1.twinx()
ax2.plot(df['year'], df['unemployment_rate'], color='#EF4444',
         marker='o', linewidth=2, label='Unemployment (%)')
ax2.set_ylabel('Unemployment Rate (%)', color='#EF4444')

plt.title('Libya GDP and Unemployment Rate (2000–2023)')
plt.tight_layout()
plt.show()
```

---

## Method 2 — Excel (no code required)

This method loads live data directly from GitHub into Excel.
Every time you click Refresh, you get the latest data.

**Steps:**
1. Open Microsoft Excel (2016 or later)
2. Click the **Data** tab in the ribbon
3. Click **From Web** (in the Get & Transform Data section)
4. A dialog box appears asking for a URL. Paste this URL:

---

## Method 3 — R

```r
library(readr)
library(dplyr)
library(ggplot2)

url <- "https://raw.githubusercontent.com/ahmedmajid22/libya-open-data-platform/main/data/fact_libya_yearly_metrics.csv"

df <- read_csv(url)

# View structure
glimpse(df)

# Plot population
df %>%
  filter(!is.na(population_total)) %>%
  ggplot(aes(x = year, y = population_total / 1e6)) +
  geom_line(color = "steelblue", size = 1) +
  geom_point(color = "steelblue") +
  labs(title = "Libya Population (2000-2023)",
       x = "Year",
       y = "Population (millions)") +
  theme_minimal()
```

---

## Method 4 — Direct CSV Download

Click the link below to download the latest version as a file:

[📥 Download fact_libya_yearly_metrics.csv](data/fact_libya_yearly_metrics.csv)

Or right-click → Save Link As on the **Raw** button in GitHub.

---

## Column Reference

| Column | What it means |
|---|---|
| `year` | The year (2000–2023) |
| `population_total` | Total population of Libya that year |
| `gdp_usd` | Total GDP in current US dollars |
| `gdp_per_capita_usd` | GDP divided by population (World Bank official) |
| `unemployment_rate` | % of labor force that is unemployed |
| `inflation_rate` | Annual consumer price inflation % |
| `refugees_from_libya` | People who fled Libya (Phase 2 — currently null) |
| `asylum_seekers_count` | Asylum seekers from Libya (Phase 2 — currently null) |
| `gdp_per_person_calculated` | Our own GDP ÷ population calculation |
| `population_yoy_change` | Population change compared to the prior year |
| `gdp_yoy_change_usd` | GDP change in USD compared to the prior year |
| `conflict_period_note` | Label for conflict years (2011, 2014–2019) |
| `wb_source` | Source identifier (always 'world_bank' currently) |
| `wb_ingested_at` | When this data was last updated by the pipeline |

---

## Notes on Missing Values

Some years have `null` values — this is **not an error**.
It reflects genuine gaps in World Bank reporting during conflict periods:

- **2011**: Revolution — economic data partially unavailable
- **2014–2016**: Second civil war — some indicators unreported

**Do not replace nulls with zero.** Zero has a different meaning.
In your analysis, handle nulls explicitly with `dropna()` in Python
or `na.rm = TRUE` in R.

---

## License

This dataset is released under **CC BY 4.0**.
Free to use, share, and adapt — just credit the source.

**Citation:**
> Libya Open Data Platform. (2024). Libya Yearly Metrics Dataset.
> GitHub. https://github.com/ahmedmajid22/libya-open-data-platform