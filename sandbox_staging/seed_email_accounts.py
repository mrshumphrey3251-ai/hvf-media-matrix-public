"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: SEED EMAIL ACCOUNTS
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import sqlite3



    # ==============================================================================

    # HVF Omni-Industrial Matrix | MULTI-ACCOUNT REGISTRATION PROBE

    # Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)

    # Registers default multi-inbox accounts into email_accounts table

    # ==============================================================================



    DB_PATH = r"C:\HVF_Repos\hvf-media-matrix-private\hvf_memory_vault.db"



    accounts = [

        (

            "HVF_PRIMARY_EXECUTIVE",

            "humphreyvirtualfarm@gmail.com",

            "imap.gmail.com",

            993,

            "smtp.gmail.com",

            465,

            "HVF_EXECUTIVE_EMAIL_APP_PASSWORD",

            1,

            1

        ),

        (

            "HVF_DEFENSE_TENCAP",

            "contracts@humphreyvirtualfarms.defense",

            "imap.gmail.com",

            993,

            "smtp.gmail.com",

            465,

            "HVF_DEFENSE_EMAIL_APP_PASSWORD",

            1,

            1

        )

    ]



    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()



    for acc in accounts:

        cur.execute("""

        INSERT OR REPLACE INTO email_accounts 

        (account_alias, email_address, imap_server, imap_port, smtp_server, smtp_port, env_password_key, use_ssl, is_active)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, acc)



    conn.commit()



    cur.execute("SELECT id, account_alias, email_address, imap_server, is_active FROM email_accounts")

    rows = cur.fetchall()

    conn.close()



    print("=" * 80)

    print("REGISTERED MULTI-ACCOUNT MONITORED INBOXES:")

    print("=" * 80)

    for r in rows:

        print(f"  * Account ID: {r[0]} | Alias: {r[1]} | Address: {r[2]} | Server: {r[3]} | Active: {r[4]}")

    print("=" * 80)


if __name__ == "__main__":
    render()
