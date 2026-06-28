-- 00_basic_counts.sql
-- Replace analysis_table with the prepared analysis table or view.

SELECT COUNT(*) AS n_observations FROM analysis_table;

-- Counts by unit and time, if applicable.
SELECT COUNT(DISTINCT unit_id) AS n_units FROM analysis_table;
SELECT COUNT(DISTINCT time_id) AS n_time_periods FROM analysis_table;
