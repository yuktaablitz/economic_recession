# load_to_mongo.py

from pymongo import MongoClient
import pandas as pd

# Import the dataframes directly from other scripts
from fred import unemployment_df, interest_df
from worldbank import gdp_df, inflation_df

# === Step 1: Prepare & Clean Data ===
gdp_df['year'] = gdp_df['year'].astype(int)
inflation_df['year'] = inflation_df['year'].astype(int)
unemployment_df['year'] = pd.to_datetime(unemployment_df['date']).dt.year
interest_df['year'] = pd.to_datetime(interest_df['date']).dt.year

# Group FRED data by year (average)
unemployment_avg = unemployment_df.groupby('year')['unemployment'].mean().reset_index()
interest_avg = interest_df.groupby('year')['interest_rate'].mean().reset_index()

# === Step 2: Merge All ===
combined = gdp_df.merge(inflation_df, on='year', suffixes=('_gdp', '_inflation')) \
                 .merge(unemployment_avg, on='year') \
                 .merge(interest_avg, on='year')

# === Step 3: Load to MongoDB ===
client = MongoClient("mongodb://localhost:27017/")
db = client["econ_data"]
collection = db["yearly_reports"]
collection.delete_many({})  # Optional: clears previous entries

records = []
for _, row in combined.iterrows():
    doc = {
        "year": int(row["year"]),
        "indicators": {
            "gdp_growth": row.get("value_gdp"),
            "inflation_rate": row.get("value_inflation"),
            "unemployment": row.get("unemployment"),
            "interest_rate": row.get("interest_rate"),
        },
        "source": ["World Bank", "FRED"]
    }
    records.append(doc)

collection.insert_many(records)
print(f"✅ Inserted {len(records)} documents into MongoDB.")
