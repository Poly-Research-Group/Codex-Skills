---
name: archival_empirical_data_preparation_with_research_intake_python_sql
summary: Elicit research context and hypotheses, then prepare archival empirical data for Information Systems research using Python and SQL before Stata-based econometric analysis.
description: Use this skill when a research project needs research-design-aware preparation of archival cross-sectional, repeated cross-sectional, panel, cohort-time, or event-time data for empirical hypothesis testing in Information Systems research. The skill first asks for and confirms the research context, research questions, hypotheses, unit of analysis, timing, data sources, variable roles, control-variable logic, sample frame, and table requirements. It then guides Codex to clean raw data, stage data in a SQL database, build identifiers and time variables, merge sources, construct theory-aligned variables, select and audit controls, define samples, run diagnostics, output ISR-style descriptive statistics tables, and export analysis-ready files for later Stata econometric analysis. It does not choose or estimate econometric models.
---

# Archival Empirical Data Preparation for IS Research Using Python and SQL

## Primary goal

First, elicit and confirm the research context, research questions, hypotheses, unit of analysis, timing logic, data sources, variable roles, control-variable rationale, and manuscript-table requirements. Do not begin cleaning, merging, transformation, or code generation until this research-design intake is complete enough to define the analysis dataset.

Then create a reproducible, analysis-ready data package for archival empirical research in Information Systems. The data package must align the dataset with the study's hypotheses, unit of analysis, temporal ordering, data-generating process, and intended identification logic before any econometric model is selected or estimated.

Use Python and SQL as the primary data-preparation stack. Stata is a downstream econometric-analysis environment. This skill may export `.dta` files for Stata, but it should not use Stata to clean, merge, transform, or model the data unless the user explicitly asks.

The target deliverable is not merely a dataset. It is a research-design-aware data package containing raw-source documentation, SQL staging tables or views, Python transformation scripts, analysis-ready data, codebook, source inventory, hypothesis-variable map, control-variable audit, sample-flow table, merge audit, missingness audit, outlier audit, panel or cross-sectional structure audit, ISR-style summary statistics tables, correlation outputs, and a model-readiness memo.

## Use this skill when

Use this skill when the user wants to:

- Prepare archival data for IS empirical research.
- Construct panel, cross-sectional, repeated cross-sectional, cohort-time, or event-time datasets.
- Clean, merge, reshape, collapse, aggregate, transform, or label research data.
- Use Python and SQL databases for reproducible data preparation.
- Prepare data for later Stata models such as OLS, HDFE, panel FE/RE/CRE, DID, event study, IV, treatment effects, count models, limited dependent-variable models, survival models, or dynamic panel models.
- Produce manuscript-facing descriptive statistics tables in a style commonly seen in Information Systems Research empirical papers.

Do not use this skill to select the final estimator, run hypothesis tests, interpret coefficients, or write the results section. Those tasks belong to model-selection and model-specific Stata implementation skills.

## Default technology stack

Default to the following stack unless the user's project has a different environment:

| Layer | Default | Use for |
|---|---|---|
| Python | `pandas`, `numpy`, `pyyaml`, `pathlib`, `logging` | Data import, cleaning, diagnostics, variable construction, metadata exports, `.dta` export. |
| SQL database | DuckDB for local file-based projects; SQLite when dependency-light portability is required; PostgreSQL or cloud warehouse when data already reside there | Staging raw data, auditable joins, aggregations, merge diagnostics, analysis views. |
| File formats | Parquet for intermediate large data; CSV for inspection; DTA for Stata handoff | Efficient storage and cross-software portability. |
| Stata | Downstream only | Econometric models after the data-preparation skill has produced `analysis_ready.dta`. |

Rules:

1. Never manually edit raw files.
2. Never overwrite raw tables; create staged, clean, or analysis tables/views.
3. Use SQL for joins, row-count audits, aggregation, and declarative sample construction where possible.
4. Use Python for file ingestion, type normalization, complex transformations, text/network construction, diagnostics, table generation, and export.
5. Every output must be reproducible from `templates/python/00_master.py` and the SQL scripts.
6. The final dataset must be exported in at least one Stata-readable format, usually `analysis_ready.dta`, plus a neutral format such as Parquet or CSV.

## Operating principles

0. Ask for and confirm the research context, research questions, hypotheses, unit of analysis, timing, data sources, and variable roles before preparing data.
1. Start from hypotheses and research design, not from raw files.
2. Define the row-level unit of analysis before cleaning or merging.
3. Verify unique identifiers before every merge and before saving analysis data.
4. Treat merge cardinality as a research-design assumption that must be audited.
5. Construct variables with explicit theoretical role, source, timing, formula, and sample implication.
6. Keep pre-treatment controls separate from mediators, mechanisms, post-treatment variables, colliders, and outcomes.
7. Select controls through theory, temporal ordering, and identification logic; never through statistical significance alone.
8. Make all exclusions and sample restrictions reproducible and visible in `sample_flow.csv`.
9. Preserve raw and transformed versions of key variables unless storage constraints make this infeasible.
10. Audit missingness, outliers, and panel structure before exporting analysis data.
11. Export publication-facing summary statistics tables when requested or when the dataset is being prepared for manuscript drafting.
12. Stop before modeling when core design conditions are unresolved.


## Mandatory research-context intake before data preparation

Codex must begin with a user-facing intake interview unless the user has already provided a manuscript, proposal, preregistration, detailed research memo, or completed intake form. Even when such materials are provided, Codex must extract the implied design and ask about missing or ambiguous items before preparing data.

Do not inspect, clean, merge, transform, or export data until Codex can state the following in concrete terms:

| Intake area | Minimum required information |
|---|---|
| Research context | Project title or working label, empirical setting, platform/industry/context, focal phenomenon, and research question. |
| Hypotheses | At least one hypothesis or empirical relationship, including expected direction when the study is confirmatory. For exploratory projects, explicitly label the relationship as exploratory. |
| Construct logic | Dependent construct, key independent construct, treatment/event if any, moderators, mediators/mechanisms, and theoretical role of each construct. |
| Unit and time | Intended row-level unit of analysis, time grain if any, panel/cross-sectional/event-time structure, observation window, and unit/time identifiers. |
| Data sources | Raw files/tables/APIs, source coverage, source units, available IDs, expected merge keys, and source limitations. |
| Variable roles | Candidate dependent variables, key independent variables, treatment/event variables, moderators, mediators/mechanisms, controls, fixed effects, clustering dimensions, and sample restrictions. |
| Temporal ordering | When each key variable and candidate control is measured relative to treatment/event/key independent variable and outcome. |
| Sample frame | Inclusion/exclusion rules, treatment/control or exposed/unexposed groups if relevant, and whether restrictions are defined before observing outcomes. |
| Transformation rules | Planned lags/leads, logs, inverse hyperbolic sine transformations, winsorization/trimming, scaling, aggregation, or text/network measures. |
| Manuscript outputs | Summary-statistics variables, variable display names/descriptions, whether an ISR-style grouped/decomposed table is needed, and output formats. |

### Required first response when intake information is missing

When the user asks Codex to prepare data but has not provided the above information, Codex must ask the following questions before writing code. It may combine or shorten the questions if the user already answered some of them.

```text
Before I prepare the data pipeline, I need to lock the empirical design so the dataset is built around the hypotheses rather than around whatever columns happen to be available.

1. Research context: What is the project about? Please provide the empirical setting/platform, focal phenomenon, and main research question.
2. Hypotheses: What are the hypotheses or focal empirical relationships? For each one, please specify the expected direction if applicable.
3. Unit of analysis: What should one row in the final analysis dataset represent, such as creator-day, user-week, firm-quarter, app-month, transaction, creator-category-session, or student-assignment?
4. Time structure: Is the data cross-sectional, panel, repeated cross-sectional, event-time, or cohort-time? What is the time grain and observation window?
5. Data sources: What raw files, tables, APIs, or databases will be used? What IDs and timestamps exist in each source?
6. Variables: What are the intended dependent variables, key independent variables or treatment/event variables, moderators, mediators/mechanisms, candidate controls, fixed effects, and clustering dimensions?
7. Timing: Which variables are pre-treatment or predetermined, which are contemporaneous, and which may be post-treatment mechanisms or outcomes?
8. Sample frame: What units and time periods should be included or excluded, and why?
9. Transformations: Are there expected lags/leads, log or IHS transformations, winsorization/trimming rules, aggregations, or text/network measures?
10. Outputs: Which variables should appear in the ISR-style descriptive statistics table, and do you need a grouped/decomposed table?
```

### Intake approval gate

After receiving the user's answers, Codex must produce a short research-design summary and ask the user to confirm or correct it before generating the data-preparation code. The summary should include:

1. Research context and focal phenomenon.
2. Hypotheses or empirical relationships.
3. Final dataset unit of analysis and time grain.
4. Planned source tables/files and merge keys.
5. Variable-role map: DV, IV/treatment/event, moderators, mediators/mechanisms, candidate controls, fixed effects, clustering dimensions, sample restrictions.
6. Timing map and bad-control risks.
7. Planned outputs, including ISR-style summary-statistics tables.
8. Unresolved questions that block or constrain data preparation.

Codex may proceed only after one of the following occurs:

- The user explicitly confirms the design summary.
- The user instructs Codex to proceed with clearly stated assumptions, and Codex records those assumptions in `docs/assumptions_log.md` and `docs/research_context_brief.md`.

If the user wants a rapid prototype, Codex may create skeleton files, but the skeleton must contain placeholders and must not claim the data are analysis-ready.

### Required intake artifacts

Create these files before the main data-preparation pipeline:

| Artifact | Purpose |
|---|---|
| `docs/research_context_brief.md` | Human-readable summary of context, research question, hypotheses, unit of analysis, data sources, variables, timing, and assumptions. |
| `output/audits/research_design_intake.yaml` | Machine-readable intake record used by the pipeline validator. |
| `output/audits/hypothesis_register.csv` | One row per hypothesis or exploratory relationship, including expected direction and empirical role. |
| `output/audits/construct_measurement_plan.csv` | Construct-to-measure mapping before variables are constructed. |
| `output/audits/identification_timing_plan.csv` | Timing and identification audit for key variables, controls, mechanisms, and outcomes. |
| `docs/assumptions_log.md` | Explicit record of unresolved assumptions and user-approved defaults. |

Quality gate: If `research_design_intake.yaml` is missing or still contains placeholders for research question, hypotheses/relationships, unit of analysis, data structure, raw sources, or variable roles, stop and ask the user for the missing information.

## Required inputs

Before writing code, extract or request the following information. If some details are missing, create `docs/assumptions_log.md` and proceed only if the missing detail is not a blocking issue.

| Input | Required content |
|---|---|
| Research question and hypotheses | H1, H2, H3, etc.; focal constructs; expected direction; mechanism; boundary condition. |
| Unit of analysis | What one row should represent, such as creator-day, user-week, firm-quarter, app-month, token-collection-day, student-assignment, transaction, or creator-category-session. |
| Time structure | Cross-section, repeated cross-section, balanced panel, unbalanced panel, event-time panel, cohort-time panel, or no time dimension. |
| Raw data sources | File names, source owners, acquisition dates, APIs, scraping scripts, licenses, codebooks, and source-specific caveats. |
| Expected identifiers | Unit IDs, time IDs, source-specific IDs, merge keys, group IDs, category IDs, geography IDs, treatment IDs. |
| Variable map | Dependent variables, key independent variables, treatment/event variables, moderators, mediators, mechanisms, controls, fixed effects, clustering dimensions, sample restrictions. |
| Timing rules | When each variable is measured relative to treatment/event/outcome. |
| Sample frame | Inclusion/exclusion criteria defined before observing outcomes where possible. |
| Merge plan | Expected `1:1`, `1:m`, `m:1`, or explicitly justified complex linkage for each merge. |
| Transformation rules | Logs, inverse hyperbolic sine, winsorization, trimming, scaling, standardization, aggregation, lag/lead construction. |
| Manuscript table requirements | Which variables belong in the main descriptive statistics table, whether a grouped/decomposed table is needed, display names, descriptions, decimal rules, and table notes. |

## Required output package

Create a folder named `analysis_package/` or equivalent. It must contain the following artifacts unless the user explicitly narrows the task.

| Artifact | Description |
|---|---|
| `data/analysis/analysis_ready.dta` | Final Stata dataset for later econometric analysis. |
| `data/analysis/analysis_ready.parquet` | Preferred neutral analysis dataset for reproducible inspection and non-Stata workflows. |
| `data/analysis/analysis_ready.csv` | Optional CSV version when useful for inspection or sharing. |
| `data/analysis/analysis_database.duckdb` or equivalent | SQL database containing staged, clean, and analysis tables/views when feasible. |
| `docs/research_context_brief.md` | Confirmed research context, hypotheses, unit of analysis, data structure, source plan, timing logic, assumptions, and unresolved issues. |
| `output/audits/research_design_intake.yaml` | Machine-readable record of the confirmed research-design intake. |
| `output/audits/hypothesis_register.csv` | One row per hypothesis or exploratory relationship, including expected sign and construct roles. |
| `output/audits/construct_measurement_plan.csv` | Mapping from theoretical constructs to preferred and alternative empirical measures. |
| `output/audits/identification_timing_plan.csv` | Timing audit for treatment/key IV, outcomes, controls, moderators, mediators, and mechanisms. |
| `output/audits/source_inventory.csv` | Raw and intermediate source files, provenance, acquisition date, source notes, and import script. |
| `output/audits/hypothesis_variable_map.csv` | Mapping from hypotheses to constructs, variables, timing, expected sign, and empirical role. |
| `output/audits/variable_construction_log.csv` | Variable name, label, formula, source file/table, source variables, timing, role, and notes. |
| `output/audits/control_variable_audit.csv` | Candidate controls, theoretical rationale, timing, inclusion decision, bad-control risk, fixed-effect absorption risk, and main/robustness recommendation. |
| `output/audits/control_selection_memo.md` | Narrative justification for included, excluded, mechanism-only, and robustness-only controls. |
| `output/audits/merge_audit.csv` | Merge keys, expected cardinality, duplicate-key checks, matched/unmatched rows, and decisions. |
| `output/audits/sample_flow.csv` | Observation and unit counts after each restriction, merge, cleaning rule, and final sample definition. |
| `output/audits/missingness_audit.csv` | Missingness by variable and, when relevant, by time period, treatment status, and unit type. |
| `output/audits/outlier_audit.csv` | Distribution diagnostics, extreme values, transformation decisions, trimming/winsorization rules. |
| `output/audits/panel_audit.csv` | Panel balance, number of units, number of periods, gaps, entry/exit, within/between variation. |
| `output/tables/descriptive_statistics_full.csv` | Machine-readable descriptive statistics with N, mean, SD, percentiles, min, and max. |
| `output/tables/summary_statistics_isr_main.csv` | Manuscript-ready ISR-style key-variable summary table. |
| `output/tables/summary_statistics_isr_main.tex` | LaTeX version of the ISR-style key-variable table. |
| `output/tables/summary_statistics_isr_main.md` | Markdown preview of the ISR-style key-variable table. |
| `output/tables/summary_statistics_isr_decomposed.csv/.tex/.md` | Optional grouped table for decomposed outcomes, mechanisms, directional flows, or construct families. |
| `output/tables/correlation_matrix.csv` | Correlations among main variables and controls, with missingness handled transparently. |
| `docs/model_readiness_memo.md` | Narrative summary of dataset construction, unresolved risks, and implications for model selection. |
| `docs/README_reproducibility.md` | Software version, folder structure, execution order, expected outputs, source restrictions, and replication instructions. |
| `logs/` | Logs for each Python script and the master run. |

## Standard project structure

Use this structure unless the project already has an established structure.

```text
project_root/
  config/
    project_config.yaml
  code/
    python/
      00_master.py
      01_ingest_raw.py
      02_clean_sources.py
      03_build_keys_time.py
      04_merge_build_analysis.py
      05_construct_variables.py
      06_define_samples.py
      07_data_diagnostics.py
      08_export_isr_summary_tables.py
      09_export_analysis_package.py
      utils.py
    sql/
      00_schema.sql
      01_staging_views.sql
      02_merge_views.sql
      03_analysis_views.sql
      04_diagnostic_queries.sql
      05_summary_statistics.sql
  data/
    raw/
    interim/
    clean/
    analysis/
  output/
    audits/
    tables/
    figures/
  logs/
  docs/
    research_context_brief.md
    assumptions_log.md
    README_reproducibility.md
    model_readiness_memo.md
```

## Workflow

### Step 0. Conduct and validate the research-design intake

Start with the mandatory research-context intake. If the user has not supplied the research context, hypotheses, unit of analysis, time structure, data sources, variable roles, timing rules, sample frame, and output requirements, ask the intake questions before writing code.

After the user answers, create or update `docs/research_context_brief.md`, `output/audits/research_design_intake.yaml`, `output/audits/hypothesis_register.csv`, `output/audits/construct_measurement_plan.csv`, and `output/audits/identification_timing_plan.csv`.

Run `00_validate_research_intake.py` before the rest of the pipeline. The validator should fail if required intake fields are blank, unknown, or still placeholders.

Quality gate:

- Codex must be able to state what one row in the final dataset represents.
- Codex must be able to map every hypothesis to at least one dependent variable and one key explanatory variable, treatment, event, mediator, mechanism, or moderator.
- Codex must identify whether each proposed control is pre-treatment, predetermined, time-invariant, contemporaneous, post-treatment, mechanism-only, or excluded.
- Codex must know the raw sources and expected merge keys before generating merge code.
- If any item is unclear, stop and ask the user for clarification or record a user-approved assumption.

### Step 1. Build the research-design data map

Read the confirmed intake artifacts, especially `hypothesis_register.csv`, `construct_measurement_plan.csv`, and `identification_timing_plan.csv`, and create `output/audits/hypothesis_variable_map.csv`. Each hypothesis must map to measurable variables and timing.

Required columns:

```text
hypothesis_id,construct,variable_name,variable_label,role,expected_sign,timing_relative_to_treatment,unit_level,time_level,source_table_or_file,construction_status,notes
```

Allowed values for `role`:

```text
dependent_variable,key_independent_variable,treatment,event,moderator,mediator,mechanism,pre_treatment_control,precision_control,fixed_effect,cluster_dimension,sample_restriction,robustness_variable,descriptive_only
```

Quality gate:

- Every dependent variable must have a unit level and time level.
- Every key independent variable, treatment, moderator, mediator, and control must have timing relative to the outcome.
- Controls must be marked as pre-treatment, baseline, predetermined, or time-invariant. If not, flag them as potential bad controls.
- If the design is causal, no variable should be labeled as a control if it is measured after treatment or plausibly affected by treatment.

### Step 2. Freeze raw data provenance

Create `output/audits/source_inventory.csv` before importing or modifying data.

Required columns:

```text
source_id,raw_file_name,source_type,source_owner_or_url,acquisition_date,coverage_start,coverage_end,unit_in_raw_file,time_grain_in_raw_file,license_or_access_notes,import_script,known_limitations
```

Rules:

- Do not edit files in `data/raw/`.
- Load raw files into staging tables or views using Python scripts.
- Save import logs containing row counts, column counts, variable names, inferred types, parse warnings, and file hashes when feasible.
- When source data are generated through APIs or scraping, preserve the collection script, request parameters, API version if available, and retrieval timestamp.

### Step 3. Import raw data into SQL staging tables

Use Python to read raw files and write to the SQL database. Default to DuckDB for local projects.

Common Python import pattern:

```python
from pathlib import Path
import duckdb
import pandas as pd
from utils import load_config, ensure_dirs, log_table_profile, write_table

cfg = load_config("config/project_config.yaml")
ensure_dirs(cfg)
con = duckdb.connect(cfg["database"]["path"])

source_path = Path(cfg["paths"]["raw"]) / "source_file.csv"
df = pd.read_csv(source_path, encoding="utf-8")
write_table(con, df, "raw_source_file", schema="raw", overwrite=True)
log_table_profile(con, "raw.raw_source_file", cfg)
```

Common SQL staging pattern:

```sql
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS clean;
CREATE SCHEMA IF NOT EXISTS analysis;

CREATE OR REPLACE VIEW clean.source_file_clean AS
SELECT
    lower(trim(original_id)) AS unit_id_clean,
    CAST(event_timestamp AS TIMESTAMP) AS event_ts,
    CAST(metric_value AS DOUBLE) AS metric_value,
    * EXCLUDE (original_id, event_timestamp, metric_value)
FROM raw.raw_source_file;
```

After every import, record:

- Source row count.
- Source column count.
- Missingness in key raw IDs and dates.
- Duplicate raw keys.
- Type conversions and parse failures.
- Any source rows dropped during import, with reasons.

### Step 4. Define identifiers, row key, and time variables

Create or verify the unit ID and time ID before cleaning decisions that may aggregate, collapse, or merge observations.

For cross-sectional data:

```sql
SELECT unit_id, COUNT(*) AS n
FROM clean.main_table
GROUP BY unit_id
HAVING COUNT(*) > 1;
```

For panel data:

```sql
SELECT unit_id, time_id, COUNT(*) AS n
FROM clean.main_panel
GROUP BY unit_id, time_id
HAVING COUNT(*) > 1;
```

For event-time data:

```sql
CREATE OR REPLACE VIEW analysis.event_time_base AS
SELECT
    unit_id,
    calendar_date,
    event_date,
    date_diff('day', event_date, calendar_date) AS event_time,
    * EXCLUDE (unit_id, calendar_date, event_date)
FROM clean.unit_day;
```

Rules:

- Use stable numeric IDs where possible, but preserve original string IDs.
- Never overwrite original identifiers. Create standardized versions such as `creator_id_std` or `firm_id_clean`.
- Document all ID recoding, normalization, or crosswalk decisions in `variable_construction_log.csv`.
- In SQL, test uniqueness with grouped duplicate queries before creating analysis tables.
- In Python, enforce uniqueness using explicit assertions:

```python
assert not df.duplicated(["unit_id", "time_id"]).any(), "Duplicate unit-time rows detected."
```

### Step 5. Clean each source independently

Clean each source before merging.

Required cleaning checks:

- Normalize variable names to a consistent naming convention.
- Parse dates and timestamps with explicit timezone assumptions.
- Standardize string IDs using lowercasing, trimming, whitespace normalization, and source-specific rules.
- Convert numeric strings to numeric values only after documenting parse failures.
- Validate categorical values against known domains.
- Identify impossible values, structural zeros, source errors, and duplicated records.
- Preserve raw values for variables that require substantive recoding.

Python pattern:

```python
def normalize_string_id(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
         .str.strip()
         .str.lower()
         .str.replace(r"\s+", " ", regex=True)
    )

clean_df["creator_id_clean"] = normalize_string_id(raw_df["creator_name"])
clean_df["date"] = pd.to_datetime(raw_df["timestamp"], utc=True).dt.date
```

SQL pattern:

```sql
CREATE OR REPLACE VIEW clean.creator_profile_clean AS
SELECT
    lower(regexp_replace(trim(creator_name), '\\s+', ' ', 'g')) AS creator_id_clean,
    CAST(profile_created_at AS TIMESTAMP) AS profile_created_at,
    CAST(followers AS BIGINT) AS followers,
    mature_content_flag::BOOLEAN AS mature_content_flag
FROM raw.creator_profile;
```

### Step 6. Audit and execute merges

Before every join, create or update `merge_plan.csv`.

Required columns:

```text
merge_id,left_table,right_table,expected_cardinality,left_keys,right_keys,required_match_rate,keep_unmatched_left,keep_unmatched_right,substantive_rationale
```

Codex must perform pre-merge duplicate-key checks and post-merge row-count checks.

SQL merge-audit pattern:

```sql
-- Left duplicate-key check
SELECT key1, key2, COUNT(*) AS n
FROM clean.left_table
GROUP BY key1, key2
HAVING COUNT(*) > 1;

-- Right duplicate-key check
SELECT key1, key2, COUNT(*) AS n
FROM clean.right_table
GROUP BY key1, key2
HAVING COUNT(*) > 1;

-- Match-rate audit
SELECT
    COUNT(*) AS left_rows,
    SUM(CASE WHEN r.key1 IS NOT NULL THEN 1 ELSE 0 END) AS matched_rows,
    SUM(CASE WHEN r.key1 IS NULL THEN 1 ELSE 0 END) AS unmatched_left_rows,
    AVG(CASE WHEN r.key1 IS NOT NULL THEN 1.0 ELSE 0.0 END) AS match_rate
FROM clean.left_table l
LEFT JOIN clean.right_table r
  ON l.key1 = r.key1 AND l.key2 = r.key2;
```

Merge rules:

- Do not use joins that create row multiplication unless the multiplication is theoretically intended and documented.
- Treat many-to-many joins as hard-stop risks unless they are pre-aggregated, converted into bridge/crosswalk tables, or justified by the design.
- Save unmatched records to audit tables when they affect sample size or substantive interpretation.
- Record matched/unmatched rows in `merge_audit.csv`.

### Step 7. Select and audit controls

Create `control_variable_audit.csv` before finalizing the analysis dataset.

Required columns:

```text
candidate_control,construct,source_table_or_file,measurement_timing,theoretical_rationale,confounding_path_addressed,include_main_model,include_robustness,exclude_reason,bad_control_risk,post_treatment_risk,mediator_or_mechanism_risk,collider_risk,mechanical_overlap_with_dv,fixed_effect_absorption_risk,recommended_operationalization,notes
```

Control-selection rules:

- Include a control in the main dataset and main model plan only when it is theoretically justified, temporally valid, and not mechanically downstream of the focal explanatory variable.
- Prefer pre-treatment, lagged, baseline, or predetermined controls when causal interpretation is intended.
- Do not include mediators or mechanisms as main-model controls unless the explicit goal is mechanism decomposition and the interpretation is adjusted accordingly.
- Do not include variables affected by the treatment, focal independent variable, or outcome shock as ordinary controls.
- Do not select controls because they are statistically significant, improve model fit, or are readily available.
- Flag variables that will be absorbed by fixed effects; retain them only if needed for descriptive tables, interactions, heterogeneous effects, or non-FE specifications.

Control classes:

| Class | Main-model default | Examples |
|---|---|---|
| Pre-treatment confounder | Include | Baseline size, prior activity, prior performance, prior popularity, tenure. |
| Precision control | Include if temporally valid and theoretically harmless | Pre-period volatility, seasonality indicators, baseline category conditions. |
| Design control / fixed effect | Include if aligned with identification | Unit FE, time FE, category FE, geography FE, platform-section FE. |
| Moderator | Include as interaction component when hypothesized | Network structure, platform maturity, creator popularity. |
| Mediator or mechanism | Exclude from main total-effect model | Post-treatment engagement, post-treatment exposure, current algorithmic rank. |
| Collider / bad control | Exclude | Variables jointly affected by treatment and unobserved outcome shocks. |

Output `control_selection_memo.md` summarizing included controls, excluded controls, mechanism-only variables, robustness-only variables, and unresolved risks.

### Step 8. Construct variables

Construct variables only after identifiers, timing, and merge logic are stable.

For every constructed variable, log:

```text
variable_name,variable_label,role,formula_or_algorithm,source_tables,source_variables,unit_level,time_level,timing_relative_to_treatment,raw_variable_preserved,transformation_type,missingness_rule,outlier_rule,notes
```

Rules:

- Preserve raw variables and create transformed versions with transparent suffixes: `_log`, `_ihs`, `_z`, `_winsor`, `_lag1`, `_lead1`, `_pre`, `_post`.
- For log transformations, specify how zeros and negative values are handled.
- For inverse hyperbolic sine transformations, document why it is used.
- For winsorization or trimming, store cutoffs and affected observation counts.
- For lags/leads, group by unit and sort by time; never use future information in predictors unless explicitly constructing placebo leads or event-study variables.
- For treatment/event indicators, verify that event timing is not inferred from post-treatment outcomes unless the research design explicitly requires it.

Python lag pattern:

```python
df = df.sort_values(["unit_id", "time_id"])
df["prior_viewers_lag1"] = df.groupby("unit_id")["viewers"].shift(1)
```

SQL lag pattern:

```sql
CREATE OR REPLACE VIEW analysis.unit_time_with_lags AS
SELECT
    *,
    LAG(viewers, 1) OVER (PARTITION BY unit_id ORDER BY time_id) AS viewers_lag1,
    LEAD(treatment, 1) OVER (PARTITION BY unit_id ORDER BY time_id) AS treatment_lead1
FROM analysis.unit_time_base;
```

### Step 9. Define samples and track sample flow

Create `sample_flow.csv` with one row for every restriction, merge, cleaning rule, and final sample.

Required columns:

```text
step_id,step_name,script_or_query,condition_applied,observations_before,observations_after,observations_dropped,units_before,units_after,units_dropped,time_periods_before,time_periods_after,rationale,notes
```

Rules:

- Define the eligible sample before observing outcomes where possible.
- Distinguish theoretically motivated restrictions from data-quality exclusions.
- Report attrition separately by treatment/control group when a treatment design exists.
- If a restriction changes the treated/control composition materially, flag it in `model_readiness_memo.md`.

### Step 10. Audit missingness, outliers, and panel structure

Missingness audit:

- Overall missingness by key variable.
- Missingness by source table.
- Missingness by time period.
- Missingness by treatment status or cohort when relevant.
- Distinguish structural missingness, true zeros, API/source failures, not-yet-observed units, and censoring.

Outlier audit:

- Distribution summaries for raw and transformed variables.
- Extreme values and their source rows.
- Percent affected by trimming or winsorization.
- Rationale for retaining, transforming, trimming, or winsorizing.

Panel audit:

- Unit count, time-period count, observations per unit, min/max periods.
- Balanced vs. unbalanced panel status.
- Gaps in time series.
- Entry and exit patterns.
- Within- and between-unit variation for dependent variables, key independent variables, treatment, moderators, and controls.

Quality gate:

- If the key independent variable has no within-unit variation, flag that unit fixed-effects models cannot estimate its main effect.
- If treatment timing is ambiguous or inconsistent, do not export final analysis data for causal modeling.
- If missingness is strongly related to treatment or outcome timing, flag possible attrition bias.

### Step 11. Output ISR-style summary statistics tables

When manuscript-facing tables are requested, produce ISR-style summary statistics tables using `summary_statistics_plan.csv` and the final analysis sample.

Main table format:

```text
Table X. Descriptive Statistics of Key Variables
Variable | Description | Mean | Standard deviation | Minimum | Maximum
...
Number of observations | N
```

Grouped/decomposed table format:

```text
Table X. Descriptive Statistics of Decomposed [Outcome/Mechanism/Flow]
Direction/Group | Variable | Description | Mean | Standard deviation | Minimum | Maximum
...
Number of observations | N
```

Formatting rules:

- Use variable order from `summary_statistics_plan.csv`, not alphabetical order.
- Use manuscript-facing display names, including subscripts or LaTeX names when available.
- Include concise but substantively informative descriptions.
- Report Mean, Standard deviation, Minimum, and Maximum for each displayed variable.
- Report a single `Number of observations` row when all variables share the same sample N.
- If N differs across variables, either compute descriptive statistics on the common analysis sample or add an `N` column and include a note that variable-specific N differs because of missingness.
- For binary variables, report the mean as the share of ones and min/max as 0/1.
- For factor-coded variables, include category coding in the description or a table note.
- For transformed variables, make clear whether the table reports the raw or transformed variable.
- For heavily skewed variables, include median and percentiles in `descriptive_statistics_full.csv`, but keep the ISR-style main table compact unless the user requests additional columns.
- Export at least `.csv`, `.tex`, and `.md` versions. Optional `.xlsx` may be produced if the project workflow needs spreadsheet editing.

### Step 12. Export the analysis package for Stata

Export the final analysis dataset to Stata only after all data-preparation quality gates pass.

Python export pattern:

```python
analysis_df.to_parquet("data/analysis/analysis_ready.parquet", index=False)
analysis_df.to_csv("data/analysis/analysis_ready.csv", index=False)
analysis_df.to_stata(
    "data/analysis/analysis_ready.dta",
    write_index=False,
    version=118,
)
```

Also export:

- `variable_labels.csv` with variable labels and descriptions.
- `stata_handoff_notes.md` explaining unit of analysis, time index, panel declaration, candidate fixed effects, candidate clustering dimensions, and known data limitations.
- `model_readiness_memo.md` summarizing whether the dataset is ready for model selection.

Do not run Stata regressions in this skill.

## Hard-stop conditions

Stop and ask for user guidance, or create a blocking issue in `model_readiness_memo.md`, when any of the following occurs:

- The research context, research question, hypotheses/relationships, unit of analysis, data structure, raw sources, or variable roles have not been provided or confirmed.
- The unit of analysis is undefined or inconsistent across hypotheses.
- The final row key is not unique.
- A join creates unexplained row multiplication.
- A many-to-many relationship is used without a justified bridge table or aggregation rule.
- Treatment/event timing is missing, inconsistent, or inferred from post-treatment outcomes without justification.
- Proposed controls include post-treatment variables, mediators, mechanisms, colliders, or variables mechanically overlapping with the dependent variable.
- Key variables contain impossible values that cannot be resolved or explained.
- Missingness in dependent variables, treatments, or key independent variables is large and unexamined.
- The sample-flow table shows unexplained attrition that materially changes the sample.
- The final pipeline cannot be run from `00_master.py` without manual steps.

## Final response after applying this skill

When Codex finishes using this skill on a project, the final response to the user should include:

1. The path to `analysis_package/`.
2. A concise recap of the confirmed research context, hypotheses, unit of analysis, and data sources.
3. A concise summary of the final unit of analysis, time structure, sample size, unit count, and time-period count.
4. A list of generated audit files.
5. A summary of controls included/excluded and any bad-control risks.
6. A link or path to ISR-style summary statistics tables.
7. A list of unresolved issues, if any.
8. A clear statement that econometric model selection and Stata estimation are deferred to the next skill.
