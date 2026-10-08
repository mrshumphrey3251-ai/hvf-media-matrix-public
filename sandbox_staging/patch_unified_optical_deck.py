"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: PATCH UNIFIED OPTICAL DECK
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sys

    import re

    import py_compile



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    TARGET_FILES = [

        os.path.join(BASE_DIR, "ebony_console.py"),

        os.path.join(BASE_DIR, "ebony_console_GREEN.py")

    ]



    UNIFIED_DECK_BLOCK = """# ==============================================================================

    # SOVEREIGN COMMUNICATIONS DECK // DUAL-SENSOR OPTICAL + TEXT + TALK

    # Authority: Mr. Humphrey (Founder & CEO) | DFARS 252.227-7018 Compliant

    # ==============================================================================

    st.header("📡 Sovereign Communications Deck // Project Ebony")

    st.markdown("Unified tactical matrix: **Optical Surveillance**, **Encrypted P2P Text**, and **Sovereign Voice Link**.")



    # --- SECTION 1: DUAL-SENSOR OPTICAL SURVEILLANCE ---

    st.subheader("🔴 1. LIVE OPTICAL MATRIX")



    tab_desktop, tab_tablet = st.tabs(["🖥️ Desktop Arducam Stream", "📱 Tablet / Mobile Camera Ingest"])



    with tab_desktop:

        opt_c1, opt_c2 = st.columns([2.3, 1])

        with opt_c1:

            # Auto-aligning dynamic host viewport: automatically binds to localhost or 100.87.162.117

            st.markdown('''

                <div style="position: relative; width: 100%; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden;">

                    <div style="position: absolute; top: 8px; left: 10px; z-index: 10; font-family: monospace; font-size: 0.75em; background-color: rgba(11,14,20,0.85); padding: 2px 8px; border: 1px solid #242d3d; border-radius: 2px;">

                        <span style="color: #ef4444; font-weight: bold;">● LIVE 30 FPS</span> | <span style="color: #e2a03f;">DESKTOP ARDUCAM-1080P-HDR</span>

                    </div>

                    <img id="arducam_live_feed" 

                         src="" 

                         style="width: 100%; height: auto; min-height: 360px; display: block; object-fit: cover;"

                         onerror="this.onerror=null; this.src=''; this.parentElement.querySelector('#standby_msg').style.display='block';" />

                    <div id="standby_msg" style="display:none; padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;">

                        <div style="color:#e2a03f; font-size:1.1em; font-weight:bold;">OPTICAL STREAM STANDBY</div>

                        <div>Verifying connection to host port 8502...</div>

                    </div>

                </div>

                <script>

                    // Dynamically extract connecting hostname (localhost on PC, 100.87.162.117 on Tablet)

                    const hostName = window.location.hostname || "100.87.162.117";

                    const imgElem = document.getElementById("arducam_live_feed");

                    if (imgElem) {

                        imgElem.src = "http://" + hostName + ":8502/video_feed";

                    }

                </script>

            ''', unsafe_allow_html=True)



        with opt_c2:

            st.markdown('''

                <div style="border: 1px solid #242d3d; padding: 12px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">

                    <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 6px;">DESKTOP SENSOR METRICS</div>

                    <b>Hardware:</b> Arducam-1080P-HDR<br>

                    <b>Bus:</b> USB DirectShow Bus<br>

                    <b>Frame Rate:</b> 30 FPS Synchronous<br>

                    <b>Host Stream:</b> Port 8502 (Auto-Aligned)<br>

                    <b>Compliance:</b> DFARS 252.227-7018

                </div>

            ''', unsafe_allow_html=True)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if st.button("🔄 Refresh Stream Viewport", key="btn_refresh_arducam_viewport"):

                st.rerun()



    with tab_tablet:

        st.markdown("Direct client-side optical capture from your Galaxy Tab Active5 (zero apps or port setup required).")

        tab_cam_intel = st.camera_input("📸 Capture Optical Intel from Tablet Camera", key="tablet_direct_cam_input")

        if tab_cam_intel is not None:

            st.image(tab_cam_intel, caption="TABLET SENSOR TELEMETRY // INGESTED INTO C2 MEMORY", use_container_width=True)

            st.success("Optical intelligence successfully acquired from tablet.")



    st.markdown("---")



    # --- SECTION 2 & 3: ENCRYPTED TEXT DISPATCH & SOVEREIGN VOICE TALK ---

    col_text, col_talk = st.columns([1.5, 1.2])



    with col_text:

        st.subheader("💬 2. ENCRYPTED P2P TEXT")

        st.markdown("Cryptographic message dispatch (AES-128/Fernet ciphertext at rest).")



        p2p_msg = st.text_input("Outbound Tactical Transmission", key="triad_p2p_text_input", placeholder="Enter secure message payload...")

        if st.button("📨 Transmit Encrypted Text", key="btn_triad_transmit_text", type="primary"):

            if p2p_msg:

                try:

                    import sqlite3

                    from datetime import datetime

                    from cryptography.fernet import Fernet



                    key_path = r"C:\\HVF_Repos\\hvf-media-matrix-private\\memory_core\\vault.key"

                    db_path = r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db"

                    with open(key_path, "rb") as kf:

                        cipher = Fernet(kf.read().strip())

                    enc_payload = cipher.encrypt(p2p_msg.encode("utf-8")).decode("utf-8")



                    conn = sqlite3.connect(db_path, timeout=10.0, isolation_level=None)

                    conn.execute(\"\"\"

                        INSERT INTO p2p_chat_logs (sender, encrypted_payload, timestamp, status)

                        VALUES (?, ?, ?, ?)

                    \"\"\", ("CEO", enc_payload, datetime.now().isoformat(), "CIPHERTEXT_AT_REST"))

                    conn.close()

                    st.success("Transmitted and sealed into sovereign vault.")

                except Exception as ex_txt:

                    st.error(f"Transmission error: {ex_txt}")

                st.rerun()



        # Encrypted Text Ledger Display

        try:

            import sqlite3

            from cryptography.fernet import Fernet

            key_path = r"C:\\HVF_Repos\\hvf-media-matrix-private\\memory_core\\vault.key"

            db_path = r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db"

            with open(key_path, "rb") as kf:

                dec_cipher = Fernet(kf.read().strip())



            c_p2p = sqlite3.connect(db_path, timeout=10.0, isolation_level=None)

            cur_p2p = c_p2p.cursor()

            cur_p2p.execute("SELECT sender, encrypted_payload, timestamp FROM p2p_chat_logs ORDER BY id DESC LIMIT 6")

            logs = cur_p2p.fetchall()

            c_p2p.close()



            st.markdown("<div style='max-height: 180px; overflow-y: auto; padding: 6px; background: #0b0e14; border: 1px solid #242d3d; border-radius: 2px;'>", unsafe_allow_html=True)

            for s, enc_m, ts in reversed(logs):

                try:

                    clear_m = dec_cipher.decrypt(enc_m.encode("utf-8")).decode("utf-8")

                except Exception:

                    clear_m = "[CIPHERTEXT_LOCKED]"

                st.markdown(f"<div style='font-family:monospace; font-size:0.82em; padding:3px 0;'><b>{s}:</b> {clear_m} <span style='color:#e2a03f; font-size:0.75em;'>🛡️ [ENCRYPTED]</span></div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception:

            pass



    with col_talk:

        st.subheader("🎙️ 3. SOVEREIGN VOICE TALK")

        st.markdown("Direct voice capture & acoustic link to Ebony AI.")



        if hasattr(st, "audio_input"):

            voice_rec = st.audio_input("🎙️ Record Voice Transmission", key="triad_voice_capture")

            if voice_rec is not None:

                st.audio(voice_rec, format="audio/wav")

                st.success("Voice transmission captured for Ebony.")

        else:

            st.info("🎙️ Voice link active via ADA Voice Engine header.")



        st.markdown('''

            <div style="border: 1px solid #242d3d; padding: 12px; background-color: #121722; font-size: 0.82em; color: #94a3b8; border-radius: 2px; margin-top: 10px;">

                <div style="color: #00ff80; font-weight: bold; font-family: monospace; margin-bottom: 4px;">ACOUSTIC BUS STATUS</div>

                ● <b>Voice Gateway:</b> ADA Voice Link Online<br>

                ● <b>Speech Codec:</b> Native WebAudio / PCM<br>

                ● <b>Hotword:</b> "Ebony"<br>

                ● <b>Sovereignty:</b> Zero Third-Party Relays

            </div>

        ''', unsafe_allow_html=True)"""



    def build_indented_block(raw_code, indent_spaces):

        indent = " " * indent_spaces

        return "\n".join((indent + line) if line.strip() else "" for line in raw_code.strip().splitlines())



    print("=" * 80)

    print("PATCHING CONSOLES WITH DUAL-SENSOR OPTICAL VIEWPORT")

    print("=" * 80)



    for fpath in TARGET_FILES:

        if not os.path.exists(fpath):

            continue



        with open(fpath, "r", encoding="utf-8") as f:

            content = f.read()



        start_match = re.search(r'(^[ \t]*(?:elif|if)\s+active_module\s*==[^\n]*?(?:Comms|WebRTC)[^\n]*:\s*\n)', content, re.MULTILINE)

        if not start_match:

            print(f"  * [FAIL] Could not match Comms Deck branch in {os.path.basename(fpath)}.")

            continue



        start_pos = start_match.end()

        condition_line = start_match.group(1)

        condition_indent = len(condition_line) - len(condition_line.lstrip())

        body_indent = condition_indent + 4



        next_match = re.search(r'^[ \t]*(?:elif|if)\s+active_module\s*==', content[start_pos:], re.MULTILINE)

        if next_match:

            end_pos = start_pos + next_match.start()

        else:

            side_match = re.search(r'^[ \t]*with\s+col_side:', content[start_pos:], re.MULTILINE)

            end_pos = start_pos + side_match.start() if side_match else len(content)



        formatted_block = build_indented_block(UNIFIED_DECK_BLOCK, body_indent)

        new_content = content[:start_pos] + formatted_block + "\n\n" + content[end_pos:]



        with open(fpath, "w", encoding="utf-8") as f:

            f.write(new_content)



        py_compile.compile(fpath, doraise=True)

        print(f"  * [SUCCESS] Clean compile: {os.path.basename(fpath)}")



    print("=" * 80)


if __name__ == "__main__":
    render()
