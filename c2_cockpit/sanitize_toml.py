import os
import sys
import toml

# ==============================================================================
# HVF Omni-Industrial Matrix | TOML BOM & CORRUPTION PURGE UTILITY
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Purge U+FEFF Byte Order Marks from Local and Global Streamlit Configs
# ==============================================================================

CLEAN_TOML_CONTENT = """[theme]
primaryColor = "#00D2FF"
backgroundColor = "#050A15"
secondaryBackgroundColor = "#111827"
textColor = "#E2E8F0"
font = "sans serif"

[server]
headless = true
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 50

[browser]
gatherUsageStats = false

[client]
showErrorDetails = true
toolbarMode = "minimal"
"""

TARGET_PATHS = [
    os.path.join(os.getcwd(), ".streamlit", "config.toml"),
    os.path.expanduser("~/.streamlit/config.toml")
]

print("=" * 80)
print("PURGING TOML ARTIFACTS & WRITING PURE UTF-8 CONFIGURATIONS")
print("=" * 80)

for path in TARGET_PATHS:
    target_dir = os.path.dirname(path)
    os.makedirs(target_dir, exist_ok=True)

    # Write pure UTF-8 without BOM
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(CLEAN_TOML_CONTENT.strip() + "\n")
    print(f"[REWRITTEN] Clean configuration written to: {path}")

    # Verify parser
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        parsed = toml.loads(raw_text)
        print(f"[VERIFIED]  Successfully parsed {path}")
        print(f"            Theme Primary: {parsed.get('theme', {}).get('primaryColor')}")
    except Exception as e:
        print(f"[FAIL]      Parse error on {path}: {e}")
        sys.exit(1)

print("=" * 80)
print("ALL STREAMLIT CONFIGURATIONS SANITIZED AND VERIFIED")
print("=" * 80)
