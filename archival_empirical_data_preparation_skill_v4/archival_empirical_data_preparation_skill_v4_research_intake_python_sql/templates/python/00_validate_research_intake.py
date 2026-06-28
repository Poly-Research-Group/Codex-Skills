"""Validate research-design intake before data preparation.

This script intentionally fails fast when the empirical design has not been
specified. It should run before ingestion, cleaning, merging, or transformation.

Run from the project root:
    python code/python/00_validate_research_intake.py --config config/project_config.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from utils import load_config, setup_logger, ensure_dirs

PLACEHOLDERS = {"", "TODO", "TBD", "NA", "N/A", "null", "None", "YOUR_PROJECT_NAME", "unit-time", "unit_id", "time_id"}


def _is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() in PLACEHOLDERS
    if isinstance(value, list):
        return len(value) == 0 or all(_is_blank(v) for v in value)
    if isinstance(value, dict):
        return len(value) == 0 or all(_is_blank(v) for v in value.values())
    return False


def _get(d: dict[str, Any], path: str) -> Any:
    cur: Any = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _has_nonblank_research_question(intake: dict[str, Any]) -> bool:
    rqs = _get(intake, "research_context.research_questions")
    if not isinstance(rqs, list):
        return False
    return any(not _is_blank(rq.get("question") if isinstance(rq, dict) else rq) for rq in rqs)


def _has_nonblank_hypothesis(intake: dict[str, Any]) -> bool:
    hyps = intake.get("hypotheses")
    if not isinstance(hyps, list):
        return False
    for hyp in hyps:
        if isinstance(hyp, dict) and not _is_blank(hyp.get("statement")):
            return True
    return False


def validate_intake(intake_path: Path) -> list[str]:
    issues: list[str] = []
    if not intake_path.exists():
        return [f"Missing research-design intake file: {intake_path}"]

    with intake_path.open("r", encoding="utf-8") as f:
        intake = yaml.safe_load(f) or {}

    required_paths = {
        "research_context.project_title": "project title",
        "research_context.empirical_context": "empirical context/platform/industry",
        "research_context.focal_phenomenon": "focal phenomenon",
        "empirical_design.unit_of_analysis": "unit of analysis",
        "empirical_design.data_structure": "data structure",
    }
    for path, label in required_paths.items():
        if _is_blank(_get(intake, path)):
            issues.append(f"Missing or placeholder value for {label} ({path}).")

    if not _has_nonblank_research_question(intake):
        issues.append("At least one research question is required.")

    if not _has_nonblank_hypothesis(intake):
        issues.append("At least one hypothesis or explicitly exploratory empirical relationship is required.")

    sources = intake.get("raw_data_sources")
    if not isinstance(sources, list) or not any(isinstance(s, dict) and not _is_blank(s.get("file_or_table_name")) for s in sources):
        issues.append("At least one raw data source with file/table/API name is required.")

    variables = intake.get("variables", {})
    if _is_blank(variables.get("dependent_variables")):
        issues.append("At least one dependent variable or dependent construct is required.")
    if _is_blank(variables.get("key_independent_variables")) and _is_blank(variables.get("treatment_or_event_variables")):
        issues.append("At least one key independent variable, treatment variable, event variable, or focal explanatory construct is required.")

    status = intake.get("intake_status", {})
    if not bool(status.get("confirmed_by_user")):
        issues.append("The intake has not been marked as confirmed_by_user: true. Confirm the design summary or record user-approved assumptions before proceeding.")

    return issues


def validate_csv_has_rows(path: Path, label: str) -> list[str]:
    if not path.exists():
        return [f"Missing {label}: {path}"]
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        return [f"Could not read {label} at {path}: {exc}"]
    if df.empty:
        return [f"{label} exists but has no rows. Populate it before preparing data."]
    return []


def main(config_path: str) -> None:
    cfg = load_config(config_path)
    ensure_dirs(cfg)
    logger = setup_logger(cfg, "00_validate_research_intake")

    intake_cfg = cfg.get("research_intake", {})
    intake_path = Path(intake_cfg.get("intake_yaml", "output/audits/research_design_intake.yaml"))
    hypothesis_register = Path(intake_cfg.get("hypothesis_register", "output/audits/hypothesis_register.csv"))
    construct_plan = Path(intake_cfg.get("construct_measurement_plan", "output/audits/construct_measurement_plan.csv"))
    timing_plan = Path(intake_cfg.get("identification_timing_plan", "output/audits/identification_timing_plan.csv"))

    issues = []
    issues.extend(validate_intake(intake_path))
    issues.extend(validate_csv_has_rows(hypothesis_register, "hypothesis register"))
    issues.extend(validate_csv_has_rows(construct_plan, "construct measurement plan"))
    issues.extend(validate_csv_has_rows(timing_plan, "identification timing plan"))

    if issues:
        logger.error("Research-design intake is incomplete. Blocking data-preparation pipeline.")
        for issue in issues:
            logger.error("- %s", issue)
        raise SystemExit("Research-design intake incomplete. Complete the intake artifacts or ask the user for missing information before preparing data.")

    logger.info("Research-design intake validation passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
