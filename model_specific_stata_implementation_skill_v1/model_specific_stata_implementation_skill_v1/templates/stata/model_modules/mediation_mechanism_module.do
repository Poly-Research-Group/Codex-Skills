****************************************************
* Mediation / mechanism module
****************************************************

* Use official mediate only when formal causal mediation assumptions and timing are approved.
* Otherwise, use sequential mechanism evidence with explicit interpretation limits.

* Sequential mechanism evidence example:
xtreg MEDIATOR c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
estimates store MECH_path_a

xtreg $Y_MAIN c.$FOCAL c.MEDIATOR $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
estimates store MECH_path_b

* Indirect-effect style calculation only if theoretically and statistically justified.
* nlcom _b[MEDIATOR] * PATH_A_COEFFICIENT

* Formal causal mediation example (requires approved support and compatible model):
* mediate (OUTCOME_MODEL) (MEDIATOR_MODEL) (TREATMENT), vce(robust)
