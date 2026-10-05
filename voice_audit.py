import toml, requests
try:
    path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
    sec = toml.load(path)
    key = sec.get("ELEVENLABS_API_KEY", "").strip()
    if not key or "YOUR_" in key:
        print("[-] FATAL: ELEVENLABS_API_KEY is missing or invalid in the vault.")
    else:
        headers = {"xi-api-key": key}
        print("[*] Firing direct payload to ElevenLabs Neural Voice API...")
        res = requests.get("https://api.elevenlabs.io/v1/user", headers=headers, timeout=10)
        if res.status_code == 200:
            print("[+] VOCAL MATRIX STRIKE SUCCESSFUL. ElevenLabs credential is live and unrestricted.")
        else:
            print(f"[-] VOCAL MATRIX FAILED. HTTP {res.status_code}: {res.text}")
except Exception as e:
    print(f"[-] SYSTEM ERROR: {e}")
