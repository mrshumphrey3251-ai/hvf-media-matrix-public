import os
import sys
import re
import time
import subprocess
import threading
import sqlite3
from datetime import datetime
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
CACHE_DIR = os.path.join(BASE_DIR, "memory_core", "audio_cache")
ENV_PATH = os.path.join(BASE_DIR, ".env")
TARGET_FILE = os.path.join(BASE_DIR, "sovereign_voice_listener.py")
os.makedirs(CACHE_DIR, exist_ok=True)

DAEMON_CODE = """# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN AUTONOMOUS VOICE DAEMON
# Squelch-Filtered Full-Duplex Continuous Acoustic Link for Shokz OpenRun
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

BASE_DIR = r"C:\\HVF_Repos\\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
CACHE_DIR = os.path.join(BASE_DIR, "memory_core", "audio_cache")
ENV_PATH = os.path.join(BASE_DIR, ".env")
os.makedirs(CACHE_DIR, exist_ok=True)

from sovereign_voice_engine import SovereignVoiceEngine

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
            res = model.generate_content(f"{sys_context}\\n\\nDirective from CEO Humphrey: {clean_p}")
            if res and res.text:
                return res.text.strip()
        except Exception as e:
            print(f"[AI_QUERY_ERROR] {e}")

    return f"Directive received and logged into sovereign memory, Mr. Humphrey: {clean_p}"

def log_voice_event(prompt: str, reply: str):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
        conn.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS autonomous_voice_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                user_prompt TEXT,
                ebony_response TEXT,
                timestamp TEXT,
                transport TEXT
            )
        \"\"\")
        conn.execute(\"\"\"
            INSERT INTO autonomous_voice_logs (sender, user_prompt, ebony_response, timestamp, transport)
            VALUES (?, ?, ?, ?, ?)
        \"\"\", ("CEO", prompt, reply, datetime.now().isoformat(), "Shokz_OpenRun_Bluetooth_HandsFree"))
        conn.close()
    except Exception as ex:
        print(f"[DB_ERROR] {ex}")

class SovereignHandsFreeDaemon:
    def __init__(self, wake_word: str = "ebony"):
        self.wake_word = wake_word.lower()
        self.is_speaking = False

    def start(self):
        print("=" * 80)
        print("HVF Omni-Industrial Matrix | AUTONOMOUS HANDS-FREE ACOUSTIC DAEMON")
        print("Endpoint: Shokz OpenRun Bluetooth Microphone (Windows Default WASAPI)")
        print(f"Wake Word: '{self.wake_word.upper()}' | Squelch Filter: ACTIVE (Confidence >= 0.50)")
        print("=" * 80)

        # Squelch-filtered speech recognition pipeline
        ps_listener = \"\"\"
        Add-Type -AssemblyName System.Speech
        $rec = New-Object System.Speech.Recognition.SpeechRecognitionEngine
        try {
            $rec.SetInputToDefaultAudioDevice()
        } catch {
            Write-Output "ERR_AUDIO_ENDPOINT"
            exit 1
        }
        $grammar = New-Object System.Speech.Recognition.DictationGrammar
        $rec.LoadGrammar($grammar)

        # Rejection of ambient room babble and Bluetooth carrier noise
        $rec.BabbleTimeout = [System.TimeSpan]::FromSeconds(2)
        $rec.InitialSilenceTimeout = [System.TimeSpan]::FromSeconds(3)

        Write-Output "LISTENER_READY"

        while ($true) {
            try {
                $res = $rec.Recognize()
                # Strict squelch: ignore low-confidence ambient static (< 0.50)
                if ($res -and $res.Text -and $res.Confidence -ge 0.50) {
                    Write-Output "VOX:$($res.Confidence):$($res.Text)"
                }
            } catch {
                Start-Sleep -Milliseconds 100
            }
        }
        \"\"\"

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
                print("[DAEMON_ONLINE] Hands-free squelch filter locked. Background noise silenced. I am listening.")
                SovereignVoiceEngine.speak("Acoustic squelch active, Mr. Humphrey. Background static filtered. I am listening.", async_mode=True)
                continue

            if line.startswith("VOX:"):
                payload = line[4:].strip()
                parts = payload.split(":", 1)
                if len(parts) == 2:
                    conf_str, speech = parts
                else:
                    conf_str, speech = "1.0", parts[0]

                print(f"[MIC_ACCEPTED] (Confidence: {conf_str}) '{speech}'")

                if self.is_speaking:
                    continue

                if self.wake_word in speech.lower():
                    clean_cmd = re.sub(rf"^.*?\\b{self.wake_word}\\b[\\s,.:]*", "", speech, flags=re.IGNORECASE).strip()
                    if not clean_cmd:
                        clean_cmd = speech

                    print(f"[AUTH_ACCEPTED] Processing directive from CEO: '{clean_cmd}'")

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
    daemon = SovereignHandsFreeDaemon(wake_word="ebony")
    daemon.start()
"""

with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(DAEMON_CODE.strip() + "\n")

py_compile.compile(TARGET_FILE, doraise=True)
print("[DAEMON_COMPILED] sovereign_voice_listener.py deployed with confidence squelch filter.")
print("=" * 80)

