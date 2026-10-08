import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

OPTICAL_COMPLETE_BLOCK = """# --- LIVE SWARM OPTICAL FEED (DESKTOP HARDWARE & ACTIVE MOBILE WEBRTC) ---
st.subheader("🔴 LIVE // SWARM OPTICAL FEED")
st.markdown("Hardware Matrix & WebRTC streaming via Sovereign Tailscale Link.")

if "active_optical_mode" not in st.session_state:
    st.session_state["active_optical_mode"] = "DESKTOP_HD"

# Tactical Source Selection Controls
sw_c1, sw_c2, sw_c3, sw_c4 = st.columns([1.5, 1.5, 1.5, 1.2])
with sw_c1:
    is_hd = st.session_state["active_optical_mode"] == "DESKTOP_HD"
    if st.button("🖥️ Desktop Arducam HD", key="btn_mode_desk_hd", type="primary" if is_hd else "secondary"):
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:8502/switch_device?index=1", timeout=2.0)
        except Exception:
            pass
        st.session_state["active_optical_mode"] = "DESKTOP_HD"
        st.rerun()

with sw_c2:
    is_sd = st.session_state["active_optical_mode"] == "DESKTOP_SD"
    if st.button("🖥️ Desktop Arducam SD", key="btn_mode_desk_sd", type="primary" if is_sd else "secondary"):
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:8502/switch_device?index=0", timeout=2.0)
        except Exception:
            pass
        st.session_state["active_optical_mode"] = "DESKTOP_SD"
        st.rerun()

with sw_c3:
    is_mob = st.session_state["active_optical_mode"] == "MOBILE_PHONE"
    if st.button("📱 Mobile Phone Uplink", key="btn_mode_mob_uplink", type="primary" if is_mob else "secondary"):
        st.session_state["active_optical_mode"] = "MOBILE_PHONE"
        st.rerun()

with sw_c4:
    gw_choice = st.selectbox("Gateway", ["100.87.162.117", "127.0.0.1"], key="gw_selector_box")

stream_gw = gw_choice

# Live Video Viewport Rendering
opt_c1, opt_c2 = st.columns([2.2, 1])
with opt_c1:
    if st.session_state["active_optical_mode"] in ["DESKTOP_HD", "DESKTOP_SD"]:
        stream_url = f"http://{stream_gw}:8502/video_feed"
        st.markdown(f'''
            <div style="position: relative; width: 100%; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden;">
                <img src="{stream_url}" 
                     style="width: 100%; height: auto; min-height: 380px; display: block; object-fit: cover;"
                     onerror="this.onerror=null; this.src=''; this.parentElement.innerHTML='<div style=\\'padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;\\'><div style=\\'color:#e2a03f; font-size:1.1em; font-weight:bold;\\'>OPTICAL STREAM STANDBY</div><div>Start optical_stream_daemon.py on port 8502. Gateway: {stream_gw}:8502</div></div>';" />
            </div>
        ''', unsafe_allow_html=True)
    else:
        # Active HTML5 WebRTC Mobile Camera Player
        import streamlit.components.v1 as components
        mobile_cam_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin: 0; padding: 0; background-color: #0b0e14; font-family: monospace; }
                .container { position: relative; width: 100%; height: 380px; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden; display: flex; align-items: center; justify-content: center; }
                video { width: 100%; height: 100%; object-fit: cover; }
                .badge { position: absolute; top: 8px; left: 10px; z-index: 10; font-size: 11px; background-color: rgba(11,14,20,0.85); padding: 2px 8px; border: 1px solid #242d3d; border-radius: 2px; color: #ef4444; font-weight: bold; }
                .status-overlay { position: absolute; color: #94a3b8; text-align: center; font-size: 13px; z-index: 1; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="badge">● LIVE // MOBILE CLIENT WEBRTC</div>
                <div id="status_msg" class="status-overlay">Requesting Mobile Camera Access...</div>
                <video id="webcam" autoplay playsinline muted></video>
            </div>
            <script>
                const video = document.getElementById('webcam');
                const status = document.getElementById('status_msg');
                navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } } })
                    .then(stream => {
                        video.srcObject = stream;
                        status.style.display = 'none';
                    })
                    .catch(err => {
                        status.innerHTML = '<span style="color:#ef4444;">Camera Access Denied or Unavailable</span><br>' + err.message;
                    });
            </script>
        </body>
        </html>
        '''
        components.html(mobile_cam_html, height=395)

with opt_c2:
    mode_label = "DESKTOP WORKSTATION SENSOR" if st.session_state["active_optical_mode"] != "MOBILE_PHONE" else "MOBILE CLIENT CAMERA"
    st.markdown(f'''
        <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">
            <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px; text-transform: uppercase;">OPTICAL BUS TELEMETRY</div>
            <b>Active Sensor:</b> {mode_label}<br>
            <b>Hardware Bus:</b> Arducam-1080P-HDR<br>
            <b>Stream Endpoint:</b> http://{stream_gw}:8502<br>
            <b>Transport:</b> DirectShow / WebRTC<br>
            <b>Watermark:</b> Hardware-Inscribed<br>
            <b>Compliance:</b> DFARS 252.227-7018
        </div>
    ''', unsafe_allow_html=True)"""

def build_indented_block(raw_code, indent_spaces):
    indent = " " * indent_spaces
    return "\n".join((indent + line) if line.strip() else "" for line in raw_code.strip().splitlines())

print("=" * 80)
print("EMBEDDING ACTIVE MOBILE WEBRTC & WATERMARKED DESKTOP VIEWPORT")
print("=" * 80)

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

        formatted_embed = build_indented_block(OPTICAL_COMPLETE_BLOCK, indent_len)
        new_content = content[:p_start] + formatted_embed + "\n\n" + (" " * indent_len) + content[p_end:]

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Embedded Active Mobile WebRTC into {os.path.basename(fpath)}.")
    else:
        print(f"  * [WARN] Anchors not matched in {os.path.basename(fpath)}.")

print("\n" + "=" * 80)
print("ACTIVE OPTICAL ENGINE INTEGRATION COMPLETE")
print("=" * 80)
