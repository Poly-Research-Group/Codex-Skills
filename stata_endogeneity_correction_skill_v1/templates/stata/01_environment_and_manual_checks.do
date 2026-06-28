/**********************************************************************
01_environment_and_manual_checks.do
Check Stata version, commands, and optional community packages.
**********************************************************************/

about
which regress
which xtreg
which ivregress
which didregress
which teffects
which cfregress
which etregress
which xtabond
which xtdpdsys

* Optional community packages. Do not install without user approval.
foreach pkg in reghdfe ftools ivreg2 xtabond2 csdid eventstudyinteract did_imputation psmatch2 pstest rbounds boottest outreg2 esttab {
    cap which `pkg'
    if _rc {
        di as txt "Optional community command not found: `pkg'. Use only after user approval and installation."
    }
    else {
        di as result "Optional community command available: `pkg'"
    }
}
