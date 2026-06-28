# Endogeneity Intake Questionnaire

Codex must ask these questions before running endogeneity checks or correction models.

## Research context

1. What is the empirical setting and focal phenomenon?
2. What is the unit of analysis and time granularity?
3. What are the main hypotheses and expected directions?
4. Which hypotheses are causal claims, associational claims, mechanism claims, or robustness-only claims?

## Variables and timing

1. What are the dependent variables?
2. What are the focal independent variables, treatments, events, or endogenous regressors?
3. What candidate controls are available, and when are they measured?
4. Are any controls plausibly mediators, mechanisms, colliders, or post-treatment variables?
5. What fixed effects and clustering dimensions are proposed?

## Endogeneity sources

For each focal relationship, indicate which threats apply:

- Omitted stable unit heterogeneity.
- Omitted common time shocks.
- Omitted time-varying confounders.
- Reverse causality or simultaneity.
- Measurement error or proxy validity concerns.
- Sample selection or attrition.
- Endogenous treatment assignment.
- Dynamic persistence / lagged outcome bias.
- Platform algorithmic confounding.
- Interference/spillovers.

## Available identification resources

1. Are there credible instruments? What is the relevance and exclusion-restriction argument?
2. Is there a policy shock, platform rule change, launch, cutoff, or event?
3. Are there treated and control groups? Are there pre-treatment periods?
4. Are pre-treatment covariates rich enough for matching or weighting?
5. Is there a meaningful lag structure?
6. Are there multiple measures or validation data for noisy constructs?
7. Is outcome observation conditional on a selection process?

## Output preferences

1. Should endogeneity correction be part of the main model, robustness checks, or additional analyses?
2. Should community commands be allowed? Which packages are approved?
3. Should tables use official `etable`, `esttab`, or `outreg2`?
4. Should controls appear in the main table or an appendix? Default is main table.
