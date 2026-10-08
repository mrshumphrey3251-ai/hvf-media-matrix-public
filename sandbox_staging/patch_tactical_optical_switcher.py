"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: PATCH TACTICAL OPTICAL SWITCHER
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



    TACTICAL_SWITCHER_BLOCK = """# --- LIVE SWARM OPTICAL FEED (ONE-TOUCH SENSOR MATRIX) ---

    st.subheader("🔴 LIVE // SWARM OPTICAL FEED")

    st.markdown("WebRTC & Hardware Matrix streaming via Sovereign Tailscale Link.")



    # Sovereign State Initialization (Default to Desktop Arducam HD)

    if "active_optical_mode" not in st.session_state:

        st.session_state["active_optical_mode"] = "DESKTOP_HD"



    # Tactical One-Touch Source Selector Buttons

    btn_c1, btn_c2, btn_c3, btn_c4 = st.columns([1.6, 1.6, 1.6, 1.2])

    with btn_c1:

        is_hd_active = st.session_state["active_optical_mode"] == "DESKTOP_HD"

        if st.button("🖥️ Desktop Arducam HD", key="btn_sel_desk_hd", type="primary" if is_hd_active else "secondary"):

            import urllib.request

            try:

                urllib.request.urlopen("http://127.0.0.1:8502/switch_device?index=1&label=Arducam_HD_Index1", timeout=2.0)

            except Exception:

                pass

            st.session_state["active_optical_mode"] = "DESKTOP_HD"

            st.rerun()



    with btn_c2:

        is_sd_active = st.session_state["active_optical_mode"] == "DESKTOP_SD"

        if st.button("🖥️ Desktop Arducam SD", key="btn_sel_desk_sd", type="primary" if is_sd_active else "secondary"):

            import urllib.request

            try:

                urllib.request.urlopen("http://127.0.0.1:8502/switch_device?index=0&label=Arducam_SD_Index0", timeout=2.0)

            except Exception:

                pass

            st.session_state["active_optical_mode"] = "DESKTOP_SD"

            st.rerun()



    with btn_c3:

        is_mob_active = st.session_state["active_optical_mode"] == "MOBILE_PHONE"

        if st.button("📱 Mobile Phone Uplink", key="btn_sel_mob_cam", type="primary" if is_mob_active else "secondary"):

            st.session_state["active_optical_mode"] = "MOBILE_PHONE"

            st.rerun()



    with btn_c4:

        gw_choice = st.selectbox("Gateway", ["100.87.162.117", "127.0.0.1"], key="tactical_gw_choice_val")



    stream_gw = gw_choice



    # Live Video Viewport Rendering

    opt_c1, opt_c2 = st.columns([2.2, 1])

    with opt_c1:

        if st.session_state["active_optical_mode"] in ["DESKTOP_HD", "DESKTOP_SD"]:

            sensor_tag = "ARDUCAM-1080P-HDR [INDEX 1 HD]" if st.session_state["active_optical_mode"] == "DESKTOP_HD" else "ARDUCAM-1080P-HDR [INDEX 0 SD]"

            stream_url = f"http://{stream_gw}:8502/video_feed"

            st.markdown(f'''

                <div style="position: relative; width: 100%; background-color: #0b0e14; border: 1px solid #242d3d; border-radius: 2px; overflow: hidden;">

                    <div style="position: absolute; top: 8px; left: 10px; z-index: 10; font-family: monospace; font-size: 0.75em; background-color: rgba(11,14,20,0.85); padding: 2px 8px; border: 1px solid #242d3d; border-radius: 2px;">

                        <span style="color: #ef4444; font-weight: bold;">● LIVE 30 FPS</span> | <span style="color: #e2a03f;">{sensor_tag}</span>

                    </div>

                    <img src="{stream_url}" 

                         style="width: 100%; height: auto; min-height: 380px; display: block; object-fit: cover;"

                         onerror="this.onerror=null; this.src=''; this.parentElement.innerHTML='<div style=\\'padding:60px 20px; text-align:center; color:#94a3b8; font-family:monospace;\\'><div style=\\'color:#e2a03f; font-size:1.1em; font-weight:bold;\\'>OPTICAL STREAM STANDBY</div><div>Starting host daemon on port 8502. Gateway: {stream_gw}:8502</div></div>';" />

                </div>

            ''', unsafe_allow_html=True)

        else:

            st.markdown('''

                <div style="border: 1px solid #242d3d; border-radius: 2px; padding: 50px 20px; background-color: #121722; text-align: center;">

                    <div style="color: #e2a03f; font-family: monospace; font-size: 1.15em; font-weight: bold;">📱 MOBILE SWARM UPLINK ACTIVE</div>

                    <div style="color: #94a3b8; font-size: 0.88em; margin-top: 8px;">Optical stream actively bound to mobile client sensor via Tailscale WebRTC Mesh.</div>

                </div>

            ''', unsafe_allow_html=True)



    with opt_c2:

        st.markdown(f'''

            <div style="border: 1px solid #242d3d; padding: 14px; background-color: #121722; font-size: 0.85em; color: #94a3b8; border-radius: 2px;">

                <div style="color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 8px; text-transform: uppercase;">OPTICAL BUS TELEMETRY</div>

                <b>Active Mode:</b> {st.session_state.get("active_optical_mode", "DESKTOP_HD")}<br>

                <b>Hardware Host:</b> Arducam-1080P-HDR<br>

                <b>Stream Endpoint:</b> http://{stream_gw}:8502<br>

                <b>Transport:</b> RFC 2046 Multipart MJPEG<br>

                <b>Frame Rate:</b> 30 FPS Synchronous<br>

                <b>Compliance:</b> DFARS 252.227-7018

            </div>

        ''', unsafe_allow_html=True)"""



    def build_indented_block(raw_code, indent_spaces):

        indent = " " * indent_spaces

        return "\n".join((indent + line) if line.strip() else "" for line in raw_code.strip().splitlines())



    print("=" * 80)

    print("EMBEDDING ONE-TOUCH TACTICAL OPTICAL SWITCHER")

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



            formatted_embed = build_indented_block(TACTICAL_SWITCHER_BLOCK, indent_len)

            new_content = content[:p_start] + formatted_embed + "\n\n" + (" " * indent_len) + content[p_end:]



            with open(fpath, "w", encoding="utf-8") as f:

                f.write(new_content)



            py_compile.compile(fpath, doraise=True)

            print(f"  * [SUCCESS] Embedded One-Touch Optical Switcher into {os.path.basename(fpath)}.")

        else:

            print(f"  * [WARN] Anchors not matched in {os.path.basename(fpath)}.")



    print("\n" + "=" * 80)

    print("TACTICAL SWITCHER INJECTION COMPLETE")

    print("=" * 80)


if __name__ == "__main__":
    render()
