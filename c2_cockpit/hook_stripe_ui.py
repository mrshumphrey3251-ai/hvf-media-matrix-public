import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_tier_manager.py")
content = target.read_text(encoding="utf-8")

# Ensure ebony_stripe_billing imports
stripe_import = """from ebony_stripe_billing import get_checkout_url_for_tier, STRIPE_TIER_CATALOG"""

if "from ebony_stripe_billing import" not in content:
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines[:30]):
        if line.startswith("import ") or line.startswith("from "):
            insert_idx = i + 1
    content = "".join(lines[:insert_idx]) + "\n" + stripe_import + "\n" + "".join(lines[insert_idx:])

# Replace render_tier_restriction_screen upgrade buttons with direct Stripe checkout hooks
new_render_tier_restriction = '''def render_tier_restriction_screen(module_name: str, required_tier_name: str, current_tier: str):
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
                    This subscription has reached its maximum authorized device quota:
                    <br>• Tier 1: 1 Device Node ($19.99/mo)
                    <br>• Tier 1.5: 3 Device Nodes ($39.99/mo)
                    <br>• Tier 2: 5 Device Nodes ($249/mo)
                    <br>• Tier 3: 10 Device Nodes ($2,499/yr)
                    <br><br>
                    To authorize this new physical machine, upgrade your subscription tier to unlock additional hardware seats.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    cur_meta = TIER_METADATA.get(current_tier, {})
    required_tier_key = MODULE_TIER_MAPPING.get(module_name, TIER_COMMAND)
    checkout_url = get_checkout_url_for_tier(required_tier_key)
    
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
                Access to this sovereign command capability is governed by commercial licensing tiers. Select the Stripe Checkout option below to instantly unlock this capability.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 2.2, 1.2])
    with col2:
        with st.container(border=True):
            st.markdown(f"#### 💳 Commercial Upgrade: {required_tier_name}")
            st.markdown("Direct automated billing powered by **Stripe Sovereign Ingress** under **CAGE 1AHA8**.")
            st.link_button("💳 PROCEED TO SECURE STRIPE CHECKOUT", url=checkout_url, use_container_width=True)
            
            if st.button("⬅ RETURN TO DISPATCH DECK", key=f"btn_ret_comms_{module_name}", use_container_width=True):
                st.session_state["nav_module_override"] = "📨 Sovereign Dispatch Deck"
                st.rerun()'''

start_fn = content.find("def render_tier_restriction_screen")
if start_fn != -1:
    end_fn = content.find("def render_maintenance_screen", start_fn)
    content = content[:start_fn] + new_render_tier_restriction + "\n\n" + content[end_fn:]
    target.write_text(content, encoding="utf-8")
    print("[+] Successfully bound Stripe checkout link buttons to ebony_tier_manager.py.")

py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_tier_manager.py compiled cleanly with exit code 0!")