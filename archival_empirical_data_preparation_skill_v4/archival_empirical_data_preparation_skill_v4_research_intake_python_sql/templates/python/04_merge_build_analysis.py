"""Run merge/join SQL and record merge diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from utils import append_csv_row, connect_db, ensure_dirs, load_config, run_sql_file, setup_logger

MERGE_AUDIT_COLUMNS = [
    "merge_id", "left_table", "right_table", "join_type", "keys", "expected_cardinality",
    "left_rows_before", "right_rows_before", "left_duplicate_key_rows", "right_duplicate_key_rows",
    "rows_after", "matched_rows", "unmatched_left_rows", "unmatched_right_rows", "match_rate",
    "row_multiplication_detected", "decision", "notes"
]


def duplicate_count(con, table: str, keys: list[str]) -> int:
    key_expr = ", ".join(keys)
    q = f"""
    SELECT COUNT(*) FROM (
        SELECT {key_expr}, COUNT(*) AS n
        FROM {table}
        GROUP BY {key_expr}
        HAVING COUNT(*) > 1
    ) x
    """
    return int(con.execute(q).fetchone()[0])


def row_count(con, table: str) -> int:
    return int(con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "04_merge_build_analysis")
    con = connect_db(cfg)
    sql_dir = Path(__file__).resolve().parents[1] / "sql"
    audit_path = Path(cfg["paths"]["audits"]) / "merge_audit.csv"

    merge_plan_path = Path(cfg["paths"]["audits"]) / "merge_plan.csv"
    if merge_plan_path.exists():
        plan = pd.read_csv(merge_plan_path)
        for _, m in plan.iterrows():
            keys = [k.strip() for k in str(m.get("left_keys", "")).split(",") if k.strip()]
            left = str(m.get("left_table", "")).strip()
            right = str(m.get("right_table", "")).strip()
            if not left or not right or not keys:
                continue
            try:
                left_rows = row_count(con, left)
                right_rows = row_count(con, right)
                left_dups = duplicate_count(con, left, keys)
                right_dups = duplicate_count(con, right, keys)
                append_csv_row(audit_path, {
                    "merge_id": m.get("merge_id", ""),
                    "left_table": left,
                    "right_table": right,
                    "join_type": "planned",
                    "keys": ",".join(keys),
                    "expected_cardinality": m.get("expected_cardinality", ""),
                    "left_rows_before": left_rows,
                    "right_rows_before": right_rows,
                    "left_duplicate_key_rows": left_dups,
                    "right_duplicate_key_rows": right_dups,
                    "rows_after": "pending",
                    "matched_rows": "pending",
                    "unmatched_left_rows": "pending",
                    "unmatched_right_rows": "pending",
                    "match_rate": "pending",
                    "row_multiplication_detected": "pending",
                    "decision": "pre_merge_checked",
                    "notes": "Review duplicate counts before executing joins.",
                }, MERGE_AUDIT_COLUMNS)
                if str(m.get("expected_cardinality", "")).lower() in ["1:1", "1:m"] and left_dups > 0:
                    raise ValueError(f"Left duplicate keys violate expected cardinality for {m.get('merge_id')}")
                if str(m.get("expected_cardinality", "")).lower() in ["1:1", "m:1"] and right_dups > 0:
                    raise ValueError(f"Right duplicate keys violate expected cardinality for {m.get('merge_id')}")
            except Exception as e:
                logger.warning("Could not complete merge pre-audit for %s: %s", m.get("merge_id"), e)

    for script in ["02_merge_views.sql", "03_analysis_views.sql"]:
        path = sql_dir / script
        if path.exists():
            logger.info("Running %s", path)
            run_sql_file(con, path)

    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
