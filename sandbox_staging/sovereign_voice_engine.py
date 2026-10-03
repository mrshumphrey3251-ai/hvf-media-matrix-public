import os
import re
import base64
import subprocess
import threading

class SovereignVoiceEngine:
    _lock = threading.Lock()

    @classmethod
    def vocalize_response(cls, response_text: str):
        if not response_text: return
        
        # Clean text for speech (strip complex markdown that breaks the synthesizer)
        text = re.sub(r"[#*_~>\[\]\(\)]", " ", response_text)
        text = text.replace('"', '').replace("'", "")
        text = re.sub(r"\s+", " ", text).strip()

        b64 = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Synchronous Execution: Forces Python to wait until speech completes
        with cls._lock:
            ps = f"""
            Add-Type -AssemblyName System.Speech
            $bytes = [System.Convert]::FromBase64String('{b64}')
            $text = [System.Text.Encoding]::UTF8.GetString($bytes)
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
            try {{ $synth.SelectVoiceByHints('Female') }} catch {{}}
            $synth.Speak($text)
            $synth.Dispose()
            """
            subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps])
