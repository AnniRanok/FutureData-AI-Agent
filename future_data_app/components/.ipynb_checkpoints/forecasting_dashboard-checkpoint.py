#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.forecasting import (
    generate_forecast_data,
    calculate_impact_scenarios,
    get_ai_recommendations
)

def render_forecasting_dashboard(data):
    """
    Renders the forecasting and recommendations dashboard
    """
    st.header("Forecasting & Recommendations Dashboard")
    st.write("Generate forecasts, run simulations, and receive AI-powered recommendations")
    
    # Display dashboard image for visual appeal
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(
            "https://pixabay.com/get/g96aa0225952aebeb56c0d5f815183a5993501cd59027928eb86382ff8fff1679306c9b36c460bb567d4631e621b97834fc5da4ed2330ff14110766632039e402_1280.jpg",
            caption="Financial Forecasting",
            width=300
        )
    
    with col2:
        # Key forecast metrics
        kpi1, kpi2, kpi3 = st.columns(3)
        
        forecasted_revenue_growth = data['forecast']['revenue_growth']
        kpi1.metric(
            label="Forecasted Revenue Growth",
            value=f"{forecasted_revenue_growth:.1f}%",
            delta=f"{forecasted_revenue_growth - data['metrics']['yoy_revenue_growth']:.1f}%" 
        )
        
        forecasted_ebitda = data['forecast']['ebitda_margin']
        kpi2.metric(
            label="Forecasted EBITDA",
            value=f"{forecasted_ebitda:.1f}%",
            delta=f"{forecasted_ebitda - data['metrics']['ebitda_margin']:.1f}%"
        )
        
        roi = data['forecast']['roi']
        kpi3.metric(
            label="Expected ROI",
            value=f"{roi:.1f}%"
        )
    
    # Tabs for different forecasting aspects
    tabs = st.tabs([
        "Forecast Overview", 
        "Simulation", 
        "Scenario Planning", 
        "AI Recommendations"
    ])
    
    # Forecast overview tab
    with tabs[0]:
        st.subheader("Financial Forecast Overview")
        
        # Time period selection for forecast
        forecast_period = st.selectbox(
            "Forecast Period",
            ["12 Months", "24 Months", "36 Months", "5 Years"]
        )
        
        # Generate forecast data
        forecast_data = generate_forecast_data(data, forecast_period)
        
        # Line chart for revenue forecast
        fig = go.Figure()
        
        # Add historical revenue line
        fig.add_trace(
            go.Scatter(
                x=forecast_data["historical"]["period"],
                y=forecast_data["historical"]["revenue"],
                name="Historical Revenue",
                line=dict(color="#0A2463", width=3)
            )
        )
        
        # Add forecasted revenue line
        fig.add_trace(
            go.Scatter(
                x=forecast_data["forecast"]["period"],
                y=forecast_data["forecast"]["revenue"],
                name="Forecasted Revenue",
                line=dict(color="#00C853", width=3, dash="dash")
            )
        )
        
        # Add upper and lower bounds to show confidence interval
        fig.add_trace(
            go.Scatter(
                x=forecast_data["forecast"]["period"],
                y=forecast_data["forecast"]["revenue_upper"],
                name="Upper Bound (95% CI)",
                line=dict(color="rgba(0, 200, 83, 0.2)", width=0),
                showlegend=False
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=forecast_data["forecast"]["period"],
                y=forecast_data["forecast"]["revenue_lower"],
                name="Lower Bound (95% CI)",
                line=dict(color="rgba(0, 200, 83, 0.2)", width=0),
                fill="tonexty",
                fillcolor="rgba(0, 200, 83, 0.2)",
                showlegend=False
            )
        )
        
        fig.update_layout(
            title="Revenue Forecast with Confidence Interval",
            xaxis_title="Period",
            yaxis_title="Revenue (€ Millions)",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display forecast metrics table
        st.subheader("Forecast Metrics")
        
        # Create metrics dataframe for display
        metrics_df = pd.DataFrame({
            "Period": forecast_data["forecast"]["period"],
            "Revenue (€M)": [round(rev/1000000, 2) for rev in forecast_data["forecast"]["revenue"]],
            "EBITDA (€M)": [round(ebitda/1000000, 2) for ebitda in forecast_data["forecast"]["ebitda"]],
            "Net Income (€M)": [round(income/1000000, 2) for income in forecast_data["forecast"]["net_income"]],
            "Growth Rate (%)": forecast_data["forecast"]["growth_rate"]
        })
        
        st.dataframe(metrics_df, hide_index=True, use_container_width=True)
        
        # Key growth drivers
        st.subheader("Key Growth Drivers")
        
        growth_drivers = pd.DataFrame({
            "Driver": ["Market Expansion", "New Products", "Price Increases", "Cost Optimization", "Acquisitions"],
            "Impact (€M)": [8.5, 6.2, 3.7, 2.1, 5.4],
            "Probability": [0.8, 0.7, 0.9, 0.95, 0.6]
        })
        
        # Calculate expected value
        growth_drivers["Expected Value (€M)"] = growth_drivers["Impact (€M)"] * growth_drivers["Probability"]
        
        # Create horizontal bar chart
        fig = px.bar(
            growth_drivers.sort_values("Expected Value (€M)", ascending=True),
            y="Driver",
            x="Expected Value (€M)",
            orientation="h",
            color="Probability",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[0.5, 1],
            labels={"Expected Value (€M)": "Expected Value (€ Millions)", "Driver": "Growth Driver"}
        )
        
        fig.update_layout(height=350)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Simulation tab
    with tabs[1]:
        st.subheader("Interactive Business Simulation")
        st.write("Adjust parameters to simulate different business scenarios")
        
        col1, col2 = st.columns([1, 2])
        
        # Parameter adjustments
        with col1:
            st.subheader("Simulation Parameters")
            
            price_change = st.slider(
                "Price Change (%)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.5,
                help="Adjust pricing strategy"
            )
            
            volume_change = st.slider(
                "Volume Change (%)",
                min_value=-15.0,
                max_value=15.0,
                value=0.0,
                step=0.5,
                help="Adjust sales volume"
            )
            
            cost_change = st.slider(
                "Cost Change (%)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.5,
                help="Adjust operational costs"
            )
            
            fx_rate = st.slider(
                "EUR/USD FX Rate",
                min_value=1.00,
                max_value=1.20,
                value=1.10,
                step=0.01,
                help="Adjust foreign exchange rate"
            )
            
            tax_rate = st.slider(
                "Effective Tax Rate (%)",
                min_value=15.0,
                max_value=35.0,
                value=25.0,
                step=0.5,
                help="Adjust tax assumptions"
            )
            
            # Run simulation button
            run_simulation = st.button("Run Simulation")
        
        # Simulation results display
        with col2:
            if run_simulation:
                st.subheader("Simulation Results")
                
                # Calculate impact of parameter changes
                impact_data = calculate_impact_scenarios(
                    data, 
                    price_change=price_change,
                    volume_change=volume_change,
                    cost_change=cost_change,
                    fx_rate=fx_rate,
                    tax_rate=tax_rate
                )
                
                # Display impact on key metrics
                col1, col2, col3 = st.columns(3)
                
                revenue_impact = impact_data["revenue_impact"]
                col1.metric(
                    label="Revenue Impact",
                    value=f"€{revenue_impact/1000000:.1f}M",
                    delta=f"{impact_data['revenue_impact_pct']:.1f}%"
                )
                
                ebitda_impact = impact_data["ebitda_impact"]
                col2.metric(
                    label="EBITDA Impact",
                    value=f"€{ebitda_impact/1000000:.1f}M",
                    delta=f"{impact_data['ebitda_impact_pct']:.1f}%"
                )
                
                net_income_impact = impact_data["net_income_impact"]
                col3.metric(
                    label="Net Income Impact",
                    value=f"€{net_income_impact/1000000:.1f}M",
                    delta=f"{impact_data['net_income_impact_pct']:.1f}%"
                )
                
                # Waterfall chart showing impact of each parameter
                impact_waterfall = pd.DataFrame({
                    "Factor": ["Base", "Price", "Volume", "Cost", "FX", "Tax", "Final"],
                    "Impact": [0, 
                              impact_data["price_impact"]/1000000, 
                              impact_data["volume_impact"]/1000000,
                              impact_data["cost_impact"]/1000000,
                              impact_data["fx_impact"]/1000000,
                              impact_data["tax_impact"]/1000000,
                              0],
                    "Position": [impact_data["base_ebitda"]/1000000,
                                0, 0, 0, 0, 0,
                                impact_data["new_ebitda"]/1000000]
                })
                
                # Create waterfall chart
                fig = go.Figure(go.Waterfall(
                    name="EBITDA Bridge",
                    orientation="v",
                    measure=["absolute", "relative", "relative", "relative", "relative", "relative", "absolute"],
                    x=impact_waterfall["Factor"],
                    textposition="outside",
                    y=impact_waterfall["Impact"],
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                ))
                
                fig.update_layout(
                    title="EBITDA Bridge Analysis (€ Millions)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Risk assessment
                risk_levels = impact_data["risk_assessment"]
                
                st.subheader("Risk Assessment")
                
                for risk, level in risk_levels.items():
                    level_color = "red" if level == "High" else "orange" if level == "Medium" else "green"
                    st.markdown(f"**{risk}**: <span style='color:{level_color}'>{level}</span>", unsafe_allow_html=True)
                
                # AI recommendation based on simulation
                if impact_data["ebitda_impact_pct"] > 5:
                    st.success("""
                    **AI Recommendation**: This scenario shows significant positive impact. 
                    Consider implementing these changes with careful monitoring of market response to price changes.
                    """)
                elif impact_data["ebitda_impact_pct"] < -5:
                    st.error("""
                    **AI Recommendation**: This scenario shows significant negative impact.
                    Not recommended without substantial strategic revisions.
                    """)
                else:
                    st.info("""
                    **AI Recommendation**: This scenario shows moderate impact.
                    Consider a phased implementation to test market response.
                    """)
            else:
                st.info("Adjust the parameters and click 'Run Simulation' to see results")
                
                # Show an example of previous simulation
                st.image(
                    "https://pixabay.com/get/g8591ce70aae26ee77b191a116683034b9156368fb4415bf914546f34f512bfbbb901aa2744c03361ebe1d2ab3d363f0e60568830a9b8dd6a20e0d8040d271d11_1280.jpg",
                    caption="Example Simulation Results",
                    width=500
                )
    
    # Scenario planning tab
    with tabs[2]:
        st.subheader("Scenario Planning")
        
        # Scenario selection
        scenario_options = [
            "Base Case",
            "Optimistic Scenario",
            "Pessimistic Scenario",
            "Market Disruption",
            "Rapid Expansion"
        ]
        
        selected_scenarios = st.multiselect(
            "Select scenarios to compare",
            options=scenario_options,
            default=["Base Case", "Optimistic Scenario", "Pessimistic Scenario"]
        )
        
        if selected_scenarios:
            # Generate scenario data
            scenario_data = {}
            for scenario in selected_scenarios:
                if scenario == "Base Case":
                    growth_rate = 5.0
                    margin_change = 0.0
                elif scenario == "Optimistic Scenario":
                    growth_rate = 8.5
                    margin_change = 2.0
                elif scenario == "Pessimistic Scenario":
                    growth_rate = 2.0
                    margin_change = -1.5
                elif scenario == "Market Disruption":
                    growth_rate = -3.0
                    margin_change = -4.0
                elif scenario == "Rapid Expansion":
                    growth_rate = 12.0
                    margin_change = -0.5
                
                # Generate forecast for this scenario
                scenario_data[scenario] = {
                    "growth_rate": growth_rate,
                    "margin_change": margin_change,
                    "data": generate_forecast_data(data, "24 Months", growth_rate, margin_change)
                }
            
            # Create a chart to compare scenarios
            fig = go.Figure()
            
            # Colors for different scenarios
            colors = {
                "Base Case": "#0A2463",
                "Optimistic Scenario": "#00C853",
                "Pessimistic Scenario": "#FF5252",
                "Market Disruption": "#9C27B0",
                "Rapid Expansion": "#FF9800"
            }
            
            # Add a line for each selected scenario
            for scenario in selected_scenarios:
                fig.add_trace(
                    go.Scatter(
                        x=scenario_data[scenario]["data"]["forecast"]["period"],
                        y=[rev/1000000 for rev in scenario_data[scenario]["data"]["forecast"]["revenue"]],
                        name=f"{scenario} (Growth: {scenario_data[scenario]['growth_rate']}%)",
                        line=dict(color=colors.get(scenario, "#0A2463"), width=3)
                    )
                )
            
            fig.update_layout(
                title="Revenue Forecast by Scenario (€ Millions)",
                xaxis_title="Period",
                yaxis_title="Revenue (€ Millions)",
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Comparison table for selected scenarios
            st.subheader("Scenario Comparison")
            
            # Create dataframe for comparison
            comparison_data = []
            
            for scenario in selected_scenarios:
                # Calculate average metrics for the scenario
                avg_revenue = np.mean(scenario_data[scenario]["data"]["forecast"]["revenue"])
                avg_ebitda = np.mean(scenario_data[scenario]["data"]["forecast"]["ebitda"])
                avg_margin = avg_ebitda / avg_revenue * 100 if avg_revenue > 0 else 0
                
                comparison_data.append({
                    "Scenario": scenario,
                    "Avg. Revenue (€M)": round(avg_revenue/1000000, 2),
                    "Avg. EBITDA (€M)": round(avg_ebitda/1000000, 2),
                    "Avg. EBITDA Margin (%)": round(avg_margin, 2),
                    "Growth Rate (%)": scenario_data[scenario]["growth_rate"]
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            st.dataframe(comparison_df, hide_index=True, use_container_width=True)
            
            # Radar chart for scenario comparison
            if len(selected_scenarios) >= 2:
                st.subheader("Scenario Comparison - Key Metrics")
                
                # Prepare data for radar chart
                radar_data = []
                
                for scenario in selected_scenarios:
                    s_data = scenario_data[scenario]["data"]["forecast"]
                    
                    # Calculate metrics for radar chart
                    avg_growth = np.mean(s_data["growth_rate"])
                    avg_ebitda_margin = np.mean([e/r*100 for e, r in zip(s_data["ebitda"], s_data["revenue"]) if r > 0])
                    roi = np.mean(s_data["roi"]) if "roi" in s_data else avg_ebitda_margin * 0.8
                    risk_score = 7 - (scenario_data[scenario]["growth_rate"] / 2)  # Higher growth = lower risk score
                    sustainability = 8 - abs(scenario_data[scenario]["margin_change"])  # Less margin change = more sustainable
                    
                    radar_data.append({
                        "Scenario": scenario,
                        "Growth Potential": avg_growth,
                        "Profitability": avg_ebitda_margin,
                        "ROI": roi,
                        "Risk (inverted)": risk_score,  # Lower is better
                        "Sustainability": sustainability
                    })
                
                radar_df = pd.DataFrame(radar_data)
                
                # Melt the dataframe for radar chart
                radar_melted = radar_df.melt(
                    id_vars=["Scenario"],
                    var_name="Metric",
                    value_name="Value"
                )
                
                # Create radar chart
                fig = px.line_polar(
                    radar_melted,
                    r="Value",
                    theta="Metric",
                    color="Scenario",
                    line_close=True,
                    color_discrete_map=colors
                )
                
                fig.update_layout(height=500)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Impact analysis
                st.subheader("Business Impact Analysis")
                
                # Select base scenario for comparison
                base_scenario = st.selectbox(
                    "Select base scenario for comparison",
                    options=selected_scenarios,
                    index=selected_scenarios.index("Base Case") if "Base Case" in selected_scenarios else 0
                )
                
                # Calculate impact compared to base scenario
                impact_analysis = []
                
                base_revenue = np.mean(scenario_data[base_scenario]["data"]["forecast"]["revenue"])
                base_ebitda = np.mean(scenario_data[base_scenario]["data"]["forecast"]["ebitda"])
                
                for scenario in selected_scenarios:
                    if scenario != base_scenario:
                        scenario_revenue = np.mean(scenario_data[scenario]["data"]["forecast"]["revenue"])
                        scenario_ebitda = np.mean(scenario_data[scenario]["data"]["forecast"]["ebitda"])
                        
                        revenue_impact = scenario_revenue - base_revenue
                        revenue_impact_pct = (revenue_impact / base_revenue) * 100 if base_revenue > 0 else 0
                        
                        ebitda_impact = scenario_ebitda - base_ebitda
                        ebitda_impact_pct = (ebitda_impact / base_ebitda) * 100 if base_ebitda > 0 else 0
                        
                        impact_analysis.append({
                            "Scenario": scenario,
                            "Revenue Impact (€M)": round(revenue_impact/1000000, 2),
                            "Revenue Impact (%)": round(revenue_impact_pct, 2),
                            "EBITDA Impact (€M)": round(ebitda_impact/1000000, 2),
                            "EBITDA Impact (%)": round(ebitda_impact_pct, 2)
                        })
                
                if impact_analysis:
                    impact_df = pd.DataFrame(impact_analysis)
                    
                    st.dataframe(impact_df, hide_index=True, use_container_width=True)
                else:
                    st.info(f"Select additional scenarios to compare with {base_scenario}")
        else:
            st.info("Select at least one scenario to view forecast")
    
    # AI recommendations tab
    with tabs[3]:
        st.subheader("AI-Generated Recommendations")
        
        if st.button("Generate AI Recommendations"):
            with st.spinner("Analyzing financial data and generating recommendations..."):
                # Generate AI recommendations
                recommendations = get_ai_recommendations(data)
                
                st.markdown("### Executive Summary")
                st.markdown(recommendations["executive_summary"])
                
                # Strategic opportunities
                st.subheader("Strategic Opportunities")
                
                for opportunity in recommendations["strategic_opportunities"]:
                    with st.expander(opportunity["title"]):
                        st.markdown(f"**Expected Impact**: {opportunity['impact']}")
                        st.markdown(f"**Timeline**: {opportunity['timeline']}")
                        st.markdown(f"**Description**: {opportunity['description']}")
                        st.markdown(f"**Key Actions**:")
                        for action in opportunity["key_actions"]:
                            st.markdown(f"- {action}")
                
                # Risk analysis
                st.subheader("Risk Analysis")
                
                risk_data = pd.DataFrame({
                    "Risk": [risk["title"] for risk in recommendations["risks"]],
                    "Probability": [risk["probability"] for risk in recommendations["risks"]],
                    "Impact": [risk["impact"] for risk in recommendations["risks"]],
                    "Severity": [risk["probability"] * risk["impact"] for risk in recommendations["risks"]]
                })
                
                # Create bubble chart for risk analysis
                fig = px.scatter(
                    risk_data,
                    x="Probability",
                    y="Impact",
                    size="Severity",
                    color="Severity",
                    hover_name="Risk",
                    text="Risk",
                    color_continuous_scale=["green", "yellow", "red"],
                    title="Risk Assessment Matrix"
                )
                
                fig.update_traces(textposition="top center")
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display risk mitigation strategies
                for risk in recommendations["risks"]:
                    if risk["probability"] * risk["impact"] >= 0.4:  # Only show mitigation for high severity risks
                        with st.expander(f"Mitigation Strategy: {risk['title']}"):
                            st.markdown(risk["mitigation"])
                
                # Performance levers
                st.subheader("Key Performance Levers")
                
                levers_data = pd.DataFrame(recommendations["performance_levers"])
                
                # Create horizontal bar chart for performance levers
                fig = px.bar(
                    levers_data.sort_values("impact", ascending=True),
                    y="lever",
                    x="impact",
                    orientation="h",
                    color="feasibility",
                    color_continuous_scale=["red", "yellow", "green"],
                    range_color=[0, 1],
                    title="Impact of Performance Levers",
                    labels={"impact": "Potential Impact (€ Millions)", "lever": "Performance Lever"}
                )
                
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Business insights
                st.subheader("Data-Driven Business Insights")
                
                for insight in recommendations["business_insights"]:
                    st.markdown(f"**{insight['title']}**")
                    st.markdown(insight["description"])
                    st.markdown("---")
                
                # Decision framework
                st.subheader("Executive Decision Framework")
                
                decision_data = pd.DataFrame(recommendations["decision_framework"])
                
                st.dataframe(decision_data, hide_index=True, use_container_width=True)
                
                # Slide for presentation to executives
                st.subheader("Executive Summary Slide")
                
                exec_col1, exec_col2 = st.columns([2, 1])
                
                with exec_col1:
                    st.image(
                        "https://pixabay.com/get/g53637582939dd59942edb1b6898f3315e3cd57741feea110423478849b84dd69ce37827266ac560fb4ea7bfa56ed47eda7d3d8e4fb8f6b9ee5454f271b506492_1280.jpg",
                        caption="Executive Presentation",
                        width=400
                    )
                
                with exec_col2:
                    st.markdown("### Key Takeaways")
                    for takeaway in recommendations["executive_takeaways"]:
                        st.markdown(f"- {takeaway}")

