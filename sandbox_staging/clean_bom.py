"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: CLEAN BOM
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sys



    # ==============================================================================

    # HVF Omni-Industrial Matrix | BYTE ORDER MARK (BOM) PURGE ENGINE

    # Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)

    # System: Strip U+FEFF Non-Printable Artifacts from Production Scripts

    # ==============================================================================



    TARGET_FILES = [

        r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console.py",

        r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console_GREEN.py"

    ]



    print("=" * 80)

    print("PURGING EMBEDDED BOM (U+FEFF) CHARACTERS FROM CONSOLE SCRIPTS")

    print("=" * 80)



    for fpath in TARGET_FILES:

        if os.path.exists(fpath):

            # utf-8-sig automatically strips leading BOM on read

            with open(fpath, "r", encoding="utf-8-sig") as f:

                content = f.read()



            # Explicitly purge any internal/shifted \ufeff occurrences

            cleaned_content = content.replace("\ufeff", "")



            # Write back as standard UTF-8 without BOM

            with open(fpath, "w", encoding="utf-8") as f:

                f.write(cleaned_content)



            print(f"[SUCCESS] Cleaned and sanitized: {os.path.basename(fpath)}")

        else:

            print(f"[WARN] Target not found: {fpath}")



    print("=" * 80)

    print("BOM PURGE COMPLETE - READY FOR PY_COMPILE")

    print("=" * 80)


if __name__ == "__main__":
    render()
