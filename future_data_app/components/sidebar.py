#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

def render_sidebar():
    """
    Renders the sidebar navigation and returns the selected page
    """
    st.sidebar.image("attached_assets/logo-transparent.png", 
                     width=200)
    
    st.sidebar.title("Navigation")
    
    # Navigation options - reordered to put Data Quality before Performance Analysis
    pages = [
        "Home",
        "Data Quality",
        "Performance Analysis", 
        "Forecasting & Recommendations"
    ]
    
    selected_page = st.sidebar.radio("Select Module", pages)
    
    # Data source section
    st.sidebar.subheader("Data Source")
    
    # CPM system selection
    cpm_system = st.sidebar.selectbox(
        "Connected CPM System",
        ["Anaplan", "OneStream", "Oracle Hyperion", "SAP BPC", "IBM Planning Analytics"]
    )
    
    # Time period selection
    reporting_period = st.sidebar.selectbox(
        "Reporting Period",
        ["Q4 2023", "Q3 2023", "Q2 2023", "Q1 2023", "FY 2022"]
    )
    
    # Simulated data refresh button
    if st.sidebar.button("Refresh Data"):
        st.sidebar.success("Data refreshed successfully!")
    
    # Display data health score
    st.sidebar.metric(
        label="Data Health Score", 
        value="92%",
        delta="5%"
    )
    
    # Help section
    with st.sidebar.expander("Need Help?"):
        st.write("""
        This application connects to your corporate performance management system
        to provide AI-powered analysis and recommendations.
        
        For assistance, contact support@futuredata.ai
        """)
    
    return selected_page

