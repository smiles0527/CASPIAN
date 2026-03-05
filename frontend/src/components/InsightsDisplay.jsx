export default function InsightsDisplay({ insights }) {
  if (!insights) return null;

  const { insights: summary, care_plan } = insights;

  return (
    <div className="insights-display">
      <h2>Your Insights</h2>
      {summary && (
        <section>
          <h3>Summary</h3>
          <p className="summary">{summary}</p>
        </section>
      )}
      {care_plan && (
        <section>
          <h3>Care Plan</h3>
          <div className="care-plan">{formatCarePlan(care_plan)}</div>
        </section>
      )}
      <p className="disclaimer">
        These insights are for support only. Always see your clinician for medical decisions.
      </p>
    </div>
  );
}

function formatCarePlan(text) {
  const lines = text.split("\n").filter((l) => l.trim());
  const items = lines.map((line) => {
    const trimmed = line.replace(/^[\-\*]\s*/, "").trim();
    return trimmed ? trimmed : null;
  }).filter(Boolean);
  return (
    <ul>
      {items.map((item, i) => (
        <li key={i}>{item}</li>
      ))}
    </ul>
  );
}
