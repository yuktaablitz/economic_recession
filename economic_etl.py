from fred import unemployment_df, interest_df
from worldbank import gdp_df, inflation_df
from pymongo import MongoClient
import pandas as pd

def main():
    # === Connect to MongoDB ===
    client = MongoClient("mongodb://localhost:27017/")
    db = client["econ_data"]
    yearly_collection = db["yearly_reports"]

    # === Clean & Prepare ===
    gdp_df['year'] = gdp_df['year'].astype(int)
    inflation_df['year'] = inflation_df['year'].astype(int)
    unemployment_df['year'] = pd.to_datetime(unemployment_df['date']).dt.year
    interest_df['year'] = pd.to_datetime(interest_df['date']).dt.year

    # === Group by Year (Average) ===
    unemployment_avg = unemployment_df.groupby('year')['unemployment'].mean().reset_index()
    interest_avg = interest_df.groupby('year')['interest_rate'].mean().reset_index()

    # === Merge All ===
    merged = gdp_df.merge(inflation_df, on='year', suffixes=('_gdp', '_inflation'))
    merged = merged.merge(unemployment_avg, on='year')
    merged = merged.merge(interest_avg, on='year')

    # === Format for Mongo ===
    docs = []
    for _, row in merged.iterrows():
        doc = {
            "year": int(row['year']),
            "indicators": {
                "gdp_growth": row['value_gdp'],
                "inflation_rate": row['value_inflation'],
                "unemployment": row['unemployment'],
                "interest_rate": row['interest_rate']
            },
            "source": ["World Bank", "FRED"]
        }
        docs.append(doc)

    # === Load to MongoDB ===
    yearly_collection.delete_many({})
    yearly_collection.insert_many(docs)
    print(f"✅ Inserted {len(docs)} economic records.")
