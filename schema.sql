-- Star schema for the economic warehouse (PostgreSQL)

CREATE TABLE IF NOT EXISTS dim_time (
    year            INTEGER PRIMARY KEY,
    decade          VARCHAR(10) NOT NULL,
    recession_flag  BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS fact_economic_summary (
    id                   SERIAL PRIMARY KEY,
    year                 INTEGER NOT NULL REFERENCES dim_time(year),
    gdp_growth           DOUBLE PRECISION,
    inflation_rate       DOUBLE PRECISION,
    unemployment         DOUBLE PRECISION,
    interest_rate        DOUBLE PRECISION,
    avg_sentiment_score  DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_fact_year ON fact_economic_summary(year);
