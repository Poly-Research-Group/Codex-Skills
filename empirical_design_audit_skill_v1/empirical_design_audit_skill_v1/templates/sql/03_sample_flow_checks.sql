-- 03_sample_flow_checks.sql
-- Build project-specific sample-flow checks by applying each restriction in order.
-- Example skeleton:

SELECT 'raw_analysis_table' AS step, COUNT(*) AS n_observations, COUNT(DISTINCT unit_id) AS n_units
FROM analysis_table
UNION ALL
SELECT 'nonmissing_key_variables' AS step, COUNT(*) AS n_observations, COUNT(DISTINCT unit_id) AS n_units
FROM analysis_table
WHERE dv IS NOT NULL AND main_iv IS NOT NULL;
