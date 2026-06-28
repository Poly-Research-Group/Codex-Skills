# Empirical Design Audit Skill

This package contains a reusable Codex Skill for auditing archival empirical research designs before econometric model selection or estimation.

The skill is intended to be used after the data-preparation skill has produced an analysis-ready dataset and metadata package. It verifies unit of analysis, timing, treatment/event construction, controls, sample restrictions, fixed-effect and clustering feasibility, and identification threats. The output is a design-audit package and a handoff memo for the later Stata model-selection skill.

The default audit stack is Python + SQL. Stata is treated as downstream.
