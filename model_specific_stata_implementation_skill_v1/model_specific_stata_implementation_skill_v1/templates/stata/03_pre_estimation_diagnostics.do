****************************************************
* 03_pre_estimation_diagnostics.do
* Diagnostics before main estimation.
****************************************************

* ---- Fill these macros after C2 diagnostic-plan approval ----
global Y_MAIN       "DEPENDENT_VARIABLE"
global FOCAL       "FOCAL_IV_OR_TREATMENT"
global MODERATOR   "MODERATOR_IF_ANY"
global CONTROLS    "CONTROL_1 CONTROL_2 CONTROL_3"
global ALL_X       "$FOCAL $MODERATOR $CONTROLS"

di as text "Missingness diagnostics"
misstable summarize $Y_MAIN $ALL_X $UNIT_ID $TIME_ID $CLUSTER_ID

summarize $Y_MAIN $ALL_X if $SAMPLE_MAIN, detail

* Correlations among nonabsorbed focal variables and controls.
pwcorr $ALL_X if $SAMPLE_MAIN, sig obs star(0.05)

* VIF approximation. For FE/HDFE models, this is a nonabsorbed-covariate redundancy diagnostic,
* not a substitute for within-variation and FE collinearity checks.
capture noisily regress $Y_MAIN $ALL_X if $SAMPLE_MAIN
if !_rc {
    estat vif
}
else {
    di as error "VIF approximation failed; inspect missingness, support, or exact collinearity."
}

* Within/between variation for panel models.
xtsum $Y_MAIN $ALL_X if $SAMPLE_MAIN

* Outcome support templates.
count if $Y_MAIN < 0 & $SAMPLE_MAIN
count if $Y_MAIN == 0 & $SAMPLE_MAIN
count if $Y_MAIN == 1 & $SAMPLE_MAIN
summarize $Y_MAIN if $SAMPLE_MAIN, detail

* Count outcome checks: uncomment for count models.
* quietly summarize $Y_COUNT if $SAMPLE_MAIN
* di as result "Mean = " r(mean) " Var = " r(Var)
* count if $Y_COUNT < 0 & $SAMPLE_MAIN
* count if $Y_COUNT == 0 & $SAMPLE_MAIN

* Fractional outcome checks: uncomment for fractional models.
* count if ($Y_FRAC < 0 | $Y_FRAC > 1) & $SAMPLE_MAIN
* count if $Y_FRAC == 0 & $SAMPLE_MAIN
* count if $Y_FRAC == 1 & $SAMPLE_MAIN

* Interaction feasibility. Factor-variable notation should be used in estimation.
* If using generated interaction only for diagnostics, mark it temporary.
capture drop _tmp_interaction
capture gen double _tmp_interaction = $FOCAL * $MODERATOR if $SAMPLE_MAIN
capture xtsum _tmp_interaction if $SAMPLE_MAIN
