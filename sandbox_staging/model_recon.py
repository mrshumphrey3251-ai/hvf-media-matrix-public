"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: MODEL RECON
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import urllib.request

    import json

    import os



    print("Initiating Google API Reconnaissance...")



    env_path = os.path.join(os.path.dirname(__file__), ".env")

    api_key = None

    if os.path.exists(env_path):

        with open(env_path, "r", encoding="utf-8") as f:

            for line in f:

                if line.startswith("GEMINI_API_KEY="):

                    api_key = line.strip().split("=", 1)[1]

                    break



    if not api_key:

        print("CRITICAL: API Key not found in vault.")

        exit()



    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    try:

        req = urllib.request.Request(url)

        with urllib.request.urlopen(req) as response:

            data = json.loads(response.read().decode())

            print("\n=== AUTHORIZED COGNITIVE MODELS ===")

            for m in data.get('models', []):

                if 'generateContent' in m.get('supportedGenerationMethods', []):

                    print(m['name'])

            print("===================================")

    except Exception as e:

        print(f"Recon failed: {e}. The API key may be invalid or restricted.")


if __name__ == "__main__":
    render()
