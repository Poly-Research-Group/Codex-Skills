/**********************************************************************
12_export_isr_style_tables.do
Export ISR-style endogeneity results.
Controls are included by default. Update model lists before running.
**********************************************************************/

* Official etable route. Add/remove model names based on completed analyses.
cap noisily etable, estimates(baseline_pooled fe_main lagged_x_fe iv_2sls did_official psmatch_atet xtabond_main) ///
    showstars showstarsnote ///
    title("Endogeneity Correction and Robustness Checks") ///
    export("$tables/endogeneity_results_main.docx", replace)

cap noisily etable, estimates(baseline_pooled fe_main lagged_x_fe iv_2sls did_official psmatch_atet xtabond_main) ///
    showstars showstarsnote ///
    title("Endogeneity Correction and Robustness Checks") ///
    export("$tables/endogeneity_results_main.html", replace)

* Optional esttab route if approved.
cap which esttab
if _rc == 0 {
    esttab baseline_pooled fe_main lagged_x_fe iv_2sls did_official psmatch_atet xtabond_main using "$tables/endogeneity_results_main.tex", ///
        replace se star(+ 0.10 * 0.05 ** 0.01 *** 0.001) ///
        stats(N r2 r2_w, labels("Number of observations" "R-squared" "Within R-squared")) ///
        title("Endogeneity Correction and Robustness Checks")
}

* Optional outreg2 route if approved.
cap which outreg2
if _rc == 0 {
    outreg2 [baseline_pooled fe_main lagged_x_fe iv_2sls did_official psmatch_atet xtabond_main] using "$tables/endogeneity_results_main.doc", replace word ///
        bdec(3) tdec(2) addtext("Controls", "Included", "Fixed effects", "See table rows")
}
