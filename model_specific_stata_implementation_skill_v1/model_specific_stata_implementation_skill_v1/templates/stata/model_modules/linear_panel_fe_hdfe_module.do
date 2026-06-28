****************************************************
* Linear / Panel FE / HDFE module
****************************************************

* Required diagnostics before use:
* - xtset and unit-time uniqueness
* - within variation in focal variables
* - multicollinearity among nonabsorbed variables
* - cluster count and cluster-size distribution
* - variables omitted by collinearity

xtset $UNIT_ID $TIME_ID
xtreg $Y_MAIN c.$FOCAL $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
estimates store MODEL_LINEAR_FE

* Moderation version
xtreg $Y_MAIN c.$FOCAL##c.$MODERATOR $CONTROLS i.$TIME_ID if $SAMPLE_MAIN, fe vce(cluster $CLUSTER_ID)
estimates store MODEL_LINEAR_FE_MOD
margins, dydx($FOCAL) at($MODERATOR=(P10 P50 P90))
