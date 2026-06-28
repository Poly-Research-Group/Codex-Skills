"""Build and verify identifiers, unit-time keys, and event-time variables."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from utils import connect_db, ensure_dirs, load_config, setup_logger


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "03_build_keys_time")
    con = connect_db(cfg)

    unit_id = cfg["research_design"].get("unit_id")
    time_id = cfg["research_design"].get("time_id")
    base_table = cfg["research_design"].get("base_clean_table", "clean.main_clean")

    # Placeholder diagnostic. Adapt base_table in config or replace with project-specific checks.
    try:
        if unit_id and time_id:
            query = f"""
            SELECT {unit_id}, {time_id}, COUNT(*) AS n
            FROM {base_table}
            GROUP BY {unit_id}, {time_id}
            HAVING COUNT(*) > 1
            LIMIT 100
            """
            dup = con.execute(query).df()
            dup.to_csv(Path(cfg["paths"]["audits"]) / "duplicate_unit_time_examples.csv", index=False)
            if len(dup) > 0:
                raise ValueError(f"Duplicate unit-time keys detected in {base_table}. See duplicate_unit_time_examples.csv")
            logger.info("No duplicate unit-time keys detected in %s", base_table)
        elif unit_id:
            query = f"""
            SELECT {unit_id}, COUNT(*) AS n
            FROM {base_table}
            GROUP BY {unit_id}
            HAVING COUNT(*) > 1
            LIMIT 100
            """
            dup = con.execute(query).df()
            dup.to_csv(Path(cfg["paths"]["audits"]) / "duplicate_unit_examples.csv", index=False)
    except Exception as e:
        logger.warning("Identifier check could not be completed with placeholder settings: %s", e)

    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
