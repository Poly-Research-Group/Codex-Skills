# Example Implementation Workflow

1. User uploads `stata_command_plan.csv`, `analysis_ready.dta`, and model-selection handoff artifacts.
2. Codex reads the command plan and runs `templates/python/00_retrieve_stata_manuals.py`.
3. Codex presents C1: manual retrieval checkpoint.
4. Codex generates project-specific Stata scripts from templates.
5. Codex runs diagnostics in Stata and presents C3: diagnostic-results checkpoint.
6. After approval, Codex runs main models, moderation models, robustness checks, and additional analyses.
7. Codex exports ISR-style tables with controls included.
8. Codex drafts `stata_implementation_report.md` summarizing results.

## Example command plan columns

See `examples/stata_command_plan_example.csv`.
