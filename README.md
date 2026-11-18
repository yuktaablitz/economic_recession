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
 ┃ ┣ 📄 1_Sentiment_Dashboard.py   # sentiment vs. indicators (MongoDB)
 ┃ ┗ 📄 2_OLAP_Dashboard.py        # OLAP queries on the star schema (PostgreSQL)
 ┣ 📂 .streamlit/config.toml
 ┣ 📄 Home.py                      # Streamlit entry point
 ┣ 📄 config.py                    # connection settings + API keys from .env
 ┣ 📄 worldbank.py                 # GDP growth + inflation (World Bank API)
 ┣ 📄 fred.py                      # unemployment + Fed funds rate (FRED API)
 ┣ 📄 economic_etl.py              # merge indicators by year -> MongoDB econ_data.yearly_reports
 ┣ 📄 sentiment_etl.py             # NewsAPI headlines + TextBlob polarity -> MongoDB econ_data.sentiment_news
 ┣ 📄 sentiment_dag.py             # Airflow DAG: sentiment ETL >> economic ETL, daily
 ┣ 📄 load_to_postgres.py          # MongoDB -> PostgreSQL star schema (dim_time, fact_economic_summary)
 ┣ 📄 run_olap_queries.py          # 6 OLAP queries printed to the console
 ┣ 📄 schema.sql                   # star schema DDL
 ┣ 📄 docker-compose.yml           # local MongoDB + PostgreSQL
 ┗ 📄 requirements.txt
```

---

## 👩‍💻 Team Members

- **Yuktaa Sri Addanki** – Data Analyst & OLAP Queries  
- **Chelsi Shulamite Elturi** – Data Collection & ETL  
- **Manjot Kaur** – ETL Pipeline & Data Engineering  
- **Anurag Josyula** – Visualizations & Reporting

---

## 🚀 How to Run

Requires Python 3.10+ and Docker (or local MongoDB and PostgreSQL installs).

1. Clone and install
```bash
git clone https://github.com/yuktaablitz/economic_recession.git
cd economic_recession
python3 -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m textblob.download_corpora lite
```

2. Configure
```bash
cp .env.example .env     # add your free FRED_API_KEY and NEWSAPI_KEY
```

3. Start the databases (PostgreSQL creates the star schema from `schema.sql` on first start)
```bash
docker compose up -d
```
Using your own PostgreSQL instead? Create the `econ_db` database and `econ_user` user, then run `psql -U econ_user -d econ_db -f schema.sql`.

4. Run the pipeline
```bash
python sentiment_etl.py      # NewsAPI headlines + sentiment -> MongoDB
python economic_etl.py       # World Bank + FRED indicators -> MongoDB
python load_to_postgres.py   # MongoDB -> PostgreSQL star schema
python run_olap_queries.py   # optional: print the OLAP results
```

5. Open the dashboards
```bash
streamlit run Home.py
```

### Optional: schedule it with Airflow

`sentiment_dag.py` runs the sentiment ETL and then the economic ETL every day. Install Airflow in its own environment
(see the [Airflow install guide](https://airflow.apache.org/docs/apache-airflow/stable/start.html)), copy or symlink
this folder into your `dags/` folder, and the DAG `daily_sentiment_etl` will appear in the UI.

### Notes

- NewsAPI's free plan only returns the last 30 days of headlines. To give earlier years a sentiment value,
  `sentiment_etl.py` assigns the current 30-day average to each year from 1960 (rows marked `source: "Projected"`).
  Treat historical sentiment as a placeholder, not measured data.
- The recession flag in `dim_time` is a simple rule: unemployment above 6% or negative GDP growth.

---

## 📚 References

- [World Bank API](https://data.worldbank.org/)
- [FRED Economic Data](https://fred.stlouisfed.org/)
- [NewsAPI](https://newsapi.org/)
- [TextBlob](https://textblob.readthedocs.io/)
- [Streamlit](https://streamlit.io/)
- [Apache Airflow](https://airflow.apache.org/)

---

*Last updated on November 17, 2026*
