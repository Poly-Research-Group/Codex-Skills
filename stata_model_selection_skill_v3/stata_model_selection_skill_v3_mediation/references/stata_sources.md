# Stata Source Notes for the Model-Selection Skill

Use official Stata documentation as the default source for available commands and syntax. Community-contributed commands should be treated as optional and used only with explicit user approval and package checks.

Key official Stata documentation areas to consult when updating this skill:

- Stata features overview: model families across linear models, panel/longitudinal data, mixed models, binary/count/limited outcomes, choice models, extended regression models, GLMs, finite mixtures, spatial autoregressive models, time series, survival analysis, Bayesian analysis, causal inference/treatment effects, lasso, SEM, latent class analysis, and more.
- Linear regression: `regress`, including robust, cluster-robust, multiway cluster, bootstrap/jackknife, and HAC VCE options.
- Panel models: `xtreg`, including fixed effects, random effects, between effects, population-averaged models, and correlated random effects where available.
- Difference-in-differences: `didregress` and `xtdidregress`, plus heterogeneous DID commands where available in the user's Stata version.
- Instrumental variables: `ivregress`, `xtivreg`, and postestimation diagnostics such as first-stage, endogeneity, overidentification, and weak-IV robust inference where available.
- Control-function models: `cfregress` and `cfprobit` where available.
- HDFE: official `absorb()` support for `areg`, `xtreg, fe`, and `ivregress 2sls` where available.
- Binary, count, limited, survival, multilevel, SEM/GSEM, lasso, spatial, Bayesian, and finite-mixture model manuals.

Optional community commands often used in archival IS/econometric work include `reghdfe`, `ppmlhdfe`, `csdid`, `eventstudyinteract`, `did_imputation`, `rdrobust`, `synth`, `sdid`, `ivreg2`, `xtabond2`, and `ddml`. These should not be assumed installed.


Additional official Stata mediation sources to consult:

- Causal mediation analysis feature page: https://www.stata.com/features/overview/causal-mediation-analysis/
- `[CAUSAL] mediate` manual: https://www.stata.com/manuals/causalmediate.pdf
- Causal mediation analysis with two mediators / StataNow feature page: https://www.stata.com/statanow/causal-mediation-analysis-two-mediators/
- `[CAUSAL] mediate multiple` manual: https://www.stata.com/manuals/causalmediatemultiple.pdf
- SEM feature page: https://www.stata.com/features/overview/structural-equation-modeling/
- GSEM feature page: https://www.stata.com/features/overview/generalized-sem/

For mediation, Codex should default to official Stata commands. Community-contributed commands such as `paramed`, `medeff`, `sgmediation`, `medsem`, or `khb` may be mentioned only as optional routes requiring user approval, package checks, and a method citation in the manuscript.
