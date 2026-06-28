"""Export ISR-style summary statistics tables.

Inputs:
- output/audits/summary_statistics_plan.csv
- analysis final table from SQL database

Outputs:
- output/tables/summary_statistics_isr_main.csv
- output/tables/summary_statistics_isr_main.tex
- output/tables/summary_statistics_isr_main.md
- optional decomposed versions
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from utils import (
    compute_summary_stats,
    connect_db,
    dataframe_to_latex_booktabs,
    ensure_dirs,
    load_config,
    read_table,
    save_markdown_table,
    setup_logger,
)


def export_table(df: pd.DataFrame, plan: pd.DataFrame, include_col: str, title: str, stem: str, cfg: dict, include_group: bool = False) -> None:
    tables_dir = Path(cfg["paths"]["tables"])
    table, common_n_flag = compute_summary_stats(df, plan, include_col, cfg)
    if table.empty:
        return
    n_values = table["N"].dropna().astype(int).unique().tolist() if "N" in table.columns else []
    use_common_n = bool(cfg.get("summary_tables", {}).get("use_common_n_row", True)) and common_n_flag and len(n_values) == 1
    common_n = int(n_values[0]) if use_common_n else None

    display_cols = ["Variable", "Description", "Mean", "Standard deviation", "Minimum", "Maximum"]
    if include_group:
        display_cols = ["Group"] + display_cols
    csv_cols = display_cols if common_n is not None else display_cols + ["N"]

    table[csv_cols].to_csv(tables_dir / f"{stem}.csv", index=False)
    latex = dataframe_to_latex_booktabs(table, caption=title, label=f"tab:{stem}", include_group=include_group, common_n=common_n)
    (tables_dir / f"{stem}.tex").write_text(latex, encoding="utf-8")
    save_markdown_table(table, tables_dir / f"{stem}.md", title, include_group=include_group, common_n=common_n)


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "08_export_isr_summary_tables")
    con = connect_db(cfg)
    final_table = cfg["research_design"].get("final_analysis_table", "analysis.analysis_ready")
    plan_path = Path(cfg["paths"]["audits"]) / "summary_statistics_plan.csv"

    if not plan_path.exists():
        logger.warning("summary_statistics_plan.csv not found. Skipping ISR-style tables.")
        return

    df = read_table(con, final_table)
    plan = pd.read_csv(plan_path)

    export_table(
        df,
        plan,
        include_col="include_in_main_table",
        title=cfg.get("summary_tables", {}).get("main_table_title", "Descriptive Statistics of Key Variables"),
        stem="summary_statistics_isr_main",
        cfg=cfg,
        include_group=False,
    )
    export_table(
        df,
        plan,
        include_col="include_in_decomposed_table",
        title=cfg.get("summary_tables", {}).get("decomposed_table_title", "Descriptive Statistics of Decomposed Variables"),
        stem="summary_statistics_isr_decomposed",
        cfg=cfg,
        include_group=True,
    )
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
