"""
MODULE_NAME: action_desk
AUTHOR: Jeffery Humphrey (CEO Clearance)
ROLE: Master Operational Action Desk & Sovereign Dispatch Matrix
"""

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
    in_prog = len([i for i in items if i.get("status") == "IN_PROGRESS"])
    pending = len([i for i in items if i.get("status") == "PENDING"])
    verified = len([i for i in items if i.get("status") == "VERIFIED"])

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
                new_id = "ACT-" + str(100 + len(items) + 1)
                items.append({
                    "id": new_id,
                    "task": new_task.strip(),
                    "priority": new_prio,
                    "status": "PENDING",
                    "owner": new_owner.strip()
                })
                save_items(items)
                st.success("Mission " + new_id + " dispatched.")
                st.rerun()

    st.markdown("#### ⚡ Active Operations Queue")
    for idx, item in enumerate(items):
        item_id = str(item.get("id", "ACT-000"))
        task_desc = str(item.get("task", ""))
        priority = str(item.get("priority", "NORMAL"))
        status = str(item.get("status", "PENDING"))
        owner = str(item.get("owner", "Unassigned"))

        with st.container():
            c_badge, c_desc, c_stat, c_act = st.columns([1, 4, 2, 2])
            
            prio_color = "🔴" if priority == "CRITICAL" else ("🟠" if priority == "HIGH" else "🟢")
            c_badge.markdown(prio_color + " **" + item_id + "**")
            c_desc.markdown("**" + task_desc + "**")
            c_desc.caption("Owner: " + owner)

            stat_index = ["PENDING", "IN_PROGRESS", "VERIFIED"].index(status) if status in ["PENDING", "IN_PROGRESS", "VERIFIED"] else 0
            new_status = c_stat.selectbox(
                "Status",
                ["PENDING", "IN_PROGRESS", "VERIFIED"],
                index=stat_index,
                key="stat_" + item_id
            )
            if new_status != status:
                items[idx]["status"] = new_status
                save_items(items)
                st.rerun()

            if c_act.button("🗑️ Remove", key="del_" + item_id):
                items.pop(idx)
                save_items(items)
                st.rerun()
            st.divider()
