-- Repository star/watch event history from GH Archive.
-- Parameterize @repo_full_name, @start_ts, @end_ts, @start_yyyymm, @end_yyyymm.

SELECT
  repo.name AS repo_full_name,
  DATE(created_at) AS event_date,
  COUNT(*) AS n_watch_events
FROM `githubarchive.month.*`
WHERE _TABLE_SUFFIX BETWEEN @start_yyyymm AND @end_yyyymm
  AND created_at BETWEEN TIMESTAMP(@start_ts) AND TIMESTAMP(@end_ts)
  AND repo.name = @repo_full_name
  AND type = 'WatchEvent'
GROUP BY repo_full_name, event_date;
