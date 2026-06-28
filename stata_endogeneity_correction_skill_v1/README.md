# Stata Endogeneity Correction and Checks Skill

This package contains a Codex Skill for diagnosing and implementing Stata-based endogeneity mitigation strategies in archival Information Systems research.

Main file: `SKILL.md`

Key templates:

- `templates/stata/`: Stata implementation shells.
- `templates/python/00_retrieve_endogeneity_manuals.py`: manual-source audit helper.
- `templates/metadata/`: method registry, threat register, diagnostics map, and checkpoint log schemas.
- `templates/docs/`: memo templates for IV, DID, matching, dynamic panel, selection, measurement error, and ISR-style reporting.
- `templates/checklists/endogeneity_quality_gate.md`: final audit checklist.
- `examples/example_platform_endogeneity_workflow.md`: example use case for platform research.

The skill emphasizes that endogeneity is a research-design problem. Methods such as controls, fixed effects, lags, IV, DID, PSM/IPW, and dynamic panel GMM are valid only under assumptions that must be stated, audited, and reported.
