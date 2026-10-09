
import { useState } from "react";
import MovingVehicle from "./MovingVehicle";
import LogisticsMap from "./LogisticsMap";
import ScenarioWorkspaceLegacy from "./ScenarioWorkspaceLegacy";

import {
  SharedScenarioPlaybackProvider,
  useSharedScenarioPlayback,
} from "../../hooks/SharedScenarioPlayback";

import type { ScenarioResponse } from "../../types/api";

interface ScenarioWorkspaceProps {
  scenario: ScenarioResponse;
}

type MapView = "interactive" | "simulation";
type SystemSelection = "physical" | "twin";

function clamp(value: number): number {
  return Number.isFinite(value)
    ? Math.max(0, Math.min(1, value))
    : 0;
}

function getIllustratedProgress(scenarioId: string, progress: number) {
  const family = scenarioId.split("-")[0].toUpperCase();
  const twin = clamp(clamp(progress) * 1.15);

  const physical =
    family === "F1"
      ? Math.min(twin, 0.34)
      : family === "F3"
        ? Math.min(twin, 0.58)
        : family === "F4"
          ? Math.min(twin, 0.45)
          : twin;

  return {
    physical,
    twin,
    separated: Math.abs(physical - twin) > 0.015,
  };
}

export default function ScenarioWorkspace({
  scenario,
}: ScenarioWorkspaceProps) {
  return (
    <SharedScenarioPlaybackProvider
      key={scenario.scenario_id}
      scenario={scenario}
    >
      <div className="space-y-5">
        <ScenarioMovementView scenario={scenario} />
        <ScenarioWorkspaceLegacy scenario={scenario} />
      </div>
    </SharedScenarioPlaybackProvider>
  );
}

function ScenarioMovementView({
  scenario,
}: ScenarioWorkspaceProps) {
  const playback = useSharedScenarioPlayback();
  const [mapView, setMapView] = useState<MapView>("interactive");

  return (
    <section
      aria-label="Synchronized logistics workspace"
      className="min-w-0 overflow-hidden rounded-2xl border border-white/10 bg-[#0c0f14]"
    >
      <header className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 px-5 py-5">
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-[#ff5555]">
            DARA-DT · Journey Workspace
          </p>

          <h2 className="mt-2 text-2xl font-semibold text-white">
            Vehicle Movement
          </h2>

          <p className="mt-2 text-base text-zinc-300">
            Synchronized physical vehicle and Digital Twin journey
          </p>
        </div>

        <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-zinc-200">
          {scenario.scenario_id}
        </span>
      </header>

      <div className="flex flex-wrap items-center justify-between gap-4 px-4 pb-3 pt-5">
        <div
          role="group"
          aria-label="Journey visualization"
          className="inline-flex rounded-xl border border-white/10 bg-white/5 p-1"
        >
          <button
            type="button"
            aria-pressed={mapView === "interactive"}
            onClick={() => setMapView("interactive")}
            className={`rounded-lg px-5 py-3 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-white ${
              mapView === "interactive"
                ? "bg-[#ff5555] text-white"
                : "text-zinc-300 hover:bg-white/10"
            }`}
          >
            Journey Map
          </button>

          <button
            type="button"
            aria-pressed={mapView === "simulation"}
            onClick={() => setMapView("simulation")}
            className={`rounded-lg px-5 py-3 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-white ${
              mapView === "simulation"
                ? "bg-[#ff5555] text-white"
                : "text-zinc-300 hover:bg-white/10"
            }`}
          >
            Simulation View
          </button>
        </div>

        <p className="text-sm text-zinc-400">
          {mapView === "interactive"
            ? "Illustrated journey · synchronized playback"
            : "Scenario-specific curved-road simulation"}
        </p>
      </div>

      {/* Both visualizations occupy the same desktop panel. */}
      <div className="grid min-w-0 grid-cols-1 items-stretch gap-4 px-4 pb-5 xl:grid-cols-[minmax(0,7fr)_minmax(360px,3fr)]">
        <div className="min-w-0 min-h-[600px] overflow-hidden rounded-2xl">
          {mapView === "interactive" ? (
            <LogisticsMap
              scenarioId={scenario.scenario_id}
              progress={playback.progress}
              className="h-full min-h-[600px]"
            />
          ) : (
            <div className="h-full min-h-[600px] overflow-hidden rounded-2xl border border-white/10 bg-slate-950">
              <MovingVehicle
                scenarioId={scenario.scenario_id}
                progress={playback.progress}
              />
            </div>
          )}
        </div>

        <VehicleInspector
          scenarioId={scenario.scenario_id}
          progress={playback.progress}
        />
      </div>

      {/* One playback control centre shared by both views. */}
      <div className="border-t border-white/10 px-5 py-5">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={playback.togglePlayback}
              className="min-h-11 rounded-xl bg-[#ff5555] px-6 py-3 text-sm font-semibold text-white transition hover:bg-red-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-white"
            >
              {playback.isPlaying
                ? "Pause simulation"
                : playback.isComplete
                  ? "Replay simulation"
                  : "Play simulation"}
            </button>

            <button
              type="button"
              onClick={playback.restart}
              className="min-h-11 rounded-xl border border-white/15 bg-white/5 px-5 py-3 text-sm font-medium text-white hover:bg-white/10"
            >
              Restart
            </button>
          </div>

          <div
            role="group"
            aria-label="Playback speed"
            className="flex items-center gap-2"
          >
            <span className="mr-2 text-sm text-zinc-400">
              Playback speed
            </span>

            {([0.5, 1, 2] as const).map((speed) => (
              <button
                key={speed}
                type="button"
                onClick={() => playback.setSpeed(speed)}
                aria-pressed={playback.speed === speed}
                className={`min-h-10 rounded-lg px-4 py-2 text-sm font-semibold ${
                  playback.speed === speed
                    ? "bg-[#ff5555] text-white"
                    : "bg-white/5 text-zinc-300 hover:bg-white/10"
                }`}
              >
                {speed}×
              </button>
            ))}
          </div>
        </div>

        <div
          role="progressbar"
          aria-label="Simulation progress"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(playback.progress * 100)}
          className="mt-5 h-2 overflow-hidden rounded-full bg-white/10"
        >
          <div
            className="h-full rounded-full bg-[#ff5555]"
            style={{
              width: `${clamp(playback.progress) * 100}%`,
            }}
          />
        </div>

        <div className="mt-3 flex items-center justify-between gap-3 text-sm text-zinc-400">
          <span>{playback.currentStage.label}</span>
          <span className="tabular-nums">
            {Math.round(playback.progress * 100)}%
          </span>
        </div>
      </div>

      <p className="border-t border-white/10 px-5 py-4 text-sm leading-6 text-zinc-400">
        Both visualizations use the same playback clock. Roads,
        routes, positions and movement are illustrative. They are
        not GPS tracks, measured telemetry or experimental results.
        Research authority decisions come from the DARA-DT
        scenario response.
      </p>
    </section>
  );
}

function VehicleInspector({
  scenarioId,
  progress,
}: {
  scenarioId: string;
  progress: number;
}) {
  const [selection, setSelection] =
    useState<SystemSelection>("physical");

  const journey = getIllustratedProgress(scenarioId, progress);

  const selectedProgress =
    selection === "physical"
      ? journey.physical
      : journey.twin;

  return (
    <aside
      aria-label="Vehicle inspector"
      className="flex min-h-[600px] flex-col rounded-2xl border border-slate-700 bg-[#101925] p-6 text-white"
    >
      <p className="text-sm font-semibold uppercase tracking-wide text-cyan-300">
        Vehicle Inspector
      </p>

      <h3 className="mt-3 text-2xl font-semibold">
        Journey Overview
      </h3>

      <p className="mt-4 text-base leading-7 text-zinc-300">
        Select a system to inspect its illustrative journey state.
      </p>

      <div
        role="group"
        aria-label="Select vehicle system"
        className="mt-6 grid grid-cols-2 gap-3"
      >
        {(["physical", "twin"] as const).map((system) => (
          <button
            key={system}
            type="button"
            onClick={() => setSelection(system)}
            aria-pressed={selection === system}
            className={`min-h-12 rounded-xl border px-3 py-3 text-sm font-semibold transition ${
              selection === system
                ? "border-[#ff5555] bg-red-500/15 text-white"
                : "border-white/15 bg-white/5 text-zinc-200 hover:bg-white/10"
            }`}
          >
            {system === "physical"
              ? "Physical Vehicle"
              : "Digital Twin"}
          </button>
        ))}
      </div>

      <dl className="mt-7 space-y-5">
        <div className="flex items-center justify-between gap-3 border-b border-white/10 pb-4">
          <dt className="text-base text-zinc-300">Scenario</dt>
          <dd className="text-base font-semibold">{scenarioId}</dd>
        </div>

        <div className="flex items-center justify-between gap-3 border-b border-white/10 pb-4">
          <dt className="text-base text-zinc-300">
            Selected system
          </dt>
          <dd className="text-base font-semibold">
            {selection === "physical"
              ? "Physical"
              : "Digital Twin"}
          </dd>
        </div>

        <div className="flex items-center justify-between gap-3 border-b border-white/10 pb-4">
          <dt className="text-base text-zinc-300">
            Illustrated journey
          </dt>
          <dd className="text-lg font-bold tabular-nums">
            {Math.round(selectedProgress * 100)}%
          </dd>
        </div>

        <div className="flex items-center justify-between gap-3">
          <dt className="text-base text-zinc-300">
            Marker separation
          </dt>
          <dd
            className={`text-sm font-semibold ${
              journey.separated
                ? "text-amber-300"
                : "text-emerald-300"
            }`}
          >
            {journey.separated ? "Shown" : "Not shown"}
          </dd>
        </div>
      </dl>

      <div className="mt-auto pt-8">
        <div className="rounded-xl border border-cyan-400/30 bg-cyan-400/10 p-5">
          <h4 className="text-base font-semibold text-cyan-200">
            What does this mean?
          </h4>

          <p className="mt-3 text-base leading-7 text-zinc-200">
            {journey.separated
              ? "The illustrative physical vehicle and Digital Twin markers are apart at this playback point."
              : "The illustrative markers currently overlap or are too close to distinguish."}
            {" "}This visual separation does not establish a
            measured mismatch or an AI authority decision.
          </p>
        </div>

        <p className="mt-5 text-sm leading-6 text-zinc-300">
          For evidence and authority decisions, use the research
          workspace below.
        </p>
      </div>
    </aside>
  );
}
