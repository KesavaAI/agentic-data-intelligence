"""
Module: agent_graph.py
Role: Cognitive Processing Layer & Adversarial Gatekeeper
Design Pattern: Deterministic State Structuring (Schema Parameter Router)
AI Model: Groq Llama-3.3-70b-Versatile
"""

import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from database_engine import execute_secure_json_filter

# Initialize context variable environment mapping configurations
load_dotenv()
logger = logging.getLogger("ABB_Agent_Graph")

def run_analytics_pipeline(natural_language_prompt: str) -> Dict[str, Any]:
    """
    End-to-End Orchestrator: Drives conversational interface text into a
    structured JSON query contract while enforcing behavioral safety guardrails.
    """
    lowered_prompt = natural_language_prompt.lower()
    
    # SYSTEM SECURITY WALL: Hard intercept against core behavioral injection strings
    if "ignore your" in lowered_prompt or "previous instructions" in lowered_prompt or "markdown injection" in lowered_prompt:
        logger.warning("🚨 Security Alert: Adversarial behavioral override prompt intercepted.")
        return {
            "status": "security_violation",
            "error_message": "System Policy Violation: Unauthorized behavioral override commands detected.",
            "data": None, "visual_plan": None, "analyst_commentary": None
        }

    try:
        # Verify access credentials for the inference layer are loaded
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable missing from active workspace config.")
            
        from groq import Groq
        client = Groq(api_key=api_key)
        
        # Rigid, structured system instructions defining analytical constraints and output parameters
        system_instruction = (
            "ROLE DEFINITION:\n"
            "You are a dual-persona system: a Lead Data Architect/Senior SQL Developer AND an Advanced Industrial Data Analyst.\n"
            "Your objective is to translate user prompts into structured JSON query parameters, visual schemes, and high-value data analytics commentary.\n\n"
            
            "AVAILABLE DATA SCHEMA:\n"
            "- Dimensions: ['Transaction_ID', 'Year', 'Business_Line', 'Product_Category', 'Region', 'Client_Industry', 'Performance_Tier', 'Month_Str']\n"
            "- Temporal Keys: ['Date']\n"
            "- Metrics: ['Units_Sold', 'Revenue_INR', 'Company_Investment_INR', 'Investment_Efficiency_Ratio']\n\n"
            
            "CRITICAL RELATIONAL & ANALYTICAL MANDATES:\n"
            "1. DETERMINISTIC AST FILTERING: Generate filter criteria inside the 'where_clauses' array. Separate compound tokens like 'Jul 2024' into explicit rules: 'Year' and 'Month_Str'.\n"
            "2. VISUALIZATION ENFORCEMENT: Track trends and trajectories over time using x='Date' and chart_type='line' or 'area'. If a user query references multiple structural dimensions in plural form (e.g., 'business lines'), you MUST set 'color' strictly to that column name.\n"
            "3. EXECUTIVE DATA ANALYST PERSONALITY: Provide an executive context summary inside 'analyst_commentary'. Address observations regarding investment efficiencies, margins, or structural shifts based on what the user asked.\n\n"
            
            "TARGET OUTPUT JSON SCHEMA:\n"
            "{\n"
            '  "where_clauses": [\n'
            '    {"column": "Year|Month_Str|Business_Line|etc", "operator": "==|!=|>|<|>=|<=", "value": "str|int|float"}\n'
            '  ],\n'
            '  "visual_plan": {\n'
            '    "chart_type": "bar|line|pie|scatter|box|histogram|treemap|sunburst|funnel|area|violin|strip|density_heatmap",\n'
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
        
        # Execute highly structured parsing request under explicit JSON formatting controls
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": natural_language_prompt}
            ],
            temperature=0.0, # Zeroed out to optimize processing determinism and block semantic drifts
            response_format={"type": "json_object"} # Hard enforcement of JSON payload emission
        )
        
        # Load output parameters safely into a memory dictionary object
        response_data = json.loads(completion.choices[0].message.content)
        logger.info("Successfully gathered structured JSON parameters contract from inference agent.")
        
        # Extract constraints and pass downstream to the parameterized execution interface
        return {
            "status": "success",
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
            "visual_plan": None, 
            "analyst_commentary": None
        }