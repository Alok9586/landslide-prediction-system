import pandas as pd
import requests
import random
import time

df = pd.read_csv("data/filtered_landslides.csv", parse_dates=["event_date"])

# Sample 300 real events - keeps runtime reasonable
positive_events = df.sample(n=min(300, len(df)), random_state=42).reset_index(drop=True)

def get_historical_rainfall(lat, lon, date):
    """
    Fetches daily rainfall for the event date and the 2 days before it,
    using Open-Meteo's free historical archive API.
    """
    start = (date - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
    end = date.strftime("%Y-%m-%d")

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "daily": "precipitation_sum",
        "timezone": "auto"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        daily_rain = data["daily"]["precipitation_sum"]
        daily_rain = [x if x is not None else 0 for x in daily_rain]

        rainfall_24h = daily_rain[-1]
        rainfall_72h = sum(daily_rain)
        return rainfall_24h, rainfall_72h
    except Exception as e:
        print(f"  Skipped ({lat},{lon},{date.date()}): {e}")
        return None, None

rows = []
for i, event in positive_events.iterrows():
    r24, r72 = get_historical_rainfall(event["latitude"], event["longitude"], event["event_date"])
    if r24 is not None:
        rows.append({
            "latitude": event["latitude"],
            "longitude": event["longitude"],
            "event_date": event["event_date"],
            "rainfall_24h": r24,
            "rainfall_72h": r72,
            "landslide_occurred": 1
        })
    print(f"[{i+1}/{len(positive_events)}] done")
    time.sleep(0.3)   # be polite to the free API - avoids rate limiting

out_df = pd.DataFrame(rows)
out_df.to_csv("data/real_rainfall_events.csv", index=False)
print(f"\nSaved {len(out_df)} events with real rainfall data")
print(out_df.head())