import streamlit as st
from functions import (
    calculate_vo2max,
    calculate_cp_wprime,
    estimate_fatmax,
    estimate_vlamax,
    fuel_split
)
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="MPCC Performance Report", layout="centered")
st.title("MPCC Performance Report Generator")

# Input
name = st.text_input("Athlete Name")
weight = st.number_input("Body Weight (kg)", min_value=30.0, max_value=150.0, value=70.0)
p_5min = st.number_input("5-min Power (W)", value=300)
p_3min = st.number_input("3-min Power (W)", value=320)
p_12min = st.number_input("12-min Power (W)", value=280)
p_15s = st.number_input("15s Peak Power (W)", value=900)
p_1min = st.number_input("1-min Avg Power (W)", value=600)

if st.button("Calculate"):
    # Calculations
    vo2max = calculate_vo2max(p_5min, weight)
    cp, w_prime = calculate_cp_wprime(p_3min, p_12min)
    fatmax = estimate_fatmax(p_5min)
    vlamax = estimate_vlamax(p_15s, p_1min)

    # Results
    st.subheader("Performance Metrics")
    st.write(f"**VO2max:** {vo2max:.1f} ml/kg/min")
    st.write(f"**Critical Power (CP):** {cp:.1f} W")
    st.write(f"**W′ (Anaerobic Work Capacity):** {w_prime:.1f} kJ")
    st.write(f"**VLamax (Estimate):** {vlamax:.2f} mmol/l/s")
    st.write(f"**FATmax Estimate:** {fatmax:.0f} W")

    # Chart
    st.subheader("Power Duration Curve")
    durations = [15, 60, 180, 300, 720]
    powers = [p_15s, p_1min, p_3min, p_5min, p_12min]

    x = np.linspace(10, 900, 200)
    y = w_prime * 1000 / x + cp  # simple 2-parameter model fit

    fig, ax = plt.subplots()
    ax.plot(x, y, label="Model Fit", color="blue")
    ax.scatter(durations, powers, color="red", label="Test Data")
    ax.axhline(cp, color="gray", linestyle="--", label="CP")
    ax.set_xlabel("Duration (s)")
    ax.set_ylabel("Power (W)")
    ax.set_title("Power Duration Curve")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
