/**********************************************************************
06_control_function_endogenous_treatment.do
Control-function and endogenous-treatment models.
Use only after C5 approval.
**********************************************************************/

* Linear control-function model
cap noisily cfregress $y $controls ($x = $instrument_z), vce(cluster $cluster_id) first
if _rc == 0 estimates store cf_linear

* Endogenous interaction shell; replace moderator variable.
* global moderator "z_mod"
* cfregress $y $controls $moderator ($x = $instrument_z, interact($moderator)), mainonly(c.$x#c.$moderator) vce(cluster $cluster_id) first
* estimates store cf_interaction

* Endogenous binary treatment model, if treat is binary and approved.
cap noisily etregress $y $controls, treat($treat = $instrument_z $controls) vce(robust) first
if _rc == 0 {
    estimates store etregress_ml
    margins r.$treat, vce(unconditional)
}

* Count outcome endogenous treatment shell.
* etpoisson y_count $controls, treat($treat = $instrument_z $controls) vce(robust) first
* estimates store etpoisson_ml
