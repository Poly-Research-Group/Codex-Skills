# Specification Strategy Memo

## Baseline equation logic

`<Write the equation in manuscript notation.>`

## Variable roles

| Role | Variable(s) | Timing | Notes |
|---|---|---|---|
| Dependent variable | `<DV>` | `<TIMING>` | `<NOTES>` |
| Focal IV/treatment | `<IV>` | `<TIMING>` | `<NOTES>` |
| Moderator | `<MODERATOR>` | `<TIMING>` | `<NOTES>` |
| Mediator/mechanism | `<MEDIATOR>` | `<TIMING>` | `<NOTES>` |
| Controls | `<CONTROLS>` | `<TIMING>` | `<NOTES>` |
| Fixed effects | `<FE>` | `N/A` | `<NOTES>` |
| Clustering | `<CLUSTER>` | `N/A` | `<NOTES>` |

## Controls

Controls included in the main model should be pre-treatment or predetermined variables supported by theory and the upstream bad-control audit. Controls excluded from the main model should be listed with reasons.

## Fixed effects

Explain each fixed effect as a source of unobserved heterogeneity or design control. Confirm that the focal variable retains identifying variation after the fixed effects are included.

## Clustering and inference

Explain the cluster level and why it matches the treatment assignment, repeated observation, market/category/geography shock, dyadic dependence, or serial correlation structure.

## Transformations and interpretation

Explain logs, IHS, winsorization, standardization, offsets, or event-time transformations and how coefficients should be interpreted.

## Interaction and marginal-effects plan

For moderation or nonlinear models, specify marginal effects, simple slopes, contrasts, or plots needed to interpret the hypothesis.
