"""Ingest raw files into SQL staging tables.

Adapt the source list to the project. This script should never modify files in data/raw/.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from utils import clean_column_names, connect_db, ensure_dirs, file_sha256, load_config, log_table_profile, setup_logger, write_table


def read_source(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in [".csv", ".txt"]:
        return pd.read_csv(path)
    if suffix in [".tsv"]:
        return pd.read_csv(path, sep="\t")
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    if suffix in [".parquet"]:
        return pd.read_parquet(path)
    if suffix in [".json"]:
        return pd.read_json(path)
    raise ValueError(f"Unsupported file type: {path}")


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "01_ingest_raw")
    con = connect_db(cfg)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    raw_dir = Path(cfg["paths"]["raw"])
    inventory_path = Path(cfg["paths"]["audits"]) / "source_inventory.csv"

    if not inventory_path.exists():
        logger.warning("source_inventory.csv not found. Creating a source inventory stub from raw folder files.")
        rows = []
        for i, path in enumerate(sorted(raw_dir.glob("*")), start=1):
            if path.is_file():
                rows.append({
                    "source_id": f"S{i}",
                    "raw_file_name": path.name,
                    "source_type": path.suffix.lower().lstrip("."),
                    "source_owner_or_url": "",
                    "acquisition_date": "",
                    "coverage_start": "",
                    "coverage_end": "",
                    "unit_in_raw_file": "",
                    "time_grain_in_raw_file": "",
                    "license_or_access_notes": "",
                    "import_script": "01_ingest_raw.py",
                    "known_limitations": "",
                })
        pd.DataFrame(rows).to_csv(inventory_path, index=False)

    inventory = pd.read_csv(inventory_path)
    import_log_rows = []
    for _, row in inventory.iterrows():
        raw_file = str(row.get("raw_file_name", "")).strip()
        if not raw_file:
            continue
        path = raw_dir / raw_file
        if not path.exists():
            logger.warning("Raw file not found: %s", path)
            continue
        df = read_source(path)
        df.columns = clean_column_names(df.columns)
        table_name = Path(raw_file).stem.lower().replace("-", "_").replace(" ", "_")
        write_table(con, df, table_name, schema="raw", overwrite=True)
        log_table_profile(con, f"raw.{table_name}", cfg)
        import_log_rows.append({
            "source_id": row.get("source_id", ""),
            "raw_file_name": raw_file,
            "table_name": f"raw.{table_name}",
            "sha256": file_sha256(path),
            "n_rows": len(df),
            "n_columns": len(df.columns),
            "columns": ",".join(df.columns.astype(str)),
        })
        logger.info("Imported %s as raw.%s with %s rows", raw_file, table_name, len(df))

    pd.DataFrame(import_log_rows).to_csv(Path(cfg["paths"]["audits"]) / "import_log.csv", index=False)
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
