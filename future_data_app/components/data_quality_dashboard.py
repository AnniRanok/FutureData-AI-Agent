#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_quality import (
    get_data_quality_metrics,
    get_anomalies,
    get_validation_results,
    get_data_quality_trends,
    generate_action_plan
)

def render_data_quality_dashboard(data):
    """
    Renders the data quality dashboard
    """
    st.header("Data Quality Dashboard")
    st.write("Identify data issues and ensure the accuracy of your financial reporting")
    
    # Data quality metrics overview
    quality_metrics = get_data_quality_metrics(data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Overall Data Quality",
            value=f"{quality_metrics['overall_score']}%",
            delta=f"{quality_metrics['overall_score_change']}%"
        )
    
    with col2:
        st.metric(
            label="Completeness",
            value=f"{quality_metrics['completeness']}%"
        )
    
    with col3:
        st.metric(
            label="Accuracy",
            value=f"{quality_metrics['accuracy']}%"
        )
    
    with col4:
        st.metric(
            label="Consistency",
            value=f"{quality_metrics['consistency']}%"
        )
    
    # Display dashboard image for visual appeal
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("data_quality.png", use_column_width=True)

    
    with col2:
        # Data quality score gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=quality_metrics['overall_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Data Quality Score"},
            delta={'reference': quality_metrics['previous_score']},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00C853"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 90], 'color': "yellow"},
                    {'range': [90, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabs for different data quality aspects
    tabs = st.tabs([
        "Anomalies & Validation", 
        "Data Quality by Department", 
        "Quality Trends", 
        "Action Plan"
    ])
    
    # Anomalies and validation tab
    with tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Data Anomalies")
            anomalies = get_anomalies(data)
            
            if anomalies.empty:
                st.success("No anomalies detected!")
            else:
                st.dataframe(
                    anomalies,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Example anomaly detail
                if not anomalies.empty:
                    with st.expander("Revenue Anomaly Example"):
                        st.markdown("""
                        **Detected Issue:** Order of magnitude error
                        
                        **Description:** Revenue amount €1,000 (should be €1,000,000)
                        
                        **AI Finding:** System detected a potential decimal error. This value is significantly lower than historical revenue for this product line.
                        
                        **Recommended Action:** Confirm decimal placement with data entry team.
                        """)
        
        with col2:
            st.subheader("Validation Results")
            validation_results = get_validation_results(data)
            
            # Create pie chart for validation status
            status_counts = validation_results["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            
            fig = px.pie(
                status_counts,
                values="Count",
                names="Status",
                title="Validation Status Distribution",
                color="Status",
                color_discrete_map={
                    "Passed": "#00C853",
                    "Warning": "orange",
                    "Failed": "red"
                }
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=300)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Validation table
            st.dataframe(
                validation_results,
                use_container_width=True,
                hide_index=True
            )
    
    # Data quality by department tab
    with tabs[1]:
        st.subheader("Data Quality by Department")
        
        # Generate department quality data
        dept_quality = pd.DataFrame({
            "Department": ["Accounting", "Sales", "Marketing", "Operations", "HR", "Supply Chain"],
            "Quality Score": [95, 87, 82, 91, 98, 85],
            "Issues": [2, 7, 9, 4, 1, 8]
        })
        
        # Create horizontal bar chart
        fig = px.bar(
            dept_quality,
            y="Department",
            x="Quality Score",
            orientation="h",
            color="Quality Score",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[70, 100],
            text="Quality Score",
            title="Data Quality Score by Department",
            labels={"Quality Score": "Quality Score (%)", "Department": "Department"}
        )
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bubble chart showing departments, quality score, and number of issues
        fig = px.scatter(
            dept_quality,
            x="Quality Score",
            y="Issues",
            size="Issues",
            color="Department",
            hover_name="Department",
            text="Department",
            title="Department Quality vs. Number of Issues",
            labels={"Quality Score": "Quality Score (%)", "Issues": "Number of Issues"}
        )
        
        fig.update_traces(textposition='top center')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Quality trends tab
    with tabs[2]:
        st.subheader("Data Quality Trends")
        
        quality_trends = get_data_quality_trends()
        
        # Line chart for overall quality trend
        fig = px.line(
            quality_trends,
            x="period",
            y="overall_score",
            title="Data Quality Score Trend",
            labels={"overall_score": "Quality Score (%)", "period": "Period"},
            markers=True
        )
        
        fig.update_traces(line=dict(color="#0A2463", width=3))
        fig.update_layout(height=350)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Quality metrics trends
        st.subheader("Quality Metrics Trends")
        
        # Melt the dataframe to create a long format for the metrics
        trend_metrics = quality_trends.melt(
            id_vars=["period"],
            value_vars=["completeness", "accuracy", "consistency"],
            var_name="Metric",
            value_name="Score"
        )
        
        # Create multi-line chart
        fig = px.line(
            trend_metrics,
            x="period",
            y="Score",
            color="Metric",
            title="Quality Metrics Trends",
            labels={"Score": "Score (%)", "period": "Period"},
            markers=True
        )
        
        fig.update_layout(height=350)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Action plan tab
    with tabs[3]:
        st.subheader("AI-Generated Action Plan")
        
        if st.button("Generate Action Plan"):
            with st.spinner("Analyzing data quality issues..."):
                action_plan = generate_action_plan(data)
                
                st.markdown("### Executive Summary")
                st.markdown(action_plan["executive_summary"])
                
                st.markdown("### Priority Issues")
                for i, issue in enumerate(action_plan["priority_issues"], 1):
                    st.markdown(f"**{i}. {issue['title']}**")
                    st.markdown(f"- **Severity**: {issue['severity']}")
                    st.markdown(f"- **Impact**: {issue['impact']}")
                    st.markdown(f"- **Resolution**: {issue['resolution']}")
                
                st.markdown("### Action Items")
                
                for i, action in enumerate(action_plan["action_items"], 1):
                    with st.expander(f"Action {i}: {action['title']}"):
                        st.markdown(f"**Owner**: {action['owner']}")
                        st.markdown(f"**Priority**: {action['priority']}")
                        st.markdown(f"**Due Date**: {action['due_date']}")
                        st.markdown(f"**Description**: {action['description']}")
                        st.markdown(f"**Expected Outcome**: {action['expected_outcome']}")
                
                st.markdown("### Impact on Reporting Timeline")
                st.markdown(action_plan["timeline_impact"])
                
                # Display Gantt chart for action items timeline
                df_gantt = pd.DataFrame([
                    {
                        "Task": action["title"],
                        "Start": action["start_date"],
                        "Finish": action["due_date"],
                        "Priority": action["priority"],
                        "Owner": action["owner"]
                    }
                    for action in action_plan["action_items"]
                ])
                
                fig = px.timeline(
                    df_gantt, 
                    x_start="Start", 
                    x_end="Finish", 
                    y="Task",
                    color="Priority",
                    color_discrete_map={
                        "High": "red",
                        "Medium": "orange",
                        "Low": "green"
                    },
                    hover_name="Task",
                    title="Action Items Timeline"
                )
                
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)

