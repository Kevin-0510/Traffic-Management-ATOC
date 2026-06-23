import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Agentic Traffic Management Platform",
    layout="wide"
)

# =====================================
# AUTO REFRESH
# =====================================

st_autorefresh(
    interval=2000,
    key="live_refresh"
)

# =====================================
# HEADER
# =====================================

st.title("🚦 Agentic Traffic Management Platform")

st.caption(
    "Multi-Agent Traffic Control and Congestion Management System"
)

# =====================================
# LOAD DATA
# =====================================

try:

    df = pd.read_csv("../data/live_traffic.csv")

    if df.empty:
        st.warning("Waiting for simulation data...")
        st.stop()

    latest = df.iloc[-1]

    avg_queue = round(
        (
            df["j0_queue"].mean()
            +
            df["j1_queue"].mean()
        ) / 2,
        2
    )

    peak_traffic = int(
        df["total_vehicles"].max()
    )

    # =====================================
    # SYSTEM STATUS
    # =====================================

    st.subheader("🖥️ System Status")

    s1, s2, s3, s4 = st.columns(4)

    s1.success("SUMO Online")
    s2.success("Agent Active")
    s3.success("Dashboard Live")
    s4.success("Data Feed Connected")

    st.divider()

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    st.subheader("📋 Executive Summary")

    st.info(
        f"""
Peak Traffic Observed: {peak_traffic}

Average Queue Length: {avg_queue}

Current Congestion Level: {latest['congestion_level']}

Current Agent Action: {latest['agent_action']}
"""
    )

    # =====================================
    # KPI CARDS
    # =====================================

    st.subheader("📊 Live Traffic Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "J0 Queue",
        int(latest["j0_queue"])
    )

    col2.metric(
        "J1 Queue",
        int(latest["j1_queue"])
    )

    col3.metric(
        "Total Vehicles",
        int(latest["total_vehicles"])
    )

    col4.metric(
        "Peak Traffic",
        peak_traffic
    )

    st.divider()

    # =====================================
    # AI INSIGHT PANEL
    # =====================================

    st.subheader("🤖 AI Traffic Insight")

    action = latest["agent_action"]

    if action == "MONITORING":

        st.success(
            """
Traffic flow is normal.

Agent is continuously monitoring queue levels and waiting for congestion indicators.
"""
        )

    elif "EXTEND_J0" in action:

        st.warning(
            """
Congestion detected near Junction J0.

AI Recommendation:
• Extend green phase
• Reduce queue accumulation
• Improve corridor throughput
"""
        )

    elif "EXTEND_J1" in action:

        st.warning(
            """
Congestion detected near Junction J1.

AI Recommendation:
• Extend green phase
• Prevent spillback effects
• Improve vehicle clearance
"""
        )

    elif "PROPAGATE" in action:

        st.error(
            """
Congestion propagation detected.

AI Recommendation:
• Coordinate neighboring junctions
• Prepare downstream signal timing
• Prevent network-wide congestion
"""
        )

    else:

        st.info(action)

    st.divider()

    # =====================================
    # CONGESTION STATUS
    # =====================================

    st.subheader("🚨 Congestion Status")

    congestion = latest["congestion_level"]

    if congestion == "LOW":
        st.success("🟢 LOW CONGESTION")

    elif congestion == "MEDIUM":
        st.warning("🟡 MEDIUM CONGESTION")

    else:
        st.error("🔴 HIGH CONGESTION")

    st.divider()

    # =====================================
    # LIVE GRAPH
    # =====================================

    st.subheader("📈 Live Queue Evolution")

    recent = df.tail(300)

    fig = px.line(
        recent,
        x="time",
        y=["j0_queue", "j1_queue"],
        markers=True,
        title="Queue Length Trend"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Simulation Time",
        yaxis_title="Queue Length"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # TABLES
    # =====================================

    left, right = st.columns(2)

    with left:

        st.subheader("🧠 Recent Agent Decisions")

        st.dataframe(
            recent[
                [
                    "time",
                    "agent_action"
                ]
            ].tail(20),
            use_container_width=True
        )

    with right:

        st.subheader("📑 Traffic Analytics")

        st.dataframe(
            recent.tail(20),
            use_container_width=True
        )

    st.divider()

    # =====================================
    # FOOTER
    # =====================================

    st.caption(
        "Agentic Traffic Management Platform | Multi-Agent Traffic Control Prototype"
    )

except Exception as e:

    st.error(str(e))