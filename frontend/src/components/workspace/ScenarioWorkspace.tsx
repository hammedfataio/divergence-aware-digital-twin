import type {
  ScenarioResponse,
} from "../../types/api";


interface ScenarioWorkspaceProps {
  scenario: ScenarioResponse;
}


function ScenarioWorkspace({
  scenario,
}: ScenarioWorkspaceProps) {
  return (
    <section className="scenario-workspace">
      <header className="scenario-workspace-header">
        <div>
          <p>Scenario Analysis</p>

          <h2>{scenario.scenario_id}</h2>

          <p>{scenario.description}</p>
        </div>
      </header>


      <div className="scenario-workspace-summary">
        <article>
          <h3>Physical System</h3>

          <p>
            Entities:{" "}
            <strong>
              {scenario.physical_state.entities.length}
            </strong>
          </p>
        </article>


        <article>
          <h3>Digital Twin</h3>

          <p>
            Entities:{" "}
            <strong>
              {scenario.twin_state.entities.length}
            </strong>
          </p>
        </article>


        <article>
          <h3>Divergence</h3>

          <p>
            Detected divergences:{" "}
            <strong>
              {scenario.divergences.length}
            </strong>
          </p>
        </article>


        <article>
          <h3>Runtime Evidence</h3>

          <p>
            Evidence records:{" "}
            <strong>
              {scenario.runtime_evidence.length}
            </strong>
          </p>
        </article>


        <article>
          <h3>Propagation</h3>

          <p>
            Propagation records:{" "}
            <strong>
              {scenario.propagation.length}
            </strong>
          </p>
        </article>
      </div>


      <section className="decision-panel">
        <h3>AI Decision</h3>

        <dl>
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

          <div>
            <dt>Dependencies</dt>
            <dd>
              {
                scenario.ai_decision.dependencies
                  .length
              }
            </dd>
          </div>
        </dl>
      </section>


      <section className="divergence-panel">
        <h3>Divergence Analysis</h3>

        {scenario.divergences.length === 0 ? (
          <p>
            No physical-to-twin divergence was
            detected for this scenario.
          </p>
        ) : (
          <ul>
            {scenario.divergences.map(
              (divergence, index) => (
                <li
                  key={`${divergence.entity_id}-${divergence.variable}-${index}`}
                >
                  <strong>
                    {divergence.entity_id}
                  </strong>

                  {" — "}

                  {divergence.variable}

                  {" — physical: "}

                  {String(
                    divergence.physical_value,
                  )}

                  {" — twin: "}

                  {String(
                    divergence.twin_value,
                  )}

                  {" — decision relevant: "}

                  {divergence.decision_relevant ===
                  null
                    ? "unknown"
                    : divergence.decision_relevant
                      ? "yes"
                      : "no"}

                  {" — decision impacting: "}

                  {divergence.decision_impacting ===
                  null
                    ? "unknown"
                    : divergence.decision_impacting
                      ? "yes"
                      : "no"}
                </li>
              ),
            )}
          </ul>
        )}
      </section>


      <section className="evidence-panel">
        <h3>Runtime Evidence</h3>

        {scenario.runtime_evidence.length === 0 ? (
          <p>
            No runtime evidence records are
            available.
          </p>
        ) : (
          <ul>
            {scenario.runtime_evidence.map(
              (evidence, index) => (
                <li
                  key={`${evidence.source}-${evidence.dependency}-${index}`}
                >
                  <strong>
                    {evidence.source}
                  </strong>

                  {" — "}

                  {evidence.dependency}

                  {" — status: "}

                  {evidence.status}

                  {" — confidence: "}

                  {evidence.confidence === null
                    ? "not available"
                    : evidence.confidence}
                </li>
              ),
            )}
          </ul>
        )}
      </section>


      <section className="propagation-panel">
        <h3>Propagation</h3>

        {scenario.propagation.length === 0 ? (
          <p>
            No propagation records are available.
          </p>
        ) : (
          <ul>
            {scenario.propagation.map(
              (record, index) => (
                <li
                  key={`${record.origin}-${index}`}
                >
                  <strong>
                    {record.origin}
                  </strong>

                  {" — "}

                  {record.propagating
                    ? "propagating"
                    : "not propagating"}

                  {record.affected_dependency
                    ? ` — affected dependency: ${record.affected_dependency}`
                    : ""}

                  {record.path.length > 0
                    ? ` — path: ${record.path.join(
                        " → ",
                      )}`
                    : ""}
                </li>
              ),
            )}
          </ul>
        )}
      </section>


      <section className="assurance-panel">
        <h3>Runtime Assurance</h3>

        {scenario.assurance_results.length ===
        0 ? (
          <p>
            No assurance results are available.
          </p>
        ) : (
          <ul>
            {scenario.assurance_results.map(
              (result) => (
                <li key={result.policy}>
                  <strong>{result.policy}</strong>

                  {" — authority: "}

                  {result.authority}

                  {" — "}

                  {result.intervene
                    ? "intervention"
                    : "no intervention"}

                  {" — relevant divergences: "}

                  {
                    result.relevant_divergence_count
                  }

                  {" — reason: "}

                  {result.reason}
                </li>
              ),
            )}
          </ul>
        )}
      </section>


      <section className="ground-truth-panel">
        <h3>Ground Truth</h3>

        {scenario.ground_truth ? (
          <>
            <p>
              Intervention required:{" "}
              <strong>
                {scenario.ground_truth
                  .intervention_required
                  ? "yes"
                  : "no"}
              </strong>
            </p>

            {scenario.ground_truth.reason && (
              <p>
                Reason:{" "}
                {scenario.ground_truth.reason}
              </p>
            )}
          </>
        ) : (
          <p>
            Ground truth unavailable.
          </p>
        )}
      </section>


      <section className="evaluation-panel">
        <h3>Policy Evaluation</h3>

        {Object.keys(
          scenario.evaluations,
        ).length === 0 ? (
          <p>
            No policy evaluations are available.
          </p>
        ) : (
          <ul>
            {Object.entries(
              scenario.evaluations,
            ).map(
              ([policy, evaluation]) => (
                <li key={policy}>
                  <strong>{policy}</strong>

                  {" — "}

                  {evaluation.outcome}

                  {" — "}

                  {evaluation.correct
                    ? "correct"
                    : "incorrect"}
                </li>
              ),
            )}
          </ul>
        )}
      </section>
    </section>
  );
}


export default ScenarioWorkspace;
