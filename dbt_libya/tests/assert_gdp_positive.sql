/*
assert_gdp_positive.sql
Custom dbt test: GDP in USD must be positive when it is not null.

A zero or negative GDP value is not physically meaningful for this dataset.
If this test returns any rows, it means something went wrong in the source
data or the transformation pipeline.

How dbt tests work:
  - This query returns rows that FAIL the test condition.
  - If the query returns 0 rows → test PASSES (green in dbt test output).
  - If the query returns any rows → test FAILS (red in dbt test output).
*/

SELECT
    year,
    gdp_usd
FROM {{ ref('fact_libya_yearly_metrics') }}
WHERE
    gdp_usd IS NOT NULL
    AND gdp_usd <= 0