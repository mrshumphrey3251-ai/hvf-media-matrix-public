import os
import sys
import re
import py_compile

# ==============================================================================
# HVF Omni-Industrial Matrix | MIL-STD DEFENSE C2 THEME & VETO GATE REPAIR
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# Design Standard: MIL-STD-1472 Defense Command & Control Interface
# ==============================================================================

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILE = os.path.join(BASE_DIR, "ebony_console_GREEN.py")

print("=" * 80)
print("DEPLOYING MILITARY DEFENSE C2 PALETTE & RESOLVING NAMEERROR LINE 1239")
print("=" * 80)

if not os.path.exists(TARGET_FILE):
    print(f"[FAIL] Target file not found: {TARGET_FILE}")
    sys.exit(1)

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Eradicate faulty Line 1239 injection
content = re.sub(
    r"[ \t]*# --- ADDITIVE CEO KINEMATIC VETO[^\n]*\n[ \t]*email_triage_core\.render_veto_controls\(d_id,\s*sender\)[ \t]*\n?",
    "\n",
    content
)
content = re.sub(
    r"[ \t]*email_triage_core\.render_veto_controls\(d_id,\s*sender\)[ \t]*\n?",
    "\n",
    content
)
print("[SUCCESS] Eradicated faulty 'render_veto_controls(d_id, sender)' call.")

# 2. Locate existing col_btn1, col_btn2 and upgrade to 3-column tactical controls
target_cols = "col_btn1, col_btn2 = st.columns(2)"
if target_cols in content:
    # Detect the ID variable used inside the button actions
    idx = content.find(target_cols)
    sub = content[idx:idx+800]
    
    # Match ID variable from SQL query or button key
    id_var = "d_id"
    key_match = re.search(r"key=f?[\"'][^\"']*?\{([\w\[\].]+)\}", sub)
    sql_match = re.search(r"WHERE id\s*=\s*\?\s*\",\s*\(([\w\[\].]+),?\)", sub)
    
    if sql_match:
        id_var = sql_match.group(1)
    elif key_match:
        id_var = key_match.group(1)
    else:
        # Fallback inspection for loop variables
        loop_match = re.search(r"for\s+([\w,\s]+)\s+in\s+", content[:idx])
        if loop_match:
            vars_list = [v.strip() for v in loop_match.group(1).split(",")]
            id_var = vars_list[0]
            
    print(f"[SUCCESS] Detected dispatch row ID variable: [{id_var}]")
    
    # Replace columns with 3-column tactical layout
    content = content.replace(target_cols, "col_btn1, col_btn2, col_btn3 = st.columns([1.2, 1, 1.2])")
    
    # Inject col_btn3 after col_btn2 block if not already present
    if "col_btn3" not in content.split("col_btn1, col_btn2, col_btn3 = st.columns([1.2, 1, 1.2])")[1][:1200]:
        # Find the end of col_btn2 block
        col2_pos = content.find("with col_btn2:")
        if col2_pos != -1:
            # Find next block with lower or equal indentation
            lines = content[col2_pos:].split("\n")
            base_indent = len(lines[0]) - len(lines[0].lstrip())
            insert_line_idx = len(lines)
            for l_idx, line in enumerate(lines[1:], 1):
                if line.strip() and (len(line) - len(line.lstrip())) <= base_indent:
                    insert_line_idx = l_idx
                    break
            
            indent_str = " " * base_indent
            block_btn_code = f"""{indent_str}with col_btn3:
{indent_str}    if st.button("🚫 Block Sender", key=f"blk_{{{id_var}}}", type="primary"):
{indent_str}        try:
{indent_str}            import sqlite3
{indent_str}            conn_b = sqlite3.connect(r"C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db")
{indent_str}            cur_b = conn_b.cursor()
{indent_str}            cur_b.execute("SELECT sender_address FROM staged_email_dispatches WHERE id = ?", ({id_var},))
{indent_str}            s_res = cur_b.fetchone()
{indent_str}            conn_b.close()
{indent_str}            s_raw = s_res[0] if s_res else ""
{indent_str}            suc, b_msg = email_triage_core.block_sender(s_raw, reason="CEO_TACTICAL_VETO")
{indent_str}            if suc:
{indent_str}                st.warning(f"🚫 {{b_msg}}")
{indent_str}            else:
{indent_str}                st.error(f"Block failed: {{b_msg}}")
{indent_str}        except Exception as ex_b:
{indent_str}            st.error(f"Block error: {{ex_b}}")
{indent_str}        st.rerun()"""
            
            reconstructed = "\n".join(lines[:insert_line_idx]) + "\n" + block_btn_code + "\n" + "\n".join(lines[insert_line_idx:])
            content = content[:col2_pos] + reconstructed
            print("[SUCCESS] Injected database-grounded 🚫 Block Sender control into col_btn3.")
else:
    print("[INFO] Target columns pattern already customized.")

# 3. MIL-STD DEFENSE C2 THEME INJECTION (Replaces Festive Green)
TACTICAL_C2_CSS = """
    <style>
    /* Baseline Ballistic Matte Gunmetal & Professional Typography */
    .stApp { 
        background-color: #0b0e14 !important; 
        color: #e2e8f0 !important; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Tactical Monospace Defense Headers (Tactical Amber) */
    h1, h2, h3, h4 { 
        color: #e2a03f !important; 
        font-family: "SF Mono", "Consolas", "Courier New", monospace !important; 
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        border-bottom: 1px solid #242d3d !important;
        padding-bottom: 6px !important;
        margin-top: 12px !important;
    }
    
    /* High-Contrast Input Fields & Text Areas */
    .stTextInput>div>div>input { 
        background-color: #121722 !important; 
        color: #f1f5f9 !important; 
        border: 1px solid #334155 !important;
        border-radius: 2px !important;
    }
    .stTextArea>div>div>textarea { 
        background-color: #121722 !important; 
        color: #f8fafc !important; 
        border: 1px solid #334155 !important;
        border-radius: 2px !important;
        font-family: "SF Mono", "Consolas", monospace !important;
        font-size: 0.9em !important;
        line-height: 1.45 !important;
    }
    
    /* Tactical Buttons: Matte Steel & Amber Hover */
    .stButton>button { 
        border: 1px solid #475569 !important; 
        color: #cbd5e1 !important; 
        font-family: "SF Mono", "Consolas", monospace !important;
        font-weight: 600 !important; 
        background-color: #161c28 !important; 
        width: 100% !important; 
        border-radius: 2px !important; 
        padding: 0.45rem !important; 
        transition: all 0.2s ease-in-out !important; 
    }
    .stButton>button:hover { 
        background-color: #1f2737 !important; 
        color: #e2a03f !important; 
        border-color: #e2a03f !important; 
    }
    
    /* 🚫 Block Sender Action: High-Alert Crimson Defense Button */
    .stButton>button[data-baseweb="button"]:has(div:contains("🚫")) { 
        border-color: #b91c1c !important; 
        color: #fca5a5 !important; 
        background-color: #2b1114 !important;
    }
    .stButton>button[data-baseweb="button"]:has(div:contains("🚫")):hover { 
        background-color: #dc2626 !important; 
        color: #ffffff !important; 
        border-color: #ef4444 !important; 
    }
    
    /* Tactical Container Cards */
    .card-header { 
        font-weight: 700 !important; 
        font-size: 0.95em !important; 
        color: #cbd5e1 !important; 
        border-bottom: 1px solid #232b3b !important; 
        padding-bottom: 6px !important; 
    }
    .status-badge { 
        padding: 2px 8px !important; 
        border-radius: 2px !important; 
        font-size: 0.75em !important; 
        font-weight: 700 !important; 
        float: right !important; 
        letter-spacing: 0.05em !important;
    }
    .status-clean { 
        background-color: #1e3a5f !important; 
        color: #93c5fd !important; 
        border: 1px solid #3b82f6 !important;
    }
    .status-threat { 
        background-color: #450a0a !important; 
        color: #fca5a5 !important; 
        border: 1px solid #ef4444 !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #121722 !important;
        border: 1px solid #242d3d !important;
        border-radius: 2px !important;
        color: #94a3b8 !important;
    }
    </style>
"""

# Replace stylesheet
style_pattern = r"<style>.*?</style>"
if re.search(style_pattern, content, flags=re.DOTALL):
    content = re.sub(style_pattern, TACTICAL_C2_CSS.strip(), content, count=1, flags=re.DOTALL)
    print("[SUCCESS] Replaced green stylesheet with MIL-STD Defense C2 Tactical Theme.")
else:
    content = f'st.markdown("""{TACTICAL_C2_CSS}""", unsafe_allow_html=True)\n' + content

# Replace hardcoded neon green hex values with Tactical C2 colors
content = content.replace("#3fb950", "#e2a03f")  # Neon green -> Tactical Amber
content = content.replace("#58a6ff", "#f1f5f9")  # Light blue -> Crisp Off-White
content = content.replace("#161b22", "#121722")  # Gray card -> Dark Slate Panel
content = content.replace("#30363d", "#242d3d")  # Border gray -> Armor Steel Border

# Mirror updates to ebony_console.py
with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)

ALT_FILE = os.path.join(BASE_DIR, "ebony_console.py")
with open(ALT_FILE, "w", encoding="utf-8") as f:
    f.write(content)

py_compile.compile(TARGET_FILE, doraise=True)
py_compile.compile(ALT_FILE, doraise=True)

print(f"[SUCCESS] Defense C2 theme compiled cleanly into ebony_console_GREEN.py and ebony_console.py")
print("=" * 80)

