"""Utility functions for empirical design audits.

These templates are intentionally conservative. They diagnose design-readiness; they do not
estimate hypothesis-testing models.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import json
import logging
import sys

import pandas as pd

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


def setup_logging(output_root: Path, script_name: str) -> None:
    log_dir = output_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_dir / f"{script_name}.log", mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def read_config(path: str | Path = "config/audit_config.yaml") -> Dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Missing audit config: {path}")
    if yaml is None:
        raise ImportError("pyyaml is required to read audit_config.yaml")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def output_root(config: Dict[str, Any]) -> Path:
    return Path(config.get("data", {}).get("output_root", "design_audit_package"))


def ensure_output_dirs(config: Dict[str, Any]) -> Dict[str, Path]:
    root = output_root(config)
    dirs = {
        "root": root,
        "audits": root / "output" / "audits",
        "figures": root / "output" / "figures",
        "docs": root / "docs",
        "logs": root / "logs",
    }
    for p in dirs.values():
        p.mkdir(parents=True, exist_ok=True)
    return dirs


def load_analysis_data(config: Dict[str, Any]) -> pd.DataFrame:
    data_cfg = config.get("data", {})
    path = Path(data_cfg.get("analysis_dataset_path", ""))
    fmt = (data_cfg.get("analysis_dataset_format") or path.suffix.replace(".", "")).lower()
    if not path.exists():
        raise FileNotFoundError(f"Analysis dataset not found: {path}")
    if fmt in {"parquet", "pq"}:
        return pd.read_parquet(path)
    if fmt in {"csv", "txt"}:
        return pd.read_csv(path)
    if fmt in {"dta", "stata"}:
        return pd.read_stata(path)
    raise ValueError(f"Unsupported analysis dataset format: {fmt}")


def read_optional_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def save_csv(df: pd.DataFrame, dirs: Dict[str, Path], name: str) -> Path:
    path = dirs["audits"] / name
    df.to_csv(path, index=False)
    logging.info("Saved %s", path)
    return path


def write_md(text: str, dirs: Dict[str, Path], name: str) -> Path:
    path = dirs["docs"] / name
    path.write_text(text, encoding="utf-8")
    logging.info("Saved %s", path)
    return path


def get_row_key(config: Dict[str, Any]) -> List[str]:
    row_key = config.get("design", {}).get("row_key", [])
    if isinstance(row_key, str):
        return [row_key]
    return list(row_key or [])


def columns_exist(df: pd.DataFrame, cols: Iterable[str]) -> Dict[str, bool]:
    return {c: c in df.columns for c in cols if c}


def missing_columns(df: pd.DataFrame, cols: Iterable[str]) -> List[str]:
    return [c for c in cols if c and c not in df.columns]


def severity_from_bool(flag: bool, if_true: str = "high", if_false: str = "none") -> str:
    return if_true if flag else if_false


def status_from_severity(severity: str) -> str:
    if severity in {"critical", "high"}:
        return "not_ready"
    if severity in {"medium", "low"}:
        return "conditionally_ready"
    return "ready"


def summarize_group_sizes(df: pd.DataFrame, col: str) -> Dict[str, Any]:
    if col not in df.columns:
        return {"n": 0, "min": None, "median": None, "max": None, "singleton_count": None, "singleton_share": None}
    sizes = df.groupby(col, dropna=False).size()
    if sizes.empty:
        return {"n": 0, "min": None, "median": None, "max": None, "singleton_count": None, "singleton_share": None}
    singleton_count = int((sizes == 1).sum())
    return {
        "n": int(sizes.shape[0]),
        "min": int(sizes.min()),
        "median": float(sizes.median()),
        "max": int(sizes.max()),
        "singleton_count": singleton_count,
        "singleton_share": float(singleton_count / sizes.shape[0]),
    }


def variable_list(config: Dict[str, Any], key: str) -> List[str]:
    vals = config.get("variables", {}).get(key, [])
    if vals is None:
        return []
    if isinstance(vals, str):
        return [vals]
    return list(vals)


def all_design_variables(config: Dict[str, Any]) -> List[str]:
    v = []
    for key in ["outcomes", "key_independent_variables", "treatments", "moderators", "mediators", "mechanisms", "candidate_controls", "fixed_effects", "clustering_dimensions", "sample_indicators"]:
        v.extend(variable_list(config, key))
    extra = [config.get("design", {}).get("unit_id"), config.get("design", {}).get("time_id"), config.get("variables", {}).get("treatment_time"), config.get("variables", {}).get("event_time")]
    v.extend([x for x in extra if x])
    return sorted(set([x for x in v if x]))
