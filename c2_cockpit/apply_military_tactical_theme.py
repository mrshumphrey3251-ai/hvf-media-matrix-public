import os
import sys
import re
import py_compile

# ==============================================================================
# HVF Omni-Industrial Matrix | DEFENSE C2 TACTICAL PALETTE ENGINE
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# Design Standard: MIL-STD-1472 Defense Command & Control Interface
# ==============================================================================

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILE = os.path.join(BASE_DIR, "ebony_console_GREEN.py")

print("=" * 80)
print("DEPLOYING MILITARY DEFENSE C2 THEME TO EBONY COMMAND DECK")
print("=" * 80)

if not os.path.exists(TARGET_FILE):
    print(f"[FAIL] Target console not found at: {TARGET_FILE}")
    sys.exit(1)

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# MIL-STD Tactical Defense CSS Definition
TACTICAL_C2_CSS = """
    <style>
    /* Baseline Background and Typography */
    .stApp { 
        background-color: #0b0e14 !important; 
        color: #e2e8f0 !important; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Tactical Monospace Headers (Defense C2 Amber) */
    h1, h2, h3, h4 { 
        color: #e2a03f !important; 
        font-family: "SF Mono", "Consolas", "Courier New", monospace !important; 
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        border-bottom: 1px solid #242d3d;
        padding-bottom: 4px;
    }
    
    /* High-Legibility Input and Monospace Text Areas */
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
    
    /* Command Buttons - Tactical Armor Finish */
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
    
    /* Veto Threat Action Override (Block Sender) */
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
    
    /* Card Containers and Badges */
    .card-header { 
        font-weight: 700 !important; 
        font-size: 1.0em !important; 
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
    
    /* Expander Panels */
    .streamlit-expanderHeader {
        background-color: #121722 !important;
        border: 1px solid #242d3d !important;
        border-radius: 2px !important;
        color: #94a3b8 !important;
    }
    </style>
"""

# 1. Replace existing <style> block
style_pattern = r"<style>.*?</style>"
if re.search(style_pattern, content, flags=re.DOTALL):
    content = re.sub(style_pattern, TACTICAL_C2_CSS.strip(), content, count=1, flags=re.DOTALL)
    print("[SUCCESS] Replaced green stylesheet with Defense C2 Tactical styling.")
else:
    print("[WARN] <style> block not matched. Prepending tactical stylesheet.")
    content = f'st.markdown("""{TACTICAL_C2_CSS}""", unsafe_allow_html=True)\n' + content

# 2. Replace hardcoded inline green styling references
content = content.replace("#3fb950", "#e2a03f")   # Neon green -> Tactical Amber
content = content.replace("#161b22", "#131822")   # GitHub black -> Matte Gunmetal
content = content.replace("#30363d", "#242d3d")   # Gray borders -> Tactical Slate borders
content = content.replace("#58a6ff", "#f1f5f9")   # Light blue text -> Crisp Off-White text

with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)

py_compile.compile(TARGET_FILE, doraise=True)
print(f"[SUCCESS] Defense C2 theme compiled cleanly into: {TARGET_FILE}")
print("=" * 80)

