# User Checkpoint Protocol for Stata Model Selection

This protocol prevents Codex from silently choosing an estimator family, fixed-effect structure, control set, or robustness plan without the researcher's review.

## Checkpoint C0. Intake confirmation
Codex must summarize the project title, empirical setting, research question, hypotheses, DV/IV/treatment roles, unit of analysis, time structure, data structure, identification strategy, controls, fixed effects, clustering candidates, and Stata environment. Codex must ask the user to confirm or correct this summary before proceeding.

## Checkpoint C1. Upstream readiness
Codex must summarize whether the data-preparation and empirical-design audit outputs classify the project as ready, conditionally ready, or blocked. If the audit contains high-risk issues, Codex must ask the user how to resolve them before recommending a primary estimator.

## Checkpoint C2. Outcome and data-structure classification
Codex must classify each dependent variable and the relevant data structure. For each outcome, Codex must ask whether the classification is correct, especially for ambiguous outcomes such as nonnegative skewed continuous variables, signed net-flow variables, fractional/proportion outcomes, and censored/corner-solution outcomes.

## Checkpoint C3. Identification and estimand
Codex must state whether each hypothesis is associational, causal, mechanism, moderation, mediation, prediction, or descriptive. Codex must state the implied estimand and ask the user to confirm whether the intended manuscript language matches the empirical design.

## Checkpoint C4. Primary-estimator shortlist
Codex must provide a ranked shortlist of candidate estimator families. It must explain why each candidate is plausible, why some families are rejected, and what diagnostics would decide between close alternatives.

## Checkpoint C5. Specification strategy
Codex must show the proposed baseline specification, control strategy, fixed effects, clustering, transformations, interaction terms, and marginal-effects plan. Codex must explicitly identify excluded bad controls and mechanism-only variables.

## Checkpoint C6. Community-command approval
Codex must ask whether community-contributed Stata commands may be recommended. If official Stata commands are sufficient, they should be the default. If user-written commands are recommended, Codex must include package checks and version notes.

## Checkpoint C7. Robustness and reporting
Codex must summarize the diagnostic requirements, robustness checks, model-fit statistics, coefficient/marginal-effect reporting, figures, and table notes before exporting the final model-selection package.

## Logging rule
Every checkpoint must be recorded in `output/model_selection/user_checkpoint_log.csv`. If a checkpoint is skipped, the model-selection recommendation must be labeled conditional.


## C3a. Mediation and mechanism checkpoint

When a hypothesis includes a mediator, mechanism, channel, or indirect effect, Codex must pause and show: treatment/key IV, mediator(s), outcome, timing order, mediator count, mediator ordering, support of mediator(s) and outcome, confounder plan for each path, FE/clustering feasibility, and the proposed mediation route. User approval is required before recommending `mediate`, two-mediator `mediate`, `sem`, `gsem`, or sequential-equation mechanism analysis.
