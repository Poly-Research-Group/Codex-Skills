/**********************************************************************
03_mediation_selection_skeleton.do
Purpose: Placeholder code skeleton for mediation/model-selection handoff.
This file is not final analysis code. Replace placeholders only after C3a
mediation/mechanism checkpoint is approved.
**********************************************************************/

version 19
set more off

*------------------------------------------------------------
* 0. Confirm user-approved mediation route
*------------------------------------------------------------
* Required: treatment/key IV, mediator(s), outcome, timing, controls,
* FE, clustering, Stata version, and claim type.

* local y        "OUTCOME_VAR"
* local t        "TREATMENT_OR_KEY_IV"
* local m1       "MEDIATOR_1"
* local m2       "MEDIATOR_2"   // optional
* local controls "PRETREATMENT_CONTROLS"
* local clustvar "CLUSTER_VAR"

*------------------------------------------------------------
* 1. Official one-mediator causal mediation route
*------------------------------------------------------------
* Example syntax only. Choose outcome/mediator model after support audit.
*
* mediate (`y' `controls', linear) (`m1' `controls', linear) (`t'), ///
*     vce(cluster `clustvar') all aequations
* estat cde, mvalue((mean) `m1')
* estat proportion
* estat effectsplot

*------------------------------------------------------------
* 2. Official two-mediator route, if StataNow feature is available
*------------------------------------------------------------
* Parallel example:
* mediate (`y' `controls') (`m2' `controls') (`m1' `controls') (`t'), parallel ///
*     vce(cluster `clustvar') aequations
*
* Sequential example:
* mediate (`y' `controls') (`m2' `controls') (`m1' `controls') (`t'), sequential ///
*     tinteraction minteraction vce(cluster `clustvar') aequations

*------------------------------------------------------------
* 3. SEM/GSEM path model route
*------------------------------------------------------------
* sem (`m1' <- `t' `controls') (`y' <- `t' `m1' `controls'), ///
*     vce(cluster `clustvar') standardized
* estat teffects
* estat gof, stats(all)
*
* gsem (`m1' <- `t' `controls', family(gaussian) link(identity)) ///
*      (`y'  <- `t' `m1' `controls', family(gaussian) link(identity)), ///
*      vce(cluster `clustvar')
* nlcom (_b[`m1':`t'] * _b[`y':`m1'])

*------------------------------------------------------------
* 4. Sequential-equation mechanism route for panel/HDFE settings
*------------------------------------------------------------
* Total effect model: treatment -> outcome without mediator
* regress `y' `t' `controls', vce(cluster `clustvar')
*
* Mediator equation: treatment -> mediator
* regress `m1' `t' `controls', vce(cluster `clustvar')
*
* Direct/mechanism equation: treatment + mediator -> outcome
* regress `y' `t' `m1' `controls', vce(cluster `clustvar')
*
* Product-of-coefficients or path effect only if scale and assumptions are defensible:
* nlcom (_b_mediator_equation[`t'] * _b_outcome_equation[`m1'])

* End of skeleton.
