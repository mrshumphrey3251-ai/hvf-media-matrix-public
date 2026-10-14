import re
import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target console not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")

render_func = '''
def render_communications_dispatch_ui():
    st.divider()
    st.markdown("### 📋 SOVEREIGN COMMUNICATIONS AUDIT LEDGER")
    st.caption("Air-gapped Zero-API Email Ingestion & Autonomous Dispatch Attestation // Local WORM Ledger")
    
    col_act, col_stat = st.columns([2, 1])
    with col_act:
        if st.button("⚡ EXECUTE AUTONOMOUS INBOX POLL", key="btn_trigger_email_poll_deck", use_container_width=True):
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

# 1. Ensure render function is injected near top
if "def render_communications_dispatch_ui" not in content:
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines[:120]):
        if line.startswith("import ") or line.startswith("from "):
            insert_idx = i + 1
    content = "".join(lines[:insert_idx]) + "\n" + render_func + "\n" + "".join(lines[insert_idx:])
    print("[+] Injected render_communications_dispatch_ui function.")

# 2. Revert Cockpit HUD tabs back to the 3 standard tabs
content = re.sub(
    r'tab_ledger,\s*tab_scada,\s*tab_swarm,\s*tab_comm\s*=\s*st\.tabs\(\[\s*["\']C2 Audit Ledger["\'],\s*["\']SCADA Telemetry["\'],\s*["\']Agent Swarm["\'],\s*["\'][^"\']+["\']\s*\]\)',
    'tab_ledger, tab_scada, tab_swarm = st.tabs(["C2 Audit Ledger", "SCADA Telemetry", "Agent Swarm"])',
    content
)

# 3. Strip any with tab_comm: blocks
lines = content.splitlines(keepends=True)
no_tab_comm = []
skip = False
for line in lines:
    if line.strip() == "with tab_comm:":
        skip = True
        continue
    if skip:
        if "render_communications_dispatch_ui" in line:
            skip = False
            continue
        elif line.strip() == "":
            continue
        else:
            skip = False
    no_tab_comm.append(line)

print("[+] Reverted Cockpit HUD tabs to 3 baseline channels and purged tab_comm references.")

# 4. Inject render_communications_dispatch_ui() into Sovereign Dispatch Deck
deck_start = -1
for i, line in enumerate(no_tab_comm):
    if "SOVEREIGN DISPATCH & STRATEGIC TRIAGE DECK" in line or '"📨 Sovereign Dispatch Deck"' in line:
        deck_start = i
        break

if deck_start == -1:
    print("[ERROR] Could not find Sovereign Dispatch Deck module.")
    sys.exit(1)

# Find enclosing if/elif for Dispatch Deck
if_line_idx = -1
deck_indent = ""
for i in range(deck_start, -1, -1):
    l = no_tab_comm[i]
    if l.strip().startswith("if ") or l.strip().startswith("elif "):
        if_line_idx = i
        deck_indent = l[:len(l) - len(l.lstrip())]
        break

# Find end of Dispatch Deck block
block_end_idx = -1
for i in range(if_line_idx + 1, len(no_tab_comm)):
    l = no_tab_comm[i]
    if l.strip() == "":
        continue
    l_indent = l[:len(l) - len(l.lstrip())]
    if len(l_indent) <= len(deck_indent) and (l.strip().startswith("elif ") or l.strip().startswith("else ") or l.strip().startswith("def ") or len(l_indent) < len(deck_indent)):
        block_end_idx = i
        break

if block_end_idx == -1:
    block_end_idx = len(no_tab_comm)

body_indent = deck_indent + "    "
insert_block = [
    f"\n{body_indent}render_communications_dispatch_ui()\n"
]

final_lines = no_tab_comm[:block_end_idx] + insert_block + no_tab_comm[block_end_idx:]
target.write_text("".join(final_lines), encoding="utf-8")
print(f"[+] Mounted communications audit ledger directly inside Sovereign Dispatch Deck at line {block_end_idx + 1}.")

print("[*] Running py_compile verification...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")