"""Master pipeline for archival empirical data preparation.

Run from the project root:
    python code/python/00_master.py --config config/project_config.yaml
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from utils import ensure_dirs, load_config, setup_logger


STEPS = [
    "00_validate_research_intake.py",
    "01_ingest_raw.py",
    "02_clean_sources.py",
    "03_build_keys_time.py",
    "04_merge_build_analysis.py",
    "05_construct_variables.py",
    "06_define_samples.py",
    "07_data_diagnostics.py",
    "08_export_isr_summary_tables.py",
    "09_export_analysis_package.py",
]


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "00_master")
    code_dir = Path(__file__).resolve().parent
    logger.info("Starting archival empirical data-preparation pipeline.")
    for step in STEPS:
        logger.info("Running %s", step)
        cmd = [sys.executable, str(code_dir / step), "--config", config_path]
        completed = subprocess.run(cmd, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"Pipeline failed at {step} with exit code {completed.returncode}")
    logger.info("Pipeline completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
