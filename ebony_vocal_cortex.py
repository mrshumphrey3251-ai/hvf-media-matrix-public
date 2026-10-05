"""
HVF SOVEREIGN VOCAL CORTEX - LOCAL SYNTHESIS ENGINE
System: Project Ebony - Acoustic Rendering Subsystem
Compliance: Sovereign Air-Gap Local Execution
"""

import subprocess
import os
import re
import base64

DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ebony_audio.wav")

def clean_speech_text(text: str) -> str:
    """Strips Markdown syntax, asterisks, headers, and code blocks for clean phonetic delivery."""
    t = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    t = re.sub(r'[*#_`\[\]]', '', t)
    t = re.sub(r'\[.*?\]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def ignite_voice(text: str, output_file: str = None) -> str:
    """
    Sovereign Vocal Cortex: Zero-cost, 100% local speech synthesis.
    Renders safely to .wav via Base64 transport to prevent command-line parsing collisions.
    """
    if output_file is None:
        output_file = DEFAULT_OUTPUT

    spoken_text = clean_speech_text(text)
    if not spoken_text:
        return None

    try:
        print("[*] Engaging Sovereign Local Vocal Cortex (Rendering Audio Matrix)...")

        # Encode text and path to Base64 to make argument parsing immune to special characters
        b64_text = base64.b64encode(spoken_text.encode("utf-8")).decode("ascii")
        b64_path = base64.b64encode(os.path.abspath(output_file).encode("utf-8")).decode("ascii")

        ps_cmd = (
            f"$txt = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{b64_text}')); "
            f"$outPath = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{b64_path}')); "
            "Add-Type -AssemblyName System.Speech; "
            "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "$synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female); "
            "$synth.SetOutputToWaveFile($outPath); "
            "$synth.Speak($txt); "
            "$synth.Dispose();"
        )

        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            text=True
        )

        if res.returncode == 0 and os.path.exists(output_file):
            print(f"[+] SOVEREIGN VOCAL AUDIO SECURED: {output_file}")
            return output_file
        else:
            print(f"[-] VOCAL EXECUTION ERROR: {res.stderr}")
            return None
    except Exception as e:
        print(f"[-] VOCAL FAILOVER EXPOSED: {str(e)}")
        return None
