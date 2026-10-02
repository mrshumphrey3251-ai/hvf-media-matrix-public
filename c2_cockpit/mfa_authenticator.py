import time
from mfa_matrix import generate_sovereign_token

def run_authenticator():
    print("\n==================================================")
    print("[*] SOVEREIGN AUTHENTICATOR // TIER-1 SECURE")
    print("==================================================")
    print("Leave this terminal open to view your live cryptographic tokens.\n")
    try:
        while True:
            token = generate_sovereign_token()
            print(f"\r[+] ACTIVE MFA TOKEN: {token} (Regenerates every 30s)    ", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[*] AUTHENTICATOR OFFLINE.")

if __name__ == "__main__":
    run_authenticator()
