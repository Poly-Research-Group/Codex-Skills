-- Repository event activity context from GH Archive.
-- Parameterize @repo_full_name, @start_ts, @end_ts, @start_yyyymm, @end_yyyymm.

SELECT
  repo.name AS repo_full_name,
  DATE(created_at) AS event_date,
  type AS event_type,
  COUNT(*) AS n_events,
  COUNT(DISTINCT actor.login) AS n_distinct_actors
FROM `githubarchive.month.*`
WHERE _TABLE_SUFFIX BETWEEN @start_yyyymm AND @end_yyyymm
  AND created_at BETWEEN TIMESTAMP(@start_ts) AND TIMESTAMP(@end_ts)
  AND repo.name = @repo_full_name
GROUP BY repo_full_name, event_date, event_type;
