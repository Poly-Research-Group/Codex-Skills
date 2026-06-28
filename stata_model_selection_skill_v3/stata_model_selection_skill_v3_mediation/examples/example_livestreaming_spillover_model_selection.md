# Example: Livestreaming Content-Switching Spillover Study

This example illustrates the type of reasoning the Stata Model Selection Skill should produce. It is adapted as a generic pattern from a livestreaming platform study, not as a template to copy mechanically.

## Research context

A study examines whether entrant streamers' content switching affects incumbent streamers' viewer flows. The analysis dataset is at the incumbent streamer-session level. The outcomes include direct net viewer flow from entrant to incumbent and indirect net viewer flow from outside-category streamers to incumbents.

## Outcome support

The direct and indirect flow variables are count-based net flows that can be negative. Because standard count models require nonnegative support, a signed net-flow outcome should not be modeled directly with Poisson or negative binomial. Plausible primary families include transformed continuous models, HDFE/panel models, or multilevel models when category-level heterogeneity and random slopes are central. A count-model robustness route can separately model inflows and outflows when the theory supports decomposing the net-flow measure.

## Data structure

The dataset is a streamer-session panel with repeated observations over sessions and categories. The model-selection skill should verify streamer/session identifiers, panel balance or gaps, within-streamer variation in treatment or event exposure, and the fixed effects needed for streamer, category, and time heterogeneity.

## Possible model-selection logic

| Design feature | Implication |
|---|---|
| Signed net-flow DV | Do not select Poisson/NB as primary for the signed DV. Consider transformed continuous model or decompose inflow/outflow for count robustness. |
| Streamer-session panel | Panel/HDFE or multilevel model families are plausible. |
| Content-switching event | Event-timing and pre/post construction should be audited. |
| Category heterogeneity | Category FE, category-level controls, or random category slopes may be considered depending on estimand. |
| Lagged viewership control | Timing audit required to ensure the lag is pre-outcome and not post-treatment leakage. |
| Moderation by entrant popularity | Interaction model with marginal-effects/simple-slope interpretation required. |

## Candidate estimator recommendation

Primary family could be a panel/HDFE or multilevel linear model for transformed signed net-flow outcomes, depending on whether the theoretical target is within-streamer effects or category-level random heterogeneity. If the design uses fixed effects for streamers, categories, and sessions, the skill should route to the HDFE implementation skill. If the design explicitly allows slopes/intercepts to vary by category, the skill should route to the multilevel implementation skill.

## Required diagnostics

- Validate streamer-session row key.
- Summarize distribution of signed net-flow outcomes before and after transformation.
- Confirm negative values and transformation constant.
- Verify treatment/event timing.
- Check fixed-effect absorption and within-unit variation.
- Check cluster counts and serial correlation.
- For moderation, plan marginal effects or simple slopes.

## Robustness plan

- Alternative observational windows.
- Untransformed outcome if defensible.
- Decomposed inflow and outflow count models.
- Dynamic panel robustness if lagged outcomes are theoretically central.
- Subsample based on content similarity or category type.
