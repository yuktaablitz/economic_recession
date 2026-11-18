import requests
from textblob import TextBlob
from pymongo import MongoClient
from datetime import datetime, timedelta
import time
import statistics

from config import MONGO_URI, MONGO_DB, NEWSAPI_KEY


def main():
    # === MongoDB Connection ===
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    sentiment_collection = db["sentiment_news"]

    # === Optional: Clear previous data ===
    sentiment_collection.delete_many({})

    # === NewsAPI Setup ===
    API_KEY = NEWSAPI_KEY
    if not API_KEY:
        raise SystemExit("Set NEWSAPI_KEY in .env (free key: https://newsapi.org/register)")
    query = "economy OR inflation OR stocks OR unemployment OR market OR recession OR layoffs"

    # Use last 30 days only (Free plan limit)
    today = datetime.today()
    from_date = today - timedelta(days=30)

    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&from={from_date.strftime('%Y-%m-%d')}"
        f"&to={today.strftime('%Y-%m-%d')}"
        f"&language=en&sortBy=popularity&pageSize=100&apiKey={API_KEY}"
    )

    print(f"Fetching: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        print("Status Code:", response.status_code)
        if response.status_code != 200:
            print("Response Content:", response.text)
            return

        articles = response.json().get("articles", [])
        all_docs = []
        sentiments = []
        for article in articles:
            title = article.get("title", "")
            published_at = article.get("publishedAt", "")
            date_only = published_at.split("T")[0] if "T" in published_at else published_at

            sentiment = TextBlob(title).sentiment.polarity  # -1 to +1
            sentiments.append(sentiment)

            doc = {
                "headline": title,
                "published_date": date_only,
                "sentiment_score": sentiment,
                "source": "NewsAPI",
                "inserted_at": datetime.utcnow()
            }
            all_docs.append(doc)

        if all_docs:
            sentiment_collection.insert_many(all_docs)
            print(f"✅ Inserted {len(all_docs)} articles into MongoDB.")

            # === Project sentiment to historical years ===
            avg_sentiment = statistics.mean(sentiments)
            print(f"📈 Projecting average sentiment ({avg_sentiment:.2f}) to prior years...")
            from datetime import timezone

            for year in range(1960, today.year):
                sentiment_collection.insert_one({
                    "headline": f"Projected sentiment for {year}",
                    "published_date": f"{year}-01-01",
                    "sentiment_score": avg_sentiment,
                    "source": "Projected",
                    "inserted_at": datetime.now(timezone.utc)
                })
            print(f"✅ Inserted projected sentiment for years 1960 to {today.year - 1}.")
        else:
            print("⚠️ No articles found in response.")
    except Exception as e:
        print(f"Exception occurred: {e}")


if __name__ == "__main__":
    main()
