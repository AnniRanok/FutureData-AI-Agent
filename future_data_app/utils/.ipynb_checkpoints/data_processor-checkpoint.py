#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from data.sample_financial_data import generate_sample_financial_data

def load_data():
    """
    Load financial data from the data source
    For demonstration purposes, this function returns sample data
    In a real scenario, this would connect to the CPM system
    """
    # Generate sample financial data
    return generate_sample_financial_data()

def process_revenue_data(data):
    """
    Process revenue data for analysis
    """
    # Extract revenue data
    revenue_data = data["financial_data"]["revenue"]
    
    # Calculate total revenue by period
    total_revenue = revenue_data.groupby("period")["amount"].sum().reset_index()
    
    # Calculate growth rates
    total_revenue["growth_rate"] = total_revenue["amount"].pct_change() * 100
    
    return total_revenue

def process_cost_data(data):
    """
    Process cost data for analysis
    """
    # Extract cost data
    cost_data = data["financial_data"]["costs"]
    
    # Calculate total costs by period and category
    total_costs_by_category = cost_data.groupby(["period", "category"])["amount"].sum().reset_index()
    
    # Calculate total costs by period
    total_costs = cost_data.groupby("period")["amount"].sum().reset_index()
    
    return {
        "total_costs": total_costs,
        "by_category": total_costs_by_category
    }

def calculate_profitability(data):
    """
    Calculate profitability metrics
    """
    # Process revenue and cost data
    revenue_data = process_revenue_data(data)
    cost_data = process_cost_data(data)
    
    # Merge revenue and cost data by period
    profitability = pd.merge(
        revenue_data,
        cost_data["total_costs"],
        on="period",
        suffixes=("_revenue", "_cost")
    )
    
    # Calculate gross profit and margin
    profitability["gross_profit"] = profitability["amount_revenue"] - profitability["amount_cost"]
    profitability["gross_margin"] = (profitability["gross_profit"] / profitability["amount_revenue"]) * 100
    
    return profitability

def get_product_performance(data):
    """
    Get product performance metrics
    """
    # Extract product data
    products = data["products"]
    
    # Calculate profitability metrics
    products["profit"] = products["revenue"] - products["cost"]
    products["profit_margin"] = (products["profit"] / products["revenue"]) * 100
    
    # Sort by profit margin to identify top and bottom performers
    top_performers = products.sort_values("profit_margin", ascending=False).head(10)
    bottom_performers = products.sort_values("profit_margin", ascending=True).head(10)
    
    return {
        "all_products": products,
        "top_performers": top_performers,
        "bottom_performers": bottom_performers
    }

def get_geographic_performance(data):
    """
    Get performance metrics by geographic region
    """
    # Extract geographic data
    geo_data = data["geographic"]
    
    # Calculate profitability metrics
    geo_data["profit"] = geo_data["revenue"] - geo_data["cost"]
    geo_data["profit_margin"] = (geo_data["profit"] / geo_data["revenue"]) * 100
    
    # Sort by profit margin
    geo_performance = geo_data.sort_values("profit_margin", ascending=False)
    
    return geo_performance

def get_forecast_data(data):
    """
    Get forecast data for analysis
    """
    # Extract forecast data
    forecast = data["forecast"]
    
    # Calculate deviation from actual
    actuals = data["financial_data"]["revenue"]
    
    # Get the most recent period
    current_period = actuals["period"].max()
    
    # Filter forecast for the current period
    current_forecast = forecast[forecast["period"] == current_period]
    current_actuals = actuals[actuals["period"] == current_period]
    
    # Calculate variances
    variance_analysis = []
    
    for _, forecast_row in current_forecast.iterrows():
        category = forecast_row["category"]
        forecast_amount = forecast_row["amount"]
        
        # Find the corresponding actual amount
        actual_row = current_actuals[current_actuals["category"] == category]
        
        if not actual_row.empty:
            actual_amount = actual_row["amount"].values[0]
            variance = actual_amount - forecast_amount
            variance_pct = (variance / forecast_amount) * 100 if forecast_amount != 0 else 0
            
            variance_analysis.append({
                "category": category,
                "forecast": forecast_amount,
                "actual": actual_amount,
                "variance": variance,
                "variance_pct": variance_pct
            })
    
    return pd.DataFrame(variance_analysis)

