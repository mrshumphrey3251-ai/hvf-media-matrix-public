code = """\"\"\"
MODULE_NAME: action_desk
AUTHOR: Jeffery Humphrey (CEO Clearance)
ROLE: Master Operational Action Desk & Sovereign Dispatch Matrix
\"\"\"

import streamlit as st
from datetime import datetime, timezone
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "governance" / "architecture" / "ACTION_ITEMS.json"

def load_items():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return [
        {"id": "ACT-101", "task": "Verify Grain Silo Thermal Differential Telemetry", "priority": "HIGH", "status": "IN_PROGRESS", "owner": "Ebony SCADA"},
        {"id": "ACT-102", "task": "Calibrate Weather Station Sensor Array", "priority": "NORMAL", "status": "PENDING", "owner": "Field Ops"},
        {"id": "ACT-103", "task": "Review Merkle Ledger Cryptographic Seals", "priority": "CRITICAL", "status": "VERIFIED", "owner": "CEO Clearance"}
    ]

def save_items(items):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

def render():
    st.markdown("## 📋 Sovereign Action Desk & Operations Dispatch")
    st.caption("Active Level 5 Production Command Deck | Live Task & Mission Pipeline")

    items = load_items()

    col1, col2, col3, col4 = st.columns(4)
    total = len(items)
    in_prog = len([i for i in items if i["status"] == "IN_PROGRESS"])
    pending = len([i for i in items if i["status"] == "PENDING"])
    verified = len([i for i in items if i["status"] == "VERIFIED"])

    col1.metric("Total Missions", total)
    col2.metric("In Progress", in_prog, delta="Active Operations")
    col3.metric("Pending Queue", pending)
    col4.metric("Verified Complete", verified)

    st.markdown("---")

    with st.expander("➕ Dispatch New Operational Action Item", expanded=False):
        c_task, c_prio, c_own = st.columns([3, 1, 1])
        new_task = c_task.text_input("Mission / Task Description:")
        new_prio = c_prio.selectbox("Priority:", ["LOW", "NORMAL", "HIGH", "CRITICAL"], index=1)
        new_owner = c_own.text_input("Assigned Node:", value="Ebony Autonomous")

        if st.button("🚀 DISPATCH MISSION ITEM", type="primary"):
            if new_task.strip():
                new_id = f"ACT-{100 + len(items) + 1}"
                items.append({
                    "id": new_id,
                    "task": new_task.strip(),
                    "priority": new_prio,
                    "status": "PENDING",
                    "owner": new_owner.strip()
                })
                save_items(items)
                st.success(f"Mission {new_id} dispatched.")
                st.rerun()

    st.markdown("#### ⚡ Active Operations Queue")
    for idx, item in enumerate(items):
        with st.container():
            c_badge, c_desc, c_stat, c_act = st.columns([1, 4, 2, 2])
            
            prio_color = "🔴" if item["priority"] == "CRITICAL" else ("🟠" if item["priority"] == "HIGH" else "🟢")
            c_badge.write(f"{prio_color} **{item['id']}**")
            c_desc.write(f"**{item['task']}**\n\n`Owner: {item['owner']}`")
            
            new_status = c_stat.selectbox(
                "Status",
                ["PENDING", "IN_PROGRESS", "VERIFIED"],
                index=["PENDING", "IN_PROGRESS", "VERIFIED"].index(item["status"]),
                key=f"stat_{item['id']}"
            )
            if new_status != item["status"]:
                items[idx]["status"] = new_status
                save_items(items)
                st.rerun()

            if c_act.button("🗑️ Remove", key=f"del_{item['id']}"):
                items.pop(idx)
                save_items(items)
                st.rerun()
            st.divider()
"""

from pathlib import Path
for p in [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\level5_extensions\action_desk.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\level5_extensions\action_desk.py")
]:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[+] Wrote real Action Desk UI to: {p}")
