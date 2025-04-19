import streamlit as st
st.set_page_config(page_title="Economic Sentiment Dashboard", layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime

# === Connect to MongoDB ===
client = MongoClient("mongodb://localhost:27017/")
db = client["econ_data"]
sentiment_collection = db["sentiment_news"]
indicators_collection = db["yearly_reports"]

# === Load Data ===
sentiment_df = pd.DataFrame(list(sentiment_collection.find()))
econ_df = pd.DataFrame(list(indicators_collection.find()))

# === Data Cleanup ===
sentiment_df['published_date'] = pd.to_datetime(sentiment_df['published_date'])
sentiment_df['year'] = sentiment_df['published_date'].dt.year
sentiment_yearly = sentiment_df.groupby('year')['sentiment_score'].mean().reset_index()

indicators = pd.json_normalize(econ_df['indicators'])
econ_df = pd.concat([econ_df['year'], indicators], axis=1)


st.write("Sentiment yearly shape:", sentiment_yearly.shape)
st.write("Economic indicators shape:", econ_df.shape)


merged_df = pd.merge(sentiment_yearly, econ_df, on='year', how='inner')
merged_df = merged_df[pd.to_numeric(merged_df['year'], errors='coerce').notna()]
merged_df['year'] = merged_df['year'].astype(int)

# Handle case where year is still empty
if merged_df['year'].isnull().all():
    st.error("No valid year data found. Please check the source collections.")
    st.stop()

# === Streamlit Dashboard ===
st.title("📊 Economic Sentiment Dashboard")
st.markdown("Use this tool to explore how public sentiment aligns with economic indicators over time.")

# === Tabs ===
tabs = st.tabs(["📈 Sentiment Trends", "📉 OLAP Comparisons", "🧠 Composite Insight"])

# === Tab 1: Sentiment Trends ===
with tabs[0]:
    st.subheader("Sentiment vs Economic Indicators")
    metric = st.selectbox("Choose an Indicator", ["inflation_rate", "gdp_growth", "unemployment", "interest_rate"])

    fig, ax = plt.subplots()
    ax.plot(merged_df['year'], merged_df['sentiment_score'], label='Sentiment Score', marker='o')
    ax.plot(merged_df['year'], merged_df[metric], label=metric.replace('_', ' ').title(), marker='s')
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.set_title(f"Sentiment vs {metric.replace('_', ' ').title()}")
    ax.legend()
    st.pyplot(fig)

    st.info("""
        *Sentiment Score*: Average polarity of financial headlines (-1 to +1).
        *Economic Indicators*: Extracted from World Bank & FRED.
    """)

# === Tab 2: OLAP Comparisons ===
with tabs[1]:
    st.subheader("Compare Across Multiple Indicators")

    if len(merged_df['year'].dropna()) == 0:
        st.warning("Year column is empty or invalid. Check input data.")
    else:
        year_min = int(merged_df['year'].min())
        year_max = int(merged_df['year'].max())
        if not merged_df['year'].dropna().empty:
            year_min = int(merged_df['year'].dropna().min())
            year_max = int(merged_df['year'].dropna().max())

            selected_years = st.slider("Select Year Range",year_min,year_max,(year_min, year_max))
        else:
            st.error("No valid year data found. Please check the source collections.")
            st.stop()

        filt = merged_df[(merged_df['year'] >= selected_years[0]) & (merged_df['year'] <= selected_years[1])]

        st.line_chart(filt.set_index('year')[['gdp_growth', 'inflation_rate', 'unemployment', 'interest_rate', 'sentiment_score']])

# === Tab 3: Composite Insight ===
with tabs[2]:
    st.subheader("📌 Composite Insight Metric")

    def compute_score(row):
        norm_sentiment = (row['sentiment_score'] + 1) / 2  # normalize to 0-1
        return round((norm_sentiment * 0.5 + (row['gdp_growth'] - row['inflation_rate']) * 0.5), 2)

    merged_df['insight_score'] = merged_df.apply(compute_score, axis=1)

    st.line_chart(merged_df.set_index('year')['insight_score'])

    def interpret(score):
        if score > 1:
            return "✅ Positive Outlook"
        elif score > 0:
            return "⚠️ Cautious Optimism"
        else:
            return "❌ Negative Sentiment"

    st.markdown("### Summary")
    for _, row in merged_df.iterrows():
        st.write(f"{int(row['year'])}: {interpret(row['insight_score'])} (Score: {row['insight_score']})")
        
    st.markdown("### Recommendations")
    for _, row in merged_df.iterrows():
        if row['insight_score'] > 1:
            st.success(f"{int(row['year'])}: Positive outlook. Investment in growth sectors can be considered.")
        elif row['insight_score'] > 0:
            st.warning(f"{int(row['year'])}: Mixed signals. Diversification and monitoring are advisable.")
        else:
            st.error(f"{int(row['year'])}: Negative sentiment. Risk-averse strategies recommended.")    
