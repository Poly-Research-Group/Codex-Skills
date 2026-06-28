---
name: model_specific_stata_implementation
summary: Implement Stata estimator commands selected by the model-selection skill for archival empirical IS research, with manual retrieval, pre-estimation diagnostics, user checkpoints, moderation/interaction best practices, robustness checks, and ISR-style result tables that include controls.
description: Use this skill after the archival data-preparation skill, empirical design audit skill, and Stata model-selection skill. The skill reads artifacts such as stata_command_plan.csv, hypothesis_model_map.csv, diagnostics_requirements.csv, reporting_requirements.csv, robustness_plan.csv, control_bad_control_audit.csv, fixed_effect_clustering_readiness_audit.csv, and analysis_ready.dta. It retrieves command documentation from the Stata Press manual pages and command-specific Stata manual PDFs, summarizes syntax and postestimation requirements, prepares and runs Stata diagnostics, asks for approval before specification changes, implements main models and robustness checks, tests moderation or interaction effects with factor variables and margins-based interpretation, and exports ISR-style tables modeled on Zhao et al. (2022).
---

# Model-Specific Stata Implementation for Archival IS Research

## Primary goal

Translate a confirmed Stata model-selection plan into reproducible, diagnosis-aware, manuscript-ready Stata analyses. This skill should implement the commands selected by the Stata Model Selection Skill, not reselect the econometric design from scratch.

The skill must retrieve and read the manuals or help files for the requested Stata commands, run pre-estimation diagnostics, recommend specification adjustments only when diagnostics justify them, obtain user approval before changing the specification, estimate main models, robustness checks, and additional analyses, test moderation or interaction effects using Stata best practices, and export ISR-style result tables with control-variable coefficients included.

## Position in the empirical workflow

Use this skill after:

1. The archival empirical data-preparation skill has produced `analysis_ready.dta` and variable metadata.
2. The empirical design audit skill has verified unit of analysis, timing, treatment construction, controls, sample restrictions, and identification threats.
3. The Stata model-selection skill has produced a model-selection handoff package, including `stata_command_plan.csv`.

This skill may produce the final Stata analysis package, but it should not perform raw-data cleaning, Python/SQL data preparation, or substantive construct construction unless the user explicitly asks for a small Stata-side variable-generation step that was already approved upstream.

## Required inputs

Codex should request or locate the following files before implementation:

- `analysis_ready.dta`
- `stata_command_plan.csv`
- `hypothesis_model_map.csv`
- `diagnostics_requirements.csv`
- `reporting_requirements.csv`
- `robustness_plan.csv`
- `control_bad_control_audit.csv`
- `fixed_effect_clustering_readiness_audit.csv`
- `model_selection_handoff_memo.md` or `stata_implementation_handoff_memo.md`
- project-specific variable labels, outcome descriptions, hypothesis labels, and table titles
- Stata version and community-command policy

If any file is unavailable, ask the user whether to upload it, substitute an equivalent artifact, or proceed with assumptions logged in `output/implementation/assumptions_log.md`.

## Manual retrieval rule

The first technical step is to retrieve command documentation for every command or package listed in `stata_command_plan.csv`.

Use this source hierarchy:

1. **Stata Press manual volume pages** as the manual index. Start with the relevant Stata Press manual volume page, such as `https://www.stata-press.com/manuals/base-reference-manual/`, and follow its table-of-contents links to command-specific manual pages/PDFs.
2. **Command-specific Stata manual PDFs** from Stata’s manual PDF paths, typically `https://www.stata.com/manuals/<manual-file>.pdf`. For example, `regress` maps to `https://www.stata.com/manuals/rregress.pdf`; `xtreg` maps to `https://www.stata.com/manuals/xtxtreg.pdf`.
3. **Official Stata help inside Stata** using `help command` or `view help command` when the installed Stata version differs from the online manual version.
4. **Community package help files** only after checking installation with `which command`, `help command`, `ssc describe package`, or `net describe package`. Do not treat community help files as official Stata manuals.

Do not distribute or paste long excerpts from manuals. Produce a short manual digest that records syntax, required options, postestimation tools, model-fit statistics, variance-estimation options, and version-specific constraints. Save the digest to `output/manuals/manual_digest.md` and the retrieval audit to `output/manuals/manual_retrieval_log.csv`.

If a manual cannot be retrieved, stop at checkpoint C1 and ask the user whether to continue with installed Stata help, a manually supplied PDF, or an alternative command.

## Mandatory user checkpoints

Codex must pause at these checkpoints unless the user explicitly asks for an autonomous first pass with all assumptions documented.

| Checkpoint | When | What Codex must show | Approval required |
|---|---|---|---|
| C0. Implementation contract | Before retrieving manuals or writing code | Dataset path, command plan, Stata version, model families, hypotheses, dependent variables, focal variables, controls, fixed effects, clustering, robustness checks, output requirements, and community-command policy | Yes |
| C1. Manual retrieval | After reading `stata_command_plan.csv` and retrieving manuals/help | Commands found, manual source for each command, missing manuals, community packages, syntax constraints, postestimation tools, and any Stata-version mismatch | Yes if anything is missing, community-contributed, or version-sensitive |
| C2. Diagnostic plan | Before running diagnostics | Required diagnostics for unit/time structure, missingness, outcome support, transformations, multicollinearity, FE feasibility, cluster feasibility, interaction feasibility, and model-family assumptions | Yes |
| C3. Diagnostic results and adjustment | After diagnostics and before estimation | Findings, hard stops, warnings, proposed adjustments, variables affected, and whether the main model, robustness model, or table structure changes | Yes for every adjustment |
| C4. Main specification | Before estimating main models | Exact Stata commands, dependent variables, focal variables, controls, fixed effects, VCE/clustering, interaction notation, sample restrictions, and model-storage names | Yes |
| C5. Moderation/interaction | Before interpreting moderation/interaction results | Interaction terms, centering choices, marginal-effect grid, simple-slope tests, predicted-outcome plots, and whether nonlinear models require margins-based interpretation | Yes for each moderation hypothesis |
| C6. Robustness/additional analyses | Before running robustness checks | Robustness list, purpose of each check, command to be used, sample/window/measure changes, and expected table location | Yes |
| C7. Results table and interpretation | Before final export | ISR-style table shell, coefficient order, inclusion of controls, fit statistics, table notes, significance markers, and interpretation paragraph structure | Yes |

Record each checkpoint in `output/implementation/user_checkpoint_log.csv` with checkpoint ID, timestamp, user decision, assumptions approved, unresolved risks, and downstream effect.

## Pre-estimation diagnostics

Run diagnostics before implementation. The diagnostic plan should be tailored to the selected model family but should usually include the following.

### 1. Dataset and sample integrity

- Confirm the analysis file, data signature, Stata version, and sample filters.
- Verify the declared unit of analysis using `isid` where applicable.
- Check duplicate row keys using `duplicates report` and `duplicates tag`.
- Verify panel declaration using `xtset`, `xtdescribe`, `xtsum`, and, where relevant, time-gap checks.
- Confirm that the estimation sample does not change unexpectedly across main models because of missing values.

### 2. Missingness and support

- Use `misstable summarize` for all dependent variables, focal variables, controls, moderators, mediators, fixed-effect variables, and clustering variables.
- Check whether zeros, ones, negatives, and extreme values are valid for each outcome family.
- For log transformations, verify that the transformed variable was constructed upstream and that no future information or sample-specific minimum causes leakage.
- For count models, report the mean, variance, zero count, negative count, and exposure/offset validity.
- For fractional models, check that values are in `[0,1]`; distinguish strictly interior `(0,1)` outcomes from outcomes with many boundary values at 0 or 1.

### 3. Multicollinearity among IVs and controls

- Always run a correlation matrix among non-absorbed focal variables, moderators, and controls.
- Run `regress` on the outcome with the focal variables and controls, excluding high-dimensional fixed-effect dummies where appropriate, then run `estat vif`.
- If the main model is FE/HDFE, treat VIF as a diagnostic for nonabsorbed covariate redundancy, not as a definitive test of FE specification validity.
- Check exact collinearity during the actual estimator run; record variables omitted because of collinearity.
- Do not automatically drop a focal IV, treatment, moderator, or theoretically required control solely because VIF is high. Propose an adjustment memo and ask for approval.

### 4. Fixed-effect and clustering feasibility

- Verify that focal variables have identifying variation within the fixed-effect dimensions.
- Check whether time-invariant variables are absorbed by unit fixed effects.
- Check singleton observations and observations dropped by absorption.
- Count clusters and summarize cluster-size distribution.
- If the number of clusters is small, recommend a small-cluster sensitivity route such as wild-cluster bootstrap only if approved and available.

### 5. Model-family diagnostics

- Linear/panel FE: residual distribution, leverage or influence where feasible, heteroskedasticity strategy, within variation, and serial-correlation sensitivity when panel timing is central.
- Count: overdispersion, excess zeros, exposure/offset, separation/nonexistence risks, Poisson vs. NB comparison, and PPML/HDFE route if nonnegative outcomes and high-dimensional FE require it.
- Fractional: boundary mass at 0/1, link function, marginal effects, and robustness to linear FE/HDFE approximation if panel fixed effects are central.
- Binary/categorical: separation, rare outcomes, marginal effects, predicted probabilities, and FE-induced sample loss.
- IV/control-function: first-stage availability, weak-instrument diagnostics, overidentification tests, endogeneity tests, and reduced-form estimates.
- DID/event study: treatment timing, pre-period support, no-anticipation windows, event-time support, pretrend tests/plots, and clustering at the treatment-assignment level.
- Mediation/mechanism: treatment-mediator-outcome timing, mediator-outcome confounding, formal mediation vs. mechanism evidence, indirect-effect computation, and bootstrap/sensitivity requirements.

## Specification adjustment protocol

Diagnostic results may justify specification changes, but Codex must not silently alter the model.

Use this protocol:

1. Classify each diagnostic finding as `hard_stop`, `high_risk`, `moderate_warning`, or `minor_note`.
2. For each issue, state the affected hypothesis, variable, estimator, and table.
3. Propose one or more remedies.
4. Explain the tradeoff between econometric defensibility and theoretical interpretation.
5. Ask the user to approve the adjustment before implementation.
6. Save all approved changes in `output/implementation/specification_adjustment_memo.md`.

Examples:

- Severe multicollinearity among controls: verify duplicate construction, avoid dropping focal variables, consider removing redundant controls, combining highly correlated controls, reporting alternative-control robustness, or keeping them with interpretive caution.
- Focal variable has no within-unit variation: do not run a unit-FE main model for that hypothesis unless the focal variable enters through an estimable interaction; switch to the model-selection skill’s secondary estimator only after approval.
- Fixed effects absorb the moderator main effect: explain that the interaction may still be estimable if the focal variable varies within unit/time; report the omitted main effect transparently.
- Count outcome has heavy overdispersion: keep Poisson with robust SE if justified by conditional mean logic, add NB robustness, or use PPML/HDFE where appropriate and approved.
- Fractional outcome has many zeros or ones: use `fracreg` or a two-part robustness strategy rather than forcing `betareg` on boundary values.

## Moderation and interaction best practices in Stata

When a model includes moderation or interaction effects, follow these rules.

1. Use factor-variable notation whenever supported: `c.x##c.z`, `i.treat##c.z`, `c.x##i.group`, or `i.treat##i.group`.
2. Include lower-order terms unless absorbed by fixed effects or excluded by a clearly justified design. If a lower-order term is absorbed, note this in the table notes and interpretation memo.
3. Mean-center or standardize continuous moderators only for interpretability or numerical stability. Do not describe centering as a solution to conceptual multicollinearity.
4. For linear models, report the interaction coefficient and use `lincom`, `margins`, or `contrast` for simple slopes or group contrasts.
5. For nonlinear models, do not interpret the interaction coefficient alone as the moderation effect. Use `margins`, `margins, dydx() at()`, `contrast`, `lincom`, `nlcom`, or `marginsplot` as appropriate.
6. For panel FE/HDFE models, verify that the interaction term has within-identifying variation after fixed effects.
7. Report the moderator values used for simple slopes: mean, mean ± 1 SD, selected percentiles, theoretically meaningful values, or observed category values.
8. Export both a moderation table and, where useful, a predicted-outcome or marginal-effect plot.

Canonical examples:

```stata
* Continuous-by-continuous interaction
xtreg y c.x##c.z controls i.time, fe vce(cluster unit_id)
estimates store H1_mod
margins, dydx(x) at(z=(p10 p50 p90)) post
marginsplot, ytitle("Marginal effect of X on Y") xtitle("Moderator Z")

* Treatment-by-continuous moderator
xtreg y i.treat##c.z controls i.time, fe vce(cluster unit_id)
lincom 1.treat + 1.treat#c.z * 0
margins, dydx(treat) at(z=(p10 p50 p90))

* Treatment-by-categorical moderator
xtreg y i.treat##i.group controls i.time, fe vce(cluster unit_id)
margins group, dydx(treat)
contrast r.treat@group
```

## Result-table formatting rule

Follow the result-table conventions modeled on Zhao et al. (2022) unless the user specifies another target journal style:

- Title each table descriptively, for example, `Table X. Results of Main Effects`, `Table X. Results of Moderating Effects`, or `Table X. Robustness Checks`.
- Use model columns `(1)`, `(2)`, `(3)`, etc.
- Include a header row describing the dependent variable or dependent-variable family.
- Place focal variables first, followed by interaction terms for moderation models.
- Include a visible `Control variable` section and include coefficients for controls in the table. Do not collapse controls to `Yes` unless the user explicitly approves an appendix-only control table.
- Include fixed-effect and design rows, such as `Unit fixed effects`, `Time fixed effects`, `Category fixed effects`, `Session dummy`, or other project-specific dimensions.
- Include model/sample statistics: number of observations, number of units/categories/groups, R-squared or within R-squared for linear models, pseudo R-squared/log pseudolikelihood/AIC/BIC for nonlinear models, and model-specific diagnostics such as AR(2), Hansen J, first-stage F, or overdispersion statistics where relevant.
- Show standard errors in parentheses below or beside coefficients, following the chosen export format.
- Use significance notes such as `+ p < 0.10, * p < 0.05, ** p < 0.01, *** p < 0.001` unless the user requests another convention.
- Robustness tables should mirror the main model table structure so that readers can compare coefficient signs, magnitudes, controls, fixed effects, N, and model fit.

## Output package

The completed skill should produce:

- `code/00_master_model_implementation.do`
- `code/01_environment_and_manual_checks.do`
- `code/02_load_and_verify_data.do`
- `code/03_pre_estimation_diagnostics.do`
- `code/04_main_models.do`
- `code/05_moderation_interactions.do`
- `code/06_robustness_additional_analyses.do`
- `code/07_export_isr_results_tables.do`
- `output/manuals/manual_retrieval_log.csv`
- `output/manuals/manual_digest.md`
- `output/diagnostics/pre_estimation_diagnostics_report.md`
- `output/implementation/specification_adjustment_memo.md`
- `output/results/model_results_registry.csv`
- `output/tables/main_results_isr_style.tex`
- `output/tables/moderation_results_isr_style.tex`
- `output/tables/robustness_results_isr_style.tex`
- `output/figures/interaction_margins_*.png` or `.pdf` when relevant
- `output/implementation/stata_implementation_report.md`
- `output/implementation/user_checkpoint_log.csv`

## Hard stops

Stop and ask the user before estimation if any of the following occurs:

- The command plan is missing or inconsistent with the model-selection handoff.
- The manual or installed help for a requested command cannot be retrieved.
- The analysis dataset does not exist or cannot be loaded by Stata.
- The declared unit/time key is not unique for a panel model.
- A focal variable or treatment has no identifying variation in the proposed specification.
- A proposed control is flagged as post-treatment, mediator, collider, or mechanically constructed from the outcome.
- The outcome support contradicts the model family.
- The fixed effects absorb the focal effect and no interaction or alternative estimand is specified.
- Cluster count is too small for conventional clustered inference and no sensitivity route is approved.
- A community command is required but not approved or not installed.

## Do not do these things

- Do not select controls by p-value.
- Do not remove focal variables or controls because of VIF without user approval and theoretical justification.
- Do not manually create interaction variables when factor-variable notation is available and compatible.
- Do not interpret nonlinear interaction coefficients as marginal moderation effects without margins-based analysis.
- Do not hide controls behind a single `Control variable = Yes` row when the user requires control coefficients.
- Do not rewrite the empirical design because one diagnostic is inconvenient; return to the model-selection skill or ask for approval if a model-family change is needed.
- Do not paste large blocks of manual text into outputs. Summarize command syntax and implementation implications.
