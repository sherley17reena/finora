function AgentActivity({
  agentLogs,
  onRefresh,
}) {
  return (
    <>
      <header>
        <p className="welcome">Orchestration Log</p>
        <h2>Agent Activity</h2>

        <p className="subtitle">
          See which Finora agents and tools were used.
        </p>
      </header>

      <section className="panel">
        <div className="activity-heading">
          <h3>Recent Activity</h3>

          <button
            className="refresh-button"
            onClick={onRefresh}
          >
            Refresh
          </button>
        </div>

        {agentLogs.length === 0 ? (
          <p>No agent activity found.</p>
        ) : (
          <div className="activity-list">
            {[...agentLogs].reverse().map((log) => (
              <div
                className="activity-item"
                key={log.id}
              >
                <div className="activity-agent">
                  <strong>{log.agent}</strong>
                  <span>{log.action}</span>
                </div>

                <p>
                  <strong>Tool:</strong> {log.tool}
                </p>

                <p>
                  <strong>Arguments:</strong>{" "}
                  {log.arguments}
                </p>

                <p className="activity-time">
                  {new Date(
                    log.timestamp
                  ).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}

export default AgentActivity;