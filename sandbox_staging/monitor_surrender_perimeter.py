"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: MONITOR SURRENDER PERIMETER
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sqlite3

    from datetime import datetime, timedelta



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")



    def check_perimeter():

        conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT subcontractor, severance_timestamp, surrender_deadline, status 

            FROM legal_surrender_tracker 

            ORDER BY id DESC LIMIT 1

        """)

        row = cursor.fetchone()



        if not row:

            print("[ERROR] No active surrender tracker found in memory vault.")

            conn.close()

            return



        subcontractor, sev_time, deadline_str, status = row

        deadline = datetime.fromisoformat(deadline_str)

        now = datetime.now()

        remaining = deadline - now



        print("=" * 80)

        print("HVF Omni-Industrial Matrix | SECTION 9.3 LEGAL SURRENDER PERIMETER")

        print("=" * 80)

        print(f"  Target Entity      : {subcontractor}")

        print(f"  Severance Executed : {sev_time}")

        print(f"  Surrender Deadline : {deadline_str} CDT")

        print(f"  Current Time       : {now.strftime('%Y-%m-%d %H:%M:%S')}")

        print("-" * 80)



        if remaining.total_seconds() > 0:

            total_seconds = int(remaining.total_seconds())

            hours = total_seconds // 3600

            minutes = (total_seconds % 3600) // 60

            seconds = total_seconds % 60

            print(f"  STATUS             : COUNTDOWN ACTIVE")

            print(f"  TIME REMAINING     : {hours} Hours, {minutes} Minutes, {seconds} Seconds")

            print(f"  RADIO SILENCE      : STRICTLY ENFORCED (Do Not Initiate Contact)")

            print(f"  INBOX SURVEILLANCE : Active on humphreyvirtualfarm@gmail.com")



            # Log heartbeat audit

            conn.execute("""

                INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)

                VALUES (?, ?, ?, ?, ?, ?)

            """, (

                "Jeffery Humphrey, CEO",

                subcontractor,

                "SURRENDER_COUNTDOWN_HEARTBEAT",

                f"Perimeter heartbeat: {hours}h {minutes}m remaining until key surrender deadline.",

                now.isoformat(),

                "PERIMETER_SECURE"

            ))

        else:

            print(f"  STATUS             : DEADLINE EXPIRED")

            print(f"  ACTION REQUIRED    : Escalate to formal legal referral and IP enforcement.")



        conn.close()

        print("=" * 80)



    if __name__ == "__main__":

        check_perimeter()




if __name__ == "__main__":
    render()
