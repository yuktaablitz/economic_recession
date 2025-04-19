import streamlit as st

st.set_page_config(page_title="Economic Insights Launcher", layout="centered")

st.title("📊 Economic Recession Project")
st.markdown("Explore insights powered by MongoDB and PostgreSQL")

option = st.selectbox("Choose a dashboard", ["📈 Sentiment Dashboard", "🧮 OLAP Dashboard"])

if option == "📈 Sentiment Dashboard":
    st.markdown("Click [here](./Sentiment_Dashboard) to open the Sentiment Dashboard.")

if option == "🧮 OLAP Dashboard":
    st.markdown("Click [here](./OLAP_Dashboard) to open the OLAP Dashboard.")
