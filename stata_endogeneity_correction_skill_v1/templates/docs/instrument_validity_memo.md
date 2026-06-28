# Instrument Validity Memo

## Instrument set

- Endogenous regressor(s):
- Instrument(s):
- Sample:
- Fixed effects:
- Cluster level:

## Relevance

Explain why the instrument should predict the endogenous regressor.

## Exclusion restriction

Explain why the instrument should affect the outcome only through the endogenous regressor.

## Timing

Confirm the instrument is predetermined or plausibly exogenous relative to the outcome.

## Threats to validity

- Direct effect on outcome:
- Correlation with omitted shocks:
- Mechanical relationship with DV:
- Measurement after treatment/outcome:
- Weak first stage:
- Instrument affected by platform algorithm:

## Required diagnostics

- First-stage estimates.
- `estat firststage, all` where applicable.
- Reduced-form outcome model.
- `estat endogenous` where applicable.
- `estat overid` where overidentified.
- `estat weakrobust` where applicable.
- Placebo tests on pre-treatment outcomes or predetermined covariates.
- Sensitivity to alternative instrument sets.
