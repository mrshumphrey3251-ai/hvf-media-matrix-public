import os

print("[*] Engaging Mobile WebKit Optical Override...")
file_path = "hvf_intercom_broker.py"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Inject the mandatory mobile rendering tags if they are missing
    if "playsinline" not in content:
        # Force all video elements to render inline and bypass mobile autoplay blocks
        content = content.replace("<video ", "<video playsinline webkit-playsinline muted ")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[SUCCESS] Mobile WebKit tags injected. Tablet OS will now yield the lens.")
    else:
        print("[INFO] Mobile tags already present. The block is at the OS level.")
else:
    print("[FATAL] hvf_intercom_broker.py not found.")
