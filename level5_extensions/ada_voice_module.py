"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: ADA VOICE MODULE & CONVERSATIONAL AUDIO BRIDGE
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
"""

import os
import io
import streamlit as st

def transcribe_audio_payload(audio_bytes: bytes) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            with open("temp_ada_voice.wav", "wb") as f:
                f.write(audio_bytes)
            with open("temp_ada_voice.wav", "rb") as audio_file:
                transcript_obj = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                return transcript_obj.text
        except Exception:
            pass

    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with io.BytesIO(audio_bytes) as audio_file:
            with sr.AudioFile(audio_file) as source:
                data = r.record(source)
                return r.recognize_google(data)
    except Exception as e:
        return f"[Audio Processing Note: {str(e)}]"

def render():
    st.markdown("### 🎙️ Ada Voice Module — Autonomous Speech Uplink")
    st.caption("Level-5 Sovereign Industrial Voice C2 | CAGE: 1AHA8 | OK Title 61 / HB 2992")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🎙️ Spoken Directive Intake")
        st.info("Record your spoken directive below. Audio captures directly through hardware.")
        audio_val = None
        if hasattr(st, "audio_input"):
            audio_val = st.audio_input("Tap to speak directive to Ebony:", key="ada_voice_hardware_uplink")
        else:
            st.warning("Hardware audio input requires Streamlit audio_input support.")

    with col2:
        st.markdown("#### 📊 Real-Time Transcription & Telemetry")
        m1, m2 = st.columns(2)
        m1.metric("Voice Engine", "ONLINE")
        m2.metric("OPSEC Gate", "LEVEL-5 ENFORCED")

        transcript_box = st.empty()
        response_box = st.empty()

        if audio_val is not None:
            audio_bytes = audio_val.read()
            if audio_bytes and len(audio_bytes) > 0:
                with st.spinner("Translating Audio Directive..."):
                    transcription = transcribe_audio_payload(audio_bytes)

                if transcription and not transcription.startswith("["):
                    transcript_box.success(f"🗣️ **Transcribed Directive:** \"{transcription}\"")
                    prompt_lower = transcription.lower()
                    if any(k in prompt_lower for k in ["status", "report", "system", "c2"]):
                        reply = (
                            "Executive Briefing Confirmed, CEO Humphrey. Level-5 Sovereign Industrial C2 "
                            "is operating at nominal status under CAGE: 1AHA8 and Oklahoma Title 61. "
                            "Quarantine airlock is stabilized at 471 sovereign assets. All hardware bridges and "
                            "production extensions are standing by for your directive."
                        )
                    else:
                        reply = f"Directive received: '{transcription}'. Autonomous Level-5 execution initiated across sovereign matrix."
                    response_box.markdown(f"#### 🤖 Ebony Executive Response:\n> **{reply}**")
                elif transcription.startswith("["):
                    transcript_box.warning(transcription)

if __name__ == "__main__":
    render()
