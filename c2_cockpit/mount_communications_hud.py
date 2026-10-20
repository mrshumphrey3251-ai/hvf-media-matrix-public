import re
import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target console file not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")

render_func = '''
def render_communications_dispatch_ui():
    st.markdown("### 📬 SOVEREIGN COMMUNICATIONS DISPATCH // EXECUTIVE LEDGER")
    st.caption("Air-gapped Zero-API Email Ingestion & Autonomous Dispatch Attestation")
    
    col_act, col_stat = st.columns([2, 1])
    with col_act:
        if st.button("⚡ EXECUTE AUTONOMOUS INBOX POLL", key="btn_trigger_email_poll_hud", use_container_width=True):
            try:
                import sys
                from pathlib import Path
                _cockpit_dir = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit")
                if str(_cockpit_dir) not in sys.path:
                    sys.path.insert(0, str(_cockpit_dir))
                from ebony_email_dispatcher import poll_and_auto_dispatch
                res = poll_and_auto_dispatch()
                st.success(f"Inbox Poll Completed: Processed {len(res)} event(s).")
                st.rerun()
            except Exception as _e:
                st.error(f"Polling failure: {_e}")
                
    with col_stat:
        try:
            import json
            from pathlib import Path
            cfg_p = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit\\email_accounts.json")
            if cfg_p.exists():
                cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
                st.metric("Active Mailboxes", f"{len(cfg)} Configured")
            else:
                st.metric("Active Mailboxes", "0 Configured")
        except Exception:
            st.metric("Active Mailboxes", "Offline")
            
    try:
        import sqlite3
        import pandas as pd
        from pathlib import Path
        db_p = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit\\matrix_ledger.db")
        if db_p.exists():
            conn = sqlite3.connect(str(db_p))
            q = "SELECT timestamp AS 'Timestamp (UTC)', sender AS 'Sender', subject AS 'Subject', classification AS 'Category', status AS 'Status', drafted_response AS 'Drafted Response' FROM email_dispatch_ledger ORDER BY timestamp DESC LIMIT 25"
            df = pd.read_sql_query(q, conn)
            conn.close()
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No recorded communications in ledger.")
        else:
            st.warning("Matrix WORM database offline.")
    except Exception as _err:
        st.error(f"Cannot query ledger: {_err}")
'''

# 1. Inject render function if missing
if "def render_communications_dispatch_ui" not in content:
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines[:100]):
        if line.startswith("import ") or line.startswith("from "):
            insert_idx = i + 1
    content = "".join(lines[:insert_idx]) + "\n" + render_func + "\n" + "".join(lines[insert_idx:])
    print("[+] render_communications_dispatch_ui function injected.")

# 2. Check if tabs can be dynamically augmented
pattern = r'([a-zA-Z0-9_,\s]+)=\s*st\.tabs\(\[\s*(.*?)\s*\]\)'
matches = list(re.finditer(pattern, content, re.DOTALL))
patched_tab = False

for m in matches:
    vars_part = m.group(1).strip()
    tabs_list_str = m.group(2).strip()
    if ("SCADA" in tabs_list_str.upper() or "SWARM" in tabs_list_str.upper()) and "Communications" not in tabs_list_str:
        new_var = "tab_comm"
        new_vars = f"{vars_part}, {new_var}"
        new_tabs = f'{tabs_list_str}, "📬 Communications Dispatch"'
        replacement = f"{new_vars} = st.tabs([{new_tabs}])"
        content = content[:m.start()] + replacement + content[m.end():]
        
        append_block = f"""

with {new_var}:
    render_communications_dispatch_ui()
"""
        content += append_block
        patched_tab = True
        print(f"[+] Successfully mounted tab '{new_var}' to HUD tabs list.")
        break

if not patched_tab and "render_communications_dispatch_ui()" not in content:
    content += """

with st.expander("📬 SOVEREIGN COMMUNICATIONS DISPATCH // EXECUTIVE LEDGER", expanded=True):
    render_communications_dispatch_ui()
"""
    print("[+] Mounted communications view in primary cockpit container.")

target.write_text(content, encoding="utf-8")
print("[VERIFYING] Running py_compile on ebony_console_GREEN.py...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with exit code 0!")