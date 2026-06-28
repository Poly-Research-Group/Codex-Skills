"""Export final analysis package, including Stata-ready .dta."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from utils import assert_unique, connect_db, ensure_dirs, load_config, read_table, setup_logger


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "09_export_analysis_package")
    con = connect_db(cfg)

    final_table = cfg["research_design"].get("final_analysis_table", "analysis.analysis_ready")
    unit_id = cfg["research_design"].get("unit_id")
    time_id = cfg["research_design"].get("time_id")
    analysis_dir = Path(cfg["paths"]["analysis"])
    docs_dir = Path(cfg["paths"]["docs"])
    analysis_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    df = read_table(con, final_table)
    if unit_id in df.columns and time_id in df.columns:
        assert_unique(df, [unit_id, time_id], label="analysis_ready")
    elif unit_id in df.columns and cfg["research_design"].get("data_structure") == "cross_section":
        assert_unique(df, [unit_id], label="analysis_ready")

    parquet_path = analysis_dir / "analysis_ready.parquet"
    csv_path = analysis_dir / "analysis_ready.csv"
    dta_path = analysis_dir / "analysis_ready.dta"

    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False)
    # Stata version 118 supports modern Stata .dta files. Adjust if needed.
    df.to_stata(dta_path, write_index=False, version=118)

    variable_labels = pd.DataFrame({
        "variable_name": df.columns,
        "variable_label": df.columns,
        "stata_type_note": [str(df[c].dtype) for c in df.columns],
    })
    variable_labels.to_csv(analysis_dir / "variable_labels.csv", index=False)

    handoff = f"""# Stata Handoff Notes

- Analysis dataset: `{dta_path}`
- Unit of analysis: {cfg['research_design'].get('unit_of_analysis')}
- Unit ID: {unit_id}
- Time ID: {time_id}
- Number of observations: {len(df):,}
- Number of variables: {len(df.columns):,}

## Suggested Stata setup

```stata
use "{dta_path}", clear
```

If panel data:

```stata
xtset {unit_id or 'unit_id'} {time_id or 'time_id'}
```

## Notes

This dataset was prepared using Python and SQL. Econometric model selection and estimation should be conducted in the later Stata model-selection and model-implementation skills.
"""
    (docs_dir / "stata_handoff_notes.md").write_text(handoff, encoding="utf-8")
    logger.info("Exported analysis package to %s", analysis_dir)
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
