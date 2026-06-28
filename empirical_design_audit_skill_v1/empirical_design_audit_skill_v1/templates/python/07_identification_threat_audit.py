from __future__ import annotations
import pandas as pd
from utils_audit import read_config, ensure_output_dirs, setup_logging, save_csv

BASE_THREATS = [
    ("omitted_confounding", "Omitted time-varying confounders", "Unobserved changes may drive both treatment/key IV and outcome."),
    ("reverse_causality", "Reverse causality", "The expected outcome or anticipated outcome may affect the key IV/treatment."),
    ("selection", "Selection into treatment/sample", "Units may select into treatment, platform participation, visibility, or the observed sample."),
    ("measurement_error", "Measurement error", "API, scraping, or platform measures may be noisy or selectively missing."),
    ("algorithmic_confounding", "Algorithmic confounding", "Platform ranking, recommendation, moderation, or monetization systems may jointly affect exposure and outcomes."),
    ("interference", "Interference/spillovers", "One unit's treatment may affect another unit's outcome, violating no-interference assumptions."),
    ("attrition", "Attrition/survivorship", "Entry, exit, suspension, deletion, or inactive periods may change sample composition."),
    ("seasonality_shocks", "Seasonality and platform-wide shocks", "Time shocks, release calendars, news events, or platform policy changes may confound effects."),
]

DESIGN_SPECIFIC = {
    "did_event_study": [
        ("parallel_trends", "Parallel-trends plausibility", "Treated and comparison units should have comparable pre-treatment trends."),
        ("anticipation", "Anticipation", "Units may change behavior before treatment/event if they anticipate it."),
        ("staggered_heterogeneity", "Staggered adoption heterogeneity", "Treatment effects may vary across cohorts and event time."),
        ("concurrent_events", "Concurrent shocks", "Other events may coincide with treatment timing."),
    ],
    "iv": [
        ("instrument_relevance", "Instrument relevance", "Instrument must shift the endogenous regressor."),
        ("exclusion_restriction", "Exclusion restriction", "Instrument should affect outcome only through the endogenous regressor."),
        ("instrument_timing", "Instrument timing", "Instrument should be predetermined relative to outcome."),
    ],
    "rd": [
        ("cutoff_manipulation", "Running-variable manipulation", "Units may sort around the threshold."),
        ("local_continuity", "Local continuity", "Potential outcomes and covariates should be continuous at cutoff."),
    ],
    "network_spillover": [
        ("exposure_mapping", "Exposure mapping", "Network exposure must be defined before observing outcomes."),
        ("endogenous_network", "Endogenous network formation", "Network ties may be formed in response to expected outcomes."),
        ("reflection", "Reflection problem", "Peer outcomes and focal outcomes may be simultaneously determined."),
    ],
    "dynamic_panel": [
        ("lagged_dv_bias", "Lagged dependent variable bias", "Lagged outcomes with fixed effects can create dynamic panel bias."),
        ("instrument_proliferation", "Instrument proliferation", "Dynamic panel instruments can overfit endogenous variables."),
    ],
}


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "07_identification_threat_audit")
    intended = config.get("design", {}).get("intended_design_family", []) or []
    if isinstance(intended, str):
        intended = [intended]
    rows = []
    idx = 1
    for key, threat, why in BASE_THREATS:
        rows.append({
            "threat_id": f"T{idx:03d}",
            "design_family": "general",
            "threat": threat,
            "why_it_matters": why,
            "evidence_from_data_or_metadata": "requires_review",
            "severity": "medium",
            "status": "conditionally_ready",
            "mitigation_or_robustness": "Document design logic; consider FE, pre-period controls, placebo tests, sensitivity checks, or alternative samples as appropriate.",
            "blocks_model_selection": "no",
            "notes": "",
        })
        idx += 1
    for family in intended:
        for key, threat, why in DESIGN_SPECIFIC.get(family, []):
            rows.append({
                "threat_id": f"T{idx:03d}",
                "design_family": family,
                "threat": threat,
                "why_it_matters": why,
                "evidence_from_data_or_metadata": "requires_review",
                "severity": "medium",
                "status": "conditionally_ready",
                "mitigation_or_robustness": "Add design-specific diagnostic before model interpretation.",
                "blocks_model_selection": "no",
                "notes": "",
            })
            idx += 1
    save_csv(pd.DataFrame(rows), dirs, "identification_threat_register.csv")


if __name__ == "__main__":
    main()
