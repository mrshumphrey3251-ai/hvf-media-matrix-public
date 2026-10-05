import requests, toml
try:
    sec = toml.load(r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml")
    key = sec.get("GROQ_API_KEY", "").strip()
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "Test"}]}
    print("[*] Firing direct payload to Groq Cloud...")
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10)
    print(f"[+] HTTP STATUS: {res.status_code}")
    print(f"[+] RAW RESPONSE: {res.text}")
except Exception as e:
    print(f"[-] FATAL PERIMETER BLOCK: {e}")
