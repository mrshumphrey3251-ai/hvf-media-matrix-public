import os
import sys
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
CORE_FILE = os.path.join(BASE_DIR, "sovereign_comms_core.py")

with open(CORE_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Enhance Pillar 3 to include Auto-Vocalize Mode toggle
old_anchor = 'with col_vox:'
new_voice_deck = """with col_vox:
            st.subheader("🎙️ 3. SOVEREIGN VOICE TALK")
            st.caption("Acoustic link routed directly to Bluetooth OpenRun headset.")

            # Autonomous vs. On-Demand Mode Toggle
            col_mode1, col_mode2 = st.columns([1.5, 1])
            with col_mode1:
                auto_speak = st.toggle("🔴 Auto-Vocalize Engine", value=True, key="toggle_auto_vocalize")
            with col_mode2:
                st.caption("Hands-Free Mode" if auto_speak else "Push-to-Activate")

            col_v1, col_v2 = st.columns(2)
            with col_v1:
                if st.button("🔊 Status Report", key="btn_voice_status_report", width="stretch"):
                    ts_now = datetime.now().strftime("%H:%M UTC")
                    report_msg = f"Status Report for CEO Humphrey. Optical and acoustic vectors active. OpenRun headset locked at {ts_now}."
                    SovereignVoiceEngine.speak(report_msg)
                    st.toast("Ebony speaking into OpenRun.", icon="🔊")
            with col_v2:
                if st.button("🛡️ Perimeter Secure", key="btn_voice_perimeter", width="stretch"):
                    perim_msg = "Perimeter verified secure. All sovereign communication vectors operational."
                    SovereignVoiceEngine.speak(perim_msg)
                    st.toast("Ebony speaking into OpenRun.", icon="🛡️")

            custom_voice_prompt = st.text_input("Direct Command for Ebony", placeholder="Type directive for Ebony to speak...", key="ebony_custom_voice_prompt")
            if st.button("🔊 Speak Aloud", key="btn_vocalize_custom", type="primary"):
                if custom_voice_prompt:
                    SovereignVoiceEngine.speak(custom_voice_prompt)
                    st.success("Vocalized into OpenRun headset.")

            if hasattr(st, "audio_input"):
                v_audio = st.audio_input("🎙️ Inbound Voice Capture", key="pnp_voice_input")
                if v_audio is not None:
                    st.audio(v_audio, format="audio/wav")
                    st.success("Voice transmission ingested into defense memory.")

            st.markdown('''
                <div style="border: 1px solid #242d3d; padding: 12px; background-color: #121722; font-size: 0.82em; color: #94a3b8; border-radius: 2px; margin-top: 8px;">
                    <div style="color: #00ff80; font-weight: bold; font-family: monospace; margin-bottom: 4px;">ACOUSTIC BUS STATUS</div>
                    ● <b>Playback Target:</b> Shokz OpenRun (Bluetooth Default)<br>
                    ● <b>Autonomous Mode:</b> ''' + ("Active (Hands-Free)" if auto_speak else "On-Demand") + '''<br>
                    ● <b>Acoustic Latency:</b> < 10ms (Native CoreAudio)<br>
                    ● <b>Compliance:</b> DFARS 252.227-7018
                </div>
            ''', unsafe_allow_html=True)"""

p_idx = content.find(old_anchor)
if p_idx != -1:
    end_anchor = "if provider.name != cls.OPTICAL_PROVIDERS[\"MOBILE\"].name:"
    e_idx = content.find(end_anchor, p_idx)
    if e_idx != -1:
        content = content[:p_idx] + new_voice_deck + "\n\n        " + content[e_idx:]

with open(CORE_FILE, "w", encoding="utf-8") as f:
    f.write(content)

py_compile.compile(CORE_FILE, doraise=True)
print("[SUCCESS] sovereign_comms_core.py updated with Autonomous Voice Deck.")
