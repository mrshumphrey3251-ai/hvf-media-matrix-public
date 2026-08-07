import os
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("[HVF SYSTEM] Initializing Sovereign Gmail Dispatch Engine...")

app_password = os.environ.get("GMAIL_APP_PASSWORD")
sender_email = "humphreyvirtualfarm@gmail.com"

if not app_password:
    print("[HVF ERROR] GMAIL_APP_PASSWORD not found in environment.")
    exit(1)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, app_password)
except Exception as e:
    print(f"[HVF NETWORK ERROR] Authentication failed: {e}")
    exit(1)

for filepath in glob.glob("OUTBOX/*_payload.txt"):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    to_line = lines[0].strip()
    subject_line = lines[1].strip()
    body = "".join(lines[3:])
    
    email_vector = to_line.split("<")[1].split(">")[0]
    subject = subject_line.replace("Subject: ", "")
    
    msg = MIMEMultipart()
    msg['From'] = f"Jeffery Humphrey <{sender_email}>"
    msg['To'] = email_vector
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server.send_message(msg)
        print(f" -> [200 OK] {filepath} securely routed to {email_vector} via Gmail TLS.")
    except Exception as e:
        print(f" -> [HVF TRANSMISSION ERROR] Could not route {filepath}: {e}")

server.quit()
print("[HVF SYSTEM] Delivery cycle complete. Target inboxes breached.")
