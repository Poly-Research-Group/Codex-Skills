# Matching / Weighting Balance Memo

## Treatment model

- Treatment variable:
- Treatment model covariates:
- Why each covariate is pre-treatment:
- Outcome:
- Estimand: ATE / ATET

## Balance and overlap

- Common support / overlap:
- Standardized differences before/after:
- Variance ratios before/after:
- Variables with poor balance:
- Caliper/neighbor/weight trimming decisions:

## Diagnostics

- `tebalance summarize`.
- `tebalance density` or `tebalance box` for key continuous covariates.
- `tebalance overid` when supported.
- `teoverlap` when supported.
- Sensitivity to treatment model specification.

## Interpretation boundary

Matching/weighting addresses selection on observables only. State remaining unobservable-selection concern.
