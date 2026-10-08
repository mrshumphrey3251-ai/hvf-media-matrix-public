"""
MODULE: Hydrology Pump Controller
ROLE: Real-time irrigation density calculation and cavitation interlocks.
"""
import streamlit as st

def render():
    tactical_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800;900&display=swap');
    
    .metric-card {
        background: #0b1324;
        border: 1px solid #1e293b;
        border-left: 4px solid #00f3ff;
        padding: 20px;
        border-radius: 4px;
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-val { font-size: 38px; font-weight: 900; color: #00f3ff; font-family: 'JetBrains Mono', monospace; }
    .metric-lbl { font-size: 14px; font-weight: 800; color: #94a3b8; letter-spacing: 1.5px; }
    
    @keyframes flash { 0% { opacity: 1; text-shadow: 0 0 20px #ff0000; } 50% { opacity: 0.5; text-shadow: none; } 100% { opacity: 1; text-shadow: 0 0 20px #ff0000; } }
    .alert-red { background: #2a0a0a; border: 2px solid #ff0000; padding: 20px; text-align: center; color: #ff0000; font-weight: 900; font-size: 22px; animation: flash 1s infinite; font-family: 'JetBrains Mono', monospace; }
    .alert-green { background: #022c16; border: 2px solid #10b981; padding: 20px; text-align: center; color: #10b981; font-weight: 900; font-size: 22px; font-family: 'JetBrains Mono', monospace; }
    </style>
    """
    st.markdown(tactical_css, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #00f3ff; font-family: \"JetBrains Mono\", monospace; text-transform: uppercase;'>💧 Sovereign Hydrology Pump Controller</h3>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("<div style='color: #94a3b8; font-weight: bold; margin-bottom: 10px;'>🎛️ MANUAL SWITCHGEAR</div>", unsafe_allow_html=True)
        pressure = st.slider("Deep Well Pressure (PSI)", min_value=0, max_value=150, value=85, step=1)
        gpm = st.slider("GPM Flow Rate", min_value=0, max_value=2000, value=1200, step=10)
        acres = st.number_input("Active Field Sector (Acres)", min_value=1.0, value=120.0, step=1.0)

    with col2:
        st.markdown("<div style='color: #94a3b8; font-weight: bold; margin-bottom: 10px;'>📊 ACTIVE KINETIC TELEMETRY</div>", unsafe_allow_html=True)
        
        # Real-Time Irrigation Density Math
        density = (gpm * 60) / acres
        
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-lbl">GALLONS / ACRE / HOUR</div>
            <div class="metric-val">{density:,.1f}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Dynamic Cavitation Interlock
        if pressure < 40:
            st.markdown('<div class="alert-red">⚠ CRITICAL: CAVITATION RISK</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-green">🟢 PUMPS NOMINAL</div>', unsafe_allow_html=True)
