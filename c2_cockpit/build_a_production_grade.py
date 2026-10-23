import streamlit as st

st.set_page_config(page_title="Battery SCADA Monitor", layout="centered", initial_sidebar_state="collapsed")

# High‑tech dark‑mode CSS with glowing borders
st.markdown(
    """
    <style>
    .metric-card {
        background: #111;
        border: 2px solid #00ffea;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 0 15px #00ffea;
        color: #fff;
    }
    .metric-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #00ffea;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-top: 5px;
    }
    .alert {
        color: #ff4d4d;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def render():
    st.title("⚡ Battery SCADA Monitor")
    st.subheader("Real‑time metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        voltage = st.number_input("Bus Voltage (V)", min_value=0.0, max_value=1000.0, value=400.0, step=0.1)
    with col2:
        temperature = st.number_input("Pack Temperature (°C)", min_value=-40.0, max_value=150.0, value=30.0, step=0.1)
    with col3:
        capacity = st.number_input("Battery Capacity (Ah)", min_value=0.0, max_value=10000.0, value=200.0, step=1.0)

    # SoC calculation (simple linear approximation)
    min_v, max_v = 300.0, 420.0  # typical Li‑ion voltage range
    soc = max(0.0, min(100.0, ((voltage - min_v) / (max_v - min_v)) * 100))

    # Render metric cards
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-title">State of Charge (SoC)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{soc:.1f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-title">Bus Voltage</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{voltage:.2f} V</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-title">Pack Temperature</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{temperature:.1f} °C</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Contactor isolation logic
    if temperature > 55.0:
        st.warning("⚠️ Temperature exceeds safe limit! Initiating contactor isolation.")
        if st.button("Isolate Contactors Now"):
            st.success("✅ Contactors isolated.")
    else:
        st.success("✅ All systems nominal.")

if __name__ == "__main__":
    render()