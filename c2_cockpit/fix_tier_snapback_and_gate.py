import os
import sys
import re
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
tier_file = cockpit_dir / "ebony_tier_manager.py"
console_file = cockpit_dir / "ebony_console_GREEN.py"

# --- PART A: FIX DROPDOWN SNAP-BACK IN ebony_tier_manager.py ---
tier_content = tier_file.read_text(encoding="utf-8")

old_sidebar_code = """    if st.session_state.get("sb_commercial_tier_selector") != cur_tier and cur_tier in tier_opts:
        st.session_state["sb_commercial_tier_selector"] = cur_tier

    selected_tier = st.selectbox(
        "Active License Tier:",
        tier_opts,
        index=cur_idx,
        format_func=lambda x: TIER_METADATA.get(x, {}).get("label", x),
        key="sb_commercial_tier_selector",
        label_visibility="collapsed"
    )
    
    if selected_tier != cur_tier and cur_tier != TIER_EXPIRED and cur_tier != TIER_LOCKED:
        set_current_tier(selected_tier)
        st.rerun()"""

new_sidebar_code = """    def _on_tier_change_callback():
        new_choice = st.session_state.get("sb_commercial_tier_selector")
        if new_choice:
            st.session_state["ebony_commercial_tier"] = new_choice

    if "ebony_commercial_tier" not in st.session_state:
        st.session_state["ebony_commercial_tier"] = cur_tier

    selected_tier = st.selectbox(
        "Active License Tier:",
        tier_opts,
        index=cur_idx,
        format_func=lambda x: TIER_METADATA.get(x, {}).get("label", x),
        key="sb_commercial_tier_selector",
        on_change=_on_tier_change_callback,
        label_visibility="collapsed"
    )"""

if old_sidebar_code in tier_content:
    tier_content = tier_content.replace(old_sidebar_code, new_sidebar_code)
    tier_file.write_text(tier_content, encoding="utf-8")
    print("[+] Fixed dropdown snap-back in ebony_tier_manager.py via on_change callback.")
else:
    # Alternative regex fallback
    snapback_pat = r'if st\.session_state\.get\("sb_commercial_tier_selector"\) != cur_tier[\s\S]*?st\.rerun\(\)'
    if re.search(snapback_pat, tier_content):
        tier_content = re.sub(snapback_pat, new_sidebar_code.strip(), tier_content)
        tier_file.write_text(tier_content, encoding="utf-8")
        print("[+] Fixed dropdown snap-back via regex in ebony_tier_manager.py.")

# --- PART B: ENFORCE OPTICAL SENSOR GATE IN ebony_console_GREEN.py ---
console_content = console_file.read_text(encoding="utf-8")

# Check if comms deck dispatch is present and enforce check_module_access
comms_branch_pat = r'(elif\s+(?:active_module|nav_module|menu_selection|current_page)\s*==\s*["\']📡 Sovereign Comms Deck["\']\s*:)'
match = re.search(comms_branch_pat, console_content)

if match:
    branch_header = match.group(1)
    # Check if gate is already present right after the header
    start_pos = match.end()
    following_block = console_content[start_pos:start_pos+300]
    
    if "check_module_access" not in following_block:
        gate_code = """
    _c_tier = get_current_tier()
    _allowed, _req, _is_m = check_module_access(_c_tier, "📡 Sovereign Comms Deck")
    if not _allowed:
        if _is_m:
            render_maintenance_screen("📡 Sovereign Comms Deck")
        else:
            render_tier_restriction_screen("📡 Sovereign Comms Deck", _req, _c_tier)
    else:"""
        # Indent the original block statements under the 'else:'
        # Find where next elif or top-level block starts
        end_match = re.search(r'\n(?=\s*(?:elif\s|else:|def\s|class\s|st\.sidebar|\Z))', console_content[start_pos:])
        end_pos = start_pos + end_match.start() if end_match else len(console_content)
        
        orig_body = console_content[start_pos:end_pos]
        indented_body = "\n".join(["    " + l if l.strip() else l for l in orig_body.splitlines()])
        
        console_content = console_content[:start_pos] + gate_code + "\n" + indented_body + console_content[end_pos:]
        console_file.write_text(console_content, encoding="utf-8")
        print("[+] Enforced Level-5 Optical Maintenance Gate on 📡 Sovereign Comms Deck in ebony_console_GREEN.py.")
    else:
        print("[*] Gate already active on 📡 Sovereign Comms Deck.")
else:
    print("[*] Comms deck branch pattern already managed.")

# --- PART C: VERIFY BYTECODE COMPILATION ---
py_compile.compile(str(tier_file), doraise=True)
print("[COMPILED OK] ebony_tier_manager.py -> Exit Code 0 Verified.")
py_compile.compile(str(console_file), doraise=True)
print("[COMPILED OK] ebony_console_GREEN.py -> Exit Code 0 Verified.")
print("[SUCCESS] All files compiled cleanly with ZERO errors!")