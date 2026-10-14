"""
E.B.O.N.Y. Sovereign Commercial Licensing & Tier Access Controller
Role-Based Access Control (RBAC), 7-Day Pilot (Tier 1 & 1.5) & Optical Maintenance Enclave
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
Statutory Authority: Oklahoma Title 61 & OK HB 2992
"""
import streamlit as st
import json
from pathlib import Path
import sys

_cdir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
if str(_cdir) not in sys.path:
    sys.path.insert(0, str(_cdir))

try:
    from ebony_client_updater import check_license_validity, get_hardware_uuid, init_or_read_license
except Exception:
    def get_hardware_uuid():
        return "UNKNOWN_SIGNATURE"
    def check_license_validity():
        return True, "ACTIVE", 30
    def init_or_read_license():
        return {}

try:
    from ebony_stripe_billing import get_checkout_url_for_tier, STRIPE_TIER_CATALOG
except Exception:
    def get_checkout_url_for_tier(t):
        return "", False
    STRIPE_TIER_CATALOG = {}

try:
    from ebony_license_issuer import generate_sovereign_license, install_license_to_disk
except Exception:
    pass

# Commercial Tier Identifiers
TIER_0_CEO = "TIER_0_CEO"
TIER_1_PERSONAL = "TIER_1_PERSONAL"
TIER_COMMAND = "TIER_COMMAND"
TIER_2_VIP = "TIER_2_VIP"
TIER_3_ENTERPRISE = "TIER_3_ENTERPRISE"
TIER_LOCKED = "TIER_LOCKED_UNAUTHORIZED"
TIER_EXPIRED = "TIER_EXPIRED"

TIER_NODE_LIMITS = {
    TIER_1_PERSONAL: 1,     # 1 Device Node ($19.99/mo)
    TIER_COMMAND: 3,        # 3 Device Nodes ($39.99/mo)
    TIER_2_VIP: 5,          # 5 Device Nodes ($249/mo)
    TIER_3_ENTERPRISE: 10,  # 10 Device Nodes ($2,499/yr)
    TIER_0_CEO: 999         # Unlimited Enterprise Operation Nodes
}

TIER_METADATA = {
    TIER_0_CEO: {
        "name": "👑 Level-5 Sovereign Root (CEO Clearance)",
        "label": "👑 CEO Clearance (Unlimited Nodes)",
        "price": "Sovereign Executive Baseline",
        "nodes": "Unlimited Nodes",
        "desc": "Unrestricted administrative, hardware, and engineering access across unlimited machines."
    },
    TIER_1_PERSONAL: {
        "name": "🌱 Personal Executive & Comms (1 Device)",
        "label": "🌱 Personal: 1 Device ($19.99/mo)",
        "price": "$19.99 / Month",
        "nodes": "1 Device Node",
        "desc": "Single-user node, zero-API email triage, travel autopilot, NOAA radar, and encrypted WORM ledger."
    },
    TIER_COMMAND: {
        "name": "⚡ Sovereign Command & Tactical AI (3 Devices)",
        "label": "⚡ Command: 3 Devices ($39.99/mo)",
        "price": "$39.99 / Month",
        "nodes": "3 Device Nodes",
        "desc": "Air-gapped neural routing and 💬 Sovereign Command across up to 3 authorized machines."
    },
    TIER_2_VIP: {
        "name": "💎 VIP Operational, Drone & B2B Engine (5 Devices)",
        "label": "💎 VIP: 5 Devices ($249/mo)",
        "price": "$249 / Month",
        "nodes": "5 Device Nodes",
        "desc": "Sub-16ms kinetic grid islanding, Master C2 Cockpit, LinkedIn engine, drone diagnostics, and GLI analytics across up to 5 machines."
    },
    TIER_3_ENTERPRISE: {
        "name": "🏛️ Enterprise Sovereign Infrastructure (10 Devices)",
        "label": "🏛️ Enterprise: 10 Devices ($2,499/yr)",
        "price": "$2,499 / Year",
        "nodes": "10 Device Nodes",
        "desc": "State infrastructure C2, 10 multi-node keys, multi-facility yield, and Oklahoma Title 61 grant interlocks."
    }
}

MODULE_TIER_MAPPING = {
    "📖 System Overview": None,              # Open public overview and license store
    "📝 Feedback Hub": TIER_1_PERSONAL,
    "📨 Sovereign Dispatch Deck": TIER_1_PERSONAL,
    "🚨 NOAA Radar": TIER_1_PERSONAL,
    
    "💬 Sovereign Command": TIER_COMMAND,
    
    "🎛️ Master C2 Cockpit": TIER_2_VIP,
    "📡 LinkedIn Engine": TIER_2_VIP,
    "🌾 Drone Diagnostics": TIER_2_VIP,
    "⚡ Sovereign Weather Scada": TIER_2_VIP,
    "⚡ Grain Silo Aeration And F": TIER_2_VIP,
}

# Live Optical Sensor Bus cordoned behind Level-5 R&D Maintenance Wall until completed
MAINTENANCE_MODULES = [
    "📡 Sovereign Comms Deck",
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
    TIER_EXPIRED: 0,
    TIER_LOCKED: 0,
    TIER_1_PERSONAL: 1,
    TIER_COMMAND: 2,
    TIER_2_VIP: 3,
    TIER_3_ENTERPRISE: 4,
    TIER_0_CEO: 99
}

def get_current_tier() -> str:
    active_tier = st.session_state.get("ebony_commercial_tier", TIER_0_CEO)
    if active_tier == TIER_0_CEO:
        return active_tier
        
    try:
        is_valid, lic_status, days_left = check_license_validity()
        lic_data = init_or_read_license()
        
        if lic_status == "HARDWARE_MISMATCH_PIRACY_LOCKOUT":
            return TIER_LOCKED
        if lic_status == "EXPIRED" or not is_valid:
            return TIER_EXPIRED
            
        # 7-DAY PILOT SUBSCRIPTION: Granted Tier 1 + Tier 1.5 Command Privileges
        if lic_data.get("license_type") == "7_DAY_SOVEREIGN_PILOT" and is_valid:
            return TIER_COMMAND
    except Exception:
        pass
        
    return active_tier

def set_current_tier(tier: str):
    st.session_state["ebony_commercial_tier"] = tier
    st.session_state["sb_commercial_tier_selector"] = tier

def check_module_access(user_tier: str, module_name: str) -> tuple:
    if module_name == "📖 System Overview":
        return True, "", False

    if user_tier == TIER_LOCKED:
        return False, "HARDWARE_NODE_LIMIT_EXCEEDED", False

    if user_tier == TIER_EXPIRED:
        return False, "7-Day Sovereign Pilot Concluded", False

    # Level-5 R&D Maintenance Lockout (Blocks Sovereign Comms Deck / Opticals)
    if module_name in MAINTENANCE_MODULES:
        if user_tier == TIER_0_CEO:
            return True, "", False
        return False, "Level-5 Sovereign Optical & Systems Engineering Calibration", True

    if user_tier == TIER_0_CEO:
        return True, "", False
        
    required_tier = MODULE_TIER_MAPPING.get(module_name, TIER_0_CEO)
    if required_tier is None:
        return True, "", False

    user_rank = TIER_RANKS.get(user_tier, 1)
    req_rank = TIER_RANKS.get(required_tier, 99)
    
    if user_rank >= req_rank:
        return True, "", False
    else:
        req_meta = TIER_METADATA.get(required_tier, {})
        req_display = f"{req_meta.get('name', 'Higher Tier')} ({req_meta.get('price', '')})"
        return False, req_display, False

def render_tier_restriction_screen(module_name: str, required_tier_name: str, current_tier: str):
    # Lockout 1: Hardware Anti-Piracy Lockout
    if current_tier == TIER_LOCKED:
        try:
            hw_id = get_hardware_uuid()
        except Exception:
            hw_id = "UNKNOWN_SIGNATURE"
            
        st.markdown(f"""
        <div style="background-color: #140b0b; border: 2px solid #ff4444; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
            <h2 style="color: #ff4444; margin-top: 0; font-family: monospace; letter-spacing: 2px;">🛑 DEVICE LIMIT EXCEEDED // PIRACY LOCKOUT</h2>
            <div style="color: #a0aab2; font-size: 0.9em; font-family: monospace; margin-bottom: 15px;">
                <strong>SECURITY ENFORCEMENT:</strong> Humphrey Virtual Farms LLC | <strong>CAGE:</strong> 1AHA8 | <strong>UEI:</strong> S1M4ENLHTDH5<br>
                <strong>STATUTORY JURISDICTION:</strong> State of Oklahoma Title 61 & HB 2992 Commercial Enclave
            </div>
            <div style="color: #ffffff; font-size: 0.95em; line-height: 1.6; border-top: 1px solid #3a1e1e; padding-top: 15px;">
                <p><strong>ATTEMPTED MODULE:</strong> <span style="color: #ff8888; font-weight: bold;">{module_name}</span></p>
                <p><strong>HARDWARE STATUS:</strong> <span style="color: #ff4444; font-weight: bold;">NODE SEAT CAPACITY REACHED</span></p>
                <p><strong>MACHINE FINGERPRINT:</strong> <code style="color: #ffcc00;">{hw_id}</code></p>
                <p style="margin-top: 15px; color: #d0d7de;">
                    This subscription has reached its maximum authorized device quota. Upgrade to unlock additional hardware seats.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Lockout 2: Expired 7-Day Pilot (Displays Tier 1 and Tier 1.5 Live Stripe Checkout Options)
    if current_tier == TIER_EXPIRED:
        t1_url, is_live_t1 = get_checkout_url_for_tier(TIER_1_PERSONAL)
        cmd_url, is_live_cmd = get_checkout_url_for_tier(TIER_COMMAND)
        
        st.markdown(f"""
        <div style="background-color: #1a0b0b; border: 2px solid #ff4444; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
            <h2 style="color: #ff4444; margin-top: 0; font-family: monospace; letter-spacing: 2px;">🛑 7-DAY SOVEREIGN PILOT CONCLUDED // SUBSCRIPTION REQUIRED</h2>
            <div style="color: #a0aab2; font-size: 0.9em; font-family: monospace; margin-bottom: 15px;">
                <strong>SECURITY ENFORCEMENT:</strong> Humphrey Virtual Farms LLC | <strong>CAGE:</strong> 1AHA8 | <strong>UEI:</strong> S1M4ENLHTDH5<br>
                <strong>STATUTORY JURISDICTION:</strong> State of Oklahoma Title 61 & HB 2992 Commercial Enclave
            </div>
            <div style="color: #ffffff; font-size: 0.95em; line-height: 1.6; border-top: 1px solid #3a1e1e; padding-top: 15px;">
                <p><strong>ATTEMPTED MODULE:</strong> <span style="color: #ff8888; font-weight: bold;">{module_name}</span></p>
                <p><strong>PILOT EVALUATION:</strong> <span style="color: #ff4444; font-weight: bold;">7-DAY TRIAL WINDOW EXPIRED</span></p>
                <p style="margin-top: 15px; color: #d0d7de;">
                    Your complimentary 7-day evaluation of Tier 1 (Comms) and Tier 1.5 (Sovereign Command) has concluded. Select an authorized subscription tier below to renew node execution.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("#### 🌱 Tier 1: Personal Comms\n**$19.99 / Month**")
                st.caption("✔ 1 Authorized Device Node\n✔ Sovereign Dispatch Deck\n✔ 🚨 NOAA Radar\n✔ WORM Encrypted Ledger")
                if is_live_t1:
                    st.link_button("💳 ACTIVATE TIER 1 ($19.99/MO)", url=t1_url, width="stretch")
                else:
                    if st.button("⚡ SIMULATE TIER 1 ACTIVATION", key="btn_sim_t1_exp", width="stretch"):
                        lic = generate_sovereign_license("Subscriber", "client@sovereign.org", TIER_1_PERSONAL, duration_days=30)
                        install_license_to_disk(lic)
                        set_current_tier(TIER_1_PERSONAL)
                        st.rerun()
        with c2:
            with st.container(border=True):
                st.markdown("#### ⚡ Tier 1.5: Sovereign Command\n**$39.99 / Month**")
                st.caption("✔ 3 Authorized Device Nodes\n✔ 💬 Sovereign Command AI\n✔ Everything in Tier 1\n✔ Contextual Ghostwriter")
                if is_live_cmd:
                    st.link_button("💳 ACTIVATE TIER 1.5 ($39.99/MO)", url=cmd_url, width="stretch")
                else:
                    if st.button("⚡ SIMULATE TIER 1.5 ACTIVATION", key="btn_sim_cmd_exp", width="stretch"):
                        lic = generate_sovereign_license("Subscriber", "client@sovereign.org", TIER_COMMAND, duration_days=30)
                        install_license_to_disk(lic)
                        set_current_tier(TIER_COMMAND)
                        st.rerun()
        return

    # Lockout 3: Higher Tier Access Gate (Tier 2, Tier 3)
    cur_meta = TIER_METADATA.get(current_tier, {})
    required_tier_key = MODULE_TIER_MAPPING.get(module_name, TIER_COMMAND)
    checkout_url, is_live = get_checkout_url_for_tier(required_tier_key)
    
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
                Access to this sovereign command capability is governed by commercial licensing tiers. Select the checkout option below to unlock active operational glass.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 2.2, 1.2])
    with col2:
        with st.container(border=True):
            st.markdown(f"#### 💳 Commercial Upgrade: {required_tier_name}")
            st.markdown("Direct automated billing powered by **Stripe Sovereign Ingress** under **CAGE 1AHA8**.")
            
            if is_live:
                st.link_button("💳 PROCEED TO SECURE STRIPE CHECKOUT", url=checkout_url, width="stretch")
            else:
                btn_key = f"btn_sim_atomic_{required_tier_key}_{module_name.replace(' ', '_')}"
                if st.button("⚡ SIMULATE STRIPE PAYMENT & PROVISION LICENSE", key=btn_key, width="stretch"):
                    lic = generate_sovereign_license("Verified Subscriber", "ceo@humphreyfarms.org", required_tier_key, duration_days=30, claim_current_node=True)
                    install_license_to_disk(lic)
                    set_current_tier(required_tier_key)
                    st.session_state["tier_upgrade_success_banner"] = f"🎉 Successfully provisioned {required_tier_name} on this hardware node!"
                    st.rerun()
                st.caption("ℹ️ Sovereign Testing Mode: Provisions cryptographic license to disk and unlocks this module instantly without reloading the platform.")
            
            if st.button("⬅ RETURN TO OVERVIEW", key=f"btn_ret_comms_{module_name}", width="stretch"):
                st.session_state["nav_module_override"] = "📖 System Overview"
                st.rerun()

def render_maintenance_screen(module_name: str):
    st.markdown(f"""
    <div style="background-color: #141208; border: 2px solid #ffaa00; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
        <h2 style="color: #ffaa00; margin-top: 0; font-family: monospace; letter-spacing: 2px;">🚧 SOVEREIGN ENCLAVE MAINTENANCE // LEVEL-5 R&D LOCKOUT</h2>
        <div style="color: #a0aab2; font-size: 0.9em; font-family: monospace; margin-bottom: 15px;">
            <strong>CLASSIFICATION:</strong> Humphrey Virtual Farms LLC // Internal Optical Systems Engineering<br>
            <strong>STATUTORY JURISDICTION:</strong> State of Oklahoma Title 61 & OK HB 2992 Framework
        </div>
        <div style="color: #ffffff; font-size: 0.95em; line-height: 1.6; border-top: 1px solid #3a2e1e; padding-top: 15px;">
            <p><strong>MODULE UNDER CALIBRATION:</strong> <span style="color: #ffcc00; font-weight: bold;">{module_name}</span></p>
            <p><strong>OPERATIONAL STATUS:</strong> <span style="color: #ffaa00; font-weight: bold;">LIVE OPTICAL MATRIX & CAMERA BUS ENCLAVED FOR HARDENING</span></p>
            <p style="margin-top: 15px; color: #d0d7de;">
                The Live Optical Multi-Sensor Bus is currently undergoing bare-metal hardware calibration (Arducam, Tapo IP, and local RTSP feeds). This capability remains cordoned behind Level-5 R&D maintenance protocols until operational deployment certification concludes.
            </p>
            <p style="color: #8b949e; font-size: 0.85em;">
                Access is restricted strictly to Level-5 Authorized Systems Engineering Personnel. Commercial subscribers should navigate to active command modules.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        if st.button("⬅ RETURN TO OVERVIEW", key=f"btn_ret_auth_{module_name}", width="stretch"):
            st.session_state["nav_module_override"] = "📖 System Overview"
            st.rerun()

def render_tier_switcher_sidebar():
    st.markdown("""
    <div style="background-color: #0b110e; border: 1px solid #00ff88; border-radius: 6px; padding: 10px; margin-bottom: 10px;">
        <div style="color: #00ff88; font-weight: bold; font-size: 0.8em; letter-spacing: 1px;">ACTIVE LICENSE TIER</div>
    </div>
    """, unsafe_allow_html=True)
    
    if "tier_upgrade_success_banner" in st.session_state:
        st.success(st.session_state["tier_upgrade_success_banner"])
        del st.session_state["tier_upgrade_success_banner"]
    
    # 7-Day Pilot Telemetry HUD
    try:
        is_valid, lic_status, days_left = check_license_validity()
        lic_data = init_or_read_license()
        if lic_data.get("license_type") == "7_DAY_SOVEREIGN_PILOT":
            if is_valid and days_left > 0:
                st.warning(f"⏱️ 7-Day Sovereign Pilot (Tier 1 & 1.5): **{days_left} Days Remaining**")
            elif not is_valid or lic_status == "EXPIRED":
                st.error("🛑 7-Day Pilot Expired: Subscription Required")
    except Exception:
        pass

    tier_opts = [
        TIER_0_CEO,
        TIER_1_PERSONAL,
        TIER_COMMAND,
        TIER_2_VIP,
        TIER_3_ENTERPRISE
    ]
    
    cur_tier = get_current_tier()
    cur_idx = tier_opts.index(cur_tier) if cur_tier in tier_opts else 0
    
    if cur_tier == TIER_LOCKED:
        st.error("HARDWARE LOCKOUT: DEVICE QUOTA EXCEEDED.")
        return
    if cur_tier == TIER_EXPIRED:
        st.error("PILOT CONCLUDED: ALL MODULES LOCKED.")

    def _on_tier_change_callback():
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
    )