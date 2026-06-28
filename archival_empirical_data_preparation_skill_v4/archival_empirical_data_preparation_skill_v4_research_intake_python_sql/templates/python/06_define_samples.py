"""Define final analysis sample and record sample flow."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from utils import append_csv_row, connect_db, ensure_dirs, load_config, read_table, setup_logger, write_table

SAMPLE_FLOW_COLUMNS = [
    "step_id", "step_name", "script_or_query", "condition_applied", "observations_before", "observations_after",
    "observations_dropped", "units_before", "units_after", "units_dropped", "time_periods_before", "time_periods_after",
    "rationale", "notes"
]


def count_unique(df: pd.DataFrame, col: str | None) -> int | str:
    if col and col in df.columns:
        return int(df[col].nunique(dropna=True))
    return ""


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "06_define_samples")
    con = connect_db(cfg)

    source_table = cfg["research_design"].get("constructed_table", "analysis.analysis_constructed")
    final_table = cfg["research_design"].get("final_analysis_table", "analysis.analysis_ready")
    unit_id = cfg["research_design"].get("unit_id")
    time_id = cfg["research_design"].get("time_id")
    sample_flow_path = Path(cfg["paths"]["audits"]) / "sample_flow.csv"

    try:
        df = read_table(con, source_table)
    except Exception as e:
        logger.warning("Could not read %s. Creating placeholder final sample. Error: %s", source_table, e)
        df = pd.DataFrame()

    before = len(df)
    before_units = count_unique(df, unit_id)
    before_times = count_unique(df, time_id)

    # Apply project-specific conditions from config. Conditions use pandas query syntax.
    conditions = cfg.get("sample", {}).get("eligibility_conditions", []) or []
    for i, condition in enumerate(conditions, start=1):
        obs_before = len(df)
        units_before = count_unique(df, unit_id)
        times_before = count_unique(df, time_id)
        df = df.query(condition).copy()
        append_csv_row(sample_flow_path, {
            "step_id": f"SAMPLE_{i}",
            "step_name": "Eligibility condition",
            "script_or_query": "06_define_samples.py",
            "condition_applied": condition,
            "observations_before": obs_before,
            "observations_after": len(df),
            "observations_dropped": obs_before - len(df),
            "units_before": units_before,
            "units_after": count_unique(df, unit_id),
            "units_dropped": (units_before - count_unique(df, unit_id)) if isinstance(units_before, int) else "",
            "time_periods_before": times_before,
            "time_periods_after": count_unique(df, time_id),
            "rationale": "Configured eligibility condition",
            "notes": "",
        }, SAMPLE_FLOW_COLUMNS)

    append_csv_row(sample_flow_path, {
        "step_id": "FINAL",
        "step_name": "Final analysis sample",
        "script_or_query": "06_define_samples.py",
        "condition_applied": "all configured sample conditions",
        "observations_before": before,
        "observations_after": len(df),
        "observations_dropped": before - len(df),
        "units_before": before_units,
        "units_after": count_unique(df, unit_id),
        "units_dropped": (before_units - count_unique(df, unit_id)) if isinstance(before_units, int) else "",
        "time_periods_before": before_times,
        "time_periods_after": count_unique(df, time_id),
        "rationale": "Final sample for model selection and descriptive statistics",
        "notes": "",
    }, SAMPLE_FLOW_COLUMNS)

    write_table(con, df, final_table.split(".")[-1], schema=final_table.split(".")[0], overwrite=True)
    logger.info("Wrote %s with %s rows", final_table, len(df))
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
