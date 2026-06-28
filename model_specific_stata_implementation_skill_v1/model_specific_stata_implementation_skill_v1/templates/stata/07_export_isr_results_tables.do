****************************************************
* 07_export_isr_results_tables.do
* Export ISR-style results tables with controls included.
****************************************************

* Official Stata route. etable syntax varies by Stata version; verify manual/help.
* Use estimates dir to confirm stored models.
estimates dir

* Simple official table skeleton. Refine after C7 approval.
* etable, estimates(M_main_1 M_mod_1) showstars showstarsnote ///
*     export("$TABLES/main_results_isr_style.docx", replace)

* Community esttab route only if approved.
capture which esttab
if !_rc {
    esttab M_main_1 M_mod_1 using "$TABLES/main_results_isr_style.tex", replace ///
        b(%9.3f) se(%9.3f) parentheses ///
        star(+ 0.10 * 0.05 ** 0.01 *** 0.001) ///
        stats(N r2, labels("Number of observations" "R2") fmt(%9.0fc %9.3f)) ///
        label compress nomtitles nonotes
}
else {
    di as error "esttab not installed or not approved. Use etable/collect or export estimates manually."
}

* Always save estimation results for reproducibility.
estimates save "$OUTPUT/results/stored_estimates", replace
