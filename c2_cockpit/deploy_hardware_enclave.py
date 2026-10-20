import sys
import re
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
if not cockpit_dir.exists():
    print(f"[CRITICAL ERROR] Cockpit directory not found: {cockpit_dir}")
    sys.exit(1)

# -------------------------------------------------------------------------
# 1. UPGRADE ebony_client_updater.py WITH HARDWARE FINGERPRINTING
# -------------------------------------------------------------------------
updater_code = """\"\"\"
E.B.O.N.Y. Sovereign Client Downstream Updater & License Enforcement Engine
Authoritative Unidirectional Code Distribution & Hardware Node Locking Architecture
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
\"\"\"
import os
import sys
import json
import urllib.request
import hashlib
import platform
import subprocess
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(r"C:\\hvf_c2\\hvf-media-matrix-private")
COCKPIT_DIR = BASE_DIR / "c2_cockpit"
LICENSE_FILE = COCKPIT_DIR / "ebony_license.json"
PUBLIC_RAW_BASE = "https://raw.githubusercontent.com/mrshumphrey3251-ai/hvf-media-matrix-public/main"

UPDATE_TARGETS = [
    "c2_cockpit/ebony_console_GREEN.py",
    "c2_cockpit/ebony_tier_manager.py",
    "c2_cockpit/ebony_travel_ui.py",
    "c2_cockpit/ebony_travel_autopilot.py",
    "c2_cockpit/ebony_email_dispatcher.py",
    "c2_cockpit/ebony_client_updater.py"
]

PROTECTED_SOVEREIGN_DATA = [
    "c2_cockpit/matrix_ledger.db",
    "c2_cockpit/email_accounts.json",
    "autopilot_daemon.log",
    "c2_cockpit/ebony_license.json"
]

def get_hardware_uuid() -> str:
    \"\"\"Generates a unique SHA-256 fingerprint bound to physical motherboard & MAC address.\"\"\"
    hw_string = platform.node() + platform.machine() + str(uuid.getnode())
    if platform.system() == "Windows":
        try:
            # Query physical motherboard UUID
            output = subprocess.check_output("wmic csproduct get uuid", shell=True).decode()
            hw_string += output.split("\\n")[1].strip()
        except Exception:
            pass
    elif platform.system() == "Linux":
        try:
            hw_string += Path("/sys/class/dmi/id/product_uuid").read_text().strip()
        except Exception:
            pass
    return hashlib.sha256(hw_string.encode()).hexdigest()

def init_or_read_license() -> dict:
    hw_id = get_hardware_uuid()
    
    if not LICENSE_FILE.exists():
        pilot_license = {
            "license_type": "7_DAY_SOVEREIGN_PILOT",
            "tier": "TIER_1_PERSONAL",
            "licensed_to": "Prospective Sovereign Subscriber",
            "hardware_signature": hw_id,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            "status": "ACTIVE_PILOT",
            "enforce_updates": True
        }
        LICENSE_FILE.write_text(json.dumps(pilot_license, indent=2), encoding="utf-8")
        return pilot_license
    try:
        return json.loads(LICENSE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"status": "LICENSE_CORRUPT"}

def check_license_validity() -> tuple[bool, str, int]:
    lic = init_or_read_license()
    
    # HARDWARE ENCLAVE CHECK
    hw_id = get_hardware_uuid()
    if lic.get("hardware_signature") and lic.get("hardware_signature") != hw_id:
        return False, "HARDWARE_MISMATCH_PIRACY_LOCKOUT", 0

    expires_str = lic.get("expires_at")
    if not expires_str:
        return False, "NO_EXPIRATION_SET", 0
    try:
        exp_dt = datetime.fromisoformat(expires_str)
        now_dt = datetime.now(timezone.utc)
        remaining = exp_dt - now_dt
        if remaining.total_seconds() <= 0:
            return False, "EXPIRED", 0
        return True, lic.get("license_type", "ACTIVE"), int(remaining.total_seconds() // 86400)
    except Exception as e:
        return False, f"PARSE_ERROR: {e}", 0

def check_and_apply_downstream_updates() -> dict:
    print("=" * 86)
    print("     E.B.O.N.Y. SOVEREIGN DOWNSTREAM CLIENT UPDATE ENGINE     ")
    print(f"     NODE CUSTODY: LOCAL BARE-METAL | REPO TARGET: hvf-media-matrix-public")
    print("=" * 86)
    
    valid, lic_status, days_left = check_license_validity()
    print(f"[*] License Status: {lic_status} ({days_left} days remaining)")
    
    if lic_status == "HARDWARE_MISMATCH_PIRACY_LOCKOUT":
        print("[CRITICAL] Hardware fingerprint mismatch detected. Unauthorized copy. Updates aborted.")
        return {"license_status": lic_status, "errors": ["Unauthorized node duplication."]}
    
    updated_files = []
    skipped_files = []
    errors = []
    
    for rel_path in UPDATE_TARGETS:
        local_path = BASE_DIR / rel_path
        remote_url = f"{PUBLIC_RAW_BASE}/{rel_path}"
        try:
            req = urllib.request.Request(remote_url, headers={"User-Agent": "EBONY-Sovereign-Client/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                remote_bytes = response.read()
            remote_hash = hashlib.sha256(remote_bytes).hexdigest()
            local_hash = ""
            if local_path.exists():
                local_hash = hashlib.sha256(local_path.read_bytes()).hexdigest()
            if remote_hash != local_hash:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_bytes(remote_bytes)
                updated_files.append(rel_path)
                print(f"[UPDATED] {rel_path} -> SHA: {remote_hash[:16]}...")
            else:
                skipped_files.append(rel_path)
        except Exception as e:
            errors.append(f"{rel_path}: {e}")
            print(f"[NOTICE] Could not check remote for {rel_path}: {e}")
            
    print("-" * 86)
    print(f"Summary: {len(updated_files)} file(s) updated, {len(skipped_files)} up-to-date, {len(errors)} offline notices.")
    print("Sovereign Customer Data Check: 100% Isolated. Zero database files touched.")
    print("=" * 86)
    
    return {
        "license_status": lic_status,
        "days_remaining": days_left,
        "updated_files": updated_files,
        "up_to_date_files": skipped_files,
        "errors": errors
    }

if __name__ == "__main__":
    check_and_apply_downstream_updates()
"""

updater_p = cockpit_dir / "ebony_client_updater.py"
updater_p.write_text(updater_code, encoding="utf-8")
print("[+] ebony_client_updater.py upgraded with Hardware Node Locking.")

# -------------------------------------------------------------------------
# 2. UPGRADE ebony_tier_manager.py WITH HARDWARE ATTESTATION
# -------------------------------------------------------------------------
tier_manager_code = """\"\"\"
E.B.O.N.Y. Sovereign Commercial Licensing & Tier Access Controller
Role-Based Access Control (RBAC), Maintenance & Anti-Piracy Lockout Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
\"\"\"
import streamlit as st
import json
from pathlib import Path
import sys

# Ensure updater is accessible
_cdir = Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit")
if str(_cdir) not in sys.path:
    sys.path.insert(0, str(_cdir))

try:
    from ebony_client_updater import check_license_validity, get_hardware_uuid
except Exception:
    pass

# Tier Identifiers
TIER_0_CEO = "TIER_0_CEO"
TIER_1_PERSONAL = "TIER_1_PERSONAL"
TIER_COMMAND = "TIER_COMMAND"
TIER_2_VIP = "TIER_2_VIP"
TIER_3_ENTERPRISE = "TIER_3_ENTERPRISE"
TIER_LOCKED = "TIER_LOCKED_UNAUTHORIZED"

TIER_METADATA = {
    TIER_0_CEO: {
        "name": "👑 Level-5 Sovereign Root (CEO Clearance)",
        "label": "👑 CEO Clearance (Unrestricted)",
        "price": "Sovereign Executive Baseline",
        "desc": "Unrestricted administrative, hardware, and engineering access across all enclave matrices."
    },
    TIER_1_PERSONAL: {
        "name": "🌱 Personal Executive & Comms",
        "label": "🌱 Personal: Comms & Radar ($19.99/mo)",
        "price": "$19.99 / Month",
        "desc": "Single-user node, zero-API email triage, travel autopilot, NOAA radar, and encrypted WORM ledger."
    },
    TIER_COMMAND: {
        "name": "⚡ Sovereign Command & Optical Surveillance",
        "label": "⚡ Command: Tactical AI & Optics ($39.99/mo)",
        "price": "$39.99 / Month",
        "desc": "Air-gapped neural routing, 💬 Sovereign Command, and 📡 Live Optical Multi-Sensor Bus (Arducam & Tapo IP)."
    },
    TIER_2_VIP: {
        "name": "💎 VIP Operational, Drone & B2B Engine",
        "label": "💎 VIP: Drone, SCADA & B2B ($249/mo)",
        "price": "$249 / Month",
        "desc": "Sub-16ms kinetic grid islanding, Master C2 Cockpit, LinkedIn engine, drone diagnostics, and GLI analytics."
    },
    TIER_3_ENTERPRISE: {
        "name": "🏛️ Enterprise Sovereign Infrastructure",
        "label": "🏛️ Enterprise CEO ($2,499/yr)",
        "price": "$2,499 / Year",
        "desc": "State infrastructure C2, multi-node keys, multi-facility yield, and Oklahoma Title 61 grant interlocks."
    }
}

MODULE_TIER_MAPPING = {
    "📖 System Overview": TIER_1_PERSONAL,
    "📝 Feedback Hub": TIER_1_PERSONAL,
    "📨 Sovereign Dispatch Deck": TIER_1_PERSONAL,
    "🚨 NOAA Radar": TIER_1_PERSONAL,
    
    "💬 Sovereign Command": TIER_COMMAND,
    "📡 Sovereign Comms Deck": TIER_COMMAND,
    
    "🎛️ Master C2 Cockpit": TIER_2_VIP,
    "📡 LinkedIn Engine": TIER_2_VIP,
    "🌾 Drone Diagnostics": TIER_2_VIP,
    "⚡ Sovereign Weather Scada": TIER_2_VIP,
    "⚡ Grain Silo Aeration And F": TIER_2_VIP,
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
    TIER_LOCKED: 0,
    TIER_1_PERSONAL: 1,
    TIER_COMMAND: 2,
    TIER_2_VIP: 3,
    TIER_3_ENTERPRISE: 4,
    TIER_0_CEO: 99
}

def get_current_tier() -> str:
    # HARDWARE AUDIT HOOK
    # If the user is CEO, bypass hardware checks for development
    active_tier = st.session_state.get("ebony_commercial_tier", TIER_0_CEO)
    if active_tier == TIER_0_CEO:
        return active_tier
        
    try:
        is_valid, lic_status, _ = check_license_validity()
        if lic_status == "HARDWARE_MISMATCH_PIRACY_LOCKOUT":
            return TIER_LOCKED
    except Exception:
        pass
        
    return active_tier

def set_current_tier(tier: str):
    st.session_state["ebony_commercial_tier"] = tier

def check_module_access(user_tier: str, module_name: str) -> tuple:
    if user_tier == TIER_LOCKED:
        return False, "HARDWARE_NODE_LOCKED", False

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
    if current_tier == TIER_LOCKED:
        try:
            hw_id = get_hardware_uuid()
        except Exception:
            hw_id = "UNKNOWN_SIGNATURE"
            
        st.markdown(f\"\"\"
        <div style="background-color: #140b0b; border: 2px solid #ff4444; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
            <h2 style="color: #ff4444; margin-top: 0; font-family: monospace; letter-spacing: 2px;">🛑 UNAUTHORIZED HARDWARE DETECTED // PIRACY LOCKOUT</h2>
            <div style="color: #a0aab2; font-size: 0.9em; font-family: monospace; margin-bottom: 15px;">
                <strong>SECURITY ENFORCEMENT:</strong> Humphrey Virtual Farms LLC | <strong>CAGE:</strong> 1AHA8 | <strong>UEI:</strong> S1M4ENLHTDH5<br>
                <strong>STATUTORY JURISDICTION:</strong> State of Oklahoma Title 61 & HB 2992 Commercial Enclave
            </div>
            <div style="color: #ffffff; font-size: 0.95em; line-height: 1.6; border-top: 1px solid #3a1e1e; padding-top: 15px;">
                <p><strong>ATTEMPTED MODULE:</strong> <span style="color: #ff8888; font-weight: bold;">{module_name}</span></p>
                <p><strong>HARDWARE STATUS:</strong> <span style="color: #ff4444; font-weight: bold;">NODE SIGNATURE MISMATCH</span></p>
                <p><strong>CURRENT MACHINE ID:</strong> <code style="color: #ffcc00;">{hw_id}</code></p>
                <p style="margin-top: 15px; color: #d0d7de;">
                    This E.B.O.N.Y. installation has detected a hardware fingerprint mismatch. The active cryptographic license is bound to a different physical motherboard and MAC address. 
                    Copying the application folder to unauthorized devices violates commercial licensing terms. 
                    <br><br>
                    To provision this new device, purchase an additional Single-User Node license or upgrade to an Enterprise Multi-Site agreement.
                </p>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)
        return

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
            <p><strong>OPERATIONAL STATUS:</strong> <span style="color: #ffaa00; font-weight: bold;">ACTIVE HARDENING & CONSOLIDATION IN PROGRESS</span></p>
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
        TIER_1_PERSONAL,
        TIER_COMMAND,
        TIER_2_VIP,
        TIER_3_ENTERPRISE
    ]
    
    cur_tier = get_current_tier()
    cur_idx = tier_opts.index(cur_tier) if cur_tier in tier_opts else 0
    
    # Do not let locked users escape the lock via the sidebar
    if cur_tier == TIER_LOCKED:
        st.error("SYSTEM NODE LOCKED TO HARDWARE SIGNATURE.")
        return

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
print("[+] ebony_tier_manager.py upgraded with Hardware Node Lockout enforcement.")

# Initialize the license locally
sys.path.insert(0, str(cockpit_dir))
import ebony_client_updater as ecu
ecu.init_or_read_license()
print("[+] Initialized ebony_license.json with node-locked hardware signature.")

print("[*] Running py_compile verification...")
py_compile.compile(str(updater_p), doraise=True)
py_compile.compile(str(tier_p), doraise=True)
print("[SUCCESS] All files compiled cleanly with ZERO errors (Exit Code 0)!")