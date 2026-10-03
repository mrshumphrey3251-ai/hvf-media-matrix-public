import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

UNIFIED_TRIAD_CODE = """# ==============================================================================
# SOVEREIGN COMMUNICATIONS TRIAD // VIDEO + TEXT + TALK
# Authority: Mr. Humphrey (Founder & CEO) | DFARS 252.227-7018 Compliant
# ==============================================================================
st.header("📡 Sovereign Communications Deck // Project Ebony")
st.markdown("Unified sovereign matrix: **Live Video**, **Encrypted Text Dispatch**, and **Tactical Voice Link**.")

# 1. GATEWAY NETWORK LINK
gw_col1, gw_col2 = st.columns([3, 1])
with gw_col1:
    st.caption("Active Secure Mesh Transport: Tailscale Encrypted WireGuard (100.87.162.117)")
with gw_col2:
    active_gw = st.selectbox("Mesh Gateway", ["100.87.162.117", "127.0.0.1"], key="triad_gw_select")

# --- PILLAR 1: LIVE VIDEO STREAM (ARDUCAM-1080P-HDR) ---
st.subheader("🔴 1. LIVE OPTICAL FEED // ARDUCAM-1080P-HDR")
video_col1, video_col2 = st.columns([2.3, 1])
with video_col1:
    stream_url = f"http://{active_gw}:8502/video_feed"
    st.markdown(f'''
        <div style="position: relative; width: 100%; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden;">
            <div style="position: absolute; top: 8px; left: 10px; z-index: 10; font-family: monospace; font-size: 0.75em; background-color: rgba(11,14,20,0.85); padding: 2px 8px; border: 1px solid #242d3d; border-radius: 2px;">
                <span style="color: #ef4444; font-weight: bold;">● LIVE 30 FPS</span> | <span style="color: #e2a03f;">ARDUCAM-1080P-HDR</span>
            </div>
            <img src="{stream_url}" 
                 style="width: 100%; height: auto; min-height: 360px; display: block; object-fit: cover;"
                 onerror="this.onerror=null; this.src=''; this.parentElement.innerHTML='<div style=\\'padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;\\'><div style=\\'color:#e2a03f; font-size:1.1em; font-weight:bold;\\'>ARDUCAM STREAM STANDBY</div><div>Optical daemon active on port 8502. Gateway: {active_gw}:8502</div></div>';" />
        </div>
    ''', unsafe_allow_html=True)

with video_col2:
    st.markdown(f'''
        <div style="border: 1px solid #242d3d; padding: 12px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">
            <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 6px;">OPTICAL BUS TELEMETRY</div>
            <b>Hardware:</b> Arducam-1080P-HDR<br>
            <b>Bus:</b> USB DirectShow Bus<br>
            <b>Frame Rate:</b> 30 FPS Synchronous<br>
            <b>Endpoint:</b> http://{active_gw}:8502<br>
            <b>Compliance:</b> DFARS 252.227-7018
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Optical Link", key="btn_refresh_triad_vid"):
        st.rerun()

st.markdown("---")

# --- PILLAR 2 & 3: TEXT DISPATCH & VOICE TALK LINK ---
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
    
    # Direct Browser Push-to-Talk Audio Input
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
print("HVF Omni-Industrial Matrix | UNIFYING VIDEO, TEXT, AND TALK")
print("=" * 80)

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue

    print(f"\nProcessing target: {os.path.basename(fpath)}")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Anchor to Comms Deck module start and next module boundary
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

    formatted_block = build_indented_block(UNIFIED_TRIAD_CODE, body_indent)
    new_content = content[:start_pos] + formatted_block + "\n\n" + content[end_pos:]

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    py_compile.compile(fpath, doraise=True)
    print(f"  * [SUCCESS] Clean compile: {os.path.basename(fpath)}")

print("\n" + "=" * 80)
print("TRIAD INTEGRATION COMPLETE: VIDEO, TEXT, AND TALK UNIFIED")
print("=" * 80)

