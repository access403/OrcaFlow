const categoryStyles = {
  Research: "research",
  Development: "development",
  Analysis: "analysis",
};

export default function AgentCard({ name, category, description, active }) {
  return (
    <article className={`agent-card${active ? " selected" : ""}`}>
      <span className={`agent-icon ${categoryStyles[category]}`} aria-hidden="true">
        {category === "Research" ? "R" : category === "Development" ? "D" : "A"}
      </span>
      <div className="agent-copy">
        <div className="agent-title">
          <h3>{name}</h3>
          {active && <span className="selected-tag">Selected</span>}
        </div>
        <p>{description}</p>
      </div>
      <span className="agent-arrow" aria-hidden="true">-&gt;</span>
    </article>
  );
}
