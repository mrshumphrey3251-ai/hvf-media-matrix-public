"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: UPGRADE DIRECT DISPATCH
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os
    import sys
    import py_compile

    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
    CORE_FILE = os.path.join(BASE_DIR, "email_triage_core.py")

    print("=" * 80)
    print("EXPANDING EMAIL_TRIAGE_CORE.PY: DIRECT OUTBOUND COMPOSITION ENGINE")
    print("=" * 80)

    if not os.path.exists(CORE_FILE):
        print(f"[FAIL] Core file not found at: {CORE_FILE}")
        sys.exit(1)

    with open(CORE_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    DIRECT_SEND_CODE = '''
    def send_direct_outbound_email(to_addr: str, subject: str, body: str, account_alias: str = "HVF_PRIMARY_EXECUTIVE", category: str = "DIRECT_EXECUTIVE_OUTBOUND") -> tuple:
        """
        Directly composes and transmits a sovereign outbound email via SSL SMTP (Port 465).
        Enforces DFARS provenance headers, decrypts token in-memory, and writes an immutable
        audit entry into staged_email_dispatches with status 'DISPATCHED_SUCCESS'.
        """
        clean_recipient = extract_clean_email(to_addr)
        if not clean_recipient:
            return False, f"Invalid destination recipient address: {to_addr}"

        if not subject.strip():
            return False, "Outbound transmission must include a subject line."

        if not body.strip():
            return False, "Outbound transmission body cannot be empty."

        try:
            conn = get_db_connection(timeout=30.0)
            cur = conn.cursor()

            # 1. Retrieve authenticated endpoint credentials
            cur.execute("""
                SELECT email_address, smtp_server, smtp_port, encrypted_password 
                FROM email_accounts 
                WHERE account_alias = ? AND is_active = 1
            """, (account_alias,))
            acc_info = cur.fetchone()

            if not acc_info or not acc_info[3]:
                # Fallback to HVF_PRIMARY_EXECUTIVE
                cur.execute("""
                    SELECT email_address, smtp_server, smtp_port, encrypted_password 
                    FROM email_accounts 
                    WHERE account_alias = 'HVF_PRIMARY_EXECUTIVE' AND is_active = 1
                """)
                acc_info = cur.fetchone()

            if not acc_info or not acc_info[3]:
                conn.close()
                return False, f"No active credentials configured for account '{account_alias}'."

            auth_email, smtp_srv, smtp_prt, enc_pwd = acc_info
            clear_pwd = decrypt_credential(enc_pwd)

            if not clear_pwd:
                conn.close()
                return False, "Failed to decrypt SMTP authentication credentials in-memory."

            # 2. Build RFC5322 MIME Transmission with Defense Headers
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject.strip()
            msg["From"] = f"HVF Omni-Industrial Matrix <{auth_email}>"
            msg["To"] = clean_recipient
            msg["Reply-To"] = auth_email
            msg["X-Originating-System"] = "Ebony AI Sovereign Command Deck"
            msg["X-HVF-CAGE"] = "1AHA8"
            msg["X-Compliance"] = "DFARS 252.227-7018"

            msg.attach(MIMEText(body.strip(), "plain", "utf-8"))

            # 3. Transmit via SSL SMTP (Port 465)
            server = smtplib.SMTP_SSL(str(smtp_srv).strip(), int(smtp_prt), timeout=30.0)
            server.login(auth_email, clean_token(clear_pwd))
            server.sendmail(auth_email, [clean_recipient], msg.as_string())
            server.quit()

            # 4. Record Dispatch in Audit Ledger
            now_ts = datetime.now().isoformat()
            cur.execute("""
                INSERT INTO staged_email_dispatches 
                (account_alias, message_uid, sender_address, recipient_address, subject, date_received, raw_body_sanitized, threat_status, triage_category, draft_response, veto_status)
                VALUES (?, 'OUTBOUND_DIRECT', ?, ?, ?, ?, ?, 'INSPECTED_CLEAN', ?, ?, 'DISPATCHED_SUCCESS')
            """, (account_alias, auth_email, clean_recipient, subject.strip(), now_ts, body.strip(), category, body.strip()))

            conn.close()
            return True, f"Outbound transmission successfully dispatched to {clean_recipient} via {smtp_srv}:{smtp_prt}."

        except Exception as e:
            return False, f"Direct outbound dispatch failed: {str(e)}"

    def generate_direct_draft_assistance(to_recipient: str, objective_prompt: str) -> str:
        """Generates an executive-level outbound message grounded in the Iron Dome knowledge base."""
        if not client:
            return "Groq inference client offline. Please enter outbound message body manually."

        context = query_iron_dome(objective_prompt, objective_prompt)

        system_prompt = f"""You are Ebony, sovereign AI for HVF Omni-Industrial Matrix (CAGE: 1AHA8, UEI: S1M4ENLHTDH5), led by Founder & CEO Jeffery Humphrey.
    Draft a commanding, professional, and authoritative outbound executive correspondence based on the objective provided.
    Grounded in HVF's prime contracting standing, defense posture, and relevant operational intelligence.

    --- DESTINATION RECIPIENT: {to_recipient}
    --- STRATEGIC OBJECTIVE: {objective_prompt}

    --- SOVEREIGN INTEL CONTEXT ---
    {context}
    -------------------------------

    Provide ONLY the final email body text. Close with:
    Office of the Chief Executive
    HVF Omni-Industrial Matrix
    Prime Contractor | CAGE: 1AHA8"""

        try:
            res = client.chat.completions.create(
                model=ACTIVE_MODEL,
                messages=[{"role": "user", "content": system_prompt}],
                temperature=0.2
            )
            return res.choices[0].message.content.strip()
        except Exception as e:
            return f"[AI DRAFTING ERROR]: {e}"
    '''

    if "def send_direct_outbound_email" not in code:
        code = code.strip() + "\n\n" + DIRECT_SEND_CODE.strip() + "\n"
        with open(CORE_FILE, "w", encoding="utf-8") as f:
            f.write(code)
        print("[SUCCESS] Appended 'send_direct_outbound_email()' and 'generate_direct_draft_assistance()' to email_triage_core.py.")
    else:
        print("[INFO] Direct send routines already present in email_triage_core.py.")

    py_compile.compile(CORE_FILE, doraise=True)
    print(f"[SUCCESS] email_triage_core.py compiled cleanly with zero syntax errors.")
    print("=" * 80)




if __name__ == "__main__":
    render()
