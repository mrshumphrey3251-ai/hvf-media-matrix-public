"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: FLINK ALERT JOB
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import yaml



    def load_rules(filepath):

        with open(filepath, 'r') as f:

            return yaml.safe_load(f)



    def process_telemetry(telemetry, rules):

        for rule in rules['rules']:

            if "soil_moisture < 15" in rule['condition'] and telemetry.get('soil_moisture', 100) < 15:

                print(f"[ALERT FIRED] {rule['name']} - Sending {rule['actions'][0]['type']} to {rule['actions'][0]['target']}")

            if "gli < 0.2" in rule['condition'] and telemetry.get('gli', 1.0) < 0.2:

                print(f"[ALERT FIRED] {rule['name']} - Triggering {rule['actions'][0]['target']}.")



    if __name__ == '__main__':

        print("HVF Real-Time Alert Engine Staged...")

        rules = load_rules('src/alert_engine/alert_rules.yaml')

        process_telemetry({"soil_moisture": 12, "gli": 0.45}, rules)


if __name__ == "__main__":
    render()
