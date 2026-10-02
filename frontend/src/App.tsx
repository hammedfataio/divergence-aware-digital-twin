import { useEffect, useState } from "react";

import {
  ApiError,
  getHealth,
  getProjectStatus,
  getScenarios,
  runScenario,
} from "./api/client";

import ApplicationShell from "./components/layout/ApplicationShell";
import ScenarioControl from "./components/scenario/ScenarioControl";
import SystemStatus from "./components/status/SystemStatus";
import ScenarioWorkspace from "./components/workspace/ScenarioWorkspace";

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
  const [health, setHealth] =
    useState<HealthResponse | null>(null);

  const [project, setProject] =
    useState<ProjectStatusResponse | null>(null);

  const [scenarios, setScenarios] =
    useState<string[]>([]);

  const [selectedScenario, setSelectedScenario] =
    useState<string>("");

  const [scenarioResult, setScenarioResult] =
    useState<ScenarioResponse | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [runningScenario, setRunningScenario] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

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
          setSelectedScenario(
            scenarioResponse[0],
          );
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


  function handleScenarioChange(
    scenarioId: string,
  ) {
    setSelectedScenario(scenarioId);
    setScenarioResult(null);
    setScenarioError(null);
  }


  async function handleRunScenario() {
    if (!selectedScenario || runningScenario) {
      return;
    }

    setRunningScenario(true);
    setScenarioError(null);
    setScenarioResult(null);

    try {
      const result =
        await runScenario(selectedScenario);

      setScenarioResult(result);
    } catch (caughtError: unknown) {
      setScenarioError(
        getErrorMessage(caughtError),
      );
    } finally {
      setRunningScenario(false);
    }
  }


  return (
    <ApplicationShell>
      <SystemStatus
        health={health}
        project={project}
        loading={loading}
        error={error}
      />

      {!loading && !error && (
        <ScenarioControl
          scenarios={scenarios}
          selectedScenario={selectedScenario}
          runningScenario={runningScenario}
          error={scenarioError}
          onScenarioChange={
            handleScenarioChange
          }
          onRunScenario={() => {
            void handleRunScenario();
          }}
        />
      )}

      {scenarioResult && (
        <ScenarioWorkspace
          scenario={scenarioResult}
        />
      )}
    </ApplicationShell>
  );
}


export default App;
