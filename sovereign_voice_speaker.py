"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: SOVEREIGN ACOUSTIC SYNTHESIS WORKER (COREAUDIO / SAPI)
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
"""

import sys
import re

def synthesize_speech(text: str):
    if not text or not text.strip():
        return
    
    # Strip markdown and excessive symbols for smooth vocal delivery
    clean_text = re.sub(r'[*_#>`~\[\]\(\)]', ' ', text).strip()
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # Tier 1: Local pyttsx3 Engine (SAPI5 Native)
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        voices = engine.getProperty('voices')
        for v in voices:
            if any(k in v.name.lower() for k in ['zira', 'female', 'eva', 'cortana']):
                engine.setProperty('voice', v.id)
                break
        engine.say(clean_text)
        engine.runAndWait()
        return
    except Exception:
        pass

    # Tier 2: Synchronous Windows SAPI via COM (Runs to completion in this worker process)
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(clean_text, 0)
        return
    except Exception:
        pass

    # Tier 3: Windows System.Speech via PowerShell
    try:
        import subprocess
        clean_safe = clean_text.replace('"', '').replace("'", "")
        ps_inline = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{clean_safe}")'
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_inline], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        phrase = " ".join(sys.argv[1:])
        synthesize_speech(phrase)