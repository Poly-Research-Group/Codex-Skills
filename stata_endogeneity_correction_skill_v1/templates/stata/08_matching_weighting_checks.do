/**********************************************************************
08_matching_weighting_checks.do
Matching, weighting, and balance diagnostics.
Use only pre-treatment covariates in treatment model.
**********************************************************************/

* Official PSM route
cap noisily teffects psmatch ($y) ($treat $controls), atet nneighbor(1) osample(ps_osample)
if _rc == 0 {
    estimates store psmatch_atet
    cap noisily tebalance summarize
    cap noisily tebalance density $x
    cap graph export "$figures/tebalance_density_x.png", replace
    cap noisily tebalance box $x
    cap graph export "$figures/tebalance_box_x.png", replace
    cap noisily teoverlap
    cap graph export "$figures/teoverlap.png", replace
}

* IPW route
cap noisily teffects ipw ($y) ($treat $controls), atet
if _rc == 0 {
    estimates store ipw_atet
    cap noisily tebalance summarize, baseline
    cap noisily tebalance overid
    cap noisily teoverlap
}

* Doubly robust routes
cap noisily teffects ipwra ($y $controls) ($treat $controls), atet
if _rc == 0 {
    estimates store ipwra_atet
    cap noisily tebalance summarize, baseline
}

cap noisily teffects aipw ($y $controls) ($treat $controls), atet
if _rc == 0 {
    estimates store aipw_atet
    cap noisily tebalance summarize, baseline
}

* Optional psmatch2 route if approved and installed.
cap which psmatch2
if _rc == 0 {
    psmatch2 $treat $controls, outcome($y) neighbor(1) logit common ate
    cap which pstest
    if _rc == 0 pstest $controls, both
}
