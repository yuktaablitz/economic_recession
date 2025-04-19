import psycopg2
import pandas as pd
from pymongo import MongoClient

# === MongoDB Connection ===
client = MongoClient("mongodb://localhost:27017/")
db = client["econ_data"]
sentiment_collection = db["sentiment_news"]
indicators_collection = db["yearly_reports"]

# === Load data from MongoDB ===
sentiment_df = pd.DataFrame(list(sentiment_collection.find()))
econ_df = pd.DataFrame(list(indicators_collection.find()))

# === Preprocess sentiment ===
sentiment_df['published_date'] = pd.to_datetime(sentiment_df['published_date'])
sentiment_df['year'] = sentiment_df['published_date'].dt.year
sentiment_yearly = sentiment_df.groupby('year')['sentiment_score'].mean().reset_index()

# === Preprocess economic indicators ===
indicators = pd.json_normalize(econ_df['indicators'])
econ_df = pd.concat([econ_df['year'], indicators], axis=1)

# === Merge and clean ===
merged_df = pd.merge(sentiment_yearly, econ_df, on='year', how='inner')
merged_df = merged_df.dropna(subset=['gdp_growth', 'inflation_rate', 'unemployment', 'interest_rate'])

# === PostgreSQL Connection ===
conn = psycopg2.connect(
    dbname="econ_db",
    user="econ_user",
    password="econpass",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# === Insert into dim_time and fact_economic_summary ===
for _, row in merged_df.iterrows():
    year = int(row['year'])
    decade = f"{str(year)[:3]}0s"
    recession_flag = bool(row['unemployment'] > 6 or row['gdp_growth'] < 0)

    # Insert into dim_time
    cur.execute("""
        INSERT INTO dim_time (year, decade, recession_flag)
        VALUES (%s, %s, %s)
        ON CONFLICT (year) DO NOTHING
    """, (year, decade, recession_flag))

    # Insert into fact table
    cur.execute("""
        INSERT INTO fact_economic_summary (
            year, gdp_growth, inflation_rate, unemployment, interest_rate, avg_sentiment_score
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        year,
        float(row['gdp_growth']),
        float(row['inflation_rate']),
        float(row['unemployment']),
        float(row['interest_rate']),
        float(row['sentiment_score'])
    ))

conn.commit()
cur.close()
conn.close()

print("✅ Data successfully loaded to PostgreSQL.")
