---
name: stata_econometric_model_selection
summary: Select appropriate Stata estimator families for archival empirical IS research after data preparation and empirical design audit, with mandatory user checkpoints, explicit fractional-response model selection, and expanded Stata mediation-model routing.
description: Use this skill after the archival empirical data-preparation skill and empirical design audit skill. It maps research questions, hypotheses, dependent-variable support, data structure, timing, treatment or event construction, identification logic, fixed effects, clustering needs, mechanism/mediation claims, and design threats to appropriate Stata estimator families. It produces a model-selection report, hypothesis-to-estimator map, diagnostics requirements, reporting requirements, robustness plan, Stata code skeletons, user checkpoint log, mediation-selection memo, and a handoff memo for model-specific Stata implementation skills. It does not clean data and should not run final hypothesis-testing regressions unless explicitly requested.
---

# Stata Econometric Model Selection for Archival IS Research

## Primary goal

Select defensible Stata estimator families for hypothesis testing in archival Information Systems research. The skill must map the research question, hypotheses, dependent-variable structure, data structure, identification strategy, unobserved-heterogeneity strategy, controls, and inference needs to appropriate Stata model families.

This is a model-selection and specification-planning skill. It should not clean raw data, construct new analysis variables, choose controls by statistical significance, or run final hypothesis-testing regressions as though the empirical analysis were complete. Its output should be a transparent recommendation package explaining which estimator family should be primary, which alternatives should be considered, which diagnostics must be completed, what results must be reported, and what risks remain before the model-specific implementation skill is invoked. For mediation claims, the skill must distinguish descriptive mechanism evidence from causal mediation decomposition and must choose among `mediate`, two-mediator `mediate`, `sem`, `gsem`, and sequential-equation approaches according to timing, outcome/mediator support, identification assumptions, panel/FE needs, and Stata-version availability.

## Position in the empirical workflow

Use this skill after the user has completed:

1. Research-design-aware archival data preparation.
2. Empirical design audit before modeling.

Expected upstream outputs include `analysis_ready.dta`, `research_context_brief.md`, `model_readiness_memo.md`, `design_audit_report.md`, `pre_model_go_no_go.md`, `model_selection_handoff_memo.md`, `hypothesis_design_audit.csv`, `control_bad_control_audit.csv`, `fixed_effect_clustering_readiness_audit.csv`, `identification_threat_register.csv`, `outcome_support_audit.csv`, and `estimator_readiness_matrix.csv`.

Expected downstream outputs include inputs for model-specific skills such as Stata HDFE/OLS implementation, panel FE/RE/CRE implementation, DID/event-study implementation, IV/control-function implementation, count-model implementation, limited-dependent-variable implementation, treatment-effects/matching implementation, survival-model implementation, dynamic-panel implementation, multilevel-model implementation, SEM/GSEM implementation, or lasso/ML-assisted causal inference implementation.

## When to use this skill

Use this skill when the user wants to:

- Choose an appropriate econometric model family in Stata before implementing analyses.
- Map hypotheses to primary, secondary, and robustness estimator families.
- Decide whether the dependent variable should be modeled as continuous, binary, count, fractional, censored, ordinal, nominal, duration, or repeated-choice data.
- Decide whether the data call for cross-sectional, panel, event-time, repeated cross-sectional, cohort-time, dyadic, network/spatial, time-series, survival, or multilevel estimators.
- Decide whether the identification strategy is associational, panel fixed effects, DID/event study, IV, control function, treatment effects, matching/weighting, RD, synthetic control, dynamic panel, survival, mediation, moderation, or another design.
- Determine diagnostic requirements, reporting requirements, robustness checks, and Stata code skeletons before implementation.

Do not use this skill as a substitute for empirical design audit. If the unit of analysis, timing, treatment construction, control validity, sample restrictions, or identification threats have not been audited, first use the empirical design audit skill.

## Mandatory first step: model-selection intake and confirmation

Before selecting models, Codex must confirm the model-selection contract. If the required information is missing from the upstream audit package or the current conversation, ask the user:

```text
Before I select Stata estimator families, I need to confirm the model-selection contract.

1. Research context: What is the project title, empirical setting, and focal phenomenon?
2. Hypotheses: What are the hypotheses or focal empirical relationships? For each, identify the dependent variable, key independent variable or treatment/event, expected direction, moderators, mediators/mechanisms, and estimand if known.
3. Claim type: Is each hypothesis intended as causal, associational, predictive, descriptive, mechanism, heterogeneity, mediation, or moderation evidence?
4. Dependent-variable support: For each outcome, is it continuous, log-transformed continuous, binary, count, nonnegative continuous, fractional/proportion, ordinal, nominal, censored/truncated, duration/time-to-event, ranking/choice, or network/spatial?
5. Data structure: Is the analysis dataset cross-sectional, repeated cross-sectional, panel, event-time panel, cohort-time panel, dyadic panel, network panel, survival/risk-set, or aggregate time series?
6. Unit and time identifiers: What are the unit ID, time ID, treatment/cohort/event ID, group/category/geography IDs, and cluster candidates?
7. Identification strategy: Is the intended strategy OLS/HDFE, panel FE/RE/CRE, DID/event study, IV/control function, treatment effects/matching, RD, synthetic control, dynamic panel, survival, multilevel, SEM/GSEM, lasso/DML, or another design?
8. Treatment/event/exposure: If applicable, how is treatment or event timing constructed? Is adoption staggered, reversible, continuous/intensity-based, or single-shock?
9. Endogeneity concerns: Are reverse causality, simultaneity, omitted variables, selection, measurement error, algorithmic confounding, spillovers/interference, or dynamic feedback major concerns?
10. Controls and fixed effects: Which controls survived the control/bad-control audit? Which fixed effects are theoretically required, and could any absorb the focal variable?
11. Inference: What is the likely error-correlation structure? Which level should be clustered: unit, treatment group, market/category, geography, dyad, time, or multiple dimensions?
12. Stata environment: Which Stata version will be used? Should recommendations be limited to official Stata commands, or may community-contributed commands be included with installation checks?
13. Output requirements: Do you want a narrative model-selection memo only, a full model-selection package, Stata skeleton `.do` files, or a handoff to a specific model-implementation skill?
```

After receiving the answers, produce a concise model-selection plan and ask the user to confirm or correct it. Proceed only after confirmation or after the user explicitly authorizes proceeding with documented assumptions.

## Required user checkpoints

Codex must not treat model selection as a fully automatic step. It must pause for user review at the following checkpoints unless the user has explicitly requested an autonomous draft with all assumptions documented.

| Checkpoint | When Codex must pause | What Codex must show the user | Approval required before proceeding |
|---|---|---|---|
| C0. Intake confirmation | Before any estimator-family recommendation | Research context, hypotheses, DV/IV/treatment roles, unit/time structure, data structure, claim type, intended identification strategy, controls, FE candidates, clustering candidates, and Stata environment | Yes |
| C1. Upstream readiness checkpoint | After reading the data-preparation and design-audit artifacts | Whether the project is ready, conditionally ready, or blocked; unresolved issues from unit, timing, treatment, control, sample, FE, clustering, and identification audits | Yes if any issue is marked high risk |
| C2. Outcome and data-structure classification checkpoint | Before matching model families | Classification of each dependent variable, including whether it is continuous, log-continuous, binary, count, fractional/proportion, bounded, censored, duration, choice, spatial/network, or latent; classification of cross-section/panel/event-time/dyadic/risk-set structure | Yes |
| C3. Identification and estimand checkpoint | Before naming a primary estimator | Whether each hypothesis is causal, associational, mechanism, moderation, mediation, prediction, or descriptive; proposed estimand such as conditional mean, ATE, ATT/ATET, LATE, dynamic effect, marginal effect, hazard ratio, or probability difference | Yes |
| C3a. Mediation and mechanism checkpoint | Before recommending any mediation estimator | Whether the project claims causal mediation or mechanism evidence; treatment, mediator, and outcome timing; mediator count; mediator ordering; outcome and mediator supports; confounders for treatment-outcome, treatment-mediator, and mediator-outcome paths; whether treatment-induced mediator-outcome confounding is plausible; whether panel FE/HDFE are essential; and whether StataNow two-mediator features are available | Yes for any mediation/mechanism hypothesis |
| C4. Primary-estimator shortlist checkpoint | Before finalizing the recommended estimator family | Ranked shortlist of feasible estimator families, reasons for exclusion, required diagnostics, and whether the choice depends on unresolved assumptions | Yes |
| C5. Specification-strategy checkpoint | Before writing Stata skeletons | Proposed baseline specification, transformations, controls, fixed effects, clustering, interaction/marginal-effects plan, and whether any controls are excluded as bad controls | Yes |
| C6. Community-command checkpoint | Before recommending user-written Stata packages | Official Stata route, optional community-contributed route, installation checks, package names, and why the community command is needed | Yes |
| C7. Robustness and reporting checkpoint | Before exporting the final model-selection package | Robustness plan, diagnostic requirements, fit statistics, coefficient/marginal-effect reporting, figures, and model table notes | Yes |

Codex must record each checkpoint in `output/model_selection/user_checkpoint_log.csv` with the checkpoint ID, decision, user response, assumptions approved, unresolved risks, timestamp, and downstream effect on the model-selection recommendation.

If the user skips a checkpoint, Codex must label the resulting recommendation as `conditional`, list the skipped checkpoint in `docs/assumptions_and_decision_log.md`, and avoid presenting the recommendation as final.

## Required input package

Expect these files when the upstream design audit has been completed:

```text
design_audit_package/
  docs/design_audit_report.md
  docs/pre_model_go_no_go.md
  docs/model_selection_handoff_memo.md
  docs/identification_threat_memo.md
  docs/assumptions_log.md
  output/audits/hypothesis_design_audit.csv
  output/audits/unit_time_structure_audit.csv
  output/audits/timing_and_leakage_audit.csv
  output/audits/treatment_event_construction_audit.csv
  output/audits/outcome_support_audit.csv
  output/audits/control_bad_control_audit.csv
  output/audits/sample_restriction_attrition_audit.csv
  output/audits/fixed_effect_clustering_readiness_audit.csv
  output/audits/identification_threat_register.csv
  output/audits/estimator_readiness_matrix.csv
  output/audits/robustness_seed_plan.csv
analysis_package/
  data/analysis/analysis_ready.dta
  data/analysis/analysis_ready.parquet
  docs/research_context_brief.md
  docs/model_readiness_memo.md
  output/audits/hypothesis_register.csv
  output/audits/hypothesis_variable_map.csv
  output/audits/control_variable_audit.csv
  output/audits/panel_audit.csv
  output/tables/summary_statistics_isr_main.tex
```

If these artifacts are missing, ask for the missing design information and create a minimal model-selection intake record. If the upstream design audit has classified the project as `not ready`, do not select a primary estimator. Instead, return a blocking-issue memo and list what must be resolved.

## Required output package

Create a folder named `stata_model_selection_package/` unless the user specifies another location. It should contain:

| Artifact | Purpose |
|---|---|
| `docs/model_selection_report.md` | Main narrative report explaining the recommended primary estimator family, alternatives, assumptions, diagnostics, reporting needs, and unresolved risks. |
| `docs/estimator_recommendation_memo.md` | Concise memo for manuscript planning: why the model fits the hypotheses and design. |
| `docs/specification_strategy_memo.md` | Explains baseline specification, control strategy, fixed effects, clustering, transformations, and interaction/marginal-effects plan. |
| `docs/stata_implementation_handoff_memo.md` | Handoff to model-specific Stata implementation skills. |
| `docs/assumptions_and_decision_log.md` | User-approved assumptions, model-selection decisions, rejected estimator families, skipped checkpoints, and reasons. |
| `docs/user_checkpoint_protocol.md` | Required user checkpoints and approval logic for model selection. |
| `docs/fractional_model_selection_notes.md` | Specific guidance for fractional, proportion, share, percentage, and bounded outcomes. |
| `output/model_selection/model_selection_intake.yaml` | Machine-readable intake record. |
| `output/model_selection/user_checkpoint_log.csv` | Record of checkpoint prompts, user approvals, assumptions, and unresolved risks. |
| `output/model_selection/hypothesis_model_map.csv` | One row per hypothesis/outcome: claim type, DV support, data structure, primary estimator, alternatives, diagnostics, reporting, and robustness. |
| `output/model_selection/estimator_recommendation_matrix.csv` | Candidate estimator families with readiness, fit, advantages, limitations, and selection status. |
| `output/model_selection/specification_blueprint.csv` | Baseline equation components: DV, focal IV/treatment, controls, FE, clustering, transformations, interactions, lags/leads. |
| `output/model_selection/diagnostics_requirements.csv` | Diagnostics required before or during implementation for each selected estimator family. |
| `output/model_selection/reporting_requirements.csv` | Statistics, tables, figures, coefficients, marginal effects, and fit measures that must be reported. |
| `output/model_selection/robustness_plan.csv` | Robustness checks implied by the model family and design threats. |
| `output/model_selection/stata_command_plan.csv` | Stata commands to be used, package status, user-written commands requiring installation, and version notes. |
| `output/model_selection/model_family_rejection_log.csv` | Estimator families considered but rejected, with reasons. |
| `output/model_selection/implementation_skill_routing.csv` | Which model-specific skill should be invoked next. |
| `stata/00_model_selection_skeleton.do` | Stata skeleton for setup, data declaration, diagnostic pre-checks, and placeholder model commands. |
| `stata/01_diagnostics_shell.do` | Stata diagnostic shell for data structure, outcome support, FE variation, and cluster counts. |
| `stata/02_reporting_shell.do` | Stata shell for table/figure export placeholders. |

## Model-selection principles

1. Start from the research question and estimand, not from a preferred Stata command.
2. Distinguish associational, causal, mechanism, heterogeneity, mediation, prediction, and descriptive claims. Do not recommend a causal estimator merely because the project uses archival data.
3. Match the estimator to the dependent-variable support. Continuous, binary, count, fractional, censored, ordinal, nominal, choice, duration, and network/spatial outcomes imply different model families and reporting conventions.
4. Match the estimator to the data structure. Cross-sections, repeated cross-sections, panels, event-time panels, dyads, risk sets, hierarchical data, and aggregate time series have different identifying variation and error structures.
5. Respect the empirical design audit. If timing, treatment construction, controls, sample restrictions, or identification threats are unresolved, produce a conditional recommendation rather than a definitive model choice.
6. Treat control variables as design variables. Use the upstream control/bad-control audit; do not add controls because they improve fit or significance.
7. Treat fixed effects as identifying restrictions. Before recommending fixed effects, check that the focal variables vary within the proposed absorbed dimensions.
8. Treat clustering as part of identification and inference. Cluster at the treatment-assignment, sampling, or serial-correlation level when applicable; consider multiway clustering, wild-cluster bootstrap, or randomization inference when the design requires it.
9. For nonlinear models, plan marginal effects or predicted quantities. Do not rely only on raw logit/probit/count-model coefficients for substantive interpretation.
10. For interactions, plan marginal effects, simple slopes, plots, or contrasts. Do not interpret interaction coefficients mechanically in nonlinear models.
11. For DID/event-study designs, prioritize treatment timing, comparison groups, no-anticipation, parallel-trends evidence, cohort heterogeneity, and spillovers before choosing a command.
12. For IV/control-function designs, never recommend the estimator without documenting instrument relevance, exclusion logic, timing, first-stage diagnostics, weak-IV diagnostics, and overidentification tests when applicable.
13. For mediation claims, never recommend treating the mediator as an ordinary control in the main-effect model. First classify the analysis as causal mediation, mechanism evidence, or robustness decomposition; then verify temporal ordering, confounding assumptions, and estimator feasibility.
14. For count and nonnegative outcomes, do not assume log-transformed OLS is sufficient. Consider Poisson/PPML, negative binomial, exposure/offset, zero inflation, and HDFE feasibility.
14. Use the simplest credible estimator as the primary model and reserve more elaborate estimators for robustness or mechanism tests unless the research design requires complexity.
15. Use cautious language: “recommended primary family,” “conditional alternative,” “diagnostic required before implementation,” and “not appropriate under current design.”

## Decision hierarchy

For each hypothesis or focal empirical relationship, follow this hierarchy:

### 1. Claim type and estimand

Classify the hypothesis as one of:

- Association or conditional correlation.
- Causal average effect: ATE, ATT/ATET, LATE, ITT, dose-response, dynamic effect.
- Mechanism or mediation.
- Moderation or heterogeneity.
- Prediction/classification.
- Descriptive decomposition.
- Structural or latent-construct relationship.

The claim type determines whether ordinary regression is sufficient or whether a design-based estimator is needed.

### 1a. Mediation and mechanism-specific decision module

If any hypothesis uses language such as mechanism, mediation, pathway, channel, portability through, spillover through, explanation, indirect effect, or process, Codex must run a mediation/mechanism checkpoint before choosing a model family. The checkpoint must separate three different empirical claims:

| Claim type | What it means | Model-selection implication |
|---|---|---|
| Mechanism evidence | The treatment/key IV predicts a theoretically intermediate variable, and that variable is associated with the outcome in a temporally coherent way. | Sequential equations or panel/HDFE models may be sufficient, but do not label the estimate as a causal indirect effect unless causal mediation assumptions are defended. |
| Causal mediation | The goal is to decompose a causal total effect into natural direct effect, natural indirect effect, controlled direct effect, proportion mediated, or path-specific effects. | Prefer Stata's official `mediate` family when outcome/mediator/treatment support and assumptions match; otherwise consider `sem`/`gsem` or sequential equations with explicit limitations. |
| Measurement/path model | The theory involves latent constructs, multiple indicators, path analysis, or simultaneous structural equations. | Consider `sem` for linear observed/latent models or `gsem` for generalized, multilevel, and nonlinear path models. |

Codex must ask or infer the following before selecting a mediation model:

1. Is the treatment or focal independent variable measured before the mediator?
2. Is the mediator measured before the outcome?
3. Is the mediator post-treatment but pre-outcome, rather than a contemporaneous outcome or post-outcome variable?
4. How many mediators are focal: one, two, or more than two?
5. If there are two mediators, are they parallel or sequentially ordered?
6. What is the support of the outcome and each mediator: continuous, binary, count, fractional, ordinal, nominal, censored, duration, or latent?
7. Are the treatment, mediator, and outcome equations expected to require the same covariates, different covariates, fixed effects, random effects, or clustering?
8. Are there observed pretreatment confounders for treatment-outcome, treatment-mediator, and mediator-outcome paths?
9. Is any mediator-outcome confounder itself caused by the treatment?
10. Are spillovers/interference plausible, especially in network/platform settings?
11. Are unit fixed effects, high-dimensional fixed effects, or staggered event-time structure essential for identification?
12. Should the output be interpreted as causal decomposition, mechanism evidence, or descriptive path association?

Use the following mediation model routing table:

| Mediation setting | Candidate Stata family | Select when | Do not select when |
|---|---|---|---|
| One observed mediator; causal decomposition target | `mediate` | Outcome and mediator are continuous, binary, or count; treatment is binary, multivalued, or continuous; the researcher can defend causal mediation assumptions. | Required outcome/mediator support is outside `mediate`; panel/HDFE structure is essential and unsupported; mediator timing or confounding assumptions fail. |
| Two observed mediators; causal decomposition target | `mediate` with two mediators, where available in StataNow | Two mediators are theoretically parallel or sequential; current Stata environment supports this feature; documented support/assumptions match the command. | User's Stata version lacks the feature; more than two mediators are required; outcome/mediator support is unsupported; ordering of mediators is unclear. |
| Linear path model or latent constructs | `sem`, with `estat teffects`, `nlcom`, or equivalent postestimation as needed | Theory requires latent variables, measurement models, multiple indicators, path models, direct/indirect effects, group invariance, or SEM fit indices. | Outcome/mediator responses require generalized links or multilevel structure that `sem` cannot represent; causal mediation assumptions are not defensible but causal language is planned. |
| Generalized, nonlinear, multilevel, or mixed-response path model | `gsem`, with `nlcom`, `margins`, and simulation/bootstrap where needed | Outcomes or mediators are binary, count, ordinal, fractional, survival, or multilevel; random effects or generalized links are substantively required. | Effects are to be interpreted as natural direct/indirect causal effects but the estimands are not aligned with `gsem` output; model is unidentified or convergence is unreliable. |
| Panel/HDFE mechanism evidence | Base estimator family for each equation, plus `nlcom`/bootstrap for product-of-coefficients where appropriate | Unit FE, time FE, dyad FE, or HDFE are essential; the goal is mechanism evidence rather than formal causal mediation decomposition. | The manuscript claims natural direct/indirect effects without defending additional mediation assumptions; mediator is a bad control in the main-effect equation. |
| Simple classical mediation in cross-sectional data | Sequential `regress`/`logit`/`poisson` equations plus `nlcom` or bootstrap | Used as a transparent exploratory or robustness decomposition, especially in older Stata versions. | Nonlinear scaling, unobserved confounding, or post-treatment confounding makes product-of-coefficients interpretation misleading. |

Required diagnostics for mediation and mechanism analyses:

- Timing audit: treatment/key IV precedes mediator, mediator precedes outcome, and lags/windows do not use future information.
- Confounding audit: treatment-outcome, treatment-mediator, and mediator-outcome confounders are identified and measured pretreatment where needed.
- Treatment-induced confounder audit: no mediator-outcome confounder should itself be caused by treatment unless an advanced design explicitly handles it.
- Support audit: outcome and mediator supports match the selected command; boundary, zero, count, binary, or latent status is correctly handled.
- FE and clustering audit: required unit/time/category/dyad FE and cluster levels are feasible in the selected family.
- Identification language audit: causal mediation language is permitted only when assumptions are explicitly stated; otherwise label the analysis as mechanism evidence.
- Model fit/convergence audit: SEM/GSEM models require identification, convergence, and fit checks; `mediate` models require auxiliary-equation and overlap/support checks.

Required reporting for mediation and mechanism analyses:

- A causal/path diagram or table listing treatment, mediator(s), outcome, timing, and hypothesized path direction.
- Selected model family and why alternatives were rejected.
- Direct, indirect, total, controlled direct effects, potential-outcome means, or path coefficients as appropriate to the selected family.
- Effect scale: risk difference, odds ratio, risk ratio, incidence-rate ratio, coefficient scale, or marginal-effect scale.
- Treatment-mediator and mediator-mediator interaction handling.
- Auxiliary equation specifications for outcome and mediator models.
- Covariates in each equation, fixed effects, clustering, sample restrictions, and Stata version/command availability.
- Robustness checks: alternative mediator timing, alternative mediator measures, direct-effect-only model, placebo mediator/outcome, bootstrap or simulation CIs, and sensitivity analysis when available.

Hard stops for mediation:

- The mediator is measured before the treatment but interpreted as a post-treatment mechanism.
- The mediator is measured after or simultaneously with the outcome and no temporal justification is provided.
- The proposed main-effect model includes the mediator as a control while still interpreting the total treatment effect.
- The analysis claims causal mediation but has no mediator-outcome confounding plan.
- A treatment-induced mediator-outcome confounder is plausible and unaddressed.
- Stata's `mediate` is recommended for an unsupported outcome, mediator, treatment, or FE structure.
- Multiple mediators are proposed but their theoretical ordering is unclear.

### 2. Dependent-variable support

Classify the dependent variable before selecting a command:

| Outcome support | Candidate Stata families |
|---|---|
| Continuous or approximately continuous | `regress`, `areg`, `xtreg`, `mixed`, `glm`, `qreg`, HDFE commands. |
| Log-transformed continuous | Same as continuous, with transformation diagnostics and percentage interpretation. |
| Binary | `regress` as LPM when justified, `logit`, `probit`, `logistic`, `clogit`, `xtlogit`, `xtprobit`, `melogit`, `meprobit`, `eprobit`. |
| Count | `poisson`, `nbreg`, `gnbreg`, `xtpoisson`, `xtnbreg`, `mepoisson`, `menbreg`, `zip`, `zinb`, `tpoisson`, `tnbreg`, PPML/HDFE alternatives. |
| Nonnegative skewed continuous | `glm`, PPML-like approaches, transformed OLS, two-part/hurdle models where appropriate. |
| Fraction/proportion/share/rate bounded in [0,1] | `fracreg logit`, `fracreg probit`, `glm` with fractional logit-style mean specification, `betareg` for open-interval proportions, two-part/hurdle models if many structural 0/1 values, and linear FE as a robustness approximation when fixed effects are central and carefully justified. |
| Ordinal | `ologit`, `oprobit`, `meologit`, `meoprobit`, `gsem`. |
| Nominal/category choice | `mlogit`, `mprobit`, `clogit`, `nlogit`, `asclogit`, `cmclogit`, `cmmixlogit`, `cmxtmixlogit`. |
| Censored/truncated/corner solution | `tobit`, `intreg`, `truncreg`, `xttobit`, `churdle`, `heckman`, `eregress/eintreg` where endogenous selection/treatment exists. |
| Duration/time to event | `stset`, `stcox`, `streg`, `stcrreg`, `mestreg`, `stteffects`. |
| Repeated choices/rankings | choice-model commands, panel choice models, conditional logit, mixed logit. |
| Latent constructs/path relationships | `sem`, `gsem`, `mediate` when causal mediation assumptions and support match, `nlcom`/bootstrap for path products, latent-class or finite-mixture commands. |
| Spatial/network spillover | `spmatrix`, `spregress`, `spxtregress`, `spivregress`, network-lag or exposure models. |

#### Fractional-response and bounded-outcome decision rules

When the dependent variable is a share, proportion, percentage, ratio, engagement rate, market share, retention share, conversion rate, percentage of AI-generated work, share of token holdings, or any variable naturally bounded in `[0,1]`, Codex must perform a separate fractional-outcome checkpoint before recommending OLS.

Codex must classify the fractional outcome into one of these cases:

| Fractional outcome case | Preferred family to consider | Key caution |
|---|---|---|
| Continuous proportion with valid 0 and/or 1 values | Fractional response model, usually `fracreg logit` or `fracreg probit` | Report marginal effects or predicted proportions; check mass at boundaries. |
| Proportion strictly inside `(0,1)` | `betareg` or fractional response model | Beta regression is inappropriate if unmodeled exact 0/1 values are common. |
| Share with many structural zeros | Two-part model: first model positive share, then conditional fractional/beta model | Distinguish true zeros from missing/non-exposure. |
| Share with many structural ones | Boundary-aware fractional model or two-part/boundary-mass strategy | Explain why ones are structural, not data errors. |
| Fractional outcome in panel with essential unit FE | Compare fractional response, linear FE approximation, HDFE OLS, and robustness alternatives | FE may be central for identification, but nonlinear FE can change sample and interpretation. |
| Fractional outcome based on a numerator/denominator process | Consider binomial/logit-style GLM using numerator and denominator where available | Requires denominator and event-count interpretation. |

Required diagnostics for fractional outcomes: support check, boundary mass at 0 and 1, denominator/exposure definition when applicable, missingness and true-zero audit, link-function rationale, predicted-value range, marginal-effects plan, fixed-effect feasibility, clustering level, and robustness to alternative fractional/linear specifications.

Required reporting for fractional outcomes: N, outcome scale, mean and boundary mass, estimator/link, coefficients plus average marginal effects or predicted proportions, fixed effects, clustering, sample restrictions, and interpretation in percentage-point or proportional terms.

### 3. Data structure

Classify the dataset:

| Data structure | Model-selection implication |
|---|---|
| Cross-sectional | Use cross-sectional regression, GLM, limited-DV, treatment-effects, IV, selection, matching, RD, SEM, or spatial models as warranted. |
| Repeated cross-sectional | Consider pooled models with time FE, `didregress`, treatment effects, repeated-cross-section DID, or time-clustered inference. |
| Panel | Consider `xtset`; panel FE/RE/CRE, HDFE, dynamic panel, panel count/binary models, panel IV, panel DID, or cluster-robust pooled models. |
| Event-time panel | Consider event-study/DID/synthetic-control designs; verify event-time support, anticipation, comparison group, and cohort heterogeneity. |
| Cohort-time panel | Consider cohort-specific DID, staggered adoption methods, cohort-by-time FE, or grouped event-study approaches. |
| Dyadic or network panel | Consider dyad FE, sender/receiver FE, network spillover measures, multiway clustering, or spatial/network models. |
| Hierarchical/nested data | Consider multilevel/mixed models or fixed effects depending on estimand and within-cluster variation. |
| Survival/risk-set data | Use `stset`; select Cox, parametric survival, competing-risk, or survival treatment-effects models. |
| Aggregate time series | Use `tsset`; consider ARIMA, VAR, VEC, GARCH, local projections, interrupted time series, or Newey-West/HAC inference. |

### 4. Identification strategy

Select by design logic:

| Identification strategy | Candidate Stata family | Required before selection |
|---|---|---|
| Conditional association | OLS/GLM/panel/HDFE/limited-DV family matching outcome support. | Valid timing and controls; no causal overclaim. |
| Unit-level unobserved heterogeneity | `xtreg, fe`, `areg`, HDFE, `xtreg, cre`, `mixed` where appropriate. | Within-unit variation in focal variables; FE absorption audit. |
| DID / event study | `didregress`, `xtdidregress`, `hdidregress`/`xthdidregress` if available, HDFE event-study regressions, community `csdid`, `eventstudyinteract`, `did_imputation`. | Valid treatment timing, untreated/not-yet-treated comparison, no anticipation, pretrend/event-time support, cluster level. |
| Staggered adoption DID | Heterogeneous DID/event-study estimators preferred; simple TWFE only as descriptive baseline or under defensible homogeneity assumptions. | Cohort structure, dynamic effects, treatment reversibility, comparison group, negative-weight/heterogeneity risk. |
| IV / LATE | `ivregress 2sls`, `ivregress liml`, `ivregress gmm`, `xtivreg`, `ivprobit`, `ivtobit`, `ivpoisson`. | Instrument relevance, exclusion restriction, timing, first-stage, weak-IV diagnostics, overidentification where possible. |
| Control function | `cfregress`, `cfprobit`, extended-regression commands. | Endogenous-variable model, excluded variables, correct first-stage family, endogeneity tests. |
| Selection on observables | `teffects ra/ipw/ipwra/aipw/psmatch/nnmatch`, lasso treatment effects. | Pre-treatment covariates, overlap/common support, balance diagnostics, treatment assignment model. |
| Regression discontinuity | Community `rdrobust` or local polynomial implementation. | Running variable, cutoff, manipulation test, covariate continuity, bandwidth plan. |
| Synthetic control / synthetic DID | Community `synth`, `sdid`, related commands. | Few treated units or aggregate treatment, donor pool, pre-treatment fit, placebo inference. |
| Dynamic feedback / lagged DV | `xtabond`, `xtdpdsys`, `xtdpd`, panel VAR tools. | Panel length, lag structure, instrument count, serial-correlation tests, overidentification tests. |
| Mediation/mechanism | `mediate` for official causal mediation with supported outcome/mediator/treatment structure; StataNow two-mediator `mediate` when available; `sem` for linear/latent path models; `gsem` for generalized or multilevel path models; sequential base-equation models with `nlcom`/bootstrap for mechanism evidence. | Treatment-mediator-outcome timing; mediator count and ordering; no post-treatment control misuse in main model; mediator-outcome confounding plan; causal mediation assumptions; FE/clustering feasibility; Stata version availability. |
| Moderation/heterogeneity | Interactions in appropriate base model; `margins`, `contrast`, `lincom`, subgroup or interacted FE models. | Moderator timing, scale, collinearity, nonlinear interaction interpretation plan. |
| Spillovers/interference | Network/spatial exposure models, spatial autoregressive models, cluster-level treatment exposure, or design redefinition. | Exposure mapping, SUTVA violation memo, direct/indirect effect definitions, appropriate clustering. |

### 5. Fixed effects, random effects, and multilevel structure

Use this hierarchy:

1. If the estimand requires within-unit changes and unobserved unit heterogeneity may correlate with regressors, prefer unit fixed effects or HDFE, provided the focal variable has within-unit variation.
2. If time-invariant regressors are focal and correlated heterogeneity is plausible, consider correlated random effects (`xtreg, cre`) before defaulting to random effects.
3. If the purpose is to model hierarchical variance, partial pooling, or random slopes, consider multilevel models (`mixed`, `melogit`, `mepoisson`, etc.).
4. Do not choose random effects merely because fixed effects absorb a desired variable. The identifying assumption must be credible.
5. For high-dimensional categorical controls, prefer Stata’s official `absorb()` options where available or approved community HDFE commands.

### 6. Inference structure

Select standard errors before implementation:

| Error structure | Recommended inference plan |
|---|---|
| Heteroskedastic cross-sectional errors | Robust or HC corrections. |
| Repeated observations within unit | Cluster at unit or treatment-assignment level. |
| Group-level treatment | Cluster at treatment-assignment group; consider wild-cluster bootstrap if few clusters. |
| Two correlated dimensions, such as unit and time or dyad endpoints | Multiway clustering where supported; otherwise approved community command or bootstrap strategy. |
| Time-series autocorrelation | HAC/Newey-West or time-series model. |
| Spatial/network correlation | Spatial/network model or appropriate clustered/randomization inference. |
| Survey sample | `svy:` with design weights, strata, and PSUs. |
| Multiple imputation | `mi estimate:` with imputation diagnostics. |

## Stata model-family registry

The skill should use `templates/metadata/stata_model_family_registry.csv` as the canonical registry. At minimum, include these families in the selection space:

- Linear/OLS/HDFE: `regress`, `areg`, `xtreg, fe absorb()`, `ivregress 2sls, absorb()`, optional `reghdfe`.
- Panel: `xtreg, fe`, `xtreg, re`, `xtreg, be`, `xtreg, pa`, `xtreg, cre`, `xtgls`, `xtpcse`, `xtgee`.
- GLM and robust alternatives: `glm`, `qreg`, `rreg`, `fracreg`, `betareg`.
- Binary: `logit`, `logistic`, `probit`, `cloglog`, `clogit`, `xtlogit`, `xtprobit`, `melogit`, `meprobit`, `eprobit`.
- Ordinal/nominal/choice: `ologit`, `oprobit`, `mlogit`, `mprobit`, `nlogit`, `asclogit`, `cmclogit`, `cmmixlogit`, `cmxtmixlogit`, `meologit`, `meoprobit`.
- Count: `poisson`, `nbreg`, `gnbreg`, `zip`, `zinb`, `tpoisson`, `tnbreg`, `xtpoisson`, `xtnbreg`, `mepoisson`, `menbreg`, optional `ppmlhdfe`.
- Limited outcomes and selection: `tobit`, `intreg`, `truncreg`, `xttobit`, `churdle`, `heckman`, `heckprobit`.
- Endogeneity: `ivregress`, `xtivreg`, `ivprobit`, `ivtobit`, `ivpoisson`, `cfregress`, `cfprobit`, `eregress`, `eprobit`, `eintreg`, `eoprobit`.
- Treatment effects and causal inference: `teffects`, `stteffects`, `didregress`, `xtdidregress`, `hdidregress`, `xthdidregress` if available, lasso treatment-effects commands, optional community DID/synthetic-control commands.
- Dynamic panel: `xtabond`, `xtdpdsys`, `xtdpd`, panel VAR commands where available.
- Time series: `arima`, `arfima`, `var`, `svar`, `vec`, `newey`, `prais`, `garch`, `sspace`, local projections.
- Survival: `stset`, `stcox`, `streg`, `stcrreg`, `mestreg`.
- Multilevel: `mixed`, `menl`, `melogit`, `meprobit`, `mepoisson`, `menbreg`, `meologit`, `meoprobit`, `metobit`, `mecloglog`, `mestreg`.
- Mediation and mechanism models: official `mediate` for one-mediator causal mediation; two-mediator `mediate` where available in StataNow; `sem` for linear and latent path models; `gsem` for generalized, nonlinear, multilevel, or mixed-response mediation/path models; sequential base-equation models with `nlcom`, `bootstrap`, or `simulate` for mechanism evidence when FE/HDFE or panel structure is central.
- SEM/GSEM/path models: `sem`, `gsem`, `estat teffects` where available, `nlcom`, `testnl`, `margins`, `predict`, `estat mindices`, `estat gof`, and group-invariance tools as appropriate.
- Spatial/network: `spmatrix`, `spregress`, `spxtregress`, `spivregress`.
- Lasso/ML-assisted inference: `lasso`, `elasticnet`, `sqrtlasso`, `dsregress`, `poregress`, `xporegress`, `telasso`, optional `ddml`.
- Bayesian and mixtures: `bayes:`, `bayesmh`, `fmm:`, latent-class models.
- Survey/MI/resampling prefixes: `svy:`, `mi estimate:`, `bootstrap:`, `jackknife:`, `permute:`.

## Required diagnostics by selected family

For every selected family, populate `diagnostics_requirements.csv`. Required diagnostics include:

| Family | Required diagnostics |
|---|---|
| OLS/HDFE | Outcome distribution; residual scale; heteroskedasticity; influential observations; multicollinearity among non-absorbed covariates; FE absorption; within-FE variation; cluster counts. |
| Panel FE/RE/CRE | `xtset`; panel balance/gaps; within/between variation; time-invariant variables; FE vs RE/CRE logic; serial correlation; cluster plan. |
| DID/event study | Treatment timing; comparison group; pre-treatment support; no-anticipation window; pretrend tests/plots; cohort heterogeneity; event-time binning; spillovers; treatment reversibility. |
| IV/control function | First-stage relevance; weak-IV diagnostics; reduced form; overidentification when applicable; endogeneity test; exclusion-restriction memo; first-stage functional form. |
| Binary/ordinal/nominal | Outcome prevalence; rare events; separation/perfect prediction; link function; marginal effects; classification only if predictive claim. |
| Count/nonnegative | Zero mass; overdispersion; exposure/offset; separation for Poisson/HDFE; IRR/marginal-effects plan; alternative count vs transformed OLS specification. |
| Fractional/bounded | Support and boundary mass at 0/1; denominator/exposure audit; true zero vs missing; link function; predicted-value range; marginal effects; two-part/beta/fractional choice; FE feasibility; scale interpretation. |
| Censored/truncated/selection | Censoring/truncation rule; true zero vs non-observation; selection equation; exclusion restriction for selection; latent vs observed effect. |
| Treatment effects/matching | Overlap/common support; balance before/after; standardized mean differences; propensity distribution; dropped observations; sensitivity to caliper/model. |
| RD | Running variable density; cutoff manipulation; covariate continuity; bandwidth; polynomial order; donut test; alternative bandwidths. |
| Survival | Valid `stset`; risk set; censoring; event count; proportional hazards; competing risks; time-varying covariates. |
| Dynamic panel | Lag structure; AR(1)/AR(2); Hansen/Sargan; instrument count; collapsed instruments; finite-sample concerns. |
| Multilevel | Cluster sizes; random-intercept/slope logic; ICC; convergence; covariance structure; random-effect distribution; cross-classification. |
| Mediation/mechanism | Treatment-mediator-outcome timing; mediator count and ordering; mediator/outcome support; confounding assumptions for treatment-outcome, treatment-mediator, and mediator-outcome paths; treatment-induced confounders; FE/clustering feasibility; overlap/support; interaction terms; scale of effects; bootstrap/simulation CIs when needed. |
| SEM/GSEM/path models | Model identification; measurement validity; fit indices for SEM; convergence for GSEM; indirect/path effects; group invariance where relevant; bootstrapped or delta-method CIs; temporal ordering of mediator. |
| Spatial/network | Weight matrix/exposure definition; spatial/network dependence; direct/indirect/total effects; alternative network definitions. |
| Lasso/DML | Candidate control set; folds/seeds; tuning method; selected variables; cross-fitting; post-selection inference; out-of-sample performance when predictive. |

## Reporting requirements

For each selected family, populate `reporting_requirements.csv`. At minimum:

- Always report sample size, unit of analysis, observation window, sample restrictions, dependent-variable definition, key independent-variable/treatment definition, controls, fixed effects, clustering level, and software/package versions.
- Linear models: coefficients, standard errors, p-values or confidence intervals, R-squared, adjusted/within R-squared where meaningful, number of units/groups, fixed effects, clustering, and Root MSE if relevant.
- Nonlinear models: marginal effects or predicted probabilities/counts, not only raw coefficients; log likelihood, pseudo R-squared, AIC/BIC where appropriate.
- Panel models: number of units, number of periods, observations per unit, within/between/overall R-squared where available.
- DID/event studies: ATT/ATET, group/time identifiers, event-time coefficient plot, pretrend tests, omitted event period, treatment cohorts, cluster level, and robustness to event windows.
- IV/control-function models: first-stage results, weak-IV diagnostics, endogeneity tests, overidentification tests, reduced form, and instrument-validity rationale.
- Count models: IRRs or marginal effects, exposure/offset, alpha/overdispersion where relevant, zero mass, and fit comparison where useful.
- Fractional/bounded models: outcome scale and support, boundary mass at 0/1, estimator/link, marginal effects or predicted proportions, FE/clustering, and interpretation in percentage points or proportions.
- Treatment-effects/matching: ATE/ATET/POM, overlap and balance diagnostics, treatment model, outcome model, and dropped observations.
- Survival models: hazard ratios or survival-time ratios, subjects, failures, time at risk, censoring, PH diagnostics, and survival/hazard plots when useful.
- Dynamic panel: lagged DV coefficient, AR(1)/AR(2), Hansen/Sargan, instrument count, number of groups, periods, and instrument strategy.
- Multilevel models: random-effect variance components, ICC, cluster sizes, convergence status, and marginal/predicted effects.
- Mediation: treatment, mediator(s), and outcome timing; model family; auxiliary equation specifications; direct, indirect, total, controlled direct, path-specific, and proportion-mediated effects where applicable; effect scale; interaction handling; covariates in each equation; fixed effects and clustering; assumptions for causal interpretation; and robustness/sensitivity checks.
- SEM/GSEM: path coefficients, direct/indirect/total effects, model fit where applicable, factor loadings for measurement models, convergence status for GSEM, and identification notes.

## Robustness planning

For each selected primary estimator, create a robustness plan. Typical checks include:

| Primary family | Robustness candidates |
|---|---|
| OLS/HDFE | Alternative transformations; alternative FE sets; alternative clusters; winsorized/unwinsorized outcomes; lagged controls; placebo outcomes; subsamples. |
| Panel FE | CRE/RE comparison when time-invariant variables matter; lagged DV sensitivity; unit-specific trends; alternative clustering; balanced-panel subsample. |
| DID/event study | Alternative windows; placebo treatment dates; fake-treated groups; alternative comparison groups; cohort-specific estimates; excluding early/late adopters; dynamic effects. |
| IV | Alternative instruments; LIML vs 2SLS; weak-IV robust confidence intervals; reduced form; overidentified subsets; falsification outcomes. |
| Count | Poisson vs negative binomial; PPML/HDFE; transformed OLS; exposure/offset alternatives; zero-inflated/hurdle checks. |
| Binary | Logit/probit/LPM comparison; rare-event correction if needed; marginal-effects robustness; FE-logit vs LPM FE where appropriate. |
| Treatment effects | Alternative propensity models; IPW vs AIPW/IPWRA; matching ratio/caliper; overlap trimming; balance sensitivity. |
| Survival | Cox vs parametric survival; PH violations; alternative time scales; competing-risk model; censoring sensitivity. |
| Dynamic panel | Instrument lag depth; collapsed instruments; difference vs system GMM; restricting instrument count; excluding short panels. |
| Multilevel | Fixed-effects alternative; random-slope alternatives; cluster-size restrictions; covariance structure alternatives. |
| Mediation/mechanism | Alternative mediator timing/lags; alternative mediator measures; nointeraction vs interaction specifications; bootstrap/simulation CIs; direct-effect-only model; placebo mediator/outcome; alternative confounder sets; sensitivity analysis where available; sequential vs parallel mediator ordering if theory permits. |
| SEM/GSEM/path models | Alternative measurement model; alternative link functions; direct-effect-only model; group invariance constraints; random-effect structure; convergence and starting-value sensitivity. |

## Hard-stop and high-risk conditions

Stop and ask for clarification before recommending a primary estimator if any of these hold:

- The upstream design audit says `not ready`.
- Unit of analysis is unknown or row key is not unique.
- Dependent-variable support is unknown or inconsistent with proposed model family.
- Treatment/event timing is unclear or uses post-outcome information.
- Key controls are post-treatment, mediators, colliders, or mechanically related to the outcome, and the user has not authorized their exclusion.
- Proposed fixed effects absorb the focal variable and no alternative specification is planned.
- DID/event-study design lacks comparison units, pre-treatment periods, or valid event timing.
- Staggered treatment adoption is present and the plan relies only on simple TWFE without heterogeneity diagnostics or justification.
- IV design lacks a credible exclusion restriction or first-stage relevance plan.
- Matching/treatment-effects design lacks overlap/common support diagnostics.
- Mediation is claimed but mediator timing, mediator-outcome confounding, treatment-induced confounding, mediator ordering, or Stata command support is unresolved.
- Count, binary, fractional/proportion, bounded, or survival outcomes are modeled as continuous without justification and robustness.
- Cluster count is too small for conventional clustered inference and no small-cluster strategy is proposed.
- Spillovers/interference are theoretically central but the proposed model assumes no interference.

## Stata command planning rules

1. Use official Stata commands as the default recommendation.
2. Ask whether community-contributed commands are allowed. If yes, include installation checks and package/version documentation.
3. Record Stata version. If the user uses an older Stata version, avoid commands not available in that version or provide fallback commands.
4. When generating `.do` files, include `version`, `log using`, `set more off`, `datasignature`, path macros, `xtset`/`tsset`/`stset` placeholders, package checks, diagnostics placeholders, model placeholders, and export placeholders.
5. Do not write final model code with real variable names unless the required variable map has been confirmed.
6. For nonlinear models, include `margins` and `marginsplot` placeholders.
7. For interactions, include `lincom`, `margins`, `contrast`, and coefficient-plot placeholders where appropriate.
8. For mediation, include `mediate`/`sem`/`gsem`/sequential-equation placeholders as selected; include auxiliary-equation displays, direct/indirect/total/CDE/proportion-mediated output where supported, `estat effectsplot`/path plots where useful, and `nlcom`/bootstrap placeholders for product-of-coefficients or path-specific quantities when appropriate.
9. For DID/event studies, include event-time construction checks, pretrend diagnostics, and coefficient-plot placeholders.
9. For IV, include first-stage, weak-IV, overidentification, and endogeneity-test placeholders.
10. For all models, include table notes documenting sample, fixed effects, controls, clustering, and transformations.

## Model-selection report structure

The narrative report should use this structure:

1. Project and hypothesis overview.
2. Upstream readiness summary from the design audit.
3. Dependent-variable and data-structure classification.
4. Claim type and estimand classification by hypothesis.
5. Recommended primary estimator family by hypothesis.
6. Alternative estimators considered and rejected.
7. Control, fixed-effect, and clustering strategy.
8. Mediation/mechanism routing, if any: mediator timing, mediator ordering, direct/indirect estimands, and whether the claim is causal mediation or mechanism evidence.
9. Required diagnostics before implementation.
9. Reporting requirements for manuscript tables/figures.
10. Robustness and sensitivity plan.
11. Stata command plan and package/version dependencies.
12. Handoff to model-specific implementation skill.
13. Assumptions and unresolved risks.

## Output quality standards

- Every recommendation must be tied to a hypothesis, outcome, data structure, identification strategy, and diagnostic requirement.
- The report must explicitly explain why each rejected family is less appropriate.
- The primary estimator family should be clearly separated from robustness estimators.
- The skill must not use a model merely because it is common in IS research; it must fit the estimand and empirical design.
- If multiple models are plausible, rank them and state what evidence would decide among them.
- Do not skip user checkpoints unless the user explicitly authorizes proceeding with documented assumptions.
- If the empirical design can only support associational evidence, say so directly and recommend language consistent with that limitation.
