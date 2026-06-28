/**********************************************************************
07_did_event_study_checks.do
DID and event-study endogeneity checks.
Use only when treatment timing and comparison group are approved.
**********************************************************************/

* Treatment timing support
bysort $group_id $time_id: egen max_treat_gt = max($treat)
tab $time_id max_treat_gt, missing
bysort $group_id: egen ever_treated = max($treat)
tab ever_treated

didregress ($y $controls) ($treat), group($group_id) time($time_id) vce(cluster $group_id)
estimates store did_official

cap noisily estat trendplots
cap graph export "$figures/did_trendplots.png", replace
cap noisily estat ptrends
cap noisily estat granger
cap noisily estat grangerplot, nleads(4) nlags(6)
cap graph export "$figures/did_grangerplot.png", replace
cap noisily estat bdecomp

* Panel DID route
xtset $unit_id $time_id
cap noisily xtdidregress ($y $controls) ($treat), group($group_id) time($time_id) vce(cluster $group_id)
if _rc == 0 estimates store xtdid_official

* Optional event-time TWFE shell; user must construct event_time upstream or approve here.
* reghdfe $y ib(-1).event_time##i.ever_treated $controls, absorb($unit_id $time_id) vce(cluster $group_id)
* estimates store event_twfe

drop max_treat_gt ever_treated
