import os
import time
import hashlib

TARGET_DIR = os.path.dirname(os.path.abspath(__file__))
# The core files we are protecting from unauthorized overwrites
TARGET_FILES = ["app.py", "hvf_memory_vault.db"]

def get_hash(filepath):
    if not os.path.exists(filepath): 
        return None
    with open(filepath, 'rb') as f: 
        return hashlib.md5(f.read()).hexdigest()

print("==================================================")
print("🛡️ KINETIC INTRUSION SENTINEL ONLINE")
print("==================================================")
print("Monitoring core architecture for unauthorized mutations...")

state = {}
for f in TARGET_FILES:
    path = os.path.join(TARGET_DIR, f)
    state[f] = get_hash(path)

try:
    while True:
        time.sleep(3)
        for f in TARGET_FILES:
            path = os.path.join(TARGET_DIR, f)
            current_hash = get_hash(path)
            
            if current_hash != state[f]:
                print(f"\n[!!!] KINETIC ALERT: UNAUTHORIZED MODIFICATION DETECTED IN {f} [!!!]")
                print(f"Timestamp: {time.ctime()}")
                # Update state to prevent alert spam, waiting for the next mutation
                state[f] = current_hash 
except KeyboardInterrupt:
    print("\n[!] Sentinel disengaged by Master CEO.")
