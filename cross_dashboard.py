import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Cross Junction AI Traffic Dashboard",
    layout="wide"
)

st_autorefresh(
    interval=2000,
    key="cross_refresh"
)

st.title("🚦 Cross Junction Traffic")

st.caption(
    "Multi-Agent Traffic Optimization using Congestion Prediction, Priority Routing and Signal Control"
)

# ==================================================
# LOAD TRAFFIC DATA
# ==================================================

try:

    df = pd.read_csv(
        "../data/cross_live_traffic.csv"
    )

    if df.empty:
        st.warning(
            "Waiting for simulation data..."
        )
        st.stop()

    latest = df.iloc[-1]

    # ==================================================
    # SYSTEM STATUS
    # ==================================================

    st.subheader("🖥 System Status")

    a, b, c, d = st.columns(4)

    a.success("SUMO Online")
    b.success("ML Model Active")
    c.success("Priority Agent Active")
    d.success("Signal Agent Active")

    st.divider()

    # ==================================================
    # EXECUTIVE SUMMARY
    # ==================================================

    avg_north = round(
        df["north_vehicles"].mean(),
        2
    )

    avg_west = round(
        df["west_vehicles"].mean(),
        2
    )

    peak_traffic = int(
        max(
            df["north_vehicles"].max(),
            df["west_vehicles"].max()
        )
    )

    current_congestion = round(
        latest["north_congestion"]
        +
        latest["west_congestion"],
        2
    )

    st.subheader("📋 Executive Summary")

    st.info(
        f"""
Peak Traffic Observed: {peak_traffic}

Average North Traffic: {avg_north}

Average West Traffic: {avg_west}

Combined Congestion Score: {current_congestion}

Current Agent Action: {latest['agent_action']}
"""
    )

    st.divider()

    # ==================================================
    # LIVE METRICS
    # ==================================================

    st.subheader("📊 Live Traffic Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "North Vehicles",
        int(latest["north_vehicles"])
    )

    c2.metric(
        "West Vehicles",
        int(latest["west_vehicles"])
    )

    c3.metric(
        "North Score",
        round(latest["north_score"], 2)
    )

    c4.metric(
        "West Score",
        round(latest["west_score"], 2)
    )

    st.divider()

    # ==================================================
    # AI INSIGHT
    # ==================================================

    st.subheader("🤖 AI Traffic Insight")

    action = latest["agent_action"]

    if action == "NORTH_GREEN":

        st.success(
            "North corridor prioritized due to higher congestion and emission score."
        )

    elif action == "WEST_GREEN":

        st.warning(
            "West corridor prioritized due to higher congestion and emission score."
        )

    else:

        st.info(
            "Traffic flow balanced."
        )

    st.divider()

    # ==================================================
    # LIVE DIGITAL TWIN
    # ==================================================

    st.subheader("🚦 Live Digital Twin")

    try:

        vehicles = pd.read_csv(
            "../data/cross_vehicle_positions.csv"
        )

        fig = go.Figure()

        # Horizontal Road

        fig.add_shape(
            type="rect",
            x0=-60,
            x1=60,
            y0=30,
            y1=36,
            fillcolor="gray",
            line=dict(width=0)
        )

        # Vertical Road

        fig.add_shape(
            type="rect",
            x0=-35,
            x1=-29,
            y0=-60,
            y1=60,
            fillcolor="gray",
            line=dict(width=0)
        )

        # Vehicles

        fig.add_trace(
            go.Scatter(
                x=vehicles["x"],
                y=vehicles["y"],
                mode="markers",
                marker=dict(
                    size=16,
                    color=vehicles["speed"],
                    colorscale="Turbo",
                    showscale=True,
                    colorbar=dict(
                        title="Speed"
                    )
                ),
                text=vehicles["vehicle_id"],
                hovertemplate=
                "Vehicle: %{text}<br>" +
                "X: %{x}<br>" +
                "Y: %{y}<br>"
            )
        )

        fig.update_layout(
            height=700,
            paper_bgcolor="black",
            plot_bgcolor="black",
            xaxis=dict(
                range=[-50, -15],
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                range=[20, 60],
                scaleanchor="x",
                showgrid=False,
                zeroline=False
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as twin_error:

        st.error(
            f"Digital Twin Error: {twin_error}"
        )

    st.divider()

    # ==================================================
    # CHARTS
    # ==================================================

    recent = df.tail(300)

    st.subheader("📈 Vehicle Volume Trend")

    fig1 = px.line(
        recent,
        x="time",
        y=[
            "north_vehicles",
            "west_vehicles"
        ]
    )

    fig1.update_layout(
        height=450
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.divider()

    st.subheader("🎯 Priority Score Trend")

    fig2 = px.line(
        recent,
        x="time",
        y=[
            "north_score",
            "west_score"
        ]
    )

    fig2.update_layout(
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    st.subheader("🔥 Congestion Trend")

    fig3 = px.line(
        recent,
        x="time",
        y=[
            "north_congestion",
            "west_congestion"
        ]
    )

    fig3.update_layout(
        height=450
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # TABLES
    # ==================================================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🧠 Recent Agent Decisions"
        )

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

        st.subheader(
            "📑 Analytics Data"
        )

        st.dataframe(
            recent.tail(20),
            use_container_width=True
        )

except Exception as e:

    st.error(str(e))