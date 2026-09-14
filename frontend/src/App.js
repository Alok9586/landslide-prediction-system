import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000/api";

function riskColor(level) {
  switch (level) {
    case "LOW": return "#2d6a4f";
    case "MEDIUM": return "#e9c46a";
    case "HIGH": return "#f4a261";
    case "CRITICAL": return "#e63946";
    default: return "#999";
  }
}

function App() {
  const [latest, setLatest] = useState(null);
  const [readings, setReadings] = useState([]);
  const [error, setError] = useState(null);

  const fetchData = () => {
    fetch(`${API_BASE}/latest/`)
      .then((res) => res.json())
      .then((data) => {
        setLatest(data);
        setError(null);
      })
      .catch(() => setError("Could not reach backend. Is Django running?"));

    fetch(`${API_BASE}/readings/`)
      .then((res) => res.json())
      .then((data) => {
        setReadings(data.readings || []);
        setError(null);
      })
      .catch(() => setError("Could not reach backend. Is Django running?"));
  };

  useEffect(() => {
    fetchData();                                    // fetch immediately on load
    const interval = setInterval(fetchData, 10000);  // then every 10 seconds
    return () => clearInterval(interval);            // cleanup when component unmounts
  }, []);

  return (
    <div className="App">
      <h1>Landslide Risk Dashboard</h1>

      {error && <p className="error">{error}</p>}

      {latest && (
        <div
          className="risk-card"
          style={{ borderColor: riskColor(latest.risk_level) }}
        >
          <h2 style={{ color: riskColor(latest.risk_level) }}>
            {latest.risk_level}
          </h2>
          <p>Probability: {latest.risk_probability}</p>
          <p>Soil moisture: {latest.soil_moisture}%</p>
          <p>Tilt: {latest.tilt_x}°</p>
          <p>Vibration count: {latest.vibration_count}</p>
          <p>Rainfall (24h): {latest.rainfall_24h} mm</p>
          <p>Rainfall (72h): {latest.rainfall_72h} mm</p>
          <p className="timestamp">Last updated: {latest.timestamp}</p>
        </div>
      )}

      <h3>Recent Readings</h3>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Risk</th>
            <th>Probability</th>
            <th>Soil %</th>
            <th>Tilt</th>
            <th>Vibration</th>
          </tr>
        </thead>
        <tbody>
          {readings.map((r, i) => (
            <tr key={i}>
              <td>{r.timestamp}</td>
              <td style={{ color: riskColor(r.risk_level) }}>{r.risk_level}</td>
              <td>{r.risk_probability}</td>
              <td>{r.soil_moisture}</td>
              <td>{r.tilt_x}</td>
              <td>{r.vibration_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;