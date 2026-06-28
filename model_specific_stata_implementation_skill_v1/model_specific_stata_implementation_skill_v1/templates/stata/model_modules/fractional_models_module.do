****************************************************
* Fractional models module: fracreg / beta regression
****************************************************

* Required diagnostics before use:
* - outcome in [0,1]
* - boundary mass at 0 and 1
* - denominator/exposure logic
* - marginal effects required for interpretation

count if (Y_FRAC < 0 | Y_FRAC > 1) & $SAMPLE_MAIN
count if Y_FRAC == 0 & $SAMPLE_MAIN
count if Y_FRAC == 1 & $SAMPLE_MAIN
summarize Y_FRAC if $SAMPLE_MAIN, detail

fracreg logit Y_FRAC c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
estimates store MODEL_FRACREG
margins, dydx($FOCAL)

* Only for strictly interior proportions.
* betareg Y_FRAC c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, vce(cluster $CLUSTER_ID)
* estimates store MODEL_BETAREG
