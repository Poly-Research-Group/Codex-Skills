-- Exact @copilot invocation discovery.
-- Parameterize @start_yyyymm, @end_yyyymm, @start_ts, @end_ts.

SELECT
  created_at AS candidate_event_time_utc,
  type AS event_type,
  repo.name AS repo_full_name,
  actor.login AS human_invoker_login,
  JSON_VALUE(payload, '$.issue.html_url') AS issue_or_pr_url,
  SAFE_CAST(JSON_VALUE(payload, '$.issue.number') AS INT64) AS issue_or_pr_number,
  JSON_VALUE(payload, '$.comment.html_url') AS comment_url,
  JSON_VALUE(payload, '$.comment.body') AS comment_body,
  'exact_invocation_candidate' AS candidate_signal_family,
  TO_JSON_STRING(payload) AS payload_json
FROM `githubarchive.month.*`
WHERE _TABLE_SUFFIX BETWEEN @start_yyyymm AND @end_yyyymm
  AND created_at BETWEEN TIMESTAMP(@start_ts) AND TIMESTAMP(@end_ts)
  AND type IN ('IssueCommentEvent', 'PullRequestReviewCommentEvent')
  AND REGEXP_CONTAINS(
    LOWER(JSON_VALUE(payload, '$.comment.body')),
    r'(^|[^a-z0-9_-])@copilot([^a-z0-9_-]|$)'
  );
