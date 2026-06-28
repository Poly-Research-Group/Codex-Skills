"""
00_validate_model_selection_inputs.py

Optional helper for the Stata Model Selection Skill. It checks whether the expected
upstream data-preparation and empirical-design-audit artifacts exist before Codex
selects Stata estimator families. It does not choose models by itself.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml

REQUIRED_RELATIVE_FILES = [
    "design_audit_package/docs/design_audit_report.md",
    "design_audit_package/docs/pre_model_go_no_go.md",
    "design_audit_package/docs/model_selection_handoff_memo.md",
    "design_audit_package/output/audits/hypothesis_design_audit.csv",
    "design_audit_package/output/audits/outcome_support_audit.csv",
    "design_audit_package/output/audits/control_bad_control_audit.csv",
    "design_audit_package/output/audits/fixed_effect_clustering_readiness_audit.csv",
    "design_audit_package/output/audits/identification_threat_register.csv",
    "analysis_package/data/analysis/analysis_ready.dta",
]

PLACEHOLDER_MARKERS = ["<", ">", "TODO", "TBD", "PLACEHOLDER"]


def contains_placeholder(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".", help="Project root containing analysis_package and design_audit_package")
    parser.add_argument("--config", default=None, help="Optional model_selection_config.yaml")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    missing = []
    placeholders = []

    for rel in REQUIRED_RELATIVE_FILES:
        p = root / rel
        if not p.exists():
            missing.append(rel)
        elif p.suffix.lower() in {".md", ".yaml", ".yml", ".csv"} and contains_placeholder(p):
            placeholders.append(rel)

    if args.config:
        config_path = Path(args.config).resolve()
        if not config_path.exists():
            missing.append(str(config_path))
        else:
            with config_path.open("r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            if cfg.get("model_selection_contract", {}).get("require_upstream_design_audit", True) and missing:
                pass

    output_dir = root / "stata_model_selection_package" / "logs"
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "model_selection_input_validation.txt"

    lines = []
    lines.append(f"Project root: {root}")
    lines.append("\nMissing required files:")
    lines.extend([f"- {m}" for m in missing] or ["- None"])
    lines.append("\nFiles that may contain placeholders:")
    lines.extend([f"- {p}" for p in placeholders] or ["- None"])

    if missing:
        lines.append("\nSTATUS: NOT READY. Resolve missing upstream artifacts or complete manual intake before selecting models.")
        status = 1
    else:
        lines.append("\nSTATUS: READY FOR MODEL-SELECTION INTAKE. Review placeholder warnings before final recommendations.")
        status = 0

    log_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nValidation log written to: {log_path}")
    return status


if __name__ == "__main__":
    sys.exit(main())
