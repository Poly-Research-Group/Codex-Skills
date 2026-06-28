****************************************************
* 02_load_and_verify_data.do
* Load analysis-ready data and verify dataset structure.
****************************************************

use "$DATA/analysis_ready.dta", clear
compress
describe
datasignature
count

* ---- Required macros: fill after C0 approval ----
global UNIT_ID      "UNIT_ID"
global TIME_ID      "TIME_ID"
global CLUSTER_ID   "CLUSTER_ID"
global SAMPLE_MAIN  "1==1"

* ---- Verify key structure ----
* For panel models, the unit-time key should be unique unless row is intentionally dyadic/multilevel.
capture isid $UNIT_ID $TIME_ID
if _rc {
    di as error "Unit-time key is not unique. Run duplicate audit before panel estimation."
    duplicates report $UNIT_ID $TIME_ID
    duplicates tag $UNIT_ID $TIME_ID, gen(_dup_unit_time)
    tab _dup_unit_time
    * Stop by default. User must approve next step.
    error 459
}

xtset $UNIT_ID $TIME_ID
xtdescribe
xtsum

* Cluster support
capture confirm variable $CLUSTER_ID
if !_rc {
    tab $CLUSTER_ID if $SAMPLE_MAIN, missing
    quietly levelsof $CLUSTER_ID if $SAMPLE_MAIN, local(clusters)
    local nclusters : word count `clusters'
    di as result "Number of clusters = `nclusters'"
}
