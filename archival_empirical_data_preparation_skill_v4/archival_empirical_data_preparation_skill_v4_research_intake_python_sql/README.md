# Archival Empirical Data Preparation Skill for IS Research with Research-Design Intake

This reusable Codex Skill first elicits and confirms the research context, research questions, hypotheses, unit of analysis, timing, data sources, variable roles, and output requirements; then it prepares archival empirical datasets for Information Systems research using Python and SQL. It is designed to produce analysis-ready cross-sectional, panel, repeated cross-sectional, cohort-time, or event-time data for later econometric analysis in Stata.

The skill emphasizes research-design validity: unit of analysis, temporal ordering, merge cardinality, control-variable logic, sample construction, missingness, outliers, and panel structure are audited before the final dataset is exported.

## What changed in this version

This version adds a mandatory research-design intake and approval gate before any data cleaning, merging, transformation, or export. It also treats Python and SQL as the primary data-preparation tools. Stata is used downstream for econometric modeling, not for data preparation. The package still exports `analysis_ready.dta` for Stata.

This version also adds ISR-style summary statistics tables, including a main key-variable table and an optional grouped/decomposed table. The table format follows the common structure used in empirical ISR papers: Variable, Description, Mean, Standard deviation, Minimum, Maximum, with a Number of observations row when the variables share a common analysis sample.

## Main components

- `SKILL.md`: Main Codex Skill instructions.
- `templates/docs/research_intake_questionnaire.md`: Questions Codex must ask before data preparation when the research design is incomplete.
- `templates/metadata/research_design_intake.yaml`: Machine-readable intake record.
- `templates/metadata/hypothesis_register.csv`, `construct_measurement_plan.csv`, and `identification_timing_plan.csv`: Design-first mapping templates.
- `templates/python/`: Python pipeline templates, including `00_validate_research_intake.py`, which blocks the pipeline if intake artifacts are incomplete.
- `templates/sql/`: SQL staging, merge, analysis, and diagnostics templates.
- `templates/config/project_config.yaml`: Project configuration template.
- `templates/metadata/`: CSV and memo templates for design maps, audits, and variable documentation.
- `templates/docs/`: Reproducibility and model-readiness memo templates.
- `templates/checklists/`: Quality gates for control selection, bad controls, merge logic, and final data readiness.
- `examples/`: Examples of ISR-style summary statistics tables and timing/control audits.

## Recommended next skill

After this skill generates `analysis_ready.dta`, `model_readiness_memo.md`, and the audit outputs, use a separate Stata model-selection skill to decide among OLS/HDFE, panel FE/RE/CRE, DID/event study, IV, count models, treatment effects, limited dependent-variable models, or other estimators.
