-- Diagnostic query templates.

-- Duplicate unit-time rows:
-- SELECT unit_id, time_id, COUNT(*) AS n
-- FROM analysis.analysis_ready
-- GROUP BY unit_id, time_id
-- HAVING COUNT(*) > 1;

-- Missingness by treatment status:
-- SELECT treatment,
--        COUNT(*) AS n,
--        SUM(CASE WHEN outcome IS NULL THEN 1 ELSE 0 END) AS missing_outcome,
--        AVG(CASE WHEN outcome IS NULL THEN 1.0 ELSE 0.0 END) AS missing_outcome_rate
-- FROM analysis.analysis_ready
-- GROUP BY treatment;

-- Within-unit variation for key variables:
-- SELECT unit_id,
--        MIN(key_independent_variable) AS min_key_iv,
--        MAX(key_independent_variable) AS max_key_iv,
--        COUNT(DISTINCT key_independent_variable) AS n_distinct_key_iv
-- FROM analysis.analysis_ready
-- GROUP BY unit_id;
