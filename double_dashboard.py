import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
st.set_page_config(
    page_title="Double Junction AI Dashboard",
    layout="wide"
)
st_autorefresh(
    interval=2000,
    key="double_refresh"
)
st.title("🚦 Double Junction Traffic Dashboard")
st.caption(
    "Multi-Agent Traffic Optimization with Congestion Monitoring, Signal Control and Propagation Agents"
)
try:
    df = pd.read_csv("../data/live_traffic.csv")
    if df.empty:
        st.warning("Waiting for simulation data...")
        st.stop()
    latest = df.iloc[-1]
    st.subheader("🖥 System Status")
    a,b,c,d = st.columns(4)
    a.success("SUMO Online")
    b.success("J0 Agent Active")
    c.success("J1 Agent Active")
    d.success("Propagation Agent Active")
    st.divider()
    peak_traffic = int(df["total_vehicles"].max())
    avg_traffic = round(
        df["total_vehicles"].mean(),
        2
    )
    st.subheader("📋 Executive Summary")
    st.info(
        f"""
Peak Traffic Observed: {peak_traffic}
Average Traffic Volume: {avg_traffic}
Current Congestion Level: {latest['congestion_level']}
Current Agent Action: {latest['agent_action']}
"""
    )
    st.divider()
    st.subheader("📊 Live Metrics")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric(
        "J0 Queue",
        int(latest["j0_queue"])
    )
    c2.metric(
        "J1 Queue",
        int(latest["j1_queue"])
    )
    c3.metric(
        "Total Vehicles",
        int(latest["total_vehicles"])
    )
    c4.metric(
        "Congestion",
        latest["congestion_level"]
    )
    st.divider()
    # =====================================
    # DIGITAL TWIN
    # =====================================
    st.subheader("🚗 Live Digital Twin")
    try:
        vehicles = pd.read_csv(
            "../data/double_vehicle_positions.csv"
        )
        fig = go.Figure()
        # Main horizontal road
        fig.add_shape(
            type="rect",
            x0=-80,
            x1=40,
            y0=-5,
            y1=5,
            fillcolor="lightgray",
            line=dict(color="lightgray")
        )
        # Junction 1
        fig.add_shape(
            type="rect",
            x0=-35,
            x1=-25,
            y0=-40,
            y1=40,
            fillcolor="lightgray",
            line=dict(color="lightgray")
        )
        # Junction 2
        fig.add_shape(
            type="rect",
            x0=15,
            x1=25,
            y0=-40,
            y1=40,
            fillcolor="lightgray",
            line=dict(color="lightgray")
        )
        fig.add_trace(
            go.Scatter(
                x=vehicles["x"],
                y=vehicles["y"],
                mode="markers",
                marker=dict(
                    size=14,
                    color=vehicles["speed"],
                    colorscale="Turbo",
                    showscale=True,
                    colorbar=dict(
                        title="Speed"
                    )
                ),
                text=vehicles["vehicle_id"]
            )
        )
        fig.update_layout(
            height=700,
            showlegend=False,
            plot_bgcolor="black",
            paper_bgcolor="black",
            xaxis=dict(
                range=[-90, 50],
                visible=False
            ),
            yaxis=dict(
                range=[-50, 50],
                visible=False,
                scaleanchor="x"
            )
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    except Exception:
        st.warning(
            "Vehicle positions not available yet."
        )
    st.divider()
    st.subheader("🤖 AI Decision")
    action = latest["agent_action"]
    if action == "EXTEND_J0_GREEN":
        st.success(
            "J0 congestion detected. Green phase extended."
        )
    elif action == "EXTEND_J1_GREEN":
        st.warning(
            "J1 congestion detected. Green phase extended."
        )
    elif action == "PROPAGATE_J0_TO_J1":
        st.error(
            "Congestion propagation detected. J1 optimized."
        )
    else:
        st.info(
            "Traffic conditions normal."
        )
    st.divider()
    recent = df.tail(300)
    st.subheader("📈 Queue Trend")
    fig1 = px.line(
        recent,
        x="time",
        y=[
            "j0_queue",
            "j1_queue"
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
    st.subheader("🚗 Total Traffic Trend")
    fig2 = px.line(
        recent,
        x="time",
        y="total_vehicles",
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
    left,right = st.columns(2)
    with left:
        st.subheader("🧠 Recent Decisions")
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
        st.subheader("📑 Analytics Data")
        st.dataframe(
            recent.tail(20),
            use_container_width=True
        )
except Exception as e:
    st.error(str(e))