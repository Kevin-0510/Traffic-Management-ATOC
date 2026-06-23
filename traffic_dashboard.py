import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="Agentic Traffic Management",
    layout="wide"
)

# ----------------------------------
# LOAD DATA
# ----------------------------------

df = pd.read_csv("../data/traffic_analytics.csv")

latest = df.iloc[-1]

avg_queue = round(
    (df["j0_queue"].mean() + df["j1_queue"].mean()) / 2,
    2
)

peak_traffic = int(df["total_vehicles"].max())

# ----------------------------------
# HEADER
# ----------------------------------

st.title("🚦 Agentic Traffic Management Dashboard")

st.info(
    f"""
    Total Records: {len(df)}

    Peak Traffic Observed: {peak_traffic}

    Current Congestion Status: {latest['congestion_level']}

    Last Agent Action: {latest['agent_action']}
    """
)

# ----------------------------------
# KPI SECTION
# ----------------------------------

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
    "Peak Traffic",
    peak_traffic
)

col4.metric(
    "Average Queue",
    avg_queue
)

# ----------------------------------
# AI INSIGHT
# ----------------------------------

st.subheader("🤖 AI Traffic Insight")

if latest["congestion_level"] == "HIGH":

    st.error(
        "High congestion detected. Adaptive signal extension recommended."
    )

elif latest["congestion_level"] == "MEDIUM":

    st.warning(
        "Moderate congestion detected. Traffic agents are monitoring the corridor."
    )

else:

    st.success(
        "Traffic flow is normal. No intervention required."
    )

# ----------------------------------
# TRAFFIC TREND GRAPH
# ----------------------------------

st.subheader("📈 Traffic Queue Trends")

fig = px.line(
    df,
    x="time",
    y=["j0_queue", "j1_queue"],
    labels={
        "value": "Queue Length",
        "time": "Simulation Time"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# CONGESTION DISTRIBUTION
# ----------------------------------

st.subheader("🚗 Congestion Distribution")

congestion_counts = (
    df["congestion_level"]
    .value_counts()
    .reset_index()
)

congestion_counts.columns = [
    "Congestion",
    "Count"
]

fig2 = px.bar(
    congestion_counts,
    x="Congestion",
    y="Count"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------------------------------
# RECENT DECISIONS
# ----------------------------------

st.subheader("🧠 Agent Decision Log")

st.dataframe(
    df[
        [
            "time",
            "agent_action"
        ]
    ].tail(20),
    use_container_width=True
)

# ----------------------------------
# RAW DATA
# ----------------------------------

st.subheader("📊 Analytics Dataset")

st.dataframe(
    df.tail(50),
    use_container_width=True
)