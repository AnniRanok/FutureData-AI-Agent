#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.openai_helper import generate_forecast_recommendations

def generate_forecast_data(data, forecast_period, growth_override=None, margin_override=None):
    """
    Generate forecast data for the dashboard
    """
    # Extract base data
    financial_data = data["financial_data"]
    metrics = data["metrics"]
    
    # Determine number of periods based on forecast period selection
    if forecast_period == "12 Months":
        forecast_periods = 4  # Quarterly for 1 year
    elif forecast_period == "24 Months":
        forecast_periods = 8  # Quarterly for 2 years
    elif forecast_period == "36 Months":
        forecast_periods = 12  # Quarterly for 3 years
    else:  # 5 Years
        forecast_periods = 20  # Quarterly for 5 years
    
    # Historical periods (last 2 years)
    historical_periods = ["2021-Q3", "2021-Q4", "2022-Q1", "2022-Q2", 
                         "2022-Q3", "2022-Q4", "2023-Q1", "2023-Q2"]
    
    # Historical revenue data
    historical_revenue = [90.5, 100.2, 92.3, 97.8, 95.4, 105.8, 98.5, 105.2]
    historical_revenue = [r * 1000000 for r in historical_revenue]  # Convert to full values
    
    # Historical EBITDA data (as percentage of revenue)
    historical_ebitda_margin = [0.18, 0.19, 0.17, 0.18, 0.17, 0.18, 0.16, 0.17]
    historical_ebitda = [r * m for r, m in zip(historical_revenue, historical_ebitda_margin)]
    
    # Historical net income data (as percentage of revenue)
    historical_net_income_margin = [0.12, 0.13, 0.11, 0.12, 0.11, 0.12, 0.10, 0.11]
    historical_net_income = [r * m for r, m in zip(historical_revenue, historical_net_income_margin)]
    
    # Create historical data DataFrame
    historical_data = {
        "period": historical_periods,
        "revenue": historical_revenue,
        "ebitda": historical_ebitda,
        "net_income": historical_net_income
    }
    
    # Generate forecast periods
    last_period = historical_periods[-1]
    year = int(last_period.split("-")[0])
    quarter = int(last_period.split("-Q")[1])
    
    forecast_period_list = []
    
    for i in range(forecast_periods):
        quarter = quarter + 1
        if quarter > 4:
            quarter = 1
            year += 1
        forecast_period_list.append(f"{year}-Q{quarter}")
    
    # Use provided growth rate or default to the one in data
    growth_rate = growth_override if growth_override is not None else data["forecast"]["revenue_growth"]
    
    # Calculate forecast revenue with some variability
    np.random.seed(42)  # For reproducibility
    
    # Base growth rate with quarterly variability
    quarterly_growth_rates = []
    
    for i in range(forecast_periods):
        # Add some quarterly variability to the growth rate
        if i % 4 == 0:  # Q1 typically lower
            adjusted_growth = growth_rate - 1.0 + np.random.normal(0, 0.5)
        elif i % 4 == 3:  # Q4 typically higher
            adjusted_growth = growth_rate + 1.5 + np.random.normal(0, 0.5)
        else:  # Q2 and Q3 closer to the average
            adjusted_growth = growth_rate + np.random.normal(0, 0.7)
        
        quarterly_growth_rates.append(adjusted_growth)
    
    # Calculate forecast revenue
    base_revenue = historical_revenue[-1]
    forecast_revenue = []
    
    for rate in quarterly_growth_rates:
        quarter_growth = rate / 4  # Convert annual rate to quarterly
        next_revenue = base_revenue * (1 + quarter_growth / 100)
        forecast_revenue.append(next_revenue)
        base_revenue = next_revenue
    
    # Calculate confidence intervals
    forecast_revenue_upper = [r * (1 + (0.05 * (i + 1))) for i, r in enumerate(forecast_revenue)]
    forecast_revenue_lower = [r * (1 - (0.05 * (i + 1))) for i, r in enumerate(forecast_revenue)]
    
    # Use provided margin override or default margins
    ebitda_margin_base = margin_override if margin_override is not None else historical_ebitda_margin[-1]
    
    # Calculate forecast EBITDA and net income with gradual margin improvement
    forecast_ebitda_margin = []
    forecast_net_income_margin = []
    
    for i in range(forecast_periods):
        # Gradual margin improvement
        if margin_override is not None:
            em = ebitda_margin_base
        else:
            em = ebitda_margin_base + (i * 0.002)  # Gradual improvement
        
        nim = em * 0.65  # Net income as percentage of EBITDA
        
        forecast_ebitda_margin.append(em)
        forecast_net_income_margin.append(nim)
    
    forecast_ebitda = [r * m for r, m in zip(forecast_revenue, forecast_ebitda_margin)]
    forecast_net_income = [r * m for r, m in zip(forecast_revenue, forecast_net_income_margin)]
    
    # Calculate ROI for each period
    forecast_roi = [(ni / r) * 100 for ni, r in zip(forecast_net_income, forecast_revenue)]
    
    # Create forecast data dictionary
    forecast_data = {
        "period": forecast_period_list,
        "revenue": forecast_revenue,
        "revenue_upper": forecast_revenue_upper,
        "revenue_lower": forecast_revenue_lower,
        "ebitda": forecast_ebitda,
        "net_income": forecast_net_income,
        "growth_rate": quarterly_growth_rates,
        "roi": forecast_roi
    }
    
    # Return both historical and forecast data
    return {
        "historical": historical_data,
        "forecast": forecast_data
    }

def calculate_impact_scenarios(data, price_change=0, volume_change=0, cost_change=0, fx_rate=1.10, tax_rate=25):
    """
    Calculate impact of parameter changes on financial projections
    """
    # Base financial metrics
    base_revenue = data["metrics"]["revenue"]
    base_ebitda = data["metrics"]["ebitda"]
    base_net_income = data["metrics"]["net_income"]
    base_tax_rate = data["metrics"]["tax_rate"]
    base_fx_rate = data["metrics"]["fx_rate"]
    
    # Calculate impacts
    
    # Price impact: direct effect on revenue and flows to EBITDA and net income
    price_impact = base_revenue * (price_change / 100)
    
    # Volume impact: affects revenue with corresponding cost changes
    volume_impact = base_revenue * (volume_change / 100)
    
    # Cost impact: direct effect on EBITDA and net income
    cost_impact = -(base_revenue * (cost_change / 100))
    
    # FX impact: calculated based on international exposure
    international_exposure = base_revenue * 0.40  # Assume 40% international exposure
    fx_impact = international_exposure * ((fx_rate - base_fx_rate) / base_fx_rate)
    
    # Tax impact: affects only net income
    tax_impact = -((base_ebitda + price_impact + volume_impact + cost_impact) * (tax_rate - base_tax_rate) / 100)
    
    # Calculate total impacts
    revenue_impact = price_impact + volume_impact
    ebitda_impact = price_impact + volume_impact + cost_impact + fx_impact
    net_income_impact = ebitda_impact + tax_impact
    
    # Calculate percentage impacts
    revenue_impact_pct = (revenue_impact / base_revenue) * 100
    ebitda_impact_pct = (ebitda_impact / base_ebitda) * 100
    net_income_impact_pct = (net_income_impact / base_net_income) * 100
    
    # Calculate new values
    new_revenue = base_revenue + revenue_impact
    new_ebitda = base_ebitda + ebitda_impact
    new_net_income = base_net_income + net_income_impact
    
    # Risk assessment
    risk_assessment = {
        "FX Risk": "High" if abs(fx_impact) > 1000000 else "Medium" if abs(fx_impact) > 500000 else "Low",
        "Margin Risk": "High" if ebitda_impact_pct < -5 else "Medium" if ebitda_impact_pct < 0 else "Low",
        "Competitive Risk": "High" if price_change > 5 else "Medium" if price_change > 2 else "Low",
        "Execution Risk": "High" if volume_change > 10 else "Medium" if volume_change > 5 else "Low",
        "Overall Risk": "High" if ebitda_impact_pct < -10 else "Medium" if ebitda_impact_pct < 0 else "Low"
    }
    
    # Return impact analysis
    return {
        "price_impact": price_impact,
        "volume_impact": volume_impact,
        "cost_impact": cost_impact,
        "fx_impact": fx_impact,
        "tax_impact": tax_impact,
        "revenue_impact": revenue_impact,
        "ebitda_impact": ebitda_impact,
        "net_income_impact": net_income_impact,
        "revenue_impact_pct": revenue_impact_pct,
        "ebitda_impact_pct": ebitda_impact_pct,
        "net_income_impact_pct": net_income_impact_pct,
        "base_revenue": base_revenue,
        "base_ebitda": base_ebitda,
        "base_net_income": base_net_income,
        "new_revenue": new_revenue,
        "new_ebitda": new_ebitda,
        "new_net_income": new_net_income,
        "risk_assessment": risk_assessment
    }

def get_ai_recommendations(data):
    """
    Get AI-generated recommendations based on financial data
    """
    # This would normally call the OpenAI helper, but for simplicity in case of API issues,
    # we'll use a pre-defined set of recommendations
    from utils.openai_helper import generate_forecast_recommendations
    
    # Generate recommendations
    try:
        recommendations = generate_forecast_recommendations(data)
        return recommendations
    except Exception as e:
        # Fallback to pre-defined recommendations
        from utils.openai_helper import get_fallback_forecast_recommendations
        return get_fallback_forecast_recommendations()

