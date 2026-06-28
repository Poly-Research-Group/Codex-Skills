Build a Python pipeline for collecting public GitHub data for a research project on visible AI delegation in collaborative software work.

Scope restriction: this project is data collection only. Do not run causal analysis, statistical models, final matching, or substantive inference. The pipeline should discover candidate GitHub episodes, hydrate public GitHub objects, extract visible AI-delegation trace flags, construct temporally aligned collection covariate snapshots, validate data quality, and export raw/processed data plus codebooks.

Main trace families:
1. Platform-attributed AI traces, such as validated AI actor/app PR authorship, commits, comments, reviews, issue assignment, or timeline activity.
2. Exact human invocation traces, especially public @copilot mentions in issues/PRs/review comments followed by subsequent AI actor activity in the same episode.

Robustness/context traces to collect:
- AI self-disclosure in PR bodies, comments, or commit messages.
- AI coauthorship trailers.
- Reviewer attribution of work to AI.
- Repository AI instruction files.

Use GH Archive/BigQuery for candidate discovery and GitHub REST API for hydration. Preserve raw JSON. Export normalized Parquet tables. Include idempotent collection, rate-limit handling, pagination, validation reports, manual-audit samples, actor dictionary audit, and approval gates.

Implement the modules and tables specified in SKILL.md. Stop at each human approval gate and wait for explicit approval before continuing.
