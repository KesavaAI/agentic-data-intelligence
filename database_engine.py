"""
Module: database_engine.py
Role: Custom Data Engine Tier Abstraction
Design Pattern: Read-Only Abstract Parameter Filter (AST Processor)
Security Model: Zero Raw SQL Exposure - Parameter-Bound Data Extraction Only
Optimized: Compound Filter Processing to Support Multi-Value Target Rules
"""

import os
import logging
from collections import defaultdict  # Added for multi-value grouping rules
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configure Enterprise-grade logging for administrative visibility
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ABB_Data_Engine")

def generate_abb_dataset(records: int = 1250):
    """
    Utility Function: Seeds and generates a synthetic industrial dataset
    mimicking ABB's corporate business architecture and regional sales distribution.
    Exports cleanly to a local Excel file for staging.
    """
    np.random.seed(42) # Establish deterministic baseline for data reproducibility
    
    # Structural Mapping of Corporate Business Segments and underlying product lines
    business_segments = {
        "Electrification": ["Smart Switchgear", "Distribution Transformers", "Circuit Breakers", "EV Charging Stations"],
        "Motion": ["Industrial AC Drives", "Synchronous Motors", "Softstarters", "Generators"],
        "Process Automation": ["Distributed Control Systems (DCS)", "Measurement Analytics", "Turbochargers"],
        "Robotics & Discrete Automation": ["Articulated Industrial Robots", "Paint Robots", "FlexPicker Delta Robots"]
    }
    
    regions = ["North India", "South India", "West India", "East India"]
    client_industries = ["Automotive", "Data Centers", "Pharmaceuticals", "Cement & Steel", "Power Utilities", "Water Treatment"]
    
    start_date = datetime(2023, 1, 1)
    data = []
    
    # Loop to generate randomized, realistic industrial transactions
    for i in range(records):
        seg = np.random.choice(list(business_segments.keys()))
        prod = np.random.choice(business_segments[seg])
        reg = np.random.choice(regions)
        ind = np.random.choice(client_industries)
        
        # Calculate random temporal offsets spanning ~3 years
        days_offset = np.random.randint(0, 1100)
        txn_date = start_date + timedelta(days=days_offset)
        
        units = int(np.random.randint(1, 15))
        unit_price = float(np.random.randint(50000, 750000))
        revenue = units * unit_price
        
        # Calculate localized corporate investments against gross transaction value
        investment_pct = np.random.uniform(0.4, 0.75)
        company_investment = revenue * investment_pct
        
        # Construct row matrix mapping exactly to the system's database schema
        data.append({
            "Transaction_ID": f"ABB-{100000 + i}",
            "Date": txn_date.strftime("%Y-%m-%d"),
            "Year": txn_date.year,
            "Business_Line": seg,
            "Product_Category": prod,
            "Region": reg,
            "Client_Industry": ind,
            "Units_Sold": units,
            "Revenue_INR": round(revenue, 2),
            "Company_Investment_INR": round(company_investment, 2)
        })
        
    df = pd.DataFrame(data)
    df.to_excel("abb_sales_data.xlsx", index=False)
    logger.info(f"📦 Step 1 Complete: 'abb_sales_data.xlsx' verified with {len(df)} rows.")

class ABBDataEngine:
    """
    Core Class: Implements the safe, read-only analytical interface layer.
    Parses and translates Whitelist-Approved JSON parameters into explicit Pandas filters.
    """
    def __init__(self, file_path: str = "abb_sales_data.xlsx"):
        # Mount the file store; if missing, automatically trigger the pipeline generator
        try:
            self.df = pd.read_excel(file_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            logger.info("Successfully mounted target staging sales dataset.")
        except Exception as e:
            logger.warning(f"Target staging asset missing, running generator: {e}")
            generate_abb_dataset()
            self.df = pd.read_excel(file_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Inject computed metrics needed by executive leadership dashboards
        self._inject_analytical_features()

    def _inject_analytical_features(self):
        """
        Private Helper: Extends the data matrix with synthetic financial metrics
        and explicit temporal/performance classification categories.
        """
        if self.df.empty:
            return
        
        # Calculate structural Investment Efficiency Ratios safely (guarding against zero-division)
        self.df['Investment_Efficiency_Ratio'] = self.df['Revenue_INR'] / self.df['Company_Investment_INR'].replace(0, 1)
        
        # Calculate gross operating margins to establish categorical corporate performance tiers
        margin_pct = (self.df['Revenue_INR'] - self.df['Company_Investment_INR']) / self.df['Company_Investment_INR'].replace(0, 1)
        self.df['Performance_Tier'] = 'Low Margin'
        self.df.loc[margin_pct >= 0.40, 'Performance_Tier'] = 'Standard'
        self.df.loc[margin_pct > 0.60, 'Performance_Tier'] = 'High Margin'
        
        # Inject standard short-string month columns for clean UI timeline grouping
        self.df['Month_Str'] = self.df['Date'].dt.strftime('%b')

    def safely_filter_data(self, filter_rules: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Security Enforcement Engine: Evaluates a collection of schema-constrained JSON AST rules.
        Optimized to dynamically bundle equality rules targeting the same structural dimensions 
        into logical vector matching checks rather than recursive drops.
        """
        working_df = self.df.copy()
        if not filter_rules:
            return working_df
            
        # 1. Map rules to a relational dictionary to evaluate compound operations
        grouped_rules = defaultdict(list)
        for rule in filter_rules:
            if rule.get("column"):
                grouped_rules[rule["column"]].append(rule)
                
        # 2. Iterate through isolated column parameter vectors
        for col, rules in grouped_rules.items():
            if col not in working_df.columns:
                continue
                
            # Isolate all standard matching check items ('==') for the active targeted dimension
            equality_vals = [r.get("value") for r in rules if r.get("operator") == "==" and r.get("value") is not None]
            
            # If multiple matching targets hit the same dimension, process as an aggregate logical OR
            if len(equality_vals) > 1:
                try:
                    sanitized_vals = []
                    for v in equality_vals:
                        s_val = str(v).strip()
                        if col == "Year":
                            sanitized_vals.append(int(float(s_val)))
                        elif pd.api.types.is_numeric_dtype(working_df[col]):
                            sanitized_vals.append(float(s_val))
                        else:
                            sanitized_vals.append(s_val.lower())
                            
                    logger.info(f"Applying compound operational rule: Enforcing {col} IN {sanitized_vals}")
                    
                    # Apply modern vectorized membership filtering (.isin)
                    if pd.api.types.is_string_dtype(working_df[col]):
                        working_df = working_df[working_df[col].astype(str).str.lower().isin(sanitized_vals)]
                    else:
                        working_df = working_df[working_df[col].isin(sanitized_vals)]
                        
                    # Filter down rules remaining for this column block to evaluate bounding parameters (<, >, etc)
                    rules = [r for r in rules if r.get("operator") != "=="]
                except (ValueError, TypeError) as err:
                    logger.error(f"Compound rule processing exception caught: {err}")
                    return pd.DataFrame(columns=self.df.columns)
            
            # 3. Fall back to clean sequential processing for standalone boundary rules
            for rule in rules:
                op = rule.get("operator")
                val = rule.get("value")
                if val is None:
                    continue
                    
                try:
                    sanitized_val = str(val).strip()
                    
                    # Force strict data-type casting based on structural schema rules
                    if col == "Year":
                        val = int(float(sanitized_val))
                    elif pd.api.types.is_numeric_dtype(working_df[col]):
                        val = float(sanitized_val)
                    
                    logger.info(f"Applying operational rule: Enforcing {col} {op} {val}")
                    
                    # Map JSON operators to native Pandas logical indices safely
                    if op == "==":
                        if isinstance(val, str):
                            working_df = working_df[working_df[col].astype(str).str.lower() == val.lower().strip()]
                        else:
                            working_df = working_df[working_df[col] == val]
                    elif op == "!=": working_df = working_df[working_df[col] != val]
                    elif op == ">": working_df = working_df[working_df[col] > val]
                    elif op == "<": working_df = working_df[working_df[col] < val]
                    elif op == ">=": working_df = working_df[working_df[col] >= val]
                    elif op == "<=": working_df = working_df[working_df[col] <= val]
                except (ValueError, TypeError) as err:
                    logger.error(f"Rule processing exception caught: {err}")
                    # Security Fallback: Instantly return an empty DataFrame if a payload tries to drop types
                    return pd.DataFrame(columns=self.df.columns)
                    
        return working_df

def execute_secure_json_filter(where_clauses: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Global Functional Pipeline Gate: Initializes a runtime data engine session
    and extracts parameter-bound records safely.
    """
    engine = ABBDataEngine()
    return engine.safely_filter_data(where_clauses)