-- 04_balance_pretrend_support_checks.sql
-- Descriptive support for DID/event-study readiness. This is not a hypothesis test.
-- Replace treated, relative_time, and dv.

SELECT treated, relative_time,
       COUNT(*) AS n_observations,
       AVG(dv) AS mean_outcome
FROM analysis_table
WHERE relative_time < 0
GROUP BY treated, relative_time
ORDER BY relative_time, treated;
