/**********************************************************************
11_sensitivity_placebo_checks.do
Sensitivity and placebo shells. Run only approved checks.
**********************************************************************/

* Alternative control sets
* global controls_min "c1 c2"
* global controls_full "c1 c2 c3 c4 c5"
* xtreg $y $x $controls_min $fe_time, fe vce(cluster $cluster_id)
* estimates store fe_controls_min
* xtreg $y $x $controls_full $fe_time, fe vce(cluster $cluster_id)
* estimates store fe_controls_full

* Placebo outcome shell
* global placebo_y "pre_treatment_outcome"
* xtreg $placebo_y $x $controls $fe_time, fe vce(cluster $cluster_id)
* estimates store placebo_outcome

* Placebo treatment timing shell for DID
* global placebo_treat "placebo_treat"
* didregress ($y $controls) ($placebo_treat), group($group_id) time($time_id) vce(cluster $group_id)
* estimates store placebo_did

* Alternative lag shells
* xtreg $y L2.$x $controls $fe_time, fe vce(cluster $cluster_id)
* estimates store lagged_x2_fe
