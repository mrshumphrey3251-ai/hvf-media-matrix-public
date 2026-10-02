import os

print("[*] Engaging Optical Override...")
file_path = "hvf_intercom_broker.py"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Sever the audio requirement to bypass the hardware crash
    content = content.replace("getUserMedia({ video: true, audio: true })", "getUserMedia({ video: true, audio: false })")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] Microphone dependency severed. Optical link prioritized.")
else:
    print("[FATAL] hvf_intercom_broker.py not found in this directory.")