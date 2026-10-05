import { useEffect, useState } from "react";
import {
  AlertCircle,
  LoaderCircle,
  Radio,
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
import ScenarioControl from "./components/scenario/ScenarioControl";
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


function AppLoadingState() {
  return (
    <section className="flex min-h-[420px] items-center justify-center">
      <div className="flex max-w-sm flex-col items-center text-center">
        <div className="relative mb-5 grid size-14 place-items-center rounded-2xl border border-violet-400/10 bg-violet-500/[0.06]">
          <div className="absolute inset-0 animate-pulse rounded-2xl bg-violet-400/[0.025]" />

          <LoaderCircle
            size={23}
            strokeWidth={1.8}
            className="animate-spin text-violet-400"
          />
        </div>

        <h2 className="text-sm font-semibold text-zinc-200">
          Connecting to DARA-DT
        </h2>

        <p className="mt-2 text-xs leading-5 text-zinc-600">
          Loading the runtime assurance service and available
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

        <h2 className="text-sm font-semibold text-zinc-200">
          Research API unavailable
        </h2>

        <p className="mt-2 text-xs leading-5 text-zinc-500">
          DARA-DT cannot load operational situations until the
          research API is connected.
        </p>

        <div className="mt-5 flex items-start gap-2 rounded-xl border border-white/[0.05] bg-black/20 p-3 text-left">
          <AlertCircle
            size={15}
            strokeWidth={1.8}
            className="mt-0.5 shrink-0 text-red-400"
          />

          <span className="text-[11px] leading-5 text-zinc-500">
            {message}
          </span>
        </div>
      </div>
    </section>
  );
}


function EmptyWorkspace() {
  return (
    <section className="relative overflow-hidden rounded-2xl border border-white/[0.055] bg-[#0c0f14]">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
      >
        <div className="absolute left-1/2 top-1/2 size-[520px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-violet-500/[0.035] blur-[110px]" />

        <div
          className="absolute inset-0 opacity-[0.025]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)",
            backgroundSize: "42px 42px",
          }}
        />
      </div>

      <div className="relative flex min-h-[430px] flex-col items-center justify-center px-6 text-center">
        <div className="relative mb-6">
          <div className="absolute inset-0 scale-[2.4] rounded-full bg-violet-500/[0.05] blur-2xl" />

          <div className="relative grid size-16 place-items-center rounded-2xl border border-violet-400/15 bg-violet-500/[0.07] shadow-[0_0_50px_rgba(139,92,246,0.07)]">
            <Radio
              size={27}
              strokeWidth={1.6}
              className="text-violet-300"
            />
          </div>

          <span className="absolute -right-1 -top-1 flex size-3">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-30" />
            <span className="relative inline-flex size-3 rounded-full border-2 border-[#0c0f14] bg-emerald-400" />
          </span>
        </div>

        <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-violet-400">
          Digital Twin Ready
        </div>

        <h2 className="max-w-xl text-xl font-semibold tracking-[-0.02em] text-zinc-100 sm:text-2xl">
          Select a situation to see the system think
        </h2>

        <p className="mt-3 max-w-lg text-[13px] leading-6 text-zinc-500">
          Run an operational situation to visualise the
          real-world state, Digital Twin, AI recommendation,
          information problems and DARA-DT trust decision.
        </p>

        <div className="mt-7 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-[10px] text-zinc-600">
          <span className="flex items-center gap-1.5">
            <span className="size-1.5 rounded-full bg-blue-400" />
            Real-world state
          </span>

          <span className="flex items-center gap-1.5">
            <span className="size-1.5 rounded-full bg-violet-400" />
            Digital Twin
          </span>

          <span className="flex items-center gap-1.5">
            <span className="size-1.5 rounded-full bg-amber-400" />
            AI recommendation
          </span>

          <span className="flex items-center gap-1.5">
            <span className="size-1.5 rounded-full bg-emerald-400" />
            Trust check
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

          {scenarioResult ? (
            <ScenarioWorkspace
              scenario={scenarioResult}
            />
          ) : (
            <EmptyWorkspace />
          )}

          {runtimeReady ? (
            <div className="flex items-center justify-between border-t border-white/[0.04] px-1 pt-3">
              <div className="flex items-center gap-2 text-[10px] text-zinc-700">
                <span className="size-1.5 rounded-full bg-emerald-500/70" />
                DARA-DT runtime connected
              </div>

              <span className="text-[10px] text-zinc-700">
                Research-backed operational demonstrator
              </span>
            </div>
          ) : null}
        </div>
      )}
    </ApplicationShell>
  );
}


export default App;