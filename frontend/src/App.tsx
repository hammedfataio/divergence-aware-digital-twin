import { useActiveView } from "./hooks/useActiveView";
import DaraView from "./components/control/DaraView";
import VehicleTrackingView from "./components/tracking/VehicleTrackingView";
import OperationsView from "./components/operations/OperationsView";
import AISafetyView from "./components/safety/AISafetyView";
import { useEffect, useState } from "react";
import {
  AlertCircle,
  LoaderCircle,
  ServerOff,
} from "lucide-react";

import {
  ApiError,
  getHealth,
  getProjectStatus,
  getScenarios,
  runScenario,
} from "./api/client";

import ApplicationShell from "./components/layout/ApplicationShell";

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


function AppLoadingState() {
  return (
    <section className="flex min-h-[420px] items-center justify-center">
      <div className="flex max-w-sm flex-col items-center text-center">
        <div className="relative mb-5 grid size-14 place-items-center rounded-2xl border border-violet-400/10 bg-violet-500/[0.06]">
          <div className="absolute inset-0 animate-pulse rounded-2xl bg-violet-400/[0.025]" />

          <LoaderCircle
            size={23}
            strokeWidth={1.8}
            className="animate-spin text-blue-600"
          />
        </div>

        <h2 className="text-sm font-semibold text-slate-900">
          Connecting to DARA-DT
        </h2>

        <p className="mt-2 text-xs leading-5 text-slate-500">
          Loading the simulation service and available
          operational situations.
        </p>
      </div>
    </section>
  );
}


function ApplicationErrorState({
  message,
}: {
  message: string;
}) {
  return (
    <section className="flex min-h-[420px] items-center justify-center">
      <div className="w-full max-w-lg rounded-2xl border border-red-400/10 bg-red-400/[0.035] p-7 text-center">
        <div className="mx-auto mb-5 grid size-12 place-items-center rounded-xl border border-red-400/10 bg-red-400/[0.06]">
          <ServerOff
            size={21}
            strokeWidth={1.8}
            className="text-red-400"
          />
        </div>

        <h2 className="text-sm font-semibold text-slate-900">
          Simulation service unavailable
        </h2>

        <p className="mt-2 text-xs leading-5 text-slate-600">
          DARA-DT cannot load operational situations until the
          simulation service is connected.
        </p>

        <div className="mt-5 flex items-start gap-2 rounded-xl border border-white/[0.05] bg-black/20 p-3 text-left">
          <AlertCircle
            size={15}
            strokeWidth={1.8}
            className="mt-0.5 shrink-0 text-red-400"
          />

          <span className="text-[11px] leading-5 text-slate-600">
            {message}
          </span>
        </div>
      </div>
    </section>
  );
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
          `Simulation service unavailable: ${getErrorMessage(
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


  const activeView = useActiveView();

  const runtimeReady =
    health?.status === "ok" &&
    project !== null;


  return (
    <ApplicationShell>
      {loading ? (
        <AppLoadingState />
      ) : error ? (
        <ApplicationErrorState
          message={error}
        />
      ) : (
        <div className="space-y-4">

          {activeView === "ai-safety" ? (
            <AISafetyView
              scenario={scenarioResult}
              scenarioId={selectedScenario || "F0-A"}
            />
          ) : activeView === "operations" ? (
            <OperationsView
              scenarios={scenarios}
              selectedScenario={selectedScenario}
              runningScenario={runningScenario}
              error={scenarioError}
              onScenarioChange={handleScenarioChange}
              onRunScenario={() => void handleRunScenario()}
            />
          ) : activeView === "vehicle-tracking" ? (
            <VehicleTrackingView
              scenarioId={selectedScenario || "F0-A"}
            />
          ) : (
          <DaraView
            scenarios={scenarios}
            selectedScenario={selectedScenario}
            runningScenario={runningScenario}
            error={scenarioError}
            onScenarioChange={handleScenarioChange}
            onRunScenario={() => void handleRunScenario()}
            scenarioId={selectedScenario || "F0-A"}
            scenario={scenarioResult}
          />
          )}



          {runtimeReady ? (
            <div className="flex items-center justify-between border-t border-white/[0.04] px-1 pt-3">
              <div className="flex items-center gap-2 text-[10px] text-zinc-700">
                <span className="size-1.5 rounded-full bg-emerald-500/70" />
                DARA-DT runtime connected
              </div>

              <span className="text-[10px] text-zinc-700">
                Simulated environment · No live vehicle telemetry
              </span>
            </div>
          ) : null}
        </div>
      )}
    </ApplicationShell>
  );
}


export default App;