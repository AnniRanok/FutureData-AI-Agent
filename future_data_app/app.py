#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import streamlit as st
from components.sidebar import render_sidebar
from components.performance_dashboard import render_performance_dashboard
from components.data_quality_dashboard import render_data_quality_dashboard
from components.forecasting_dashboard import render_forecasting_dashboard
from utils.data_processor import load_data

# Set page configuration
st.set_page_config(
    page_title="Future Data AI Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main application
def main():
    # App title and brief introduction
    st.title("Future Data AI Agent")
    
    # Load sample financial data
    financial_data = load_data()
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Render the appropriate dashboard based on user selection
    if selected_page == "Performance Analysis":
        render_performance_dashboard(financial_data)
    elif selected_page == "Data Quality":
        render_data_quality_dashboard(financial_data)
    elif selected_page == "Forecasting & Recommendations":
        render_forecasting_dashboard(financial_data)
    else:
        # Landing page with overview
        st.header("Corporate Finance AI Assistant")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Transform Your Financial Analysis")
            st.write("""
            Future Data AI Agent plugs into your existing CPM suite, 
            giving you AI-powered insights and automating the grunt work 
            so your team can focus on strategic decision making.
            """)
            
            st.info("""
            **Get Started**: Select a module from the sidebar to explore how 
            our AI can help your finance team with performance analysis, 
            data quality checks, and forecasting.
            """)
            
            key_metrics = {
                "Close Timeline Saved": "6 days",
                "Data Quality Score": "92%",
                "FX Exposure Risk": "€1.4M"
            }
            
            for metric, value in key_metrics.items():
                st.metric(label=metric, value=value)
        
        with col2:
            st.image("business-2790180_1280.png", use_column_width=True)


            with st.expander("Why Future Data AI Agent?"):
                st.write("""
                - **Built specifically for corporate finance teams**
                - **Connects with Anaplan, Hyperion, or OneStream**
                - **Reduces manual reconciliation by 68%**
                - **Flat €466/month pricing - no surprises**
                - **48-hour setup with no coding required**
                """)

if __name__ == "__main__":
    main()

