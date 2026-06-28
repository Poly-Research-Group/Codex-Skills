# Estimator Red Flags

Flag these conditions before recommending a primary Stata estimator family.

## General

- [ ] The empirical design audit says the dataset is not ready.
- [ ] The unit of analysis is not confirmed.
- [ ] The row key is not unique.
- [ ] Outcome support is unknown or mismatched to the proposed estimator.
- [ ] Model choice is being made because a command is familiar, not because it fits the estimand.

## Timing and controls

- [ ] Treatment/key IV is measured after the outcome.
- [ ] A proposed control is post-treatment.
- [ ] A proposed control is a mediator, mechanism, or collider.
- [ ] A proposed control is mechanically constructed from the dependent variable.
- [ ] Controls are selected using p-values or fit improvements.

## Fixed effects and clustering

- [ ] Proposed fixed effects absorb the focal variable.
- [ ] There is insufficient within-unit or within-FE variation.
- [ ] Cluster count is small and no small-cluster correction is planned.
- [ ] Clustering ignores the level of treatment assignment or shock correlation.

## Design-specific

- [ ] DID lacks pre-treatment periods or comparison units.
- [ ] Staggered DID uses only simple TWFE despite likely heterogeneous effects.
- [ ] IV lacks exclusion restriction or weak-IV diagnostics.
- [ ] Matching lacks overlap and balance diagnostics.
- [ ] RD lacks a defensible cutoff or running variable.
- [ ] Survival model lacks valid risk-set/censoring definition.
- [ ] Dynamic panel GMM has too many instruments relative to groups.
- [ ] Network/spillover theory is central but the model assumes no interference.


## Mediation-specific gate

- [ ] If any hypothesis is mediation/mechanism-based, C3a has been completed.
- [ ] Treatment, mediator, and outcome timing are documented.
- [ ] Mediator count and ordering are documented.
- [ ] Confounders for treatment-outcome, treatment-mediator, and mediator-outcome paths are documented.
- [ ] Treatment-induced mediator-outcome confounding risk is assessed.
- [ ] The selected route is labeled as causal mediation or mechanism evidence.
- [ ] Stata command support and Stata version are confirmed.
