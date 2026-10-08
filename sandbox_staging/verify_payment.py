"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: VERIFY PAYMENT
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import sqlite3

    DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("SELECT invite_code, grant_role, is_used, used_by FROM member_invite_keys ORDER BY id DESC LIMIT 1")

    row = cur.fetchone()

    conn.close()

    print(f"DATABASE VAULT VERIFIED: Key={row[0]} | Role={row[1]} | Used={row[2]} | Recipient={row[3]}")

if __name__ == "__main__":
    render()
