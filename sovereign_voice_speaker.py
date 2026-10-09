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
    clean_text = re.sub(r'[*_#>`~\[\]\(\)]', ' ', text).strip()
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # 1. Native Windows SAPI COM (Synchronous, guaranteed delivery to default sound card)
    try:
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(clean_text, 0)
        pythoncom.CoUninitialize()
        return
    except Exception:
        pass

    # 2. Local pyttsx3 fallback
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(clean_text)
        engine.runAndWait()
        return
    except Exception:
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        phrase = " ".join(sys.argv[1:])
        synthesize_speech(phrase)
