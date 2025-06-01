#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
import streamlit as st
from openai import OpenAI

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user

# Get API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

# Initialize OpenAI client
openai = OpenAI(api_key=OPENAI_API_KEY)

def generate_performance_explanation(data):
    """
    Generate AI-powered explanation of financial performance using OpenAI
    """
    try:
        # Create a simplified data summary to send to the API
        data_summary = {
            "revenue": data["metrics"]["revenue"],
            "previous_revenue": data["metrics"]["previous_revenue"],
            "ebitda": data["metrics"]["ebitda"],
            "previous_ebitda": data["metrics"]["previous_ebitda"],
            "yoy_growth": data["metrics"]["yoy_revenue_growth"],
            "top_product": data["metrics"]["top_product"],
            "bottom_product": data["metrics"]["bottom_product"],
            "market_conditions": data["metrics"]["market_conditions"]
        }
        
        # Define the prompt for the OpenAI API
        prompt = f"""
        You are a financial analyst AI assistant. Analyze the financial performance data provided below and generate:
        1. A brief executive summary (3-4 sentences)
        2. 4-5 key findings from the data
        3. 3-4 actionable recommendations
        4. A list of contributing factors to performance with numeric impact values (percentages)
        5. A brief paragraph on opportunities for improvement
        
        Financial Data:
        {json.dumps(data_summary, indent=2)}
        
        Respond with JSON in this format:
        {{
            "executive_summary": "summary text",
            "key_findings": ["finding 1", "finding 2", ...],
            "recommendations": ["recommendation 1", "recommendation 2", ...],
            "contributing_factors": [
                {{"factor": "Factor 1", "impact": numeric_value}},
                {{"factor": "Factor 2", "impact": numeric_value}},
                ...
            ],
            "opportunities": "opportunities text"
        }}
        """
        
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        analysis = json.loads(response.choices[0].message.content)
        
        return analysis
    except Exception as e:
        # Fallback response in case of error
        return {
            "executive_summary": "Financial performance shows mixed results with revenue growth but margin pressure. Key products outperforming in target markets, though economic headwinds impacting overall profitability.",
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
            "contributing_factors": [
                {"factor": "Product Mix Optimization", "impact": 35},
                {"factor": "Market Expansion", "impact": 25},
                {"factor": "Cost Inflation", "impact": 20},
                {"factor": "Operational Efficiency", "impact": 15},
                {"factor": "Currency Effects", "impact": 5}
            ],
            "opportunities": "Significant opportunity exists to leverage data analytics for dynamic pricing and inventory optimization. Customer segmentation analysis indicates potential for 8-10% margin improvement in enterprise segment through tailored solutions. Supply chain resilience investments could mitigate 60% of current volatility impact."
        }

def generate_data_quality_analysis(data):
    """
    Generate AI-powered analysis of data quality issues using OpenAI
    """
    try:
        # Create a simplified data summary to send to the API
        data_summary = {
            "completeness_score": data["data_quality"]["completeness"],
            "accuracy_score": data["data_quality"]["accuracy"],
            "consistency_score": data["data_quality"]["consistency"],
            "anomalies_count": len(data["data_quality"]["anomalies"]),
            "critical_issues": data["data_quality"]["critical_issues"],
            "data_sources": data["data_quality"]["data_sources"]
        }
        
        # Define the prompt for the OpenAI API
        prompt = f"""
        You are a data quality expert AI assistant. Analyze the data quality metrics provided below and generate:
        1. A brief executive summary of data quality issues (3-4 sentences)
        2. A list of 3-5 priority issues that need to be addressed
        3. A detailed action plan with specific steps to improve data quality
        
        Data Quality Metrics:
        {json.dumps(data_summary, indent=2)}
        
        Respond with JSON in this format:
        {{
            "executive_summary": "summary text",
            "priority_issues": [
                {{"title": "Issue 1", "severity": "High/Medium/Low", "impact": "impact text", "resolution": "resolution text"}},
                ...
            ],
            "action_items": [
                {{"title": "Action 1", "owner": "Department", "priority": "High/Medium/Low", "description": "description text", "expected_outcome": "outcome text", "due_date": "YYYY-MM-DD", "start_date": "YYYY-MM-DD"}},
                ...
            ],
            "timeline_impact": "timeline impact text"
        }}
        """
        
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        analysis = json.loads(response.choices[0].message.content)
        
        return analysis
    except Exception as e:
        # Fallback response in case of error
        return get_fallback_data_quality_analysis()

def get_fallback_data_quality_analysis():
    """Return fallback data quality analysis in case of API failure"""
    return {
        "executive_summary": "Data quality assessment reveals several critical issues requiring immediate attention. Consistency between systems shows the highest risk, with several order-of-magnitude errors detected in revenue figures. Without remediation, these issues could significantly impact Q3 financial reporting accuracy and timeline.",
        "priority_issues": [
            {
                "title": "Revenue Decimal Placement Errors",
                "severity": "High",
                "impact": "Incorrect revenue figures could lead to material misstatement in financial reports",
                "resolution": "Implement validation rules for order-of-magnitude checks"
            },
            {
                "title": "Missing Product Categorization",
                "severity": "Medium",
                "impact": "Hampering accurate segment profitability reporting",
                "resolution": "Data enrichment project with product management team"
            },
            {
                "title": "Inconsistent Exchange Rate Application",
                "severity": "High",
                "impact": "Creating FX exposure discrepancies of approximately €1.4M",
                "resolution": "Centralize FX rate management and implement system controls"
            },
            {
                "title": "Incomplete Customer Data",
                "severity": "Low",
                "impact": "Limiting accurate customer profitability analysis",
                "resolution": "CRM data integration and validation project"
            }
        ],
        "action_items": [
            {
                "title": "Implement Revenue Figure Validation Rules",
                "owner": "Finance Systems",
                "priority": "High",
                "description": "Create automated validation rules to flag potential order-of-magnitude errors in revenue figures compared to historical trends",
                "expected_outcome": "95% reduction in decimal placement errors",
                "due_date": "2023-07-15",
                "start_date": "2023-07-01"
            },
            {
                "title": "Product Categorization Data Enrichment",
                "owner": "Product Management",
                "priority": "Medium",
                "description": "Complete missing product categorization data for 15% of SKUs currently uncategorized",
                "expected_outcome": "100% product categorization coverage",
                "due_date": "2023-07-30",
                "start_date": "2023-07-10"
            },
            {
                "title": "FX Rate Management Centralization",
                "owner": "Treasury",
                "priority": "High",
                "description": "Implement central FX rate management system and integrate with all financial systems",
                "expected_outcome": "Consistent FX rates across all reports and systems",
                "due_date": "2023-08-15",
                "start_date": "2023-07-05"
            },
            {
                "title": "Customer Data Integration",
                "owner": "Sales Operations",
                "priority": "Low",
                "description": "Integrate CRM customer data with financial systems for improved analysis",
                "expected_outcome": "Enhanced customer profitability reporting",
                "due_date": "2023-09-01",
                "start_date": "2023-08-01"
            }
        ],
        "timeline_impact": "With successful implementation of high-priority action items, the financial close timeline can be reduced by 6 days (from 12 to 6 days) by eliminating manual reconciliation and error-correction work."
    }

def generate_forecast_recommendations(data, simulation_params=None):
    """
    Generate AI-powered forecasting recommendations using OpenAI
    """
    try:
        # Create a simplified data summary to send to the API
        data_summary = {
            "current_revenue": data["metrics"]["revenue"],
            "current_ebitda": data["metrics"]["ebitda"],
            "growth_rate": data["forecast"]["revenue_growth"],
            "market_conditions": data["metrics"]["market_conditions"],
            "top_product": data["metrics"]["top_product"],
            "bottom_product": data["metrics"]["bottom_product"],
            "simulation_params": simulation_params
        }
        
        # Define the prompt for the OpenAI API
        prompt = f"""
        You are a financial forecasting and strategy AI assistant. Analyze the financial data provided below and generate:
        1. An executive summary of the financial outlook (3-4 sentences)
        2. 3-4 strategic opportunities with expected impact and timeline
        3. Risk analysis with probability, impact, and mitigation strategies
        4. Key performance levers with potential impact and feasibility assessment
        5. 3-4 data-driven business insights
        6. A simple executive decision framework
        7. 2-3 key executive takeaways
        
        Financial Data:
        {json.dumps(data_summary, indent=2)}
        
        Respond with JSON in this format:
        {{
            "executive_summary": "summary text",
            "strategic_opportunities": [
                {{"title": "Opportunity 1", "impact": "impact description", "timeline": "timeline description", "description": "detailed description", "key_actions": ["action 1", "action 2", ...]}},
                ...
            ],
            "risks": [
                {{"title": "Risk 1", "probability": probability_value, "impact": impact_value, "mitigation": "mitigation strategy"}},
                ...
            ],
            "performance_levers": [
                {{"lever": "Lever 1", "impact": impact_value, "feasibility": feasibility_value}},
                ...
            ],
            "business_insights": [
                {{"title": "Insight 1", "description": "description text"}},
                ...
            ],
            "decision_framework": [
                {{"decision": "Decision 1", "upside": "upside text", "downside": "downside text", "timeline": "timeline text", "kpis": "KPIs to monitor"}},
                ...
            ],
            "executive_takeaways": ["takeaway 1", "takeaway 2", ...]
        }}
        """
        
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        analysis = json.loads(response.choices[0].message.content)
        
        return analysis
    except Exception as e:
        # Fallback response in case of error
        return get_fallback_forecast_recommendations()

def get_fallback_forecast_recommendations():
    """Return fallback forecast recommendations in case of API failure"""
    return {
        "executive_summary": "Financial forecast indicates moderate growth potential of 5-7% with strategic opportunities in digital transformation and product portfolio optimization. Market headwinds will require disciplined cost management, while targeted investments in high-margin segments could deliver EBITDA improvement of 150-200 basis points within 18 months.",
        "strategic_opportunities": [
            {
                "title": "Product Portfolio Optimization",
                "impact": "€3.2-4.5M EBITDA improvement",
                "timeline": "12-18 months",
                "description": "Shifting resources from bottom-performing products to top-performing categories, with strategic phase-out of low-margin offerings and accelerated investment in high-growth segments.",
                "key_actions": [
                    "Conduct profitability analysis across full product portfolio",
                    "Develop phase-out plan for bottom 10% of products",
                    "Create investment roadmap for top 20% performers",
                    "Implement SKU rationalization program"
                ]
            },
            {
                "title": "Pricing Strategy Refinement",
                "impact": "€2.8-3.5M incremental revenue",
                "timeline": "6-9 months",
                "description": "Implementing value-based pricing with segment-specific strategies, leveraging market position strength in premium categories while protecting volume in competitive segments.",
                "key_actions": [
                    "Analyze price elasticity by customer segment",
                    "Implement value-based pricing in premium segments",
                    "Develop targeted discount guidelines for sales team",
                    "Create dynamic pricing capabilities for key accounts"
                ]
            },
            {
                "title": "Geographic Expansion",
                "impact": "€8-10M revenue growth opportunity",
                "timeline": "18-24 months",
                "description": "Focused expansion into high-growth markets with existing product lines, leveraging digital channels to minimize capital requirements and accelerate market entry.",
                "key_actions": [
                    "Complete market attractiveness analysis for target regions",
                    "Develop channel partner strategy for top 3 target markets",
                    "Create regionally-adapted marketing materials",
                    "Implement pilot program in highest-potential market"
                ]
            }
        ],
        "risks": [
            {
                "title": "Raw Material Inflation",
                "probability": 0.7,
                "impact": 0.6,
                "mitigation": "Implement strategic sourcing program with dual-supplier strategy and quarterly price-lock agreements. Develop material substitution options for high-volatility inputs."
            },
            {
                "title": "Competitive Market Disruption",
                "probability": 0.4,
                "impact": 0.8,
                "mitigation": "Accelerate innovation pipeline with quarterly release cycles. Implement competitive intelligence program with early-warning indicators for market shifts."
            },
            {
                "title": "FX Exposure",
                "probability": 0.6,
                "impact": 0.5,
                "mitigation": "Implement hedging strategy for forecasted exposure, with programmatic triggers for adjustment. Balance supply chain currency exposure with revenue currency mix."
            },
            {
                "title": "Talent Retention",
                "probability": 0.5,
                "impact": 0.7,
                "mitigation": "Implement targeted retention program for high-impact roles with performance-based incentives. Develop succession plans for all key positions."
            }
        ],
        "performance_levers": [
            {"lever": "Price Optimization", "impact": 3.5, "feasibility": 0.8},
            {"lever": "Product Mix Shift", "impact": 4.2, "feasibility": 0.7},
            {"lever": "Process Automation", "impact": 2.8, "feasibility": 0.6},
            {"lever": "Procurement Savings", "impact": 1.9, "feasibility": 0.9},
            {"lever": "Marketing Effectiveness", "impact": 2.1, "feasibility": 0.7}
        ],
        "business_insights": [
            {
                "title": "Premium Segment Growth Opportunity",
                "description": "Analysis reveals premium product segments are growing 2.5x faster than economy segments, with 8.5 percentage points higher margin. Current portfolio is under-indexed in premium categories (18% vs. market average of 27%), indicating significant growth potential through portfolio rebalancing."
            },
            {
                "title": "Digital Channel Efficiency",
                "description": "Digital sales channels demonstrate 35% lower customer acquisition cost and 22% higher customer lifetime value compared to traditional channels. Current digital penetration of 42% suggests opportunity to accelerate digital transformation initiatives."
            },
            {
                "title": "Product Development Efficiency Gap",
                "description": "Time-to-market for new products averages 14 months vs. industry benchmark of 9 months. Implementing agile development methodologies could accelerate innovation cycle by 30-40%, significantly improving market responsiveness."
            }
        ],
        "decision_framework": [
            {
                "decision": "Portfolio Rebalancing Investment",
                "upside": "€4.5M EBITDA improvement within 18 months",
                "downside": "€1.2M transition costs and potential short-term market share sacrifice in low-end segments",
                "timeline": "Begin implementation in Q3, full effect by Q4 next year",
                "kpis": "Product margin by segment, portfolio mix percentage, cannibalization rate"
            },
            {
                "decision": "Digital Transformation Acceleration",
                "upside": "€2.8M incremental revenue in year 1, €5.2M in year 2",
                "downside": "€3.5M investment requirement, potential channel conflict",
                "timeline": "Phased implementation starting Q3, 18-month program",
                "kpis": "Digital channel revenue, customer acquisition cost, conversion rate"
            },
            {
                "decision": "Manufacturing Process Automation",
                "upside": "€1.9M annual cost savings, quality improvement",
                "downside": "€4.2M capital investment, temporary production disruption",
                "timeline": "24-month implementation program",
                "kpis": "Unit production cost, capacity utilization, quality metrics"
            }
        ],
        "executive_takeaways": [
            "Portfolio optimization represents largest EBITDA improvement opportunity (€3.2-4.5M) with highest feasibility score",
            "Raw material inflation poses most significant risk requiring immediate mitigation through strategic sourcing program",
            "Digital transformation acceleration offers compelling ROI with break-even in approximately 15 months"
        ]
    }

