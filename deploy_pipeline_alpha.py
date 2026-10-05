import os

file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

marker = 'elif active_module == "🌾 Drone Diagnostics":'

if marker in content:
    # Ensure we don't inject it twice
    if "PIPELINE ALPHA" not in content:
        parts = content.split(marker, 1)
        injection = marker + """
    st.subheader("🌾 SWARM SCADA // PIPELINE ALPHA")
    st.caption("One-way optical ingestion from the WebRTC Master Media Router.")
    
    st.components.v1.html(
        '<iframe src="http://100.87.162.117:8889/live/stream" width="100%" height="600" style="border:none;" allow="autoplay; fullscreen; camera"></iframe>',
        height=620
    )
    st.markdown("---")
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(parts[0] + injection + parts[1])
        print("[SUCCESS] Pipeline Alpha deployed to Drone Diagnostics.")
    else:
        print("[SUCCESS] Pipeline Alpha is already deployed.")
else:
    print("[FATAL] Drone Diagnostics marker not found.")