"""Connection settings and API keys, read from environment variables (or a .env file)."""
import os

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "econ_data")

PG_PARAMS = {
    "dbname": os.getenv("PG_DB", "econ_db"),
    "user": os.getenv("PG_USER", "econ_user"),
    "password": os.getenv("PG_PASSWORD", "econpass"),
    "host": os.getenv("PG_HOST", "localhost"),
    "port": int(os.getenv("PG_PORT", "5432")),
}

FRED_API_KEY = os.getenv("FRED_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
