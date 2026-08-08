import imaplib, smtplib, email, os
from email.mime.text import MIMEText
EMAIL_ACCT = "humphreyvirtualfarm@gmail.com"
APP_PASS = os.environ.get("GMAIL_APP_PASSWORD")
IGNORE_LIST = ["mailer-daemon", "postmaster", "no-reply", EMAIL_ACCT.lower()]

def process_inquiries():
    print("[HVF SYSTEM] Scanning inbox...")
    if not APP_PASS: return
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_ACCT, APP_PASS)
        mail.select('inbox')
        q = '(UNSEEN SUBJECT "[COMMERCIAL INQUIRY] Project Ebony License Acquisition")'
        status, msgs = mail.search(None, q)
        mail_ids = msgs[0].split()
        if not mail_ids: return
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_ACCT, APP_PASS)
        for i in mail_ids:
            res, data = mail.fetch(i, '(RFC822)')
            for p in data:
                if isinstance(p, tuple):
                    msg = email.message_from_bytes(p[1])
                    sender = msg['From']
                    if any(ig in sender.lower() for ig in IGNORE_LIST): continue
                    rb = "Entity Acknowledged.\n\nProject Ebony inquiry received. The Chief Architect is reviewing parameters.\n\nJeffery Humphrey\nCEO"
                    reply = MIMEText(rb)
                    reply['Subject'] = f"Re: {msg['Subject']}"
                    reply['From'], reply['To'] = EMAIL_ACCT, sender
                    smtp.send_message(reply)
        smtp.quit(); mail.logout()
    except Exception as e: print(f"[!] Error: {e}")
if __name__ == "__main__": process_inquiries()
