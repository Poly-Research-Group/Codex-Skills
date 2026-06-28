/**********************************************************************
04_controls_fe_lagged_checks.do
Controls, fixed effects, high-dimensional FE, and lagged-X checks.
**********************************************************************/

* Controls-only / baseline model already estimated in 03.

* Fixed effects model
xtset $unit_id $time_id
xtreg $y $x $controls $fe_time, fe vce(cluster $cluster_id)
estimates store fe_main

* Check identifying variation in focal variable
xtsum $x
bysort $unit_id: egen sd_x_within = sd($x)
summarize sd_x_within, detail
count if sd_x_within == 0 | missing(sd_x_within)
drop sd_x_within

* Official absorb option where available in user's Stata version
cap noisily xtreg $y $x $controls, fe absorb($time_id) vce(cluster $cluster_id)
if _rc == 0 estimates store fe_absorb_official

* Optional reghdfe route if installed and approved
cap which reghdfe
if _rc == 0 {
    reghdfe $y $x $controls, absorb($unit_id $time_id) vce(cluster $cluster_id)
    estimates store hdfe_optional
}

* Lagged X check for temporal ordering / reverse causality
xtset $unit_id $time_id
cap confirm variable L1_$x
if _rc {
    gen double L1_$x = L.$x
}
count if missing(L1_$x) & !missing($x)
xtreg $y L1_$x $controls $fe_time, fe vce(cluster $cluster_id)
estimates store lagged_x_fe

* Alternative lag shell; use only if theoretically approved.
* xtreg $y L2.$x $controls $fe_time, fe vce(cluster $cluster_id)
* estimates store lagged_x2_fe
