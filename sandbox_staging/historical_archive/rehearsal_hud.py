import streamlit as st
import json, os, time

st.set_page_config(page_title="EBONY TACTICAL HUD", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>body {background-color: #070b14; color: #f8fafc;} .stApp {background-color: #070b14;}</style>", unsafe_allow_html=True)

st.title("🛡️ PROJECT EBONY: SOVEREIGN SCADA C2")
st.subheader("OKLAHOMA COMMERCE EVALUATION DOCKET // CAGE: 1AHA8")

proof_file = os.path.join(os.path.dirname(__file__), "live_evaluator_proof.json")

# Auto-refresh loop placeholder
status_container = st.empty()
proof_container = st.empty()

with status_container.container():
    st.info("📡 WAITING FOR COMMAND DECK PROOF DISPATCH...")

if os.path.exists(proof_file):
    with open(proof_file, "r") as f:
        try:
            data = json.load(f)
            with status_container.container():
                st.success(f"**LIVE PROOF CAPTURED:** {data['title']}")
            
            with proof_container.container():
                st.markdown(f"### ❓ Evaluator Inquiry: *{data['evaluator_query']}*")
                st.markdown("---")
                cols = st.columns(len(data['telemetry']) if len(data['telemetry']) < 5 else 4)
                
                i = 0
                for k, v in data['telemetry'].items():
                    with cols[i % 4]:
                        st.metric(label=k.replace("_", " "), value=str(v).split()[0], delta="Verified")
                    i += 1
                
                st.markdown("---")
                st.json(data)
                
        except json.JSONDecodeError:
            pass

time.sleep(2)
st.rerun()
