"""
PROJECT EBONY: SOVEREIGN COMMUNICATIONS & INFERENCE ENGINE
ROLE: Resilient text cognition, multi-provider fallback, and ElevenLabs voice delivery.
"""

import os
import sys
import toml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRETS_PATH = BASE_DIR / ".streamlit" / "secrets.toml"

def get_secret(key_name: str) -> str:
    # Check OS environment first
    val = os.environ.get(key_name)
    if val:
        return val
    # Check secrets.toml
    if SECRETS_PATH.exists():
        try:
            sec = toml.load(SECRETS_PATH)
            return sec.get(key_name, "")
        except Exception:
            pass
    return ""

def generate_chat_response(prompt: str, conversation_history: list = None) -> str:
    """Multi-tiered conversational inference with zero-lockup fallback."""
    groq_key = get_secret("GROQ_API_KEY")
    gemini_key = get_secret("GEMINI_API_KEY")

    # 1. Attempt Groq with resilient model cascade
    if groq_key and not groq_key.startswith("YOUR_"):
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            # Try available Groq standard models in order
            for model_id in ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"]:
                try:
                    resp = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are Ebony, Sovereign Executive Technical Partner to the CEO. Authoritative, precise, zero filler."},
                            {"role": "user", "content": prompt}
                        ],
                        model=model_id,
                        timeout=8.0
                    )
                    return resp.choices[0].message.content.strip()
                except Exception:
                    continue
        except Exception as e:
            pass

    # 2. Attempt Google Gemini if configured
    if gemini_key and not gemini_key.startswith("YOUR_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception:
            pass

    # 3. Sovereign Safe Mode Response (System never freezes or stays mute)
    return (
        f"[SOVEREIGN SAFE-STATE] Directive acknowledged: '{prompt[:40]}...'. "
        "External inference cloud models are unprovisioned or timed out. "
        "Ring 0 core and Sandbox operations remain fully operational."
    )

def synthesize_speech_elevenlabs(text_to_speak: str) -> bytes:
    """Generate voice audio stream using ElevenLabs API."""
    api_key = get_secret("ELEVENLABS_API_KEY")
    voice_id = get_secret("ELEVENLABS_VOICE_ID") or "FGY2WhTYpPnrIDTdsKH5"

    if not api_key or api_key.startswith("YOUR_"):
        return None

    try:
        import requests
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": text_to_speak,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            print(f"[-] ElevenLabs error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[-] ElevenLabs synthesis exception: {e}")
        return None

if __name__ == "__main__":
    print("[*] Testing Sovereign Communications Portal...")
    test_out = generate_chat_response("System status report.")
    print(f"[+] Output: {test_out}")

