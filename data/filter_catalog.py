import pandas as pd

df = pd.read_csv("data/nasa_landslide_catalog.csv")

# Keep only rainfall-triggered landslides (matches our project's focus)
df = df[df["landslide_trigger"].str.lower() == "rain"]

# Drop rows missing the fields we actually need
df = df.dropna(subset=["event_date", "latitude", "longitude"])

# Keep only the columns we care about
df = df[["event_date", "latitude", "longitude", "country_name", "landslide_size"]]

# Convert event_date to a clean date format
df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
df = df.dropna(subset=["event_date"])

df.to_csv("data/filtered_landslides.csv", index=False)
print(f"Kept {len(df)} rainfall-triggered landslide events")
print(df.head())