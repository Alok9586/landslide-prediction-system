import pandas as pd
import random

positive = pd.read_csv("data/real_rainfall_events.csv")
negative = pd.read_csv("data/real_safe_events.csv")

df = pd.concat([positive, negative], ignore_index=True)

def simulate_sensor_features(row):
    """
    Generates realistic, NOISY sensor/terrain values.
    Uses overlapping bell-curve distributions (not clean fixed ranges)
    so the model has to find genuine patterns instead of memorizing
    a trivial cutoff.
    """
    if row["landslide_occurred"] == 1:
        soil_moisture = random.gauss(60, 15)      # centered higher, but overlaps with safe range
        tilt_x = random.gauss(5, 3)
        vibration_count = random.gauss(15, 8)
        slope_angle = random.gauss(28, 8)
        ndvi = random.gauss(0.35, 0.15)
    else:
        soil_moisture = random.gauss(38, 15)      # centered lower, but overlaps with danger range
        tilt_x = random.gauss(1.5, 1.5)
        vibration_count = random.gauss(4, 4)
        slope_angle = random.gauss(16, 8)
        ndvi = random.gauss(0.55, 0.15)

    # Clip to realistic physical bounds so we don't get negative moisture, etc.
    soil_moisture = round(min(max(soil_moisture, 5), 100), 2)
    tilt_x = round(min(max(tilt_x, 0), 20), 2)
    vibration_count = int(min(max(vibration_count, 0), 50))
    slope_angle = round(min(max(slope_angle, 0), 60), 2)
    ndvi = round(min(max(ndvi, 0), 1), 2)

    return pd.Series([soil_moisture, tilt_x, vibration_count, slope_angle, ndvi])

df[["soil_moisture", "tilt_x", "vibration_count", "slope_angle", "ndvi"]] = df.apply(simulate_sensor_features, axis=1)

# Reorder columns nicely
df = df[[
    "latitude", "longitude", "event_date",
    "soil_moisture", "tilt_x", "vibration_count",
    "rainfall_24h", "rainfall_72h", "slope_angle", "ndvi",
    "landslide_occurred"
]]

df = df.sample(frac=1, random_state=1).reset_index(drop=True)  # shuffle
df.to_csv("data/training_dataset.csv", index=False)

print(f"Final training dataset: {len(df)} rows")
print(df["landslide_occurred"].value_counts())
print(df.head())