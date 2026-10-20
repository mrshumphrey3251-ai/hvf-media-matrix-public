import sys
import re
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
if not cockpit_dir.exists():
    print(f"[CRITICAL ERROR] Cockpit directory not found: {cockpit_dir}")
    sys.exit(1)

# -------------------------------------------------------------------------
# 1. WRITE ebony_tier_manager.py
# -------------------------------------------------------------------------
tier_manager_code = """\"\"\"
E.B.O.N.Y. Sovereign Commercial Licensing & Tier Access Controller
Role-Based Access Control (RBAC) & Maintenance Lockout Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
\"\"\"
import streamlit as st
import json
from pathlib import Path

# Tier Identifiers
TIER_0_CEO = "TIER_0_CEO"
TIER_1_COMMS = "TIER_1_COMMS"
TIER_COMMAND = "TIER_COMMAND"
TIER_2_SCADA = "TIER_2_SCADA"
TIER_3_DRONE = "TIER_3_DRONE"

TIER_METADATA = {
    TIER_0_CEO: {
        "name": "👑 Level-5 Sovereign Root (CEO Clearance)",
        "label": "👑 CEO Clearance (Unrestricted)",
        "price": "Sovereign Executive Baseline",
        "desc": "Unrestricted administrative, hardware, and engineering access across all enclave matrices."
    },
    TIER_1_COMMS: {
        "name": "Tier 1: Sovereign Executive Comms & NOAA Radar",
        "label": "Tier 1: Executive Comms & Radar ($19.99/mo)",
        "price": "$19.99 / Month",
        "desc": "Autonomous email triage, threat scrubbing, NOAA weather radar, contextual ghostwriting, and travel debriefs."
    },
    TIER_COMMAND: {
        "name": "Tier 1.5: Sovereign Command & Tactical Intelligence",
        "label": "Tier 1.5: Sovereign Command ($39.99/mo)",
        "price": "$39.99 / Month",
        "desc": "Air-gapped deterministic neural routing, direct executive command terminal, and strategic ghostwriting."
    },
    TIER_2_SCADA: {
        "name": "Tier 2: Industrial SCADA & Grid Infrastructure",
        "label": "Tier 2: SCADA & Grid ($299/mo)",
        "price": "$299 / Month",
        "desc": "Sub-16ms kinetic grid islanding, 450A busbar telemetry, and Title 61 power supervision."
    },
    TIER_3_DRONE: {
        "name": "Tier 3: VIP Autonomous Drone Fleet & Physical Defense",
        "label": "Tier 3: VIP Drone Defense ($999/mo)",
        "price": "$999 / Month",
        "desc": "Tethered continuous-power UAS, inductive docking, ODOT bridge crack detection, and Triad Swarm control."
    }
}

MODULE_TIER_MAPPING = {
    # Tier 1 Entitlements ($19.99/mo and above)
    "📖 System Overview": TIER_1_COMMS,
    "📝 Feedback Hub": TIER_1_COMMS,
    "📨 Sovereign Dispatch Deck": TIER_1_COMMS,
    "📡 Sovereign Comms Deck": TIER_1_COMMS,
    "🚨 NOAA Radar": TIER_1_COMMS,
    
    # Tier 1.5 Entitlements ($39.99/mo and above)
    "💬 Sovereign Command": TIER_COMMAND,
    
    # Tier 2 Entitlements ($299/mo and above)
    "🎛️ Master C2 Cockpit": TIER_2_SCADA,
    "⚡ Sovereign Weather Scada": TIER_2_SCADA,
    "⚡ Grain Silo Aeration And F": TIER_2_SCADA,
    
    # Tier 3 Entitlements ($999/mo and above)
    "🌾 Drone Diagnostics": TIER_3_DRONE,
    "📡 LinkedIn Engine": TIER_3_DRONE,
}

MAINTENANCE_MODULES = [
    "⚡ Autonomous Build Forge",
    "🛡️ CEO Authorization Gate",
    "🧪 Sandbox",
    "⚙️ Empire Config",
    "⬛ Media Matrix",
    "🎨 Asset Synthesis",
    "📘 Omni-Industry Matrix",
    "⚡ Access Control",
    "⚡ Action Desk",
    "⚡ Ada Voice Module",
    "⚡ Alert Protocol",
    "⚡ Api Gateway",
    "⚡ App",
    "⚡ Apply Account Manager Ui",
    "⚡ Apply Dispatch Deck",
    "⚡ Autonomous Healing Test",
    "⚡ Chronos Companion Engine",
    "⚡ Hardware Bridge",
    "⚡ Linkedin Lead Scheduler",
    "⚡ Migrate Users Table"
]

TIER_RANKS = {
    TIER_1_COMMS: 1,
    TIER_COMMAND: 2,
    TIER_2_SCADA: 3,
    TIER_3_DRONE: 4,
    TIER_0_CEO: 99
}

def get_current_tier() -> str:
    return st.session_state.get("ebony_commercial_tier", TIER_0_CEO)

def set_current_tier(tier: str):
    st.session_state["ebony_commercial_tier"] = tier

def check_module_access(user_tier: str, module_name: str) -> tuple:
    if user_tier == TIER_0_CEO:
        return True, "", False
        
    if module_name in MAINTENANCE_MODULES:
        return False, "Level-5 Sovereign Engineering R&D", True
        
    required_tier = MODULE_TIER_MAPPING.get(module_name, TIER_0_CEO)
    user_rank = TIER_RANKS.get(user_tier, 1)
    req_rank = TIER_RANKS.get(required_tier, 99)
    
    if user_rank >= req_rank:
        return True, "", False
    else:
        req_meta = TIER_METADATA.get(required_tier, {})
        req_display = f"{req_meta.get('name', 'Higher Tier')} ({req_meta.get('price', '')})"
        return False, req_display, False

def render_tier_restriction_screen(module_name: str, required_tier_name: str, current_tier: str):
    cur_meta = TIER_METADATA.get(current_tier, {})
    st.markdown(f\"\"\"
    <div style="background-color: #140b0b; border: 2px solid #ff4444; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
        <h2 style="color: #ff4444; margin-top: 0; font-family: monospace; letter-spacing: 2px;">🔒 ACCESS RESTRICTED // HIGHER SUBSCRIPTION TIER REQUIRED</h2>
        <div style="color: #a0aab2; font-size: 0.9em; font-family: monospace; margin-bottom: 15px;">
            <strong>SECURITY ENFORCEMENT:</strong> Humphrey Virtual Farms LLC | <strong>CAGE:</strong> 1AHA8 | <strong>UEI:</strong> S1M4ENLHTDH5<br>
            <strong>STATUTORY JURISDICTION:</strong> State of Oklahoma Title 61 & HB 2992 Commercial Enclave
        </div>
        <div style="color: #ffffff; font-size: 0.95em; line-height: 1.6; border-top: 1px solid #3a1e1e; padding-top: 15px;">
            <p><strong>ATTEMPTED MODULE:</strong> <span style="color: #ff8888; font-weight: bold;">{module_name}</span></p>
            <p><strong>YOUR ACTIVE SUBSCRIPTION:</strong> <span style="color: #00ff88; font-weight: bold;">{cur_meta.get('name', current_tier)}</span></p>
            <p><strong>REQUIRED COMMERCIAL TIER:</strong> <span style="color: #ffcc00; font-weight: bold;">{required_tier_name}</span></p>
            <p style="margin-top: 15px; color: #d0d7de;">
                Access to this sovereign command capability is governed by commercial licensing tiers. Upgrade your subscription to unlock active operational glass.
            </p>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        with st.container(border=True):
            st.markdown("#### ⚡ Upgrade Your Subscription Tier")
            st.markdown("Direct sole-source procurement and commercial licensing available under **CAGE 1AHA8**.")
            st.info(f"Target Capability: **{required_tier_name}**")
            
            c_u1, c_u2 = st.columns(2)
            with c_u1:
                if st.button("📋 UPGRADE LICENSE", key=f"btn_upg_req_{module_name}", use_container_width=True):
                    st.success("Upgrade inquiry registered. An executive dispatch has been staged for processing.")
            with c_u2:
                if st.button("⬅ RETURN TO DISPATCH DECK", key=f"btn_ret_comms_{module_name}", use_container_width=True):
                    st.session_state["nav_module_override"] = "📨 Sovereign Dispatch Deck"
                    st.rerun()

def render_maintenance_screen(module_name: str):
    st.markdown(f\"\"\"
    <div style="background-color: #141208; border: 2px solid #ffaa00; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
        <h2 style="color: #ffaa00; margin-top: 0; font-family: monospace; letter-spacing: 2px;">🚧 SOVEREIGN ENCLAVE MAINTENANCE // LEVEL-5 R&D LOCKOUT</h2>
        <div style="color: #a0aab2; font-size: 0.9em; font-family: monospace; margin-bottom: 15px;">
            <strong>CLASSIFICATION:</strong> Humphrey Virtual Farms LLC // Internal Systems Engineering<br>
            <strong>STATUTORY JURISDICTION:</strong> State of Oklahoma Title 61 & OK HB 2992 Framework
        </div>
        <div style="color: #ffffff; font-size: 0.95em; line-height: 1.6; border-top: 1px solid #3a2e1e; padding-top: 15px;">
            <p><strong>MODULE UNDER CALIBRATION:</strong> <span style="color: #ffcc00; font-weight: bold;">{module_name}</span></p>
            <p><strong>OPERATIONAL STATUS:</strong> <span style="color: #ffaa00; font-weight: bold;">ACTIVE HARDENING & STATUTORY ALIGNMENT IN PROGRESS</span></p>
            <p style="margin-top: 15px; color: #d0d7de;">
                This module is designated as an internal engineering workbench, diagnostic tool, or migration script. It is currently locked behind Level-5 R&D maintenance protocols to preserve commercial production integrity.
            </p>
            <p style="color: #8b949e; font-size: 0.85em;">
                Access is restricted strictly to Level-5 Authorized Systems Engineering Personnel. Commercial subscribers should navigate to their authorized command modules.
            </p>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        if st.button("⬅ RETURN TO DISPATCH DECK", key=f"btn_ret_auth_{module_name}", use_container_width=True):
            st.session_state["nav_module_override"] = "📨 Sovereign Dispatch Deck"
            st.rerun()

def render_tier_switcher_sidebar():
    st.markdown(\"\"\"
    <div style="background-color: #0b110e; border: 1px solid #00ff88; border-radius: 6px; padding: 10px; margin-bottom: 10px;">
        <div style="color: #00ff88; font-weight: bold; font-size: 0.8em; letter-spacing: 1px;">ACTIVE LICENSE TIER</div>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    tier_opts = [
        TIER_0_CEO,
        TIER_1_COMMS,
        TIER_COMMAND,
        TIER_2_SCADA,
        TIER_3_DRONE
    ]
    
    cur_tier = get_current_tier()
    cur_idx = tier_opts.index(cur_tier) if cur_tier in tier_opts else 0
    
    selected_tier = st.selectbox(
        "Active License Tier:",
        tier_opts,
        index=cur_idx,
        format_func=lambda x: TIER_METADATA.get(x, {}).get("label", x),
        key="sb_commercial_tier_selector",
        label_visibility="collapsed"
    )
    
    if selected_tier != cur_tier:
        set_current_tier(selected_tier)
        st.rerun()
"""

tier_p = cockpit_dir / "ebony_tier_manager.py"
tier_p.write_text(tier_manager_code, encoding="utf-8")
print("[+] ebony_tier_manager.py written to disk.")

# -------------------------------------------------------------------------
# 2. INJECT TIER SWITCHER & BARRIER DIRECTLY INTO ebony_console_GREEN.py
# -------------------------------------------------------------------------
console_p = cockpit_dir / "ebony_console_GREEN.py"
content = console_p.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

# Clean out any previous partial injection
cleaned_lines = []
skip_old_barrier = False
for line in lines:
    if "SOVEREIGN COMMERCIAL TIER BARRIER" in line:
        skip_old_barrier = True
        continue
    if skip_old_barrier:
        if line.strip().startswith("st.stop()"):
            skip_old_barrier = False
            continue
        elif any(k in line for k in ["_user_tier =", "_allowed,", "render_maintenance_screen", "render_tier_restriction_screen"]):
            continue
        else:
            skip_old_barrier = False
    if "render_tier_switcher_sidebar()" in line:
        continue
    cleaned_lines.append(line)

content = "".join(cleaned_lines)
lines = content.splitlines(keepends=True)

# Ensure imports at the top
tier_import_statement = """import sys
from pathlib import Path
_cdir = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit")
if str(_cdir) not in sys.path:
    sys.path.insert(0, str(_cdir))
from ebony_tier_manager import (
    check_module_access,
    render_tier_restriction_screen,
    render_maintenance_screen,
    render_tier_switcher_sidebar,
    get_current_tier
)"""

if "from ebony_tier_manager import" not in content:
    insert_idx = 0
    for i, line in enumerate(lines[:120]):
        if line.startswith("import ") or line.startswith("from "):
            insert_idx = i + 1
    lines = lines[:insert_idx] + [tier_import_statement + "\n\n"] + lines[insert_idx:]
    print("[+] Imported ebony_tier_manager into ebony_console_GREEN.py.")

# Locate the command modules radio / selectbox
nav_idx = -1
for i, line in enumerate(lines):
    if ("radio(" in line or "selectbox(" in line) and any(m in "".join(lines[max(0, i-5):min(len(lines), i+15)]) for m in ["Master C2 Cockpit", "Command Modules", "Sovereign Dispatch Deck"]):
        nav_idx = i
        break

if nav_idx == -1:
    for i, line in enumerate(lines):
        if "🎛️ Master C2 Cockpit" in line:
            for j in range(i, max(0, i-20), -1):
                if "radio(" in lines[j] or "selectbox(" in lines[j]:
                    nav_idx = j
                    break
            break

if nav_idx == -1:
    print("[CRITICAL ERROR] Could not locate module selection radio in console script.")
    sys.exit(1)

nav_line = lines[nav_idx]
var_name = nav_line.split("=")[0].strip()
indent = nav_line[:len(nav_line) - len(nav_line.lstrip())]
print(f"[+] Located module selector variable '{var_name}' at line {nav_idx + 1}.")

# Locate closing parenthesis of the radio call
close_idx = nav_idx
while close_idx < len(lines) and ")" not in lines[close_idx]:
    close_idx += 1

print(f"[+] Module selector extends from line {nav_idx + 1} to line {close_idx + 1}.")

# Build injection blocks
top_call = f"{indent}render_tier_switcher_sidebar()\n"
bottom_barrier = f"""
{indent}# --- SOVEREIGN COMMERCIAL TIER BARRIER & MAINTENANCE LOCKOUT ---
{indent}_user_tier = get_current_tier()
{indent}_allowed, _req_tier, _is_maint = check_module_access(_user_tier, {var_name})
{indent}if not _allowed:
{indent}    if _is_maint:
{indent}        render_maintenance_screen({var_name})
{indent}    else:
{indent}        render_tier_restriction_screen({var_name}, _req_tier, _user_tier)
{indent}    st.stop()
"""

# Reconstruct lines
final_lines = lines[:nav_idx] + [top_call] + lines[nav_idx:close_idx+1] + [bottom_barrier] + lines[close_idx+1:]
console_p.write_text("".join(final_lines), encoding="utf-8")
print(f"[+] Injected render_tier_switcher_sidebar and barrier check into {console_p.name}.")

# -------------------------------------------------------------------------
# 3. VERIFY COMPILATION ACROSS ENTIRE PLATFORM
# -------------------------------------------------------------------------
print("[*] Running py_compile verification...")
py_compile.compile(str(tier_p), doraise=True)
py_compile.compile(str(console_p), doraise=True)
print("[SUCCESS] ebony_tier_manager.py and ebony_console_GREEN.py compiled cleanly (Exit Code 0)!")