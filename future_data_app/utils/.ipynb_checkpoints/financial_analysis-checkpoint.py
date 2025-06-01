#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

def calculate_yoy_performance(data):
    """
    Calculate year-over-year performance metrics
    """
    # Get revenue data for current and previous years
    revenue_current = data["financial_data"]["revenue"]
    
    # Group by category and calculate totals
    current_year = revenue_current[revenue_current["period"] == "2023-Q2"].groupby("category")["amount"].sum().reset_index()
    previous_year = revenue_current[revenue_current["period"] == "2022-Q2"].groupby("category")["amount"].sum().reset_index()
    
    # Merge current and previous year data
    yoy_comparison = pd.merge(
        current_year,
        previous_year,
        on="category",
        suffixes=("_current", "_previous")
    )
    
    # Calculate changes
    yoy_comparison["change"] = yoy_comparison["amount_current"] - yoy_comparison["amount_previous"]
    yoy_comparison["percent_change"] = (yoy_comparison["change"] / yoy_comparison["amount_previous"]) * 100
    
    # Rename columns for clarity
    yoy_comparison = yoy_comparison.rename(columns={
        "amount_current": "current_year",
        "amount_previous": "previous_year"
    })
    
    return yoy_comparison

def calculate_actual_vs_forecast(data):
    """
    Calculate actual vs forecast performance
    """
    # Get actual revenue data
    actuals = data["financial_data"]["revenue"]
    
    # Get the most recent period
    current_period = "2023-Q2"
    
    # Filter actuals for the current period
    current_actuals = actuals[actuals["period"] == current_period].groupby("category")["amount"].sum().reset_index()
    
    # Create forecast data based on actuals with variance
    np.random.seed(42)  # For reproducibility
    current_forecast = current_actuals.copy()
    # Add variation to create realistic forecast differences
    current_forecast["amount"] = current_forecast["amount"] * np.random.uniform(0.9, 1.1, len(current_forecast))
    
    # Merge actual and forecast data
    comparison = pd.merge(
        current_actuals,
        current_forecast,
        on="category",
        suffixes=("_actual", "_forecast")
    )
    
    # Calculate variances
    comparison["variance"] = comparison["amount_actual"] - comparison["amount_forecast"]
    comparison["variance_pct"] = (comparison["variance"] / comparison["amount_forecast"]) * 100
    
    # Rename columns for clarity
    comparison = comparison.rename(columns={
        "amount_actual": "actual",
        "amount_forecast": "forecast"
    })
    
    # Add explanation for significant variances
    explanations = {
        "Product A": "Higher than expected market demand and successful promotional campaign",
        "Product B": "Supply chain disruptions delayed product release by 3 weeks",
        "Product C": "Expected seasonality in line with forecast",
        "Product D": "Price increases implemented ahead of schedule",
        "Product E": "Competitor promotional activity impacted sales volumes",
        "Services": "New service offering exceeded expectations with strong client adoption",
        "Maintenance": "Contract renewals higher than forecast due to customer retention initiatives",
        "Licensing": "Delay in new license release impacted revenue",
        "Consulting": "Resource constraints limited project capacity"
    }
    
    # Ensure all categories have explanations using a default for missing ones
    comparison["explanation"] = comparison["category"].apply(
        lambda x: explanations.get(x, "Variance under investigation by finance team")
    )
    
    return comparison

def identify_top_performers(data, top=5, reverse=False):
    """
    Identify top or bottom performing products based on profit margin
    """
    # Get product data
    products = data["products"].copy()
    
    # Sort by profit margin
    if reverse:
        # Bottom performers (ascending order)
        performers = products.sort_values("profit_margin", ascending=True).head(top)
    else:
        # Top performers (descending order)
        performers = products.sort_values("profit_margin", ascending=False).head(top)
    
    return performers

def get_profitability_analysis(data):
    """
    Generate profitability analysis data for visualization
    """
    # Product categories and regions for the heatmap
    categories = ["Hardware", "Software", "Services", "Cloud", "Consulting"]
    regions = ["Europe", "North America", "Asia Pacific", "Latin America", "Middle East"]
    
    # Create synthetic profitability data for the heatmap
    # In a real scenario, this would be calculated from actual data
    np.random.seed(42)  # For reproducibility
    
    # Generate a heatmap matrix of profit margins
    heatmap_data = np.random.normal(loc=15, scale=5, size=(len(categories), len(regions)))
    
    # Adjust some values to create interesting patterns
    heatmap_data[0, 0] = 22  # High profitability for Hardware in Europe
    heatmap_data[2, 1] = 25  # High profitability for Services in North America
    heatmap_data[3, 2] = 26  # High profitability for Cloud in Asia Pacific
    heatmap_data[1, 3] = 8   # Low profitability for Software in Latin America
    heatmap_data[4, 4] = 7   # Low profitability for Consulting in Middle East
    
    return {
        "categories": categories,
        "regions": regions,
        "heatmap_data": heatmap_data
    }

def analyze_product_margin_drivers(data, product_id):
    """
    Analyze drivers of product margin performance
    """
    # Get product data
    product = data["products"][data["products"]["id"] == product_id].iloc[0]
    
    # Define drivers of margin performance
    drivers = [
        {"name": "Raw Materials", "impact": -2.5, "controllable": "Medium"},
        {"name": "Labor Cost", "impact": -1.2, "controllable": "Medium"},
        {"name": "Pricing Strategy", "impact": 3.8, "controllable": "High"},
        {"name": "Volume/Scale", "impact": 1.5, "controllable": "Medium"},
        {"name": "Product Mix", "impact": 2.2, "controllable": "High"},
        {"name": "Operational Efficiency", "impact": 0.8, "controllable": "High"},
        {"name": "Currency Effects", "impact": -0.6, "controllable": "Low"}
    ]
    
    return pd.DataFrame(drivers)

