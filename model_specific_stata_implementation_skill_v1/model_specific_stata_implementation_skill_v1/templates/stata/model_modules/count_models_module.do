****************************************************
* Count models module: poisson, nbreg, xtpoisson, xtnbreg
****************************************************

* Required diagnostics before use:
* - outcome nonnegative integer/count support
* - zeros and overdispersion
* - exposure/offset definition if modeling rates
* - FE/clustering feasibility

summarize Y_COUNT if $SAMPLE_MAIN, detail
count if Y_COUNT < 0 & $SAMPLE_MAIN
count if Y_COUNT == 0 & $SAMPLE_MAIN

poisson Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
estimates store MODEL_POISSON
margins, dydx($FOCAL)

nbreg Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
estimates store MODEL_NB

xtpoisson Y_COUNT c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
estimates store MODEL_XTPOISSON
