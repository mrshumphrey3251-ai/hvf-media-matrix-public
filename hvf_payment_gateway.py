import os
import json
import sqlite3
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv(override=True)
REPO_DIR = os.path.abspath(r"C:\HVF_Repos\hvf-media-matrix-private")
DB_PATH = os.path.join(REPO_DIR, "hvf_memory_vault.db")

SMTP_EMAIL = os.getenv("HVF_SMTP_EMAIL", "humphreyvirtualfarm@gmail.com")
SMTP_PASS = os.getenv("HVF_SMTP_APP_PASSWORD", "")

app = Flask(__name__)

def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS member_invite_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invite_code TEXT UNIQUE NOT NULL,
            issued_by TEXT NOT NULL,
            grant_role TEXT NOT NULL DEFAULT 'MEMBER',
            is_used INTEGER DEFAULT 0,
            used_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Check if grant_role column exists (auto-migration)
    cur.execute("PRAGMA table_info(member_invite_keys)")
    cols = [col[1] for col in cur.fetchall()]
    if "grant_role" not in cols:
        cur.execute("ALTER TABLE member_invite_keys ADD COLUMN grant_role TEXT NOT NULL DEFAULT 'MEMBER'")
    conn.commit()
    conn.close()

def record_license_in_db(invite_code: str, target_role: str, customer_email: str):
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO member_invite_keys (invite_code, issued_by, grant_role, is_used, used_by)
        VALUES (?, 'STRIPE_GATEWAY', ?, 0, ?)
    """, (invite_code, target_role, customer_email))
    conn.commit()
    conn.close()

def send_fulfillment_email(to_email: str, license_key: str, tier_name: str):
    if not SMTP_PASS:
        return
    subject = f"⚡ Your Humphrey Virtual Farm Access License [{license_key}]"
    body = f"""
    <html>
    <body style="background-color: #050709; color: #FFFFFF; font-family: Arial, sans-serif; padding: 25px;">
        <h2 style="color: #00FF66;">⚡ Humphrey Virtual Farm | Sovereign Platform Access</h2>
        <p>Thank you for your subscription to <strong>{tier_name}</strong>.</p>
        <div style="background-color: #0c1118; border: 2px solid #00FF66; border-radius: 6px; padding: 15px; font-size: 1.4rem; font-weight: bold; color: #70FF00; text-align: center; margin: 20px 0;">
            {license_key}
        </div>
        <p>Enter this key under <strong>Activate VIP Code</strong> in the HVF portal.</p>
    </body>
    </html>
    """
    msg = MIMEMultipart()
    msg["From"] = f"Humphrey Virtual Farm <{SMTP_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASS)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Email notification error: {str(e)}")

@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    try:
        payload = request.get_json(silent=True) or {}
        event_type = payload.get("type", "")
        data_obj = payload.get("data", {}).get("object", {})

        is_simulated = request.args.get("simulated") == "true"
        if event_type == "checkout.session.completed" or is_simulated:
            customer_email = data_obj.get("customer_details", {}).get("email") or request.args.get("email", "client@example.com")
            amount_total = data_obj.get("amount_total", 24900)

            if amount_total >= 200000:
                target_role = "CLIENT_CEO"
                prefix = "HVF-CORP"
                tier_name = "Enterprise Farm CEO Annual Plan ($2,499/yr)"
            elif amount_total >= 20000:
                target_role = "MEMBER"
                prefix = "HVF-VIP"
                tier_name = "VIP Farm Member Monthly Plan ($249/mo)"
            else:
                target_role = "MEMBER"
                prefix = "HVF-PERS"
                tier_name = "Personal Sovereign Monthly Plan ($19.99/mo)"

            license_key = f"{prefix}-{secrets.token_hex(3).upper()}"
            record_license_in_db(license_key, target_role, customer_email)
            send_fulfillment_email(customer_email, license_key, tier_name)

            return jsonify({"status": "SUCCESS", "license": license_key, "role": target_role, "recipient": customer_email}), 200

        return jsonify({"status": "IGNORED"}), 200
    except Exception as ex:
        return jsonify({"status": "ERROR", "message": str(ex)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ONLINE", "gateway": "HVF Payment Dispatcher v1.1"}), 200

if __name__ == "__main__":
    ensure_db()
    app.run(host="0.0.0.0", port=5000)