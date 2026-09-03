import streamlit as st
import requests

st.set_page_config(page_title="Ebony Command Deck", layout="wide")
st.title("🟢 Ebony Command Deck (Sovereign Node)")

API_URL = "http://127.0.0.1:8000"
HEADERS = {"x-auth-token": "CEO_OVERRIDE"}

tab1, tab2 = st.tabs(["Command & Telemetry", "Asset Synthesis"])

with tab1:
    st.header("Matrix Telemetry")
    if st.button("Ping Matrix"):
        try:
            res = requests.get(f"{API_URL}/telemetry", headers=HEADERS)
            st.json(res.json())
        except Exception as e:
            st.error(f"Matrix Offline: {e}")

    if st.button("Engage Autonomous Loop"):
        try:
            res = requests.post(f"{API_URL}/autonomous/engage", headers=HEADERS)
            st.success(res.json()["message"])
        except Exception as e:
            st.error(f"Matrix Offline: {e}")

with tab2:
    st.header("Sovereign Image Synthesis")
    prompt = st.text_input("Enter Graphic Prompt:")
    if st.button("Generate Asset"):
        try:
            res = requests.post(f"{API_URL}/synthesis/image", params={"prompt": prompt}, headers=HEADERS)
            st.info(res.json()["message"])
        except Exception as e:
            st.error(f"Matrix Offline: {e}")
