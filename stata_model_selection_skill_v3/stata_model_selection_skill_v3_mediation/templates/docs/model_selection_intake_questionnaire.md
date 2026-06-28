# Model-Selection Intake Questionnaire

Use this questionnaire before selecting any Stata estimator family. If the upstream empirical design audit already answers a question, summarize the answer and ask the user to confirm it.

## 1. Research context

- Project title or short label:
- Empirical setting:
- Focal phenomenon:
- Main research question:

## 2. Hypotheses and claim type

For each hypothesis or focal relationship:

- Hypothesis ID:
- Hypothesis text:
- Claim type: association, causal effect, moderation, mediation, mechanism, prediction, descriptive decomposition, or other.
- Expected direction:
- Estimand: coefficient, elasticity, marginal effect, ATE, ATT/ATET, LATE, hazard ratio, odds ratio, direct/indirect effect, or other.

## 3. Dependent variables

For each outcome:

- Variable name:
- Theoretical construct:
- Support: continuous, log continuous, binary, count, nonnegative, fractional/proportion/share/rate, bounded continuous, ordinal, nominal, censored/truncated, duration/time-to-event, choice, network/spatial, latent.
- Timing relative to treatment/key IV:
- Transformation already applied:
- Zero/negative/censoring issues:
- If fractional/proportion/share/rate: Is the variable scaled as 0–1 or 0–100? Are exact 0 or 1 values possible? Are boundary values structural? Is there an observed numerator and denominator?
- If fractional/proportion/share/rate: Are unit fixed effects central to identification, and should linear FE be considered as a robustness approximation?

## 4. Data structure

- Unit of analysis:
- Unit ID:
- Time ID:
- Time grain:
- Data structure: cross-sectional, repeated cross-sectional, panel, event-time panel, cohort-time panel, dyadic panel, network panel, survival/risk-set, aggregate time series.
- Is the panel balanced?
- Are there gaps, entry, exit, or attrition?

## 5. Identification strategy

- Intended empirical design:
- Treatment/event/exposure variable:
- Treatment timing variable:
- Cohort variable, if any:
- Comparison group:
- No-anticipation window:
- Pre-treatment periods available:
- Post-treatment periods available:
- Is treatment staggered, reversible, continuous, or binary?
- Are spillovers/interference theoretically relevant?

## 6. Endogeneity concerns

- Omitted confounding:
- Reverse causality:
- Simultaneity:
- Selection:
- Measurement error:
- Platform algorithmic confounding:
- Dynamic feedback:
- Network/spillover interference:
- Proposed remedy, if any:

## 7. Controls, fixed effects, and clustering

- Controls that survived bad-control audit:
- Controls excluded from the main model:
- Mechanism-only or mediation variables:
- Proposed fixed effects:
- Fixed effects that may absorb focal variables:
- Proposed clustering dimension:
- Number of clusters, if known:
- Multiway clustering needed?
- Weights or survey design?

## 8. Stata environment

- Stata version:
- Official Stata commands only, or allow community-contributed commands?
- Required packages already installed:
- Preferred output format: Stata `.do`, LaTeX tables, Excel tables, CSV artifacts, or markdown report.

## 9. User confirmation and checkpoint preferences

Before proceeding, summarize the model-selection contract and ask the user to confirm or correct it. Also ask whether the user wants Codex to stop at every required checkpoint or to produce a conditional draft while logging assumptions.

Required checkpoints are C0 intake confirmation, C1 upstream readiness, C2 outcome/data classification, C3 identification/estimand, C4 primary-estimator shortlist, C5 specification strategy, C6 community-command approval, and C7 robustness/reporting.
