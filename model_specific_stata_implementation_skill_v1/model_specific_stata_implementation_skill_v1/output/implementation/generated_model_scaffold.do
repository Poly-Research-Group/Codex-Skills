****************************************************
* Project-specific Stata model implementation scaffold
* Generated from stata_command_plan.csv
****************************************************

* Commands requested by model-selection skill:
* - xtset: Declare streamer-week panel
* - xtreg, fe: Primary linear FE route with creator clustering
* - xtreg, fe absorb(): Native Stata 19 HDFE route for linear panel FE models with absorbed week FE
* - regress: Pooled descriptive robustness and generated-transform checks
* - areg: Official absorbed-linear fallback for high-dimensional categorical variables where useful
* - poisson: Support-matched count outcome route
* - xtpoisson: Panel count route where FE/count assumptions fit
* - nbreg: Overdispersion robustness for count outcomes
* - xtnbreg: Panel negative-binomial robustness where appropriate
* - fracreg: Fractional-response robustness for mechanism shares
* - margins: Marginal effects and moderation interpretation
* - marginsplot: Moderation/predicted-outcome plots
* - lincom: Direct contrasts and simple slopes
* - nlcom: Indirect effects, VAF components, and nonlinear combinations
* - bootstrap: Bootstrap sensitivity for mediation-style decomposition
* - testnl: Nonlinear tests where needed
* - reghdfe: Legacy/community HDFE convenience and multiway clustering route
* - ftools: Dependency for reghdfe
* - ppmlhdfe: PPML-HDFE robustness for count/nonnegative outcomes
* - boottest: Wild-cluster bootstrap sensitivity
* - estout/esttab: Manuscript table export convenience

* Fill in these macros only after C4 main-specification approval.
global ANALYSIS_DTA "data/analysis_ready.dta"
global UNIT_ID      "UNIT_ID"
global TIME_ID      "TIME_ID"
global CLUSTER_ID   "CLUSTER_ID"
global CONTROLS     "CONTROL_1 CONTROL_2 CONTROL_3"
global FE_TIME      "i.TIME_ID"

* Example model placeholder:
* xtset $UNIT_ID $TIME_ID
* xtreg DEPVAR c.FOCAL_VAR##c.MODERATOR $CONTROLS i.TIME_ID, fe vce(cluster $CLUSTER_ID)
* estimates store MODEL_NAME
