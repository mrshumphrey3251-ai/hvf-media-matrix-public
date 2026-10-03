import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
CORE_FILE = os.path.join(BASE_DIR, "email_triage_core.py")

print("=" * 80)
print("INJECTING OUTBOUND SMTP TRANSMISSION ROUTINE INTO EMAIL_TRIAGE_CORE.PY")
print("=" * 80)

if not os.path.exists(CORE_FILE):
    print(f"[FAIL] File not found: {CORE_FILE}")
    sys.exit(1)

with open(CORE_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Ensure smtplib and MIME libraries are imported
if "import smtplib" not in content:
    content = "import smtplib\nfrom email.mime.text import MIMEText\nfrom email.mime.multipart import MIMEMultipart\n" + content

# Outbound Dispatch Implementation
DISPATCH_FUNCTION = '''
def dispatch_outbound_transmission(dispatch_id: int, final_body_override: str = None) -> tuple:
    """
    Executes live outbound SMTP transmission for a CEO-approved dispatch.
    Decrypts stored application token in-memory, connects to SSL port 465,
    transmits the final payload, and logs the execution audit in SQLite vault.
    """
    try:
        conn = get_db_connection(timeout=30.0)
        cur = conn.cursor()
        
        # 1. Fetch staged dispatch payload
        cur.execute("""
            SELECT account_alias, sender_address, recipient_address, subject, draft_response 
            FROM staged_email_dispatches 
            WHERE id = ?
        """, (dispatch_id,))
        row = cur.fetchone()
        
        if not row:
            conn.close()
            return False, f"Dispatch ID #{dispatch_id} not found in staging ledger."
            
        acc_alias, to_addr, from_addr, orig_subj, original_draft = row
        body_to_send = final_body_override if final_body_override is not None else original_draft
        
        # 2. Extract clean recipient address
        clean_recipient = extract_clean_email(to_addr)
        if not clean_recipient:
            conn.close()
            return False, f"Invalid recipient destination: {to_addr}"
            
        # 3. Retrieve and decrypt account credentials
        cur.execute("""
            SELECT email_address, smtp_server, smtp_port, encrypted_password 
            FROM email_accounts 
            WHERE account_alias = ? AND is_active = 1
        """, (acc_alias,))
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
            return False, f"No active credentials configured for account '{acc_alias}'."
            
        auth_email, smtp_srv, smtp_prt, enc_pwd = acc_info
        clear_pwd = decrypt_credential(enc_pwd)
        
        if not clear_pwd:
            conn.close()
            return False, "Failed to decrypt SMTP authentication token in-memory."
            
        # 4. Construct RFC5322 MIME transmission
        subj_prefix = "Re: " if not orig_subj.lower().startswith("re:") else ""
        outbound_subj = f"{subj_prefix}{orig_subj}"
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = outbound_subj
        msg["From"] = f"HVF Omni-Industrial Matrix <{auth_email}>"
        msg["To"] = clean_recipient
        msg["Reply-To"] = auth_email
        msg["X-Originating-System"] = "Ebony AI Defense C2 Core"
        msg["X-HVF-CAGE"] = "1AHA8"
        
        msg.attach(MIMEText(body_to_send, "plain", "utf-8"))
        
        # 5. Connect and Transmit via SSL SMTP (Port 465)
        server = smtplib.SMTP_SSL(str(smtp_srv).strip(), int(smtp_prt), timeout=30.0)
        server.login(auth_email, clean_token(clear_pwd))
        server.sendmail(auth_email, [clean_recipient], msg.as_string())
        server.quit()
        
        # 6. Update Veto Ledger to Dispatched State
        now_ts = datetime.now().isoformat()
        cur.execute("""
            UPDATE staged_email_dispatches 
            SET veto_status = 'DISPATCHED_SUCCESS',
                draft_response = ?
            WHERE id = ?
        """, (body_to_send, dispatch_id))
        conn.close()
        
        return True, f"Outbound transmission #{dispatch_id} successfully delivered to {clean_recipient}."
        
    except Exception as e:
        return False, f"SMTP transmission failed: {str(e)}"
'''

if "def dispatch_outbound_transmission" not in content:
    content = content.strip() + "\n\n" + DISPATCH_FUNCTION.strip() + "\n"
    with open(CORE_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] Appended 'dispatch_outbound_transmission()' to email_triage_core.py.")
else:
    print("[INFO] 'dispatch_outbound_transmission()' is already present in email_triage_core.py.")

py_compile.compile(CORE_FILE, doraise=True)
print(f"[SUCCESS] email_triage_core.py compiled cleanly with zero syntax errors.")
print("=" * 80)

