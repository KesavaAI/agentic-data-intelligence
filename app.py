"""
Module: app.py
Role: Streamlit User Canvas & Visual Resilience Layer
Features: Dynamic Layout Adaptation, Schema Discovery, Sample Prompt Chips, Discrete Temporal Grouping Engine.
Visual Engines: Plotly Express Framework
Branding: Secure Text-to-Viz Analytics Engine (Zero-SQL AST Architecture)
"""

import re
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# --- PAGE CONFIGURATION & LAYOUT HARDENING ---
st.set_page_config(
    page_title="Secure Text-to-Viz Analytics Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for zero-clipping, responsive chart containers, and clean UI styling
st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.0rem !important;
            max-width: 95% !important;
        }
        .stPlotlyChart {
            margin-bottom: 0px !important;
        }
        .metric-badge {
            background-color: #1e293b;
            color: #38bdf8;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            display: inline-block;
            margin-right: 6px;
            margin-bottom: 6px;
            border: 1px solid #334155;
        }
    </style>
""", unsafe_allow_html=True)

# Session State Initializations
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "active_query" not in st.session_state:
    st.session_state.active_query = ""

# --- SIDEBAR CONTROL PANEL & DOMAIN GUIDE ---
with st.sidebar:
    st.markdown("### 🛠️ Analytics Control Center")
    if st.button("📝 New Notebook Canvas", use_container_width=True):
        st.session_state.active_query = ""
        st.rerun()
        
    st.markdown("---")
    
    # Dataset Domain Knowledge Guide
    st.markdown("### 🗂️ Dataset Domain Guide")
    try:
        from database_engine import ABBDataEngine
        engine = ABBDataEngine()
        
        st.markdown("**Business Lines:**")
        st.caption(", ".join(engine.df["Business_Line"].unique()))
        
        st.markdown("**Regions:**")
        st.caption(", ".join(engine.df["Region"].unique()))
        
        st.markdown("**Client Industries:**")
        st.caption(", ".join(engine.df["Client_Industry"].unique()))
    except Exception:
        st.caption("Unable to load domain guide.")
        
    st.markdown("---")
    st.markdown("<p style='font-size: 14px; font-weight: bold; color: #888888;'>Session Query Ledger</p>", unsafe_allow_html=True)
    
    if st.session_state.query_history:
        for idx, historical_prompt in enumerate(reversed(st.session_state.query_history)):
            display_text = historical_prompt if len(historical_prompt) <= 30 else f"{historical_prompt[:27]}..."
            if st.button(f"💬 {display_text}", key=f"hist_{idx}", use_container_width=True, help=historical_prompt):
                st.session_state.active_query = historical_prompt
                st.rerun()
    else:
        st.markdown("<p style='font-size: 12px; color: #555555; font-style: italic;'>No recent operations</p>", unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("Clear Cache & Logs", use_container_width=True):
        st.cache_data.clear()
        st.session_state.query_history = []
        st.session_state.active_query = ""
        st.rerun()

# --- MAIN WORKSPACE GRAPHICS & PROBLEM-SOLUTION BRANDING ---
st.title("🛡️ Secure Text-to-Viz Analytics Engine")

# Enhanced Architecture Status Badges
st.markdown("""
<div style="display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;">
    <span style="background-color: #1e293b; color: #38bdf8; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; border: 1px solid #0284c7;">🤖 Llama-3.3-70b (Groq)</span>
    <span style="background-color: #064e3b; color: #34d399; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; border: 1px solid #059669;">🔒 AST Secure Filter</span>
    <span style="background-color: #312e81; color: #a5b4fc; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; border: 1px solid #4338ca;">📊 Plotly Express</span>
</div>
""", unsafe_allow_html=True)

st.caption("Zero-SQL, Type-Safe AST Engine Translating Natural Language to Industrial Visualizations.")
st.markdown("---")

# 1. DATASET DISCOVERY EXPANDER
with st.expander("🔍 Discover Dataset Schema & Sample Data"):
    try:
        from database_engine import ABBDataEngine
        engine = ABBDataEngine()
        
        col_sch1, col_sch2 = st.columns([1, 2])
        with col_sch1:
            st.markdown("**Available Columns & Dtypes:**")
            schema_df = pd.DataFrame({
                "Column Name": engine.df.columns,
                "Data Type": [str(dtype) for dtype in engine.df.dtypes]
            })
            st.dataframe(schema_df, hide_index=True, use_container_width=True)
            
        with col_sch2:
            st.markdown("**Sample Data Records (First 3 Rows):**")
            st.dataframe(engine.df.head(3), hide_index=True, use_container_width=True)
    except Exception as exp_err:
        st.warning(f"Could not load dataset schema: {exp_err}")

# 2. SAMPLE PROMPT CHIPS
st.markdown("**💡 Quick Query Suggestions:**")
btn_c1, btn_c2, btn_c3 = st.columns(3)

with btn_c1:
    if st.button("📊 Revenue by Business Line (2024)", use_container_width=True):
        st.session_state.active_query = "Show me total Revenue_INR by Business_Line where Year is equal to 2024"
        st.rerun()

with btn_c2:
    if st.button("📈 Trajectory Across 2023, 2024, and 2025", use_container_width=True):
        st.session_state.active_query = "Show me a trend of sales across 2023, 2024, and 2025"
        st.rerun()

with btn_c3:
    if st.button("🌍 Regional Units Sold by Client Industry", use_container_width=True):
        st.session_state.active_query = "Show me Units_Sold by Region and Client_Industry as a bar chart"
        st.rerun()

# 3. PROMPT INPUT BOX
user_query = st.text_input(
    "Query input:", 
    value=st.session_state.active_query,
    placeholder="e.g., Show me the trajectory of business lines where the year is equal to 2024",
    label_visibility="collapsed"
)

# Strip literal quotes entered by users or suggestion chips
if user_query:
    user_query = user_query.strip("'\"")

if user_query:
    if not st.session_state.query_history or st.session_state.query_history[-1] != user_query:
        st.session_state.query_history.append(user_query)
        st.session_state.active_query = user_query
        st.rerun()

    with st.spinner("🤖 Executing Secure Relational Plan & Analytics Synthesis..."):
        from agent_graph import run_analytics_pipeline
        execution_state = run_analytics_pipeline(user_query)
        
        if execution_state.get("status") == "security_violation":
            st.error(f"🛡️ Security Alert Infrastructure: {execution_state.get('error_message', 'Invalid execution structure or unauthorized access pattern detected.')}")
        elif execution_state.get("status") == "success":
            filtered_df = execution_state.get("data")
            visual_plan = execution_state.get("visual_plan", {})
            commentary = execution_state.get("analyst_commentary", {})
            generated_sql = execution_state.get("generated_code", "")

            # --- ALWAYS-VISIBLE SQL & AST BACKEND LOG ---
            if generated_sql:
                with st.expander("💻 View Generated Query & Security Logs", expanded=False):
                    st.code(generated_sql, language="sql")
                    st.success("🔒 **AST Security Pass:** Read-Only AST evaluator verified zero SQL injection vectors.")

            if filtered_df is None or filtered_df.empty:
                st.warning("⚠️ Data filter constraints returned 0 matching records. Visualization suspended.")
            else:
                # EXECUTIVE BRIEFING LAYER WITH ENHANCED METRIC BADGES
                if commentary and isinstance(commentary, dict):
                    st.markdown("### 📑 Data Analyst Executive Briefing")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Executive Context Summary:** {commentary.get('executive_summary', 'N/A')}")
                        st.markdown(f"⚠️ **Anomalies Under Inspection:** *{commentary.get('anomalies_to_inspect', 'N/A')}*")
                    with col2:
                        st.markdown("**Key Metrics to Track:**")
                        metrics = commentary.get("key_metrics_to_watch", [])
                        if metrics:
                            badge_html = "".join([f'<span class="metric-badge">📌 {m}</span>' for m in metrics])
                            st.markdown(f'<div style="margin-top: 5px;">{badge_html}</div>', unsafe_allow_html=True)
                        else:
                            st.caption("No key metrics flagged.")
                    st.markdown("---")

                # VISUALIZATION CANVAS
                st.subheader("📊 Dynamic Analytical Visualization Canvas")
                
                chart_type = visual_plan.get("chart_type", "bar")
                x_axis = visual_plan.get("x")
                y_axis = visual_plan.get("y")
                color_dim = visual_plan.get("color")
                path_hierarchy = visual_plan.get("path", [])
                
                viz_df = filtered_df.copy()
                column_map = {c.lower(): c for c in viz_df.columns}
                if x_axis and x_axis.lower() in column_map: x_axis = column_map[x_axis.lower()]
                if y_axis and y_axis.lower() in column_map: y_axis = column_map[y_axis.lower()]
                if color_dim and color_dim.lower() in column_map: color_dim = column_map[color_dim.lower()]
                if path_hierarchy:
                    path_hierarchy = [column_map[p.lower()] for p in path_hierarchy if p.lower() in column_map]

                if not x_axis or x_axis not in viz_df.columns:
                    x_axis = "Business_Line"
                if not y_axis or y_axis not in viz_df.columns:
                    y_axis = "Revenue_INR"

                # Cast discrete temporal keys (Year) to string categories to prevent floating decimal axis ticks
                if x_axis and str(x_axis).lower() == "year":
                    viz_df['Year'] = viz_df['Year'].astype(str)
                if color_dim and str(color_dim).lower() == "year":
                    viz_df['Year'] = viz_df['Year'].astype(str)

                # Continuous Daily Timeline Pre-Aggregation
                if x_axis == "Date" and chart_type in ["line", "area"]:
                    if not pd.api.types.is_numeric_dtype(viz_df[y_axis]):
                        y_axis = "Revenue_INR"
                    timeline_grouping = ["Date"]
                    if color_dim and color_dim in viz_df.columns:
                        timeline_grouping.append(color_dim)
                    viz_df = viz_df.groupby(timeline_grouping, as_index=False)[y_axis].sum()
                    viz_df = viz_df.sort_values(by="Date")

                # Discrete Category & Year Aggregation Engine (Resolves spaghetti line charts)
                elif x_axis != "Date" and y_axis in viz_df.columns and pd.api.types.is_numeric_dtype(viz_df[y_axis]):
                    group_cols = list(dict.fromkeys(([x_axis] if x_axis else []) + ([color_dim] if color_dim else []) + path_hierarchy))
                    group_cols = [col for col in group_cols if col in viz_df.columns]
                    if group_cols:
                        viz_df = viz_df.groupby(group_cols, as_index=False)[y_axis].sum()

                # High-Density Parameter Tail Aggregation
                axis_to_check = x_axis if chart_type not in ["treemap", "sunburst"] else (path_hierarchy[-1] if path_hierarchy else x_axis)
                if axis_to_check and axis_to_check != "Date":
                    unique_count = viz_df[axis_to_check].nunique()
                    if unique_count > 15:
                        st.info(f"⚡ High Density Signal: Column '{axis_to_check}' has {unique_count} parameters. Aggregating tail into 'Other Data Streams'.")
                        top_categories = viz_df.groupby(axis_to_check)[y_axis if pd.api.types.is_numeric_dtype(viz_df[y_axis]) else 'Units_Sold'].sum().nlargest(15).index
                        viz_df[axis_to_check] = viz_df[axis_to_check].apply(lambda x: x if x in top_categories else "Other Data Streams")

                # Handle Non-Numeric / Transaction Counting Requests
                if str(y_axis).lower() in ['count', 'transactions', 'none', ''] and x_axis != "Date":
                    if chart_type not in ['histogram', 'box', 'violin', 'strip', 'density_heatmap']:
                        group_cols = list(dict.fromkeys(([x_axis] if x_axis else []) + ([color_dim] if color_dim else []) + path_hierarchy))
                        group_cols = [col for col in group_cols if col in viz_df.columns]
                        if group_cols:
                            viz_df = viz_df.groupby(group_cols, as_index=False).size()
                            viz_df = viz_df.rename(columns={'size': 'Transaction Count'})
                            y_axis = 'Transaction Count'

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
                        # Auto-barmode grouped for discrete categorical side-by-side comparisons
                        fig = px.bar(viz_df, x=x_axis, y=y_axis, color=color_dim, barmode="group", title=visual_plan.get("title"))
                        
                    # --- DYNAMIC ADAPTIVE LAYOUT ENGINE ---
                    num_categories = viz_df[x_axis].nunique() if (x_axis and x_axis in viz_df.columns) else 10
                    
                    dynamic_height = 520
                    if num_categories > 10 or chart_type in ["treemap", "sunburst", "density_heatmap"]:
                        dynamic_height = 620

                    bottom_margin = 130 if num_categories > 4 else 60

                    fig.update_layout(
                        autosize=True,
                        height=dynamic_height,
                        margin=dict(t=60, l=70, r=40, b=bottom_margin),
                        xaxis=dict(
                            autorange=True,
                            title_font=dict(size=13, color="#e0e0e0"),
                            tickfont=dict(size=11),
                            tickangle=-45 if num_categories > 4 else 0
                        ),
                        yaxis=dict(
                            autorange=True,
                            title_font=dict(size=13, color="#e0e0e0"),
                            tickfont=dict(size=11)
                        ),
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )

                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'responsive': True})
                        
                except Exception as canvas_err:
                    st.error(f"Visual Resilience Layer caught runtime rendering fault: {canvas_err}")
        else:
            st.error(f"Pipeline Interrupted: {execution_state.get('error_message', 'Critical Execution Intercept.')}")

# --- WELCOME ONBOARDING CARD (EMPTY INITIAL STATE) ---
else:
    st.info("💡 **Ready for Analysis:** Click any sample prompt chip above or enter a natural language query in the input box to trigger the AST security pipeline and generate analytics.")