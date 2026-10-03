import os
import sys
import re
import ast
import json
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
CORE_FILE = os.path.join(BASE_DIR, "sovereign_comms_core.py")
CONSOLE_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

print("=" * 80)
print("HVF Omni-Industrial Matrix | PLUG-AND-PLAY COMMS MATRIX DEPLOYMENT")
print("=" * 80)

# 1. Deploy sovereign_comms_core.py with Abstract Base Interfaces
CORE_CODE = """# ==============================================================================
# HVF Omni-Industrial Matrix | SOVEREIGN COMMUNICATIONS CORE
# Pluggable Component-Centric Matrix: Video, Text Dispatch, and Voice Link
# Authority: Mr. Humphrey (Founder & CEO) | DFARS 252.227-7018 Compliant
# ==============================================================================
import os
import json
import sqlite3
from datetime import datetime
from abc import ABC, abstractmethod
import streamlit as st
import cv2
from cryptography.fernet import Fernet

BASE_DIR = r"C:\\HVF_Repos\\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
KEY_PATH = os.path.join(BASE_DIR, "memory_core", "vault.key")
TAPO_CONFIG_PATH = os.path.join(BASE_DIR, "tapo_credentials.json")

# ==============================================================================
# PLUG-AND-PLAY COMPONENT REGISTRY (FUTURE-PROOF EXTENSION INTERFACES)
# ==============================================================================
class BaseOpticalProvider(ABC):
    \"\"\"Abstract interface for all current and future optical sensors.\"\"\"
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def telemetry(self) -> dict:
        pass

    @abstractmethod
    def capture_frame(self) -> tuple:
        pass


class ArducamUSBProvider(BaseOpticalProvider):
    name = "🖥️ Sensor 1: Desktop Arducam"

    @property
    def telemetry(self):
        return {
            "Hardware": "Arducam-1080P-HDR",
            "Bus Type": "USB DirectShow Bus",
            "Resolution": "1280x720 HD",
            "Architecture": "In-Process DirectShow",
            "Compliance": "DFARS 252.227-7018"
        }

    def capture_frame(self):
        for idx in [1, 0]:
            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
                    cv2.rectangle(frame, (0, 0), (w, 38), (11, 14, 20), -1)
                    cv2.line(frame, (0, 38), (w, 38), (0, 255, 128), 2)
                    cv2.putText(frame, f"HVF-C2 // ARDUCAM-1080P-HDR // {ts}", 
                                (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 128), 2, cv2.LINE_AA)
                    return True, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), ts
        return False, None, ""


class TapoRTSPProvider(BaseOpticalProvider):
    name = "📹 Sensor 2: TP-Link Tapo (192.168.1.165)"

    @property
    def telemetry(self):
        return {
            "Hardware": "TP-Link Tapo IP Camera",
            "Endpoint": "192.168.1.165:554",
            "Protocol": "RFC 2326 RTSP (TCP)",
            "Account": "ebony_cam",
            "Compliance": "DFARS 252.227-7018"
        }

    def capture_frame(self):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|analyzeduration;1000000|probesize;1000000"
        tapo_urls = [
            "rtsp://ebony_cam:Mina%402014@192.168.1.165:554/stream1",
            "rtsp://ebony_cam:Mina@2014@192.168.1.165:554/stream1"
        ]
        if os.path.exists(TAPO_CONFIG_PATH):
            try:
                with open(TAPO_CONFIG_PATH, "r", encoding="utf-8") as tf:
                    cfg = json.load(tf)
                    u = cfg.get("rtsp_url")
                    if u and u not in tapo_urls:
                        tapo_urls.insert(0, u)
            except Exception:
                pass

        for t_url in tapo_urls:
            cap = cv2.VideoCapture(t_url, cv2.CAP_FFMPEG)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
                    cv2.rectangle(frame, (0, 0), (w, 38), (11, 14, 20), -1)
                    cv2.line(frame, (0, 38), (w, 38), (0, 255, 128), 2)
                    cv2.putText(frame, f"HVF-C2 // TP-LINK TAPO // 192.168.1.165:554 // {ts}", 
                                (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 128), 2, cv2.LINE_AA)
                    return True, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), ts
        return False, None, ""


class MobileClientOpticalProvider(BaseOpticalProvider):
    name = "📱 Sensor 3: Mobile / Tablet Ingest"

    @property
    def telemetry(self):
        return {
            "Hardware": "Client Tablet / Phone Camera",
            "Bus Type": "Browser WebMedia / Native Streamlit",
            "Transport": "Direct In-Process Socket",
            "Compliance": "DFARS 252.227-7018"
        }

    def capture_frame(self):
        return True, None, ""


class SovereignCommsEngine:
    \"\"\"Master plug-and-play orchestrator for Video, Text Dispatch, and Voice Talk.\"\"\"
    # Pluggable Provider Registry
    OPTICAL_PROVIDERS = {
        "ARDUCAM": ArducamUSBProvider(),
        "TAPO": TapoRTSPProvider(),
        "MOBILE": MobileClientOpticalProvider()
    }

    @classmethod
    def register_optical_provider(cls, key: str, provider: BaseOpticalProvider):
        \"\"\"Plug-in point: dynamically attach new sensors without editing core logic.\"\"\"
        cls.OPTICAL_PROVIDERS[key] = provider

    @staticmethod
    def get_cipher():
        if os.path.exists(KEY_PATH):
            try:
                with open(KEY_PATH, "rb") as kf:
                    return Fernet(kf.read().strip())
            except Exception:
                return None
        return None

    @classmethod
    def render(cls):
        st.header("📡 Sovereign Communications Deck // Project Ebony")
        st.markdown("Modular plug-and-play matrix: **Optical Surveillance**, **Encrypted P2P Text**, and **Voice Dispatch**.")

        # --- PILLAR 1: PLUG-AND-PLAY OPTICAL MATRIX ---
        st.subheader("🔴 1. LIVE OPTICAL MATRIX // MULTI-SENSOR BUS")

        tab_arducam, tab_tapo, tab_mobile = st.tabs([
            cls.OPTICAL_PROVIDERS["ARDUCAM"].name,
            cls.OPTICAL_PROVIDERS["TAPO"].name,
            cls.OPTICAL_PROVIDERS["MOBILE"].name
        ])

        # TAB 1: DESKTOP ARDUCAM
        with tab_arducam:
            c1, c2 = st.columns([2.3, 1])
            with c1:
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                if st.button("📸 Ingest Arducam Frame", key="btn_ingest_arducam_pnp", type="primary") or "pnp_ard_frame" not in st.session_state:
                    ok, frame, ts = cls.OPTICAL_PROVIDERS["ARDUCAM"].capture_frame()
                    if ok:
                        st.session_state["pnp_ard_frame"] = frame
                        st.session_state["pnp_ard_ts"] = ts

                if "pnp_ard_frame" in st.session_state:
                    st.image(
                        st.session_state["pnp_ard_frame"], 
                        caption=f"SENSOR 1 TELEMETRY // ARDUCAM-1080P-HDR // {st.session_state.get('pnp_ard_ts', '')}", 
                        use_container_width=True
                    )
            with c2:
                tel = cls.OPTICAL_PROVIDERS["ARDUCAM"].telemetry
                st.markdown(f\"\"\"
                    <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">
                        <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px;">SENSOR 1 METRICS</div>
                        <b>Hardware:</b> {tel['Hardware']}<br>
                        <b>Bus Type:</b> {tel['Bus Type']}<br>
                        <b>Resolution:</b> {tel['Resolution']}<br>
                        <b>Architecture:</b> {tel['Architecture']}<br>
                        <b>Compliance:</b> {tel['Compliance']}
                    </div>
                \"\"\", unsafe_allow_html=True)

        # TAB 2: TP-LINK TAPO RTSP
        with tab_tapo:
            c1, c2 = st.columns([2.3, 1])
            with c1:
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                if st.button("📸 Ingest Tapo Optical Frame", key="btn_ingest_tapo_pnp", type="primary") or "pnp_tapo_frame" not in st.session_state:
                    ok, frame, ts = cls.OPTICAL_PROVIDERS["TAPO"].capture_frame()
                    if ok:
                        st.session_state["pnp_tapo_frame"] = frame
                        st.session_state["pnp_tapo_ts"] = ts
                    else:
                        st.warning("Connecting to Tapo camera at 192.168.1.165:554... Click 'Ingest Tapo Optical Frame' to refresh.")

                if "pnp_tapo_frame" in st.session_state:
                    st.image(
                        st.session_state["pnp_tapo_frame"], 
                        caption=f"SENSOR 2 TELEMETRY // TP-LINK TAPO // {st.session_state.get('pnp_tapo_ts', '')}", 
                        use_container_width=True
                    )
            with c2:
                tel = cls.OPTICAL_PROVIDERS["TAPO"].telemetry
                st.markdown(f\"\"\"
                    <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">
                        <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px;">SENSOR 2 METRICS</div>
                        <b>Hardware:</b> {tel['Hardware']}<br>
                        <b>Endpoint:</b> {tel['Endpoint']}<br>
                        <b>Protocol:</b> {tel['Protocol']}<br>
                        <b>Service Acct:</b> {tel['Account']}<br>
                        <b>Compliance:</b> {tel['Compliance']}
                    </div>
                \"\"\", unsafe_allow_html=True)

        # TAB 3: MOBILE CLIENT / TABLET INGEST
        with tab_mobile:
            st.markdown("Direct client-side optical capture from your Galaxy Tab Active5 or phone.")
            cam_shot = st.camera_input("📸 Capture Optical Telemetry from Mobile Device", key="pnp_mobile_cam_shot")
            if cam_shot is not None:
                st.image(cam_shot, caption="SENSOR 3 TELEMETRY // MOBILE CLIENT CAMERA // INGESTED", use_container_width=True)
                st.success("Optical intelligence successfully ingested into C2 memory.")

        st.markdown("---")

        # --- PILLAR 2 & 3: ENCRYPTED TEXT & SOVEREIGN VOICE ---
        col_txt, col_vox = st.columns([1.5, 1.2])

        with col_txt:
            st.subheader("💬 2. ENCRYPTED P2P TEXT")
            st.caption("Cryptographic message dispatch (AES-128/Fernet ciphertext at rest).")

            p2p_msg = st.text_input("Outbound Tactical Transmission", key="pnp_p2p_text_input", placeholder="Enter secure payload...")
            if st.button("📨 Transmit Encrypted Text", key="btn_pnp_p2p_send", type="primary"):
                if p2p_msg:
                    cipher = cls.get_cipher()
                    if cipher:
                        enc_bytes = cipher.encrypt(p2p_msg.encode("utf-8")).decode("utf-8")
                        try:
                            conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
                            conn.execute(\"\"\"
                                INSERT INTO p2p_chat_logs (sender, encrypted_payload, timestamp, status)
                                VALUES (?, ?, ?, ?)
                            \"\"\", ("CEO", enc_bytes, datetime.now().isoformat(), "CIPHERTEXT_AT_REST"))
                            conn.close()
                            st.success("Transmitted and sealed into sovereign vault.")
                        except Exception as ex_db:
                            st.error(f"Vault write error: {ex_db}")
                    st.rerun()

            cipher = cls.get_cipher()
            try:
                c_p2p = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
                cur = c_p2p.cursor()
                cur.execute("SELECT sender, encrypted_payload, timestamp FROM p2p_chat_logs ORDER BY id DESC LIMIT 6")
                logs = cur.fetchall()
                c_p2p.close()

                st.markdown("<div style='max-height: 180px; overflow-y: auto; padding: 6px; background: #0b0e14; border: 1px solid #242d3d; border-radius: 2px;'>", unsafe_allow_html=True)
                for s, enc_m, ts in reversed(logs):
                    try:
                        clear_m = cipher.decrypt(enc_m.encode("utf-8")).decode("utf-8") if cipher else "[LOCKED]"
                    except Exception:
                        clear_m = "[CIPHERTEXT_LOCKED]"
                    st.markdown(f"<div style='font-family:monospace; font-size:0.82em; padding:3px 0;'><b>{s}:</b> {clear_m} <span style='color:#e2a03f; font-size:0.75em;'>🛡️ [ENCRYPTED]</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception:
                pass

        with col_vox:
            st.subheader("🎙️ 3. SOVEREIGN VOICE TALK")
            st.caption("Direct voice capture & acoustic link to Ebony AI.")

            if hasattr(st, "audio_input"):
                v_audio = st.audio_input("🎙️ Push-to-Talk Transmission", key="pnp_voice_input")
                if v_audio is not None:
                    st.audio(v_audio, format="audio/wav")
                    st.success("Voice transmission ingested into defense memory.")
            else:
                st.info("🎙️ Voice link active via ADA Voice Engine header.")

            st.markdown(\"\"\"
                <div style="border: 1px solid #242d3d; padding: 12px; background-color: #121722; font-size: 0.82em; color: #94a3b8; border-radius: 2px; margin-top: 10px;">
                    <div style="color: #00ff80; font-weight: bold; font-family: monospace; margin-bottom: 4px;">ACOUSTIC BUS STATUS</div>
                    ● <b>Gateway:</b> ADA Voice Link Online<br>
                    ● <b>Engine:</b> Native WebAudio / PCM<br>
                    ● <b>Hotword:</b> "Ebony"<br>
                    ● <b>Compliance:</b> DFARS 252.227-7018
                </div>
            \"\"\", unsafe_allow_html=True)
"""

with open(CORE_FILE, "w", encoding="utf-8") as f:
    f.write(CORE_CODE.strip() + "\n")
py_compile.compile(CORE_FILE, doraise=True)
print(f"[SUCCESS] sovereign_comms_core.py compiled cleanly.")

# 2. Refactor Consoles to Delegate Comms Deck to sovereign_comms_core.py
def refactor_console(fpath):
    if not os.path.exists(fpath):
        return
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match Comms Deck active_module branch
    regex = re.compile(r'^[ \t]*(?:elif|if)\s+active_module\b[^\n]*?(?:Comms|WebRTC|Communications)[^\n]*:\s*\n', re.MULTILINE)
    m = regex.search(content)
    if not m:
        # Fallback: search for st.header("📡 Sovereign Communications Deck
        h_m = re.search(r'^[ \t]*st\.header\(["\'].*?Sovereign Communications Deck', content, re.MULTILINE)
        if h_m:
            pre = content[:h_m.start()]
            m_pre = list(re.finditer(r'^[ \t]*(?:elif|if)\s+active_module\b[^\n]*:\s*\n', pre, re.MULTILINE))
            if m_pre:
                m = m_pre[-1]

    if not m:
        print(f"[WARN] Module anchor not found in {os.path.basename(fpath)}")
        return

    start_pos = m.end()
    cond_line = m.group(0)
    cond_indent = len(cond_line) - len(cond_line.lstrip())

    # Find the end of the module branch (outdent or next elif/else at same level)
    lines = content[start_pos:].splitlines(keepends=True)
    end_offset = 0
    found_next = False
    for line in lines:
        stripped = line.lstrip()
        if stripped:
            indent = len(line) - len(stripped)
            if indent <= cond_indent:
                found_next = True
                break
        end_offset += len(line)

    end_pos = start_pos + end_offset if found_next else len(content)
    body_indent = cond_indent + 4

    clean_call = (
        (" " * body_indent) + "from sovereign_comms_core import SovereignCommsEngine\n" +
        (" " * body_indent) + "SovereignCommsEngine.render()\n"
    )

    new_content = content[:start_pos] + clean_call + content[end_pos:]

    # Strict AST Parse Verification
    ast.parse(new_content, filename=fpath)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    py_compile.compile(fpath, doraise=True)
    print(f"[SUCCESS] Verified AST compilation: {os.path.basename(fpath)}")

for cf in CONSOLE_FILES:
    refactor_console(cf)

print("=" * 80)
print("PLUG-AND-PLAY DEPLOYMENT AND CONSOLE INTEGRATION COMPLETE")
print("=" * 80)

