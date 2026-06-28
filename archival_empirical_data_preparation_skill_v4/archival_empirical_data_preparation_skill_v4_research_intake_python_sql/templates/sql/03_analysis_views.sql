-- Analysis views for constructed base samples, event-time variables, and lags/leads.

-- Example panel lag construction:
-- CREATE OR REPLACE VIEW analysis.analysis_base_with_lags AS
-- SELECT
--     *,
--     LAG(outcome, 1) OVER (PARTITION BY unit_id ORDER BY time_id) AS outcome_lag1,
--     LAG(key_independent_variable, 1) OVER (PARTITION BY unit_id ORDER BY time_id) AS key_iv_lag1
-- FROM analysis.analysis_base;

-- Example event-time construction:
-- CREATE OR REPLACE VIEW analysis.event_time_panel AS
-- SELECT
--     *,
--     date_diff('day', event_date, time_id) AS event_time,
--     CASE WHEN time_id >= event_date THEN 1 ELSE 0 END AS post_event
-- FROM analysis.analysis_base;

-- Default placeholder: if analysis.analysis_base exists, expose it as analysis.analysis_ready_candidate.
-- CREATE OR REPLACE VIEW analysis.analysis_ready_candidate AS SELECT * FROM analysis.analysis_base;
