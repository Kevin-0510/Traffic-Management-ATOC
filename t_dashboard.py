import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="T Junction AI Traffic Dashboard",
    layout="wide"
)

# =====================================
# AUTO REFRESH
# =====================================

st_autorefresh(
    interval=2000,
    key="t_refresh"
)

# =====================================
# HEADER
# =====================================

st.title("🚦 T Junction AI Traffic Dashboard")

st.caption(
    "Priority Routing + Adaptive Signal Control + Congestion Monitoring"
)

try:

    df = pd.read_csv("../data/t_live_traffic.csv")

    if df.empty:
        st.warning("Waiting for simulation data...")
        st.stop()

    latest = df.iloc[-1]

    # =====================================
    # SYSTEM STATUS
    # =====================================

    st.subheader("🖥 System Status")

    a, b, c, d = st.columns(4)

    a.success("SUMO Online")
    b.success("Priority Agent Active")
    c.success("Signal Agent Active")
    d.success("Analytics Connected")

    st.divider()

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    peak_traffic = int(df["total_vehicles"].max())

    avg_total = round(
        df["total_vehicles"].mean(),
        2
    )

    st.subheader("📋 Executive Summary")

    st.info(
        f"""
Peak Traffic Observed: {peak_traffic}

Average Traffic Volume: {avg_total}

Current Priority Direction: {latest['priority_direction']}

Current Agent Action: {latest['agent_action']}

Current Congestion Level: {latest['congestion_level']}
"""
    )

    st.divider()

    # =====================================
    # LIVE METRICS
    # =====================================

    st.subheader("📊 Live Traffic Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Left Vehicles",
        int(latest["left_vehicles"])
    )

    c2.metric(
        "Right Vehicles",
        int(latest["right_vehicles"])
    )

    c3.metric(
        "Top Vehicles",
        int(latest["top_vehicles"])
    )

    c4.metric(
        "Total Vehicles",
        int(latest["total_vehicles"])
    )

    st.divider()

    # =====================================
    # FLOW METRICS
    # =====================================

    st.subheader("🚗 Traffic Flow Analysis")

    f1, f2 = st.columns(2)

    f1.metric(
        "Horizontal Flow",
        int(latest["horizontal_vehicles"])
    )

    f2.metric(
        "Vertical Flow",
        int(latest["vertical_vehicles"])
    )

    st.divider()

    # =====================================
    # AI DECISION PANEL
    # =====================================

    st.subheader("🤖 AI Decision")

    st.success(
        f"""
Priority Direction:
{latest['priority_direction']}

Signal Action:
{latest['agent_action']}
"""
    )

    st.divider()

    # =====================================
    # CONGESTION STATUS
    # =====================================

    st.subheader("🚨 Congestion Status")

    congestion = latest["congestion_level"]

    if congestion == "LOW":
        st.success("🟢 LOW")

    elif congestion == "MEDIUM":
        st.warning("🟡 MEDIUM")

    else:
        st.error("🔴 HIGH")

    st.divider()

    recent = df.tail(300)

    # =====================================
    # TRAFFIC TREND
    # =====================================

    st.subheader("📈 Traffic Volume Trend")

    fig1 = px.line(
        recent,
        x="time",
        y=[
            "left_vehicles",
            "right_vehicles",
            "top_vehicles"
        ],
        markers=True
    )

    fig1.update_layout(
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # FLOW TREND
    # =====================================

    st.subheader("📊 Flow Trend")

    fig2 = px.line(
        recent,
        x="time",
        y=[
            "horizontal_vehicles",
            "vertical_vehicles"
        ],
        markers=True
    )

    fig2.update_layout(
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # TABLES
    # =====================================

    left, right = st.columns(2)

    with left:

        st.subheader("🧠 Recent Decisions")

        st.dataframe(
            recent[
                [
                    "time",
                    "priority_direction",
                    "agent_action"
                ]
            ].tail(20),
            use_container_width=True
        )

    with right:

        st.subheader("📑 Analytics Data")

        st.dataframe(
            recent.tail(20),
            use_container_width=True
        )

except Exception as e:

    st.error(str(e))