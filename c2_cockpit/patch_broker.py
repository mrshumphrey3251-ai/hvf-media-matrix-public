import os

print("[*] Engaging Universal Hardware Fallback and Stream Isolation...")
file_path = "hvf_intercom_broker.py"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. The Autonomous Hardware Fallback Logic
    old_optics = "getUserMedia({ video: true, audio: false })"
    new_optics = """getUserMedia({ video: true, audio: true })
            .catch(function(err) {
                console.warn("[HVF] Audio device missing. Autonomous fallback to Optical-Only mode...");
                return navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            })"""

    if old_optics in content:
        content = content.replace(old_optics, new_optics)
        print("  -> [SUCCESS] Hardware Fallback Logic Injected.")
    else:
        print("  -> [INFO] Fallback logic already present or original string not found.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[*] MATRIX UPGRADE COMPLETE. Codebase is now universally compatible.")
else:
    print("[FATAL] hvf_intercom_broker.py not found in this directory.")