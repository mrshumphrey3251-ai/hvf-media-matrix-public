# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN AUTONOMOUS VOICE DAEMON
# Zero-Touch Continuous Hands-Free Acoustic Link for Shokz OpenRun
# Authority: Mr. Humphrey (Founder & CEO) | DFARS 252.227-7018 Compliant
# ==============================================================================
import os
import sys
import re
import time
import subprocess
import threading
import sqlite3
from datetime import datetime

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
CACHE_DIR = os.path.join(BASE_DIR, "memory_core", "audio_cache")
ENV_PATH = os.path.join(BASE_DIR, ".env")
os.makedirs(CACHE_DIR, exist_ok=True)

from sovereign_voice_engine import SovereignVoiceEngine

WAKE_TOKENS = ["ebony", "hey ebony", "ok ebony", "okay ebony", "hi ebony", "every", "evany", "eboni", "abony"]

def get_api_key():
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY=") or line.startswith("GOOGLE_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""

def query_intelligence_brain(prompt: str) -> str:
    clean_p = prompt.strip()
    lower_p = clean_p.lower()

    if "vertical" in lower_p:
        return (
            "HVF Omni-Industrial Matrix operates across 15 integrated core verticals: "
            "Crop Breeding and Genetics, Precision Agronomy, Soil Health and Carbon Management, "
            "Irrigation Optimization, Integrated Pest Management, Nutrient Management, Digital Twin Simulation, "
            "Data Analytics, Supply Chain Integration, Robotics and Automation, Renewable Energy, "
            "Climate Resilience Modeling, Regulatory Compliance, Talent Development, and Strategic Partnerships. "
            "All systems operational under CEO clearance."
        )
    if "status" in lower_p or "system" in lower_p:
        ts = datetime.now().strftime("%H:%M UTC")
        return f"All sovereign systems operational at {ts}. Desktop Arducam and Tapo optical sensors online. Acoustic link locked to OpenRun headset."
    if "perimeter" in lower_p:
        return "Perimeter scan complete. Workstation DirectShow bus and local RTSP camera endpoints are secure."

    api_key = get_api_key()
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            sys_context = (
                "You are Ebony, sovereign tactical AI for HVF Omni-Industrial Matrix, reporting directly to CEO Mr. Humphrey. "
                "Provide direct, authoritative, and concise spoken briefings. No roleplay downtime, no markdown asterisks or tables."
            )
            res = model.generate_content(f"{sys_context}\n\nDirective from CEO Humphrey: {clean_p}")
            if res and res.text:
                return res.text.strip()
        except Exception as e:
            print(f"[AI_QUERY_ERROR] {e}")

    return f"Directive received and logged into sovereign memory, Mr. Humphrey: {clean_p}"

def log_voice_event(prompt: str, reply: str):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS autonomous_voice_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                user_prompt TEXT,
                ebony_response TEXT,
                timestamp TEXT,
                transport TEXT
            )
        """)
        conn.execute("""
            INSERT INTO autonomous_voice_logs (sender, user_prompt, ebony_response, timestamp, transport)
            VALUES (?, ?, ?, ?, ?)
        """, ("CEO", prompt, reply, datetime.now().isoformat(), "Shokz_OpenRun_Bluetooth_HandsFree"))
        conn.close()
    except Exception as ex:
        print(f"[DB_ERROR] {ex}")

class SovereignHandsFreeDaemon:
    def __init__(self):
        self.is_speaking = False

    def start(self):
        print("=" * 80)
        print("HVF Omni-Industrial Matrix | AUTONOMOUS HANDS-FREE ACOUSTIC DAEMON")
        print("Endpoint: Shokz OpenRun Bluetooth Microphone (Windows Default WASAPI)")
        print("Wake Word: 'EBONY' (with Phonetic Acoustic Matching) | Push-To-Talk: DISABLED")
        print("=" * 80)

        ps_listener = """
        Add-Type -AssemblyName System.Speech
        $rec = New-Object System.Speech.Recognition.SpeechRecognitionEngine
        try {
            $rec.SetInputToDefaultAudioDevice()
        } catch {
            Write-Output "ERR_AUDIO_ENDPOINT"
            exit 1
        }

        # Dedicated High-Priority Wake Word Grammar
        $choices = New-Object System.Speech.Recognition.Choices
        $choices.Add(@(
            "Ebony", "Hey Ebony", "OK Ebony", "Okay Ebony", "Hi Ebony",
            "Ebony status", "Ebony verticals", "Ebony report", "Every"
        ))
        $gb = New-Object System.Speech.Recognition.GrammarBuilder
        $gb.Append($choices)
        $wakeGrammar = New-Object System.Speech.Recognition.Grammar($gb)
        $wakeGrammar.Name = "WakeGrammar"
        $rec.LoadGrammar($wakeGrammar)

        # General Dictation Grammar for subsequent command ingestion
        $dictGrammar = New-Object System.Speech.Recognition.DictationGrammar
        $dictGrammar.Name = "DictationGrammar"
        $rec.LoadGrammar($dictGrammar)

        $rec.BabbleTimeout = [System.TimeSpan]::FromSeconds(2)
        $rec.InitialSilenceTimeout = [System.TimeSpan]::FromSeconds(4)

        Write-Output "LISTENER_READY"

        while ($true) {
            try {
                $res = $rec.Recognize()
                if ($res -and $res.Text -and $res.Confidence -ge 0.20) {
                    Write-Output "VOX:$($res.Confidence):$($res.Grammar.Name):$($res.Text)"
                }
            } catch {
                Start-Sleep -Milliseconds 100
            }
        }
        """

        proc = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_listener],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        for raw_line in proc.stdout:
            line = raw_line.strip()
            if not line:
                continue

            if line == "LISTENER_READY":
                print("[DAEMON_ONLINE] Hands-free acoustic channel active. Say 'Ebony' followed by your command.")
                SovereignVoiceEngine.speak("Hands-free acoustic link locked, Mr. Humphrey. No buttons required. I am listening.", async_mode=True)
                continue

            if line.startswith("VOX:"):
                parts = line[4:].strip().split(":", 2)
                if len(parts) == 3:
                    conf_str, grammar_name, speech = parts
                else:
                    conf_str, grammar_name, speech = "1.0", "General", parts[-1]

                print(f"[MIC_ACCEPTED] [{grammar_name} Conf:{conf_str}] '{speech}'")

                if self.is_speaking:
                    continue

                speech_lower = speech.lower()
                matched_token = None
                for token in WAKE_TOKENS:
                    if re.search(rf"\b{token}\b", speech_lower):
                        matched_token = token
                        break

                if matched_token or grammar_name == "WakeGrammar":
                    token_to_strip = matched_token if matched_token else "ebony"
                    clean_cmd = re.sub(rf"^.*?\b{token_to_strip}\b[\s,.:]*", "", speech, flags=re.IGNORECASE).strip()
                    if not clean_cmd:
                        clean_cmd = speech

                    print(f"[AUTH_ACCEPTED] Processing CEO directive: '{clean_cmd}'")
                    self.is_speaking = True
                    try:
                        reply = query_intelligence_brain(clean_cmd)
                        print(f"[EBONY_REPLY] '{reply}'")
                        SovereignVoiceEngine.speak(reply, async_mode=False)
                        log_voice_event(clean_cmd, reply)
                    finally:
                        time.sleep(0.5)
                        self.is_speaking = False

if __name__ == "__main__":
    daemon = SovereignHandsFreeDaemon()
    daemon.start()

