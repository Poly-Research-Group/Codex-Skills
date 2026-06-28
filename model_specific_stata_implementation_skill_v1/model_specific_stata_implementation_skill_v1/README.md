# Model-Specific Stata Implementation Skill

This Codex Skill implements Stata model families selected by the upstream Stata Model Selection Skill. It is designed for archival Information Systems research using Stata for econometric analysis.

Core features:

- Reads `stata_command_plan.csv` and model-selection handoff artifacts.
- Retrieves command documentation from Stata Press manual pages and command-specific Stata manual PDFs.
- Uses installed Stata help and `which` checks for community-contributed commands.
- Runs pre-estimation diagnostics before estimation, including multicollinearity among focal variables and controls.
- Requires checkpoints before specification changes.
- Uses factor-variable notation and `margins`/`lincom`/`contrast` for moderation and interaction effects.
- Exports ISR-style results tables with control coefficients included.

Start with `SKILL.md`.
