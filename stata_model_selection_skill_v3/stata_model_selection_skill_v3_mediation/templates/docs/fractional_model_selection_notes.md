# Fractional, Proportion, Share, Rate, and Bounded Outcome Model Selection Notes

Use this note when a dependent variable is bounded in `[0,1]`, naturally interpretable as a share/proportion/rate, or constructed as a numerator divided by a denominator.

## Required classification
Codex must classify the outcome as one of the following before selecting a Stata model family:

1. Fractional response with possible exact 0 and/or 1 values.
2. Open-interval proportion strictly inside `(0,1)`.
3. Proportion with many structural zeros.
4. Proportion with many structural ones.
5. Fractional panel outcome where unit fixed effects are central to identification.
6. Numerator/denominator outcome where the denominator is observed.
7. Bounded continuous outcome that is not substantively a fraction.

## Candidate Stata families

| Case | Candidate commands | Notes |
|---|---|---|
| Fractional response with 0/1 values | `fracreg logit`, `fracreg probit`, `glm` with appropriate link/family | Report marginal effects or predicted proportions. |
| Strictly open-interval proportion | `betareg`, `fracreg` | Beta regression generally requires values strictly between 0 and 1 unless a boundary strategy is used. |
| Many structural zeros or ones | Two-part model using `logit`/`probit` for boundary mass plus fractional/beta/linear model for interior values | Requires substantive explanation of structural boundary values. |
| Panel with essential fixed effects | Compare `fracreg`/`glm`, linear FE/HDFE approximation, and robustness alternatives | Check whether the fixed effects are identification-critical and whether nonlinear models drop observations. |
| Observed numerator and denominator | Consider binomial-style GLM or fractional response depending on data-generating logic | Requires numerator, denominator, and exposure logic. |

## Diagnostics
Codex must report support, boundary mass, denominator/exposure definition, missingness, true-zero status, link-function rationale, predicted-value range, fixed-effect feasibility, cluster level, and robustness alternatives.

## Reporting
Report N, outcome scale, estimator/link, coefficients and average marginal effects or predicted proportions, fixed effects, clustering, sample restrictions, and interpretation in percentage points or proportions.
