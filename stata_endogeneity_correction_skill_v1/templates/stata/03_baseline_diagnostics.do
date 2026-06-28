/**********************************************************************
03_baseline_diagnostics.do
Baseline diagnostics before endogeneity correction.
**********************************************************************/

* Summary and support
summarize $y $x $controls, detail

* Correlation among focal variables and controls
pwcorr $y $x $controls, sig obs

* VIF diagnostic using linear approximation, excluding high-dimensional FE dummies.
quietly regress $y $x $controls, vce(robust)
estimates store baseline_vif_model
estat vif

* Baseline robust/clustered model
regress $y $x $controls $fe_time, vce(cluster $cluster_id)
estimates store baseline_pooled

* Residual diagnostic shell
predict double resid_baseline if e(sample), residuals
summarize resid_baseline, detail
histogram resid_baseline, normal name(hist_resid_baseline, replace)
graph export "$figures/residual_distribution_baseline.png", replace

drop resid_baseline
