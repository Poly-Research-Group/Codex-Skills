# Model-Selection Completion Gate

Before marking model selection as complete, verify that all items are satisfied.

## Intake and upstream readiness

- [ ] Research context is confirmed.
- [ ] Hypotheses/focal relationships are confirmed.
- [ ] Upstream empirical design audit status is ready or conditionally ready.
- [ ] Blocking design issues are resolved or explicitly recorded.
- [ ] Stata version and community-command permission are recorded.

## Hypothesis-to-model mapping

- [ ] Each hypothesis has a dependent variable and outcome-support classification.
- [ ] Each hypothesis has a claim-type classification.
- [ ] Each hypothesis has a data-structure classification.
- [ ] Each hypothesis has a primary estimator family.
- [ ] Each hypothesis has at least one alternative or robustness estimator family, unless not appropriate.
- [ ] Rejected estimator families and reasons are documented.

## Specification strategy

- [ ] Controls are taken from the bad-control audit and are not selected by significance.
- [ ] Fixed effects are justified and do not accidentally absorb focal variation.
- [ ] Clustering level is justified.
- [ ] Transformations are documented.
- [ ] Interactions and nonlinear terms have an interpretation plan.

## Diagnostics and reporting

- [ ] Diagnostics requirements are specified by model family.
- [ ] Reporting requirements include fit statistics, FE, clustering, and sample information.
- [ ] Nonlinear models include marginal-effects or predicted-quantity reporting.
- [ ] DID/event-study models include pretrend and event-time figure requirements.
- [ ] IV models include first-stage and weak-IV diagnostics.
- [ ] Treatment-effect models include overlap and balance diagnostics.

## Handoff

- [ ] Implementation skill routing is specified.
- [ ] Stata code skeletons are generated or explicitly not requested.
- [ ] Assumptions and unresolved risks are recorded.


## Mediation-specific gate

- [ ] If any hypothesis is mediation/mechanism-based, C3a has been completed.
- [ ] Treatment, mediator, and outcome timing are documented.
- [ ] Mediator count and ordering are documented.
- [ ] Confounders for treatment-outcome, treatment-mediator, and mediator-outcome paths are documented.
- [ ] Treatment-induced mediator-outcome confounding risk is assessed.
- [ ] The selected route is labeled as causal mediation or mechanism evidence.
- [ ] Stata command support and Stata version are confirmed.
