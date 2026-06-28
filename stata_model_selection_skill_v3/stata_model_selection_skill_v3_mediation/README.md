# Stata Model Selection Skill v3: Checkpoints, Fractional Outcomes, and Mediation Models

This Codex Skill maps archival IS research designs to appropriate Stata estimator families after data preparation and empirical design audit.

Version 3 adds:

1. Mandatory user checkpoints C0-C7 plus a new C3a mediation/mechanism checkpoint.
2. A checkpoint log template in `templates/metadata/user_checkpoint_log.csv`.
3. A user checkpoint protocol in `templates/docs/user_checkpoint_protocol.md`.
4. Explicit fractional, proportion, share, rate, and bounded-outcome model-selection guidance.
5. Expanded fractional model registry rows for `fractional_response`, `beta_regression`, and `two_part_fractional`.
6. Expanded mediation model routing across official `mediate`, StataNow two-mediator `mediate`, `sem`, `gsem`, and sequential-equation mechanism analyses.
7. New mediation artifacts: `templates/metadata/mediation_model_family_registry.csv`, `templates/docs/mediation_model_selection_notes.md`, and `templates/stata/03_mediation_selection_skeleton.do`.

Use this skill after the Python/SQL archival data-preparation skill and the empirical design audit skill.
