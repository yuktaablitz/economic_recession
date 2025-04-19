import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

# --- Set page config ---
st.set_page_config(page_title="PostgreSQL OLAP Dashboard", layout="wide")
st.title("🧮 OLAP Insights from PostgreSQL")

# --- PostgreSQL connection ---
conn = psycopg2.connect(
    dbname="econ_db",
    user="econ_user",
    password="econpass",
    host="localhost",
    port="5432"
)

# --- Define OLAP Queries ---
queries = {
    "Avg GDP Growth by Decade": """
        SELECT t.decade, ROUND(AVG(f.gdp_growth)::numeric, 2) AS avg_gdp_growth
        FROM fact_economic_summary f
        JOIN dim_time t ON f.year = t.year
        GROUP BY t.decade
        ORDER BY t.decade;
    """,

    "Unemployment & Inflation in Recession Years": """
        SELECT f.year, f.unemployment, f.inflation_rate
        FROM fact_economic_summary f
        JOIN dim_time t ON f.year = t.year
        WHERE t.recession_flag = TRUE
        ORDER BY f.year;
    """,

    "Sentiment vs GDP Growth": """
        SELECT f.year, f.avg_sentiment_score, f.gdp_growth
        FROM fact_economic_summary f
        ORDER BY f.year;
    """,

    "Interest Rate Trends by Decade": """
        SELECT t.decade, ROUND(AVG(f.interest_rate)::numeric, 2) AS avg_interest
        FROM fact_economic_summary f
        JOIN dim_time t ON f.year = t.year
        GROUP BY t.decade
        ORDER BY t.decade;
    """,

    "Recent 5-Year Economic Summary": """
        SELECT * FROM fact_economic_summary
        ORDER BY year DESC
        LIMIT 5;
    """
}

# --- Dropdown to choose query ---
selected_query = st.selectbox("Choose an OLAP Analysis", list(queries.keys()))
query = queries[selected_query]

# --- Execute and show result ---
df = pd.read_sql_query(query, conn)
st.dataframe(df, use_container_width=True)

# --- Charting for selected queries ---
if "gdp_growth" in df.columns and "avg_sentiment_score" in df.columns:
    st.subheader("📈 Sentiment vs GDP Growth")
    st.line_chart(df.set_index("year")[["avg_sentiment_score", "gdp_growth"]])

elif "decade" in df.columns:
    st.subheader(f"📊 {selected_query}")
    st.bar_chart(df.set_index("decade"))

elif "year" in df.columns:
    st.subheader(f"📉 {selected_query}")
    st.line_chart(df.set_index("year"))

# --- Download option ---
st.download_button(
    label="📥 Download CSV",
    data=df.to_csv(index=False),
    file_name="olap_output.csv",
    mime="text/csv"
)

conn.close()
