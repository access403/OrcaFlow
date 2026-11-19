export default function WorkflowPanel({ result }) {
  return (
    <section className="workflow-card">
      <div className="workflow-heading">
        <div>
          <p className="eyebrow">TASK ROUTE</p>
          <h2>Execution plan</h2>
        </div>
        {result && <span className="plan-badge">READY</span>}
      </div>
      {result ? (
        <ol className="plan-list">
          {result.execution_plan.map((step, index) => (
            <li key={`${index}-${step}`}>
              <span className="step-number">{String(index + 1).padStart(2, "0")}</span>
              <span>{step}</span>
            </li>
          ))}
        </ol>
      ) : (
        <div className="empty-plan">
          <span className="empty-plan-icon" aria-hidden="true">01</span>
          <p>Your workflow steps will appear here after you submit a task.</p>
        </div>
      )}
    </section>
  );
}
