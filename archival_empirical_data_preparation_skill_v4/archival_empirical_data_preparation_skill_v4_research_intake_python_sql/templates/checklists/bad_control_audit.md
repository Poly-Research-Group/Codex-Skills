# Bad-Control Audit

Flag a candidate control as high risk when any answer below is yes.

| Question | Risk |
|---|---|
| Is the variable measured after the treatment/event? | Post-treatment control risk. |
| Could the treatment/event change this variable? | Overcontrol or mechanism-blocking risk. |
| Does the variable lie on the causal path from treatment to outcome? | Mediator/mechanism risk. |
| Is the variable jointly affected by treatment and unobserved outcome shocks? | Collider risk. |
| Is the variable mechanically calculated using the dependent variable? | Mechanical-overlap risk. |
| Is the variable an outcome of platform algorithms that react to the treatment? | Endogenous platform-measure risk. |
| Will the variable be absorbed by fixed effects? | Non-estimability or redundancy risk. |

High-risk controls should be excluded from the main total-effect model and, if theoretically useful, reserved for mechanism or robustness analyses with clear interpretation.
