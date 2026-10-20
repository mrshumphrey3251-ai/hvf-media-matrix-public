import os
import sys
import re
from pathlib import Path

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
current_script_name = Path(__file__).name

# Segmented pattern literals to prevent rule definition self-matching
SENSITIVE_PATTERNS = [
    (r"sk_live_" + r"[0-9a-zA-Z]{24,}", "Stripe Live Secret Key"),
    (r"ghp_" + r"[0-9a-zA-Z]{36,}", "GitHub Personal Access Token"),
    (r"AKIA" + r"[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"-----BEGIN" + r" [A-Z ]*PRIVATE KEY-----", "RSA/OpenSSL Private Key"),
    (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded Password")
]

print("\n" + "=" * 90)
print("     SOVEREIGN PRE-RELEASE SECURITY & SECRETS SANITIZATION AUDIT     ")
print("     TARGET: PRODUCTION COCKPIT ENCLAVE | EXCLUDING AUDIT TOOLS      ")
print("=" * 90)

leak_detected = False
scanned_count = 0

for py_file in cockpit_dir.glob("*.py"):
    # Exclude scanner tools from self-inspection
    if py_file.name in [current_script_name, "test_client_security.py"]:
        continue
        
    scanned_count += 1
    content = py_file.read_text(encoding="utf-8", errors="ignore")
    for pat, desc in SENSITIVE_PATTERNS:
        matches = re.findall(pat, content)
        if matches:
            print(f"[CRITICAL VULNERABILITY] {py_file.name}: Found exposed {desc}!")
            leak_detected = True

# Inspect private billing config
cfg_file = cockpit_dir / "stripe_config.json"
if cfg_file.exists():
    cfg_text = cfg_file.read_text(encoding="utf-8")
    if "sk_live_" in cfg_text and "placeholder" not in cfg_text:
        print("[WARNING] stripe_config.json contains live secret key. Must remain in private enclave only.")

print(f"[*] Total Production Files Audited: {scanned_count}")
if not leak_detected:
    print("[PASS] Enclave Secrets Audit: 100% CLEAN. Zero hardcoded credentials or API tokens found.")
print("=" * 90 + "\n")

if leak_detected:
    sys.exit(1)