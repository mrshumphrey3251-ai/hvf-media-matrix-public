import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

print("[HVF NEXUS] Initiating Autonomous Briefing Delivery Protocol...")

SENDER = "humphreyvirtualfarm@gmail.com"
PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
RECEIVER = "humphreyvirtualfarm@gmail.com"

if not PASSWORD:
    print("[!] ERROR: GMAIL_APP_PASSWORD environment variable is missing. Halting transmission.")
    exit(1)

date_str = datetime.now().strftime('%Y%m%d')
report_name = f"Executive_Brief_{date_str}.md"
report_path = os.path.join(os.getcwd(), report_name)

if not os.path.exists(report_path):
    print(f"[!] ERROR: Briefing file {report_name} not found. Halting.")
    exit(1)

with open(report_path, 'r') as f:
    content = f.read()

msg = MIMEMultipart()
msg['From'] = SENDER
msg['To'] = RECEIVER
msg['Subject'] = f"[PROJECT EBONY] Executive Telemetry Briefing - {datetime.now().strftime('%Y-%m-%d')}"
msg.attach(MIMEText(content, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, RECEIVER, msg.as_string())
    server.quit()
    print(f"[HVF NEXUS] Executive Briefing successfully transmitted to {RECEIVER}.")
except Exception as e:
    print(f"[!] Transmission Failed: {e}")
