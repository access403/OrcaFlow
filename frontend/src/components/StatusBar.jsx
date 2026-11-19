export default function StatusBar({ isLoading, selectedAgent }) {
  return (
    <footer className="status-bar">
      <span><span className={`status-dot${isLoading ? " busy" : ""}`} />{isLoading ? "Routing your task" : "All systems operational"}</span>
      <span>{selectedAgent ? `Last routed to ${selectedAgent}` : "OrcaFlow task router"}</span>
    </footer>
  );
}
