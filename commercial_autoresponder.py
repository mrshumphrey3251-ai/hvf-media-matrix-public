import imaplib
import smtplib
import email
import os
from email.mime.text import MIMEText

EMAIL_ACCT = "humphreyvirtualfarm@gmail.com"
APP_PASS = os.environ.get("GMAIL_APP_PASSWORD")

def process_inquiries():
    print("[HVF SYSTEM] Scanning inbox for commercial inquiries...")
    if not APP_PASS:
        print("[!] ERROR: GMAIL_APP_PASSWORD not set. Export it before running.")
        return
        
    try:
        # Secure IMAP Connection (Read)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_ACCT, APP_PASS)
        mail.select('inbox')
        
        # Hunt for exact subject line matches that are UNREAD
        status, messages = mail.search(None, '(UNSEEN SUBJECT "[COMMERCIAL INQUIRY] Project Ebony License Acquisition")')
        mail_ids = messages[0].split()
        
        if not mail_ids:
            print("[-] No new commercial inquiries detected. Standing by.")
            return

        # Secure SMTP Connection (Send)
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_ACCT, APP_PASS)

        for i in mail_ids:
            res, msg_data = mail.fetch(i, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = msg['From']
                    print(f"[*] Processing inquiry from: {sender}")
                    
                    # Executive Response Payload
                    reply_body = (
                        "Entity Acknowledged.\n\n"
                        "Your commercial inquiry regarding the Project Ebony architecture has been received by the HVF Intelligence Grid. "
                        "The Chief Architect is currently reviewing your deployment scale and sector parameters.\n\n"
                        "You will be contacted shortly with the executive terms of acquisition. Until authorization is explicitly granted, "
                        "the architecture remains strictly under the HVF Enterprise-Audit License.\n\n"
                        "Jeffery Humphrey\nChief Architect / CEO\nHumphrey Virtual Farm"
                    )
                    
                    reply = MIMEText(reply_body)
                    reply['Subject'] = f"Re: {msg['Subject']}"
                    reply['From'] = EMAIL_ACCT
                    reply['To'] = sender
                    
                    # Fire the response
                    smtp.send_message(reply)
                    print(f"    [+] Executive auto-response dispatched to {sender}")
        
        smtp.quit()
        mail.logout()
        print("[HVF SYSTEM] All commercial inquiries processed and locked.")
        
    except Exception as e:
        print(f"[!] System Error: {e}")

if __name__ == "__main__":
    process_inquiries()
