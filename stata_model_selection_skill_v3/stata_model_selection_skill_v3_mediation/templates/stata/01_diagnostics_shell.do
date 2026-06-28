/****************************************************************************************
  01_diagnostics_shell.do
  Purpose: Pre-estimation diagnostics shell for model selection.
****************************************************************************************/

version 19
clear all
set more off

global root        "<PROJECT_ROOT>"
global analysis    "$root/analysis_package/data/analysis"
global modelsel    "$root/stata_model_selection_package"
global output      "$modelsel/output"
global logs        "$modelsel/logs"

capture log close
log using "$logs/01_diagnostics_shell.log", replace text

use "$analysis/analysis_ready.dta", clear

* ---- Verify identifiers ----
local unit_id "<UNIT_ID>"
local time_id "<TIME_ID_OR_BLANK>"
local row_key "<ROW_KEY_VARLIST>"

capture noisily isid `row_key'
if _rc {
    di as error "Row key is not unique. Resolve before model implementation."
    duplicates report `row_key'
}

* ---- Panel/time declaration if applicable ----
capture noisily xtset `unit_id' `time_id'
if !_rc {
    xtdescribe
    xtsum <MAIN_VARIABLES>
}

* ---- Missingness and sample loss ----
misstable summarize <MAIN_VARIABLES>

* ---- Outcome-specific checks ----
foreach y in <DEPENDENT_VARIABLE_LIST> {
    di as result "Diagnostics for outcome: `y'"
    summarize `y', detail
    inspect `y'
    count if missing(`y')
    count if `y'==0 & !missing(`y')
    count if `y'<0 & !missing(`y')
}

* ---- Treatment/event timing checks ----
* Replace placeholders if treatment/event design exists.
* tab <TREATMENT>
* tab <COHORT_VAR>
* bysort <COHORT_VAR>: summarize <TIME_ID>
* tab <EVENT_TIME_VAR> <TREATMENT>, missing

* ---- Fixed-effect variation checks ----
foreach fe in <FIXED_EFFECT_LIST> {
    di as result "Fixed-effect dimension: `fe'"
    tab `fe' if e(sample)
}

* Example within-FE variation check for focal variable
* bysort <FE_DIMENSION>: egen min_x = min(<FOCAL_IV>)
* bysort <FE_DIMENSION>: egen max_x = max(<FOCAL_IV>)
* count if min_x == max_x

* ---- Cluster counts ----
foreach cl in <CLUSTER_VARIABLE_LIST> {
    preserve
    keep if !missing(`cl')
    bysort `cl': keep if _n==1
    count
    di as text "Number of clusters in `cl': " r(N)
    restore
}

log close
