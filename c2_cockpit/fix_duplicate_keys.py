import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target console not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

# 1. Locate and remove the rogue sidebar call to render_communications_dispatch_ui
cleaned_lines = []
for i, line in enumerate(lines):
    if "render_communications_dispatch_ui()" in line and not line.strip().startswith("def "):
        # If line is before main dispatch module, drop it to eliminate sidebar duplicate
        if i < 1115 and ("with st.sidebar" in "".join(lines[max(0, i-25):i]) or "expander" in "".join(lines[max(0, i-5):i])):
            print(f"[+] Purging duplicate sidebar call at line {i+1}: {line.strip()}")
            continue
    cleaned_lines.append(line)

content = "".join(cleaned_lines)

updated_render_func = """def render_communications_dispatch_ui(key_suffix="deck"):
    st.divider()
    st.markdown("### 📋 SOVEREIGN COMMUNICATIONS AUDIT LEDGER")
    st.caption("Air-gapped Zero-API Email Ingestion & Autonomous Dispatch Attestation // Local WORM Ledger")
    
    col_act, col_stat = st.columns([2, 1])
    with col_act:
        if st.button("⚡ EXECUTE AUTONOMOUS INBOX POLL", key=f"btn_trigger_email_poll_{key_suffix}", use_container_width=True):
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
"""

# 2. String slice replacement (bypassing re.sub escape sequence bugs)
start_idx = content.find("def render_communications_dispatch_ui")
if start_idx != -1:
    end_idx = content.find("def ", start_idx + 10)
    if end_idx == -1:
        end_idx = len(content)
    content = content[:start_idx] + updated_render_func + "\n\n" + content[end_idx:]
    print("[+] UI rendering block upgraded with isolated element keys.")

target.write_text(content, encoding="utf-8")

print("[*] Running py_compile verification...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")