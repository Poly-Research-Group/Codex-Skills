# Stata Implementation Handoff Memo

This memo hands model-selection decisions to the model-specific Stata implementation skill.

## Project

- Project label: `<PROJECT_LABEL>`
- Analysis-ready Stata dataset: `<PATH_TO_DTA>`
- Stata version: `<STATA_VERSION>`
- Community commands allowed: `<YES_NO>`

## Selected model families

| Hypothesis | Primary family | Stata command family | Implementation skill |
|---|---|---|---|
| H1 | `<PRIMARY_FAMILY>` | `<COMMANDS>` | `<NEXT_SKILL>` |

## Baseline specification components

| Component | Variables/details |
|---|---|
| DV | `<DV>` |
| Key IV/treatment | `<IV_OR_TREATMENT>` |
| Controls | `<CONTROLS>` |
| Fixed effects | `<FE>` |
| Random effects | `<RANDOM_EFFECTS>` |
| Clustering | `<CLUSTER>` |
| Sample | `<SAMPLE>` |
| Transformations | `<TRANSFORMATIONS>` |

## Diagnostics required before reporting results

- `<DIAGNOSTIC_1>`
- `<DIAGNOSTIC_2>`
- `<DIAGNOSTIC_3>`

## Robustness checks to implement

- `<ROBUSTNESS_1>`
- `<ROBUSTNESS_2>`
- `<ROBUSTNESS_3>`

## Reporting artifacts required

- Regression table with clearly labeled FE, controls, clustering, N, and fit statistics.
- Diagnostic table or appendix table.
- Coefficient/marginal-effects/event-study figure where required.
- Robustness table.

## Blocking issues before implementation

`<NONE_OR_LIST>`
