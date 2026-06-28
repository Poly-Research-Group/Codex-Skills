# ISR-Style Endogeneity Table Guidelines

Use the table style already adopted in the broader skills and inspired by Zhao et al. (2022): model columns, dependent-variable header rows, focal effects first, control coefficients included, fixed-effect/design rows, observations, groups/categories, model fit, standard errors in parentheses, and significance notes.

## Recommended table sequence

1. Main endogeneity correction/check table.
2. IV first-stage table, if IV is used.
3. DID/event-study diagnostic figure/table, if DID is used.
4. Matching/weighting balance table, if matching or weighting is used.
5. Dynamic panel robustness table, if GMM is used.
6. Additional robustness and placebo checks.

## Required rows by method

### IV/2SLS

- Focal endogenous regressor estimate.
- Controls.
- Fixed effects.
- Cluster level.
- Observations.
- First-stage F or available first-stage diagnostic.
- Weak-IV robust test where available.
- Overidentification test if applicable.
- Endogeneity test if applicable.

### DID/event study

- Treatment coefficient / ATET.
- Controls.
- Group/time FE.
- Cluster level.
- Observations.
- Treated and control groups.
- Pretrend p-value or diagnostic note.
- Event-study figure reference.

### Matching/weighting

- ATE/ATET.
- Treatment model covariates.
- Observations before/after adjustment.
- Balance summary rows.
- Overlap/common support note.

### Dynamic panel

- Lagged DV coefficient.
- Focal coefficient.
- Controls.
- Observations.
- Units.
- AR(2) p-value.
- Sargan/Hansen p-value.
- Instrument count.

Do not hide control coefficients unless the user explicitly approves a separate appendix table.
