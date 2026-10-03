import logging
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# HVF Media Matrix - Email API Node (Private/Unredacted)
# Engineered for secure SMTP outbound transmission

class HVFEmailNode:
    def __init__(self):
        self.logger = logging.getLogger("HVF_Email_Node")
        # Pierce the local vault
        load_dotenv()
        self.sender_email = os.getenv("GMAIL_USER")
        self.app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.target_address = "humphreyvirtualfarm@gmail.com"

    def dispatch(self, payload):
        self.logger.info(f"Initializing SMTP transmission vector for: {self.target_address}")
        
        if not self.sender_email or self.app_password == "PLACEHOLDER_AWAITING_LIVE_KEY":
            self.logger.warning("SMTP Aborted: Live transmission keys not detected in vault. Standing by.")
            return False

        try:
            msg = EmailMessage()
            msg.set_content(payload)
            msg['Subject'] = 'HVF Media Matrix - Live Intel Payload'
            msg['From'] = self.sender_email
            msg['To'] = self.target_address

            # Secure connection to Gmail SMTP
            self.logger.info("Establishing secure SSL connection to SMTP gateway...")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)
            
            self.logger.info("Payload successfully dispatched to target.")
            return True
        except Exception as e:
            self.logger.error(f"SMTP Transmission Failed: {e}")
            return False
