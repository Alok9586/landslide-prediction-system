import joblib
import pandas as pd
import sys
import os

# Get the project root folder regardless of where this script is run from
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from simulator.sensor_simulator import generate_reading
from data.fetch_weather import get_rainfall

MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "landslide_model.joblib")
model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = [
    "soil_moisture", "tilt_x", "vibration_count",
    "rainfall_24h", "rainfall_72h", "slope_angle", "ndvi"
]

# Static values for your test site - replace with real DEM/NDVI values later
SITE_SLOPE_ANGLE = 27.0
SITE_NDVI = 0.35
SITE_LATITUDE = 25.5941
SITE_LONGITUDE = 85.1376

def classify_risk(probability):
    if probability < 0.30:
        return "LOW"
    elif probability < 0.60:
        return "MEDIUM"
    elif probability < 0.85:
        return "HIGH"
    else:
        return "CRITICAL"

def run_one_cycle(risk_bias="normal"):
    # 1. Get sensor reading (swap this for real ESP32 data later)
    sensor_data = generate_reading(risk_bias=risk_bias)

    # 2. Get live rainfall
    rain_data = get_rainfall(SITE_LATITUDE, SITE_LONGITUDE)

    # 3. Assemble the feature vector the model expects
    features = pd.DataFrame([{
        "soil_moisture": sensor_data["soil_moisture"],
        "tilt_x": sensor_data["tilt_x"],
        "vibration_count": sensor_data["vibration_count"],
        "rainfall_24h": rain_data["rainfall_24h"],
        "rainfall_72h": rain_data["rainfall_72h"],
        "slope_angle": SITE_SLOPE_ANGLE,
        "ndvi": SITE_NDVI
    }])[FEATURE_COLUMNS]

    # 4. Predict probability of landslide
    probability = model.predict_proba(features)[0][1]   # probability of class "1"
    risk_level = classify_risk(probability)

    result = {
        "timestamp": sensor_data["timestamp"],
        "soil_moisture": sensor_data["soil_moisture"],
        "tilt_x": sensor_data["tilt_x"],
        "vibration_count": sensor_data["vibration_count"],
        "rainfall_24h": rain_data["rainfall_24h"],
        "rainfall_72h": rain_data["rainfall_72h"],
        "risk_probability": round(float(probability), 3),
        "risk_level": risk_level
    }
    return result

if __name__ == "__main__":
    # Test with a calm reading
    print("--- NORMAL conditions ---")
    print(run_one_cycle(risk_bias="normal"))

    # Test with a dangerous reading
    print("\n--- DANGER conditions ---")
    print(run_one_cycle(risk_bias="danger"))