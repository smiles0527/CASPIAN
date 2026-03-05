import { useState } from "react";
import SensorForm from "./components/SensorForm";
import InsightsDisplay from "./components/InsightsDisplay";
import "./App.css";

export default function App() {
  const [insights, setInsights] = useState(null);

  return (
    <div className="app">
      <header>
        <h1>CASPIAN Follow-Up Care</h1>
        <p className="tagline">
          Enter sensor values and how you feel, then click Generate Insights
        </p>
      </header>

      <main>
        <SensorForm onInsightsGenerated={setInsights} />
        <InsightsDisplay insights={insights} />
      </main>
    </div>
  );
}
