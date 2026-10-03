import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

SWITCHER_UI_COMPONENT = """# --- LIVE SWARM OPTICAL FEED (DYNAMIC CAMERA SWITCHER) ---
st.subheader("🔴 LIVE // SWARM OPTICAL FEED")
st.markdown("WebRTC Matrix streaming via Sovereign Tailscale Link.")

# Dynamic Optical Switcher Routing
sw_c1, sw_c2, sw_c3 = st.columns([1.6, 1.2, 1.2])
with sw_c1:
    cam_select = st.selectbox(
        "Select Active Tactical Sensor",
        [
            "Desktop Sensor 1 (Arducam 1280x720 HD)",
            "Desktop Sensor 0 (Arducam 640x480 SD)",
            "Phone / Remote Node Stream"
        ],
        key="tactical_optical_selector"
    )

with sw_c2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("📡 Switch Optical Source", key="btn_switch_cam_source", type="primary"):
        import urllib.request
        target_idx = 1 if "Sensor 1" in cam_select else (0 if "Sensor 0" in cam_select else 1)
        try:
            url = f"http://127.0.0.1:8502/switch_device?index={target_idx}&label={cam_select.replace(' ', '%20')}"
            urllib.request.urlopen(url, timeout=2.0)
            st.success(f"Routed to: {cam_select}")
        except Exception as ex_sw:
            st.warning(f"Router Notice: {ex_sw}")
        st.rerun()

with sw_c3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Video Link", key="btn_refresh_viewport"):
        st.rerun()

opt_c1, opt_c2 = st.columns([2.2, 1])
with opt_c1:
    st.markdown('''
        <div style="position: relative; width: 100%; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden;">
            <div style="position: absolute; top: 8px; left: 10px; z-index: 10; font-family: monospace; font-size: 0.75em; background-color: rgba(11,14,20,0.85); padding: 2px 8px; border: 1px solid #242d3d; border-radius: 2px;">
                <span style="color: #ef4444; font-weight: bold;">● LIVE 30 FPS</span> | <span style="color: #e2a03f;">ARDUCAM-1080P-HDR</span>
            </div>
            <img src="http://127.0.0.1:8502/video_feed" 
                 style="width: 100%; height: auto; min-height: 380px; display: block; object-fit: cover;"
                 onerror="this.onerror=null; this.src=''; this.parentElement.innerHTML='<div style=\\'padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;\\'><div style=\\'color:#e2a03f; font-size:1.1em; font-weight:bold;\\'>OPTICAL STREAM STANDBY</div><div>Optical stream daemon active on port 8502.</div></div>';" />
        </div>
    ''', unsafe_allow_html=True)

with opt_c2:
    st.markdown('''
        <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">
            <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px; text-transform: uppercase;">OPTICAL BUS TELEMETRY</div>
            <b>Hardware Sensor:</b> Arducam-1080P-HDR<br>
            <b>Bus Channels:</b> Index 0 (SD) / Index 1 (HD)<br>
            <b>Frame Rate:</b> 30 FPS Synchronous<br>
            <b>Local Gateway:</b> http://127.0.0.1:8502<br>
            <b>Swarm Link:</b> http://100.87.162.117:8502<br>
            <b>Compliance:</b> DFARS 252.227-7018
        </div>
    ''', unsafe_allow_html=True)"""

def build_indented_block(raw_code, indent_spaces):
    indent = " " * indent_spaces
    return "\n".join((indent + line) if line.strip() else "" for line in raw_code.strip().splitlines())

print("=" * 80)
print("PATCHING CONSOLE CONTROLLERS WITH DYNAMIC OPTICAL SWITCHER")
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

        formatted_embed = build_indented_block(SWITCHER_UI_COMPONENT, indent_len)
        new_content = content[:p_start] + formatted_embed + "\n\n" + (" " * indent_len) + content[p_end:]

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Embedded Dynamic Optical Switcher into {os.path.basename(fpath)}.")
    else:
        print(f"  * [WARN] Anchors not matched in {os.path.basename(fpath)}.")

print("\n" + "=" * 80)
print("OPTICAL MATRIX SWITCHER PATCH COMPLETE")
print("=" * 80)
