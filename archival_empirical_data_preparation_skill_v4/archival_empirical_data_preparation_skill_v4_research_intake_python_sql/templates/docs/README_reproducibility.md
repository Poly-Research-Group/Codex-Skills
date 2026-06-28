# Reproducibility README

## Project overview

Briefly describe the research project, data sources, and empirical unit of analysis.

## Software environment

- Python version:
- SQL engine:
- Main Python packages:
- Operating system:
- Stata version expected for downstream analysis:

## Folder structure

```text
project_root/
  config/
  code/python/
  code/sql/
  data/raw/
  data/interim/
  data/clean/
  data/analysis/
  output/audits/
  output/tables/
  logs/
  docs/
```

## Execution order

Run:

```bash
python code/python/00_master.py --config config/project_config.yaml
```

The master script should execute:

1. `01_ingest_raw.py`
2. `02_clean_sources.py`
3. `03_build_keys_time.py`
4. `04_merge_build_analysis.py`
5. `05_construct_variables.py`
6. `06_define_samples.py`
7. `07_data_diagnostics.py`
8. `08_export_isr_summary_tables.py`
9. `09_export_analysis_package.py`

## Expected outputs

- `data/analysis/analysis_ready.dta`
- `data/analysis/analysis_ready.parquet`
- `output/audits/*.csv`
- `output/tables/summary_statistics_isr_main.*`
- `docs/model_readiness_memo.md`

## Data access restrictions

Document whether raw data can be shared, require API credentials, or are subject to platform terms.

## Known limitations

- 
