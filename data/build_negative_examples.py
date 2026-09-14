import pandas as pd
import requests
import random
import time

df = pd.read_csv("data/filtered_landslides.csv", parse_dates=["event_date"])

# Reuse the same real locations, but pick different random dates far from
# any known event date - these represent "nothing happened here" conditions.
locations = df[["latitude", "longitude"]].drop_duplicates().sample(n=min(300, len(df)), random_state=7).reset_index(drop=True)

def random_safe_date():
    year = random.randint(2015, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return pd.Timestamp(year=year, month=month, day=day)

def get_historical_rainfall(lat, lon, date):
    start = (date - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
    end = date.strftime("%Y-%m-%d")
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": start, "end_date": end,
        "daily": "precipitation_sum", "timezone": "auto"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        daily_rain = r.json()["daily"]["precipitation_sum"]
        daily_rain = [x if x is not None else 0 for x in daily_rain]
        return daily_rain[-1], sum(daily_rain)
    except Exception as e:
        print(f"  Skipped: {e}")
        return None, None

rows = []
for i, loc in locations.iterrows():
    safe_date = random_safe_date()
    r24, r72 = get_historical_rainfall(loc["latitude"], loc["longitude"], safe_date)
    if r24 is not None:
        rows.append({
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "event_date": safe_date,
            "rainfall_24h": r24,
            "rainfall_72h": r72,
            "landslide_occurred": 0
        })
    print(f"[{i+1}/{len(locations)}] done")
    time.sleep(0.3)

out_df = pd.DataFrame(rows)
out_df.to_csv("data/real_safe_events.csv", index=False)
print(f"\nSaved {len(out_df)} safe examples")
print(out_df.head())