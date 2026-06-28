/****************************************************************************************
  02_reporting_shell.do
  Purpose: Reporting shell for tables and figures after model-specific implementation.
****************************************************************************************/

version 19
set more off

global root        "<PROJECT_ROOT>"
global modelsel    "$root/stata_model_selection_package"
global tables      "$modelsel/tables"
global figures     "$modelsel/figures"
global logs        "$modelsel/logs"

capture log close
log using "$logs/02_reporting_shell.log", replace text

* ---- Export strategy placeholders ----
* Use official collect/table commands or approved community packages.
* Example official approach:
* collect clear
* estimates replay <MODEL_NAME>
* collect layout (colname) (result[_r_b _r_se _r_p])
* collect export "$tables/main_results.tex", replace

* ---- Marginal effects / predicted quantities ----
* margins, dydx(<FOCAL_IV>)
* marginsplot, name(<FIGURE_NAME>, replace)
* graph export "$figures/<FIGURE_NAME>.png", replace width(2000)

* ---- Event-study figure ----
* coefplot <EVENT_MODEL>, keep(<EVENT_TIME_TERMS>) vertical yline(0) xline(<OMITTED_PERIOD>)
* graph export "$figures/event_study_coefficients.png", replace width(2000)

* ---- Table notes checklist ----
* Every table should state:
* - Unit of analysis
* - Sample period and sample restrictions
* - Dependent variable definition
* - Controls included
* - Fixed effects included
* - Cluster/VCE level
* - Transformation/winsorization
* - Stata version and community command if used

log close
