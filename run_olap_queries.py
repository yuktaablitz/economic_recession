import psycopg2
import pandas as pd
from config import PG_PARAMS

# Connect to PostgreSQL
conn = psycopg2.connect(**PG_PARAMS)

# === OLAP Query 1: Average GDP by Decade ===
print("\n🔹 Avg GDP by Decade 🔹")
query = """
    SELECT t.decade, ROUND(AVG(f.gdp_growth)::numeric, 2) AS avg_gdp_growth
    FROM fact_economic_summary f
    JOIN dim_time t ON f.year = t.year
    GROUP BY t.decade
    ORDER BY t.decade;
"""
df = pd.read_sql(query, conn)
print(df)

# === OLAP Query 2: Recession Years Summary ===
print("\nc Recession Year Snapshot 🔹")
query2 = """
    SELECT f.year, f.gdp_growth, f.unemployment, f.avg_sentiment_score
    FROM fact_economic_summary f
    JOIN dim_time t ON f.year = t.year
    WHERE t.recession_flag = TRUE
    ORDER BY f.year;
"""
df2 = pd.read_sql(query2, conn)
print(df2)

print("\n🔹Top 5 Years with Worst Sentiment 🔹")
query3= """SELECT year, avg_sentiment_score
FROM fact_economic_summary
ORDER BY avg_sentiment_score ASC
LIMIT 5; """

df3= pd.read_sql(query3, conn)
print(df3)

print("\n🔹Year-over-Year GDP vs Sentiment Trend 🔹")
query4= """SELECT year, gdp_growth, avg_sentiment_score
FROM fact_economic_summary
ORDER BY year;
"""

df4= pd.read_sql(query4, conn)
print(df4)

print("\n🔹High Unemployment & Negative Sentiment🔹")
query5= """SELECT year, unemployment, avg_sentiment_score
FROM fact_economic_summary
WHERE unemployment > 6 AND avg_sentiment_score < 0
ORDER BY year;
 """

df5= pd.read_sql(query5, conn)
print(df5)

print("\n🔹Decade-wise Recession Flag Count🔹")
query6= """SELECT decade, COUNT(*) AS recession_years
FROM dim_time
WHERE recession_flag = TRUE
GROUP BY decade
ORDER BY decade;
 """

df6= pd.read_sql(query6, conn)
print(df6)

conn.close()
