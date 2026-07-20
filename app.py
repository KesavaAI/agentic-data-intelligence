"""
Module: app.py
Role: Streamlit User Canvas & Visual Resilience Layer
Design Pattern: Client-Side Structural Isolation (Data Payload Optimization Gateway)
Visual Engines: Plotly Express Framework
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

# Boot dynamic runtime variable landscape settings
load_dotenv()

# Enforce clean corporate workspace geometry rules
st.set_page_config(
    page_title="ABB Enterprise Agentic Analytics Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize global UI session storage objects to maintain trace state history logs
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "active_query" not in st.session_state:
    st.session_state.active_query = ""

# --- SIDEBAR LIFE-CYCLE MANAGEMENT PANEL ---
with st.sidebar:
    st.markdown("### 🛠️ Analytics Control Center")
    if st.button("📝 New Notebook Canvas", use_container_width=True):
        st.session_state.active_query = ""
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='font-size: 14px; font-weight: bold; color: #888888;'>Session Query Ledger</p>", unsafe_allow_html=True)
    
    # Process and build history logs so users can easily toggle between analytical runs
    if st.session_state.query_history:
        for idx, historical_prompt in enumerate(reversed(st.session_state.query_history)):
            display_text = historical_prompt if len(historical_prompt) <= 30 else f"{historical_prompt[:27]}..."
            if st.button(f"💬 {display_text}", key=f"hist_{idx}", use_container_width=True, help=historical_prompt):
                st.session_state.active_query = historical_prompt
                st.rerun()
    else:
        st.markdown("<p style='font-size: 12px; color: #555555; font-style: italic;'>No recent analytical operations</p>", unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("Clear Cache & Logs", use_container_width=True):
        st.cache_data.clear()
        st.session_state.query_history = []
        st.session_state.active_query = ""
        st.rerun()

# --- MAIN INDUSTRIAL WORKSPACE GRAPHICS ---
st.title("🏭 ABB Enterprise Agentic Analytics Hub")
st.caption("Production-Hardened Mixed-Agent Zero-Code Analytics Workbench.")
st.markdown("---")

# Capture analytical text prompt input bounds
user_query = st.text_input(
    "Query input:", 
    value=st.session_state.active_query,
    placeholder="e.g., Show me the trajectory of business lines where the year is equal to 2024",
    label_visibility="collapsed"
)

# Manage operational sequence logs cleanly across context loop updates
if user_query:
    if not st.session_state.query_history or st.session_state.query_history[-1] != user_query:
        st.session_state.query_history.append(user_query)
        st.session_state.active_query = user_query
        st.rerun()

    # Launch execution pipeline wrapper tracing hooks
    with st.spinner("🤖 Executing Secure Relational Plan & Analytics Synthesis..."):
        from agent_graph import run_analytics_pipeline
        execution_state = run_analytics_pipeline(user_query)
        
        # 🛡️ Front-end Catch: Intercept structural alerts or payload missing events gracefully
        if execution_state.get("status") == "security_violation" or not execution_state.get("visual_plan"):
            st.error(f"🛡️ Security Alert Infrastructure: {execution_state.get('error_message', 'Invalid execution structure or unauthorized access pattern detected.')}")
        elif execution_state.get("status") == "success":
            filtered_df = execution_state.get("data")
            visual_plan = execution_state.get("visual_plan", {})
            commentary = execution_state.get("analyst_commentary", {})
            
            # Guard visual processing channels against complete empty-state sets
            if filtered_df is None or filtered_df.empty:
                st.warning("⚠️ Data filter constraints returned 0 matching records. Visualization and Analysis suspended.")
            else:
                # --- EXECUTIVE DATA ANALYST BRIEFING LAYER ---
                if commentary and isinstance(commentary, dict):
                    st.markdown("### 📑 Data Analyst Executive Briefing")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Executive Context Summary:** {commentary.get('executive_summary', 'N/A')}")
                        st.markdown(f"⚠️ **Anomalies / Skew Under Inspection:** *{commentary.get('anomalies_to_inspect', 'N/A')}*")
                    with col2:
                        st.markdown("**Key Metrics to Track:**")
                        for metric in commentary.get("key_metrics_to_watch", []):
                            st.markdown(f"- `{metric}`")
                    st.markdown("---")
                
                st.subheader("📊 Dynamic Analytical Visualization Canvas")
                
                # Setup visualization extraction parameters from the abstract model schema
                chart_type = visual_plan.get("chart_type", "bar")
                x_axis = visual_plan.get("x")
                y_axis = visual_plan.get("y")
                color_dim = visual_plan.get("color")
                path_hierarchy = visual_plan.get("path", [])
                
                viz_df = filtered_df.copy()
                
                # Enforce complete column name case-insensitivity mapping to optimize resilience
                column_map = {c.lower(): c for c in viz_df.columns}
                if x_axis and x_axis.lower() in column_map: x_axis = column_map[x_axis.lower()]
                if y_axis and y_axis.lower() in column_map: y_axis = column_map[y_axis.lower()]
                if color_dim and color_dim.lower() in column_map: color_dim = column_map[color_dim.lower()]
                if path_hierarchy:
                    path_hierarchy = [column_map[p.lower()] for p in path_hierarchy if p.lower() in column_map]

                # Logical Fallbacks: Protect the pipeline from schema omissions or empty value drops
                if not x_axis or x_axis not in viz_df.columns:
                    x_axis = "Business_Line"
                if not y_axis or y_axis not in viz_df.columns:
                    y_axis = "Revenue_INR"

                # --- TIME-SERIES AGGREGATOR ---
                if x_axis == "Date" and chart_type in ["line", "area"]:
                    if not pd.api.types.is_numeric_dtype(viz_df[y_axis]):
                        y_axis = "Revenue_INR"
                    timeline_grouping = ["Date"]
                    if color_dim and color_dim in viz_df.columns:
                        timeline_grouping.append(color_dim)
                    viz_df = viz_df.groupby(timeline_grouping, as_index=False)[y_axis].sum()
                    viz_df = viz_df.sort_values(by="Date")

                # --- 🛡️ DATA DENSITY GATEKEEPER COMPRESSION ENGINE ---
                axis_to_check = x_axis if chart_type not in ["treemap", "sunburst"] else (path_hierarchy[-1] if path_hierarchy else x_axis)
                
                if axis_to_check and axis_to_check != "Date":
                    unique_count = viz_df[axis_to_check].nunique()
                    # If high cardinality threatens browser performance, compress the tail indices dynamically
                    if unique_count > 15:
                        st.info(f"⚡ High Density Signal: Column '{axis_to_check}' possesses {unique_count} distinct parameters. Aggregating tail parameters into 'Other' group for frontend UI safety.")
                        
                        # Pinpoint top 15 highest-volume contributors by aggregate volume
                        top_categories = viz_df.groupby(axis_to_check)[y_axis if pd.api.types.is_numeric_dtype(viz_df[y_axis]) else 'Units_Sold'].sum().nlargest(15).index
                        
                        # Smoothly re-bucket remaining items under an 'Other' group
                        viz_df[axis_to_check] = viz_df[axis_to_check].apply(lambda x: x if x in top_categories else "Other Data Streams")

                # --- 📊 UNIFIED COUNT PRE-AGGREGATOR ---
                if str(y_axis).lower() in ['count', 'transactions', 'none', ''] and x_axis != "Date":
                    if chart_type not in ['histogram', 'box', 'violin', 'strip', 'density_heatmap']:
                        group_cols = list(dict.fromkeys(([x_axis] if x_axis else []) + ([color_dim] if color_dim else []) + path_hierarchy))
                        group_cols = [col for col in group_cols if col in viz_df.columns]
                        if group_cols:
                            viz_df = viz_df.groupby(group_cols, as_index=False).size()
                            viz_df = viz_df.rename(columns={'size': 'Transaction Count'})
                            y_axis = 'Transaction Count'
                
                elif chart_type in ['bar', 'funnel', 'treemap', 'sunburst'] and x_axis != "Date":
                    group_cols = list(dict.fromkeys([x_axis] + ([color_dim] if color_dim else []) + path_hierarchy))
                    group_cols = [col for col in group_cols if col in viz_df.columns]
                    if viz_df.duplicated(subset=[c for c in group_cols if c != y_axis]).any():
                        if group_cols and y_axis in viz_df.columns and pd.api.types.is_numeric_dtype(viz_df[y_axis]):
                            viz_df = viz_df.groupby(group_cols, as_index=False)[y_axis].sum()

                # --- GRAPH COMPILATION EXECUTION CORE ---
                try:
                    if chart_type == "line":
                        fig = px.line(viz_df, x=x_axis, y=y_axis, color=color_dim, title=visual_plan.get("title"))
                    elif chart_type == "pie":
                        fig = px.pie(viz_df, names=x_axis, values=y_axis, title=visual_plan.get("title"))
                    elif chart_type == "scatter":
                        fig = px.scatter(viz_df, x=x_axis, y=y_axis, color=color_dim, title=visual_plan.get("title"))
                    elif chart_type == "box":
                        fig = px.box(viz_df, x=x_axis, y=y_axis, color=color_dim, title=visual_plan.get("title"))
                    elif chart_type == "histogram":
                        fig = px.histogram(viz_df, x=x_axis, y=y_axis if y_axis != 'Transaction Count' else None, color=color_dim, title=visual_plan.get("title"))
                    elif chart_type in ["treemap", "sunburst"]:
                        final_path = path_hierarchy if path_hierarchy else ([color_dim, x_axis] if color_dim else [x_axis])
                        final_path = list(dict.fromkeys([p for p in final_path if p in viz_df.columns]))
                        fig = px.treemap(viz_df, path=final_path, values=y_axis if pd.api.types.is_numeric_dtype(viz_df[y_axis]) else 'Units_Sold', title=visual_plan.get("title")) if chart_type == "treemap" else px.sunburst(viz_df, path=final_path, values=y_axis if pd.api.types.is_numeric_dtype(viz_df[y_axis]) else 'Units_Sold', title=visual_plan.get("title"))
                    elif chart_type == "funnel":
                        viz_df = viz_df.sort_values(by=y_axis, ascending=False)
                        fig = px.funnel(viz_df, x=y_axis, y=x_axis, color=color_dim, title=visual_plan.get("title"))
                    elif chart_type == "area":
                        fig = px.area(viz_df, x=x_axis, y=y_axis, color=color_dim, title=visual_plan.get("title"))
                    elif chart_type == "violin":
                        fig = px.violin(viz_df, x=x_axis, y=y_axis, color=color_dim, box=True, points="all", title=visual_plan.get("title"))
                    elif chart_type == "strip":
                        fig = px.strip(viz_df, x=x_axis, y=y_axis, color=color_dim, title=visual_plan.get("title"))
                    elif chart_type == "density_heatmap":
                        fig = px.density_heatmap(viz_df, x=x_axis, y=y_axis, marginal_x="histogram", marginal_y="histogram", title=visual_plan.get("title"))
                    else:
                        fig = px.bar(viz_df, x=x_axis, y=y_axis, color=color_dim, title=visual_plan.get("title"))
                        
                    fig.update_layout(margin=dict(t=40, l=10, r=10, b=10))
                    # Mount the processed chart straight onto the working UI framework context
                    st.plotly_chart(fig, use_container_width=True)
                        
                except Exception as canvas_err:
                    st.error(f"Visual Resilience Layer caught runtime rendering fault: {canvas_err}")
        else:
            st.error(f"Pipeline Interrupted: {execution_state.get('error_message', 'Critical Execution Intercept.')}")