/*
assert_population_positive.sql
Custom dbt test: population must be positive when not null.

A negative or zero population is physically impossible.
If this test fails, something is wrong with the source data or transformation.

dbt tests work by returning rows that FAIL the test.
An empty result (0 rows) means the test PASSES.
*/

SELECT
    year,
    population_total
FROM {{ ref('fact_libya_yearly_metrics') }}
WHERE
    population_total IS NOT NULL
    AND population_total <= 0