from __future__ import annotations
from pathlib import Path
import pandas as pd

from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, all_design_variables, missing_columns


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "01_load_inputs_validate_metadata")

    df = load_analysis_data(config)
    required_vars = all_design_variables(config)
    miss = missing_columns(df, required_vars)

    metadata_files = config.get("metadata_files", {})
    rows = []
    rows.append({
        "artifact_type": "analysis_dataset",
        "path": config.get("data", {}).get("analysis_dataset_path"),
        "exists": Path(config.get("data", {}).get("analysis_dataset_path", "")).exists(),
        "required": True,
        "description": "Analysis-ready dataset",
        "notes": f"Rows={len(df)}, columns={len(df.columns)}",
    })
    for name, path in metadata_files.items():
        p = Path(path)
        rows.append({
            "artifact_type": name,
            "path": str(p),
            "exists": p.exists(),
            "required": name in {"research_design_intake", "hypothesis_register", "hypothesis_variable_map", "identification_timing_plan", "control_variable_audit"},
            "description": name.replace("_", " "),
            "notes": "",
        })

    save_csv(pd.DataFrame(rows), dirs, "audit_input_manifest.csv")

    go_rows = []
    if miss:
        go_rows.append({
            "decision_area": "variable_existence",
            "status": "not_ready",
            "severity": "high",
            "blocking_issue": "Configured variables are missing from the dataset",
            "evidence": "; ".join(miss),
            "required_user_decision": "Confirm variable names or revise data preparation",
            "recommended_next_step": "Update audit_config.yaml or rebuild analysis data",
        })
    else:
        go_rows.append({
            "decision_area": "variable_existence",
            "status": "ready",
            "severity": "none",
            "blocking_issue": "",
            "evidence": "All configured variables found",
            "required_user_decision": "",
            "recommended_next_step": "Proceed with design audits",
        })
    save_csv(pd.DataFrame(go_rows), dirs, "pre_model_go_no_go.csv")


if __name__ == "__main__":
    main()
