from __future__ import annotations
import pandas as pd
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, get_row_key, summarize_group_sizes


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "02_unit_time_structure_audit")
    df = load_analysis_data(config)

    design = config.get("design", {})
    row_key = get_row_key(config)
    missing_key_cols = [c for c in row_key if c not in df.columns]
    n = len(df)
    if missing_key_cols:
        rows = [{
            "check_id": "row_key_exists",
            "check_area": "unit_of_analysis",
            "declared_unit": design.get("unit_of_analysis"),
            "row_key": ",".join(row_key),
            "n_observations": n,
            "n_unique_rows": None,
            "n_duplicate_rows": None,
            "duplicate_rate": None,
            "n_units": None,
            "n_time_periods": None,
            "panel_balance_status": "unknown",
            "gap_status": "unknown",
            "severity": "critical",
            "status": "not_ready",
            "notes": f"Missing row-key columns: {missing_key_cols}",
        }]
        save_csv(pd.DataFrame(rows), dirs, "unit_time_structure_audit.csv")
        return

    dup_mask = df.duplicated(row_key, keep=False)
    n_dup_rows = int(dup_mask.sum())
    n_unique_rows = int(df[row_key].drop_duplicates().shape[0])
    dup_rate = n_dup_rows / n if n else 0
    unit_id = design.get("unit_id")
    time_id = design.get("time_id")
    n_units = df[unit_id].nunique(dropna=True) if unit_id in df.columns else None
    n_times = df[time_id].nunique(dropna=True) if time_id in df.columns else None

    panel_balance_status = "not_applicable"
    gap_status = "not_checked"
    if unit_id in df.columns and time_id in df.columns:
        counts = df.groupby(unit_id, dropna=False)[time_id].nunique(dropna=True)
        panel_balance_status = "balanced" if counts.nunique() == 1 else "unbalanced"
        gap_status = "requires_manual_check_for_irregular_time"  # generic; exact gap check depends on time grain

    severity = "critical" if n_dup_rows > 0 else "none"
    status = "not_ready" if n_dup_rows > 0 else "ready"
    rows = [{
        "check_id": "row_key_uniqueness",
        "check_area": "unit_of_analysis",
        "declared_unit": design.get("unit_of_analysis"),
        "row_key": ",".join(row_key),
        "n_observations": n,
        "n_unique_rows": n_unique_rows,
        "n_duplicate_rows": n_dup_rows,
        "duplicate_rate": dup_rate,
        "n_units": n_units,
        "n_time_periods": n_times,
        "panel_balance_status": panel_balance_status,
        "gap_status": gap_status,
        "severity": severity,
        "status": status,
        "notes": "Duplicate row keys must be resolved before model selection" if n_dup_rows > 0 else "Row key is unique",
    }]
    save_csv(pd.DataFrame(rows), dirs, "unit_time_structure_audit.csv")


if __name__ == "__main__":
    main()
