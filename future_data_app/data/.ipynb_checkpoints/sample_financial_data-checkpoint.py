#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

def generate_sample_financial_data():
    """
    Generate sample financial data for demonstration purposes
    In a real scenario, this data would come from the CPM system
    """
    np.random.seed(42)  # For reproducibility
    
    # Define time periods
    periods = ["2021-Q3", "2021-Q4", "2022-Q1", "2022-Q2", 
              "2022-Q3", "2022-Q4", "2023-Q1", "2023-Q2"]
    
    # Define product categories
    categories = ["Product A", "Product B", "Product C", "Product D", "Product E", 
                 "Services", "Maintenance", "Licensing", "Consulting"]
    
    # Generate revenue data
    revenue_data = []
    
    # Base revenue values per category (millions)
    base_revenues = {
        "Product A": 25,
        "Product B": 18,
        "Product C": 15,
        "Product D": 12,
        "Product E": 10,
        "Services": 8,
        "Maintenance": 7,
        "Licensing": 6,
        "Consulting": 4
    }
    
    # Generate data for each period and category with growth trend
    for i, period in enumerate(periods):
        for category in categories:
            # Add some growth and seasonality
            growth_factor = 1 + (i * 0.01) + np.random.normal(0, 0.02)
            
            # Add seasonality - Q4 higher, Q1 lower
            if period.endswith("Q4"):
                seasonality = 1.1
            elif period.endswith("Q1"):
                seasonality = 0.95
            else:
                seasonality = 1.0
            
            amount = base_revenues[category] * growth_factor * seasonality * 1000000  # Convert to actual value
            
            revenue_data.append({
                "period": period,
                "category": category,
                "amount": amount
            })
    
    revenue_df = pd.DataFrame(revenue_data)
    
    # Generate cost data
    cost_data = []
    
    # Define cost categories
    cost_categories = ["COGS", "R&D", "Sales & Marketing", "G&A", "Operations"]
    
    # Base cost as percentage of revenue for each category
    cost_percentages = {
        "COGS": 0.42,
        "R&D": 0.12,
        "Sales & Marketing": 0.15,
        "G&A": 0.08,
        "Operations": 0.05
    }
    
    # Calculate total revenue by period
    total_revenue_by_period = revenue_df.groupby("period")["amount"].sum().to_dict()
    
    # Generate cost data
    for period in periods:
        period_revenue = total_revenue_by_period[period]
        
        for cost_category in cost_categories:
            base_percentage = cost_percentages[cost_category]
            # Add some variability to the cost percentage
            actual_percentage = base_percentage + np.random.normal(0, 0.01)
            
            amount = period_revenue * actual_percentage
            
            cost_data.append({
                "period": period,
                "category": cost_category,
                "amount": amount
            })
    
    cost_df = pd.DataFrame(cost_data)
    
    # Generate product data
    product_data = []
    
    product_names = [
        "Enterprise Server X1", "Enterprise Server X2", "Cloud Storage Basic",
        "Cloud Storage Premium", "Security Suite Pro", "Security Suite Enterprise",
        "Networking Basic", "Networking Advanced", "Mobile Solution A",
        "Mobile Solution B", "Database Standard", "Database Enterprise",
        "Analytics Basic", "Analytics Premium", "Development Tools",
        "Integration Suite", "Support Basic", "Support Premium",
        "Professional Services", "Training Services"
    ]
    
    for i, name in enumerate(product_names):
        # Generate synthetic product data
        revenue = np.random.uniform(2.0, 30.0) * 1000000  # Between 2M and 30M
        cost = revenue * np.random.uniform(0.5, 0.85)  # Cost is 50-85% of revenue
        profit = revenue - cost
        profit_margin = (profit / revenue) * 100
        
        product_data.append({
            "id": i + 1,
            "name": name,
            "revenue": revenue,
            "cost": cost,
            "profit_margin": profit_margin,
            "yoy_growth": np.random.uniform(-5.0, 25.0),  # YoY growth between -5% and 25%
            "market_share": np.random.uniform(1.0, 15.0),  # Market share between 1% and 15%
            "customer_satisfaction": np.random.uniform(3.0, 4.8),  # Customer satisfaction between 3.0 and 4.8
            "raw_material_increase": np.random.uniform(5.0, 25.0) if profit_margin < 15 else 0  # Raw material increase for low-margin products
        })
    
    product_df = pd.DataFrame(product_data)
    
    # Generate geographic data
    geo_data = []
    
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East", "Africa"]
    
    for region in regions:
        # Generate synthetic geographic data
        revenue = np.random.uniform(5.0, 80.0) * 1000000  # Between 5M and 80M
        cost = revenue * np.random.uniform(0.55, 0.80)  # Cost is 55-80% of revenue
        
        geo_data.append({
            "region": region,
            "revenue": revenue,
            "cost": cost,
            "growth": np.random.uniform(-2.0, 15.0)  # Growth between -2% and 15%
        })
    
    geo_df = pd.DataFrame(geo_data)
    
    # Generate forecast data with proper structure for all periods
    forecast_data = []
    
    # For all periods, create forecast data with some deviation from actual
    for period in periods:
        for category in categories:
            # Find the actual revenue for this category in this period
            # Handle potential missing values using a fallback
            matching_rows = revenue_df[(revenue_df["period"] == period) & (revenue_df["category"] == category)]
            if len(matching_rows) > 0:
                actual = matching_rows["amount"].values[0]
            else:
                actual = 1000000  # Default value if missing
            
            # Generate a forecast with some deviation from actual
            forecast_amount = actual * np.random.uniform(0.85, 1.15)
            
            forecast_data.append({
                "period": period,
                "category": category,
                "amount": forecast_amount
            })
    
    forecast_df = pd.DataFrame(forecast_data)
    
    # Generate data quality metrics
    data_quality = {
        "overall_score": 92,
        "previous_score": 87,
        "completeness": 95,
        "accuracy": 90,
        "consistency": 89,
        "timeliness": 94,
        "critical_issues": 2,
        "data_sources": ["Anaplan", "SAP", "Excel", "PowerBI"],
        "anomalies": [
            {
                "entity": "Revenue",
                "field": "Amount",
                "value": "€1,000",
                "expected": "€1,000,000",
                "severity": "High",
                "description": "Order of magnitude error detected. Revenue value is 1000x smaller than expected."
            },
            {
                "entity": "Cost of Sales",
                "field": "Category",
                "value": "Missing",
                "expected": "COGS",
                "severity": "Medium",
                "description": "Cost category is missing for some entries in the Asia Pacific region."
            },
            {
                "entity": "FX Rates",
                "field": "EUR/USD",
                "value": "1.02, 1.08, 1.06",
                "expected": "Consistent Rate",
                "severity": "High",
                "description": "Inconsistent FX rates used across different departments."
            }
        ],
        "validation_results": [
            {
                "check": "Revenue Completeness",
                "status": "Passed",
                "description": "All revenue entries are complete for the reporting period."
            },
            {
                "check": "Cost Allocation",
                "status": "Warning",
                "description": "15% of cost entries are missing proper department allocation."
            },
            {
                "check": "Balance Sheet Reconciliation",
                "status": "Passed",
                "description": "Balance sheet accounts are reconciled within threshold."
            },
            {
                "check": "Intercompany Eliminations",
                "status": "Failed",
                "description": "Intercompany transactions not fully eliminated in consolidation."
            },
            {
                "check": "Currency Translation",
                "status": "Warning",
                "description": "Some subsidiaries using inconsistent currency translation methods."
            },
            {
                "check": "Segment Reporting",
                "status": "Passed",
                "description": "Segment reporting is consistent with management reporting."
            }
        ]
    }
    
    # Calculate key metrics
    current_revenue = revenue_df[revenue_df["period"] == "2023-Q2"]["amount"].sum()
    previous_revenue = revenue_df[revenue_df["period"] == "2022-Q2"]["amount"].sum()
    
    current_costs = cost_df[cost_df["period"] == "2023-Q2"]["amount"].sum()
    previous_costs = cost_df[cost_df["period"] == "2022-Q2"]["amount"].sum()
    
    current_ebitda = current_revenue - current_costs
    previous_ebitda = previous_revenue - previous_costs
    
    yoy_revenue_growth = ((current_revenue - previous_revenue) / previous_revenue) * 100
    ebitda_margin = (current_ebitda / current_revenue) * 100
    previous_ebitda_margin = (previous_ebitda / previous_revenue) * 100
    
    # Top and bottom products
    top_product = product_df.sort_values("profit_margin", ascending=False).iloc[0]["name"]
    bottom_product = product_df.sort_values("profit_margin", ascending=True).iloc[0]["name"]
    
    # Operating cash flow (estimated as 80% of EBITDA)
    operating_cash_flow = current_ebitda * 0.8
    previous_cash_flow = previous_ebitda * 0.8
    
    # Net income (estimated as 65% of EBITDA)
    net_income = current_ebitda * 0.65
    previous_net_income = previous_ebitda * 0.65
    
    # Calculate forecast metrics
    forecast_revenue_growth = 7.5  # Forecast 7.5% annual growth
    forecast_ebitda_margin = 18.0  # Forecast 18% EBITDA margin
    forecast_roi = 12.5  # Forecast 12.5% ROI
    
    # Assemble all data
    return {
        "financial_data": {
            "revenue": revenue_df,
            "costs": cost_df
        },
        "products": product_df,
        "geographic": geo_df,
        "forecast": forecast_df,
        "data_quality": data_quality,
        "metrics": {
            "revenue": current_revenue,
            "previous_revenue": previous_revenue,
            "ebitda": current_ebitda,
            "previous_ebitda": previous_ebitda,
            "yoy_revenue_growth": yoy_revenue_growth,
            "ebitda_margin": ebitda_margin,
            "previous_ebitda_margin": previous_ebitda_margin,
            "top_product": top_product,
            "bottom_product": bottom_product,
            "operating_cash_flow": operating_cash_flow,
            "previous_cash_flow": previous_cash_flow,
            "net_income": net_income,
            "previous_net_income": previous_net_income,
            "tax_rate": 25.0,  # Assumed tax rate
            "fx_rate": 1.10,   # Assumed FX rate (EUR/USD)
            "market_conditions": "Moderate growth with inflationary pressure"
        },
        "forecast": {
            "revenue_growth": forecast_revenue_growth,
            "ebitda_margin": forecast_ebitda_margin,
            "roi": forecast_roi
        }
    }

