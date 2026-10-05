import toml, requests, os

def ignite_voice(text, filename="ebony_test.mp3"):
    try:
        path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
        sec = toml.load(path)
        key = sec.get("ELEVENLABS_API_KEY", "").strip()
        
        if not key:
            print("[-] VOCAL FAILOVER: Missing credential in vault.")
            return False
            
        print("[*] Engaging ElevenLabs Neural Voice Matrix...")
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {"xi-api-key": key, "Content-Type": "application/json"}
        payload = {
            "text": text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(res.content)
            print(f"[+] VOCAL STRIKE SUCCESSFUL. Audio file secured: {filename}")
            return True
        else:
            print(f"[-] VOCAL FAILOVER: API Blocked - HTTP {res.status_code}")
            return False
    except Exception as e:
        print(f"[-] VOCAL FAILOVER EXPOSED: {str(e)}")
        return False
        
if __name__ == "__main__":
    ignite_voice("The sovereign matrix is fully operational. I am Ebony, and all systems are running at Tier 1 speed.")
