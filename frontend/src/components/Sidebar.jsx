const navigation = [
  { label: "Overview", short: "OV", active: true },
  { label: "Workflows", short: "WF" },
  { label: "Agent library", short: "AG" },
  { label: "Files", short: "FL" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <a className="brand" href="/" aria-label="OrcaFlow home">
        <span className="brand-mark">O</span>
        <span>orca<span className="brand-light">flow</span></span>
      </a>
      <div className="workspace-switcher">
        <span className="workspace-avatar">W</span>
        <span className="workspace-name">My workspace</span>
        <span className="switcher-arrow">v</span>
      </div>
      <p className="nav-label">WORKSPACE</p>
      <nav className="navigation" aria-label="Main navigation">
        {navigation.map((item) => (
          <a
            className={`nav-item${item.active ? " active" : ""}`}
            href={item.active ? "#workspace" : "#"}
            key={item.label}
            aria-current={item.active ? "page" : undefined}
          >
            <span className="nav-icon" aria-hidden="true">{item.short}</span>
            {item.label}
            {item.label === "Workflows" && <span className="nav-count">2</span>}
          </a>
        ))}
      </nav>
      <div className="sidebar-bottom">
        <div className="help-card">
          <span className="help-mark">?</span>
          <div>
            <strong>Need a hand?</strong>
            <span>Explore the quick guide</span>
          </div>
        </div>
        <div className="profile">
          <span className="profile-avatar">U</span>
          <span className="profile-name">Your account</span>
          <span className="profile-menu">...</span>
        </div>
      </div>
    </aside>
  );
}
