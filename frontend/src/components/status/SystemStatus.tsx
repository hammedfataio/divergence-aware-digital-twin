import type {
  HealthResponse,
  ProjectStatusResponse,
} from "../../types/api";

interface SystemStatusProps {
  health: HealthResponse | null;
  project: ProjectStatusResponse | null;
  loading: boolean;
  error: string | null;
}

function formatStatus(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function SystemStatus({
  health,
  project,
  loading,
  error,
}: SystemStatusProps) {
  if (loading) {
    return (
      <section className="system-status">
        <h2>System Status</h2>

        <div className="system-status-message">
          <span className="status-chip status-chip--twin">
            Connecting
          </span>

          <p>Connecting to the DARA-DT Research API...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="system-status">
        <h2>System Status</h2>

        <div className="system-status-message">
          <span className="status-chip status-chip--critical">
            Offline
          </span>

          <p role="alert">{error}</p>
        </div>
      </section>
    );
  }

  if (!health || !project) {
    return (
      <section className="system-status">
        <h2>System Status</h2>

        <div className="system-status-message">
          <span className="status-chip status-chip--warning">
            Unavailable
          </span>

          <p>Research system status is currently unavailable.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="system-status">
      <h2>System Status</h2>

      <div>
        <div className="system-status-overview">
          <div>
            <span className="status-chip status-chip--healthy">
              API Online
            </span>

            <p>
              Frozen research programme connected to the interactive
              demonstrator.
            </p>
          </div>

          <div className="system-status-experiment">
            <span>Research Programme</span>
            <strong>
              {project.experiments_completed}/{project.experiments_total}
            </strong>
          </div>
        </div>

        <dl>
          <div>
            <dt>API Status</dt>
            <dd>{formatStatus(health.status)}</dd>
          </div>

          <div>
            <dt>Service</dt>
            <dd>{health.service}</dd>
          </div>

          <div>
            <dt>API Version</dt>
            <dd>{health.version}</dd>
          </div>

          <div>
            <dt>Research Domain</dt>
            <dd>{project.research_domain}</dd>
          </div>

          <div>
            <dt>Experimental Domain</dt>
            <dd>{project.experimental_domain}</dd>
          </div>

          <div>
            <dt>Experiments</dt>
            <dd>
              {project.experiments_completed}/{project.experiments_total}
            </dd>
          </div>

          <div>
            <dt>Contribution Status</dt>
            <dd>{formatStatus(project.contribution_status)}</dd>
          </div>

          <div>
            <dt>Current Stage</dt>
            <dd>{formatStatus(project.current_stage)}</dd>
          </div>
        </dl>
      </div>
    </section>
  );
}

export default SystemStatus;
