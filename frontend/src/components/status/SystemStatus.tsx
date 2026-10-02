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


function SystemStatus({
  health,
  project,
  loading,
  error,
}: SystemStatusProps) {
  return (
    <section className="system-status">
      <h2>System Status</h2>

      {loading && (
        <p>
          Connecting to the DARA-DT Research API...
        </p>
      )}

      {error && (
        <p role="alert">
          {error}
        </p>
      )}

      {!loading && !error && health && project && (
        <div className="system-status-grid">
          <div>
            <span>API Status</span>
            <strong>{health.status}</strong>
          </div>

          <div>
            <span>Service</span>
            <strong>{health.service}</strong>
          </div>

          <div>
            <span>API Version</span>
            <strong>{health.version}</strong>
          </div>

          <div>
            <span>Research Domain</span>
            <strong>{project.research_domain}</strong>
          </div>

          <div>
            <span>Experimental Domain</span>
            <strong>{project.experimental_domain}</strong>
          </div>

          <div>
            <span>Experiments</span>
            <strong>
              {project.experiments_completed}/
              {project.experiments_total}
            </strong>
          </div>

          <div>
            <span>Contribution Status</span>
            <strong>
              {project.contribution_status}
            </strong>
          </div>

          <div>
            <span>Current Stage</span>
            <strong>
              {project.current_stage}
            </strong>
          </div>
        </div>
      )}
    </section>
  );
}


export default SystemStatus;
