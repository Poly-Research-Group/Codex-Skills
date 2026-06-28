# Example Control Variable Audit

| Candidate control | Role | Include in main model? | Timing | Rationale | Risk |
|---|---|---:|---|---|---|
| Prior activity | Pre-treatment confounder | Yes | Lagged or pre-period mean | May affect both treatment adoption and later outcome | Low if measured before treatment |
| Baseline popularity | Pre-treatment confounder | Yes | Baseline/pre-event | Captures persistent demand-side heterogeneity | Medium if baseline window overlaps treatment |
| Current visibility rank | Mediator / platform response | No | Post-treatment or contemporaneous | May be affected by treatment and may transmit treatment effect | High bad-control risk |
| Category fixed effects | Design control / FE | Yes | Time-invariant | Controls persistent category heterogeneity | Absorbs category-level time-invariant variables |
| Current engagement rate | Mechanism or outcome-proximate variable | No in main total-effect model | Contemporaneous/post-treatment | May be affected by the focal strategy and mechanically related to outcome | High |

The control-selection memo should explain these decisions in prose and distinguish main controls from robustness-only and mechanism-only variables.
