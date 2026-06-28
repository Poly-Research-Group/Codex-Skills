from __future__ import annotations
import pandas as pd
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, variable_list


def infer_support(s: pd.Series) -> str:
    non = s.dropna()
    if non.empty:
        return "unknown_all_missing"
    vals = set(non.unique()) if non.nunique(dropna=True) <= 20 else set()
    if vals and vals.issubset({0, 1, True, False}):
        return "binary"
    if pd.api.types.is_integer_dtype(non) and non.min() >= 0:
        return "count_nonnegative_integer"
    if pd.api.types.is_numeric_dtype(non):
        if non.min() >= 0 and non.max() <= 1:
            return "fraction_or_share"
        return "continuous_or_skewed_numeric"
    return "categorical_or_text"


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "04b_outcome_support_audit")
    df = load_analysis_data(config)

    rows = []
    for y in variable_list(config, "outcomes"):
        if y not in df.columns:
            rows.append({
                "outcome_variable": y,
                "construct": "",
                "support_type": "missing_from_data",
                "n_nonmissing": 0,
                "missing_rate": None,
                "min": None,
                "max": None,
                "zero_count": None,
                "negative_count": None,
                "censoring_or_truncation_flag": "unknown",
                "transformation": "unknown",
                "timing_status": "unknown",
                "severity": "critical",
                "status": "not_ready",
                "notes": "Outcome variable not found in dataset",
            })
            continue
        s = df[y]
        numeric = pd.api.types.is_numeric_dtype(s)
        miss = float(s.isna().mean())
        support = infer_support(s)
        zero_count = int((s == 0).sum()) if numeric else None
        neg_count = int((s < 0).sum()) if numeric else None
        if miss >= config.get("thresholds", {}).get("key_variable_missing_rate_stop", 0.30):
            severity, status = "high", "not_ready"
        elif miss >= config.get("thresholds", {}).get("key_variable_missing_rate_warn", 0.10):
            severity, status = "medium", "conditionally_ready"
        else:
            severity, status = "none", "ready"
        rows.append({
            "outcome_variable": y,
            "construct": "",
            "support_type": support,
            "n_nonmissing": int(s.notna().sum()),
            "missing_rate": miss,
            "min": float(s.min()) if numeric and s.notna().any() else None,
            "max": float(s.max()) if numeric and s.notna().any() else None,
            "zero_count": zero_count,
            "negative_count": neg_count,
            "censoring_or_truncation_flag": "requires_manual_review",
            "transformation": "requires_manual_review",
            "timing_status": "requires_timing_audit_review",
            "severity": severity,
            "status": status,
            "notes": "Outcome support should inform later Stata model selection; this audit does not choose the model.",
        })
    save_csv(pd.DataFrame(rows), dirs, "outcome_support_audit.csv")


if __name__ == "__main__":
    main()
