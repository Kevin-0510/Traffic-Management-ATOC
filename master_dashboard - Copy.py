import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Agentic Traffic Management Platform",
    layout="wide"
)

st_autorefresh(
    interval=2000,
    key="master_refresh"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🚦 Scenario Control")

scenario = st.sidebar.selectbox(
    "Select Scenario",
    [
        "Double Junction",
        "Cross Junction",
        "T Junction"
    ]
)

# =====================================
# LOAD DATA
# =====================================

if scenario == "Double Junction":

    csv_file = "../data/live_traffic.csv"

elif scenario == "Cross Junction":

    csv_file = "../data/cross_live_traffic.csv"

else:

    csv_file = "../data/t_live_traffic.csv"

# =====================================
# READ CSV
# =====================================

try:

    df = pd.read_csv(csv_file)

    if df.empty:
        st.warning("Waiting for simulation data...")
        st.stop()

    latest = df.iloc[-1]

except Exception as e:

    st.error(e)
    st.stop()

# =====================================
# HEADER
# =====================================

st.title("🚦 Agentic Traffic Management Platform")

st.caption(
    "Multi-Agent Traffic Intelligence and Congestion Management System"
)

# =====================================
# STATUS BAR
# =====================================

s1, s2, s3, s4 = st.columns(4)

s1.success("SUMO Online")
s2.success("Agents Active")
s3.success("Dashboard Live")
s4.success("Telemetry Connected")

st.divider()

# =====================================
# MAIN LAYOUT
# =====================================

left, right = st.columns([1, 1])

# =====================================
# LEFT PANEL
# =====================================

with left:

    st.subheader("📋 Executive Summary")

    st.info(
        f"""
Current Scenario: {scenario}

Rows Collected: {len(df)}

Latest Timestamp: {latest.iloc[0]}
"""
    )

    st.subheader("🤖 Agent Decision")

    if "agent_action" in df.columns:

        st.success(
            str(latest["agent_action"])
        )

    st.subheader("🚨 System Status")

    if "congestion_level" in df.columns:

        congestion = latest["congestion_level"]

        if congestion == "LOW":
            st.success("🟢 LOW")

        elif congestion == "MEDIUM":
            st.warning("🟡 MEDIUM")

        else:
            st.error("🔴 HIGH")

# =====================================
# RIGHT PANEL
# =====================================

with right:

    st.subheader("🛰 Live Digital Twin")

    if scenario == "Double Junction":

        j0 = int(latest["j0_queue"])
        j1 = int(latest["j1_queue"])

        st.code(
f"""
        J0
         |
         |
=========+=========
         |
         |
        J1

J0 Queue : {j0}

J1 Queue : {j1}
"""
        )

    elif scenario == "Cross Junction":

        north = int(latest["north_vehicles"])
        west = int(latest["west_vehicles"])

        st.code(
f"""
          NORTH
            |
            |
WEST -------+------ EAST
            |
            |
          SOUTH

North Vehicles : {north}

West Vehicles  : {west}
"""
        )

    else:

        left_v = int(latest["left_vehicles"])
        right_v = int(latest["right_vehicles"])
        top_v = int(latest["top_vehicles"])

        st.code(
f"""
             TOP
              |
              |
LEFT ---------+--------- RIGHT

Left Vehicles  : {left_v}

Right Vehicles : {right_v}

Top Vehicles   : {top_v}
"""
        )

st.divider()

# =====================================
# RAW DATA
# =====================================

st.subheader("📊 Live Analytics")

st.dataframe(
    df.tail(20),
    use_container_width=True
)

st.divider()

st.caption(
    "Agentic Traffic Management Platform | Summit Demo Version"
)