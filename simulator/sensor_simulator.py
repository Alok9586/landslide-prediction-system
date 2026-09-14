import random
import time
import json
from datetime import datetime

def generate_reading(risk_bias="normal"):
    """
    risk_bias: "normal" (calm slope) or "danger" (simulates a risky slope)
    This lets you test both safe and alert scenarios.
    """
    if risk_bias == "danger":
        soil_moisture = round(random.uniform(70, 95), 2)      # % - very wet
        tilt_x = round(random.uniform(5, 12), 2)               # degrees - tilting a lot
        tilt_y = round(random.uniform(3, 10), 2)
        vibration_count = random.randint(15, 40)               # events in last hour
    else:
        soil_moisture = round(random.uniform(20, 50), 2)       # % - normal
        tilt_x = round(random.uniform(0, 2), 2)                # barely moving
        tilt_y = round(random.uniform(0, 2), 2)
        vibration_count = random.randint(0, 5)

    reading = {
        "timestamp": datetime.utcnow().isoformat(),
        "soil_moisture": soil_moisture,
        "tilt_x": tilt_x,
        "tilt_y": tilt_y,
        "vibration_count": vibration_count
    }
    return reading

if __name__ == "__main__":
    # Runs forever, printing one fake reading every 5 seconds.
    # Change risk_bias to "danger" to test alert behaviour later.
    while True:
        data = generate_reading(risk_bias="normal")
        print(json.dumps(data, indent=2))
        time.sleep(5)