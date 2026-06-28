****************************************************
* 06_robustness_additional_analyses.do
* Robustness and additional analyses after C6 approval.
****************************************************

* Robustness examples. Keep structure parallel to main tables.

* R1: Alternative dependent variable / untransformed outcome.
* xtreg Y_ALT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
* estimates store R_alt_dv_1

* R2: Alternative time window / sample.
* xtreg $Y_MAIN c.$FOCAL $CONTROLS i.$TIME_ID if SAMPLE_WINDOW_ALT, fe vce(cluster $CLUSTER_ID)
* estimates store R_window_1

* R3: Alternative control set.
* xtreg $Y_MAIN c.$FOCAL $CONTROLS_ALT i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
* estimates store R_controls_1

* R4: Alternative estimator for count or nonnegative outcome.
* poisson Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
* estimates store R_poisson_1
* nbreg Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
* estimates store R_nb_1

* R5: Community-command optional route, only if approved and installed.
* capture which reghdfe
* if !_rc {
*     reghdfe $Y_MAIN c.$FOCAL $CONTROLS if $SAMPLE_MAIN, absorb($UNIT_ID $TIME_ID) vce(cluster $CLUSTER_ID)
*     estimates store R_reghdfe_1
* }
