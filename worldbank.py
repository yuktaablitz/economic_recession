import requests
import pandas as pd

def fetch_world_bank(indicator):
    url = f"https://api.worldbank.org/v2/country/USA/indicator/{indicator}?format=json&per_page=1000"
    r = requests.get(url)
    data = r.json()[1]
    df = pd.DataFrame([{
        "country": d["country"]["value"],
        "year": d["date"],
        "value": d["value"]
    } for d in data if d["value"] is not None])
    return df

gdp_df = fetch_world_bank("NY.GDP.MKTP.KD.ZG")  # GDP growth
inflation_df = fetch_world_bank("FP.CPI.TOTL.ZG")  # Inflation rate
