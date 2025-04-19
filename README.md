# 📊 Economic Recession Analysis and Forecasting

This project explores the correlation between public sentiment and economic indicators to better understand and predict economic recessions using a data warehouse approach.

## 🔍 Problem Statement
Economic downturns often take time to be statistically confirmed. This project aims to:
- Collect and clean economic data from credible sources (World Bank, FRED).
- Analyze financial news sentiment using NewsAPI and TextBlob.
- Combine structured and unstructured data for deeper insights using MongoDB and PostgreSQL
- Enable decision-makers to monitor economic health in real-time.

---

## 🛠️ Tech Stack

| Component       | Tool Used                          | Purpose                               |
|----------------|-------------------------------------|----------------------------------------|
| Database        | **MongoDB**, **PostgreSQL**         | NoSQL for flexibility, OLAP with RDBMS |
| ETL Orchestration | **Apache Airflow**                | Scheduling and automating data pipelines |
| Programming     | **Python**                          | Data scraping, transformation, analysis |
| Dashboard       | **Streamlit**                       | User-friendly analytics frontend        |
| Version Control | **Git & GitHub**                    | Collaboration and history tracking     |

---

## 📈 Data Pipeline Overview

1. **Data Collection**  
   - World Bank: GDP & Inflation  
   - FRED: Unemployment & Interest Rates  
   - NewsAPI: Financial headlines and sentiment

2. **ETL & Sentiment Analysis**  
   - TextBlob to compute sentiment polarity  
   - MongoDB stores sentiment and indicators  
   - Airflow schedules daily ETL

3. **Data Warehousing**  
   - Star Schema modeled in PostgreSQL  
   - Dimension: `dim_time`  
   - Fact: `fact_economic_summary`

4. **Visualization & Insights**  
   - Streamlit dashboards:
     - 📈 Sentiment Dashboard
     - 🧮 OLAP Dashboard

---

## 🧪 Project Features

- OLAP Queries for decade trends and recession snapshots
- Dashboard filters for indicators and time range
- Composite Insight Score for forecasting mood vs. economic growth
- Projection of real-time sentiment to historical years (backfilled)

---

## 📁 Folder Structure

```bash
📦 economic_recession
 ┣ 📂 pages/
 ┃ ┣ 📄 1_Sentiment_Dashboard.py
 ┃ ┣ 📄 2_OLAP_Dashboard.py
 ┣ 📂 .streamlit/
 ┃ ┣ 📄 config.toml
 ┣ 📄 home.py
 ┣ 📄 sentiment_etl.py
 ┣ 📄 economic_etl.py
 ┣ 📄 load_to_mongo.py
 ┣ 📄 load_to_postgres.py
 ┣ 📄 run_olap_queries.py
 ┣ 📄 sentiment_dag.py
 ┣ 📄 requirements.txt
```

---

## 👩‍💻 Team Members

- **Yuktaa Sri Addanki** – Data Analyst & OLAP Queries  
- **Chelsi Shulamite Elturi** – Data Collection & ETL  
- **Manjot Kaur** – ETL Pipeline & Data Engineering  
- **Anurag Josyula** – Visualizations & Reporting

---

## 🚀 How to Run

1. Clone this repo  
```bash
git clone https://github.com/yuktaablitz/economic_recession.git
cd economic_recession
```

2. Install dependencies  
```bash
pip install -r requirements.txt
```

3. Run Streamlit dashboards  
```bash
streamlit run home.py
```

---

## 📚 References

- [World Bank API](https://data.worldbank.org/)
- [FRED Economic Data](https://fred.stlouisfed.org/)
- [NewsAPI](https://newsapi.org/)
- [TextBlob](https://textblob.readthedocs.io/)
- [Streamlit](https://streamlit.io/)
- [Apache Airflow](https://airflow.apache.org/)

---

*Last updated on April 19, 2025*
