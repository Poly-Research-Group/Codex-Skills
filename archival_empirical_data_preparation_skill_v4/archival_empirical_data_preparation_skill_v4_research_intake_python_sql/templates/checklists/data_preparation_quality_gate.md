# Data Preparation Quality Gate

Before exporting `analysis_ready.dta`, verify each item.

## Research design

- [ ] Unit of analysis is explicitly defined.
- [ ] Time grain is explicitly defined or marked as cross-sectional.
- [ ] Hypotheses are mapped to variables.
- [ ] Treatment/event timing is documented when relevant.

## Raw data and provenance

- [ ] Raw files are preserved without manual edits.
- [ ] Source inventory is complete.
- [ ] Import logs exist for all raw sources.

## Keys and joins

- [ ] Final row key is unique.
- [ ] Merge plan is complete.
- [ ] Duplicate-key checks are complete before joins.
- [ ] Merge audit records matched and unmatched rows.
- [ ] No unexplained row multiplication exists.

## Variables

- [ ] Variable construction log is complete.
- [ ] Raw and transformed versions of key variables are preserved or justified.
- [ ] Lags/leads are constructed within unit and ordered by time.
- [ ] No future information is used in predictors except for explicitly labeled placebo/event-study leads.

## Controls

- [ ] Control-variable audit is complete.
- [ ] Main controls are temporally valid.
- [ ] Post-treatment controls are excluded from total-effect models.
- [ ] Mediators/mechanisms are separated from controls.
- [ ] Variables absorbed by fixed effects are flagged.

## Sample and diagnostics

- [ ] Sample-flow table is complete.
- [ ] Missingness audit is complete.
- [ ] Outlier audit is complete.
- [ ] Panel/cross-sectional structure audit is complete.
- [ ] ISR-style summary statistics table is exported when required.

## Handoff

- [ ] `analysis_ready.dta` is exported.
- [ ] Neutral-format dataset is exported.
- [ ] Model-readiness memo is complete.
