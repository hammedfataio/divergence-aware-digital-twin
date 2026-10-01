import { useEffect, useState } from "react";

import {
  ApiError,
  getHealth,
  getProjectStatus,
  getScenarios,
} from "./api/client";

import type {
  HealthResponse,
  ProjectStatusResponse,
} from "./types/api";


function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  const [project, setProject] =
    useState<ProjectStatusResponse | null>(null);

  const [scenarios, setScenarios] = useState<string[]>([]);

  const [selectedScenario, setSelectedScenario] =
    useState<string>("");

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState<string | null>(null);


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

        if (caughtError instanceof ApiError) {
          setError(
            `Research API unavailable: ${caughtError.message}`,
          );
        } else {
          setError(
            "Unable to establish a connection to the DARA-DT Research API.",
          );
        }
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
              Experimental Domain: {project.experimental_domain}
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
                onChange={(event) =>
                  setSelectedScenario(event.target.value)
                }
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

              <p>
                Selected scenario:{" "}
                <strong>{selectedScenario}</strong>
              </p>
            </>
          )}
        </section>
      )}
    </main>
  );
}


export default App;
