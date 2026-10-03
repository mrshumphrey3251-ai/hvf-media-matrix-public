import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

DIRECTSHOW_STREAM_BLOCK = '''    # --- LIVE SWARM OPTICAL FEED INGESTION MODULE ---
    st.subheader("🔴 LIVE // SWARM OPTICAL FEED (TAPO / RTSP / DIRECTSHOW USB)")

    opt_c1, opt_c2 = st.columns([2, 1])
    with opt_c1:
        stream_src = st.radio("Optical Ingest Protocol", ["Local Hardware Device (USB DirectShow)", "Network RTSP (Tapo / IP Camera)"], horizontal=True, key="opt_src_sel")

        if stream_src == "Local Hardware Device (USB DirectShow)":
            dev_choice = st.selectbox("Select Active Optical Sensor", ["Device Index 0 (640x480 Tactical Stream)", "Device Index 1 (1280x720 High-Definition Stream)"], key="opt_dev_choice")
            active_idx = 0 if "Index 0" in dev_choice else 1

            col_cap1, col_cap2 = st.columns([1.5, 2])
            with col_cap1:
                if st.button("📸 Capture Live Tactical Frame", key="btn_grab_directshow_frame", type="primary"):
                    try:
                        import cv2
                        cap = cv2.VideoCapture(active_idx, cv2.CAP_DSHOW)
                        if cap.isOpened():
                            ret, frame = cap.read()
                            cap.release()
                            if ret and frame is not None:
                                # Convert BGR to RGB for Streamlit rendering
                                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                st.session_state["live_optical_frame"] = rgb_frame
                                st.session_state["live_optical_ts"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
                                st.success(f"Frame acquired from Sensor Index [{active_idx}].")
                            else:
                                st.error("Sensor device opened but returned an empty frame.")
                        else:
                            st.error(f"Failed to bind DirectShow sensor at Index [{active_idx}].")
                    except Exception as ex_cam:
                        st.error(f"Optical capture error: {ex_cam}")

            if "live_optical_frame" in st.session_state:
                st.image(
                    st.session_state["live_optical_frame"], 
                    caption=f"SENSOR [{active_idx}] TELEMETRY // ACQUIRED: {st.session_state.get('live_optical_ts', '')}", 
                    use_container_width=True
                )
        else:
            c_rtsp1, c_rtsp2 = st.columns(2)
            with c_rtsp1:
                cam_ip = st.text_input("Camera Local IP", key="tapo_cam_ip_val", placeholder="e.g. 192.168.1.50")
                cam_user = st.text_input("Camera Account Username", key="tapo_cam_user_val", placeholder="hvf_admin")
            with c_rtsp2:
                cam_port = st.text_input("RTSP Port", value="554", key="tapo_cam_port_val")
                cam_pwd = st.text_input("Camera Account Password", type="password", key="tapo_cam_pwd_val")

            if cam_ip and cam_user and cam_pwd:
                st.markdown(f"<div style='font-family:monospace; font-size:0.85em; color:#e2a03f;'>BOUND RTSP: rtsp://{cam_user}:****@{cam_ip}:{cam_port}/stream1</div>", unsafe_allow_html=True)
                if st.button("📡 Ingest RTSP Frame", key="btn_grab_rtsp_frame"):
                    try:
                        import cv2
                        rtsp_url = f"rtsp://{cam_user}:{cam_pwd}@{cam_ip}:{cam_port}/stream1"
                        cap = cv2.VideoCapture(rtsp_url)
                        if cap.isOpened():
                            ret, frame = cap.read()
                            cap.release()
                            if ret and frame is not None:
                                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                st.image(rgb_frame, caption=f"RTSP NODE: {cam_ip} // 1080p Tactical Ingest", use_container_width=True)
                            else:
                                st.error("RTSP stream connected but frame decode failed.")
                        else:
                            st.error("Failed to connect to RTSP endpoint over port 554.")
                    except Exception as ex_rtsp:
                        st.error(f"RTSP ingest error: {ex_rtsp}")

    with opt_c2:
        st.markdown("""
            <div style='border: 1px solid #242d3d; padding: 12px; background-color: #121722; font-size: 0.85em; color: #94a3b8;'>
                <div style='color: #e2a03f; font-weight: bold; font-family: monospace; margin-bottom: 6px;'>OPTICAL BUS METRICS</div>
                <b>DirectShow Index 0:</b> 640x480 SD<br>
                <b>DirectShow Index 1:</b> 1280x720 HD<br>
                <b>Network Gateway:</b> Port 554 RTSP<br>
                <b>Encoding:</b> Raw RGB / H.264<br>
                <b>Classification:</b> DFARS 252.227-7018
            </div>
        """, unsafe_allow_html=True)'''

print("=" * 80)
print("INJECTING DIRECTSHOW LIVE VIDEO FRAME PIPELINE")
print("=" * 80)

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue

    print(f"\nProcessing target: {os.path.basename(fpath)}")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Anchor to the start of the optical feed module
    target_start = "st.subheader(\"🔴 LIVE // SWARM OPTICAL FEED"
    if target_start not in content:
        target_start = "🔴 LIVE // SWARM OPTICAL FEED"

    if target_start in content:
        pos_start = content.find(target_start)
        line_start = content.rfind("\n", 0, pos_start)

        # Find the next header (Encrypted P2P Dispatch)
        next_header = content.find("💬 Encrypted P2P Dispatch", pos_start)
        if next_header != -1:
            line_end = content.rfind("\n", 0, next_header)
            new_content = content[:line_start+1] + DIRECTSHOW_STREAM_BLOCK + "\n\n" + content[line_end+1:]
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            py_compile.compile(fpath, doraise=True)
            print(f"  * [SUCCESS] Injected DirectShow video pipeline into {os.path.basename(fpath)}.")
        else:
            print(f"  * [WARN] Next header 'Encrypted P2P Dispatch' not found in {os.path.basename(fpath)}.")
    else:
        print(f"  * [WARN] Optical feed anchor not found in {os.path.basename(fpath)}.")

print("\n" + "=" * 80)
print("DIRECTSHOW PIPELINE INTEGRATION COMPLETE")
print("=" * 80)
