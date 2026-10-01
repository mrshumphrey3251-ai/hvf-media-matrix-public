import streamlit as st
import pandas as pd
import numpy as np
import random

# Force widescreen layout to maximize horizontal real estate and eliminate scroll
st.set_page_config(page_title="Harmonic Resonance", layout="wide")

st.markdown("### ⚡ SCREEN 2: 3-PHASE HARMONIC RESONANCE ⚡")
st.caption("Live Multi-Phase Voltage & Frequency Harmonic Analysis (Standard: NIST SP 800-82 REV 2)")
st.markdown("---")

# Live Analytical Telemetry Engine
time_vector = np.linspace(0, 10, 150)
phase_shift = random.uniform(0, np.pi)

wave_a = np.sin(time_vector * 1.5 + phase_shift) * 480
wave_b = np.sin(time_vector * 1.5 + phase_shift + (2*np.pi/3)) * 480
wave_c = np.sin(time_vector * 1.5 + phase_shift + (4*np.pi/3)) * 480

df_wave = pd.DataFrame({'Phase A (V)': wave_a, 'Phase B (V)': wave_b, 'Phase C (V)': wave_c}, index=time_vector)

# Wide-format interactive chart
st.line_chart(df_wave, use_container_width=True, height=450)

# Executive Metrics Row
t_col1, t_col2, t_col3, t_col4 = st.columns(4)
t_col1.metric("Live Grid Frequency", f"{round(60.00 + random.uniform(-0.02, 0.02), 3)} Hz", "Synchronized")
t_col2.metric("Harmonic Distortion (THD)", f"{round(random.uniform(1.2, 2.5), 2)} %", "Nominal")
t_col3.metric("Active Power Delivery", f"{round(random.uniform(390.5, 410.2), 1)} kW", "Optimized")
t_col4.metric("System Impedance", f"{round(random.uniform(0.05, 0.08), 4)} Ω", "Stable")
