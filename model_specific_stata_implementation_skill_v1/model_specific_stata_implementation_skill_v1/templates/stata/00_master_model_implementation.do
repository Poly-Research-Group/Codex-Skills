****************************************************
* 00_master_model_implementation.do
* Model-specific Stata implementation master file
****************************************************
version 19
clear all
set more off
set linesize 255
set seed 20260621

* ---- Project paths: edit after C0 approval ----
global ROOT        "PROJECT_ROOT"
global DATA        "$ROOT/data"
global CODE        "$ROOT/code"
global OUTPUT      "$ROOT/output"
global LOGS        "$OUTPUT/logs"
global TABLES      "$OUTPUT/tables"
global FIGURES     "$OUTPUT/figures"
global DIAG        "$OUTPUT/diagnostics"
cap mkdir "$OUTPUT"
cap mkdir "$LOGS"
cap mkdir "$TABLES"
cap mkdir "$FIGURES"
cap mkdir "$DIAG"

cap log close _all
log using "$LOGS/00_master_model_implementation.log", replace text

* ---- Run sequence ----
do "$CODE/01_environment_and_manual_checks.do"
do "$CODE/02_load_and_verify_data.do"
do "$CODE/03_pre_estimation_diagnostics.do"

* C3 checkpoint should occur after diagnostics, before estimation.
* Proceed only after approved specification_adjustment_memo.md.

do "$CODE/04_main_models.do"
do "$CODE/05_moderation_interactions.do"
do "$CODE/06_robustness_additional_analyses.do"
do "$CODE/07_export_isr_results_tables.do"

log close
