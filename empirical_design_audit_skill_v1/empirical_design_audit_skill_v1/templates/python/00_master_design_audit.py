from __future__ import annotations
import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "01_load_inputs_validate_metadata.py",
    "01b_hypothesis_design_audit.py",
    "02_unit_time_structure_audit.py",
    "03_timing_and_leakage_audit.py",
    "04_treatment_event_construction_audit.py",
    "04b_outcome_support_audit.py",
    "05_control_and_bad_control_audit.py",
    "06_sample_restriction_attrition_audit.py",
    "07_identification_threat_audit.py",
    "08_fe_clustering_readiness_audit.py",
    "09_export_design_audit_package.py",
]


def main() -> None:
    base = Path(__file__).resolve().parent
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(base / script)], check=True)


if __name__ == "__main__":
    main()
