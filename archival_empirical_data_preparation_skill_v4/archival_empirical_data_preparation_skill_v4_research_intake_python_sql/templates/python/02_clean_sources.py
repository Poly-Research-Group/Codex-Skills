"""Clean source-specific tables and create clean schema tables/views.

Replace the placeholder SQL calls with project-specific cleaning logic.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import connect_db, ensure_dirs, load_config, run_sql_file, setup_logger


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "02_clean_sources")
    con = connect_db(cfg)
    sql_dir = Path(__file__).resolve().parents[1] / "sql"
    for script in ["00_schema.sql", "01_staging_views.sql"]:
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
