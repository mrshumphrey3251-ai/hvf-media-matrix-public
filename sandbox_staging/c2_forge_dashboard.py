"""
C2 COCKPIT: AUTONOMOUS BUILD FORGE WITH ARCHITECTURAL ROUTING (v4.0)
ROLE: CEO directive interface with target selection and module fusion controls.
"""

import streamlit as st
import sys
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
for p in [str(BASE_DIR / "dispatch_core"), str(BASE_DIR / "sandbox_staging"), str(BASE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import sovereign_coder

def render():
    st.markdown("## ⚡ Autonomous Level 5 Build Forge")
    st.caption("CEO Architectural Router | Feature Selection & Destination Dispatch")

    coder = sovereign_coder.SovereignCoder()
    existing_mods = coder.get_existing_modules()

    st.markdown("#### 🎯 Architectural Routing: Where Should This Go?")
    col_mode, col_target = st.columns([1, 1])

    with col_mode:
        deploy_mode = st.radio(
            "Select Deployment Strategy:",
            [
                "📦 Standalone Extension (Create New Module)",
                "🧬 Feature Fusion (Merge into Existing Module)"
            ],
            index=0
        )

    merge_choice = None
    with col_target:
        if "Feature Fusion" in deploy_mode:
            if not existing_mods:
                st.warning("No production modules found to merge into. Defaulting to Standalone.")
            else:
                merge_choice = st.selectbox("Select Target Module to Absorb Feature:", existing_mods)
                st.info(f"Target Destination: `level5_extensions/{merge_choice}` (in-place fusion)")
        else:
            custom_slug = st.text_input("New Module Filename (Optional):", placeholder="e.g., grain_silo_controller.py")

    st.markdown("---")
    st.markdown("#### 📝 Directive: Which Features Do You Want to Add?")
    directive = st.text_area(
        "Specify the exact capabilities, sensors, sliders, or calculations:",
        placeholder="e.g., Integrate Grain Silo Aeration and Fan Power Controller with voltage input sliders and an automated temperature differential calculation",
        height=110
    )

    if st.button("🚀 EXECUTE ARCHITECTURAL SYNTHESIS", type="primary", width="stretch"):
        if not directive.strip():
            st.error("[-] Please specify an executive directive.")
            return

        is_fusion = "Feature Fusion" in deploy_mode and merge_choice
        target_mode = "merge" if is_fusion else "standalone"

        if is_fusion:
            fname = merge_choice
        else:
            if 'custom_slug' in locals() and custom_slug.strip():
                fname = custom_slug.strip()
                if not fname.endswith(".py"):
                    fname += ".py"
            else:
                clean = re.sub(r'[^a-zA-Z0-9_]', '_', directive.lower())[:25].strip("_")
                fname = f"{clean}.py"

        with st.status(f"⚡ Ebony is synthesizing `{fname}`...", expanded=True) as status:
            if is_fusion:
                st.write(f"1️⃣ Pulling base `{merge_choice}` into quarantine sandbox...")
                st.write(f"2️⃣ Merging directive features into existing module architecture...")
            else:
                st.write("1️⃣ Synthesizing standalone Level 5 module via AI inference cascade...")

            result = coder.generate_and_stage(
                module_name=fname,
                specification=directive,
                target_mode=target_mode,
                merge_target=merge_choice
            )

            if result.get("success"):
                st.write("3️⃣ Passed `sandbox_harness.py` quarantine verification (Exit 0).")
                st.write(f"4️⃣ Staged candidate ready for CEO review in `sandbox_staging/{fname}`.")
                status.update(label=f"✅ `{fname}` Synthesized & Verified!", state="complete", expanded=True)
                st.success("Candidate ready. Navigate to the **🛡️ CEO Authorization Gate** to test interactively in the cradle.")
            else:
                st.write("❌ Sandbox quarantine verification failed:")
                st.code(result.get("error", "Unknown validation error"), language="bash")
                status.update(label="[-] Build Failed Quarantine Validation", state="error", expanded=True)
