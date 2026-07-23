"""
Module: database_engine.py
Role: Custom Data Engine Tier Abstraction
Design Pattern: Read-Only Abstract Parameter Filter (AST Processor)
Security Model: Zero Raw SQL Exposure - Parameter-Bound Data Extraction Only
Optimized: Type-Safe AST Evaluator for Temporal Arrays & Numeric Coercion
"""

import os
import re
import logging
from collections import defaultdict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configure logging for administrative visibility
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ABB_Data_Engine")

def generate_abb_dataset(records: int = 1250):
    """
    Utility Function: Seeds and generates a synthetic industrial dataset
    mimicking ABB's corporate business architecture and regional sales distribution.
    Exports cleanly to a local Excel file for staging.
    """
    np.random.seed(42)  # Establish deterministic baseline for reproducibility
    
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
    
    for i in range(records):
        seg = np.random.choice(list(business_segments.keys()))
        prod = np.random.choice(business_segments[seg])
        reg = np.random.choice(regions)
        ind = np.random.choice(client_industries)
        
        days_offset = np.random.randint(0, 1100)
        txn_date = start_date + timedelta(days=days_offset)
        
        units = int(np.random.randint(1, 15))
        unit_price = float(np.random.randint(50000, 750000))
        revenue = units * unit_price
        
        investment_pct = np.random.uniform(0.4, 0.75)
        company_investment = revenue * investment_pct
        
        data.append({
            "Transaction_ID": f"ABB-{100000 + i}",
            "Date": txn_date.strftime("%Y-%m-%d"),
            "Year": int(txn_date.year),
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
        try:
            self.df = pd.read_excel(file_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce').fillna(0).astype(int)
            logger.info("Successfully mounted target staging sales dataset.")
        except Exception as e:
            logger.warning(f"Target staging asset missing, running generator: {e}")
            generate_abb_dataset()
            self.df = pd.read_excel(file_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce').fillna(0).astype(int)
        
        self._inject_analytical_features()

    def _inject_analytical_features(self):
        """Private Helper: Extends the data matrix with synthetic financial metrics."""
        if self.df.empty:
            return
        
        self.df['Investment_Efficiency_Ratio'] = self.df['Revenue_INR'] / self.df['Company_Investment_INR'].replace(0, 1)
        margin_pct = (self.df['Revenue_INR'] - self.df['Company_Investment_INR']) / self.df['Company_Investment_INR'].replace(0, 1)
        self.df['Performance_Tier'] = 'Low Margin'
        self.df.loc[margin_pct >= 0.40, 'Performance_Tier'] = 'Standard'
        self.df.loc[margin_pct > 0.60, 'Performance_Tier'] = 'High Margin'
        self.df['Month_Str'] = self.df['Date'].dt.strftime('%b')

    def safely_filter_data(self, filter_rules: List[Dict[str, Any]]) -> pd.DataFrame:
        """Type-safe, non-destructive AST filter processor for Pandas backend."""
        working_df = self.df.copy()
        if not filter_rules:
            return working_df

        col_map = {c.lower(): c for c in working_df.columns}

        for rule in filter_rules:
            raw_col = rule.get("column", "")
            if not raw_col or raw_col.lower() not in col_map:
                continue

            actual_col = col_map[raw_col.lower()]
            op = str(rule.get("operator", "==")).lower().strip()
            val = rule.get("value")

            if val is None:
                continue

            logger.info(f"🔍 Evaluated Rule -> Col: '{actual_col}', Op: '{op}', Val: {val}")

            # Special Type Coercion for Temporal Filters (Year)
            if actual_col.lower() == "year":
                extracted_years = []
                if isinstance(val, (list, tuple, set)):
                    for v in val:
                        matches = re.findall(r'\b\d{4}\b', str(v))
                        extracted_years.extend([int(m) for m in matches])
                elif isinstance(val, (int, float)):
                    extracted_years = [int(val)]
                else:
                    matches = re.findall(r'\b\d{4}\b', str(val))
                    extracted_years = [int(m) for m in matches]

                if extracted_years:
                    logger.info(f"✅ Extracted Year Target Array: {extracted_years}")
                    working_df[actual_col] = pd.to_numeric(working_df[actual_col], errors='coerce').fillna(0).astype(int)
                    working_df = working_df[working_df[actual_col].isin(extracted_years)]
                    continue

            # Standard Categorical/Numeric Filtering
            if isinstance(val, list) or op in ["in", "contains", "between"]:
                val_list = [str(v).strip().lower() for v in (val if isinstance(val, list) else str(val).split(","))]
                working_df = working_df[working_df[actual_col].astype(str).str.lower().isin(val_list)]
            elif op in ["==", "=", "eq"]:
                working_df = working_df[working_df[actual_col].astype(str).str.lower() == str(val).lower().strip()]
            elif op in ["!=", "neq"]:
                working_df = working_df[working_df[actual_col].astype(str).str.lower() != str(val).lower().strip()]
            elif op in [">", "gt"]:
                working_df = working_df[pd.to_numeric(working_df[actual_col], errors='coerce') > float(val)]
            elif op in ["<", "lt"]:
                working_df = working_df[pd.to_numeric(working_df[actual_col], errors='coerce') < float(val)]
            elif op in [">=", "gte"]:
                working_df = working_df[pd.to_numeric(working_df[actual_col], errors='coerce') >= float(val)]
            elif op in ["<=", "lte"]:
                working_df = working_df[pd.to_numeric(working_df[actual_col], errors='coerce') <= float(val)]

        return working_df

def execute_secure_json_filter(where_clauses: List[Dict[str, Any]]) -> pd.DataFrame:
    """Global Functional Pipeline Gate."""
    engine = ABBDataEngine()
    return engine.safely_filter_data(where_clauses)


# ==============================================================================
# OPTIONAL ENTERPRISE EXTENSION: LIVE DATABASE INGESTION PATTERN
# ==============================================================================
# The default engine operates on an in-memory Pandas DataFrame loaded from static
# files (abb_sales_data.xlsx) to guarantee zero SQL injection exposure. 
#
# To connect to live relational databases (e.g., PostgreSQL, Snowflake, Redshift),
# you can swap out static loading by assigning the database output directly to `self.df`:
#
# ```python
# import os
# from sqlalchemy import create_engine
#
# def _load_from_live_database(self) -> pd.DataFrame:
#     """
#     Fetches records safely from a enterprise database and loads into self.df.
#     The AST filter layer continues to operate in-memory on `self.df`.
#     """
#     db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/abb_analytics")
#     engine = create_engine(db_url)
#     
#     # Store query output directly into self.df for AST evaluation
#     query = "SELECT * FROM sales_transactions;"
#     return pd.read_sql(query, con=engine)
# ```
# ==============================================================================