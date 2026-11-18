from fredapi import Fred

from config import FRED_API_KEY

if not FRED_API_KEY:
    raise SystemExit("Set FRED_API_KEY in .env (free key: https://fred.stlouisfed.org/docs/api/api_key.html)")

fred = Fred(api_key=FRED_API_KEY)
unemployment = fred.get_series('UNRATE')  # US unemployment rate
interest = fred.get_series('FEDFUNDS')    # Federal Funds Rate

unemployment_df = unemployment.reset_index()
unemployment_df.columns = ['date', 'unemployment']

interest_df = interest.reset_index()
interest_df.columns = ['date', 'interest_rate']
