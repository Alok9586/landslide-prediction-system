\# Real-Time Landslide Prediction System



A system that predicts landslide risk in real time by fusing ground sensor data

(soil moisture, tilt, vibration) with satellite/weather data (rainfall, terrain

slope, NDVI) and historical landslide records, running inference on an edge

device with a live cloud dashboard.



\## What's built so far

\- Real-time sensor fusion engine (currently using simulated sensor data)

\- ML model (Random Forest) trained on real NASA landslide records + real

&#x20; historical rainfall data — 93% test accuracy

\- Django REST API serving live risk data

\- React dashboard with live risk level, sensor readings, and history table



\## Tech stack

\- \*\*Model training:\*\* Python, scikit-learn, pandas

\- \*\*Backend:\*\* Django, Django REST Framework

\- \*\*Frontend:\*\* React

\- \*\*Data sources:\*\* NASA Global Landslide Catalog, Open-Meteo weather API



\## Project structure

\- `data/` — dataset building scripts + NASA landslide catalog

\- `model/` — model training script + saved trained model

\- `simulator/` — fake sensor reading generator (stand-in until real ESP32 hardware is connected)

\- `engine/` — real-time risk fusion + classification logic

\- `backend/` — Django REST API

\- `frontend/` — React dashboard



\## Running it locally

1\. `pip install -r requirements.txt`

2\. Train the model: `python model/train\_model.py`

3\. Start the backend: `cd backend \&\& python manage.py migrate \&\& python manage.py runserver`

4\. Start the risk engine: `cd engine \&\& python run\_loop.py`

5\. Start the dashboard: `cd frontend \&\& npm install \&\& npm start`



\## Next steps

\- Connect real ESP32 sensor hardware

\- Add SMS/Telegram alerts on HIGH/CRITICAL risk

\- Pull real slope and NDVI values per deployment site

