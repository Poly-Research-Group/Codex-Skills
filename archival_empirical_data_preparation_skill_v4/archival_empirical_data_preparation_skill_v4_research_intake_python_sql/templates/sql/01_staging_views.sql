-- Source-specific cleaning views.
-- Replace raw.source_table names and variable names with project-specific logic.

-- Example pattern:
-- CREATE OR REPLACE VIEW clean.source_table_clean AS
-- SELECT
--     lower(trim(original_id)) AS unit_id,
--     CAST(date_string AS DATE) AS time_id,
--     CAST(metric AS DOUBLE) AS metric,
--     * EXCLUDE (original_id, date_string, metric)
-- FROM raw.source_table;

-- Required checks after each clean view:
-- 1. Key missingness.
-- 2. Duplicate candidate keys.
-- 3. Impossible values.
-- 4. Date coverage.
