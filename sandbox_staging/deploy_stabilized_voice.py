import os
import sys
import re
import base64
import subprocess
import threading
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
VOICE_FILE = os.path.join(BASE_DIR, "sovereign_voice_engine.py")

print("=" * 80)
print("HVF Omni-Industrial Matrix | STABILIZED VOICE SYNTHESIS ENGINE")
print("Target: Elimination of Bluetooth DAC Fade & String Collision Faults")
print("=" * 80)

VOICE_CODE = """# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN VOICE SYNTHESIS ENGINE
# Low-Latency Native Hardware Acoustic Output Subsystem
# Authority: Mr. Humphrey (Founder & CEO) | DFARS 252.227-7018 Compliant
# ==============================================================================
import os
import re
import base64
import subprocess
import threading

BASE_DIR = r"C:\\HVF_Repos\\hvf-media-matrix-private"

class SovereignVoiceEngine:
    \"\"\"
    High-performance on-device speech synthesis engine.
    Drives physical workstation audio / Bluetooth OpenRun directly via Windows SAPI
    with zero external cloud dependencies or API keys.
    \"\"\"
    _lock = threading.Lock()

    @staticmethod
    def _clean_text(text: str) -> str:
        # Strip markdown syntax, code blocks, and formatting
        clean = re.sub(r"```.*?```", " code block omitted ", text, flags=re.DOTALL)
        clean = re.sub(r"`.*?`", "", clean)
        clean = re.sub(r"[#*_~>\[\]\(\)]", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        # Escape XML entities for SSML compliance
        clean = clean.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")
        return clean

    @classmethod
    def speak(cls, text: str, gender: str = "Female", rate: int = 1, volume: int = 100, async_mode: bool = True):
        if not text or not text.strip():
            return

        clean = cls._clean_text(text)
        if not clean:
            return

        # 350ms SSML Pre-Roll wake-up pad: wakes the OpenRun Bluetooth DAC before speech begins
        ssml_payload = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><break time='350ms'/>{clean}</speak>"
        b64_ssml = base64.b64encode(ssml_payload.encode("utf-8")).decode("utf-8")

        def _worker():
            with cls._lock:
                ps_script = f\"\"\"
                Add-Type -AssemblyName System.Speech
                $raw = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{b64_ssml}'))$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
                try {{
                    $synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::{gender})
                }} catch {{}}
                $synth.Rate = {rate}
                $synth.Volume = {volume}$synth.SpeakSsml($raw)$synth.Dispose()
                \"\"\"
                subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                    capture_output=True,
                    timeout=15
                )

        if async_mode:
            threading.Thread(target=_worker, daemon=True).start()
        else:
            _worker()

    @classmethod
    def vocalize_response(cls, response_text: str):
        if not response_text or not response_text.strip():
            return
        cls.speak(response_text, gender="Female", rate=1, volume=100, async_mode=True)
"""

with open(VOICE_FILE, "w", encoding="utf-8") as f:
    f.write(VOICE_CODE.strip() + "\n")

py_compile.compile(VOICE_FILE, doraise=True)
print("[SUCCESS] sovereign_voice_engine.py deployed with Base64 transport and SSML pre-roll.")

# Calibration audio test
from sovereign_voice_engine import SovereignVoiceEngine
test_phrase = "Acoustic calibration complete, Mr. Humphrey. Volume ramp stabilized."
SovereignVoiceEngine.speak(test_phrase, async_mode=False)
print(f"[SUCCESS] Calibration audio sent to OpenRun: '{test_phrase}'")
print("=" * 80)

