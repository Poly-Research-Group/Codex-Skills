from __future__ import annotations
import re
import pandas as pd
from pathlib import Path
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, variable_list, read_optional_csv

RISK_PATTERNS = re.compile(r"(future|lead|post|after|next|subsequent|cumulative|through|rank|visibility|recommend|outcome|growth)", re.IGNORECASE)


def infer_timing_risk(var: str, role: str) -> tuple[str, str, str]:
    name_risk = bool(RISK_PATTERNS.search(var or ""))
    if role in {"candidate_control", "control"} and name_risk:
        return "yes", "medium", "Control name suggests possible post-treatment, future, algorithmic, or outcome-overlap risk; verify metadata."
    return "no", "none", ""


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "03_timing_and_leakage_audit")
    df = load_analysis_data(config)

    rows = []
    role_map = []
    for role_key, role_name in [
        ("outcomes", "outcome"),
        ("key_independent_variables", "key_independent_variable"),
        ("treatments", "treatment"),
        ("moderators", "moderator"),
        ("mediators", "mediator"),
        ("mechanisms", "mechanism"),
        ("candidate_controls", "candidate_control"),
    ]:
        for var in variable_list(config, role_key):
            role_map.append((var, role_name))

    timing_path = Path(config.get("metadata_files", {}).get("identification_timing_plan", ""))
    timing_meta = read_optional_csv(timing_path) if str(timing_path) else pd.DataFrame()

    for var, role in role_map:
        in_data = var in df.columns
        relative_timing = "unknown"
        source = ""
        measurement_window = "unknown"
        if not timing_meta.empty:
            match_cols = [c for c in timing_meta.columns if c.lower() in {"variable", "variable_name", "empirical_variable"}]
            if match_cols:
                m = timing_meta[timing_meta[match_cols[0]].astype(str) == var]
                if not m.empty:
                    for candidate in ["relative_timing", "timing", "measurement_timing"]:
                        if candidate in m.columns:
                            relative_timing = str(m.iloc[0][candidate])
                    for candidate in ["measurement_window", "window"]:
                        if candidate in m.columns:
                            measurement_window = str(m.iloc[0][candidate])
                    for candidate in ["source_table", "source", "source_file"]:
                        if candidate in m.columns:
                            source = str(m.iloc[0][candidate])
        future_risk, severity, note = infer_timing_risk(var, role)
        post_treatment_risk = "yes" if role == "candidate_control" and str(relative_timing).lower() in {"post", "post_treatment", "after_treatment"} else "no"
        if post_treatment_risk == "yes":
            severity = "high"
            note = "Candidate control is marked as post-treatment; do not include in main model unless explicitly justified."
        status = "not_ready" if severity == "high" else ("conditionally_ready" if severity == "medium" else "ready")
        rows.append({
            "variable": var,
            "role": role,
            "measurement_window": measurement_window,
            "relative_timing": relative_timing,
            "source_table": source,
            "uses_lag": "unknown",
            "uses_lead": "unknown",
            "rolling_window": "unknown",
            "future_information_risk": future_risk,
            "post_treatment_risk": post_treatment_risk,
            "mechanical_outcome_overlap_risk": "unknown",
            "status": "missing_from_data" if not in_data else status,
            "recommended_action": "Verify variable existence" if not in_data else ("Review timing before model selection" if severity != "none" else "No immediate issue"),
            "notes": note,
        })
    save_csv(pd.DataFrame(rows), dirs, "timing_and_leakage_audit.csv")


if __name__ == "__main__":
    main()
