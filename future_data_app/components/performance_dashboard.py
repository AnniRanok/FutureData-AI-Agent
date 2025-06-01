#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
from utils.financial_analysis import (
    calculate_yoy_performance,
    calculate_actual_vs_forecast,
    identify_top_performers,
    get_profitability_analysis
)
from utils.openai_helper import generate_performance_explanation

def render_performance_dashboard(data):
    """
    Renders the performance analysis dashboard
    """
    st.header("Performance Analysis Dashboard")
    st.write("Analyze your organization's financial performance with AI-powered insights")
    
    # Display dashboard image for visual appeal
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("financial.png",  use_column_width=True)
    
    with col2:
        # Key performance indicators
        kpi1, kpi2, kpi3 = st.columns(3)
        
        yoy_revenue_growth = data['metrics']['yoy_revenue_growth']
        kpi1.metric(
            label="Revenue YoY Growth",
            value=f"{yoy_revenue_growth:.1f}%",
            delta=f"{yoy_revenue_growth - 5.0:.1f}%" 
        )
        
        ebitda_margin = data['metrics']['ebitda_margin']
        kpi2.metric(
            label="EBITDA Margin",
            value=f"{ebitda_margin:.1f}%",
            delta=f"{ebitda_margin - data['metrics']['previous_ebitda_margin']:.1f}%"
        )
        
        cash_flow = data['metrics']['operating_cash_flow']
        kpi3.metric(
            label="Operating Cash Flow",
            value=f"€{cash_flow/1000000:.1f}M",
            delta=f"{(cash_flow - data['metrics']['previous_cash_flow'])/1000000:.1f}M"
        )
    
    # Analysis tabs
    tabs = st.tabs([
        "Year-over-Year", 
        "Actual vs. Forecast", 
        "Product Performance", 
        "AI Insights"
    ])
    
    # Year-over-Year analysis tab
    with tabs[0]:
        st.subheader("Year-over-Year Performance")
        
        # Calculate YoY performance
        yoy_data = calculate_yoy_performance(data)
        
        # YoY chart
        fig = px.bar(
            yoy_data,
            x="category",
            y="percent_change",
            color="percent_change",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[-15, 15],
            title="Year-over-Year Growth by Category",
            labels={"percent_change": "% Change", "category": "Category"}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # YoY data table
        st.dataframe(
            yoy_data[["category", "current_year", "previous_year", "change", "percent_change"]],
            hide_index=True,
            use_container_width=True
        )
    
    # Actual vs. Forecast tab
    with tabs[1]:
        st.subheader("Actual vs. Forecast Analysis")
        
        try:
            # Actual vs. Forecast chart
            actual_vs_forecast = calculate_actual_vs_forecast(data)
            
            # Create figure
            fig = go.Figure()
            
            # Add bars for actual and forecast
            fig.add_trace(
                go.Bar(
                    x=actual_vs_forecast["category"],
                    y=actual_vs_forecast["actual"],
                    name="Actual",
                    marker_color="#00C853"
                )
            )
            
            fig.add_trace(
                go.Bar(
                    x=actual_vs_forecast["category"],
                    y=actual_vs_forecast["forecast"],
                    name="Forecast",
                    marker_color="#0A2463"
                )
            )
            
            # Add variance line
            fig.add_trace(
                go.Scatter(
                    x=actual_vs_forecast["category"],
                    y=actual_vs_forecast["variance_pct"],
                    name="Variance %",
                    yaxis="y2",
                    line=dict(color="red", width=2)
                )
            )
            
            # Update layout for dual y-axis
            fig.update_layout(
                title="Actual vs. Forecast by Category",
                yaxis=dict(title="Amount (€)"),
                yaxis2=dict(
                    title="Variance %",
                    overlaying="y",
                    side="right"
                ),
                height=400,
                barmode="group",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Explanation of significant variances
            st.subheader("Significant Variances")
            variance_table = actual_vs_forecast[actual_vs_forecast["variance_pct"].abs() > 5]
            
            if not variance_table.empty:
                st.dataframe(
                    variance_table[["category", "actual", "forecast", "variance", "variance_pct", "explanation"]],
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No significant variances found (threshold: ±5%)")
        except Exception as e:
            st.error(f"Unable to display Actual vs. Forecast analysis. Please contact your administrator.")
            st.info("Using static sample data for demonstration purposes.")
            
            # Create sample data for visualization
            sample_categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
            sample_actuals = [2500000, 1800000, 1500000, 1200000, 900000]
            sample_forecasts = [2300000, 1900000, 1500000, 1300000, 800000]
            
            # Create figure with sample data
            fig = go.Figure()
            
            fig.add_trace(go.Bar(x=sample_categories, y=sample_actuals, name="Actual", marker_color="#00C853"))
            fig.add_trace(go.Bar(x=sample_categories, y=sample_forecasts, name="Forecast", marker_color="#0A2463"))
            
            # Calculate variance percentages
            variance_pcts = [(a-f)/f*100 for a, f in zip(sample_actuals, sample_forecasts)]
            fig.add_trace(go.Scatter(x=sample_categories, y=variance_pcts, name="Variance %", 
                                    yaxis="y2", line=dict(color="red", width=2)))
            
            # Update layout
            fig.update_layout(
                title="Actual vs. Forecast by Category (Sample Data)",
                yaxis=dict(title="Amount (€)"),
                yaxis2=dict(title="Variance %", overlaying="y", side="right"),
                height=400,
                barmode="group",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Sample variance table
            st.subheader("Significant Variances")
            st.dataframe({
                "Category": ["Product A", "Product E"],
                "Actual": ["€2.5M", "€0.9M"],
                "Forecast": ["€2.3M", "€0.8M"],
                "Variance": ["€0.2M", "€0.1M"],
                "Variance %": ["8.7%", "12.5%"],
                "Explanation": [
                    "Higher than expected market demand and successful promotional campaign",
                    "New service offering exceeded expectations with strong client adoption"
                ]
            })
    
    # Product Performance tab
    with tabs[2]:
        st.subheader("Product Performance Analysis")
        
        try:
            # Top/Bottom Performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Performing Products")
                top_products = identify_top_performers(data, top=5)
                
                fig = px.bar(
                    top_products,
                    x="name",  # Using the correct column name
                    y="profit_margin",
                    color="profit_margin",
                    color_continuous_scale=["yellow", "green"],
                    range_color=[0, max(top_products["profit_margin"])],
                    title="Top 5 Products by Profit Margin",
                    labels={"profit_margin": "Profit Margin (%)", "name": "Product"}
                )
                
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Bottom Performing Products")
                bottom_products = identify_top_performers(data, top=5, reverse=True)
                
                fig = px.bar(
                    bottom_products,
                    x="name",  # Using the correct column name
                    y="profit_margin",
                    color="profit_margin",
                    color_continuous_scale=["red", "yellow"],
                    range_color=[min(bottom_products["profit_margin"]), 15],
                    title="Bottom 5 Products by Profit Margin",
                    labels={"profit_margin": "Profit Margin (%)", "name": "Product"}
                )
                
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            # Profitability heatmap
            st.subheader("Product Profitability Heatmap")
            profitability_data = get_profitability_analysis(data)
            
            fig = px.imshow(
                profitability_data["heatmap_data"],
                labels=dict(x="Region", y="Product Category", color="Profit Margin (%)"),
                x=profitability_data["regions"],
                y=profitability_data["categories"],
                color_continuous_scale="RdYlGn",
                aspect="auto",
                title="Product Profitability by Region"
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Product drill-down selector
            if st.checkbox("Drill down to specific product"):
                selected_product = st.selectbox(
                    "Select a product for detailed analysis:",
                    options=data["products"]["name"].tolist()
                )
                
                # Find the selected product
                product_data = data["products"][data["products"]["name"] == selected_product].iloc[0]
                
                st.subheader(f"Detailed Analysis: {selected_product}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Revenue", f"€{product_data['revenue']/1000000:.2f}M")
                    st.metric("Profit Margin", f"{product_data['profit_margin']:.1f}%")
                    st.metric("YoY Growth", f"{product_data['yoy_growth']:.1f}%")
                
                with col2:
                    st.metric("Cost", f"€{product_data['cost']/1000000:.2f}M")
                    st.metric("Market Share", f"{product_data['market_share']:.1f}%")
                    st.metric("Customer Satisfaction", f"{product_data['customer_satisfaction']:.1f}/5.0")
                
                if product_data['profit_margin'] < 10:
                    st.warning(f"""
                    **Margin Drop Alert**: {selected_product} margin is below target threshold.
                    - **Cause**: Raw material costs ↑ {product_data.get('raw_material_increase', 22)}%
                    - **Action**: Contract renegotiation recommended
                    """)
        except Exception as e:
            st.error(f"Unable to display Product Performance analysis. Please contact your administrator.")
            st.info("Using static sample data for demonstration purposes.")
            
            # Create sample data for visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Performing Products")
                # Sample top performers chart
                top_products = pd.DataFrame({
                    "Product": ["Enterprise Server X1", "Cloud Storage Premium", "Security Suite Pro", 
                                "Database Enterprise", "Analytics Premium"],
                    "Profit Margin": [28.5, 26.3, 24.8, 23.5, 22.0]
                })
                
                fig = px.bar(
                    top_products,
                    x="Product",
                    y="Profit Margin",
                    color="Profit Margin",
                    color_continuous_scale=["yellow", "green"],
                    title="Top 5 Products by Profit Margin",
                    labels={"Profit Margin": "Profit Margin (%)"}
                )
                
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Bottom Performing Products")
                # Sample bottom performers chart
                bottom_products = pd.DataFrame({
                    "Product": ["Mobile Solution A", "Support Basic", "Networking Basic", 
                               "Integration Suite", "Development Tools"],
                    "Profit Margin": [8.5, 9.2, 10.5, 11.2, 12.0]
                })
                
                fig = px.bar(
                    bottom_products,
                    x="Product",
                    y="Profit Margin",
                    color="Profit Margin",
                    color_continuous_scale=["red", "yellow"],
                    title="Bottom 5 Products by Profit Margin",
                    labels={"Profit Margin": "Profit Margin (%)"}
                )
                
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            # Sample heatmap
            st.subheader("Product Profitability Heatmap")
            
            # Create sample heatmap data
            categories = ["Hardware", "Software", "Services", "Cloud", "Consulting"]
            regions = ["Europe", "North America", "Asia Pacific", "Latin America", "Middle East"]
            
            # Generate a sample heatmap matrix
            np.random.seed(42)
            heatmap_data = np.random.normal(loc=15, scale=5, size=(len(categories), len(regions)))
            
            # Make some values stand out
            heatmap_data[0, 0] = 22  # Hardware in Europe
            heatmap_data[2, 1] = 25  # Services in North America
            heatmap_data[3, 2] = 26  # Cloud in Asia Pacific
            heatmap_data[1, 3] = 8   # Software in Latin America
            heatmap_data[4, 4] = 7   # Consulting in Middle East
            
            fig = px.imshow(
                heatmap_data,
                labels=dict(x="Region", y="Product Category", color="Profit Margin (%)"),
                x=regions,
                y=categories,
                color_continuous_scale="RdYlGn",
                aspect="auto",
                title="Product Profitability by Region"
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    # AI Insights tab
    with tabs[3]:
        st.subheader("AI-Generated Performance Insights")

        # Check if API key is available        
        if st.button("Generate AI Analysis"):
            if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"] or os.environ["OPENAI_API_KEY"] == "your-api-key-here":
                st.warning("OpenAI API key not configured. Please add your API key to use AI-powered analysis.")
                
                # Show sample analysis for demonstration
                st.info("Showing sample analysis for demonstration purposes")
                
                # Sample analysis
                sample_analysis = {
                    "executive_summary": "Financial performance shows mixed results with revenue growth of 7.2% but margin pressure from rising input costs. Key products are outperforming in target markets, though economic headwinds are impacting overall profitability.",
                    "key_findings": [
                        "Year-over-year revenue growth of 7.2% exceeded market average",
                        "EBITDA margin declined by 1.3 percentage points due to rising input costs",
                        "Top performing product line delivered 15% margin improvement",
                        "Geographical expansion increased revenue but with temporary margin dilution",
                        "Operating efficiency initiatives delivered cost savings of €3.2M"
                    ],
                    "recommendations": [
                        "Accelerate pricing strategy adjustments to offset margin pressure",
                        "Focus investment on top-performing product lines to capitalize on momentum",
                        "Implement targeted cost reduction in underperforming segments",
                        "Develop strategic response to projected raw material inflation"
                    ],
                    "contributing_factors": pd.DataFrame({
                        "factor": ["Product Mix Optimization", "Market Expansion", "Cost Inflation", 
                                 "Operational Efficiency", "Currency Effects"],
                        "impact": [35, 25, 20, 15, 5]
                    }),
                    "opportunities": "Significant opportunity exists to leverage data analytics for dynamic pricing and inventory optimization. Customer segmentation analysis indicates potential for 8-10% margin improvement in enterprise segment through tailored solutions. Supply chain resilience investments could mitigate 60% of current volatility impact."
                }
                
                st.markdown("### Executive Summary")
                st.markdown(sample_analysis["executive_summary"])
                
                st.markdown("### Key Findings")
                for finding in sample_analysis["key_findings"]:
                    st.markdown(f"- {finding}")
                
                st.markdown("### Recommendations")
                for recommendation in sample_analysis["recommendations"]:
                    st.markdown(f"- {recommendation}")
                
                # Graph of contributing factors
                st.subheader("Contributing Factors to Performance")
                
                fig = px.pie(
                    sample_analysis["contributing_factors"],
                    values="impact",
                    names="factor",
                    title="Factors Impacting Financial Performance",
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Examples of how to improve further
                st.subheader("Opportunities for Improvement")
                st.markdown(sample_analysis["opportunities"])
                
            else:
                with st.spinner("Analyzing financial performance..."):
                    # Generate performance explanation using OpenAI
                    analysis = generate_performance_explanation(data)
                    
                    st.markdown("### Executive Summary")
                    st.markdown(analysis["executive_summary"])
                    
                    st.markdown("### Key Findings")
                    for finding in analysis["key_findings"]:
                        st.markdown(f"- {finding}")
                    
                    st.markdown("### Recommendations")
                    for recommendation in analysis["recommendations"]:
                        st.markdown(f"- {recommendation}")
                    
                    # Graph of contributing factors
                    st.subheader("Contributing Factors to Performance")
                    
                    fig = px.pie(
                        analysis["contributing_factors"],
                        values="impact",
                        names="factor",
                        title="Factors Impacting Financial Performance",
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(height=400)
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Examples of how to improve further
                    st.subheader("Opportunities for Improvement")
                    st.markdown(analysis["opportunities"])

