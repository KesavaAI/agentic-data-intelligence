import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_abb_dataset(records=1250):
    np.random.seed(42)
    
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
    print(f"📦 Step 1 Complete: 'abb_sales_data.xlsx' created with {len(df)} rows.")

if __name__ == "__main__":
    generate_abb_dataset()