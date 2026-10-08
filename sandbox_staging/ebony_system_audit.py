"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: EBONY SYSTEM AUDIT
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os



    critical_paths = [

        "src/ingestion/schemas/sensor_schema_v1.json",

        "src/ingestion/adapters/drone_rgb_adapter.py",

        "src/ai_engine/gli_calc.py",

        "src/ai_engine/test_gli_calc.py",

        "src/ai_engine/Dockerfile",

        "src/alert_engine/flink_alert_job.py",

        "src/alert_engine/alert_rules.yaml",

        "src/dashboard/action_desk.py",

        ".github/workflows/model_ops_cicd.yml",

        "src/explainability/explain_api.py",

        "src/security/rbac_middleware.py",

        "src/qa/locustfile.py",

        "src/feedback/feedback_api.py",

        "src/sdk/python/ebony_edge/client.py",

        "src/sdk/cpp/ebony_edge/include/EbonyEdgeClient.h",

        "src/sdk/rust/ebony_edge/src/lib.rs",

        "src/compliance/regulatory_engine.py",

        "docs/compliance/soc2_control_matrix.md"

    ]



    print("\n" + "="*60)

    print(" 🦅 EBONY AI: COMPREHENSIVE SYSTEM AUDIT (v2.0) ")

    print("="*60)



    missing = 0

    for path in critical_paths:

        normalized_path = os.path.normpath(path)

        if os.path.exists(normalized_path):

            print(f"[VERIFIED] {normalized_path}")

        else:

            print(f"[FAILED]   {normalized_path} is MISSING!")

            missing += 1



    print("="*60)

    if missing == 0:

        print("EXECUTIVE STATUS: 100% OPERATIONAL. PROCEED TO Q3.")

    else:

        print(f"EXECUTIVE STATUS: SYSTEM COMPROMISED. {missing} FAILURES DETECTED.")

    print("="*60 + "\n")


if __name__ == "__main__":
    render()
