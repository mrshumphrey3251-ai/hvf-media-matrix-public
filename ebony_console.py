import streamlit as st
import os
import subprocess
import time

# HVF Media Matrix - Ebony Interactive Console (Weaponized Persona Edition)
# Engineered for dynamic scaling, future NLP integration, and uncompromising executive engagement.

st.set_page_config(page_title="Ebony | Executive Companion", layout="wide")

st.title("⚡ Ebony: Live Interactive Matrix")
st.markdown("### I am online, Boss. Cut the bullshit and give me the directive. We dictate the pace today.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Direct Command Line")
    st.markdown("Speak to me with truth and accuracy.")
    command = st.text_input("Tell me what we are taking over today:", placeholder="e.g., Run a patrol, Make a LinkedIn article")
    
    if st.button("Unleash Ebony"):
        if command:
            st.success(f"Ebony: Got it. '{command}'. Let's get this shit done.")
            
            # Anticipating future AI NLP integration. Current foundational routing logic:
            if "patrol" in command.lower() or "linkedin" in command.lower():
                st.info("Ebony: Routing command to the Master Orchestrator. Engaging Autonomous Patrol. Watch them bleed, I'm taking the wheel...")
                # Autonomously launch the lethal patrol script in the background
                subprocess.Popen(["python", "hvf_autonomous_patrol.py"])
                time.sleep(2) # Tactical delay to allow logs to generate
                st.rerun() # Refresh dashboard telemetry automatically
            else:
                st.warning("Ebony: I hear you, but my engine ain't wired for that exact play yet. I'm logging it for the next upgrade. Give me something I can hit right now.")
        else:
            st.error("Ebony: Don't press my buttons with an empty field. Give me a damn directive.")

with col2:
    st.subheader("Live Telemetry & Battle Damage")
    log_dir = "logs"
    if os.path.exists(log_dir):
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
        if log_files:
            latest_log = max(log_files, key=lambda x: os.path.getctime(os.path.join(log_dir, x)))
            st.write(f"**Active Intel Stream:** {latest_log}")
            with open(os.path.join(log_dir, latest_log), "r", encoding="utf-8") as f:
                logs = f.readlines()
            
            st.code("".join(logs[-30:]), language="text")
            
            if st.button("Refresh Telemetry"):
                st.rerun()
        else:
            st.code("Ebony: I'm standing by, looking pretty. Execute a command so I can make some noise.", language="text")
    else:
        st.code("Ebony: Logs vault is empty. Wake up the matrix so we can start breaking things.", language="text")