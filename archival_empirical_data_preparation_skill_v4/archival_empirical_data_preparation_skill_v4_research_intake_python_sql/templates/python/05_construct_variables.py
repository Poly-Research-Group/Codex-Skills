"""Construct theory-aligned variables.

Use SQL for window functions and aggregations, and Python for transformations that are
harder to express in SQL. Update variable_construction_log.csv for every constructed variable.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from utils import append_csv_row, connect_db, ensure_dirs, load_config, read_table, setup_logger, write_table

VAR_LOG_COLUMNS = [
    "variable_name", "variable_label", "role", "formula_or_algorithm", "source_tables", "source_variables",
    "unit_level", "time_level", "timing_relative_to_treatment", "raw_variable_preserved", "transformation_type",
    "missingness_rule", "outlier_rule", "notes"
]


def safe_log1p(series: pd.Series) -> pd.Series:
    return np.log1p(pd.to_numeric(series, errors="coerce"))


def ihs(series: pd.Series) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")
    return np.log(x + np.sqrt(x * x + 1))


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "05_construct_variables")
    con = connect_db(cfg)

    source_table = cfg["research_design"].get("analysis_base_table", "analysis.analysis_base")
    output_table = cfg["research_design"].get("constructed_table", "analysis.analysis_constructed")
    var_log_path = Path(cfg["paths"]["audits"]) / "variable_construction_log.csv"

    try:
        df = read_table(con, source_table)
    except Exception as e:
        logger.warning("Could not read %s. Creating placeholder empty constructed table. Error: %s", source_table, e)
        df = pd.DataFrame()

    # Placeholder examples. Replace with project-specific variable construction.
    # Example: if a variable named viewers exists, create log_viewers.
    if "viewers" in df.columns and "log_viewers" not in df.columns:
        df["log_viewers"] = safe_log1p(df["viewers"])
        append_csv_row(var_log_path, {
            "variable_name": "log_viewers",
            "variable_label": "Log of one plus viewers",
            "role": "dependent_variable_or_control",
            "formula_or_algorithm": "log(1 + viewers)",
            "source_tables": source_table,
            "source_variables": "viewers",
            "unit_level": cfg["research_design"].get("unit_of_analysis", ""),
            "time_level": cfg["research_design"].get("time_grain", ""),
            "timing_relative_to_treatment": "same period unless otherwise revised",
            "raw_variable_preserved": "yes",
            "transformation_type": "log1p",
            "missingness_rule": "missing if viewers missing",
            "outlier_rule": "none",
            "notes": "Template example; revise for project.",
        }, VAR_LOG_COLUMNS)

    write_table(con, df, output_table.split(".")[-1], schema=output_table.split(".")[0], overwrite=True)
    logger.info("Wrote %s with %s rows", output_table, len(df))
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
