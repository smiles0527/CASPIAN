import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function SensorForm({ onInsightsGenerated }) {
  const [sensors, setSensors] = useState(() =>
    Object.fromEntries(
      Array.from({ length: 20 }, (_, i) => [`sensor_${i + 1}`, ""])
    )
  );
  const [feelings, setFeelings] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSensorChange = (num, value) => {
    const parsed = value === "" ? null : parseFloat(value);
    if (value !== "" && (isNaN(parsed) || parsed < 0 || parsed > 100)) return;
    setSensors((prev) => ({ ...prev, [`sensor_${num}`]: value }));
  };

  const buildPayload = () => {
    const payload = { feelings: feelings.trim() || null };
    for (let i = 1; i <= 20; i++) {
      const v = sensors[`sensor_${i}`];
      payload[`sensor_${i}`] = v === "" || v === undefined ? null : parseFloat(v);
    }
    return payload;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/insights`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildPayload()),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        const detail = errData.detail;
        const msg = Array.isArray(detail)
          ? detail.map((d) => d.msg || JSON.stringify(d)).join("; ")
          : typeof detail === "string"
            ? detail
            : res.statusText || "Failed to generate insights";
        throw new Error(msg);
      }
      const data = await res.json();
      onInsightsGenerated(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="sensor-form">
      <h2>Sensors</h2>
      <p className="sensor-legend">
        <strong>1–6:</strong> Pressure sensors (force at high-load areas). <strong>7–20:</strong> Stimulation sensors (near nerve-rich regions, for phantom limb pain). Values 0–100.
      </p>
      <div className="sensor-group">
        <h3>Pressure (1–6)</h3>
        <div className="sensor-grid">
          {[1, 2, 3, 4, 5, 6].map((num) => (
            <div key={num} className="sensor-field">
              <label htmlFor={`sensor-${num}`}>Sensor {num}</label>
              <input
                id={`sensor-${num}`}
                type="number"
                min={0}
                max={100}
                step="0.1"
                placeholder="—"
                value={sensors[`sensor_${num}`] ?? ""}
                onChange={(e) => handleSensorChange(num, e.target.value)}
              />
            </div>
          ))}
        </div>
      </div>
      <div className="sensor-group">
        <h3>Stimulation (7–20)</h3>
        <div className="sensor-grid">
          {Array.from({ length: 14 }, (_, i) => i + 7).map((num) => (
            <div key={num} className="sensor-field">
              <label htmlFor={`sensor-${num}`}>Sensor {num}</label>
              <input
              id={`sensor-${num}`}
              type="number"
              min={0}
              max={100}
              step="0.1"
              placeholder="—"
              value={sensors[`sensor_${num}`] ?? ""}
              onChange={(e) => handleSensorChange(num, e.target.value)}
            />
          </div>
        ))}
        </div>
      </div>

      <div className="feelings-field">
        <label htmlFor="feelings">How are you feeling today?</label>
        <textarea
          id="feelings"
          rows={4}
          placeholder="Describe how you're feeling..."
          value={feelings}
          onChange={(e) => setFeelings(e.target.value)}
        />
      </div>

      {error && <p className="error">{error}</p>}

      <button type="submit" disabled={loading} className="submit-btn">
        {loading ? "Generating..." : "Generate Insights"}
      </button>
    </form>
  );
}
