from __future__ import annotations
import pandas as pd
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "01b_hypothesis_design_audit")
    df = load_analysis_data(config)

    rows = []
    for h in config.get("hypotheses", []) or []:
        dv = h.get("dependent_variable")
        kv = h.get("key_independent_variable")
        moderator = h.get("moderator")
        mediator = h.get("mediator")
        rel = h.get("relationship_type")
        missing = [v for v in [dv, kv, moderator, mediator] if v and v not in df.columns]
        blocking = ""
        severity = "none"
        status = "ready"
        notes = []
        if not dv or not kv:
            blocking = "Dependent variable or key independent/treatment variable is not specified"
            severity = "critical"
            status = "not_ready"
        elif missing:
            blocking = "Configured hypothesis variables are missing from dataset"
            severity = "high"
            status = "not_ready"
            notes.append(f"Missing: {missing}")
        if rel == "moderation" and not moderator:
            severity = "medium" if severity == "none" else severity
            status = "conditionally_ready" if status == "ready" else status
            notes.append("Moderation hypothesis lacks a moderator variable in config")
        if rel in {"mediation", "mechanism"} and not mediator:
            severity = "medium" if severity == "none" else severity
            status = "conditionally_ready" if status == "ready" else status
            notes.append("Mediation/mechanism hypothesis lacks a mediator/mechanism variable in config")
        rows.append({
            "hypothesis_id": h.get("hypothesis_id"),
            "hypothesis_statement": h.get("statement"),
            "relationship_type": rel,
            "expected_direction": h.get("expected_direction"),
            "dependent_construct": h.get("dependent_construct", ""),
            "dependent_variable": dv,
            "key_construct": h.get("key_construct", ""),
            "key_variable": kv,
            "moderator": moderator,
            "mediator": mediator,
            "mechanism": h.get("mechanism", ""),
            "estimand_target": h.get("estimand_target"),
            "required_data_structure": config.get("design", {}).get("data_structure"),
            "required_timing": "cause/key variable must precede outcome; controls must be predetermined unless explicitly mechanism analysis",
            "readiness_status": status,
            "blocking_issue": blocking,
            "notes": "; ".join(notes),
        })
    if not rows:
        rows.append({
            "hypothesis_id": "missing",
            "hypothesis_statement": "No hypotheses configured",
            "relationship_type": "unknown",
            "expected_direction": "unknown",
            "dependent_construct": "",
            "dependent_variable": "",
            "key_construct": "",
            "key_variable": "",
            "moderator": "",
            "mediator": "",
            "mechanism": "",
            "estimand_target": "unknown",
            "required_data_structure": config.get("design", {}).get("data_structure"),
            "required_timing": "unknown",
            "readiness_status": "not_ready",
            "blocking_issue": "No hypothesis or empirical relationship is configured",
            "notes": "Ask user to provide hypothesis register before model selection",
        })
    save_csv(pd.DataFrame(rows), dirs, "hypothesis_design_audit.csv")


if __name__ == "__main__":
    main()
