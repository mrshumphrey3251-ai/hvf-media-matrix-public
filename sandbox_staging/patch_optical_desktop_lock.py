import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

OPTICAL_LOCKED_BLOCK = """# --- LIVE SWARM OPTICAL FEED (DESKTOP ARDUCAM HARDWARE PRIMARY) ---
st.subheader("🔴 LIVE // SWARM OPTICAL FEED")
st.markdown("Desktop Workstation Hardware Matrix streaming via Sovereign Tailscale Link.")

# Force default to Desktop Arducam HD if not set
if "active_optical_mode" not in st.session_state or st.session_state["active_optical_mode"] == "MOBILE_PHONE":
    st.session_state["active_optical_mode"] = "DESKTOP_HD"

# Direct Tactical Action Buttons
sw_c1, sw_c2, sw_c3, sw_c4 = st.columns([1.6, 1.6, 1.6, 1.2])
with sw_c1:
    is_hd = st.session_state["active_optical_mode"] == "DESKTOP_HD"
    if st.button("🖥️ Desktop Arducam HD", key="btn_sel_desk_hd_v2", type="primary" if is_hd else "secondary"):
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:8502/switch_device?index=1", timeout=2.0)
        except Exception:
            pass
        st.session_state["active_optical_mode"] = "DESKTOP_HD"
        st.rerun()

with sw_c2:
    is_sd = st.session_state["active_optical_mode"] == "DESKTOP_SD"
    if st.button("🖥️ Desktop Arducam SD", key="btn_sel_desk_sd_v2", type="primary" if is_sd else "secondary"):
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:8502/switch_device?index=0", timeout=2.0)
        except Exception:
            pass
        st.session_state["active_optical_mode"] = "DESKTOP_SD"
        st.rerun()

with sw_c3:
    if st.button("📱 Mobile Phone Uplink", key="btn_sel_mob_cam_v2"):
        st.session_state["active_optical_mode"] = "MOBILE_PHONE"
        st.rerun()

with sw_c4:
    gw_choice = st.selectbox("Gateway", ["100.87.162.117", "127.0.0.1"], key="gw_tactical_v2")

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
                     onerror="this.onerror=null; this.src=''; this.parentElement.innerHTML='<div style=\\'padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;\\'><div style=\\'color:#e2a03f; font-size:1.1em; font-weight:bold;\\'>OPTICAL STREAM STANDBY</div><div>Ensure optical_stream_daemon.py is active on port 8502. Gateway: {stream_gw}:8502</div></div>';" />
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div style="border: 1px solid #ef4444; border-radius: 2px; padding: 30px 20px; background-color: #121722; text-align: center;">
                <div style="color: #ef4444; font-family: monospace; font-size: 1.1em; font-weight: bold;">⚠️ BROWSER SECURITY NOTICE: HTTPS REQUIRED FOR PHONE CAMERA</div>
                <div style="color: #94a3b8; font-size: 0.88em; margin-top: 8px;">
                    Mobile operating systems (iOS/Android) prohibit browser camera access over insecure HTTP connections (http://100.87.162.117).
                    To stream video from your phone, an SSL/HTTPS domain is required.
                </div>
                <div style="margin-top: 15px;">
                    <span style="color: #e2a03f; font-size: 0.85em; font-family: monospace;">Use the button below to return to the physical desktop Arducam stream.</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("🔄 Return to Desktop Arducam Feed", key="btn_return_desktop_cam", type="primary"):
            st.session_state["active_optical_mode"] = "DESKTOP_HD"
            st.rerun()

with opt_c2:
    st.markdown(f'''
        <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">
            <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px; text-transform: uppercase;">OPTICAL BUS TELEMETRY</div>
            <b>Host Hardware:</b> Arducam-1080P-HDR<br>
            <b>Bus Channels:</b> Index 1 (HD) / Index 0 (SD)<br>
            <b>Active Gateway:</b> {stream_gw}:8502<br>
            <b>Transport:</b> RFC 2046 Multipart MJPEG<br>
            <b>Watermark:</b> Driver-Inscribed<br>
            <b>Compliance:</b> DFARS 252.227-7018
        </div>
    ''', unsafe_allow_html=True)"""

def build_indented_block(raw_code, indent_spaces):
    indent = " " * indent_spaces
    return "\n".join((indent + line) if line.strip() else "" for line in raw_code.strip().splitlines())

print("=" * 80)
print("PATCHING CONSOLE CONTROLLERS WITH DESKTOP ARDUCAM DEFAULT")
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

        formatted_embed = build_indented_block(OPTICAL_LOCKED_BLOCK, indent_len)
        new_content = content[:p_start] + formatted_embed + "\n\n" + (" " * indent_len) + content[p_end:]

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Embedded Desktop Primary Viewport into {os.path.basename(fpath)}.")
    else:
        print(f"  * [WARN] Anchors not matched in {os.path.basename(fpath)}.")

print("\n" + "=" * 80)
print("DESKTOP PRIMARY PATCH COMPLETE")
print("=" * 80)
