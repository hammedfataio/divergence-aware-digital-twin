import type {
  AssuranceResult,
  EvidenceStatusValue,
  ScenarioResponse,
} from "../../types/api";

interface ScenarioWorkspaceProps {
  scenario: ScenarioResponse;
}

function formatValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "Not available";
  }

  if (typeof value === "object") {
    try {
      return JSON.stringify(value);
    } catch {
      return "Structured value";
    }
  }

  return String(value);
}

function formatLabel(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function evidenceClass(status: EvidenceStatusValue): string {
  return `evidence-${status}`;
}

function authorityClass(result: AssuranceResult): string {
  return `authority-${result.authority}`;
}

function ScenarioWorkspace({
  scenario,
}: ScenarioWorkspaceProps) {
  const primaryAssuranceResult =
    scenario.assurance_results.find(
      (result) => result.policy === "dara_dt",
    ) ??
    scenario.assurance_results[
      scenario.assurance_results.length - 1
    ] ??
    null;

  const decisionRelevantDivergences =
    scenario.divergences.filter(
      (divergence) =>
        divergence.decision_relevant === true,
    ).length;

  const decisionImpactingDivergences =
    scenario.divergences.filter(
      (divergence) =>
        divergence.decision_impacting === true,
    ).length;

  const propagatingRecords =
    scenario.propagation.filter(
      (record) => record.propagating,
    ).length;

  return (
    <div className="scenario-workspace">
      <section className="scenario-command-header">
        <div>
          <p className="workspace-eyebrow">
            Frozen EXP-010 Scenario
          </p>

          <h2>{scenario.scenario_id}</h2>

          <p>{scenario.description}</p>
        </div>

        <div className="scenario-command-indicators">
          <span className="status-chip status-chip--healthy">
            Research Data
          </span>

          <span className="status-chip status-chip--twin">
            Digital Twin Active
          </span>

          {scenario.divergences.length > 0 && (
            <span className="status-chip status-chip--warning">
              {scenario.divergences.length} Divergence
              {scenario.divergences.length === 1 ? "" : "s"}
            </span>
          )}
        </div>
      </section>

      <div className="scenario-workspace-summary">
        <article>
          <span>Physical Entities</span>
          <strong>
            {scenario.physical_state.entities.length}
          </strong>
        </article>

        <article>
          <span>Twin Entities</span>
          <strong>
            {scenario.twin_state.entities.length}
          </strong>
        </article>

        <article>
          <span>Divergences</span>
          <strong>{scenario.divergences.length}</strong>
        </article>

        <article>
          <span>Decision Relevant</span>
          <strong>{decisionRelevantDivergences}</strong>
        </article>

        <article>
          <span>Decision Impacting</span>
          <strong>{decisionImpactingDivergences}</strong>
        </article>

        <article>
          <span>Propagation</span>
          <strong>{propagatingRecords}</strong>
        </article>
      </div>

      <div className="control-centre">
        <aside className="control-rail">
          <div className="control-panel-heading">
            <div>
              <span className="panel-kicker">
                Operational Context
              </span>
              <h3>Physical / Twin State</h3>
            </div>

            <span className="status-chip status-chip--healthy">
              Connected
            </span>
          </div>

          <div className="state-comparison">
            <article className="state-card state-card--physical">
              <div className="state-card-heading">
                <span className="state-indicator state-indicator--physical" />

                <div>
                  <span>Observed</span>
                  <h4>Physical System</h4>
                </div>
              </div>

              <strong>
                {scenario.physical_state.entities.length}
              </strong>

              <span>entities</span>

              {scenario.physical_state.timestamp !== null && (
                <small>
                  Timestamp:{" "}
                  {scenario.physical_state.timestamp}
                </small>
              )}
            </article>

            <article className="state-card state-card--twin">
              <div className="state-card-heading">
                <span className="state-indicator state-indicator--twin" />

                <div>
                  <span>Represented</span>
                  <h4>Digital Twin</h4>
                </div>
              </div>

              <strong>
                {scenario.twin_state.entities.length}
              </strong>

              <span>entities</span>

              {scenario.twin_state.timestamp !== null && (
                <small>
                  Timestamp: {scenario.twin_state.timestamp}
                </small>
              )}
            </article>
          </div>

          <div className="control-panel-section">
            <div className="control-panel-heading">
              <div>
                <span className="panel-kicker">
                  AI Control
                </span>
                <h3>Decision</h3>
              </div>
            </div>

            <dl className="compact-data-list">
              <div>
                <dt>Decision ID</dt>
                <dd>
                  {scenario.ai_decision.decision_id}
                </dd>
              </div>

              <div>
                <dt>Action</dt>
                <dd>
                  {scenario.ai_decision.action}
                </dd>
              </div>

              <div>
                <dt>Vehicle</dt>
                <dd>
                  {scenario.ai_decision.vehicle_id ??
                    "Not specified"}
                </dd>
              </div>

              <div>
                <dt>Order</dt>
                <dd>
                  {scenario.ai_decision.order_id ??
                    "Not specified"}
                </dd>
              </div>
            </dl>
          </div>

          <div className="control-panel-section">
            <div className="control-panel-heading">
              <div>
                <span className="panel-kicker">
                  Decision Model
                </span>
                <h3>Dependencies</h3>
              </div>

              <strong className="panel-count">
                {scenario.ai_decision.dependencies.length}
              </strong>
            </div>

            {scenario.ai_decision.dependencies.length === 0 ? (
              <p className="empty-state">
                No decision dependencies recorded.
              </p>
            ) : (
              <div className="dependency-list">
                {scenario.ai_decision.dependencies.map(
                  (dependency, index) => (
                    <div
                      className="dependency-item"
                      key={`${dependency.dependency}-${index}`}
                    >
                      <span className="dependency-node" />

                      <div>
                        <strong>
                          {dependency.dependency}
                        </strong>

                        <span>
                          {dependency.relevant
                            ? "Decision relevant"
                            : "Not decision relevant"}
                        </span>
                      </div>
                    </div>
                  ),
                )}
              </div>
            )}
          </div>
        </aside>

        <main className="digital-twin-stage">
          <div className="stage-topbar">
            <div>
              <span className="panel-kicker">
                Live Research View
              </span>
              <h3>Digital Twin Environment</h3>
            </div>

            <div className="stage-legend">
              <span>
                <i className="legend-dot legend-dot--physical" />
                Physical
              </span>

              <span>
                <i className="legend-dot legend-dot--twin" />
                Digital Twin
              </span>

              <span>
                <i className="legend-dot legend-dot--divergence" />
                Divergence
              </span>
            </div>
          </div>

          <div className="stage-content">
            <div className="stage-centre-marker">
              <div className="twin-orbit twin-orbit--outer" />
              <div className="twin-orbit twin-orbit--inner" />

              <div className="stage-physical-node">
                <span>P</span>
              </div>

              <div className="stage-twin-node">
                <span>DT</span>
              </div>

              {scenario.divergences.length > 0 && (
                <div className="stage-divergence-link" />
              )}
            </div>

            <div className="stage-message">
              <span className="status-chip status-chip--twin">
                Scenario Loaded
              </span>

              <h4>
                Physical-to-Digital-Twin Runtime View
              </h4>

              <p>
                This spatial stage represents the runtime
                relationship between the physical system and
                its digital twin. Geographic positioning is
                intentionally not inferred from the frozen
                research data.
              </p>
            </div>

            <div className="stage-stat stage-stat--physical">
              <span>Physical</span>
              <strong>
                {scenario.physical_state.entities.length}
              </strong>
              <small>entities observed</small>
            </div>

            <div className="stage-stat stage-stat--twin">
              <span>Digital Twin</span>
              <strong>
                {scenario.twin_state.entities.length}
              </strong>
              <small>entities represented</small>
            </div>

            <div className="stage-stat stage-stat--divergence">
              <span>Divergence</span>
              <strong>{scenario.divergences.length}</strong>
              <small>
                {decisionImpactingDivergences} decision impacting
              </small>
            </div>
          </div>

          <div className="stage-footer">
            <span>
              Scenario <strong>{scenario.scenario_id}</strong>
            </span>

            <span>
              Decision{" "}
              <strong>
                {scenario.ai_decision.decision_id}
              </strong>
            </span>

            <span>
              Evidence{" "}
              <strong>
                {scenario.runtime_evidence.length}
              </strong>
            </span>

            <span>
              Propagation{" "}
              <strong>{scenario.propagation.length}</strong>
            </span>
          </div>
        </main>

        <aside className="assurance-inspector">
          <div className="control-panel-heading">
            <div>
              <span className="panel-kicker">
                Runtime Assurance
              </span>
              <h3>Authority Inspector</h3>
            </div>
          </div>

          {primaryAssuranceResult ? (
            <div className="authority-summary">
              <span>Current Authority</span>

              <strong
                className={authorityClass(
                  primaryAssuranceResult,
                )}
              >
                {formatLabel(
                  primaryAssuranceResult.authority,
                )}
              </strong>

              <small>
                Policy: {primaryAssuranceResult.policy}
              </small>

              <p>{primaryAssuranceResult.reason}</p>
            </div>
          ) : (
            <p className="empty-state">
              No assurance result available.
            </p>
          )}

          <div className="inspector-section">
            <div className="control-panel-heading">
              <div>
                <span className="panel-kicker">
                  Evidence
                </span>
                <h3>Runtime Evidence</h3>
              </div>

              <strong className="panel-count">
                {scenario.runtime_evidence.length}
              </strong>
            </div>

            {scenario.runtime_evidence.length === 0 ? (
              <p className="empty-state">
                No runtime evidence records available.
              </p>
            ) : (
              <div className="evidence-list">
                {scenario.runtime_evidence.map(
                  (evidence, index) => (
                    <article
                      className="evidence-record"
                      key={`${evidence.source}-${evidence.dependency}-${index}`}
                    >
                      <div>
                        <strong>{evidence.source}</strong>

                        <span
                          className={evidenceClass(
                            evidence.status,
                          )}
                        >
                          {formatLabel(evidence.status)}
                        </span>
                      </div>

                      <p>{evidence.dependency}</p>

                      <small>
                        Confidence:{" "}
                        {evidence.confidence === null
                          ? "Not available"
                          : evidence.confidence}
                      </small>
                    </article>
                  ),
                )}
              </div>
            )}
          </div>

          <div className="inspector-section">
            <div className="control-panel-heading">
              <div>
                <span className="panel-kicker">
                  Verification
                </span>
                <h3>Ground Truth</h3>
              </div>
            </div>

            {scenario.ground_truth ? (
              <div className="ground-truth-summary">
                <span>
                  Intervention Required
                </span>

                <strong
                  className={
                    scenario.ground_truth
                      .intervention_required
                      ? "authority-fallback"
                      : "authority-allow"
                  }
                >
                  {scenario.ground_truth
                    .intervention_required
                    ? "Yes"
                    : "No"}
                </strong>

                {scenario.ground_truth.reason && (
                  <p>
                    {scenario.ground_truth.reason}
                  </p>
                )}
              </div>
            ) : (
              <p className="empty-state">
                Ground truth unavailable.
              </p>
            )}
          </div>
        </aside>
      </div>

      <section className="operational-detail-panel">
        <div className="control-panel-heading">
          <div>
            <span className="panel-kicker">
              Physical-to-Twin Analysis
            </span>
            <h3>Divergence</h3>
          </div>

          <strong className="panel-count">
            {scenario.divergences.length}
          </strong>
        </div>

        {scenario.divergences.length === 0 ? (
          <p className="empty-state">
            No physical-to-twin divergence was detected
            for this scenario.
          </p>
        ) : (
          <div className="divergence-table">
            {scenario.divergences.map(
              (divergence, index) => (
                <article
                  className="divergence-record"
                  key={`${divergence.entity_id}-${divergence.variable}-${index}`}
                >
                  <div>
                    <span>Entity</span>
                    <strong>
                      {divergence.entity_id}
                    </strong>
                  </div>

                  <div>
                    <span>Variable</span>
                    <strong>
                      {divergence.variable}
                    </strong>
                  </div>

                  <div>
                    <span>Physical</span>
                    <strong className="authority-allow">
                      {formatValue(
                        divergence.physical_value,
                      )}
                    </strong>
                  </div>

                  <div>
                    <span>Digital Twin</span>
                    <strong className="authority-restrict">
                      {formatValue(
                        divergence.twin_value,
                      )}
                    </strong>
                  </div>

                  <div>
                    <span>Relevant</span>
                    <strong>
                      {divergence.decision_relevant ===
                      null
                        ? "Unknown"
                        : divergence.decision_relevant
                          ? "Yes"
                          : "No"}
                    </strong>
                  </div>

                  <div>
                    <span>Impacting</span>
                    <strong>
                      {divergence.decision_impacting ===
                      null
                        ? "Unknown"
                        : divergence.decision_impacting
                          ? "Yes"
                          : "No"}
                    </strong>
                  </div>
                </article>
              ),
            )}
          </div>
        )}
      </section>

      <section className="operational-detail-panel">
        <div className="control-panel-heading">
          <div>
            <span className="panel-kicker">
              Dependency Effects
            </span>
            <h3>Propagation</h3>
          </div>

          <strong className="panel-count">
            {scenario.propagation.length}
          </strong>
        </div>

        {scenario.propagation.length === 0 ? (
          <p className="empty-state">
            No propagation records are available.
          </p>
        ) : (
          <div className="propagation-list">
            {scenario.propagation.map(
              (record, index) => (
                <article
                  className="propagation-record"
                  key={`${record.origin}-${index}`}
                >
                  <div>
                    <strong>{record.origin}</strong>

                    <span
                      className={
                        record.propagating
                          ? "authority-restrict"
                          : "authority-allow"
                      }
                    >
                      {record.propagating
                        ? "Propagating"
                        : "Contained"}
                    </span>
                  </div>

                  {record.affected_dependency && (
                    <p>
                      Affected dependency:{" "}
                      <strong>
                        {record.affected_dependency}
                      </strong>
                    </p>
                  )}

                  {record.path.length > 0 && (
                    <div className="propagation-path">
                      {record.path.map(
                        (pathNode, pathIndex) => (
                          <span
                            key={`${pathNode}-${pathIndex}`}
                          >
                            {pathNode}
                          </span>
                        ),
                      )}
                    </div>
                  )}
                </article>
              ),
            )}
          </div>
        )}
      </section>

      <section className="operational-detail-panel">
        <div className="control-panel-heading">
          <div>
            <span className="panel-kicker">
              Policy Comparison
            </span>
            <h3>Runtime Assurance</h3>
          </div>

          <strong className="panel-count">
            {scenario.assurance_results.length}
          </strong>
        </div>

        {scenario.assurance_results.length === 0 ? (
          <p className="empty-state">
            No assurance results are available.
          </p>
        ) : (
          <div className="assurance-policy-grid">
            {scenario.assurance_results.map(
              (result) => (
                <article
                  className="assurance-policy-card"
                  key={result.policy}
                >
                  <span>{result.policy}</span>

                  <strong
                    className={authorityClass(result)}
                  >
                    {formatLabel(result.authority)}
                  </strong>

                  <small>
                    {result.intervene
                      ? "Intervention"
                      : "No intervention"}
                  </small>

                  <p>{result.reason}</p>

                  <footer>
                    Relevant divergences:{" "}
                    {result.relevant_divergence_count}
                  </footer>
                </article>
              ),
            )}
          </div>
        )}
      </section>

      <section className="operational-detail-panel">
        <div className="control-panel-heading">
          <div>
            <span className="panel-kicker">
              Ground-Truth Comparison
            </span>
            <h3>Policy Evaluation</h3>
          </div>

          <strong className="panel-count">
            {Object.keys(scenario.evaluations).length}
          </strong>
        </div>

        {Object.keys(scenario.evaluations).length ===
        0 ? (
          <p className="empty-state">
            No policy evaluations are available.
          </p>
        ) : (
          <div className="evaluation-grid">
            {Object.entries(
              scenario.evaluations,
            ).map(([policy, evaluation]) => (
              <article
                className="evaluation-card"
                key={policy}
              >
                <span>{policy}</span>

                <strong
                  className={
                    evaluation.correct
                      ? "authority-allow"
                      : "authority-fallback"
                  }
                >
                  {evaluation.correct
                    ? "Correct"
                    : "Incorrect"}
                </strong>

                <small>
                  {formatLabel(evaluation.outcome)}
                </small>
              </article>
            ))}
          </div>
        )}
      </section>

      <div className="assurance-timeline">
        <div className="timeline-stage timeline-stage--active">
          <span>01</span>
          Physical
        </div>

        <div className="timeline-stage timeline-stage--active">
          <span>02</span>
          Digital Twin
        </div>

        <div
          className={`timeline-stage ${
            scenario.divergences.length > 0
              ? "timeline-stage--warning"
              : "timeline-stage--active"
          }`}
        >
          <span>03</span>
          Divergence
        </div>

        <div className="timeline-stage timeline-stage--active">
          <span>04</span>
          AI Decision
        </div>

        <div className="timeline-stage timeline-stage--active">
          <span>05</span>
          Evidence
        </div>

        <div
          className={`timeline-stage ${
            primaryAssuranceResult?.intervene
              ? "timeline-stage--critical"
              : "timeline-stage--active"
          }`}
        >
          <span>06</span>
          Assurance
        </div>
      </div>
    </div>
  );
}

export default ScenarioWorkspace;
