from __future__ import annotations
import pandas as pd
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, variable_list


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "04_treatment_event_construction_audit")
    df = load_analysis_data(config)
    design = config.get("design", {})
    variables = config.get("variables", {})

    treatments = variable_list(config, "treatments") or variable_list(config, "key_independent_variables")
    treatment_time = variables.get("treatment_time") or design.get("event_time_id")
    time_id = design.get("time_id")
    unit_id = design.get("unit_id")

    rows = []
    for treat in treatments:
        if treat not in df.columns:
            rows.append({
                "treatment_or_event_variable": treat,
                "treatment_type": "unknown",
                "event_time_variable": treatment_time,
                "n_treated_units": None,
                "n_control_units": None,
                "n_never_treated_units": None,
                "n_always_treated_units": None,
                "n_pre_observations": None,
                "n_post_observations": None,
                "n_cohorts": None,
                "repeated_events": "unknown",
                "anticipation_window_defined": "unknown",
                "comparison_group_status": "unknown",
                "severity": "critical",
                "status": "not_ready",
                "notes": "Treatment/key variable not found in dataset",
            })
            continue
        s = df[treat]
        nonmiss = s.dropna()
        unique_vals = nonmiss.unique()
        binary_like = set(unique_vals).issubset({0, 1, True, False}) if len(unique_vals) <= 2 else False
        n_treated_obs = int((s == 1).sum()) if binary_like else int(nonmiss.shape[0])
        n_control_obs = int((s == 0).sum()) if binary_like else None
        n_treated_units = None
        n_control_units = None
        n_never = None
        n_always = None
        if binary_like and unit_id in df.columns:
            g = df.groupby(unit_id)[treat]
            ever = g.max()
            always = g.min()
            n_treated_units = int((ever == 1).sum())
            n_control_units = int((ever == 0).sum())
            n_never = n_control_units
            n_always = int((always == 1).sum())
        n_pre = None
        n_post = None
        n_cohorts = None
        if treatment_time and treatment_time in df.columns:
            n_cohorts = int(df[treatment_time].nunique(dropna=True))
        elif binary_like:
            n_pre = int((s == 0).sum())
            n_post = int((s == 1).sum())
        comparison_status = "present" if (binary_like and (n_treated_obs > 0 and (n_control_obs or 0) > 0)) else "needs_review"
        severity = "none" if comparison_status == "present" else "medium"
        rows.append({
            "treatment_or_event_variable": treat,
            "treatment_type": "binary" if binary_like else "continuous_or_nonbinary_key_variable",
            "event_time_variable": treatment_time,
            "n_treated_units": n_treated_units,
            "n_control_units": n_control_units,
            "n_never_treated_units": n_never,
            "n_always_treated_units": n_always,
            "n_pre_observations": n_pre,
            "n_post_observations": n_post,
            "n_cohorts": n_cohorts,
            "repeated_events": "requires_manual_check",
            "anticipation_window_defined": "requires_manual_check",
            "comparison_group_status": comparison_status,
            "severity": severity,
            "status": "ready" if severity == "none" else "conditionally_ready",
            "notes": "Binary treatment has treated and control observations" if severity == "none" else "Check treatment variation, comparison group, event timing, and anticipation logic",
        })
    save_csv(pd.DataFrame(rows), dirs, "treatment_event_construction_audit.csv")


if __name__ == "__main__":
    main()
