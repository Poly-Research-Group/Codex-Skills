# Stata Model-Selection Report

## 1. Project and hypothesis overview

Project label: `<PROJECT_LABEL>`

Empirical setting: `<EMPIRICAL_SETTING>`

Research question: `<RESEARCH_QUESTION>`

Hypotheses covered in this model-selection report:

| Hypothesis | Claim type | DV | Key IV/treatment | Expected direction | Estimand |
|---|---|---|---|---|---|
| H1 | `<CLAIM_TYPE>` | `<DV>` | `<IV_OR_TREATMENT>` | `<DIRECTION>` | `<ESTIMAND>` |

## 2. Upstream design-readiness summary

- Design-audit status: `<ready | conditionally ready | not ready>`
- Blocking issues: `<NONE_OR_LIST>`
- Conditional assumptions: `<NONE_OR_LIST>`
- Relevant design threats: `<THREAT_SUMMARY>`

## 3. Dependent-variable and data-structure classification

| Hypothesis | DV support | Data structure | Unit of analysis | Time grain | Implication for model family |
|---|---|---|---|---|---|
| H1 | `<SUPPORT>` | `<STRUCTURE>` | `<UNIT>` | `<TIME>` | `<IMPLICATION>` |

## 4. Recommended estimator families

| Hypothesis | Primary family | Primary Stata commands | Secondary families | Selection status |
|---|---|---|---|---|
| H1 | `<PRIMARY_FAMILY>` | `<COMMANDS>` | `<SECONDARY>` | `<READY/CONDITIONAL>` |

### Rationale for the primary recommendation

`<Explain how the estimator matches the claim type, DV support, data structure, identification strategy, controls, FE, and inference needs.>`

### Estimator families considered and rejected

| Hypothesis | Rejected family | Reason rejected | What would make it appropriate |
|---|---|---|---|
| H1 | `<FAMILY>` | `<REASON>` | `<CONDITION>` |

## 5. Specification blueprint

Baseline specification logic:

- Dependent variable: `<DV>`
- Focal independent variable/treatment: `<IV_OR_TREATMENT>`
- Moderators/interactions: `<MODERATOR_TERMS>`
- Mediators/mechanisms: `<MEDIATOR_PLAN>`
- Controls: `<CONFIRMED_CONTROLS>`
- Fixed effects: `<FE_PLAN>`
- Random effects, if any: `<RE_PLAN>`
- Clustering: `<CLUSTER_PLAN>`
- Transformations: `<TRANSFORMATION_PLAN>`
- Sample: `<SAMPLE_PLAN>`

## 6. Required diagnostics before implementation

| Estimator family | Required diagnostic | Method/Stata command | Pass/fail or interpretation rule |
|---|---|---|---|
| `<FAMILY>` | `<DIAGNOSTIC>` | `<COMMAND>` | `<RULE>` |

## 7. Reporting requirements

| Estimator family | Required table/figure | Required statistics | Interpretation |
|---|---|---|---|
| `<FAMILY>` | `<TABLE_OR_FIGURE>` | `<STATISTICS>` | `<INTERPRETATION>` |

## 8. Robustness and sensitivity plan

| Robustness check | Design threat addressed | Alternative model/specification | Priority |
|---|---|---|---|
| `<CHECK>` | `<THREAT>` | `<MODEL>` | `<HIGH/MEDIUM/LOW>` |

## 9. Stata command and package plan

| Command/package | Official/community | Purpose | Version/package check |
|---|---|---|---|
| `<COMMAND>` | `<OFFICIAL_OR_COMMUNITY>` | `<PURPOSE>` | `<CHECK>` |

## 10. Handoff to model-specific implementation skill

Recommended next skill: `<MODEL_SPECIFIC_SKILL>`

Inputs to pass:

- Analysis-ready dataset: `<PATH>`
- Hypothesis-model map: `output/model_selection/hypothesis_model_map.csv`
- Specification blueprint: `output/model_selection/specification_blueprint.csv`
- Diagnostics requirements: `output/model_selection/diagnostics_requirements.csv`
- Robustness plan: `output/model_selection/robustness_plan.csv`

## 11. Assumptions and unresolved risks

| Assumption/risk | Severity | User decision needed? | Recommended action |
|---|---|---|---|
| `<RISK>` | `<LOW/MEDIUM/HIGH>` | `<YES/NO>` | `<ACTION>` |
