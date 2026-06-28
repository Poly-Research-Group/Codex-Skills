from __future__ import annotations
import pandas as pd
from pathlib import Path
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, variable_list, read_optional_csv


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "05_control_and_bad_control_audit")
    df = load_analysis_data(config)

    controls = variable_list(config, "candidate_controls")
    fe_vars = set(variable_list(config, "fixed_effects"))
    timing_path = Path(config.get("metadata_files", {}).get("control_variable_audit", ""))
    meta = read_optional_csv(timing_path) if str(timing_path) else pd.DataFrame()

    rows = []
    for c in controls:
        measurement_timing = "unknown"
        rationale = "unknown"
        if not meta.empty:
            var_col = next((x for x in meta.columns if x.lower() in {"variable", "control_variable", "variable_name"}), None)
            if var_col:
                m = meta[meta[var_col].astype(str) == c]
                if not m.empty:
                    for col in ["timing", "measurement_timing", "relative_timing"]:
                        if col in m.columns:
                            measurement_timing = str(m.iloc[0][col])
                    for col in ["rationale", "theoretical_rationale"]:
                        if col in m.columns:
                            rationale = str(m.iloc[0][col])
        post_risk = str(measurement_timing).lower() in {"post", "post_treatment", "after_treatment", "after"}
        fe_absorb = c in fe_vars
        missing = c not in df.columns
        if missing:
            recommendation = "requires_user_decision"
            severity = "high"
            notes = "Control not found in dataset"
        elif post_risk:
            recommendation = "exclude_from_main_model_or_use_as_mechanism"
            severity = "high"
            notes = "Post-treatment controls can block mechanisms or introduce bias"
        elif fe_absorb:
            recommendation = "do_not_include_separately_if_absorbed_by_fixed_effects"
            severity = "medium"
            notes = "Control appears to be a fixed-effect dimension or absorbed by fixed effects"
        else:
            recommendation = "include_if_theoretical_rationale_is_confirmed"
            severity = "low" if rationale == "unknown" else "none"
            notes = "Rationale should be documented" if rationale == "unknown" else "No immediate bad-control issue detected"
        rows.append({
            "control_variable": c,
            "construct": "",
            "proposed_role": "candidate_control",
            "recommended_role": "pre_treatment_control" if not post_risk else "post_treatment_or_mechanism",
            "measurement_timing": measurement_timing,
            "theoretical_rationale": rationale,
            "pre_treatment_confounder": "unknown" if measurement_timing == "unknown" else ("yes" if not post_risk else "no"),
            "precision_control": "unknown",
            "mediator_or_mechanism": "possible" if post_risk else "unknown",
            "post_treatment_risk": "yes" if post_risk else "no",
            "collider_risk": "unknown",
            "mechanical_overlap_risk": "unknown",
            "fe_absorption_risk": "yes" if fe_absorb else "no",
            "main_model_recommendation": recommendation,
            "severity": severity,
            "notes": notes,
        })
    save_csv(pd.DataFrame(rows), dirs, "control_bad_control_audit.csv")


if __name__ == "__main__":
    main()
