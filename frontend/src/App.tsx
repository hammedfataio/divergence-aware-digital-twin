import { useEffect, useState } from "react";

import {
  ApiError,
  getHealth,
  getProjectStatus,
  getScenarios,
  runScenario,
} from "./api/client";

import type {
  HealthResponse,
  ProjectStatusResponse,
  ScenarioResponse,
} from "./types/api";


function getErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message;
  }

  return "An unexpected DARA-DT application error occurred.";
}


function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  const [project, setProject] =
    useState<ProjectStatusResponse | null>(null);

  const [scenarios, setScenarios] = useState<string[]>([]);

  const [selectedScenario, setSelectedScenario] =
    useState<string>("");

  const [scenarioResult, setScenarioResult] =
    useState<ScenarioResponse | null>(null);

  const [loading, setLoading] = useState(true);

  const [runningScenario, setRunningScenario] =
    useState(false);

  const [error, setError] = useState<string | null>(null);

  const [scenarioError, setScenarioError] =
    useState<string | null>(null);


  useEffect(() => {
    let active = true;

    async function initialiseApplication() {
      try {
        const [
          healthResponse,
          projectResponse,
          scenarioResponse,
        ] = await Promise.all([
          getHealth(),
          getProjectStatus(),
          getScenarios(),
        ]);

        if (!active) {
          return;
        }

        setHealth(healthResponse);
        setProject(projectResponse);
        setScenarios(scenarioResponse);

        if (scenarioResponse.length > 0) {
          setSelectedScenario(scenarioResponse[0]);
        }
      } catch (caughtError: unknown) {
        if (!active) {
          return;
        }

        setError(
          `Research API unavailable: ${getErrorMessage(
            caughtError,
          )}`,
        );
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void initialiseApplication();

    return () => {
      active = false;
    };
  }, []);


  async function handleRunScenario() {
    if (!selectedScenario || runningScenario) {
      return;
    }

    setRunningScenario(true);
    setScenarioError(null);
    setScenarioResult(null);

    try {
      const result = await runScenario(selectedScenario);

      setScenarioResult(result);
    } catch (caughtError: unknown) {
      setScenarioError(getErrorMessage(caughtError));
    } finally {
      setRunningScenario(false);
    }
  }


  return (
    <main>
      <header>
        <p>DARA-DT</p>

        <h1>
          Divergence-Aware Runtime Assurance
          for AI-Driven Digital Twins
        </h1>

        <p>Research Control Centre</p>
      </header>


      <section>
        <h2>System Status</h2>

        {loading && (
          <p>Connecting to the DARA-DT Research API...</p>
        )}

        {error && (
          <p role="alert">
            {error}
          </p>
        )}

        {!loading && !error && health && project && (
          <>
            <p>
              API Status: <strong>{health.status}</strong>
            </p>

            <p>
              Service: {health.service}
            </p>

            <p>
              API Version: {health.version}
            </p>

            <p>
              Research Domain: {project.research_domain}
            </p>

            <p>
              Experimental Domain:{" "}
              {project.experimental_domain}
            </p>

            <p>
              Experiments:{" "}
              {project.experiments_completed}/
              {project.experiments_total}
            </p>

            <p>
              Contribution Status:{" "}
              {project.contribution_status}
            </p>

            <p>
              Current Stage: {project.current_stage}
            </p>
          </>
        )}
      </section>


      {!loading && !error && (
        <section>
          <h2>Scenario Control</h2>

          {scenarios.length === 0 ? (
            <p>No demonstration scenarios are available.</p>
          ) : (
            <>
              <label htmlFor="scenario-select">
                Frozen EXP-010 Scenario
              </label>

              <select
                id="scenario-select"
                value={selectedScenario}
                disabled={runningScenario}
                onChange={(event) => {
                  setSelectedScenario(event.target.value);
                  setScenarioResult(null);
                  setScenarioError(null);
                }}
              >
                {scenarios.map((scenarioId) => (
                  <option
                    key={scenarioId}
                    value={scenarioId}
                  >
                    {scenarioId}
                  </option>
                ))}
              </select>

              <button
                type="button"
                disabled={
                  !selectedScenario || runningScenario
                }
                onClick={() => {
                  void handleRunScenario();
                }}
              >
                {runningScenario
                  ? "Running scenario..."
                  : "Run Scenario"}
              </button>

              {scenarioError && (
                <p role="alert">
                  {scenarioError}
                </p>
              )}
            </>
          )}
        </section>
      )}


      {scenarioResult && (
        <section>
          <h2>Scenario Result</h2>

          <p>
            Scenario:{" "}
            <strong>{scenarioResult.scenario_id}</strong>
          </p>

          <p>{scenarioResult.description}</p>


          <h3>Physical System</h3>

          <p>
            Entities:{" "}
            {scenarioResult.physical_state.entities.length}
          </p>


          <h3>Digital Twin</h3>

          <p>
            Entities:{" "}
            {scenarioResult.twin_state.entities.length}
          </p>


          <h3>Divergence</h3>

          <p>
            Detected divergences:{" "}
            {scenarioResult.divergences.length}
          </p>


          <h3>AI Decision</h3>

          <p>
            Decision ID:{" "}
            {scenarioResult.ai_decision.decision_id}
          </p>

          <p>
            Action: {scenarioResult.ai_decision.action}
          </p>

          <p>
            Dependencies:{" "}
            {scenarioResult.ai_decision.dependencies.length}
          </p>


          <h3>Runtime Evidence</h3>

          <p>
            Evidence records:{" "}
            {scenarioResult.runtime_evidence.length}
          </p>


          <h3>Propagation</h3>

          <p>
            Propagation records:{" "}
            {scenarioResult.propagation.length}
          </p>


          <h3>Runtime Assurance</h3>

          <ul>
            {scenarioResult.assurance_results.map(
              (result) => (
                <li key={result.policy}>
                  <strong>{result.policy}</strong>
                  {" — "}
                  {result.authority}
                  {" — "}
                  {result.intervene
                    ? "intervention"
                    : "no intervention"}
                </li>
              ),
            )}
          </ul>


          <h3>Ground Truth</h3>

          {scenarioResult.ground_truth ? (
            <>
              <p>
                Intervention required:{" "}
                <strong>
                  {scenarioResult.ground_truth
                    .intervention_required
                    ? "yes"
                    : "no"}
                </strong>
              </p>

              {scenarioResult.ground_truth.reason && (
                <p>
                  Reason:{" "}
                  {scenarioResult.ground_truth.reason}
                </p>
              )}
            </>
          ) : (
            <p>Ground truth unavailable.</p>
          )}


          <h3>Evaluation</h3>

          {Object.keys(scenarioResult.evaluations).length ===
          0 ? (
            <p>No policy evaluations are available.</p>
          ) : (
            <ul>
              {Object.entries(
                scenarioResult.evaluations,
              ).map(([policy, evaluation]) => (
                <li key={policy}>
                  <strong>{policy}</strong>
                  {" — "}
                  {evaluation.outcome}
                  {" — "}
                  {evaluation.correct
                    ? "correct"
                    : "incorrect"}
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </main>
  );
}


export default App;
