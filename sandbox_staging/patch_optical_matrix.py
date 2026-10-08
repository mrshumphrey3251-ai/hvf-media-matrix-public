"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: PATCH OPTICAL MATRIX
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



    SWARM_SWITCHER_COMPONENT = """# --- LIVE SWARM OPTICAL FEED (HOST-TO-SWARM MATRIX SWITCHER) ---

    st.subheader("🔴 LIVE // SWARM OPTICAL FEED")

    st.markdown("WebRTC & Hardware Matrix streaming via Sovereign Tailscale Link.")



    # Gateway & Source Matrix Controls

    gw_c1, gw_c2, gw_c3 = st.columns([1.5, 1.5, 1.2])

    with gw_c1:

        optical_source = st.radio(

            "Active Optical Feed Source",

            ["Desktop Hardware Sensor (Arducam-1080P-HDR)", "Mobile Swarm Uplink (Phone Camera)"],

            key="opt_feed_source_sel"

        )



    with gw_c2:

        if optical_source == "Desktop Hardware Sensor (Arducam-1080P-HDR)":

            desktop_cam_choice = st.selectbox(

                "Desktop Hardware Sensor Bus",

                ["Sensor Index 1 (Arducam 1280x720 HD)", "Sensor Index 0 (Arducam 640x480 SD)"],

                key="desktop_cam_index_sel"

            )

        else:

            st.markdown("<div style='font-size:0.85em; color:#94a3b8; margin-top:24px;'>Using mobile client WebRTC sensor link.</div>", unsafe_allow_html=True)



    with gw_c3:

        network_gw = st.selectbox(

            "Stream Gateway Link",

            ["Tailscale Swarm (100.87.162.117)", "Localhost (127.0.0.1)"],

            key="opt_network_gw_sel"

        )



    gw_ip = "100.87.162.117" if "Tailscale" in network_gw else "127.0.0.1"



    # Switch Action Button

    col_sw_act1, col_sw_act2 = st.columns([1.5, 2.5])

    with col_sw_act1:

        if st.button("📡 Apply Optical Routing", key="btn_apply_optical_switch", type="primary"):

            if optical_source == "Desktop Hardware Sensor (Arducam-1080P-HDR)":

                import urllib.request

                target_idx = 1 if "Index 1" in desktop_cam_choice else 0

                try:

                    url = f"http://127.0.0.1:8502/switch_device?index={target_idx}&label=DesktopSensor{target_idx}"

                    urllib.request.urlopen(url, timeout=2.0)

                    st.success(f"Desktop optical bus routed to Index [{target_idx}].")

                except Exception as ex_sw:

                    st.warning(f"Daemon link notice: {ex_sw}")

            st.rerun()



    # Display Viewport

    opt_c1, opt_c2 = st.columns([2.2, 1])

    with opt_c1:

        if optical_source == "Desktop Hardware Sensor (Arducam-1080P-HDR)":

            stream_url = f"http://{gw_ip}:8502/video_feed"

            st.markdown(f'''

                <div style="position: relative; width: 100%; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden;">

                    <div style="position: absolute; top: 8px; left: 10px; z-index: 10; font-family: monospace; font-size: 0.75em; background-color: rgba(11,14,20,0.85); padding: 2px 8px; border: 1px solid #242d3d; border-radius: 2px;">

                        <span style="color: #ef4444; font-weight: bold;">● LIVE 30 FPS</span> | <span style="color: #e2a03f;">ARDUCAM-1080P-HDR (DESKTOP)</span>

                    </div>

                    <img src="{stream_url}" 

                         style="width: 100%; height: auto; min-height: 380px; display: block; object-fit: cover;"

                         onerror="this.onerror=null; this.src=''; this.parentElement.innerHTML='<div style=\\'padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;\\'><div style=\\'color:#e2a03f; font-size:1.1em; font-weight:bold;\\'>OPTICAL STREAM STANDBY</div><div>Start optical_stream_daemon.py on port 8502. Gateway: {gw_ip}:8502</div></div>';" />

                </div>

            ''', unsafe_allow_html=True)

        else:

            st.markdown('''

                <div style="border: 1px solid #242d3d; border-radius: 2px; padding: 40px 20px; background-color: #121722; text-align: center;">

                    <div style="color: #e2a03f; font-family: monospace; font-size: 1.1em; font-weight: bold;">📱 MOBILE SWARM UPLINK ACTIVE</div>

                    <div style="color: #94a3b8; font-size: 0.88em; margin-top: 8px;">Optical stream actively bound to mobile client sensor via Tailscale WebRTC Mesh.</div>

                </div>

            ''', unsafe_allow_html=True)



    with opt_c2:

        st.markdown(f'''

            <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">

                <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px; text-transform: uppercase;">OPTICAL BUS TELEMETRY</div>

                <b>Host Hardware:</b> Arducam-1080P-HDR<br>

                <b>Bus Channels:</b> Index 1 (HD) / Index 0 (SD)<br>

                <b>Active Gateway:</b> {gw_ip}:8502<br>

                <b>Transport:</b> RFC 2046 Multipart MJPEG<br>

                <b>Cross-Origin:</b> Global CORS Authorized<br>

                <b>Compliance:</b> DFARS 252.227-7018

            </div>

        ''', unsafe_allow_html=True)"""



    def build_indented_block(raw_code, indent_spaces):

        indent = " " * indent_spaces

        return "\n".join((indent + line) if line.strip() else "" for line in raw_code.strip().splitlines())



    print("=" * 80)

    print("PATCHING CONSOLE CONTROLLERS WITH HOST-TO-SWARM MATRIX SWITCHER")

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



            formatted_embed = build_indented_block(SWARM_SWITCHER_COMPONENT, indent_len)

            new_content = content[:p_start] + formatted_embed + "\n\n" + (" " * indent_len) + content[p_end:]



            with open(fpath, "w", encoding="utf-8") as f:

                f.write(new_content)



            py_compile.compile(fpath, doraise=True)

            print(f"  * [SUCCESS] Embedded Host-to-Swarm Matrix Switcher into {os.path.basename(fpath)}.")

        else:

            print(f"  * [WARN] Anchors not matched in {os.path.basename(fpath)}.")



    print("\n" + "=" * 80)

    print("HOST-TO-SWARM MATRIX SWITCHER PATCH COMPLETE")

    print("=" * 80)


if __name__ == "__main__":
    render()
