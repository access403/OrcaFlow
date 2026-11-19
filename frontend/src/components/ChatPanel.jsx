import { useState } from "react";

export default function ChatPanel({ error, isLoading, onSubmit, result }) {
  const [task, setTask] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    const trimmedTask = task.trim();
    if (!trimmedTask || isLoading) return;
    onSubmit(trimmedTask);
  }

  return (
    <section className="chat-card" aria-label="Submit a task">
      <div className="chat-header">
        <span className="chat-orca">O</span>
        <div>
          <strong>OrcaFlow assistant</strong>
          <span>Task orchestration</span>
        </div>
        <span className="online-label"><span className="status-dot" /> Online</span>
      </div>
      <div className="chat-body">
        <div className="assistant-message">
          <p>Hi there! Tell me what you’re working on. I’ll find the right agent and map out the next steps.</p>
          <span className="message-time">Just now</span>
        </div>
        {result && (
          <div className="user-message" aria-live="polite">
            <strong>{result.selected_agent}</strong> is a good match.
            <span className="message-time">Task classified as {result.task_type}</span>
          </div>
        )}
        {error && <p className="error-message" role="alert">{error}</p>}
      </div>
      <form className="composer" onSubmit={handleSubmit}>
        <label className="visually-hidden" htmlFor="task-input">Describe your task</label>
        <textarea
          id="task-input"
          value={task}
          onChange={(event) => setTask(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              event.currentTarget.form.requestSubmit();
            }
          }}
          placeholder="Describe a task, ask a question, or share an idea..."
          rows="2"
          disabled={isLoading}
        />
        <div className="composer-footer">
          <span className="composer-hint">Enter to send · Shift + Enter for a new line</span>
          <button className="send-button" type="submit" disabled={isLoading || !task.trim()}>
            {isLoading ? "Routing..." : "Route task"}
            <span aria-hidden="true">-&gt;</span>
          </button>
        </div>
      </form>
    </section>
  );
}
