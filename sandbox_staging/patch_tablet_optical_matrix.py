import os
import sys
import re
import json
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DAEMON_FILE = os.path.join(BASE_DIR, "optical_stream_daemon.py")
CONFIG_FILE = os.path.join(BASE_DIR, "tablet_config.json")
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

# 1. Initialize default tablet configuration
if not os.path.exists(CONFIG_FILE):
    default_cfg = {
        "tablet_ip": "192.168.1.100",
        "tablet_port": 8080,
        "stream_path": "/video",
        "full_url": "http://192.168.1.100:8080/video"
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(default_cfg, f, indent=4)

# 2. Write Tablet-Adaptive Optical Daemon
DAEMON_CODE = """import os
import sys
import time
import threading
import socketserver
import json
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import cv2

PORT = 8502
BASE_DIR = r"C:\\HVF_Repos\\hvf-media-matrix-private"
CONFIG_FILE = os.path.join(BASE_DIR, "tablet_config.json")

class SovereignOpticalRouter:
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        self.active_mode = "ARDUCAM"  # "ARDUCAM" or "TABLET"
        self.target_mode = "ARDUCAM"
        self.switch_requested = False

    def request_switch(self, mode: str):
        with self.lock:
            self.target_mode = mode.upper()
            self.switch_requested = True
        print(f"[OPTICAL ROUTER] Route request -> {self.target_mode}")

    def capture_loop(self):
        cap = None
        current_mode = ""

        while self.running:
            if cap is None or self.switch_requested:
                if cap is not None:
                    cap.release()
                    time.sleep(0.2)

                with self.lock:
                    self.active_mode = self.target_mode
                    self.switch_requested = False
                    current_mode = self.active_mode

                if current_mode == "TABLET":
                    tablet_url = "http://192.168.1.100:8080/video"
                    if os.path.exists(CONFIG_FILE):
                        try:
                            with open(CONFIG_FILE, "r") as f:
                                cfg = json.load(f)
                                tablet_url = cfg.get("full_url", tablet_url)
                        except Exception:
                            pass
                    print(f"[OPTICAL ROUTER] Connecting to Tablet Stream: {tablet_url}")
                    cap = cv2.VideoCapture(tablet_url)
                else:
                    print("[OPTICAL ROUTER] Binding Desktop Arducam (DirectShow Index 1)...")
                    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                    if not cap.isOpened():
                        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                    cap.set(cv2.CAP_PROP_FPS, 30)

            if cap is None or not cap.isOpened():
                time.sleep(0.1)
                continue

            ret, raw_frame = cap.read()
            if not ret or raw_frame is None:
                time.sleep(0.02)
                continue

            h, w = raw_frame.shape[:2]
            ts_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

            # Tactical HUD Watermark
            cv2.rectangle(raw_frame, (0, 0), (w, 42), (11, 14, 20), -1)
            cv2.line(raw_frame, (0, 42), (w, 42), (226, 160, 63), 2)
            label = "DESKTOP WORKSTATION ARDUCAM (USB)" if current_mode == "ARDUCAM" else "TACTICAL TABLET UPLINK (NETWORK)"
            banner_text = f">>> {label} <<< // {w}x{h} // {ts_str}"
            cv2.putText(raw_frame, banner_text, (15, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 128), 2, cv2.LINE_AA)

            ret_enc, buffer = cv2.imencode(".jpg", raw_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if ret_enc:
                with self.lock:
                    self.frame = buffer.tobytes()

            time.sleep(0.015)

        if cap is not None:
            cap.release()

buffer_manager = SovereignOpticalRouter()

class SwarmStreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/video_feed":
            self.send_response(200)
            self.send_header("Age", "0")
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                while True:
                    with buffer_manager.lock:
                        if buffer_manager.frame is None:
                            time.sleep(0.01)
                            continue
                        current_bytes = buffer_manager.frame

                    self.wfile.write(b"--FRAME\\r\\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", str(len(current_bytes)))
                    self.end_headers()
                    self.wfile.write(current_bytes)
                    self.wfile.write(b"\\r\\n")
                    time.sleep(0.033)
            except Exception:
                pass

        elif path == "/switch_device":
            params = parse_qs(parsed.query)
            mode = params.get("mode", ["ARDUCAM"])[0]
            buffer_manager.request_switch(mode)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(f'{{"status": "SUCCESS", "active_mode": "{mode}"}}'.encode())

        elif path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with buffer_manager.lock:
                act_m = buffer_manager.active_mode
            self.wfile.write(f'{{"status": "ONLINE", "mode": "{act_m}"}}'.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, format, *args):
        return

class SwarmHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    cap_thread = threading.Thread(target=buffer_manager.capture_loop, daemon=True)
    cap_thread.start()
    time.sleep(1.0)
    server_address = ("0.0.0.0", PORT)
    httpd = SwarmHTTPServer(server_address, SwarmStreamHandler)
    print(f"[SUCCESS] Optical Daemon listening on port {PORT}")
    httpd.serve_forever()
"""

with open(DAEMON_FILE, "w", encoding="utf-8") as f:
    f.write(DAEMON_CODE.strip() + "\n")
py_compile.compile(DAEMON_FILE, doraise=True)
print("[SUCCESS] optical_stream_daemon.py updated and compiled cleanly.")

# 3. Update Console Viewport with Tablet Switching Controls
CONSOLE_UI_BLOCK = """# --- LIVE SWARM OPTICAL FEED (ARDUCAM & TABLET MATRIX) ---
st.subheader("🔴 LIVE // SWARM OPTICAL FEED")
st.markdown("Desktop Hardware & Tablet Uplink Matrix streaming via Sovereign Tailscale Link.")

if "active_optical_sensor" not in st.session_state:
    st.session_state["active_optical_sensor"] = "ARDUCAM"

sw_c1, sw_c2, sw_c3 = st.columns([1.8, 1.8, 1.2])
with sw_c1:
    is_ard = st.session_state["active_optical_sensor"] == "ARDUCAM"
    if st.button("🖥️ Sensor 1: Desktop Arducam", key="btn_sel_arducam_v4", type="primary" if is_ard else "secondary"):
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:8502/switch_device?mode=ARDUCAM", timeout=2.0)
        except Exception:
            pass
        st.session_state["active_optical_sensor"] = "ARDUCAM"
        st.rerun()

with sw_c2:
    is_tab = st.session_state["active_optical_sensor"] == "TABLET"
    if st.button("📱 Sensor 2: Tablet Uplink", key="btn_sel_tablet_v4", type="primary" if is_tab else "secondary"):
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:8502/switch_device?mode=TABLET", timeout=2.0)
        except Exception:
            pass
        st.session_state["active_optical_sensor"] = "TABLET"
        st.rerun()

with sw_c3:
    gw_choice = st.selectbox("Gateway", ["100.87.162.117", "127.0.0.1"], key="gw_tactical_v4")

# Tablet Endpoint Configuration Expander
with st.expander("⚙️ Configure Tablet Streaming Endpoint", expanded=False):
    tab_cfg_file = r"C:\\HVF_Repos\\hvf-media-matrix-private\\tablet_config.json"
    current_url = "http://192.168.1.100:8080/video"
    if os.path.exists(tab_cfg_file):
        try:
            with open(tab_cfg_file, "r") as f:
                c_data = json.load(f)
                current_url = c_data.get("full_url", current_url)
        except Exception:
            pass

    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        new_tab_url = st.text_input("Tablet MJPEG Stream URL (Displayed in Tablet App)", value=current_url, key="input_tablet_url")
    with col_t2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Save & Re-bind", key="btn_save_tablet_url"):
            with open(tab_cfg_file, "w", encoding="utf-8") as f:
                json.dump({"full_url": new_tab_url.strip()}, f, indent=4)
            st.success("Tablet endpoint updated.")
            if st.session_state["active_optical_sensor"] == "TABLET":
                import urllib.request
                try:
                    urllib.request.urlopen("http://127.0.0.1:8502/switch_device?mode=TABLET", timeout=2.0)
                except Exception:
                    pass
            st.rerun()

stream_gw = gw_choice
stream_url = f"http://{stream_gw}:8502/video_feed"

opt_c1, opt_c2 = st.columns([2.2, 1])
with opt_c1:
    st.markdown(f'''
        <div style="position: relative; width: 100%; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden;">
            <img src="{stream_url}" 
                 style="width: 100%; height: auto; min-height: 380px; display: block; object-fit: cover;"
                 onerror="this.onerror=null; this.src=''; this.parentElement.innerHTML='<div style=\\'padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;\\'><div style=\\'color:#e2a03f; font-size:1.1em; font-weight:bold;\\'>OPTICAL STREAM STANDBY</div><div>Daemon active on port 8502. Gateway: {stream_gw}:8502</div></div>';" />
        </div>
    ''', unsafe_allow_html=True)

with opt_c2:
    sensor_title = "ARDUCAM-1080P-HDR (DESKTOP USB)" if st.session_state["active_optical_sensor"] == "ARDUCAM" else "TACTICAL TABLET UPLINK (NETWORK)"
    st.markdown(f'''
        <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">
            <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px; text-transform: uppercase;">OPTICAL BUS TELEMETRY</div>
            <b>Active Sensor:</b> {sensor_title}<br>
            <b>Hardware Bus:</b> USB Bus / Wi-Fi Mesh<br>
            <b>Active Gateway:</b> {stream_gw}:8502<br>
            <b>Transport:</b> RFC 2046 Multipart MJPEG<br>
            <b>Watermark:</b> Hardware-Inscribed<br>
            <b>Compliance:</b> DFARS 252.227-7018
        </div>
    ''', unsafe_allow_html=True)"""

def build_indented_block(raw_code, indent_spaces):
    indent = " " * indent_spaces
    return "\n".join((indent + line) if line.strip() else "" for line in raw_code.strip().splitlines())

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue

    print(f"\nProcessing target: {os.path.basename(fpath)}")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    start_anchor = 'st.subheader("🔴 LIVE // SWARM OPTICAL FEED")'
    end_anchor = 'st.subheader("💬 Encrypted P2P Dispatch")'

    if start_anchor in content and end_anchor in content:
        p_start = content.find(start_anchor)
        p_end = content.find(end_anchor, p_start)
        line_start = content.rfind("\n", 0, p_start) + 1
        indent_len = p_start - line_start

        formatted_embed = build_indented_block(CONSOLE_UI_BLOCK, indent_len)
        new_content = content[:p_start] + formatted_embed + "\n\n" + (" " * indent_len) + content[p_end:]

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Embedded Tablet Optical Router into {os.path.basename(fpath)}.")
    else:
        print(f"  * [WARN] Anchors not matched in {os.path.basename(fpath)}.")

print("\n" + "=" * 80)
print("TABLET OPTICAL ROUTER INTEGRATION COMPLETE")
print("=" * 80)
