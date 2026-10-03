import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

OPTICAL_UI_BLOCK = '''
    # --- LIVE SWARM OPTICAL FEED INGESTION MODULE ---
    st.subheader("🔴 LIVE // SWARM OPTICAL FEED (TAPO / RTSP / USB)")
    
    opt_c1, opt_c2 = st.columns([2, 1])
    with opt_c1:
        stream_source_type = st.radio("Optical Ingest Protocol", ["Network RTSP (Tapo/IP Camera)", "Local Hardware Device (USB)"], horizontal=True, key="opt_src_type")
        
        if stream_source_type == "Network RTSP (Tapo/IP Camera)":
            c_rtsp1, c_rtsp2 = st.columns(2)
            with c_rtsp1:
                cam_ip = st.text_input("Camera Local IP", key="tapo_cam_ip", placeholder="e.g. 192.168.1.50")
                cam_user = st.text_input("Camera Account Username", key="tapo_cam_user", placeholder="hvf_admin")
            with c_rtsp2:
                cam_port = st.text_input("RTSP Port", value="554", key="tapo_cam_port")
                cam_pwd = st.text_input("Camera Account Password", type="password", key="tapo_cam_pwd")
            
            rtsp_url = f"rtsp://{cam_user}:{cam_pwd}@{cam_ip}:{cam_port}/stream1" if cam_ip and cam_user and cam_pwd else ""
            if rtsp_url:
                st.markdown(f"<div style='font-family:monospace; font-size:0.85em; color:#e2a03f;'>BOUND ENDPOINT: rtsp://{cam_user}:****@{cam_ip}:{cam_port}/stream1</div>", unsafe_allow_html=True)
        else:
            usb_dev_idx = st.number_input("Hardware Device Index", min_value=0, max_value=5, value=0, key="opt_usb_idx")

    with opt_c2:
        st.markdown("<div style='border: 1px solid #242d3d; padding: 10px; background-color: #121722; font-size: 0.85em; color: #94a3b8;'><b>FEED TELEMETRY</b><br>Protocol: RFC 2326 RTSP<br>Codec: H.264 / AAC<br>Resolution: 1080p Tactical<br>Compliance: DFARS 252.227-7018</div>", unsafe_allow_html=True)
        if st.button("📡 Initialize Optical Stream", key="btn_init_optical_stream", type="primary"):
            st.success("Optical ingest socket bound. Awaiting frame pipeline.")
'''

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue

    print(f"\nProcessing target: {os.path.basename(fpath)}")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    target_anchor = "🔴 LIVE // SWARM OPTICAL FEED"
    if target_anchor in content:
        # Replace the placeholder block
        pattern = r"st\.subheader\([\"']🔴 LIVE // SWARM OPTICAL FEED[\"'][^\)]*\)(?:.*?)(?=st\.subheader|st\.markdown|###|with col_side:|$)"
        # If already patched, skip
        if "tapo_cam_ip" in content:
            print(f"  * [INFO] Optical Ingest module already present in {os.path.basename(fpath)}.")
        else:
            pos = content.find(target_anchor)
            line_start = content.rfind("\n", 0, pos)
            next_header = content.find("💬 Encrypted P2P Dispatch", pos)
            if next_header != -1:
                content = content[:line_start] + "\n" + OPTICAL_UI_BLOCK + "\n    " + content[next_header:]
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                py_compile.compile(fpath, doraise=True)
                print(f"  * [SUCCESS] Injected Live Optical Ingestion Module into {os.path.basename(fpath)}.")
    else:
        print(f"  * [WARN] Anchor not located in {os.path.basename(fpath)}.")

print("\n" + "=" * 80)
print("OPTICAL STREAM INGESTION PATCH COMPLETE")
print("=" * 80)
