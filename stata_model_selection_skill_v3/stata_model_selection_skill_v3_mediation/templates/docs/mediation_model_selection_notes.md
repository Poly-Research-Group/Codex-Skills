# Mediation Model Selection Notes

Use this note when a hypothesis involves a mechanism, pathway, channel, mediator, or indirect effect.

## Mandatory distinction

Do not automatically treat a mechanism hypothesis as causal mediation. Codex must first classify the claim as one of three types: mechanism evidence, causal mediation decomposition, or SEM/GSEM path/measurement model.

## Intake questions

1. What is the treatment or focal independent variable?
2. What is the mediator or mediators?
3. What is the outcome?
4. What is the timing of treatment, mediator, and outcome?
5. Is the mediator measured after treatment and before outcome?
6. How many mediators are modeled?
7. If there are two mediators, are they parallel or sequential?
8. What is the support of the outcome and each mediator?
9. Which pretreatment confounders belong in the outcome equation and mediator equation?
10. Are any mediator-outcome confounders caused by treatment?
11. Are unit FE, time FE, dyad FE, category FE, or HDFE required?
12. What level should standard errors be clustered at?
13. What Stata version is available, and is StataNow available for two-mediator `mediate`?
14. Should the manuscript describe the result as causal mediation or mechanism evidence?

## Preferred routing

- Use `mediate` for official causal mediation with one observed mediator when the outcome, mediator, treatment, timing, and assumptions match the command.
- Use two-mediator `mediate` only when StataNow support is available and the mediator structure is explicitly parallel or sequential.
- Use `sem` for linear path models, latent constructs, measurement models, and SEM fit/reporting.
- Use `gsem` for generalized, nonlinear, multilevel, mixed-response, or latent generalized mediation/path models.
- Use sequential equation models when panel FE/HDFE/DID/event-time identification is central and formal `mediate`/SEM/GSEM cannot represent the required design. Label this as mechanism evidence unless causal mediation assumptions are explicitly defended.

## Reporting requirements

Report treatment, mediator(s), outcome, timing, covariates by equation, fixed effects, clustering, model family, direct/indirect/total/CDE/path-specific effects as appropriate, effect scale, confidence interval method, and robustness checks.

## Robustness checks

Use alternative mediator timing, alternative mediator measures, alternative confounder sets, direct-effect-only specification, total-effect specification without mediator, bootstrap or simulation CIs, placebo mediator/outcome, and sequential versus parallel ordering when theoretically plausible.
