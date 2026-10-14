"""
E.B.O.N.Y. Sovereign Commercial Licensing & Tier Access Controller
Role-Based Access Control (RBAC) & Maintenance Lockout Engine
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import streamlit as st
import json
from pathlib import Path

# Commercial Tier Identifiers
TIER_0_CEO = "TIER_0_CEO"
TIER_1_PERSONAL = "TIER_1_PERSONAL"
TIER_COMMAND = "TIER_COMMAND"
TIER_2_VIP = "TIER_2_VIP"
TIER_3_ENTERPRISE = "TIER_3_ENTERPRISE"

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
    # Tier 1: Personal ($19.99/mo and above)
    "📖 System Overview": TIER_1_PERSONAL,
    "📝 Feedback Hub": TIER_1_PERSONAL,
    "📨 Sovereign Dispatch Deck": TIER_1_PERSONAL,
    "🚨 NOAA Radar": TIER_1_PERSONAL,
    
    # Tier 1.5: Sovereign Command ($39.99/mo and above)
    "💬 Sovereign Command": TIER_COMMAND,
    "📡 Sovereign Comms Deck": TIER_COMMAND,  # Active in Tier 1.5 (Optical Matrix & Sensors)
    
    # Tier 2: VIP Member ($249/mo and above)
    "🎛️ Master C2 Cockpit": TIER_2_VIP,
    "📡 LinkedIn Engine": TIER_2_VIP,
    "🌾 Drone Diagnostics": TIER_2_VIP,
    "⚡ Sovereign Weather Scada": TIER_2_VIP,
    "⚡ Grain Silo Aeration And F": TIER_2_VIP,
}

# Incomplete, Utility & Internal Engineering Scripts Locked Under Maintenance
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
    TIER_1_PERSONAL: 1,
    TIER_COMMAND: 2,
    TIER_2_VIP: 3,
    TIER_3_ENTERPRISE: 4,
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
    st.markdown(f"""
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
    """, unsafe_allow_html=True)
    
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
    st.markdown(f"""
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
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        if st.button("⬅ RETURN TO DISPATCH DECK", key=f"btn_ret_auth_{module_name}", use_container_width=True):
            st.session_state["nav_module_override"] = "📨 Sovereign Dispatch Deck"
            st.rerun()

def render_tier_switcher_sidebar():
    st.markdown("""
    <div style="background-color: #0b110e; border: 1px solid #00ff88; border-radius: 6px; padding: 10px; margin-bottom: 10px;">
        <div style="color: #00ff88; font-weight: bold; font-size: 0.8em; letter-spacing: 1px;">ACTIVE LICENSE TIER</div>
    </div>
    """, unsafe_allow_html=True)
    
    tier_opts = [
        TIER_0_CEO,
        TIER_1_PERSONAL,
        TIER_COMMAND,
        TIER_2_VIP,
        TIER_3_ENTERPRISE
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
