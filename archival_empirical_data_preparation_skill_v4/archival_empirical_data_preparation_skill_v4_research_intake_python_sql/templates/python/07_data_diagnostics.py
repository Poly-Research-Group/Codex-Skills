"""Generate missingness, outlier, panel, and correlation diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from utils import connect_db, ensure_dirs, load_config, read_table, setup_logger


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes(include=[np.number])
    rows = []
    for col in num.columns:
        s = num[col]
        rows.append({
            "variable_name": col,
            "n": int(s.notna().sum()),
            "mean": s.mean(),
            "sd": s.std(ddof=1),
            "min": s.min(),
            "p1": s.quantile(0.01),
            "p5": s.quantile(0.05),
            "p25": s.quantile(0.25),
            "p50": s.quantile(0.50),
            "p75": s.quantile(0.75),
            "p95": s.quantile(0.95),
            "p99": s.quantile(0.99),
            "max": s.max(),
        })
    return pd.DataFrame(rows)


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "07_data_diagnostics")
    con = connect_db(cfg)
    final_table = cfg["research_design"].get("final_analysis_table", "analysis.analysis_ready")
    unit_id = cfg["research_design"].get("unit_id")
    time_id = cfg["research_design"].get("time_id")
    audits = Path(cfg["paths"]["audits"])
    tables = Path(cfg["paths"]["tables"])

    try:
        df = read_table(con, final_table)
    except Exception as e:
        logger.warning("Could not read %s for diagnostics: %s", final_table, e)
        df = pd.DataFrame()

    if df.empty:
        pd.DataFrame().to_csv(audits / "missingness_audit.csv", index=False)
        pd.DataFrame().to_csv(audits / "outlier_audit.csv", index=False)
        pd.DataFrame().to_csv(audits / "panel_audit.csv", index=False)
        return

    missing = pd.DataFrame({
        "variable_name": df.columns,
        "total_observations": len(df),
        "missing_observations": df.isna().sum().values,
    })
    missing["missing_rate"] = missing["missing_observations"] / missing["total_observations"]
    missing.to_csv(audits / "missingness_audit.csv", index=False)

    summary = numeric_summary(df)
    summary.to_csv(tables / "descriptive_statistics_full.csv", index=False)
    summary.to_csv(audits / "outlier_audit.csv", index=False)

    if unit_id in df.columns and time_id in df.columns:
        obs_per_unit = df.groupby(unit_id)[time_id].nunique()
        duplicate_rows = int(df.duplicated([unit_id, time_id]).sum())
        panel = pd.DataFrame([{
            "unit_id_variable": unit_id,
            "time_id_variable": time_id,
            "n_observations": len(df),
            "n_units": int(df[unit_id].nunique(dropna=True)),
            "n_time_periods": int(df[time_id].nunique(dropna=True)),
            "min_obs_per_unit": int(obs_per_unit.min()),
            "p25_obs_per_unit": float(obs_per_unit.quantile(0.25)),
            "median_obs_per_unit": float(obs_per_unit.median()),
            "p75_obs_per_unit": float(obs_per_unit.quantile(0.75)),
            "max_obs_per_unit": int(obs_per_unit.max()),
            "is_balanced": bool(obs_per_unit.nunique() == 1),
            "n_duplicate_unit_time_rows": duplicate_rows,
            "n_time_gaps": "requires project-specific calendar audit",
            "entry_exit_detected": bool(obs_per_unit.nunique() > 1),
            "notes": "Review panel gaps with project-specific time calendar.",
        }])
        panel.to_csv(audits / "panel_audit.csv", index=False)
        if duplicate_rows > 0:
            raise ValueError("Final analysis dataset contains duplicate unit-time rows.")

    num = df.select_dtypes(include=[np.number])
    if num.shape[1] > 1:
        num.corr().to_csv(tables / "correlation_matrix.csv")

    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
