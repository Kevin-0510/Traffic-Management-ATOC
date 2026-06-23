import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import sys
import os
from streamlit_autorefresh import st_autorefresh

# ==================================================
# PREMIUM CONCURRENT COMMAND CENTER CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="ATOC Autonomous AI Matrix",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-frequency refresh engine to animate vehicle vectors smoothly (1.5 second loop)
st_autorefresh(interval=1500, key="atoc_matrix_heartbeat")

# Custom UI Stylesheet for high-tech industrial aesthetics
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        html, body, [data-testid="stSidebar"] {
            font-family: 'JetBrains+Mono', monospace !important;
        }
        
        /* Premium Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #0E121A;
            border: 1px solid #232D3F;
            padding: 10px 14px;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        div[data-testid="stMetric"] label {
            color: #7E8B9B !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #00E676 !important;
            font-size: 1.3rem !important;
            font-weight: 700;
        }
        
        /* Unified Header Matrix */
        .node-matrix-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #FFFFFF;
            padding-bottom: 8px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        }
        
        /* AI Reasoning Box styling */
        .ai-insight-card {
            background-color: #0B1524;
            border-left: 4px solid #00B0FF;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR CONTROL MATRIX (CONCURRENT LAUNCHERS)
# ==================================================
st.sidebar.markdown("# 🕹️ ATOC CENTRAL CONTROL")
st.sidebar.caption("Orchestrate independent native SUMO environments concurrently.")
st.sidebar.divider()

def run_simulation_node(script_name, node_label):
    try:
        subprocess.Popen([sys.executable, script_name])
        st.sidebar.success(f"🚀 {node_label} Active")
    except Exception as e:
        st.sidebar.error(f"Launch Fail [{node_label}]: {str(e)}")

st.sidebar.markdown("### 🎛️ Simulation Deployment Matrix")

if st.sidebar.button("🔀 Run Cross Junction Agent", use_container_width=True):
    run_simulation_node("cross_complete_agent.py", "Cross Junction")

if st.sidebar.button("┫ Run T-Junction Agent", use_container_width=True):
    run_simulation_node("t_complete_agent.py", "T-Junction")

if st.sidebar.button("🌐 Run Double Junction Agent", use_container_width=True):
    run_simulation_node("double_complete_agent.py", "Double Junction")

st.sidebar.divider()
st.sidebar.markdown("### 📡 System Telemetry Flags")
st.sidebar.markdown("""
<div style='font-size:0.8rem; color:#8A99AD; line-height: 1.8;'>
• TELEMETRY FEED: <span style='color:#00E676;'>LIVE SYNC</span><br>
• AI REASONING CORE: <span style='color:#00B0FF;'>ACTIVE</span><br>
• VISUAL OVERLAY: <span style='color:#D500F9;'>VECTOR TWIN</span>
</div>
""", unsafe_allow_html=True)

# ==================================================
# MAIN INTERFACE STAGE HEADLINE
# ==================================================
st.markdown("# 🏙️ Agentic Traffic Operations Center (ATOC)")
st.caption("Synchronized Multi-Node Intelligence Wall — Concurrent Live Vector Twins & Generative Agent Explanations")
st.divider()

# Complete data asset routing structure mapping both telemetry files
nodes_config = {
    "Cross Junction": {
        "csv": "../data/cross_live_traffic.csv",
        "vehicles": "../data/cross_vehicle_positions.csv",
        "color": "#00E676",
        "type": "cross"
    },
    "T Junction": {
        "csv": "../data/t_live_traffic.csv",
        "vehicles": "../data/t_vehicle_positions.csv",
        "color": "#00B0FF",
        "type": "t"
    },
    "Double Junction": {
        "csv": "../data/live_traffic.csv",
        "vehicles": "../data/double_vehicle_positions.csv",
        "color": "#D500F9",
        "type": "double"
    }
}

# ==================================================
# CONCURRENT DATA PIPELINE RENDERING ENGINE
# ==================================================
for name, meta in nodes_config.items():
    
    st.markdown(f"""
        <div class="node-matrix-header" style="border-left: 4px solid {meta['color']}; padding-left: 10px;">
            <span>📍 SYSTEM NODE: {name.upper()} MANAGEMENT HUB</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not os.path.exists(meta["csv"]):
        st.info(f"⏳ Telemetry pipeline offline. Use the sidebar launcher matrix to initialize the active node.")
        st.write("")
        st.divider()
        continue
        
    try:
        df_metrics = pd.read_csv(meta["csv"])
        
        if os.path.exists(meta["vehicles"]):
            try:
                df_vehicles = pd.read_csv(meta["vehicles"])
            except:
                df_vehicles = pd.DataFrame(columns=["vehicle_id", "x", "y", "speed"])
        else:
            df_vehicles = pd.DataFrame(columns=["vehicle_id", "x", "y", "speed"])
            
        if df_metrics.empty:
            st.warning("📡 Synchronization warning: Waiting for incoming traffic telemetry frame arrays...")
            st.divider()
            continue
            
        latest_row = df_metrics.iloc[-1]
        recent_window = df_metrics.tail(60)
        
        # --- PHASE 1: DYNAMIC KPI PARSER ---
        action_val = latest_row.get("agent_action", "MONITORING")
        congestion_val = latest_row.get("congestion_level", "LOW")
        
        if meta["type"] == "cross":
            payload_vol = int(latest_row.get("north_vehicles", 0) + latest_row.get("west_vehicles", 0))
            lbl1, val1 = "North Vector Load", f"{latest_row.get('north_vehicles', 0)} Units"
            lbl2, val2 = "West Vector Load", f"{latest_row.get('west_vehicles', 0)} Units"
        elif meta["type"] == "t":
            payload_vol = int(latest_row.get("total_vehicles", 0))
            lbl1, val1 = "Priority Array Corridor", str(latest_row.get("priority_direction", "N/A"))
            lbl2, val2 = "Stem Buffer Load", f"{latest_row.get('top_vehicles', 0)} Units"
        else:
            payload_vol = int(latest_row.get("total_vehicles", 0))
            lbl1, val1 = "J0 Node Buffer", f"{latest_row.get('j0_queue', 0)} Units"
            lbl2, val2 = "J1 Node Buffer", f"{latest_row.get('j1_queue', 0)} Units"

        # --- PHASE 2: CONCURRENT KPI CARDS MATRIX ---
        kpi0, kpi1, kpi2, kpi3, kpi4 = st.columns([1.2, 1.2, 1.2, 1.5, 1.5])
        kpi0.metric("Total System Payload", f"{payload_vol} Units")
        kpi1.metric(lbl1, val1)
        kpi2.metric(lbl2, val2)
        kpi3.metric("Congestion Threshold", str(congestion_val).upper())
        kpi4.metric("AI Orchestration State", str(action_val))
        
        st.write("")
        
        # --- PHASE 3: LIVE DIGITAL TWIN VECTORS, ANALYSIS & AI INSIGHTS ---
        left_twin, center_trend, right_ai = st.columns([1.1, 1.1, 1.0])
        
        with left_twin:
            st.markdown("##### 🖥️ Live Vehicle Vector Twin Map")
            
            if meta["type"] == "cross":
                x_range, y_range = [-120, 120], [-120, 120]
            elif meta["type"] == "t":
                x_range, y_range = [-150, 150], [-150, 50]
            else:
                x_range, y_range = [-150, 150], [-100, 100]

            if not df_vehicles.empty and "x" in df_vehicles.columns and "y" in df_vehicles.columns:
                fig_twin = go.Figure()
                fig_twin.add_trace(go.Scatter(
                    x=df_vehicles["x"],
                    y=df_vehicles["y"],
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=df_vehicles["speed"],
                        colorscale="Electric",
                        cmin=0,
                        cmax=15,
                        showscale=True,
                        
                        # CORRECTED COLORBAR CONFIGURATION
                        colorbar=dict(
                            title=dict(
                                text="KM/H",
                                font=dict(size=9, color="#8A99AD")
                            ),
                            tickfont=dict(size=8, color="#8A99AD"),
                            thickness=12,
                            thicknessmode="pixels",
                            len=0.75,
                            lenmode="fraction",
                            x=1.05,
                            xanchor="left",
                            xpad=10,
                            ypad=15,
                            outlinecolor="#232D3F",
                            outlinewidth=1,
                            ticks="outside",
                            tickwidth=1,
                            ticklen=4,
                            tickcolor="#4E5D73",
                            exponentformat="none"
                        )
                    ),
                    text=df_vehicles["vehicle_id"],
                    hovertemplate="<b>ID:</b> %{text}<br><b>Speed:</b> %{marker.color:.1f} km/h<extra></extra>"
                ))
            else:
                fig_twin = go.Figure()
                fig_twin.add_annotation(text="Preparing Telemetry Sync...", showarrow=False, font=dict(color="#5A6A85", size=11))

            fig_twin.update_layout(
                height=240, plot_bgcolor="#0A0D14", paper_bgcolor="#0A0D14", margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(showgrid=True, gridcolor="#161B26", zeroline=False, visible=True, range=x_range, tickfont=dict(color="#4E5D73", size=8)),
                yaxis=dict(showgrid=True, gridcolor="#161B26", zeroline=False, visible=True, range=y_range, scaleanchor="x", scaleratio=1, tickfont=dict(color="#4E5D73", size=8))
            )
            st.plotly_chart(fig_twin, use_container_width=True, key=f"vector_twin_{name}")
            
        with center_trend:
            st.markdown("##### 📈 Volumetric Trends")
            
            if meta["type"] == "cross":
                y_targets = ["north_vehicles", "west_vehicles"]
            elif meta["type"] == "t":
                y_targets = [c for c in ["left_vehicles", "right_vehicles", "top_vehicles"] if c in recent_window.columns]
            else:
                y_targets = [c for c in ["j0_queue", "j1_queue"] if c in recent_window.columns]

            fig_trend = px.line(
                recent_window, x="time", y=y_targets,
                template="plotly_dark",
                color_discrete_sequence=[meta["color"], '#00B0FF', '#FF3D00']
            )
            fig_trend.update_layout(
                height=240, plot_bgcolor="#0A0D14", paper_bgcolor="#0A0D14", margin=dict(l=10, r=10, t=5, b=10),
                xaxis=dict(gridcolor="#161B26", tickfont=dict(size=8)),
                yaxis=dict(gridcolor="#161B26", tickfont=dict(size=8)),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=8))
            )
            st.plotly_chart(fig_trend, use_container_width=True, key=f"trend_vis_{name}")
            
        with right_ai:
            st.markdown("##### 🧠 AI Strategy & Predictive Reasoning")
            
            # Generate deterministic smart context insights depending on live parameters
            if meta["type"] == "cross":
                n_v = latest_row.get("north_vehicles", 0)
                w_v = latest_row.get("west_vehicles", 0)
                ai_desc = f"**ML Predictor:** North Congestion is at `{latest_row.get('north_congestion', 0):.2f}`, West is at `{latest_row.get('west_congestion', 0):.2f}`. "
                if "NORTH_GREEN" in str(action_val):
                    ai_desc += f"Priority Model locked onto North corridor due to higher wait score (`{latest_row.get('north_score', 0):.1f}`)."
                else:
                    ai_desc += f"Activating West green phase to clear a localized backlog of {w_v} units."
                    
            elif meta["type"] == "t":
                top_v = latest_row.get("top_vehicles", 0)
                ai_desc = f"**Priority Engine Matrix:** Dominant flow axis evaluated as `{latest_row.get('priority_direction', 'N/A')}`. "
                if top_v > 4:
                    ai_desc += f"Detected a significant stem queue backlog ({top_v} units). Signal agent overrides are scheduled to avoid starvation lock."
                else:
                    ai_desc += "Approaching pipelines are stable; adaptive loops are safely optimizing main road throughput variables."
                    
            else:
                j0_q = latest_row.get("j0_queue", 0)
                j1_q = latest_row.get("j1_queue", 0)
                if "PROPAGATE" in str(action_val):
                    ai_desc = f"🚨 **Network Alert:** J0 Queue bottleneck (`{j0_q}`) is threatening upstream grids. The **Propagation Agent** has overridden J1 to accelerate downstream dissipation."
                elif "EXTEND" in str(action_val):
                    ai_desc = f"⚠️ **Adaptive Extension:** J1 queue has crossed critical threshold limits (`{j1_q}`). Extending green phase bounds by 15s."
                else:
                    ai_desc = f"**Coordinated Network Status:** Balanced queues detected (`J0: {j0_q}`, `J1: {j1_q}`). Multi-Agent networks are operating in consensus state."
            
            st.markdown(f"""
                <div class="ai-insight-card">
                    <p style="margin: 0; font-size: 0.82rem; color: #E2E8F0; line-height: 1.5;">
                        ⚡ <b>CURRENT STATE LOG:</b><br>{ai_desc}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Predictive trend text indicators
            trend_status = "STABLE" if congestion_val == "LOW" else "ELEVATED SYSTEM STRESS"
            st.caption(f"🔮 **Predictive Outlook (30s window):** {trend_status}")
            
    except Exception as node_pipeline_error:
        st.error(f"Core process tracking engine exception parsed on node block: {str(node_pipeline_error)}")
        
    st.write("")
    st.divider()

# ==================================================
# UNIFIED INTERFACE ROOT FOOTER BANNER
# ==================================================
st.markdown("<p style='text-align: center; color: #4E5D73; font-size: 0.8rem;'>🤖 Multi-Node Intelligent Transport Twin Engine Cluster Core | Managed via TraCI Socket Pipeline Mappings</p>", unsafe_allow_html=True)