import requests

def get_rainfall(latitude, longitude):
    """
    Fetches hourly rainfall data for a location using Open-Meteo (free, no API key).
    Returns rainfall accumulated over the last 1h, 24h, and 72h.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation",
        "past_days": 3,      # gives us the last 72 hours of data
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()   # crashes loudly if the request failed - good for debugging
    result = response.json()

    hourly_rain = result["hourly"]["precipitation"]   # list of mm per hour

    rainfall_1h = hourly_rain[-1] if len(hourly_rain) >= 1 else 0
    rainfall_24h = sum(hourly_rain[-24:]) if len(hourly_rain) >= 24 else sum(hourly_rain)
    rainfall_72h = sum(hourly_rain)

    return {
        "rainfall_1h": round(rainfall_1h, 2),
        "rainfall_24h": round(rainfall_24h, 2),
        "rainfall_72h": round(rainfall_72h, 2)
    }

if __name__ == "__main__":
    # Example: Patna, Bihar coordinates - replace with your actual test site's lat/long
    latitude = 25.5941
    longitude = 85.1376

    rain_data = get_rainfall(latitude, longitude)
    print(rain_data)