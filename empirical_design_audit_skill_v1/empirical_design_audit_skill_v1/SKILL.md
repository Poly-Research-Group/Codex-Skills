---
name: empirical_design_audit_before_modeling
summary: Audit archival empirical research designs before econometric model selection or estimation.
description: Use this skill after research-design-aware data preparation and before Stata econometric model selection. It verifies unit of analysis, row keys, timing, treatment or event construction, control-variable validity, sample restrictions, fixed-effect and clustering feasibility, and identification threats for archival Information Systems research. It produces a design-audit report, go/no-go decision, identification-threat register, estimator-readiness matrix, robustness seed plan, and model-selection handoff memo. It does not run hypothesis-testing models.
---

# Empirical Design Audit Before Econometric Modeling

## Primary goal

Audit whether an analysis-ready archival dataset is empirically coherent enough to enter econometric model selection. The skill must verify that the dataset, variables, timing, sample, and identification logic match the research question and hypotheses before any hypothesis-testing model is run.

This is a pre-modeling quality gate. It does not clean raw data, construct new research variables, choose a final econometric estimator, or estimate hypothesis-testing models. Its output is an explicit assessment of whether the prepared data can support the claimed empirical design, what assumptions remain unresolved, which design threats must be addressed, and what information should be passed to the later Stata model-selection skill.

Use Python and SQL as the default audit stack. Stata is downstream. This skill may export Stata handoff notes, but it should not run Stata regressions or report hypothesis-test coefficients unless the user explicitly asks for a narrow diagnostic regression.

## When to use this skill

Use this skill when the user wants to:

- Verify an analysis-ready dataset before running econometric models.
- Audit unit of analysis, row keys, time structure, panel structure, event-time structure, or dyadic/network structure.
- Check whether treatment, event, exposure, or key independent-variable construction is valid.
- Assess whether controls are theoretically justified, temporally valid, and not bad controls.
- Review sample restrictions, missingness, attrition, trimming, winsorization, and sample-flow decisions.
- Identify threats to causal interpretation before DID, event study, IV, matching, RD, panel FE, HDFE, survival, count, limited-dependent-variable, or network-spillover analyses.
- Create a handoff memo for a later Stata model-selection or model-implementation skill.

Do not use this skill as a substitute for the data-preparation skill. If raw files have not yet been cleaned, merged, and converted into an analysis-ready dataset, first use the data-preparation skill. Do not use this skill as the final model-selection skill; it can produce an estimator-readiness matrix, but it must not select or defend a final estimator as if model selection were complete.

## Default input package

Expect, but do not require, outputs from the archival empirical data-preparation skill:

```text
analysis_package/
  data/analysis/analysis_ready.parquet
  data/analysis/analysis_ready.dta
  docs/research_context_brief.md
  docs/model_readiness_memo.md
  output/audits/research_design_intake.yaml
  output/audits/hypothesis_register.csv
  output/audits/construct_measurement_plan.csv
  output/audits/hypothesis_variable_map.csv
  output/audits/identification_timing_plan.csv
  output/audits/control_variable_audit.csv
  output/audits/variable_construction_log.csv
  output/audits/sample_flow.csv
  output/audits/merge_audit.csv
  output/audits/missingness_audit.csv
  output/audits/outlier_audit.csv
  output/audits/panel_audit.csv
```

If these artifacts are missing, ask for the missing design information and create a minimal design-audit intake record before proceeding.

## Required first step: audit intake and confirmation

Before auditing the data, Codex must confirm the empirical design. If the user has not already provided the needed information, begin by asking:

```text
Before I audit the empirical design, I need to confirm the design contract that the dataset is supposed to satisfy.

1. Research context: What is the project title or short label, empirical setting, focal phenomenon, and main research question?
2. Hypotheses: What are the hypotheses or focal empirical relationships? Please identify expected directions, moderators, mediators, mechanisms, or exploratory relationships.
3. Unit of analysis: What should one row in the final dataset represent? Examples: creator-day, creator-category-session, user-week, firm-quarter, app-month, token-collection-day, transaction, dyad-day, student-assignment.
4. Time structure: Is the data cross-sectional, repeated cross-sectional, panel, cohort-time, event-time, dyadic panel, or survival/risk-set data? What is the time grain and observation window?
5. Treatment/event/key IV: Is there a treatment, event, intervention, platform shock, adoption timing, exposure, or key independent variable? How is it constructed, and when is it measured relative to the outcome?
6. Outcomes: What are the dependent variables, and when are they measured?
7. Controls: What candidate controls should be included, what is the theoretical rationale for each, and are they measured before the treatment/key independent variable and outcome?
8. Moderators and mediators: Which variables are moderators, mediators, or mechanisms? Are they pre-treatment, contemporaneous, or post-treatment?
9. Sample restrictions: What units and time periods are eligible, and which restrictions were applied before observing outcomes?
10. Identification logic: Is the intended design associational, panel FE, DID/event study, IV, matching/treatment effects, RD, survival, dynamic panel, network/spillover, or another design?
11. Fixed effects and clustering: What fixed effects and clustering dimensions are substantively intended?
12. Data files: Where is the analysis-ready dataset and what metadata/audit files are available?
```

After receiving the answers, produce a concise audit plan and ask the user to confirm or correct it. Proceed only after confirmation or after the user explicitly authorizes proceeding with documented assumptions.

## Design audit principles

1. Start from the research question and hypotheses, not from available columns.
2. Treat the unit of analysis as a contract. All audits should be interpreted relative to the row-level unit.
3. Never let a treatment, key independent variable, or control use information from the future unless the research design explicitly requires and justifies it.
4. Separate confounders, precision controls, fixed effects, moderators, mediators, mechanisms, colliders, and outcomes.
5. Flag post-treatment controls, mechanically related controls, and platform-algorithmic variables that may be downstream of the focal effect.
6. Treat sample restrictions as identification decisions. Report how many units and observations are lost at each step, and whether loss differs by treatment status, event timing, or outcome availability.
7. Check whether the proposed fixed effects leave identifying variation in the key variables.
8. Check whether the clustering dimension matches the source of treatment assignment, serial dependence, platform shocks, or group-level correlation.
9. Diagnose threats before model selection. Do not use regression results to justify design decisions.
10. Use cautious language: “ready,” “conditionally ready,” “not ready,” and “requires user decision.” Avoid overstating causal credibility.

## Required output package

Create a folder named `design_audit_package/` unless the user specifies another location. It should contain:

| Artifact | Purpose |
|---|---|
| `docs/design_audit_report.md` | Main narrative audit report, including unit, timing, treatment, controls, sample, FE/clustering, threats, and go/no-go decision. |
| `docs/pre_model_go_no_go.md` | Concise decision memo: ready, conditionally ready, or not ready for model selection. |
| `docs/model_selection_handoff_memo.md` | Handoff memo for the later Stata model-selection skill. |
| `docs/identification_threat_memo.md` | Narrative explanation of design-specific threats and mitigation options. |
| `docs/assumptions_log.md` | User-approved assumptions and unresolved ambiguities. |
| `output/audits/audit_input_manifest.csv` | Files and metadata used in the audit. |
| `output/audits/hypothesis_design_audit.csv` | One row per hypothesis: constructs, variables, expected direction, empirical design, estimand, and readiness. |
| `output/audits/unit_time_structure_audit.csv` | Unit/time key uniqueness, duplicates, panel balance, gaps, and row-key status. |
| `output/audits/timing_and_leakage_audit.csv` | Timing of DV, IV/treatment, controls, moderators, mediators, and leakage risks. |
| `output/audits/treatment_event_construction_audit.csv` | Treatment/event/exposure construction, cohorts, pre/post availability, treatment variation, and control-group status. |
| `output/audits/outcome_support_audit.csv` | Outcome support, timing, missingness, censoring, zero mass, and transformation flags. |
| `output/audits/control_bad_control_audit.csv` | Control-variable recommendations and bad-control flags. |
| `output/audits/sample_restriction_attrition_audit.csv` | Sample-flow, missingness, attrition, treatment-status loss, and eligibility concerns. |
| `output/audits/fixed_effect_clustering_readiness_audit.csv` | FE dimensions, cluster counts, within-FE variation, and absorption risks. |
| `output/audits/identification_threat_register.csv` | Threat-by-threat risk assessment, severity, evidence, and mitigation. |
| `output/audits/estimator_readiness_matrix.csv` | Readiness of common design/model families without selecting the final estimator. |
| `output/audits/robustness_seed_plan.csv` | Robustness and sensitivity checks implied by the audit. |
| `output/figures/` | Descriptive diagnostic plots when relevant: sample-flow plot, missingness plot, treatment-timing histogram, pre-period descriptive trends, overlap plots. |
| `logs/` | Audit execution logs. |

## Standard project structure

```text
project_root/
  config/
    audit_config.yaml
  code/
    python/
      00_master_design_audit.py
      01_load_inputs_validate_metadata.py
      01b_hypothesis_design_audit.py
      02_unit_time_structure_audit.py
      03_timing_and_leakage_audit.py
      04_treatment_event_construction_audit.py
      04b_outcome_support_audit.py
      05_control_and_bad_control_audit.py
      06_sample_restriction_attrition_audit.py
      07_identification_threat_audit.py
      08_fe_clustering_readiness_audit.py
      09_export_design_audit_package.py
      utils_audit.py
    sql/
      00_basic_counts.sql
      01_unit_time_key_checks.sql
      02_treatment_event_checks.sql
      03_sample_flow_checks.sql
      04_balance_pretrend_support_checks.sql
  data/
    analysis/
      analysis_ready.parquet
      analysis_ready.dta
  output/
    audits/
    figures/
  docs/
    design_audit_report.md
    pre_model_go_no_go.md
    model_selection_handoff_memo.md
    identification_threat_memo.md
    assumptions_log.md
  logs/
```

## Audit workflow

### 0. Validate inputs and metadata

Confirm that Codex can locate the analysis-ready dataset and any existing metadata files. The audit may proceed with incomplete metadata only if the missing pieces are not blocking and all assumptions are recorded.

Minimum required metadata:

- Research question and hypotheses or empirical relationships.
- Intended unit of analysis and row key.
- Time structure and observation window.
- DV, key IV/treatment/event, moderators, mediators/mechanisms, candidate controls, fixed effects, and clustering dimensions.
- Timing for all key variables and candidate controls.
- Sample restrictions and rationale.
- Intended empirical design family.

Hard stop if the unit of analysis, dependent variable, key independent/treatment variable, or row key is unknown.

### 1. Hypothesis-to-design audit

For each hypothesis, create a row in `hypothesis_design_audit.csv` with:

- Hypothesis ID and statement.
- Relationship type: main effect, moderation, mediation, mechanism, heterogeneity, spillover, dynamic effect, treatment effect, descriptive association.
- Theoretical constructs and empirical variables.
- Expected sign or pattern.
- Outcome timing and cause timing.
- Estimand target, if applicable: conditional association, elasticity, ATT, ATE, ATET, LATE, hazard ratio, marginal effect, odds ratio, incident-rate ratio, dynamic treatment path, or mechanism path.
- Required data structure.
- Identification requirements.
- Current readiness: ready, conditionally ready, not ready, or needs user decision.

Flag mismatches, such as a moderation hypothesis without an interaction variable or a mediation hypothesis without temporally ordered mediator and outcome measures.

### 2. Unit-of-analysis and row-key audit

Verify that the dataset satisfies the declared unit of analysis.

For cross-sectional data, verify one row per unit. For panel data, verify one row per unit-time. For event-time data, verify one row per unit-event-time or unit-relative-time. For dyadic/network data, verify whether dyads are directed or undirected, whether `(i,j)` and `(j,i)` are distinct, and whether self-dyads are allowed.

Run checks for:

- Duplicate row keys.
- Missing IDs or time values.
- Unexpected many-to-one or one-to-many row patterns after aggregation.
- Multiple observations per unit-time due to unresolved lower-level data.
- Panel gaps, entry, exit, and balance.
- Aggregation weights, if lower-level records were collapsed.
- Time-zone and timestamp-normalization issues.

Hard stop if the row key is not unique and the duplicates cannot be substantively explained.

### 3. Time-structure and temporal-ordering audit

Classify the dataset as cross-section, repeated cross-section, panel, cohort-time, event-time, dyadic panel, survival/risk-set, or mixed structure. Then audit timing for all main variables.

Required checks:

- Does the key IV/treatment/event occur before the outcome?
- Are controls measured before the key IV/treatment/event or at least predetermined relative to the outcome?
- Are moderators measured before treatment, fixed before treatment, or theoretically exogenous to treatment?
- Are mediators/mechanisms measured after treatment and before outcome when mediation is claimed?
- Do lagged variables use only previous periods?
- Do rolling-window variables accidentally include the current or future outcome window?
- Do baseline measures overlap with treatment or post-treatment periods?
- Are timestamps normalized to the correct time zone and time grain?

Flag likely data leakage when variable names or metadata suggest future, post, after, cumulative-through-outcome, ranking-after-treatment, current outcome-derived, or platform-exposure-after-treatment variables are included as controls.

### 4. Treatment, event, exposure, and key-IV construction audit

If the design has a treatment, event, exposure, adoption, entry, policy shock, algorithmic change, or content switch, audit its construction before any model is selected.

Required checks:

- Treatment definition and empirical coding.
- Treatment timing and event date/time.
- Eligibility criteria defined before treatment.
- Treated, untreated, never-treated, not-yet-treated, always-treated, and reversibly treated units.
- Treatment intensity, dose, or exposure mapping if treatment is continuous or network-based.
- Whether treatment is defined using post-treatment outcomes.
- Pre-treatment and post-treatment observations available for treated and comparison units.
- Anticipation windows and no-anticipation plausibility.
- Simultaneous shocks, competing events, or platform-wide changes.
- Spillovers/interference between treated and untreated units.
- Treatment timing distribution for staggered adoption.
- Repeated events and whether event windows overlap.

Hard stop if treatment/event timing is undefined for a causal design that depends on timing.

### 5. Outcome support and measurement audit

For each dependent variable:

- Confirm the construct measured and timing relative to the cause.
- Check missingness and whether missing outcomes imply zero, non-observation, censoring, attrition, or source failure.
- Check support: continuous, binary, ordinal, nominal, count, nonnegative skewed, share/fraction, censored, truncated, duration/time-to-event, network measure.
- Flag extreme values and mechanical transformations that depend on treatment windows.
- Confirm whether transformations preserve interpretability.
- For logged outcomes, confirm treatment of zeros and negative values.
- For count outcomes, distinguish true zeros from missing activity or structural non-exposure.
- For survival outcomes, verify risk-set construction and censoring rules.

The audit should not choose the final model based only on outcome support, but it should record model-family implications for the later model-selection skill.

### 6. Control-variable and bad-control audit

For each candidate control, classify it as one of the following:

- Pre-treatment confounder.
- Predetermined baseline measure.
- Precision control.
- Fixed-effect proxy or design control.
- Moderator.
- Mediator or mechanism.
- Post-treatment variable.
- Collider.
- Outcome component or mechanically related variable.
- Robustness-only variable.
- Descriptive-only variable.
- Excluded variable.

The inclusion decision must be based on theory, temporal ordering, and design logic, not statistical significance. Flag controls as high-risk when they are measured after treatment, affected by the treatment, partly constructed from the dependent variable, driven by platform algorithms downstream of treatment, likely colliders, or absorbed by planned fixed effects.

The control audit should produce a recommendation: include in main model, include only in robustness, use only in mechanism analysis, exclude from main model, or requires user decision.

### 7. Sample-restriction and attrition audit

Audit whether the sample is defined consistently with the research design.

Required checks:

- Inclusion/exclusion rules are documented and preferably defined before observing outcomes.
- Unit counts and observation counts after each restriction.
- Treatment/control composition before and after restrictions.
- Missingness-driven loss in key variables.
- Attrition by treatment status, cohort, event time, or baseline outcome level.
- Balanced-panel restrictions and whether they create survivorship bias.
- Trimming/winsorization thresholds and whether they were set ex ante.
- Source coverage limitations, API gaps, suspended accounts, inactive units, and left/right censoring.

Hard stop if the final sample cannot be reconstructed from documented restrictions or if core restrictions depend on post-treatment outcomes without explicit justification.

### 8. Fixed-effect and clustering readiness audit

Before model selection, check whether the intended fixed effects and clustering dimensions are feasible.

For fixed effects:

- Verify all FE variables exist and have sufficient categories.
- Check whether key variables vary within intended FE dimensions.
- Flag variables that will be absorbed by unit, category, product, geography, or time fixed effects.
- Check singleton groups and sparse cells.
- Check whether two-way or high-dimensional FE would remove most identifying variation.

For clustering:

- Identify the likely dependence structure: unit-level serial correlation, treatment-assignment level, category shocks, firm shocks, geography shocks, platform-wide shocks, network/dyadic dependence, or time shocks.
- Count clusters and flag small-cluster settings.
- Check whether treatment is assigned at a higher level than the row unit.
- Consider multiway clustering if errors may correlate across two nonnested dimensions.
- Record clustering recommendations for the model-selection skill without finalizing the estimator.

### 9. Identification-threat audit

Create an identification-threat register. Include threats even when they cannot be fully resolved; the purpose is to make the model-selection skill and manuscript writing honest.

Common threats in archival IS research:

- Omitted time-varying confounders.
- Reverse causality.
- Simultaneity between users, creators, platforms, and algorithms.
- Endogenous treatment timing or adoption.
- Selection into treatment, platform participation, content contribution, or visibility.
- Measurement error in scraped/API variables.
- Source coverage changes and platform policy/API changes.
- Algorithmic confounding from ranking, recommendation, search, moderation, or monetization systems.
- Interference, spillovers, and network dependence.
- Attrition, entry/exit, survivorship, and suspended/deleted accounts.
- Seasonality, platform-wide shocks, release calendars, news shocks, or competitor events.
- Censoring, truncation, structural zeros, and inactive periods.
- Data leakage from future or post-treatment windows.

Design-specific threats:

| Intended design | Audit emphasis |
|---|---|
| Cross-sectional association | Confounding, reverse causality, measurement timing, selection into sample. |
| Pooled/panel FE | Within-unit variation, time-varying confounding, serial correlation, dynamic selection, FE absorption. |
| DID/event study | Treated/control definition, pre-period length, descriptive pre-trends, no anticipation, no concurrent shocks, staggered adoption, treatment-effect heterogeneity, treatment reversals. |
| IV/control function | Instrument relevance logic, exclusion restriction, timing, monotonicity if LATE is claimed, instrument-induced sample restrictions. |
| Matching/treatment effects | Overlap/common support, covariate timing, balance, hidden confounding, positivity. |
| RD | Running variable, cutoff rule, manipulation, sorting, local sample, covariate continuity, bandwidth feasibility. |
| Survival/duration | Risk-set construction, censoring, left truncation, time-varying covariates, competing risks. |
| Count/nonlinear outcomes | Outcome support, exposure/offset, structural zeros, censoring, separation risk. |
| Dynamic panel | Lag structure, panel length, persistence, attrition, instrument count risk, predetermined variables. |
| Network/spillover | Exposure mapping, reflection problem, interference, endogenous network formation, dyadic dependence. |

### 10. Estimator-readiness matrix

Produce `estimator_readiness_matrix.csv`, but do not select the final estimator. Each row should represent a possible design/model family and include:

- Model/design family.
- Required data conditions.
- Conditions satisfied.
- Conditions not satisfied.
- Required diagnostics later.
- Readiness status: ready, conditionally ready, not ready, not applicable.
- Notes for the later Stata model-selection skill.

Example families include OLS/HDFE, panel FE, correlated random effects, DID/event study, IV, treatment effects/matching, RD, count models, limited dependent-variable models, survival models, multilevel models, dynamic panel, SEM/GSEM, and network/spillover models.

### 11. Go/no-go decision

The audit must end with one of three statuses:

- **Ready for model selection**: No blocking issues; remaining issues are normal model-selection choices.
- **Conditionally ready**: Model selection may proceed, but specific assumptions, sample decisions, timing issues, or robustness checks must be handled.
- **Not ready**: Blocking issues prevent credible model selection; data preparation or design definition must be revised.

Do not say the design is “causal” merely because treatment timing or panel data exist. Causal language requires a defensible identification argument and threat assessment.

## Hard-stop conditions

Stop and ask for user input or data-preparation revision when any of the following occurs:

- Unit of analysis is undefined.
- Row key is not unique and duplicates are not explained.
- Outcome, key IV/treatment/event, or time index is missing for a design that requires it.
- Treatment timing is ambiguous or constructed using future outcomes.
- A DID/event-study design has no valid comparison group or no pre-treatment observations.
- Candidate controls include post-treatment variables that the user wants in the main model without an explicit rationale.
- Sample restrictions cannot be reconstructed.
- Key variables have severe unexplained missingness or impossible values.
- Intended fixed effects absorb the focal independent variable entirely.
- The design depends on an instrument, cutoff, or event date that is not documented.
- The user asks to proceed with causal claims despite unresolved identification contradictions.

## Recommended figure outputs

Generate figures only when useful and only as descriptive diagnostics:

- Sample-flow plot showing observation loss by step.
- Missingness heatmap or missingness-by-time plot.
- Treatment timing histogram or cohort distribution.
- Event-time support plot showing available treated/control observations by relative time.
- Descriptive pre-period trend plot for DID/event-study readiness.
- Overlap plot for treatment/matching designs.
- Distribution plot for key outcomes and treatment/exposure intensity.

Do not label descriptive diagnostic figures as causal evidence.

## Stata handoff expectations

The model-selection handoff memo should be written for a later Stata skill. It should include:

- Analysis dataset path and format.
- Unit, time, panel declaration equivalents, and row key.
- Hypotheses and variable names.
- Recommended candidate model families and why each is feasible or infeasible.
- Fixed-effect dimensions and potential absorption risks.
- Recommended clustering dimensions and cluster counts.
- Required diagnostics for candidate models.
- Required robustness checks and sensitivity analyses.
- Unresolved design issues that must be decided before Stata code is generated.

The handoff memo should not contain final Stata commands for hypothesis testing unless the user explicitly requests a starter skeleton.

## Tone and reporting style

Use precise, research-oriented language suitable for Information Systems empirical research. Be direct about weaknesses. The audit should be constructive, not punitive: for each risk, state the problem, why it matters, how severe it is, and what can be done next.
