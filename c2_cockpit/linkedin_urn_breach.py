import os
import requests
from dotenv import load_dotenv

# Bypass cache and read the current .env
load_dotenv(override=True)
token = os.getenv("LINKEDIN_ACCESS_TOKEN")

print("\n[EBONY RECON]: Initiating versioned secure breach...")

if not token:
    print("[EBONY RECON]: FAILED. Access token is missing.")
else:
    url_me = "https://api.linkedin.com/v2/me"
    url_userinfo = "https://api.linkedin.com/v2/userinfo"
    
    # Injecting the mandatory version stamps to bypass the 403 firewall
    headers = {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": "202401",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    try:
        # Tactic 1: Standard API Breach
        res = requests.get(url_me, headers=headers)
        if res.status_code == 200:
            urn = f"urn:li:person:{res.json()['id']}"
        else:
            # Tactic 2: OpenID Connect Fallback
            res = requests.get(url_userinfo, headers=headers)
            if res.status_code == 200:
                urn = f"urn:li:person:{res.json()['sub']}"
            else:
                urn = None
                print(f"[EBONY RECON]: Breach Failed. Target Defended.")
                print(f"Error Code: {res.status_code} | Response: {res.text}")
        
        if urn:
            print(f"[EBONY RECON]: Target Acquired -> {urn}")
            with open(".env", "a", encoding="utf-8") as f:
                f.write(f"\nLINKEDIN_AUTHOR_URN={urn}\n")
            print("[EBONY RECON]: URN successfully hardcoded into the .env chamber.")
            
    except Exception as e:
        print(f"[EBONY RECON]: Critical System Misfire: {e}")
print("\n")
