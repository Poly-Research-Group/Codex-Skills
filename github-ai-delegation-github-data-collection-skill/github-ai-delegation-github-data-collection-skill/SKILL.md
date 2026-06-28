---
name: github-ai-delegation-github-data-collection
description: Build and execute a reproducible public GitHub data collection pipeline for a research project on visible AI delegation in collaborative software work. Use this skill only for GitHub data discovery, hydration, trace extraction, data-quality validation, and export. Do not conduct causal analysis, statistical modeling, final matching, or substantive inference.
---

# GitHub AI Delegation Data Collection Skill

## 1. Scope Boundary

This skill is restricted to **GitHub data collection and data preparation** for a research project on visible AI delegation in collaborative software tasks.

The skill should help Codex build a reproducible pipeline that discovers, hydrates, validates, and exports public GitHub data related to AI delegation traces. The pipeline may create descriptive data-quality summaries, variable coverage reports, and codebooks. It must not estimate treatment effects, run causal models, produce final matched samples, interpret results, or draw substantive conclusions.

### 1.1 What the skill should do

- Collect public GitHub archival data.
- Discover candidate AI-delegated GitHub episodes.
- Hydrate GitHub objects through the GitHub API.
- Preserve raw JSON for reproducibility.
- Normalize raw data into structured Parquet tables.
- Extract visible AI delegation trace flags.
- Reconstruct event sequences within issues and pull requests.
- Collect repository, contributor, reviewer, dyad, task, and file-context variables for later analysis.
- Generate validation reports, manual-audit files, data inventories, and codebooks.
- Stop at predefined human approval gates.

### 1.2 What the skill should not do

- Do not collect private repositories, private organization telemetry, private Copilot usage metrics, or non-public user data.
- Do not infer hidden IDE-level AI assistance as observed treatment.
- Do not use non-GitHub data sources unless the user explicitly instructs otherwise.
- Do not run regression models, causal inference models, propensity-score matching, difference-in-differences, event studies, survival models, or hypothesis tests.
- Do not label empirical findings as reputational effects.
- Do not produce final analysis tables that require econometric design decisions.
- Do not use LLMs to infer sensitive personal attributes.
- Do not identify real-world identities behind GitHub accounts.

The correct deliverable is an **analysis-ready GitHub data collection package**, not an empirical findings report.

## 2. Core Collection Construct

The central collection construct is **visible AI delegation**: a public GitHub trace showing that a human contributor delegates work to an AI actor, invokes an AI actor, or that an AI actor visibly participates in a collaborative production episode.

The pipeline should treat the following as public trace evidence:

- An AI actor or AI app appears as a PR author, commit author, committer, reviewer, commenter, assignee, or timeline actor.
- A human publicly invokes an AI actor in an issue, pull request, review comment, or related discussion.
- A repository contains AI instruction/configuration files that plausibly enable AI-agent work.
- A contributor self-discloses AI assistance in PR text, commit messages, or comments.
- A reviewer or collaborator attributes a contribution to AI.

The pipeline should not claim to observe:

- Hidden Copilot autocompletions.
- Private ChatGPT/Cursor/Claude/Codex use outside GitHub.
- Undisclosed local AI assistance.
- Organization-level Copilot telemetry unless the user separately provides authorized data.

## 3. Main AI Delegation Trace Families

Use two high-precision trace families as the main collection targets.

### 3.1 Platform-attributed AI traces

Collect episodes in which GitHub metadata publicly attributes activity to a likely AI actor, AI app, or AI-related account. Examples include:

- AI-authored PR.
- AI-authored commit.
- AI-authored review or comment.
- AI-related issue assignment.
- Timeline event or GitHub app metadata indicating an AI coding agent.
- Actor login or GitHub app slug/name matching a manually validated AI coding agent dictionary.

Platform-attributed traces are high precision only after actor/app validation. Candidate actor names should never be hard-coded as ground truth without manual audit.

### 3.2 Invocation traces

Collect episodes in which a human publicly invokes an AI actor. The most important main-sample signal is exact `@copilot` invocation in issue/PR/review contexts, followed by subsequent AI actor activity in the same episode.

A main invocation trace should satisfy:

```text
human_public_invocation == 1
AND exact_invocation_pattern == 1
AND subsequent_ai_activity_in_same_episode == 1
```

The strictest baseline should prioritize exact invocation patterns such as:

```text
(?i)(?<![\w-])@copilot(?![\w-])
```

Broader mentions such as “copilot,” “AI,” “ChatGPT,” or “Claude” should be collected as robustness or weak-signal candidates, not as baseline visible delegation.

## 4. Robustness and Mechanism Trace Families to Collect

Collect these traces for later robustness, descriptive, or mechanism work. Do not make them the default main treatment unless the user explicitly approves.

### 4.1 Self-disclosure traces

Search PR bodies, issue bodies, comments, review comments, and commit messages for phrases such as:

- `generated with Copilot`
- `AI-generated`
- `LLM-assisted`
- `generated by ChatGPT`
- `Claude Code`
- `Cursor`
- `Devin`
- `Codex`

### 4.2 Coauthorship traces

Collect commit-message trailers such as:

```text
Co-authored-by: ... copilot ...
Co-authored-by: ... codex ...
Co-authored-by: ... claude ...
Co-authored-by: ... devin ...
```

### 4.3 Reviewer attribution traces

Collect reviewer or collaborator comments that indicate perceived AI involvement, for example:

- `this looks AI-generated`
- `please do not use AI-generated code`
- `Copilot introduced this bug`
- `LLM-generated`
- `AI slop`

These traces are important because they reveal visible interpretation by collaborators. They should be collected without interpreting tone or reputation unless a later analysis stage is explicitly requested.

### 4.4 Repository AI-readiness traces

Collect whether the repository contains AI-agent instruction/configuration files such as:

- `.github/copilot-instructions.md`
- `.github/instructions/*.instructions.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.cursorrules`
- `.cursor/rules/*`
- `GEMINI.md`
- `.github/dependabot.yml` only as conventional automation context, not AI delegation.

Repository AI-readiness should be treated as contextual collection data, not proof that any specific PR used AI.

## 5. Primary Collection Units

The pipeline should collect data at several linked levels.

### 5.1 Pull request episode

A PR episode is the main collection unit. It links:

- Repository metadata.
- Pull request metadata.
- Linked issue metadata when available.
- PR commits.
- Changed files.
- PR reviews.
- PR review comments.
- Issue comments.
- Timeline events.
- Labels, assignees, requested reviewers, milestones.
- Actor metadata.
- Repository context snapshots.

### 5.2 Issue episode

An issue episode is collected when AI delegation begins in an issue and the PR is created later, or when an issue contains AI assignment/invocation without an immediately linked PR.

### 5.3 Event sequence

An event sequence orders all relevant events within an episode by timestamp and classifies each actor as:

- human
- validated AI actor/app
- conventional automation bot
- unknown

### 5.4 Repository context snapshot

A repository context snapshot is collected at or before the focal episode time and includes repository maturity, governance, activity, automation, AI-readiness, language profile, and recent collaboration volume.

### 5.5 Actor snapshot

An actor snapshot captures public GitHub profile metadata available through the API. Mark these as current snapshots unless historical values are reconstructed from event history.

## 6. Approved Data Sources

Use GitHub public data sources only.

### 6.1 GH Archive / BigQuery

Use GH Archive as the large-scale candidate discovery layer. It is useful for public GitHub event discovery across time, repositories, actors, and event types.

Primary event types to scan:

```text
PullRequestEvent
IssuesEvent
IssueCommentEvent
PullRequestReviewEvent
PullRequestReviewCommentEvent
PushEvent
WatchEvent
ForkEvent
CreateEvent
```

Use GH Archive primarily to produce a normalized candidate list. Do not rely on GH Archive payloads alone for final episode records because detailed hydration through the GitHub API is needed.

### 6.2 GitHub REST API

Use GitHub REST API to hydrate detailed objects:

```text
GET /repos/{owner}/{repo}
GET /repos/{owner}/{repo}/languages
GET /repos/{owner}/{repo}/contributors
GET /repos/{owner}/{repo}/pulls/{pull_number}
GET /repos/{owner}/{repo}/pulls/{pull_number}/commits
GET /repos/{owner}/{repo}/pulls/{pull_number}/files
GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews
GET /repos/{owner}/{repo}/pulls/{pull_number}/comments
GET /repos/{owner}/{repo}/issues/{issue_number}
GET /repos/{owner}/{repo}/issues/{issue_number}/comments
GET /repos/{owner}/{repo}/issues/{issue_number}/timeline
GET /repos/{owner}/{repo}/commits/{sha}
GET /repos/{owner}/{repo}/contents/{path}
GET /users/{username}
```

Use pagination, rate-limit handling, retries, and raw JSON preservation.

### 6.3 GitHub GraphQL API

Use GraphQL only when it materially reduces hydration cost or retrieves fields not easily available through REST. Keep GraphQL queries versioned and saved in the repository.

### 6.4 GitHub Search API

Use GitHub Search API only for targeted query expansion, such as exact `@copilot` mentions, self-disclosure phrases, or reviewer-attribution phrases. Search API results should be hydrated through REST before entering the processed dataset.

## 7. Human Approval Gates

Codex must not proceed from one major collection stage to the next without producing the required checkpoint report and receiving explicit user approval.

### Gate 0: Configuration Approval

Before any collection, produce `reports/gate0_configuration_summary.md` with:

- Date range.
- Repository filters.
- Candidate trace definitions.
- Exact invocation regexes.
- Broad robustness regexes.
- AI actor candidate patterns.
- Conventional bot exclusion patterns.
- Data sources to be used.
- Expected credentials and environment variables.
- Expected output folders.

Stop and ask for approval.

### Gate 1: Candidate Discovery Approval

After GH Archive/Search candidate discovery, produce `reports/gate1_candidate_discovery.md` with:

- Candidate counts by signal family.
- Candidate counts by event type.
- Candidate counts by month.
- Candidate counts by repository.
- Candidate counts by actor/app pattern.
- Duplicate rate.
- Sample candidate URLs.
- Example payload snippets with sensitive content minimized.
- Estimated hydration volume.

Stop and ask for approval before hydration.

### Gate 2: Actor Dictionary Approval

After candidate actor extraction, produce:

```text
reports/gate2_actor_dictionary.md
data/interim/actor_dictionary_audit.parquet
```

The report must list candidate AI actors/apps and proposed labels:

- validated AI actor/app
- conventional bot
- human
- unknown
- needs manual review

For each actor/app include event counts, repositories, matched pattern, raw metadata, and example URLs.

Stop and ask for approval before final AI actor labeling.

### Gate 3: Pilot Hydration Approval

After pilot hydration, produce `reports/gate3_pilot_hydration.md` with:

- Number of candidates attempted.
- Number hydrated successfully.
- Number unavailable, deleted, private, or API-denied.
- API error categories.
- Rate-limit statistics.
- Raw JSON completeness.
- Table row counts.
- Example hydrated PR episodes.

Stop and ask for approval before deriving pilot trace flags.

### Gate 4: Trace Validation Approval

After deriving pilot trace flags and manual-audit samples, produce:

```text
reports/gate4_trace_validation.md
data/interim/manual_audit_main_positives.csv
data/interim/manual_audit_weak_positives.csv
data/interim/manual_audit_candidate_negatives.csv
```

The report must include:

- Counts of strict platform-attributed AI traces.
- Counts of strict invocation traces.
- Counts of self-disclosure traces.
- Counts of coauthorship traces.
- Counts of reviewer-attribution traces.
- Counts of repository AI-readiness traces.
- Manual precision estimate by trace family.
- False-positive categories.
- False-negative risks.
- Recommended refinements to regexes or actor labels.

Stop and ask for approval before scaling collection.

### Gate 5: Collection Coverage Approval

After pilot collection covariate construction, produce `reports/gate5_collection_coverage.md` with:

- Coverage and missingness for repository variables.
- Coverage and missingness for PR/task variables.
- Coverage and missingness for contributor variables.
- Coverage and missingness for reviewer variables.
- Coverage and missingness for dyad history variables.
- Coverage and missingness for file-context variables.
- Availability of non-AI neighboring PR episodes in the same repositories/time windows.
- Storage and runtime estimates for full collection.

Stop and ask for approval before full-scale collection.

### Gate 6: Full Collection Approval

Before full-scale collection, produce `reports/gate6_full_collection_plan.md` with:

- Final date range.
- Final query slices.
- Expected number of repositories, PRs, issues, comments, reviews, commits, and files.
- Expected API requests.
- Expected BigQuery usage.
- Expected storage volume.
- Estimated runtime.
- Restart/resume plan.
- Failure-handling plan.

Stop and ask for approval.

### Gate 7: Final Collection Package Approval

After full collection and validation, produce:

```text
reports/gate7_final_collection_report.md
reports/data_dictionary.md
reports/raw_data_inventory.md
reports/processed_data_inventory.md
```

The final report must summarize:

- Final sample counts.
- Hydration success rates.
- Trace counts by family.
- Actor classification status.
- Manual validation results.
- Missingness by table.
- Known data limitations.
- Analysis-ready table inventory.
- Variables requiring caution because they are current snapshots or potentially post-treatment.

Stop. Do not proceed to modeling or causal analysis.

## 8. Required Project Structure

Codex should create this project structure:

```text
github_ai_delegation_collection/
  README.md
  requirements.txt
  .env.example
  config/
    sample_params.yml
    api.yml
    search_terms.yml
    ai_actor_dictionary.yml
    collection_tables.yml
  sql/
    gharchive_candidate_discovery.sql
    gharchive_invocation_discovery.sql
    gharchive_repo_event_context.sql
    gharchive_star_history.sql
  src/
    __init__.py
    config.py
    logging_utils.py
    github_client.py
    gharchive_client.py
    search_github.py
    discover_candidates.py
    hydrate_github_objects.py
    collect_repository_context.py
    collect_neighbor_pr_episodes.py
    derive_trace_flags.py
    derive_event_sequences.py
    derive_collection_covariates.py
    validate_collection.py
    export_codebook.py
  data/
    raw/
    interim/
    processed/
  reports/
  notebooks/
    01_pilot_collection_diagnostics.ipynb
  tests/
    test_url_parsing.py
    test_regex_traces.py
    test_actor_classification.py
    test_pagination.py
    test_temporal_snapshots.py
    test_idempotency.py
```

## 9. Configuration Files

### 9.1 config/sample_params.yml

```yaml
project_name: github_ai_delegation_collection
start_date: "2025-05-19"
end_date: "2026-06-30"
timezone: "UTC"

scope:
  github_public_data_only: true
  allow_private_repos: false
  allow_org_copilot_telemetry: false
  allow_non_github_sources: false
  allow_modeling_or_causal_analysis: false

repo_filters:
  min_stars_at_candidate_time: 50
  min_prs_prior_180d: 20
  exclude_forks: true
  exclude_archived: true
  exclude_empty_repos: true

candidate_windows:
  pre_context_days: 180
  post_context_days: 180
  neighbor_pr_window_days: 60

main_trace_rules:
  require_exact_invocation_for_main: true
  require_subsequent_ai_activity_after_invocation: true
  max_hours_after_invocation_for_ai_activity: 168
  require_manual_actor_validation_for_platform_ai: true

pilot:
  start_date: "2025-05-19"
  end_date: "2025-06-30"
  max_candidates_to_hydrate: 500
  manual_audit_main_positive_n: 200
  manual_audit_weak_positive_n: 200
  manual_audit_candidate_negative_n: 200

hydration:
  max_retries: 5
  sleep_seconds_between_requests: 0.25
  save_raw_json: true
  overwrite_existing: false

outputs:
  raw_format: "json"
  processed_format: "parquet"
  include_text_in_raw_only: true
```

### 9.2 config/search_terms.yml

```yaml
main_invocation_regex:
  - "(?i)(?<![\\w-])@copilot(?![\\w-])"

robust_invocation_regex:
  - "(?i)(?<![\\w-])@(copilot|codex|claude|devin)(?![\\w-])"

self_disclosure_regex:
  - "(?i)generated\\s+(by|with)\\s+(github\\s+)?copilot"
  - "(?i)(ai|llm)[-\\s]?generated"
  - "(?i)(ai|llm)[-\\s]?assisted"
  - "(?i)(chatgpt|gpt-4|gpt-5|claude|claude code|cursor|devin|codex)"

coauthor_regex:
  - "(?i)co-authored-by:.*(copilot|codex|claude|devin|cursor)"

reviewer_attribution_regex:
  - "(?i)this\\s+looks\\s+ai[-\\s]?generated"
  - "(?i)please\\s+do\\s+not\\s+use\\s+ai"
  - "(?i)(copilot|chatgpt|llm|ai)\\s+(introduced|caused|generated|wrote)"
  - "(?i)ai\\s+slop"

repo_ai_instruction_paths:
  - ".github/copilot-instructions.md"
  - "AGENTS.md"
  - "CLAUDE.md"
  - ".cursorrules"
  - "GEMINI.md"
```

### 9.3 config/ai_actor_dictionary.yml

```yaml
strict_actor_logins: []
strict_app_slugs: []

candidate_actor_login_patterns:
  - "(?i)copilot"
  - "(?i)codex"
  - "(?i)claude"
  - "(?i)devin"
  - "(?i)cursor"

candidate_app_slug_patterns:
  - "(?i)copilot"
  - "(?i)codex"
  - "(?i)claude"
  - "(?i)devin"
  - "(?i)cursor"

conventional_bot_exclusions:
  - "dependabot"
  - "renovate"
  - "github-actions"
  - "codecov"
  - "semantic-release"
  - "pre-commit-ci"
  - "snyk-bot"
  - "imgbot"

manual_review_required: true
```

### 9.4 config/api.yml

```yaml
github:
  api_version: "2022-11-28"
  token_env_var: "GITHUB_TOKEN"
  base_url: "https://api.github.com"
  user_agent: "github-ai-delegation-collection-research"
  per_page: 100
  respect_rate_limits: true
  retry_on_secondary_rate_limit: true

bigquery:
  project_env_var: "GOOGLE_CLOUD_PROJECT"
  credentials_env_var: "GOOGLE_APPLICATION_CREDENTIALS"
  gharchive_dataset: "githubarchive"
```

## 10. Candidate Discovery Requirements

### 10.1 Normalized candidate schema

Every discovered candidate must be normalized to:

```text
candidate_id
candidate_source
candidate_signal_family
candidate_signal_detail
repo_full_name
owner
repo
issue_number
pull_number
candidate_event_time_utc
candidate_actor_login
candidate_actor_type_raw
candidate_app_slug
candidate_comment_url
candidate_pr_url
candidate_issue_url
payload_hash
raw_payload_path
fetched_or_discovered_at_utc
```

### 10.2 Candidate signal families

Use these exact categories:

```text
platform_attributed_ai_candidate
exact_invocation_candidate
broad_invocation_candidate
self_disclosure_candidate
coauthor_candidate
reviewer_attribution_candidate
repo_ai_readiness_candidate
neighbor_non_ai_candidate
unknown_ai_related_candidate
```

### 10.3 GH Archive discovery logic

Use GH Archive to discover candidate events with:

- exact `@copilot` comments;
- AI-like actor/app patterns;
- PR authors or issue actors matching AI candidate patterns;
- self-disclosure text;
- reviewer-attribution text.

Codex should parameterize table suffixes, dates, event types, and regexes. Discovery should be deduplicated by repository, issue/PR number, candidate signal, and event timestamp.

### 10.4 GitHub Search discovery logic

Use GitHub Search only to supplement GH Archive when discovery counts are too low or when searching exact phrases in issue/PR text. Slice searches by:

- date range;
- repository or owner;
- language/topic if needed;
- query phrase.

All Search API results must be hydrated before inclusion in processed tables.

## 11. Hydration Requirements

### 11.1 Hydrate PR episode

For every candidate PR episode, collect:

```text
repository metadata
repository languages
repository contents for selected config files
pull request metadata
pull request commits
pull request changed files
pull request reviews
pull request review comments
issue metadata for the PR number
issue comments
issue timeline events
actor profiles for relevant public actors
```

### 11.2 Hydrate issue-only episode

For issue-only candidates, collect:

```text
repository metadata
issue metadata
issue comments
issue timeline events
linked PRs if identifiable from timeline/events/body references
actor profiles for relevant public actors
```

### 11.3 Collect neighboring non-AI PR episodes

For repositories with validated AI-delegation candidates, collect neighboring PR episodes from the same repository within the configured time window. These are data-collection candidates for later comparison. Do not match, weight, or select final controls.

For each neighboring PR, collect the same PR episode objects:

```text
PR metadata
commits
files
reviews
review comments
issue comments
timeline events
repository context snapshot
```

Label them as `neighbor_non_ai_candidate` only after trace extraction confirms no visible AI trace in collected objects.

## 12. Raw Data Preservation

Save raw JSON for every API call. Raw records should retain:

```text
run_id
source_endpoint
source_url
request_params_hash
fetched_at_utc
http_status
etag_if_available
rate_limit_remaining_if_available
raw_json_path
```

Never overwrite raw JSON unless `--force` is explicitly set.

## 13. Processed Data Tables

### 13.1 Raw-normalized tables

Create these normalized tables from raw JSON:

```text
raw_candidates.parquet
repositories.parquet
repository_languages.parquet
repository_config_files.parquet
pull_requests.parquet
issues.parquet
issue_comments.parquet
issue_timeline_events.parquet
pr_commits.parquet
pr_changed_files.parquet
pr_reviews.parquet
pr_review_comments.parquet
actor_profiles.parquet
api_call_log.parquet
```

### 13.2 Trace and sequence tables

Create:

```text
ai_trace_flags.parquet
actor_classification.parquet
episode_event_sequences.parquet
repo_ai_readiness.parquet
manual_audit_samples.parquet
```

### 13.3 Collection covariate snapshot tables

Create data snapshots for later analysis. These are not model controls yet; they are collected and temporally aligned covariates.

```text
repo_context_snapshots.parquet
pr_task_snapshots.parquet
contributor_context_snapshots.parquet
reviewer_context_snapshots.parquet
dyad_context_snapshots.parquet
file_context_snapshots.parquet
temporal_context_snapshots.parquet
neighbor_pr_episode_index.parquet
```

## 14. Trace Flag Construction

### 14.1 ai_trace_flags.parquet schema

```text
episode_id
repo_full_name
pull_number
issue_number
episode_type
platform_attributed_ai_candidate
platform_attributed_ai_validated
ai_actor_login
ai_app_slug
ai_authored_pr
ai_authored_commit
ai_commented_or_reviewed
issue_assigned_to_ai_candidate
issue_assigned_to_ai_validated
exact_human_invocation
human_invoker_login
human_invocation_time_utc
subsequent_ai_activity_in_same_episode
hours_to_subsequent_ai_activity
strict_main_trace
self_disclosure_trace
coauthor_trace
reviewer_attribution_trace
repo_ai_readiness_trace
broad_ai_mention_trace
trace_validation_status
trace_validation_notes
```

### 14.2 strict_main_trace rule

```text
strict_main_trace = 1 if:
  platform_attributed_ai_validated == 1
  OR
  (exact_human_invocation == 1 AND subsequent_ai_activity_in_same_episode == 1)
```

Keep separate flags for platform-attributed AI and invocation traces. The combined `strict_main_trace` is a collection convenience, not a final empirical treatment variable.

## 15. Actor Classification

### 15.1 Classification labels

Use these labels:

```text
validated_ai_actor
candidate_ai_actor
conventional_bot
human
unknown
needs_manual_review
```

### 15.2 Classification rules

Classify as `validated_ai_actor` only if:

- login is in manually approved `strict_actor_logins`; or
- GitHub app slug/name is in manually approved `strict_app_slugs`; or
- manual audit confirms the actor/app as AI.

Classify as `conventional_bot` if:

- login matches conventional automation bot exclusions; or
- event behavior and metadata clearly indicate dependency updates, CI, release automation, linting, code coverage, or deployment.

Classify as `human` if:

- GitHub type is `User`; and
- the actor does not match bot/AI patterns; and
- no evidence indicates automation.

Classify as `unknown` or `needs_manual_review` when ambiguous.

### 15.3 Actor audit table

Create `actor_classification.parquet` with:

```text
actor_login
actor_type_raw
actor_type_assigned
matched_pattern
app_slug
app_name
n_events
n_repos
example_urls
manual_review_status
manual_review_notes
classification_timestamp_utc
```

## 16. Event Sequence Collection

Create `episode_event_sequences.parquet` with one row per event:

```text
episode_id
repo_full_name
pull_number
issue_number
event_time_utc
event_order
event_type
source_table
source_object_id
actor_login
actor_classification
app_slug
event_action
body_text_present
body_text_hash
commit_sha
review_state
file_path_if_applicable
is_ai_related_event
is_human_invocation_event
is_subsequent_ai_activity_event
```

Compute descriptive sequence features only:

```text
n_events_total
n_human_events
n_validated_ai_events
n_conventional_bot_events
n_unknown_events
first_ai_event_time_utc
first_human_invocation_time_utc
human_ai_actor_type_alternations
ai_response_cycles_after_invocation
```

Do not interpret these as empirical mechanisms or effects at this stage.

## 17. Collection Covariate Snapshots

Construct temporally aligned snapshots for later research use. All snapshot variables should store `snapshot_time_utc` and `lookback_window_days`.

### 17.1 Repository context snapshots

Collect:

```text
repo_full_name
episode_id
snapshot_time_utc
repo_created_at
repo_age_days
owner_type
primary_language
language_entropy
license_key
is_fork
is_archived
is_template
stars_current_snapshot
forks_current_snapshot
watchers_current_snapshot
open_issues_current_snapshot
has_codeowners
has_contributing_guide
has_pr_template
has_issue_template
has_security_policy
has_ci_workflow
has_ai_instruction_file
prior_pr_count_30d
prior_pr_count_90d
prior_pr_count_180d
prior_issue_count_90d
prior_commit_count_90d
prior_distinct_contributors_90d
prior_visible_ai_trace_count_90d
prior_visible_ai_trace_share_90d
prior_bot_pr_share_90d
```

Mark current API values clearly as current snapshots unless reconstructed historically.

### 17.2 PR/task snapshots

Collect:

```text
episode_id
repo_full_name
pull_number
pr_created_at_utc
author_login
author_association
is_draft
linked_issue
issue_age_hours_before_pr
n_labels
label_text
has_milestone
n_assignees
n_requested_reviewers
base_branch
title_length
body_length
additions
deletions
changed_files
n_commits
n_directories_changed
file_extension_entropy
docs_file_share
test_file_share
config_file_share
source_code_file_share
dependency_file_share
contains_security_terms
contains_bug_terms
contains_feature_terms
contains_refactor_terms
contains_test_terms
contains_doc_terms
```

### 17.3 Contributor context snapshots

Collect pre-episode contributor history within the repository:

```text
episode_id
repo_full_name
contributor_login
snapshot_time_utc
contributor_account_created_at_current_snapshot
contributor_prior_prs_repo
contributor_prior_merged_prs_repo
contributor_prior_closed_unmerged_prs_repo
contributor_prior_issues_repo
contributor_prior_comments_repo
contributor_prior_reviews_received_repo
contributor_prior_commits_repo
contributor_repo_tenure_days
contributor_prior_file_overlap_count
contributor_prior_directory_overlap_count
contributor_prior_visible_ai_trace_count
contributor_prior_visible_ai_trace_share
contributor_current_followers_snapshot
contributor_current_public_repos_snapshot
```

### 17.4 Reviewer context snapshots

Collect reviewer metadata and prior repository behavior for human reviewers/commenters:

```text
episode_id
repo_full_name
reviewer_login
snapshot_time_utc
reviewer_prior_reviews_repo
reviewer_prior_approvals_repo
reviewer_prior_changes_requested_repo
reviewer_prior_comments_repo
reviewer_prior_review_latency_mean_repo
reviewer_recent_review_workload_7d
reviewer_recent_review_workload_30d
reviewer_prior_visible_ai_exposure_count
reviewer_is_member_or_collaborator_if_available
```

### 17.5 Dyad context snapshots

Collect prior relationship between contributor and reviewer/commenter:

```text
episode_id
repo_full_name
contributor_login
reviewer_login
snapshot_time_utc
dyad_prior_interactions
dyad_prior_reviews
dyad_prior_approvals
dyad_prior_changes_requested
dyad_prior_comments
dyad_prior_merges
dyad_time_since_last_interaction_days
dyad_same_file_history_count
dyad_same_directory_history_count
```

### 17.6 File context snapshots

Collect file-level context from changed files:

```text
episode_id
repo_full_name
pull_number
snapshot_time_utc
changed_file_count
prior_file_churn_mean_180d
prior_file_churn_max_180d
prior_file_contributor_count_mean_180d
prior_file_owner_concentration_mean_180d
prior_file_review_comment_count_mean_180d
touches_codeowners_file
touches_test_files
touches_docs_files
touches_config_files
touches_source_files
```

## 18. Text Handling and Privacy-Conservative Processing

Raw comment and PR text may be collected when public and necessary for trace detection. Processed tables should minimize raw text by storing:

```text
text_present
text_length
text_hash
matched_regex_family
matched_regex_pattern_id
short_context_excerpt_if_needed_for_manual_audit
raw_json_path
```

Manual audit files may contain short excerpts needed for validation, but avoid unnecessarily exporting long public comments.

## 19. Idempotency, Logging, and Provenance

Every module must be idempotent.

Rules:

- Skip existing raw JSON unless `--force` is set.
- Use deterministic IDs for episodes, objects, and payload hashes.
- Save configuration hash for every run.
- Save run logs in `reports/run_logs/`.
- Keep raw and processed data separate.
- Never silently overwrite manual audit decisions.

Every module log should include:

```text
run_id
module_name
start_time_utc
end_time_utc
input_paths
output_paths
n_input_rows
n_output_rows
n_errors
configuration_hash
git_commit_hash_if_available
```

## 20. Module Responsibilities

### 20.1 config.py

Load YAML configuration files and expose validated configuration objects.

### 20.2 logging_utils.py

Create run IDs, structured logs, configuration hashes, and error summaries.

### 20.3 github_client.py

Implement an authenticated GitHub API client with:

- pagination;
- retry logic;
- rate-limit handling;
- secondary-rate-limit backoff;
- raw JSON saving;
- endpoint provenance;
- idempotent skip logic.

### 20.4 gharchive_client.py

Implement BigQuery execution for GH Archive discovery SQL with date slicing, table suffix handling, and safe parameterization.

### 20.5 search_github.py

Implement targeted Search API collection for exact invocation and AI-disclosure phrases. Save search results and hydrate them through REST.

### 20.6 discover_candidates.py

Produce candidate episodes from GH Archive and optional Search API. Deduplicate candidates and export `raw_candidates.parquet` plus Gate 1 reports.

### 20.7 hydrate_github_objects.py

Hydrate all GitHub objects for candidate episodes and save both raw JSON and normalized tables.

### 20.8 collect_repository_context.py

Collect repository metadata, languages, selected configuration files, governance proxies, AI-readiness files, and automation context.

### 20.9 collect_neighbor_pr_episodes.py

Collect neighboring non-AI PR episodes in the same repositories and configured time windows. This module only collects candidate comparison data; it must not perform matching or sample selection.

### 20.10 derive_trace_flags.py

Derive trace flags from hydrated GitHub objects and manually validated actor dictionary entries.

### 20.11 derive_event_sequences.py

Construct ordered event sequences and descriptive sequence features.

### 20.12 derive_collection_covariates.py

Construct repository, task, contributor, reviewer, dyad, file, and temporal context snapshots for later use.

### 20.13 validate_collection.py

Generate manual-audit samples, validation reports, missingness reports, and collection-quality summaries.

### 20.14 export_codebook.py

Generate a Markdown data dictionary listing every table, column, source object, endpoint/query, construction logic, temporal alignment rule, and caution flag.

## 21. Pilot Collection Workflow

Always run a pilot before full collection.

```bash
python -m src.discover_candidates \
  --start-date 2025-05-19 \
  --end-date 2025-06-30 \
  --source gharchive \
  --out data/interim/pilot_candidates.parquet

python -m src.hydrate_github_objects \
  --candidates data/interim/pilot_candidates.parquet \
  --max-candidates 500 \
  --out-dir data/raw/pilot/

python -m src.collect_repository_context \
  --episodes data/interim/pilot_candidates.parquet \
  --raw-dir data/raw/pilot/ \
  --out-dir data/processed/pilot/

python -m src.derive_trace_flags \
  --raw-dir data/raw/pilot/ \
  --out data/processed/pilot/ai_trace_flags.parquet

python -m src.derive_event_sequences \
  --raw-dir data/raw/pilot/ \
  --trace-flags data/processed/pilot/ai_trace_flags.parquet \
  --out data/processed/pilot/episode_event_sequences.parquet

python -m src.derive_collection_covariates \
  --raw-dir data/raw/pilot/ \
  --trace-flags data/processed/pilot/ai_trace_flags.parquet \
  --out-dir data/processed/pilot/covariates/

python -m src.validate_collection \
  --raw-dir data/raw/pilot/ \
  --processed-dir data/processed/pilot/ \
  --out reports/pilot_validation_report.md

python -m src.export_codebook \
  --processed-dir data/processed/pilot/ \
  --out reports/pilot_data_dictionary.md
```

Pilot acceptance criteria are collection-quality criteria only:

- Candidate discovery returns nontrivial candidate counts.
- Hydration success rate is acceptable.
- Raw JSON preservation works.
- Actor dictionary audit is feasible.
- Strict trace precision is acceptable based on manual audit.
- Repository/task/contributor/reviewer/dyad/file snapshots have reasonable coverage.
- Neighboring PR episode collection is feasible for repositories with AI traces.

## 22. Full Collection Workflow

Run full collection only after explicit Gate 6 approval.

```bash
python -m src.discover_candidates \
  --start-date 2025-05-19 \
  --end-date 2026-06-30 \
  --source gharchive \
  --out data/interim/candidates.parquet

python -m src.hydrate_github_objects \
  --candidates data/interim/candidates.parquet \
  --out-dir data/raw/full/

python -m src.collect_repository_context \
  --episodes data/interim/candidates.parquet \
  --raw-dir data/raw/full/ \
  --out-dir data/processed/full/

python -m src.collect_neighbor_pr_episodes \
  --episodes data/interim/candidates.parquet \
  --raw-dir data/raw/full/ \
  --out-dir data/raw/full_neighbor_prs/

python -m src.derive_trace_flags \
  --raw-dir data/raw/full/ \
  --out data/processed/ai_trace_flags.parquet

python -m src.derive_event_sequences \
  --raw-dir data/raw/full/ \
  --trace-flags data/processed/ai_trace_flags.parquet \
  --out data/processed/episode_event_sequences.parquet

python -m src.derive_collection_covariates \
  --raw-dir data/raw/full/ \
  --trace-flags data/processed/ai_trace_flags.parquet \
  --out-dir data/processed/covariates/

python -m src.validate_collection \
  --raw-dir data/raw/full/ \
  --processed-dir data/processed/ \
  --out reports/gate7_final_collection_report.md

python -m src.export_codebook \
  --processed-dir data/processed/ \
  --out reports/data_dictionary.md
```

Stop after full collection and final validation. Do not proceed to modeling.

## 23. Testing Requirements

Create tests for:

- GitHub URL parsing.
- Repository owner/name parsing.
- PR and issue number parsing.
- Exact `@copilot` regex detection.
- False-positive rejection for generic “copilot” mentions.
- Actor classification with humans, conventional bots, candidate AI actors, and validated AI actors.
- Pagination handling.
- Rate-limit backoff with mocked responses.
- Idempotent hydration skip logic.
- Temporal filtering for pre-episode snapshots.
- Text hashing and raw JSON path linkage.

## 24. README Requirements

The README must explain:

- Research data collection purpose.
- Public-GitHub-data-only scope.
- What the pipeline can and cannot observe.
- Why hidden AI use is out of scope.
- Setup and credentials.
- Configuration files.
- Approval gates.
- Pilot workflow.
- Full collection workflow.
- Raw and processed table inventory.
- Data validation protocol.
- Codebook generation.
- Known limitations.

## 25. Final Deliverables

At the end of data collection, Codex should deliver:

```text
reports/gate7_final_collection_report.md
reports/data_dictionary.md
reports/raw_data_inventory.md
reports/processed_data_inventory.md
reports/validation_report.md
data/interim/actor_dictionary_audit.parquet
data/interim/manual_audit_samples.parquet
data/processed/ai_trace_flags.parquet
data/processed/episode_event_sequences.parquet
data/processed/covariates/*.parquet
data/processed/neighbor_pr_episode_index.parquet
```

The final message should state that the GitHub data collection package is complete and ready for separate analysis planning. It should not report causal effects, hypothesis tests, or substantive conclusions.
