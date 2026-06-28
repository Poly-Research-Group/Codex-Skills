# Example Variable Timing Audit

| Variable | Empirical role | Measurement window | Valid main-model use? | Reason |
|---|---|---|---:|---|
| Treatment_i,t | Treatment / focal event | Event period | Yes | Defines exposure. |
| Outcome_i,t+1 | Dependent variable | Post-event | Yes | Occurs after treatment. |
| Prior_Outcome_i,t-1 | Pre-treatment control | Pre-event or lagged | Yes | Captures baseline outcome level without conditioning on post-treatment response. |
| Current_Visibility_i,t+1 | Mechanism | Post-event | No in total-effect model | May be caused by treatment and may mediate treatment effect. |
| Network_Structure_i,t-1 | Moderator | Pre-event or predetermined | Yes as moderator | Represents boundary condition before focal outcome. |
| Post_Engagement_i,t+1 | Mediator / mechanism | Post-event | No in main effect model | Blocks part of the hypothesized effect if controlled. |
