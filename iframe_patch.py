import os

print("[*] Engaging Master Iframe Override...")
file_path = "ebony_console_GREEN.py"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # We aggressively inject the master hardware permissions into the iframe
    if "allow=\"camera;" not in content:
        content = content.replace("<iframe src=", "<iframe allow=\"camera; microphone; autoplay; fullscreen; display-capture\" src=")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[SUCCESS] Master permissions injected. The Comms Deck iframe is now armed.")
    else:
        print("[INFO] Iframe permissions are already present. No changes made.")
else:
    print("[FATAL] ebony_console_GREEN.py not found.")