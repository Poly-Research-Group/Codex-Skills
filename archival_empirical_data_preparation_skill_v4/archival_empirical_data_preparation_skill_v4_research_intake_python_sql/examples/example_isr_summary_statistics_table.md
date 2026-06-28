# Example ISR-Style Summary Statistics Tables

## Main key-variable table

**Table X. Descriptive Statistics of Key Variables**

| Variable | Description | Mean | Standard deviation | Minimum | Maximum |
|---|---|---:|---:|---:|---:|
| After_i,t | A dummy variable equal to 1 if the unit is observed after the focal event within the analysis window | 0.5 | 0.5 | 0 | 1 |
| Outcome_i,t | Main dependent variable measured at the unit-time level | 149 | 2,021.425 | 0 | 84,643 |
| Prior_Size_i,t | Baseline or lagged size of the focal unit | 1,435.29 | 133,272.5 | 0 | 14,442,649 |
| Moderator_i,t | Hypothesized boundary condition measured before or at the focal period | 0.412 | 0.289 | 0 | 0.8 |
| Restricted_i,t | A dummy variable equal to 1 if the unit has the restricted-status indicator | 0.26 | 0.439 | 0 | 1 |

Number of observations: 2,418,488

## Grouped/decomposed table

**Table X. Descriptive Statistics of Decomposed Outcomes**

| Group | Variable | Description | Mean | Standard deviation | Minimum | Maximum |
|---|---|---|---:|---:|---:|---:|
| 1. Direct Mechanism | Direct_i,t | The difference between inflow from the focal source and outflow to the focal source | 5.214 | 53.54 | -182 | 5,065 |
| 2. Indirect Mechanism | Indirect_i,t | The difference between inflow from outside sources and outflow to outside sources | -28.5 | 502.75 | -70,671 | 412 |

Number of observations: 2,418,488

## Notes for Codex

- Use `summary_statistics_plan.csv` to decide variable order and descriptions.
- Keep the main table compact and manuscript-facing.
- Use grouped/decomposed tables when the study decomposes outcomes, mechanisms, or directional flows.
- If N differs across variables, add an `N` column or compute statistics on the common analysis sample.
