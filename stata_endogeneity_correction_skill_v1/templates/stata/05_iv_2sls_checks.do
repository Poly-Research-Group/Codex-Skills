/**********************************************************************
05_iv_2sls_checks.do
Instrumental variables / 2SLS checks.
Requires user-approved instrument_validity_memo.md.
**********************************************************************/

* First stage manually estimated for transparency
regress $x $instrument_z $controls $fe_time, vce(cluster $cluster_id)
estimates store iv_first_stage_manual

* Reduced form
regress $y $instrument_z $controls $fe_time, vce(cluster $cluster_id)
estimates store iv_reduced_form

* 2SLS
ivregress 2sls $y $controls $fe_time ($x = $instrument_z), vce(cluster $cluster_id)
estimates store iv_2sls

* Official postestimation diagnostics; some are conditional on estimator/VCE/identification.
cap noisily estat firststage, all
cap noisily estat endogenous
cap noisily estat overid
cap noisily estat weakrobust

* Panel IV shell; use only if approved.
cap noisily xtivreg $y $controls $fe_time ($x = $instrument_z), fe vce(cluster $cluster_id)
if _rc == 0 estimates store xtiv_fe

* Optional ivreg2 route if approved and installed.
cap which ivreg2
if _rc == 0 {
    ivreg2 $y $controls $fe_time ($x = $instrument_z), cluster($cluster_id) first endog($x) weakiv
    estimates store ivreg2_optional
}
