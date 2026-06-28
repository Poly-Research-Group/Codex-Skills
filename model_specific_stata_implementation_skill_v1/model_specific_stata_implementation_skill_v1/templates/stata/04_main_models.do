****************************************************
* 04_main_models.do
* Main model implementation after C4 approval.
****************************************************

* ---- Baseline linear panel FE template ----
* Replace placeholders with approved variables.
xtset $UNIT_ID $TIME_ID

* Main effect model.
xtreg $Y_MAIN c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
estimates store M_main_1

* Optional native absorb() route in Stata 19/StataNow if approved and syntax supported.
* xtreg $Y_MAIN c.$FOCAL $CONTROLS if $SAMPLE_MAIN, fe absorb(ABSORB_FE_VAR) vce(cluster $CLUSTER_ID)
* estimates store M_main_1_absorb

* Pooled/descriptive robustness if approved.
* regress $Y_MAIN c.$FOCAL $CONTROLS i.$TIME_ID i.CATEGORY_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
* estimates store M_pool_1

* Count model templates if selected.
* poisson Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
* estimates store M_pois_1
* nbreg Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
* estimates store M_nb_1
* xtpoisson Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
* estimates store M_xtpois_1

* Fractional model templates if selected.
* fracreg logit Y_FRAC c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
* estimates store M_frac_1
* margins, dydx($FOCAL)
