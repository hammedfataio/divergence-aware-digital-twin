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
  if (loading) {
    return (
      <section
        className="operations-overview"
        aria-label="Control Centre status"
      >
        <div className="operations-overview-header">
          <div>
            <span className="operations-eyebrow">
              CONTROL CENTRE
            </span>

            <h2>Connecting to DARA-DT</h2>

            <p>
              Establishing communication with the runtime
              assurance service.
            </p>
          </div>

          <span className="operations-live operations-live-loading">
            CONNECTING
          </span>
        </div>
      </section>
    );
  }

  if (error || !health || !project) {
    return (
      <section
        className="operations-overview operations-overview-error"
        aria-label="Control Centre status"
      >
        <div className="operations-overview-header">
          <div>
            <span className="operations-eyebrow">
              CONTROL CENTRE
            </span>

            <h2>Runtime Connection Unavailable</h2>

            <p>
              DARA-DT cannot currently verify AI decisions.
              Restore the research API connection before
              continuing operations.
            </p>
          </div>

          <span className="operations-live operations-live-error">
            OFFLINE
          </span>
        </div>

        {error && (
          <div
            className="operations-alert"
            role="alert"
          >
            {error}
          </div>
        )}
      </section>
    );
  }

  const programmeComplete =
    project.experiments_completed ===
    project.experiments_total;

  return (
    <section
      className="operations-overview"
      aria-labelledby="operations-overview-title"
    >
      <div className="operations-overview-header">
        <div>
          <span className="operations-eyebrow">
            CONTROL CENTRE
          </span>

          <h2 id="operations-overview-title">
            Operations Overview
          </h2>

          <p>
            Monitor autonomous logistics decisions,
            digital-twin reliability and situations
            requiring human attention.
          </p>
        </div>

        <span className="operations-live">
          <span
            className="operations-live-dot"
            aria-hidden="true"
          />
          LIVE
        </span>
      </div>

      <div className="operations-status-grid">
        <article className="operations-status-card">
          <div className="operations-card-heading">
            <span className="operations-card-icon">
              SYS
            </span>

            <span className="operations-card-label">
              SYSTEM
            </span>
          </div>

          <strong className="operations-card-value">
            Operational
          </strong>

          <p>
            Runtime assurance service connected
          </p>

          <span className="operations-card-state operations-state-positive">
            <span aria-hidden="true">●</span>
            Connected
          </span>
        </article>

        <article className="operations-status-card">
          <div className="operations-card-heading">
            <span className="operations-card-icon">
              AI
            </span>

            <span className="operations-card-label">
              AI SUPERVISION
            </span>
          </div>

          <strong className="operations-card-value">
            Ready
          </strong>

          <p>
            AI decisions can be checked by DARA-DT
          </p>

          <span className="operations-card-state operations-state-positive">
            <span aria-hidden="true">●</span>
            Assurance active
          </span>
        </article>

        <article className="operations-status-card">
          <div className="operations-card-heading">
            <span className="operations-card-icon">
              DT
            </span>

            <span className="operations-card-label">
              DIGITAL TWIN
            </span>
          </div>

          <strong className="operations-card-value">
            Available
          </strong>

          <p>
            Physical and digital states ready for comparison
          </p>

          <span className="operations-card-state operations-state-positive">
            <span aria-hidden="true">●</span>
            Monitoring ready
          </span>
        </article>

        <article className="operations-status-card">
          <div className="operations-card-heading">
            <span className="operations-card-icon">
              RX
            </span>

            <span className="operations-card-label">
              RESEARCH BASIS
            </span>
          </div>

          <strong className="operations-card-value">
            {project.experiments_completed}/
            {project.experiments_total}
          </strong>

          <p>
            Experimental programme supporting the demonstrator
          </p>

          <span
            className={`operations-card-state ${
              programmeComplete
                ? "operations-state-positive"
                : "operations-state-neutral"
            }`}
          >
            <span aria-hidden="true">●</span>

            {programmeComplete
              ? "Programme complete"
              : "Programme in progress"}
          </span>
        </article>
      </div>
    </section>
  );
}

export default SystemStatus;