from __future__ import annotations
from pathlib import Path
import pandas as pd
from utils_audit import read_config, ensure_output_dirs, setup_logging, write_md, save_csv

FAMILIES = [
    ("OLS/HDFE", "Continuous or approximately continuous outcome; sufficient variation after FE; clustering plan."),
    ("Panel FE", "Repeated observations per unit; within-unit variation in key variables; serial correlation handled."),
    ("Correlated random effects", "Panel data; time-invariant covariates of interest; correlated heterogeneity handled via means."),
    ("DID/event study", "Treatment timing; treated/control support; pre-periods; no anticipation; staggered adoption addressed."),
    ("IV/control function", "Instrument/excluded variable; relevance and exclusion logic; timing."),
    ("Treatment effects/matching", "Observable pre-treatment covariates; overlap; balance diagnostics."),
    ("Regression discontinuity", "Running variable; cutoff; local support; manipulation checks."),
    ("Count models", "Nonnegative integer outcome; exposure/offset if rate; zero and overdispersion checks."),
    ("Limited dependent variable", "Binary/ordinal/nominal/censored/fractional outcome support."),
    ("Survival/duration", "Risk set, event indicator, censoring, origin/time scale."),
    ("Dynamic panel", "Lagged outcome theory; sufficient panel length; instrument proliferation risk handled."),
    ("Network/spillover", "Network/exposure mapping; interference explicitly theorized; dependence handled."),
]


def read_audit(dirs, name):
    p = dirs["audits"] / name
    return pd.read_csv(p) if p.exists() else pd.DataFrame()


def decide_overall(dirs):
    critical = []
    for name in [
        "unit_time_structure_audit.csv",
        "timing_and_leakage_audit.csv",
        "treatment_event_construction_audit.csv",
        "outcome_support_audit.csv",
        "control_bad_control_audit.csv",
        "sample_restriction_attrition_audit.csv",
        "fixed_effect_clustering_readiness_audit.csv",
    ]:
        df = read_audit(dirs, name)
        if not df.empty and "severity" in df.columns:
            bad = df[df["severity"].astype(str).isin(["critical", "high"])]
            for _, r in bad.iterrows():
                critical.append(f"{name}: {r.to_dict()}")
    if critical:
        return "NOT READY", critical
    return "CONDITIONALLY READY", []


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "09_export_design_audit_package")

    intended = config.get("design", {}).get("intended_design_family", []) or []
    if isinstance(intended, str):
        intended = [intended]

    matrix = []
    for family, conditions in FAMILIES:
        fam_key = family.lower().replace("/", "_").replace(" ", "_")
        applicable = "candidate" if any(x in fam_key for x in [i.lower() for i in intended]) else "requires_model_selection"
        matrix.append({
            "design_or_model_family": family,
            "applicability": applicable,
            "required_conditions": conditions,
            "conditions_satisfied": "see design-audit report",
            "conditions_not_satisfied": "see design-audit report",
            "required_later_diagnostics": "to be specified by model-selection skill",
            "readiness_status": "conditionally_ready" if applicable == "candidate" else "not_assessed",
            "notes_for_model_selection_skill": "Use this as a candidate only if hypothesis/design logic supports it.",
        })
    save_csv(pd.DataFrame(matrix), dirs, "estimator_readiness_matrix.csv")


    robustness_rows = [
        {
            "robustness_id": "R001",
            "triggering_audit_issue": "general_identification_uncertainty",
            "robustness_check": "Alternative sample definitions and exclusion of ambiguous units/events",
            "design_family": ",".join(intended) if intended else "general",
            "variables_needed": "row key, treatment/key IV, outcome",
            "sample_needed": "main analysis sample and documented alternatives",
            "priority": "high",
            "notes": "Refine based on project-specific threat register before modeling",
        },
        {
            "robustness_id": "R002",
            "triggering_audit_issue": "timing_window_uncertainty",
            "robustness_check": "Alternative lag/event windows or baseline windows",
            "design_family": ",".join(intended) if intended else "general",
            "variables_needed": "time variable, event/treatment timing, outcome",
            "sample_needed": "units with sufficient observations under alternative windows",
            "priority": "medium",
            "notes": "Especially important for event-time platform studies",
        },
    ]
    save_csv(pd.DataFrame(robustness_rows), dirs, "robustness_seed_plan.csv")

    overall, critical = decide_overall(dirs)
    go_text = "# Pre-Model Go/No-Go Decision\n\n"
    go_text += f"Decision: {overall}\n\n"
    if critical:
        go_text += "## Blocking or high-severity issues\n\n"
        for issue in critical:
            go_text += f"- {issue}\n"
    else:
        go_text += "No critical hard-stop issue was detected by automated templates. Manual review of timing, identification assumptions, and controls is still required.\n"
    write_md(go_text, dirs, "pre_model_go_no_go.md")

    report = f"""# Empirical Design Audit Report

## Project

- Project title: {config.get('project', {}).get('title')}
- Empirical setting: {config.get('project', {}).get('empirical_setting')}
- Research question: {config.get('project', {}).get('research_question')}
- Intended claim strength: {config.get('project', {}).get('intended_claim_strength')}

## Overall decision

{overall}

## Automated audit outputs

The following audit tables were created in `output/audits/`:

- `audit_input_manifest.csv`
- `hypothesis_design_audit.csv`
- `unit_time_structure_audit.csv`
- `timing_and_leakage_audit.csv`
- `treatment_event_construction_audit.csv`
- `outcome_support_audit.csv`
- `control_bad_control_audit.csv`
- `sample_restriction_attrition_audit.csv`
- `fixed_effect_clustering_readiness_audit.csv`
- `identification_threat_register.csv`
- `estimator_readiness_matrix.csv`

## Manual review required

Automated checks cannot fully judge identification. Before model selection, manually review: theoretical control rationale, treatment timing, no-anticipation assumptions, spillovers/interference, platform algorithmic confounding, and sample restrictions.
"""
    write_md(report, dirs, "design_audit_report.md")

    threat_memo = f"""# Identification Threat Memo

## Intended empirical design

{config.get('design', {}).get('intended_design_family')}

## Core caution

The automated audit creates a threat register, but identification credibility requires a substantive argument. Review the threat register before model selection and decide which threats can be addressed through design, which require robustness checks, and which remain limitations.

## Highest-priority review areas

- Temporal ordering of key variables and controls.
- Treatment/event timing and anticipation.
- Platform-level shocks, algorithmic confounding, and interference.
- Sample restrictions and attrition.
- Fixed-effect absorption and clustering.
"""
    write_md(threat_memo, dirs, "identification_threat_memo.md")

    handoff = f"""# Model Selection Handoff Memo

## Dataset

- Path: {config.get('data', {}).get('analysis_dataset_path')}
- Format: {config.get('data', {}).get('analysis_dataset_format')}
- Unit of analysis: {config.get('design', {}).get('unit_of_analysis')}
- Row key: {config.get('design', {}).get('row_key')}
- Time variable: {config.get('design', {}).get('time_id')}
- Intended design family: {config.get('design', {}).get('intended_design_family')}

## Variables

- Outcomes: {config.get('variables', {}).get('outcomes')}
- Key independent variables: {config.get('variables', {}).get('key_independent_variables')}
- Treatments: {config.get('variables', {}).get('treatments')}
- Controls: {config.get('variables', {}).get('candidate_controls')}
- Fixed effects: {config.get('variables', {}).get('fixed_effects')}
- Clustering dimensions: {config.get('variables', {}).get('clustering_dimensions')}

## Required next step

Use `design_audit_report.md`, `identification_threat_register.csv`, and `estimator_readiness_matrix.csv` as inputs to the Stata model-selection skill. Do not proceed with final model implementation until all high-severity issues are resolved or explicitly accepted as limitations.
"""
    write_md(handoff, dirs, "model_selection_handoff_memo.md")


if __name__ == "__main__":
    main()
