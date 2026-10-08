import os
import sys
import re
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

print("=" * 80)
print("RESTORING STREAMLIT HEADER SYNTAX & VERIFYING AST INTEGRITY")
print("=" * 80)

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue

    print(f"\nProcessing target: {os.path.basename(fpath)}")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Repair truncated header: replace stray 💬 Encrypted... with st.subheader("💬 Encrypted...")
    # This regex catches any line containing the emoji and the closing ") that is missing st.subheader
    repaired = False
    
    # 1. Look for raw string slice errors
    pattern1 = r'^[ \t]*💬 Encrypted P2P Dispatch"\)'
    if re.search(pattern1, content, flags=re.MULTILINE):
        content = re.sub(pattern1, '    st.subheader("💬 Encrypted P2P Dispatch")', content, flags=re.MULTILINE)
        repaired = True

    # 2. Look for missing quotes
    pattern2 = r'^[ \t]*💬 Encrypted P2P Dispatch\)'
    if re.search(pattern2, content, flags=re.MULTILINE):
        content = re.sub(pattern2, '    st.subheader("💬 Encrypted P2P Dispatch")', content, flags=re.MULTILINE)
        repaired = True

    if repaired:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  * [SUCCESS] Restored Streamlit header syntax in {os.path.basename(fpath)}")
    else:
        print(f"  * [INFO] No truncated headers found matching the pattern.")

    try:
        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] AST Verified. Clean compilation with zero SyntaxErrors.")
    except Exception as e:
        print(f"  * [FAIL] Syntax validation failed: {e}")
        sys.exit(1)

print("\n" + "=" * 80)
print("SYNTAX RESTORATION COMPLETE")
print("=" * 80)
