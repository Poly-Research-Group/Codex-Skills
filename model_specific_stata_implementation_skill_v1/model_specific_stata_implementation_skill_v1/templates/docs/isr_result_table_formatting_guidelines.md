# ISR-Style Result Table Guidelines

Use these rules when exporting final result tables.

1. Use model columns labeled `(1)`, `(2)`, `(3)`, etc.
2. Add a dependent-variable header row and, when useful, a construct-specific row such as viewer-flow direction, outcome family, sample, or window.
3. Present focal variables first.
4. In moderation tables, present moderator main effect, focal main effect, and interaction term before controls unless theory requires a different order.
5. Add a visible `Control variable` section.
6. Include coefficients for controls. Do not summarize controls as `Yes` unless the user approves an appendix-only control table.
7. Add fixed-effect/design rows: `Time fixed effects`, `Unit fixed effects`, `Category fixed effects`, `Session dummy`, `Period dummy`, or project-specific labels.
8. Add N and relevant model statistics: R2, within R2, pseudo R2, log pseudolikelihood, AIC/BIC, number of units, number of categories, number of clusters, AR(2), Hansen J, first-stage F, or other model-family diagnostics.
9. Use standard errors in parentheses.
10. Use notes: `Standard errors are in parentheses. Significance levels: + p < 0.10, * p < 0.05, ** p < 0.01, *** p < 0.001.`
11. Robustness tables should mirror main tables to preserve comparability.

## Table shell

|  | Model (1) | Model (2) | Model (3) |
|---|---:|---:|---:|
| Dependent variable | DV1 | DV2 | DV3 |
| Focal variable | coef (se) | coef (se) | coef (se) |
| Interaction term | coef (se) | coef (se) | coef (se) |
| Control variable |  |  |  |
| Control 1 | coef (se) | coef (se) | coef (se) |
| Control 2 | coef (se) | coef (se) | coef (se) |
| Unit fixed effects | Yes | Yes | Yes |
| Time fixed effects | Yes | Yes | Yes |
| Number of observations | N | N | N |
| Number of units/categories | N | N | N |
| R2 / fit statistic | value | value | value |

