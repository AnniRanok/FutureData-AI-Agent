#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_data_quality_metrics(data):
    """
    Calculate data quality metrics for the dashboard
    """
    # Extract data quality metrics
    quality_metrics = data["data_quality"]
    
    # For the UI, we'll return simplified metrics
    return {
        "overall_score": quality_metrics["overall_score"],
        "previous_score": quality_metrics["previous_score"],
        "overall_score_change": quality_metrics["overall_score"] - quality_metrics["previous_score"],
        "completeness": quality_metrics["completeness"],
        "accuracy": quality_metrics["accuracy"],
        "consistency": quality_metrics["consistency"],
        "timeliness": quality_metrics["timeliness"],
        "critical_issues": quality_metrics["critical_issues"]
    }

def get_anomalies(data):
    """
    Get anomalies from the data
    """
    # Extract anomalies from the data
    anomalies = data["data_quality"]["anomalies"]
    
    # Convert to DataFrame for display
    if anomalies:
        return pd.DataFrame(anomalies)
    else:
        return pd.DataFrame(columns=["entity", "field", "value", "expected", "severity", "description"])

def get_validation_results(data):
    """
    Get validation results from the data
    """
    # Extract validation results
    validation_results = data["data_quality"]["validation_results"]
    
    # Convert to DataFrame for display
    return pd.DataFrame(validation_results)

def get_data_quality_trends():
    """
    Generate data quality trend data
    """
    # Define periods for trend data
    periods = ["2023-Jan", "2023-Feb", "2023-Mar", "2023-Apr", "2023-May", "2023-Jun"]
    
    # Generate trend data with a general improvement pattern
    # In a real scenario, this would come from historical quality metrics
    trend_data = []
    
    np.random.seed(42)  # For reproducibility
    
    # Start with lower values and gradually improve
    overall_scores = [80, 82, 85, 87, 90, 92]
    completeness = [85, 86, 88, 90, 92, 95]
    accuracy = [75, 78, 80, 85, 88, 90]
    consistency = [78, 80, 83, 85, 87, 89]
    
    for i, period in enumerate(periods):
        trend_data.append({
            "period": period,
            "overall_score": overall_scores[i],
            "completeness": completeness[i],
            "accuracy": accuracy[i],
            "consistency": consistency[i]
        })
    
    return pd.DataFrame(trend_data)

def generate_action_plan(data):
    """
    Generate a data quality action plan based on identified issues
    """
    # This would normally call the OpenAI helper, but for simplicity in case of API issues,
    # we'll use a pre-defined action plan
    from utils.openai_helper import generate_data_quality_analysis
    
    # Generate the action plan
    try:
        action_plan = generate_data_quality_analysis(data)
        return action_plan
    except Exception as e:
        # Fallback to pre-defined action plan
        from utils.openai_helper import get_fallback_data_quality_analysis
        return get_fallback_data_quality_analysis()

def get_data_quality_by_department():
    """
    Generate data quality metrics by department
    """
    # Define departments and their quality metrics
    departments = ["Accounting", "Sales", "Marketing", "Operations", "HR", "Supply Chain"]
    
    dept_quality = []
    
    np.random.seed(42)  # For reproducibility
    
    for dept in departments:
        quality_score = np.random.randint(75, 99)
        issues_count = 100 - quality_score
        
        dept_quality.append({
            "Department": dept,
            "Quality Score": quality_score,
            "Issues": issues_count
        })
    
    return pd.DataFrame(dept_quality)

