/**********************************************************************
10_sample_selection_measurement_error_checks.do
Sample-selection and measurement-error checks.
**********************************************************************/

* Sample selection shell. Replace observed and selection_exclusion before use.
* global observed "observed_outcome"
* global selection_exclusion "z_select"
* heckman $y $x $controls, select($observed = $selection_exclusion $controls) vce(robust)
* estimates store heckman_ml

* Measurement error shell. Requires defensible reliability ratio.
* global reliability_x "0.80"
* eivreg $y $x $controls, r($x $reliability_x)
* estimates store eivreg_x

* Alternative-measure robustness shell.
* global x_alt1 "x_alternative_1"
* reg $y $x_alt1 $controls $fe_time, vce(cluster $cluster_id)
* estimates store alt_measure_1
