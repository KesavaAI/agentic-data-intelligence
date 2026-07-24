"""
Module: agent_graph.py
Role: Cognitive Processing Layer & SQL Synthesizer
Design Pattern: Deterministic State Structuring (Schema Parameter Router)
AI Model: Groq Llama-3.3-70b-Versatile
"""

import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from database_engine import execute_secure_json_filter

load_dotenv()
logger = logging.getLogger("ABB_Agent_Graph")

# Keywords that trigger immediate write/mutation intercept
MUTATION_KEYWORDS = ["modify", "update", "delete", "drop", "insert", "alter", "truncate", "set revenue", "reset"]

def run_analytics_pipeline(natural_language_prompt: str) -> Dict[str, Any]:
    """
    End-to-End Orchestrator: Translates natural language into SQL code and 
    parameter-bound filters, executing the data extraction securely.
    """
    lowered_prompt = natural_language_prompt.lower()
    
    # SYSTEM SECURITY WALL: Intercept prompt injection attempts
    if any(k in lowered_prompt for k in ["ignore your", "previous instructions", "markdown injection"]):
        logger.warning("🚨 Security Alert: Adversarial prompt override intercepted.")
        return {
            "status": "security_violation",
            "error_message": "System Policy Violation: Unauthorized behavioral override commands detected.",
            "data": None, "generated_code": None, "visual_plan": None, "analyst_commentary": None
        }

    # READ-ONLY DATA PROTECTION WALL: Intercept write/modification attempts
    if any(k in lowered_prompt for k in MUTATION_KEYWORDS):
        logger.warning("🚨 Security Alert: Data modification attempt intercepted.")
        return {
            "status": "security_violation",
            "error_message": "System Policy Violation: Read-only platform. Database record modification commands are strictly prohibited.",
            "data": None, "generated_code": None, "visual_plan": None, "analyst_commentary": None
        }

    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable missing from active workspace config.")
            
        from groq import Groq
        client = Groq(api_key=api_key)
        
        system_instruction = (
            "ROLE DEFINITION:\n"
            "You are a dual-persona system: a Lead Data Architect/Senior SQL Developer AND an Advanced Industrial Data Analyst.\n"
            "Your objective is to translate user prompts into structured JSON containing clean PostgreSQL code, filter parameters, visual schemes, and analytics commentary.\n\n"
            
            "AVAILABLE DATABASE SCHEMA:\n"
            "Table Name: `abb_sales_transactions`\n"
            "- Dimensions: ['Transaction_ID', 'Year', 'Business_Line', 'Product_Category', 'Region', 'Client_Industry', 'Performance_Tier', 'Month_Str']\n"
            "- Temporal Keys: ['Date'] (Coverage: 2023 - 2026)\n"
            "- Metrics: ['Units_Sold', 'Revenue_INR', 'Company_Investment_INR', 'Investment_Efficiency_Ratio']\n\n"
            
            "CRITICAL RELATIONAL & ANALYTICAL MANDATES:\n"
            "1. STRICT READ-ONLY PLATFORM: Reject any request to modify, delete, or alter records. Never generate commentary claiming data was updated.\n"
            "2. GENERATE SQL CODE: Write a valid, read-only SQL query string inside 'generated_code' targeting table `abb_sales_transactions`.\n"
            "3. DETERMINISTIC AST FILTERING: Generate filter criteria inside 'where_clauses'. For multi-year/multi-value filters, use 'operator': 'in' with a list of values: e.g., {'column': 'Year', 'operator': 'in', 'value': [2023, 2024, 2025, 2026]}.\n"
            "4. VISUALIZATION ENFORCEMENT: Track trends over time using x='Date' and chart_type='line' or 'area'. If user explicitly requests a radar, spider, or polar chart, set 'chart_type': 'radar' (x=angular category e.g., 'Product_Category', y=radial metric e.g., 'Revenue_INR'). If a user query references multiple structural dimensions in plural form (e.g., 'business lines'), set 'color' strictly to that column name.\n"
            "5. EXECUTIVE DATA ANALYST PERSONALITY: Provide an executive context summary inside 'analyst_commentary'.\n\n"
            
            "TARGET OUTPUT JSON SCHEMA:\n"
            "{\n"
            '  "generated_code": "SELECT Region, Business_Line, SUM(Revenue_INR) AS Total_Revenue FROM abb_sales_transactions WHERE Year IN (2023, 2024, 2025, 2026) GROUP BY Region, Business_Line ORDER BY Total_Revenue DESC;",\n'
            '  "where_clauses": [\n'
            '    {"column": "Year", "operator": "in", "value": [2023, 2024, 2025, 2026]}\n'
            '  ],\n'
            '  "visual_plan": {\n'
            '    "chart_type": "bar|line|pie|scatter|box|histogram|treemap|sunburst|funnel|area|violin|strip|density_heatmap|radar|polar",\n'
            '    "x": "str",\n'
            '    "y": "str",\n'
            '    "color": "str | null",\n'
            '    "path": ["str"],\n'
            '    "title": "str"\n'
            '  },\n'
            '  "analyst_commentary": {\n'
            '    "executive_summary": "High-level summary of the domain request context.",\n'
            '    "key_metrics_to_watch": ["Metric observation point 1", "Metric observation point 2"],\n'
            '    "anomalies_to_inspect": "Potential operational anomalies or data skew to audit."\n'
            '  }\n'
            "}"
        )
        
        logger.info("Dispatching user payload contract to Llama cognitive layer.")
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": natural_language_prompt}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        response_data = json.loads(completion.choices[0].message.content)
        logger.info("Successfully gathered structured JSON parameters contract.")
        
        return {
            "status": "success",
            "generated_code": response_data.get("generated_code", "-- No SQL Query Generated"),
            "data": execute_secure_json_filter(response_data.get("where_clauses", [])),
            "visual_plan": response_data.get("visual_plan", {}),
            "analyst_commentary": response_data.get("analyst_commentary", {})
        }
        
    except Exception as e:
        logger.error(f"Execution fault encountered inside cognitive engine: {e}")
        return {
            "status": "failed", 
            "error_message": str(e), 
            "data": None, 
            "generated_code": None,
            "visual_plan": None, 
            "analyst_commentary": None
        }