import os

file_path = r"C:\HVF_Repos\hvf-media-matrix-private\ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if 'if "current_linkedin_draft" not in st.session_state:' not in content:
    insert_target = 'if "demo_mode" not in st.session_state:\n    st.session_state.demo_mode = False'
    missing_code = """

if "current_linkedin_draft" not in st.session_state:
    st.session_state.current_linkedin_draft = (
        "⚡ [HVF Sovereign Intelligence Announcement]\\n\\n"
        "Humphrey Virtual Farm has deployed our on-premise universal aerial reconnaissance link, fusing real-time drone telemetry (DJI, Autel, Skydio, Custom RTMP) with our local soil sensor mesh.\\n\\n"
        "All imagery and field analytics are computed strictly on-premise without reliance on external cloud infrastructure.\\n\\n"
        "#AgTech #SovereignAI #JefferyHumphrey #AutonomousFarming #PrecisionAg #HVF"
    )
"""
    content = content.replace(insert_target, insert_target + missing_code)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ [STEP 1 COMPLETE]: LinkedIn session state patched successfully.")
else:
    print("✅ [STEP 1 COMPLETE]: Patch already applied.")