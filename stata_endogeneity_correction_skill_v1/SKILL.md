---
name: stata_endogeneity_correction_checks
summary: Diagnose, document, and implement Stata-based endogeneity mitigation strategies for archival empirical IS research, including controls, fixed effects, lagged regressors, IV/2SLS, control-function models, DID/event studies, matching/weighting, dynamic panel GMM, sample-selection models, measurement-error checks, and ISR-style reporting.
description: Use this skill after the empirical design audit and Stata model-selection skill when the project faces or anticipates endogeneity concerns. The skill forces Codex to identify the source of endogeneity, match each threat to defensible correction/check strategies, retrieve official Stata manuals/help for selected commands, run diagnostics before model implementation, pause for user approval at decision points, implement approved Stata commands, export diagnostic and results artifacts, and write a transparent endogeneity strategy memo. It is designed for archival Information Systems research with panel, repeated cross-sectional, cross-sectional, event-time, platform, digital-trace, and firm-level data.
---

# Stata Endogeneity Correction and Checks for Archival IS Research

## Primary goal

Help Codex diagnose and mitigate endogeneity concerns in Stata without treating endogeneity as something that can be mechanically “fixed” by adding a command. The skill should force a research-design-first workflow: identify the source of endogeneity, evaluate which correction strategies are theoretically credible and empirically feasible, run pre-estimation diagnostics, obtain user approval for any specification changes, implement approved Stata models, report diagnostics and results transparently, and generate an endogeneity strategy memo suitable for an IS empirical paper.

This skill is built around the conceptual logic in the user-provided screenshots: endogeneity arises when a focal explanatory variable is correlated with the error term, which can bias regression coefficients, distort coefficient signs or magnitudes, make significance unreliable, and weaken causal interpretation. Common sources include omitted variables, reverse causality, measurement error, and sample-selection bias. Common mitigation strategies include theoretically justified controls, fixed effects, lagged explanatory variables, instrumental variables, DID/event-study designs, propensity score matching/weighting, dynamic panel models, and sample-selection models. The skill adds additional safeguards, diagnostics, Stata-specific implementation details, and reporting templates.

## Position in the empirical workflow

Use this skill after the following upstream artifacts exist, or after the user confirms equivalent information:

1. `analysis_ready.dta` from the data-preparation skill.
2. `model_selection_handoff_memo.md` and `stata_command_plan.csv` from the model-selection skill.
3. `identification_threat_register.csv`, `control_bad_control_audit.csv`, and `fixed_effect_clustering_readiness_audit.csv` from the empirical design audit skill.
4. A clear hypothesis map identifying dependent variables, focal independent variables/treatments/events, controls, moderators, mediators/mechanisms, fixed effects, clustering dimensions, and intended estimands.

This skill can be used in two ways:

- **Endogeneity audit mode**: inspect an empirical design and recommend endogeneity checks/correction strategies before implementation.
- **Implementation mode**: implement the approved Stata strategies and export diagnostics/results.

Do not perform raw-data cleaning or construct new variables unless the transformation is a small, explicitly approved Stata-side diagnostic or robustness variable, such as a lag, placebo treatment, event-time lead/lag, instrument interaction, or matched-sample flag.

## Core rule

Endogeneity mitigation must be tied to a specific identification threat. Codex must not recommend IV, DID, matching, fixed effects, or dynamic panel GMM simply because the model “needs endogeneity correction.” For every method, Codex must state what threat it addresses, what assumptions are required, what assumptions remain untestable, what diagnostics are possible, and what cannot be claimed.

## Required user intake

Before running any endogeneity correction/check, Codex must ask for or locate the following:

1. Research context and empirical setting.
2. Hypotheses and expected directions.
3. Dependent variables and their support.
4. Focal independent variables, treatments, events, or endogenous regressors.
5. Suspected endogeneity source for each focal relationship: omitted variable, reverse causality, simultaneity, measurement error, sample selection, endogenous treatment assignment, dynamic persistence, algorithmic/platform confounding, interference/spillovers, or attrition.
6. Unit of analysis and panel/time structure.
7. Available controls and their timing.
8. Proposed fixed effects and clustering dimensions.
9. Available instruments, policy shocks, thresholds, treatment timing, or matching variables.
10. Whether the user wants the endogeneity correction to be the main model, robustness check, or additional identification analysis.
11. Stata version, installed community commands, and whether community commands are allowed.
12. Table-format target. Default to ISR-style tables modeled on Zhao et al. (2022), with control coefficients included unless the user approves appendix-only controls.

If these elements are missing, stop and ask targeted questions. Do not infer an instrument, treatment event, control set, or identification strategy without user confirmation.

## Mandatory user checkpoints

Codex must pause at the following checkpoints unless the user explicitly requests an autonomous first pass with all assumptions documented.

| Checkpoint | When | What Codex must show | Approval required |
|---|---|---|---|
| C0. Endogeneity intake confirmation | Before writing code | Hypotheses, focal relationships, suspected endogeneity source, available design features, candidate correction strategies, Stata version, and community-command policy | Yes |
| C1. Threat-to-method map | After classifying threats | One row per focal relationship: threat, plausible correction/checks, required assumptions, necessary data support, and what remains unaddressed | Yes |
| C2. Manual/help retrieval | Before implementation | Stata commands to be used, official manual/help sources, community packages, unavailable commands, and version constraints | Yes if any command is missing, community-contributed, or version-sensitive |
| C3. Diagnostic plan | Before running diagnostics | Diagnostics for controls, FE, lagged regressors, IV, DID, matching/weighting, dynamic panel, sample selection, measurement error, and result reporting | Yes |
| C4. Diagnostic results | After diagnostics | Findings, hard stops, warnings, proposed adjustments, and whether the model can proceed | Yes for any adjustment |
| C5. Correction specification | Before estimation | Exact Stata commands, sample, variables, controls, fixed effects, clustering, postestimation tests, and expected outputs | Yes |
| C6. Robustness and sensitivity | Before robustness/additional checks | Placebo, alternative lags, alternative controls, alternative FE, alternative instruments, pretrends, matching calipers, dynamic panel instruments, and sensitivity checks | Yes |
| C7. Results and interpretation | Before final export | ISR-style table shell, controls, diagnostics rows, fit statistics, significance notes, and interpretation claims | Yes |

Record all checkpoint decisions in `output/endogeneity/user_checkpoint_log.csv`.

## Source-to-method decision framework

Codex should classify each endogeneity threat and use the following map. Multiple threats may apply to the same hypothesis.

| Threat | Typical empirical sign | Candidate strategies | What the strategy can address | What it cannot guarantee |
|---|---|---|---|---|
| Omitted time-invariant unit heterogeneity | Unobserved stable quality, ability, reputation, location, category, firm culture, baseline user type | Unit FE, category FE, firm FE, creator FE, product FE, correlated random effects | Removes stable unobserved heterogeneity within FE dimensions | Does not remove time-varying unobservables |
| Omitted common shocks | Platform shocks, seasonality, macro shocks, category trends | Time FE, category-by-time FE, region-by-time FE, platform-section-by-time FE | Removes shared shocks at specified level | Does not remove idiosyncratic shocks correlated with focal variable |
| Omitted time-varying confounders | Evolving popularity, marketing, quality, demand shocks | Pre-treatment controls, lagged controls, trends, event-time controls, richer FE, sensitivity analysis | Reduces observed confounding | Cannot remove unobserved time-varying confounding by itself |
| Reverse causality / simultaneity | Outcome may affect focal regressor | Lagged focal variables, IV, natural experiment, DID, dynamic panel, Granger-style placebo | Improves temporal ordering or isolates exogenous variation | Lagging alone does not prove exogeneity |
| Measurement error in focal regressor | Noisy API measure, misclassified treatment, imperfect proxy | IV, errors-in-variables if reliability known, multiple-measure triangulation, latent variable/SEM, robustness to alternative measures | Reduces attenuation or proxy-bias concerns if assumptions hold | Requires valid reliability assumptions or instruments |
| Sample-selection bias | Outcome observed only for selected units | Heckman/selection models, treatment-effects models, inverse-probability weighting, attrition analysis | Addresses selection under model/exclusion assumptions | Requires credible selection equation and often exclusion restriction |
| Endogenous treatment assignment | Treatment chosen by high-ability/high-demand units | DID/event study, IV/LATE, `teffects` under observables, `etregress`/endogenous treatment models | Depends on design: parallel trends, exclusion, selection-on-observables, or joint normality/control-function assumptions | No single method addresses all selection concerns |
| Dynamic persistence / lagged DV bias | Lagged outcome central; outcome highly persistent | Dynamic panel GMM (`xtabond`, `xtdpdsys`, optional `xtabond2`) | Addresses lagged DV with FE under many-N/few-T assumptions | Sensitive to instrument proliferation and serial-correlation tests |
| Algorithmic/platform confounding | Platform ranks/recommendations affect both X and Y | Rich time/category/rank controls, FE, event shocks, IV, DID, placebo outcomes, mechanism separation | Reduces observable platform confounding | Algorithmic endogeneity may remain unless exogenous variation is credible |
| Interference/spillovers | Treatment of one unit affects other units | Spillover-aware design, exposure mapping, cluster-level treatment, network controls, excluding neighbors, spatial/network models | Clarifies exposure and comparison groups | Standard SUTVA-based estimators may be invalid if interference is ignored |

## Hard stops

Codex must stop and ask for user guidance when any of these occur:

- No clear endogenous variable or suspected source of endogeneity is specified.
- A proposed instrument lacks a theoretical exclusion-restriction rationale.
- A proposed IV is measured after the outcome or is mechanically related to the outcome.
- The first-stage relationship is not estimable or the instrument is perfectly collinear with fixed effects.
- DID/event-study treatment timing is unclear, no valid control group exists, or no pre-period is available.
- Matching/weighting variables are post-treatment, mediators, colliders, or outcomes.
- Fixed effects absorb the focal variable and no estimable within variation remains.
- A lagged focal variable is constructed with future information or invalid time ordering.
- Dynamic panel GMM is proposed for data with very small N, very large T, or no meaningful dynamic process.
- Sample-selection correction is proposed without a selection process, outcome-observation rule, or exclusion-rationale memo.
- A method is being used only because it produced the expected coefficient sign or significance.

## Manual and help retrieval

For every selected Stata command, retrieve or summarize the official manual/help before implementation.

Use this hierarchy:

1. Stata Press manual volume pages as the source index:
   - Base Reference Manual: `https://www.stata-press.com/manuals/base-reference-manual/`
   - Causal Inference and Treatment-Effects Estimation Reference Manual: `https://www.stata-press.com/manuals/causal-inference-and-treatment-effects-reference-manual/`
   - Longitudinal-Data/Panel-Data Reference Manual: `https://www.stata-press.com/manuals/longitudinal-panel-data-reference-manual/`
2. Command-specific Stata manual PDFs, such as `rivregress.pdf`, `rivregresspostestimation.pdf`, `rcfregress.pdf`, `causaldidregress.pdf`, `causaldidregresspostestimation.pdf`, `causalteffectspsmatch.pdf`, `causaltebalance.pdf`, `xtxtreg.pdf`, `xtxtabond.pdf`, `xtxtdpdsys.pdf`, and their postestimation entries.
3. Installed Stata help: `help command`, `view help command`, `which command`.
4. Community-command documentation only after installation checks. Examples: `reghdfe`, `ivreghdfe`, `ivreg2`, `xtabond2`, `csdid`, `eventstudyinteract`, `did_imputation`, `psmatch2`, `pstest`, `rbounds`, `boottest`, `outreg2`, `esttab`.

Do not paste long manual excerpts. Save a short digest to `output/endogeneity/manual_digest.md` and a retrieval log to `output/endogeneity/manual_retrieval_log.csv`.

## Baseline diagnostics before any correction

Before applying a correction, Codex should estimate and store a baseline model that is faithful to the original hypothesis and then run diagnostics.

Required baseline diagnostics:

- Confirm row key, sample, and panel declaration.
- Check missingness among DV, focal IV/treatment, controls, moderators, FE variables, cluster variables, instruments, treatment timing, and matching variables.
- Summarize DV/focal variables and report support problems.
- Check correlations among focal IVs, moderators, instruments, and controls.
- Run a VIF diagnostic using a linear approximation with `regress ...` and `estat vif`, excluding high-dimensional FE dummies where appropriate.
- Check whether focal variables have within-unit/time variation when FE models are considered.
- Check cluster counts and cluster-size distribution.
- Compare baseline OLS/pooled, FE/HDFE, and lagged-control variants only as diagnostics; do not present this comparison as proof of causality.

## Method-specific implementation rules

### 1. Controls and theoretically motivated covariates

Use controls to reduce omitted-variable bias only when they are theoretically justified and measured before the focal treatment/regressor or are otherwise predetermined by the design. Codex must not select controls based only on significance.

Implementation shell:

```stata
reg y c.x c1 c2 c3, vce(robust)
estimates store base_ols
estat vif
```

For panel or clustered data, use the planned cluster dimension:

```stata
reg y c.x c1 c2 c3 i.time_id, vce(cluster unit_id)
estimates store base_pooled_cluster
```

Decision rules:

- Add a control only if it is a pre-treatment confounder, precision control, or design control.
- Do not include mediators or post-treatment variables in the main causal model.
- Treat controls that are mechanically related to the DV as high-risk.
- If a control is time-varying and plausibly affected by the focal regressor, move it to mechanism or robustness analysis.

### 2. Fixed effects and high-dimensional fixed effects

Use FE to control for unobserved heterogeneity that is constant within the FE dimension. FE can reduce omitted-variable bias from stable unit/category/firm/creator/product attributes, but cannot solve time-varying unobserved confounding.

Implementation shells:

```stata
xtset unit_id time_id
xtreg y c.x c1 c2 c3 i.time_id, fe vce(cluster unit_id)
estimates store fe_unit_time
```

```stata
* Optional community route, only if approved and installed
cap which reghdfe
if _rc == 0 {
    reghdfe y c.x c1 c2 c3, absorb(unit_id time_id) vce(cluster unit_id)
    estimates store hdfe_unit_time
}
```

```stata
* Official absorbed route where available in the user's Stata version
xtreg y c.x c1 c2 c3, fe absorb(time_id) vce(cluster unit_id)
estimates store xtreg_fe_absorb
```

Diagnostics:

- Check whether `x` varies within `unit_id` and within the relevant FE structure.
- Record any variables omitted because of collinearity.
- Check singleton or absorbed observations if using HDFE.
- Explain if time-invariant controls are omitted under unit FE.
- Consider CRE (`xtreg, cre`) if time-invariant covariates are theoretically central and the model-selection skill approved it.

### 3. Lagged explanatory variables and temporal-ordering checks

Use lagged X when reverse causality or simultaneity is plausible and the panel timing supports temporal precedence. Lagging X is a check, not a complete solution.

Implementation shell:

```stata
xtset unit_id time_id
xtreg y L.x c1 c2 c3 i.time_id, fe vce(cluster unit_id)
estimates store lagged_x_fe
```

Diagnostics:

- Verify that `time_id` is correctly ordered and has no invalid gaps for the lag definition.
- Report how many observations are lost due to lagging.
- Consider alternative lags: `L1.x`, `L2.x`, `L(1/3).x` only if theoretically justified.
- For highly persistent outcomes, consider dynamic panel models only when approved.

### 4. Instrumental variables / 2SLS

Use IV only when the instrument is theoretically relevant, excludable, predetermined/exogenous, and affects the outcome only through the endogenous regressor. Codex must create an `instrument_validity_memo.md` before implementation.

Implementation shell:

```stata
* Reduced form
reg y z c1 c2 c3 i.time_id, vce(cluster cluster_id)
estimates store iv_reduced_form

* First stage
reg x z c1 c2 c3 i.time_id, vce(cluster cluster_id)
estimates store iv_first_stage_manual

* 2SLS
ivregress 2sls y c1 c2 c3 i.time_id (x = z), vce(cluster cluster_id)
estimates store iv_2sls

estat firststage, all
estat endogenous
estat overid
estat weakrobust
```

Panel IV shell:

```stata
xtset unit_id time_id
xtivreg y c1 c2 c3 i.time_id (x = z), fe vce(cluster unit_id)
estimates store xtiv_fe
```

Diagnostics and reporting:

- First-stage coefficient(s), partial R-squared, F/statistics where available.
- Weak-instrument robust inference where available.
- Endogeneity tests such as Durbin/Wu–Hausman or robust equivalents after `ivregress` where appropriate.
- Overidentification tests only when overidentified; a rejection suggests instrument validity concerns.
- Reduced-form estimate of `z -> y`.
- Instrument balance/placebo tests: instrument should not predict pre-treatment outcomes or predetermined covariates in a way that violates exclusion logic.
- Sensitivity to alternative instruments or instrument subsets when available.

Never describe a statistically significant IV estimate as proof that the instrument is valid.

### 5. Control-function models

Use control-function models when IV-style endogeneity correction is needed and the endogenous regressor’s first-stage distribution or interaction structure makes control-function estimation more suitable.

Implementation shell:

```stata
cfregress y c1 c2 c3 (x = z), vce(cluster cluster_id) first
estimates store cf_linear
```

For endogenous interactions:

```stata
cfregress y c1 c2 c3 w (x = z, interact(w)), mainonly(c.x#c.w) vce(cluster cluster_id) first
estimates store cf_interaction
```

Rules:

- Check first-stage model type: linear, probit, fractional probit, or Poisson.
- Treat the control-function coefficient(s) as evidence about endogeneity only within the specified model.
- For endogenous interactions, include appropriate control-function interactions.
- Do not mix control-function logic with arbitrary residual inclusion without adjusting inference.

### 6. Endogenous binary treatment models

Use `etregress`, `eteffects`, or `etpoisson` when the focal treatment is binary and treatment assignment may be endogenous.

Implementation shell for linear outcome:

```stata
etregress y c1 c2 c3, treat(treat = z c1 c2 c3) vce(robust) first
estimates store etregress_ml
margins r.treat, vce(unconditional)
```

Rules:

- Require a treatment-assignment equation and preferably an exclusion variable.
- Report treatment equation diagnostics and first-step estimates.
- State distributional/control-function assumptions.
- Compare against simpler OLS/FE/treatment-effects estimates as robustness, not as a definitive test.

### 7. DID and event-study designs

Use DID/event study when an event, policy, shock, platform rule change, threshold, or treatment timing creates treated and comparison groups over time.

Official Stata shell:

```stata
didregress (y c1 c2 c3) (treat), group(group_id) time(time_id) vce(cluster group_id)
estimates store did_official
estat trendplots
estat ptrends
estat granger
estat grangerplot, nleads(4) nlags(6)
```

Panel shell:

```stata
xtset unit_id time_id
xtdidregress (y c1 c2 c3) (treat), group(group_id) time(time_id) vce(cluster group_id)
estimates store xtdid_official
estat trendplots
estat ptrends
estat granger
```

TWFE/event-time shell when approved:

```stata
reghdfe y ib(-1).event_time##i.treated c1 c2 c3, absorb(unit_id time_id) vce(cluster group_id)
estimates store event_twfe
```

Diagnostics:

- Treatment timing table: treated units, control units, pre-periods, post-periods, staggered cohorts.
- Parallel-trends plot/test where feasible.
- Anticipation/placebo-lead checks.
- Bacon decomposition or heterogeneous DID alternatives when treatment timing is staggered.
- Alternative windows and placebo treatment dates.
- Cluster at treatment-assignment level unless a stronger rationale is documented.

Hard warning: DID requires a credible parallel-trends argument. A significant post-treatment coefficient alone is not sufficient.

### 8. Matching, weighting, and treatment effects under selection on observables

Use matching/weighting when treatment selection can be argued to be based on observed pre-treatment covariates. This does not address unobserved confounding.

Official Stata PSM shell:

```stata
teffects psmatch (y) (treat c1 c2 c3), atet nneighbor(1) osample(ps_osample)
estimates store psmatch_atet
tebalance summarize
tebalance density c1
tebalance box c1
teoverlap
```

IPW/IPWRA/AIPW shells:

```stata
teffects ipw (y) (treat c1 c2 c3), atet
estimates store ipw_atet
tebalance summarize, baseline
tebalance overid
teoverlap

teffects ipwra (y c1 c2 c3) (treat c1 c2 c3), atet
estimates store ipwra_atet
tebalance summarize, baseline

teffects aipw (y c1 c2 c3) (treat c1 c2 c3), atet
estimates store aipw_atet
tebalance summarize, baseline
```

Optional community route, only if approved:

```stata
cap which psmatch2
if _rc == 0 {
    psmatch2 treat c1 c2 c3, outcome(y) neighbor(1) logit common ate
    cap which pstest
    if _rc == 0 pstest c1 c2 c3, both
}
```

Diagnostics:

- Covariate balance before and after adjustment.
- Standardized differences and variance ratios.
- Overlap/common support plots.
- Caliper and neighbor sensitivity.
- Treatment model specification sensitivity.
- No post-treatment covariates in the treatment model.

### 9. Dynamic panel GMM

Use dynamic panel GMM only when the dependent variable is persistent, lagged DV belongs in the model, unobserved unit effects are present, and the data structure is appropriate, typically many units and relatively few time periods.

Implementation shells:

```stata
xtset unit_id time_id
xtabond y x c1 c2 c3, lags(1) vce(robust)
estimates store xtabond_main
estat abond
estat sargan
```

```stata
xtset unit_id time_id
xtdpdsys y x c1 c2 c3, lags(1) maxldep(2) vce(robust)
estimates store xtdpdsys_main
estat abond
estat sargan
```

Optional community route:

```stata
cap which xtabond2
if _rc == 0 {
    xtabond2 y L.y x c1 c2 c3 i.time_id, gmm(L.y x, lag(2 .) collapse) iv(c1 c2 c3 i.time_id) twostep robust small
    estimates store xtabond2_main
}
```

Diagnostics:

- AR(1) and AR(2) tests; AR(2) rejection is a major problem for standard moment validity.
- Sargan/Hansen overidentification tests, with caution about instrument proliferation.
- Instrument count relative to units.
- Robustness to lag-depth restrictions and collapsed instruments.
- Compare with FE and lagged-X specifications without overclaiming.

### 10. Sample-selection models

Use selection models when the outcome is observed only for selected units and selection is plausibly nonrandom.

Implementation shell:

```stata
heckman y c.x c1 c2 c3, select(observed = z c1 c2 c3) vce(robust)
estimates store heckman_ml
```

Rules:

- Define the observation/selection process explicitly.
- Prefer an exclusion variable that affects selection but not the outcome directly.
- Report the selection equation, inverse Mills/rho/lambda-related statistics where available, and sensitivity to selection specification.
- Do not use Heckman solely because observations are missing; first distinguish structural selection from random or administrative missingness.

### 11. Measurement-error checks

Use measurement-error strategies when key variables are proxies or noisy measures.

Possible routes:

```stata
* If reliability ratio is known or defensible
 eivreg y x c1 c2 c3, r(x reliability_value)
```

```stata
* Alternative-measure robustness
reg y x_alt1 c1 c2 c3 i.time_id, vce(cluster unit_id)
estimates store alt_measure_1
reg y x_alt2 c1 c2 c3 i.time_id, vce(cluster unit_id)
estimates store alt_measure_2
```

Rules:

- Measurement error is often conceptual; fix it through construct validity and alternative measures, not just commands.
- For archival platform data, distinguish API noise, scraping error, bot activity, misclassified treatment, and proxy validity.
- Report robustness to alternative operationalizations and validation samples where possible.

## Reporting requirements

Every endogeneity output should include three layers:

1. **Endogeneity strategy memo**: threat, selected method, why it is appropriate, assumptions, diagnostics, remaining limitations.
2. **Diagnostics tables/figures**: VIF/correlation, FE variation, first stage, weak-IV, overidentification, pretrends, balance/overlap, AR(2)/Sargan/Hansen, selection equation, placebo tests.
3. **ISR-style result tables**: main model, endogeneity-correction check(s), robustness/additional analyses, with control coefficients included unless the user approves appendix-only controls.

### ISR-style endogeneity table pattern

Follow Zhao et al. (2022)-style conventions:

- Use model columns `(1)`, `(2)`, etc.
- Include dependent-variable rows.
- Put focal variables first.
- Put interaction/moderation terms directly after lower-order focal terms when relevant.
- Include a visible `Control variable` section with coefficients for controls.
- Include FE/design rows: unit FE, time FE, category FE, session dummy, period dummy, etc.
- Include model-specific diagnostic rows: first-stage F, weak-IV robust test, overidentification test, AR(2), Hansen/Sargan, pretrend p-value, balance-overid p-value, number of matched/weighted observations.
- Include observations, number of units/groups/categories/clusters, and R-squared/within R-squared/log pseudolikelihood/pseudo R-squared where meaningful.
- Use standard errors in parentheses and significance notes.

For IV tables, create either a combined table with first-stage and second-stage columns or a separate first-stage table plus second-stage table. For DID/event study, include a separate figure for pretrends/event-time coefficients. For matching/weighting, include a balance table/plot before the treatment-effect table.

## Interpretation rules

Codex should use cautious causal language unless the identification design justifies stronger claims.

Acceptable phrasing examples:

- “The FE specification addresses time-invariant unobserved heterogeneity at the creator level but does not rule out time-varying demand shocks.”
- “The IV estimates rely on the assumption that the instrument affects the outcome only through the endogenous regressor.”
- “The DID estimates are interpretable as treatment effects under the parallel-trends and no-anticipation assumptions.”
- “The matching results reduce imbalance in observed pre-treatment covariates but do not address selection on unobservables.”
- “The dynamic panel results are consistent with the main findings and pass the AR(2) diagnostic, but the validity of internal instruments depends on the moment conditions.”

Avoid:

- “Endogeneity is solved.”
- “PSM proves causality.”
- “FE eliminates endogeneity.”
- “The instrument is valid because it is significant in the first stage.”
- “The insignificant endogeneity test proves the regressor is exogenous.”

## Output package

The skill should produce the following artifacts:

- `output/endogeneity/endogeneity_strategy_memo.md`
- `output/endogeneity/endogeneity_threat_register.csv`
- `output/endogeneity/threat_to_method_map.csv`
- `output/endogeneity/manual_retrieval_log.csv`
- `output/endogeneity/manual_digest.md`
- `output/endogeneity/pre_estimation_diagnostics.csv`
- `output/endogeneity/specification_adjustment_memo.md`
- `output/endogeneity/instrument_validity_memo.md` when IV is used
- `output/endogeneity/did_design_memo.md` when DID/event study is used
- `output/endogeneity/matching_balance_memo.md` when matching/weighting is used
- `output/endogeneity/dynamic_panel_memo.md` when GMM is used
- `output/endogeneity/sample_selection_memo.md` when selection models are used
- `output/endogeneity/measurement_error_memo.md` when measurement error is considered
- `output/tables/endogeneity_results_main.tex`
- `output/tables/endogeneity_results_robustness.tex`
- `output/tables/endogeneity_diagnostics.tex`
- `output/figures/pretrend_event_study.png` where relevant
- `output/figures/balance_overlap.png` where relevant
- `output/figures/margins_interaction.png` where relevant

## Quality gate before final response

Before reporting results to the user, Codex must verify:

- Each method maps to a specific threat.
- Every required assumption is documented.
- Every diagnostic was run or explicitly marked as unavailable.
- No correction method was applied after inspecting significance only.
- Control variables are pre-treatment or explicitly justified.
- Fixed effects and clustering are documented.
- IV/DID/matching/dynamic-panel claims are not overstated.
- Result tables include control coefficients unless the user approved otherwise.
- The user checkpoint log is complete.
