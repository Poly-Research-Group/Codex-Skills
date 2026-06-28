/**********************************************************************
00_master_endogeneity.do
Master file for Stata endogeneity correction/check workflow.
Edit globals and run from the project root after user checkpoints are approved.
**********************************************************************/

version 19
clear all
set more off
set seed 20260621

* ---------- USER SETTINGS ----------
global root        "PROJECT_ROOT"
global data        "$root/data/analysis_ready.dta"
global output      "$root/output"
global tables      "$output/tables"
global figures     "$output/figures"
global logs        "$output/logs"

cap mkdir "$output"
cap mkdir "$tables"
cap mkdir "$figures"
cap mkdir "$logs"

cap log close _all
log using "$logs/endogeneity_master.log", replace text

* ---------- PIPELINE ----------
do "$root/code/01_environment_and_manual_checks.do"
do "$root/code/02_load_and_verify_data.do"
do "$root/code/03_baseline_diagnostics.do"
do "$root/code/04_controls_fe_lagged_checks.do"
do "$root/code/05_iv_2sls_checks.do"
do "$root/code/06_control_function_endogenous_treatment.do"
do "$root/code/07_did_event_study_checks.do"
do "$root/code/08_matching_weighting_checks.do"
do "$root/code/09_dynamic_panel_checks.do"
do "$root/code/10_sample_selection_measurement_error_checks.do"
do "$root/code/11_sensitivity_placebo_checks.do"
do "$root/code/12_export_isr_style_tables.do"

log close
