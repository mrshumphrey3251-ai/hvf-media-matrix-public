import imaplib
import sys
import getpass

# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN IMAP DIAGNOSTIC PROBE
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# Target: humphreyvirtualfarm@gmail.com (Direct IMAP Handshake Isolation)
# ==============================================================================

EMAIL_ADDR = "humphreyvirtualfarm@gmail.com"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

print("=" * 80)
print(f"HVF SOVEREIGN IMAP DIAGNOSTIC PROBE: {EMAIL_ADDR}")
print("=" * 80)

raw_token = getpass.getpass("Enter or Paste 16-Character App Password (input hidden): ")

# Normalize: strip spaces, newlines, tabs
clean_token = raw_token.replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "").strip()

print(f"\n[TELEMETRY] Raw Input Length:        {len(raw_token)} characters")
print(f"[TELEMETRY] Normalized Token Length:  {len(clean_token)} characters")

if len(clean_token) != 16:
    print(f"\n[WARN] Token length is {len(clean_token)}. Standard Google App Passwords are exactly 16 letters.")
    print("       Ensure you are not entering your standard Google sign-in password.")

print(f"\nInitiating TLS/SSL connection to {IMAP_SERVER}:{IMAP_PORT}...")

try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    print("[SUCCESS] TLS socket connected and SSL handshake completed.")
    
    print(f"Attempting authentication for {EMAIL_ADDR}...")
    mail.login(EMAIL_ADDR, clean_token)
    print("\n" + "*" * 80)
    print("[SUCCESS] AUTHENTICATION GRANTED BY GOOGLE.")
    print("*" * 80)
    
    status, count = mail.select("INBOX")
    print(f"[STATUS] INBOX selected. Total messages on server: {count[0].decode()}")
    
    mail.logout()
    print("\n" + "=" * 80)
    print("STATUS: CREDENTIALS ARE 100% VALID AND OPERATIONAL")
    print("=" * 80)
    
except imaplib.IMAP4.error as e:
    print(f"\n[FAIL] Google IMAP Rejection: {e}")
    print("\nActionable Root Causes:")
    print("1. Account mismatch: The App Password was generated on a different Google Account.")
    print("2. Token typo: Verify the 16 characters match the generated key exactly.")
    print("3. Password type: Ensure this is the App Password and NOT your master Google account password.")
    print("=" * 80)
except Exception as ex:
    print(f"\n[FAIL] Unexpected network or socket error: {ex}")
    print("=" * 80)

