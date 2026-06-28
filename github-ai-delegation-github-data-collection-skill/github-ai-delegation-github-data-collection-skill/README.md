# GitHub AI Delegation Data Collection Skill

This Codex skill builds a public GitHub data collection pipeline for a research project on visible AI delegation in collaborative software work.

The skill is intentionally scoped to **GitHub data collection only**. It should not run causal analysis, statistical modeling, final matching, event-study estimation, or substantive interpretation. It collects and prepares data that can later support a separate analysis plan.

## Main collection targets

The pipeline prioritizes two high-precision public trace families:

1. Platform-attributed AI traces, such as validated AI actor/app PR authorship, commits, comments, reviews, issue assignment, or timeline activity.
2. Invocation traces, especially exact `@copilot` mentions followed by subsequent AI actor activity in the same issue or PR episode.

It also collects robustness/context traces: self-disclosure, AI coauthorship trailers, reviewer attribution, and repository AI instruction files.

## Data sources

Use GitHub public data only:

- GH Archive / BigQuery for large-scale candidate discovery.
- GitHub REST API for hydration.
- GitHub Search API only for targeted query expansion.
- GitHub GraphQL API only when it improves collection efficiency.

Do not collect private repositories, organization Copilot telemetry, private usage metrics, or non-GitHub data sources.

## Approval gates

Codex must stop and wait for explicit user approval at each gate:

1. Configuration approval.
2. Candidate discovery approval.
3. Actor dictionary approval.
4. Pilot hydration approval.
5. Trace validation approval.
6. Collection coverage approval.
7. Full collection approval.
8. Final collection package approval.

## Core outputs

Raw-normalized tables include repositories, pull requests, issues, comments, reviews, commits, changed files, timeline events, actor profiles, and API call logs.

Processed collection tables include AI trace flags, actor classifications, episode event sequences, repository AI-readiness flags, collection covariate snapshots, neighboring PR episode index, validation reports, and codebooks.

## Usage

Paste `prompts/pasteable_codex_task.md` into Codex together with this skill. Codex should then implement the project structure, configuration files, SQL templates, pipeline modules, tests, pilot workflow, validation reports, and full collection workflow specified in `SKILL.md`.
