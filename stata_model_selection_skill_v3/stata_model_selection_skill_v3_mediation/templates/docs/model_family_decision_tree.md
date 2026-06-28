# Model-Family Decision Tree

Use this decision tree as a compact guide. The full selection must still be documented in the model-selection report, and Codex must pause at the required user checkpoints before finalizing recommendations.

## Step 1. Is the upstream design ready?

- Not ready: stop and return a blocking-issue memo.
- Conditionally ready: provide conditional recommendations and list required decisions.
- Ready: proceed.

## Step 2. What claim is being made?

- Association: choose a model family by DV support and data structure; avoid causal language.
- Causal effect: choose by identification strategy before distributional convenience.
- Moderation: choose a valid base model, then add interaction terms and marginal-effects/contrast plan.
- Mediation/mechanism: choose a valid base model and a separate mediator model; avoid controlling for mediator in the main total-effect model.
- Prediction: choose predictive models and validation metrics; do not interpret selected variables as causal.

## Step 3. What is the DV support?

- Continuous/log continuous: OLS/HDFE/panel/mixed/GLM/quantile.
- Binary: logit/probit/LPM/panel binary/multilevel binary.
- Count/nonnegative: Poisson/NB/PPML/zero-inflated/hurdle/exposure models.
- Fractional/proportion/share/rate: first check scale, boundary mass, and denominator; then consider `fracreg logit/probit`, `betareg` for open-interval proportions, two-part/boundary-mass models for structural zeros/ones, and linear FE/HDFE only as a justified robustness or FE-identification route.
- Ordinal/nominal/choice: ordered, multinomial, nested, conditional, or mixed choice models.
- Censored/truncated/selected: tobit/intreg/truncreg/churdle/Heckman/extended regression.
- Duration: survival models.
- Latent/path: SEM/GSEM/mediation.
- Spatial/network: spatial or exposure models.

## Step 4. What is the data structure?

- Cross-section: cross-sectional model family, treatment effects, IV, RD, SEM, spatial as needed.
- Panel: xt/HDFE/panel nonlinear/dynamic panel as needed.
- Event-time/cohort-time: DID/event study/synthetic control.
- Dyadic/network panel: dyad FE, sender/receiver FE, network exposure, multiway clustering.
- Survival risk set: stset, then survival family.
- Aggregate time series: tsset, then time-series family.

## Step 5. What is the unobserved heterogeneity strategy?

- Time-invariant unit heterogeneity correlated with regressors: FE/HDFE.
- Time-invariant focal variables needed and correlated heterogeneity plausible: CRE.
- Hierarchical variance or random slopes are substantive: multilevel.
- Design shock at aggregate level: DID/synthetic/time-series strategy.

## Step 6. What inference is needed?

- Repeated unit observations: cluster by unit or treatment-assignment level.
- Group-level treatment: cluster at group; consider wild-cluster bootstrap if few groups.
- Unit and time shocks: consider multiway clustering.
- Time-series autocorrelation: HAC or time-series model.
- Spatial/network dependence: spatial/network model or appropriate clustering/randomization.

## Step 7. What robustness must accompany the model?

Map robustness checks to identified threats, not to arbitrary specification shopping.


## Mediation and mechanism branch

If a hypothesis includes a mediator, channel, pathway, or mechanism, pause at C3a before final estimator selection. Route to official `mediate` for causal mediation with supported observed mediator/outcome/treatment structure; two-mediator `mediate` only when the user's StataNow version supports it and mediator ordering is confirmed; `sem` for linear/latent path models; `gsem` for generalized or multilevel path models; and sequential base-equation models for panel/HDFE mechanism evidence. Never include a mediator as an ordinary control in the main total-effect model without explicitly distinguishing total, direct, indirect, and mechanism specifications.
