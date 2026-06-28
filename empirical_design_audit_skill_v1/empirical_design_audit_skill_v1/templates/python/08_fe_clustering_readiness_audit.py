from __future__ import annotations
import pandas as pd
from utils_audit import read_config, ensure_output_dirs, setup_logging, load_analysis_data, save_csv, variable_list, summarize_group_sizes


def within_variation_flag(df: pd.DataFrame, group: str, var: str) -> str:
    if group not in df.columns or var not in df.columns:
        return "unknown"
    # Sample large datasets to avoid expensive groupby on huge archival files.
    x = df[[group, var]].dropna()
    if len(x) > 2_000_000:
        x = x.sample(2_000_000, random_state=20260620)
    nunique = x.groupby(group)[var].nunique(dropna=True)
    if nunique.empty:
        return "unknown"
    share_varying = float((nunique > 1).mean())
    if share_varying == 0:
        return "none_within_group"
    if share_varying < 0.10:
        return "very_limited_within_group"
    return "sufficient_for_diagnostic_purposes"


def main() -> None:
    config = read_config()
    dirs = ensure_output_dirs(config)
    setup_logging(dirs["root"], "08_fe_clustering_readiness_audit")
    df = load_analysis_data(config)
    fe_vars = variable_list(config, "fixed_effects")
    cluster_vars = variable_list(config, "clustering_dimensions")
    key_vars = variable_list(config, "key_independent_variables") + variable_list(config, "treatments")

    rows = []
    max_singleton_warn = config.get("thresholds", {}).get("max_singleton_fe_share_warn", 0.10)
    min_clusters_warn = config.get("thresholds", {}).get("min_clusters_warn", 30)

    for fe in fe_vars:
        stats = summarize_group_sizes(df, fe)
        within = "; ".join([f"{v}:{within_variation_flag(df, fe, v)}" for v in key_vars]) if key_vars else "not_checked"
        severity = "medium" if (stats.get("singleton_share") is not None and stats["singleton_share"] > max_singleton_warn) else "none"
        absorption = "high" if "none_within_group" in within else "low"
        if absorption == "high":
            severity = "high"
        rows.append({
            "dimension_type": "fixed_effect",
            "variable": fe,
            "n_categories_or_clusters": stats.get("n"),
            "min_group_size": stats.get("min"),
            "median_group_size": stats.get("median"),
            "max_group_size": stats.get("max"),
            "singleton_count": stats.get("singleton_count"),
            "singleton_share": stats.get("singleton_share"),
            "key_variable_within_variation": within,
            "absorption_risk": absorption,
            "small_cluster_risk": "not_applicable",
            "recommended_use": "requires_review" if severity != "none" else "feasible_pending_model_selection",
            "severity": severity,
            "notes": "Check singleton handling and absorbed variables before HDFE/FE modeling" if severity != "none" else "No immediate FE feasibility issue detected",
        })

    for cl in cluster_vars:
        stats = summarize_group_sizes(df, cl)
        small_cluster = stats.get("n") is not None and stats["n"] < min_clusters_warn
        rows.append({
            "dimension_type": "cluster",
            "variable": cl,
            "n_categories_or_clusters": stats.get("n"),
            "min_group_size": stats.get("min"),
            "median_group_size": stats.get("median"),
            "max_group_size": stats.get("max"),
            "singleton_count": stats.get("singleton_count"),
            "singleton_share": stats.get("singleton_share"),
            "key_variable_within_variation": "not_applicable",
            "absorption_risk": "not_applicable",
            "small_cluster_risk": "yes" if small_cluster else "no",
            "recommended_use": "consider_wild_bootstrap_or_alternative_inference" if small_cluster else "feasible_pending_model_selection",
            "severity": "medium" if small_cluster else "none",
            "notes": "Small number of clusters; later model-selection skill should handle inference carefully" if small_cluster else "Cluster count is not obviously small",
        })
    save_csv(pd.DataFrame(rows), dirs, "fixed_effect_clustering_readiness_audit.csv")


if __name__ == "__main__":
    main()
