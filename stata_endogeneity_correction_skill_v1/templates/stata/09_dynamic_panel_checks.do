/**********************************************************************
09_dynamic_panel_checks.do
Dynamic panel GMM checks for lagged dependent variable/endogeneity.
Use only for many-N/few-T panel settings and approved instrument plans.
**********************************************************************/

xtset $unit_id $time_id

* Arellano-Bond
cap noisily xtabond $y $x $controls, lags(1) vce(robust)
if _rc == 0 {
    estimates store xtabond_main
    cap noisily estat abond
    cap noisily estat sargan
}

* Arellano-Bover/Blundell-Bond system GMM
cap noisily xtdpdsys $y $x $controls, lags(1) maxldep(2) vce(robust)
if _rc == 0 {
    estimates store xtdpdsys_main
    cap noisily estat abond
    cap noisily estat sargan
}

* Optional xtabond2 route if approved and installed.
cap which xtabond2
if _rc == 0 {
    xtabond2 $y L.$y $x $controls $fe_time, gmm(L.$y $x, lag(2 .) collapse) iv($controls $fe_time) twostep robust small
    estimates store xtabond2_optional
}
