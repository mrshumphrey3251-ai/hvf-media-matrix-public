"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: FIX C2 THEME AND BUTTONS
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    import os

    import sys

    import re

    import py_compile



    # ==============================================================================

    # HVF Omni-Industrial Matrix | DEFENSE C2 TACTICAL PALETTE & VETO GATE ENGINE

    # Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)

    # Design Standard: MIL-STD-1472 Defense Command & Control Interface

    # ==============================================================================



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    FILES_TO_FIX = [

        os.path.join(BASE_DIR, "ebony_console.py"),

        os.path.join(BASE_DIR, "ebony_console_GREEN.py")

    ]



    TACTICAL_C2_CSS = """<style>

        /* Baseline Ballistic Matte Gunmetal */

        .stApp { 

            background-color: #0b0e14 !important; 

            color: #e2e8f0 !important; 

            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace !important;

        }

        /* Monospace Tactical Amber Headers */

        h1, h2, h3, h4 { 

            color: #e2a03f !important; 

            font-family: "SF Mono", "Consolas", "Courier New", monospace !important; 

            font-weight: 700 !important;

            letter-spacing: 0.04em !important;

            text-transform: uppercase !important;

            border-bottom: 1px solid #242d3d !important;

            padding-bottom: 6px !important;

        }

        /* High-Contrast Inputs and Text Areas */

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

        }

        /* Tactical Action Buttons */

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

        /* Crimson High-Alert Block Button */

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

        /* Defense Card Containers */

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

        .streamlit-expanderHeader {

            background-color: #121722 !important;

            border: 1px solid #242d3d !important;

            border-radius: 2px !important;

            color: #94a3b8 !important;

        }

    </style>"""



    print("=" * 80)

    print("DEPLOYING MIL-STD DEFENSE C2 THEME & ERADICATING NAMEERROR")

    print("=" * 80)



    for fpath in FILES_TO_FIX:

        if not os.path.exists(fpath):

            continue



        print(f"\nProcessing target: {os.path.basename(fpath)}")

        with open(fpath, "r", encoding="utf-8") as f:

            raw_content = f.read()



        # 1. Strip any rogue render_veto_controls or faulty comments

        raw_content = re.sub(r"[ \t]*# --- ADDITIVE CEO KINEMATIC VETO[^\n]*\n?", "", raw_content)

        raw_content = re.sub(r"[ \t]*email_triage_core\.render_veto_controls\([^\)]*\)[ \t]*\n?", "", raw_content)

        print("  * Purged rogue 'render_veto_controls' calls.")



        # 2. Inject Defense C2 CSS styling

        style_regex = r"<style>.*?</style>"

        if re.search(style_regex, raw_content, flags=re.DOTALL):

            raw_content = re.sub(style_regex, TACTICAL_C2_CSS, raw_content, count=1, flags=re.DOTALL)

            print("  * Injected MIL-STD Defense C2 stylesheet.")

        else:

            raw_content = f'st.markdown("""{TACTICAL_C2_CSS}""", unsafe_allow_html=True)\n' + raw_content



        # 3. Replace neon green and high-glare palettes across code

        raw_content = raw_content.replace("#3fb950", "#e2a03f")

        raw_content = raw_content.replace("#00ff41", "#e2a03f")

        raw_content = raw_content.replace("#2ea043", "#d97706")

        raw_content = raw_content.replace("#161b22", "#121722")

        raw_content = raw_content.replace("#0d1117", "#0b0e14")

        raw_content = raw_content.replace("#30363d", "#242d3d")

        raw_content = raw_content.replace("#58a6ff", "#f1f5f9")

        print("  * Replaced neon green with Defense C2 matte gunmetal and amber.")



        # 4. Surgical line-by-line 3-column button upgrade

        lines = raw_content.splitlines(keepends=True)

        cols_idx = -1

        for idx, line in enumerate(lines):

            if "col_btn1, col_btn2" in line:

                cols_idx = idx

                break



        if cols_idx != -1:

            col_indent = lines[cols_idx][:len(lines[cols_idx]) - len(lines[cols_idx].lstrip())]

            lines[cols_idx] = f"{col_indent}col_btn1, col_btn2, col_btn3 = st.columns([1.2, 1, 1.2])\n"



            # Locate with col_btn2:

            col2_idx = -1

            for idx in range(cols_idx, min(cols_idx + 40, len(lines))):

                if "with col_btn2:" in lines[idx]:

                    col2_idx = idx

                    break



            if col2_idx != -1:

                # Find end of with col_btn2 block

                insert_idx = len(lines)

                for idx in range(col2_idx + 1, min(col2_idx + 35, len(lines))):

                    curr = lines[idx]

                    if curr.strip() and (len(curr) - len(curr.lstrip())) <= len(col_indent):

                        insert_idx = idx

                        break



                # Check if block button already present

                has_btn3 = any("with col_btn3:" in l for l in lines[col2_idx:insert_idx+10])

                if not has_btn3:

                    btn3_block = [

                        f"{col_indent}with col_btn3:\n",

                        f"{col_indent}    if st.button('🚫 Block Sender', key=f'btn_block_{{disp_id}}', type='primary'):\n",

                        f"{col_indent}        try:\n",

                        f"{col_indent}            import sqlite3\n",

                        f"{col_indent}            conn_bk = sqlite3.connect(r'C:\\HVF_Repos\\hvf-media-matrix-private\\hvf_memory_vault.db')\n",

                        f"{col_indent}            cur_bk = conn_bk.cursor()\n",

                        f"{col_indent}            cur_bk.execute('SELECT sender_address FROM staged_email_dispatches WHERE id = ?', (disp_id,))\n",

                        f"{col_indent}            snd_row = cur_bk.fetchone()\n",

                        f"{col_indent}            conn_bk.close()\n",

                        f"{col_indent}            if snd_row and snd_row[0]:\n",

                        f"{col_indent}                b_ok, b_text = email_triage_core.block_sender(snd_row[0], reason='CEO_TACTICAL_VETO')\n",

                        f"{col_indent}                if b_ok:\n",

                        f"{col_indent}                    st.warning(f'🚫 {{b_text}}')\n",

                        f"{col_indent}                else:\n",

                        f"{col_indent}                    st.error(f'Block failed: {{b_text}}')\n",

                        f"{col_indent}        except Exception as b_err:\n",

                        f"{col_indent}            st.error(f'Block error: {{b_err}}')\n",

                        f"{col_indent}        st.rerun()\n"

                    ]

                    lines[insert_idx:insert_idx] = btn3_block

                    print(f"  * Injected 🚫 Block Sender control into col_btn3 at line {insert_idx}.")



        final_text = "".join(lines)

        with open(fpath, "w", encoding="utf-8") as f:

            f.write(final_text)



        py_compile.compile(fpath, doraise=True)

        print(f"  * [SUCCESS] Compiled cleanly with zero syntax errors: {os.path.basename(fpath)}")



    print("\n" + "=" * 80)

    print("DEFENSE C2 THEME & VETO CONTROLS OPERATIONAL")

    print("=" * 80)




if __name__ == "__main__":
    render()
