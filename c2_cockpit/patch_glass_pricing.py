import re
import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target file not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

# Find where the commercial subscriptions section starts
start_idx = -1
for i, line in enumerate(lines):
    if "Commercial Subscriptions & Features" in line:
        start_idx = i
        break

if start_idx == -1:
    print("[ERROR] Could not find the Commercial Subscriptions & Features section.")
    sys.exit(1)

# Find where the pricing section ends (usually the Master Platform Root header)
end_idx = -1
for i in range(start_idx + 1, len(lines)):
    if "[MASTER PLATFORM ROOT]" in lines[i] or "👑" in lines[i] and "Live Diagnostic Mesh" in lines[i]:
        # Walk backward to find the empty line or header start
        end_idx = i
        while end_idx > start_idx and lines[end_idx - 1].strip() == "":
            end_idx -= 1
        break

if end_idx == -1:
    # Fallback: scan for next st.markdown or st.write at the same or lesser indentation
    base_indent = lines[start_idx][:len(lines[start_idx]) - len(lines[start_idx].lstrip())]
    for i in range(start_idx + 1, len(lines)):
        l_ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
        if lines[i].strip() and len(l_ind) <= len(base_indent) and ("st.markdown(" in lines[i] or "st.subheader(" in lines[i]):
            end_idx = i
            break

if end_idx == -1:
    end_idx = start_idx + 30 # Safe boundary fallback

indent = lines[start_idx][:len(lines[start_idx]) - len(lines[start_idx].lstrip())]

new_cards = f"""{indent}st.markdown("### 💳 Commercial Subscriptions & Features")
{indent}tc1, tc2, tc3, tc4, tc5 = st.columns(5)
{indent}with tc1:
{indent}    with st.container(border=True):
{indent}        st.markdown("#### 🌱 PERSONAL\\n**$19.99/mo**")
{indent}        st.caption("✔ Single-User Node\\n✔ Sovereign Email Triage\\n✔ 🚨 NOAA Weather Radar\\n✔ Encrypted Vault")
{indent}with tc2:
{indent}    with st.container(border=True):
{indent}        st.markdown("#### ⚡ COMMAND\\n**$39.99/mo**")
{indent}        st.caption("✔ Everything in Personal\\n✔ 💬 Sovereign Command AI\\n✔ Neural Prompt Routing\\n✔ Contextual Ghostwriter")
{indent}with tc3:
{indent}    with st.container(border=True):
{indent}        st.markdown("#### 💎 VIP MEMBER\\n**$249/mo**")
{indent}        st.caption("✔ Everything in Command\\n✔ 🎛️ Master C2 Cockpit\\n✔ 🌾 Drone Diagnostics\\n✔ 📡 LinkedIn Engine")
{indent}with tc4:
{indent}    with st.container(border=True):
{indent}        st.markdown("#### 🏛️ ENTERPRISE\\n**$2,499/yr**")
{indent}        st.caption("✔ Everything in VIP\\n✔ State Title 61 Master\\n✔ Multi-Site Admin Keys\\n✔ Dedicated Grant Deck")
{indent}with tc5:
{indent}    with st.container(border=True):
{indent}        st.markdown("#### 📦 APPLIANCE\\n**$4,950 setup**")
{indent}        st.caption("✔ Bare-Metal Hardware\\n✔ 100% Air-Gapped Rack\\n✔ sub-16ms Kinetic Island\\n✔ + $299/mo Maint.")\n\n"""

# Replace the block
final_lines = lines[:start_idx] + [new_cards] + lines[end_idx:]
target.write_text("".join(final_lines), encoding="utf-8")
print("[+] Harmonized 5-column commercial pricing grid mounted onto glass.")

print("[*] Running py_compile verification...")
try:
    py_compile.compile(str(target), doraise=True)
    print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")
except py_compile.PyCompileError as e:
    print(f"[COMPILATION ERROR] {e}")
    sys.exit(1)