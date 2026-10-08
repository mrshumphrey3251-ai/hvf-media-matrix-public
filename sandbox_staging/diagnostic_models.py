"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: DIAGNOSTIC MODELS
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import json

    import urllib.request



    env_path = os.path.join(os.path.dirname(__file__), ".env")

    api_key = None

    if os.path.exists(env_path):

        with open(env_path, "r", encoding="utf-8") as f:

            for line in f:

                if line.startswith("GEMINI_API_KEY="):

                    api_key = line.strip().split("=", 1)[1]

                    break



    if api_key:

        print("Executing CEO Directive: Interrogating Google Network for Authorized Models...")

        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

        req = urllib.request.Request(url)

        try:

            with urllib.request.urlopen(req) as response:

                data = json.loads(response.read().decode('utf-8'))

                print("\n=== ABSOLUTE AUTHORIZED MODEL MANIFEST ===")

                valid_count = 0

                for m in data.get('models', []):

                    methods = m.get('supportedGenerationMethods', [])

                    name = m.get('name', '').replace('models/', '')

                    if 'generateContent' in methods and 'gemini' in name.lower():

                        print(f"[ACTIVE] {name}")

                        valid_count += 1

                print("==========================================")

                print(f"Total Authorized Models: {valid_count}\n")

        except Exception as e:

            print(f"Network Interrogation Failed: {e}")

    else:

        print("CRITICAL ERROR: API Key not found in .env vault.")


if __name__ == "__main__":
    render()
