-- 01_unit_time_key_checks.sql
-- Check unit-time uniqueness. Replace unit_id/time_id as needed.

SELECT unit_id, time_id, COUNT(*) AS n_rows
FROM analysis_table
GROUP BY unit_id, time_id
HAVING COUNT(*) > 1
ORDER BY n_rows DESC
LIMIT 100;

SELECT
  COUNT(*) AS n_observations,
  COUNT(DISTINCT unit_id || '|' || time_id) AS n_unique_unit_time_keys
FROM analysis_table;
