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

# === INPUT SECTION ===
name = st.text_input("Athlete Name")
weight = st.number_input("Body Weight (kg)", min_value=30.0, max_value=150.0, value=70.0)
p_5min = st.number_input("5-min Power (W)", value=300)
p_3min = st.number_input("3-min Power (W)", value=320)
p_12min = st.number_input("12-min Power (W)", value=280)
p_15s = st.number_input("15s Peak Power (W)", value=900)
p_1min = st.number_input("1-min Avg Power (W)", value=600)

if st.button("Calculate"):
    # === CALCULATIONS ===
    vo2max = calculate_vo2max(p_5min, weight)
    cp, w_prime = calculate_cp_wprime(p_3min, p_12min)
    fatmax = estimate_fatmax(p_5min)
    vlamax = estimate_vlamax(p_15s, p_1min)
    efficiency = cp / (vo2max if vo2max > 0 else 1)

    # === RESULTS ===
    st.subheader("Performance Metrics")
    st.write(f"**VO2max:** {vo2max:.1f} ml/kg/min")
    st.write(f"**Critical Power (CP):** {cp:.1f} W")
    st.write(f"**W′ (Anaerobic Work Capacity):** {w_prime:.1f} kJ")
    st.write(f"**VLamax (Estimate):** {vlamax:.2f} mmol/l/s")
    st.write(f"**FATmax Estimate:** {fatmax:.0f} W")
    st.write(f"**Efficiency (CP / VO2max):** {efficiency:.2f} W / L O₂")

    # === POWER DURATION CURVE ===
    st.subheader("Power Duration Curve")
    durations = [15, 60, 180, 300, 720]
    powers = [p_15s, p_1min, p_3min, p_5min, p_12min]
    x = np.linspace(10, 900, 200)
    y = w_prime * 1000 / x + cp

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

    # === SUBSTRATE USAGE BY ZONE ===
    st.subheader("Estimated Substrate Usage by Training Zone")
    zone_labels = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"]
    cp_ratios = [0.5, 0.65, 0.75, 0.90, 1.1, 1.35, 1.7]
    zone_powers = [round(cp * r) for r in cp_ratios]
    fat_values = []
    carb_values = []

    for p in zone_powers:
        fat, carb = fuel_split(p, cp)
        fat_values.append(fat)
        carb_values.append(carb)

    fig2, ax2 = plt.subplots()
    ax2.bar(zone_labels, fat_values, label="Fat (%)", color='green')
    ax2.bar(zone_labels, carb_values, bottom=fat_values, label="Carbohydrate (%)", color='orange')
    ax2.set_ylabel("Fuel Usage (%)")
    ax2.set_ylim(0, 120)
    ax2.set_title("Substrate Use by Training Zone (%CP)")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

    # === METABOLIC FINGERPRINT RADAR CHART ===
    st.subheader("Metabolic Fingerprint")

    radar_labels = ["VO2max", "CP", "W′", "VLamax", "FATmax", "Efficiency"]
    radar_values = [vo2max, cp, w_prime, vlamax, fatmax, efficiency]
    max_norms = [85, 400, 30, 1.0, 250, 6.0]
    radar_norm = [v / m for v, m in zip(radar_values, max_norms)]

    angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False).tolist()
    radar_norm += radar_norm[:1]
    angles += angles[:1]

    fig3, ax3 = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax3.plot(angles, radar_norm, color='blue', linewidth=2)
    ax3.fill(angles, radar_norm, color='blue', alpha=0.3)
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(radar_labels)
    ax3.set_yticks([])
    ax3.set_title("Metabolic Fingerprint (Radar Chart)", size=14)
    st.pyplot(fig3)
    
    # === FUEL USAGE CURVE (POWER VS. %FAT/CARB) ===
    st.subheader("Fuel Usage vs. Power Curve")

    power_range = np.linspace(0.4 * cp, 1.4 * cp, 100)
    fat_curve = []
    carb_curve = []

    for p in power_range:
        fat, carb = fuel_split(p, cp)
        fat_curve.append(fat)
        carb_curve.append(carb)

    fig4, ax4 = plt.subplots()
    ax4.plot(power_range, fat_curve, label="Fat %", color="green")
    ax4.plot(power_range, carb_curve, label="Carbohydrate %", color="orange")
    ax4.axvline(fatmax, color="blue", linestyle="--", label="FATmax")
    ax4.axvline(cp, color="gray", linestyle="--", label="CP")
    ax4.set_xlabel("Power (W)")
    ax4.set_ylabel("Fuel Usage (%)")
    ax4.set_title("Fuel Substrate Shift with Power")
    ax4.set_ylim(0, 110)
    ax4.legend()
    ax4.grid(True)
    st.pyplot(fig4)
