# Example: Endogeneity Workflow for a Platform Study

## Context

A researcher studies whether creator content-scope reconfiguration affects subsequent audience contribution. The main concern is that creators may reconfigure content scope in response to unobserved demand shocks, algorithmic visibility changes, or prior audience decline.

## Threat register

| Hypothesis | Threat | Why plausible | Candidate checks |
|---|---|---|---|
| H1: Reconfiguration -> contribution | Reverse causality | Contribution decline may trigger reconfiguration | Lagged reconfiguration, placebo pre-outcome, event study |
| H1 | Omitted stable creator quality | Better creators may both reconfigure and retain audiences | Creator FE |
| H1 | Time shocks | Platform-wide seasonality and category shocks | Week FE, category-by-week FE |
| H1 | Algorithmic confounding | Visibility may affect both reconfiguration and contribution | Visibility controls if pre-treatment; placebo; fixed effects; IV/event if available |
| H2: Portability mediates effect | Bad-control risk | Portability may be a mechanism, not a control | Do not include portability as control in total-effect model |

## Candidate Stata plan

1. Baseline pooled/FE models with controls and fixed effects.
2. Lagged-X robustness to improve temporal ordering.
3. Event-study around first content-scope reconfiguration if treatment timing is clear.
4. IV only if a credible exogenous source of reconfiguration exists.
5. Matching/weighting only if treatment assignment can plausibly be modeled by pre-treatment observables.
6. Dynamic panel only if lagged contribution is theoretically central and panel dimensions support GMM.

## Interpretation boundary

Creator FE and lagged X improve design credibility, but they do not fully eliminate time-varying unobserved confounding. Stronger causal language requires a credible event, instrument, or quasi-experimental design.
