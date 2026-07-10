#!/usr/bin/env python3
"""Create a local literature-review workspace and copy templates.

Usage:
    python create_lit_review_workspace.py --root . --project-name my_project
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def safe_slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value.strip())
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "literature_review_project"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an IS literature-review workspace.")
    parser.add_argument("--root", default=".", help="Root directory where the workspace should be created.")
    parser.add_argument("--project-name", default="literature_review_project", help="Project name used as the folder name.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    project_dir = root / safe_slug(args.project_name)
    lit_dir = project_dir / "literature"

    folders = [
        lit_dir / "search",
        lit_dir / "screening",
        lit_dir / "synthesis",
        lit_dir / "pdfs",
        lit_dir / "notes",
        lit_dir / "outputs",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    assets_dir = skill_dir / "assets"
    references_dir = skill_dir / "references"

    copy_map = {
        assets_dir / "search_strategy_template.md": lit_dir / "search" / "search_strategy.md",
        assets_dir / "search_approval_form.md": lit_dir / "search" / "search_approval_form.md",
        assets_dir / "search_log_template.csv": lit_dir / "search" / "search_log.csv",
        assets_dir / "screening_matrix_template.csv": lit_dir / "screening" / "screening_matrix.csv",
        assets_dir / "paper_synthesis_matrix_template.csv": lit_dir / "synthesis" / "paper_synthesis_matrix.csv",
        assets_dir / "variable_measure_matrix_template.csv": lit_dir / "synthesis" / "variable_measure_matrix.csv",
        assets_dir / "literature_stream_matrix_template.csv": lit_dir / "synthesis" / "literature_stream_matrix.csv",
        assets_dir / "construct_measures_matrix_template.csv": lit_dir / "synthesis" / "construct_measures_matrix.csv",
        assets_dir / "positioning_memo_template.md": lit_dir / "outputs" / "positioning_memo.md",
        assets_dir / "journal_scope.csv": lit_dir / "search" / "journal_scope.csv",
        references_dir / "elite_is_journal_scope.md": lit_dir / "search" / "elite_is_journal_scope.md",
    }

    for src, dest in copy_map.items():
        if src.exists():
            shutil.copyfile(src, dest)

    readme = project_dir / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {args.project_name}\n\n"
            "Literature-review workspace created for IS literature scouting and paper synthesis.\n\n"
            "Start with `literature/search/search_strategy.md`, get the search strategy approved, "
            "then log executed queries in `literature/search/search_log.csv`.\n",
            encoding="utf-8",
        )

    print(f"Created literature-review workspace at: {project_dir}")


if __name__ == "__main__":
    main()
