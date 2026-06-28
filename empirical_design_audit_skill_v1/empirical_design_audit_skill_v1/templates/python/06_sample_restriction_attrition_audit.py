from __future__ import annotations
import pandas as pd
from pathlib import Path
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, variable_list, read_optional_csv


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "06_sample_restriction_attrition_audit")
    df = load_analysis_data(config)

    rows = []
    n = len(df)
    unit_id = config.get("design", {}).get("unit_id")
    n_units = df[unit_id].nunique(dropna=True) if unit_id in df.columns else None

    sample_path = Path(config.get("metadata_files", {}).get("sample_flow", ""))
    sample_flow = read_optional_csv(sample_path) if str(sample_path) else pd.DataFrame()
    if not sample_flow.empty:
        rows.append({
            "step_id": "sample_flow_file",
            "restriction_or_issue": "Existing sample_flow.csv found; review for full attrition sequence",
            "n_observations_before": None,
            "n_observations_after": n,
            "n_units_before": None,
            "n_units_after": n_units,
            "observations_lost": None,
            "units_lost": None,
            "loss_rate": None,
            "loss_by_treatment_flag": "requires_review",
            "restriction_defined_pre_outcome": "requires_review",
            "severity": "low",
            "status": "conditionally_ready",
            "notes": f"Source: {sample_path}",
        })
    else:
        rows.append({
            "step_id": "sample_flow_missing",
            "restriction_or_issue": "No sample_flow.csv found",
            "n_observations_before": None,
            "n_observations_after": n,
            "n_units_before": None,
            "n_units_after": n_units,
            "observations_lost": None,
            "units_lost": None,
            "loss_rate": None,
            "loss_by_treatment_flag": "unknown",
            "restriction_defined_pre_outcome": "unknown",
            "severity": "medium",
            "status": "conditionally_ready",
            "notes": "Sample restrictions should be reconstructed before model selection",
        })

    key_vars = variable_list(config, "outcomes") + variable_list(config, "key_independent_variables") + variable_list(config, "treatments")
    threshold_warn = config.get("thresholds", {}).get("key_variable_missing_rate_warn", 0.10)
    threshold_stop = config.get("thresholds", {}).get("key_variable_missing_rate_stop", 0.30)
    for var in key_vars:
        if var not in df.columns:
            continue
        miss_rate = float(df[var].isna().mean())
        if miss_rate >= threshold_stop:
            severity = "high"
            status = "not_ready"
        elif miss_rate >= threshold_warn:
            severity = "medium"
            status = "conditionally_ready"
        else:
            severity = "none"
            status = "ready"
        rows.append({
            "step_id": f"missingness_{var}",
            "restriction_or_issue": f"Missingness in key variable {var}",
            "n_observations_before": n,
            "n_observations_after": int(df[var].notna().sum()),
            "n_units_before": n_units,
            "n_units_after": None,
            "observations_lost": int(df[var].isna().sum()),
            "units_lost": None,
            "loss_rate": miss_rate,
            "loss_by_treatment_flag": "requires_review",
            "restriction_defined_pre_outcome": "not_applicable",
            "severity": severity,
            "status": status,
            "notes": "Explain structural missingness, source failure, true zero, or attrition" if severity != "none" else "No major missingness issue",
        })
    save_csv(pd.DataFrame(rows), dirs, "sample_restriction_attrition_audit.csv")


if __name__ == "__main__":
    main()
