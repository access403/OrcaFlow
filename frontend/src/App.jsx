import { useState } from "react";
import AgentCard from "./components/AgentCard.jsx";
import ChatPanel from "./components/ChatPanel.jsx";
import FileUploader from "./components/FileUploader.jsx";
import Sidebar from "./components/Sidebar.jsx";
import StatusBar from "./components/StatusBar.jsx";
import WorkflowPanel from "./components/WorkflowPanel.jsx";

const agents = [
  {
    name: "ResearchOrca",
    category: "Research",
    description: "Finds context, sources, and useful background.",
  },
  {
    name: "DeveloperOrca",
    category: "Development",
    description: "Turns implementation requests into a clear plan.",
  },
  {
    name: "AnalystOrca",
    category: "Analysis",
    description: "Evaluates information and surfaces key insights.",
  },
];

export default function App() {
  const [result, setResult] = useState(null);
  const [files, setFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function submitTask(task) {
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/manager/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),
      });

      if (!response.ok) {
        const detail = await response.text();
        throw new Error(detail || `Request failed (${response.status})`);
      }

      setResult(await response.json());
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to connect to OrcaFlow.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">WORKSPACE / TASK ROUTER</p>
            <h1>OrcaFlow workspace</h1>
          </div>
          <div className="topbar-indicator">
            <span className="status-dot" />
            Ready to orchestrate
          </div>
        </header>

        <div className="dashboard">
          <section className="main-column" aria-label="Task workspace">
            <div className="welcome-card">
              <span className="welcome-icon" aria-hidden="true">O</span>
              <div>
                <p className="eyebrow">YOUR AI WORKSPACE</p>
                <h2>What would you like to work on?</h2>
                <p className="muted">
                  Describe a task and OrcaFlow will route it to the right agent.
                </p>
              </div>
            </div>
            <ChatPanel
              error={error}
              isLoading={isLoading}
              onSubmit={submitTask}
              result={result}
            />
            <FileUploader files={files} onChange={setFiles} />
          </section>

          <aside className="details-column" aria-label="Workflow details">
            <div className="section-heading">
              <div>
                <p className="eyebrow">ORCHESTRATION</p>
                <h2>Available agents</h2>
              </div>
              <span className="count-pill">03</span>
            </div>
            <div className="agent-list">
              {agents.map((agent) => (
                <AgentCard
                  key={agent.name}
                  {...agent}
                  active={result?.selected_agent === agent.name}
                />
              ))}
            </div>
            <WorkflowPanel result={result} />
          </aside>
        </div>
        <StatusBar isLoading={isLoading} selectedAgent={result?.selected_agent} />
      </main>
    </div>
  );
}
