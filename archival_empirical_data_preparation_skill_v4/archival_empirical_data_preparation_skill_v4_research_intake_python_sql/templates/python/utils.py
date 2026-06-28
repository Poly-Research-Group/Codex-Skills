"""Utility functions for archival empirical data preparation.

These functions are templates. Adapt table names, variable names, and source-specific
logic to the project.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import duckdb
import numpy as np
import pandas as pd
import yaml


DEFAULT_DATE_FORMAT = "%Y-%m-%d"


def load_config(config_path: str | Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dirs(cfg: Mapping) -> None:
    for key in ["raw", "interim", "clean", "analysis", "output", "audits", "tables", "figures", "logs", "docs"]:
        path = cfg.get("paths", {}).get(key)
        if path:
            Path(path).mkdir(parents=True, exist_ok=True)


def setup_logger(cfg: Mapping, name: str) -> logging.Logger:
    log_dir = Path(cfg["paths"]["logs"])
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh = logging.FileHandler(log_dir / f"{name}.log", encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def connect_db(cfg: Mapping) -> duckdb.DuckDBPyConnection:
    db_path = cfg["sql"].get("database_path", cfg["database"].get("path", "data/analysis/analysis_database.duckdb") if "database" in cfg else "data/analysis/analysis_database.duckdb")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(db_path)
    return con


def run_sql_file(con: duckdb.DuckDBPyConnection, path: str | Path) -> None:
    sql = Path(path).read_text(encoding="utf-8")
    if sql.strip():
        con.execute(sql)


def file_sha256(path: str | Path, block_size: int = 2**20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def clean_column_names(columns: Iterable[str]) -> list[str]:
    out = []
    for col in columns:
        c = str(col).strip().lower()
        c = c.replace(" ", "_").replace("-", "_").replace("/", "_")
        c = "".join(ch if ch.isalnum() or ch == "_" else "" for ch in c)
        while "__" in c:
            c = c.replace("__", "_")
        out.append(c.strip("_"))
    return out


def normalize_string_id(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )


def write_table(con: duckdb.DuckDBPyConnection, df: pd.DataFrame, table_name: str, schema: str = "raw", overwrite: bool = True) -> None:
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    tmp_name = "_tmp_df_to_write"
    con.register(tmp_name, df)
    mode = "CREATE OR REPLACE" if overwrite else "CREATE"
    con.execute(f"{mode} TABLE {schema}.{table_name} AS SELECT * FROM {tmp_name}")
    con.unregister(tmp_name)


def read_table(con: duckdb.DuckDBPyConnection, table: str) -> pd.DataFrame:
    return con.execute(f"SELECT * FROM {table}").df()


def assert_unique(df: pd.DataFrame, keys: Sequence[str], label: str = "dataset") -> None:
    dup = df.duplicated(list(keys), keep=False)
    if dup.any():
        examples = df.loc[dup, list(keys)].head(10).to_dict(orient="records")
        raise ValueError(f"Duplicate key rows detected in {label} for keys {keys}. Examples: {examples}")


def append_csv_row(path: str | Path, row: Mapping, columns: Sequence[str] | None = None) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([row])
    if columns:
        for col in columns:
            if col not in df.columns:
                df[col] = np.nan
        df = df[list(columns)]
    if path.exists():
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, index=False)


def table_profile(con: duckdb.DuckDBPyConnection, table: str) -> dict:
    n_rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    cols = con.execute(f"DESCRIBE {table}").df()
    return {
        "table": table,
        "n_rows": int(n_rows),
        "n_columns": int(len(cols)),
        "columns": ",".join(cols["column_name"].astype(str).tolist()),
    }


def log_table_profile(con: duckdb.DuckDBPyConnection, table: str, cfg: Mapping) -> None:
    profile = table_profile(con, table)
    append_csv_row(Path(cfg["paths"]["audits"]) / "table_profiles.csv", profile)


def format_number(value, decimals: int = 3, strip_trailing_zeros: bool = True, thousands: bool = True) -> str:
    if pd.isna(value):
        return ""
    try:
        v = float(value)
    except Exception:
        return str(value)
    fmt = f"{{:,.{decimals}f}}" if thousands else f"{{:.{decimals}f}}"
    s = fmt.format(v)
    if strip_trailing_zeros and "." in s:
        s = s.rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s


def compute_summary_stats(
    df: pd.DataFrame,
    plan: pd.DataFrame,
    include_column: str,
    cfg: Mapping,
) -> tuple[pd.DataFrame, bool]:
    selected = plan[plan[include_column].astype(str).str.lower().isin(["yes", "true", "1"])].copy()
    if selected.empty:
        return pd.DataFrame(), True
    selected["order"] = pd.to_numeric(selected.get("order", pd.Series(range(len(selected)))), errors="coerce")
    selected = selected.sort_values(["table_id", "order", "variable_name"])
    rows = []
    ns = []
    default_decimals = int(cfg.get("summary_tables", {}).get("default_decimals", 3))
    strip_zeros = bool(cfg.get("summary_tables", {}).get("strip_trailing_zeros", True))
    thousands = bool(cfg.get("summary_tables", {}).get("thousands_separator", True))
    for _, r in selected.iterrows():
        var = r["variable_name"]
        if var not in df.columns:
            rows.append({
                "Group": r.get("group_label", ""),
                "Variable": r.get("display_name", var),
                "Description": r.get("description", ""),
                "Mean": "VARIABLE_NOT_FOUND",
                "Standard deviation": "",
                "Minimum": "",
                "Maximum": "",
                "N": 0,
            })
            ns.append(0)
            continue
        s = pd.to_numeric(df[var], errors="coerce")
        n = int(s.notna().sum())
        ns.append(n)
        decimals = r.get("decimals", default_decimals)
        try:
            decimals = int(decimals)
        except Exception:
            decimals = default_decimals
        rows.append({
            "Group": r.get("group_label", ""),
            "Variable": r.get("display_name", var),
            "Description": r.get("description", ""),
            "Mean": format_number(s.mean(), decimals, strip_zeros, thousands),
            "Standard deviation": format_number(s.std(ddof=1), decimals, strip_zeros, thousands),
            "Minimum": format_number(s.min(), decimals, strip_zeros, thousands),
            "Maximum": format_number(s.max(), decimals, strip_zeros, thousands),
            "N": n,
        })
    result = pd.DataFrame(rows)
    common_n = len(set(ns)) == 1
    return result, common_n


def dataframe_to_latex_booktabs(df: pd.DataFrame, caption: str, label: str, include_group: bool = False, common_n: int | None = None) -> str:
    display = df.copy()
    cols = ["Variable", "Description", "Mean", "Standard deviation", "Minimum", "Maximum"]
    if include_group and "Group" in display.columns:
        cols = ["Group"] + cols
    if common_n is None and "N" in display.columns:
        display = display[cols + ["N"]]
    else:
        display = display[cols]
    latex = display.to_latex(index=False, escape=False, longtable=False, caption=caption, label=label)
    latex = latex.replace("\\toprule", "\\toprule")
    if common_n is not None:
        n_cols = len(display.columns)
        latex = latex.replace("\\bottomrule", f"\\midrule\n\\multicolumn{{{n_cols}}}{{l}}{{Number of observations: {common_n:,}}} \\\\\n\\bottomrule")
    return latex


def save_markdown_table(df: pd.DataFrame, path: str | Path, title: str, include_group: bool = False, common_n: int | None = None) -> None:
    cols = ["Variable", "Description", "Mean", "Standard deviation", "Minimum", "Maximum"]
    if include_group and "Group" in df.columns:
        cols = ["Group"] + cols
    out = [f"# {title}\n", df[cols].to_markdown(index=False)]
    if common_n is not None:
        out.append(f"\n\nNumber of observations: {common_n:,}\n")
    Path(path).write_text("\n".join(out), encoding="utf-8")
