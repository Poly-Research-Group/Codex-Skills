-- 02_treatment_event_checks.sql
-- Binary treatment variation and timing support. Replace variable names.

SELECT treatment, COUNT(*) AS n_observations
FROM analysis_table
GROUP BY treatment
ORDER BY treatment;

SELECT treatment_time, COUNT(DISTINCT unit_id) AS n_units, COUNT(*) AS n_observations
FROM analysis_table
WHERE treatment = 1
GROUP BY treatment_time
ORDER BY treatment_time;
