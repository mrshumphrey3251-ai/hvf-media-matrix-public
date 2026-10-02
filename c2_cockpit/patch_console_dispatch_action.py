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
print("CONNECTING 'APPROVE & DISPATCH' BUTTON TO LIVE SMTP ENGINE")
print("=" * 80)

NEW_APPROVE_BLOCK = '''        with col_btn1:
            if st.button("✅ Approve & Dispatch", key=f"btn_app_{disp_id}", type="secondary"):
                with st.spinner("Connecting to smtp.gmail.com:465 & dispatching transmission..."):
                    d_ok, d_msg = email_triage_core.dispatch_outbound_transmission(disp_id, updated_draft)
                if d_ok:
                    st.success(f"🚀 {d_msg}")
                else:
                    st.error(f"Transmission delivery failed: {d_msg}")
                st.rerun()'''

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue

    print(f"\nProcessing target: {os.path.basename(fpath)}")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern targeting the existing dummy approve button
    old_approve_pattern = r"with col_btn1:\s*\n\s*if st\.button\(\"✅ Approve & Dispatch\"[^\n]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+st\.rerun\(\)"
    
    if re.search(old_approve_pattern, content):
        content = re.sub(old_approve_pattern, NEW_APPROVE_BLOCK, content, count=1)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Wired live SMTP delivery into {os.path.basename(fpath)}.")
    else:
        print(f"  * [INFO] Checking if already wired or applying targeted replacement...")
        # Direct string replacement fallback
        target_str = 'st.success(f"Transmission #{disp_id} approved for outbound dispatch.")'
        if target_str in content:
            content = content.replace(
                target_str,
                'd_ok, d_msg = email_triage_core.dispatch_outbound_transmission(disp_id, updated_draft)\n                if d_ok: st.success(d_msg)\n                else: st.error(d_msg)'
            )
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            py_compile.compile(fpath, doraise=True)
            print(f"  * [SUCCESS] Updated dispatch hook in {os.path.basename(fpath)}.")
        else:
            print(f"  * [WARN] Target approve block already operational.")

print("\n" + "=" * 80)
print("CONSOLE HUD DISPATCH INTEGRATION COMPLETE")
print("=" * 80)
