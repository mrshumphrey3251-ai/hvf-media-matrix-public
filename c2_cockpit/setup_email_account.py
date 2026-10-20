"""
E.B.O.N.Y. Zero-API Email Account Onboarding CLI
Direct Username + Password / App Password Ingestion & Handshake Verification
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import sys
import argparse
from pathlib import Path

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
sys.path.insert(0, str(cockpit_dir))

from ebony_email_dispatcher import save_account_credentials, test_account_connection, detect_servers

def onboard_account(email_addr: str, password: str, test_online: bool = True):
    print(f"[*] Ingesting credentials for: {email_addr}")
    imap_h, smtp_h, i_p, s_p = detect_servers(email_addr)
    print(f"[*] Auto-detected endpoints: IMAP={imap_h}:{i_p} | SMTP={smtp_h}:{s_p}")

    if test_online:
        print("[*] Probing live TLS/SSL IMAP socket (Port 993)...")
        success, msg = test_account_connection(email_addr, password, imap_h)
        if success:
            print("[+] Socket authentication: SUCCESSFUL. Mailbox verified.")
        else:
            print(f"[!] Live probe response: {msg}")
            print("[*] Staging credentials locally for operational execution.")

    save_account_credentials(email_addr, password, imap_h, smtp_h)
    print(f"[+] Account '{email_addr}' committed to email_accounts.json.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E.B.O.N.Y. Email Account Onboarding")
    parser.add_argument("--email", type=str, help="Email address to onboard")
    parser.add_argument("--password", type=str, help="Standard password or 16-character App Password")
    parser.add_argument("--skip-test", action="store_true", help="Skip live IMAP probe")
    args = parser.parse_args()

    if args.email and args.password:
        onboard_account(args.email, args.password, test_online=not args.skip_test)
    else:
        print("\n=== E.B.O.N.Y. INTERACTIVE EMAIL ONBOARDING ===")
        in_email = input("Enter Email Address: ").strip()
        in_pass = input("Enter Password / 16-Char App Password: ").strip()
        if in_email and in_pass:
            onboard_account(in_email, in_pass, test_online=not args.skip_test)
        else:
            print("[!] Onboarding aborted: Email and password are required.")