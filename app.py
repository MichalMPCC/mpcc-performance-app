import streamlit as st
from functions import calculate_vo2max, calculate_cp_wprime, estimate_fatmax, estimate_vlamax, fuel_split
import matplotlib.pyplot as plt

st.title("MPCC Performance Report Generator")

name = st.text_input("Athlete Name")
weight = st.number_input("Body Weight (kg)", min_value=30.0, max_value=150.0, value=70.0)
p_5min = st.number_input("5-min Power (W)", value=300)
p_3min = st.number_input("3-min Power (W)", value=320)
p_12min = st.number_input("12-min Power (W)", value=280)
p_15s = st.number_input("15s Peak Power (W)", value=900)
p_1min = st.number_input("1-min Avg Power (W)", value=600)

if st.button("Calculate"):
    vo2max = calculate_vo2max(p_5min, weight)
    cp, w_prime = calculate_cp_wprime(p_3min, p_12min)
    fatmax = estimate_fatmax(p_5min)
    vlamax = estimate_vlamax(p_15s, p_1min)

    st.subheader("Results")
    st.write(f"VO2max: {vo2max:.1f} ml/kg/min")
    st.write(f"CP: {cp:.1f} W")
    st.write(f"W′: {w_prime:.1f} kJ")
    st.write(f"VLamax: {vlamax:.2f} mmol/l/s")
    st.write(f"FATmax: {fatmax:.0f} W")
