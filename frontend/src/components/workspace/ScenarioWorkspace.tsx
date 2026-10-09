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

/**
 * One playback provider drives both the selected vehicle visualization
 * and the existing research workspace. Switching views does not restart time.
 */
export default function ScenarioWorkspace({ scenario }: ScenarioWorkspaceProps) {
  return (
    <SharedScenarioPlaybackProvider key={scenario.scenario_id} scenario={scenario}>
      <div className="space-y-5">
        <ScenarioMovementView scenario={scenario} />
        <ScenarioWorkspaceLegacy scenario={scenario} />
      </div>
    </SharedScenarioPlaybackProvider>
  );
}

function ScenarioMovementView({ scenario }: ScenarioWorkspaceProps) {
  const playback = useSharedScenarioPlayback();
  const [mapView, setMapView] = useState<MapView>("interactive");

  return (
    <section
      aria-label="Synchronized logistics playback workspace"
      className="overflow-hidden rounded-2xl border border-white/10 bg-[#0C0F14]"
    >
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-[#F6534D]">
            M7.2 · Interactive Logistics Workspace
          </p>
          <h2 className="mt-1 text-xl font-semibold text-white">Vehicle Movement</h2>
          <p className="mt-1 text-sm text-zinc-400">
            Synchronized physical vehicle and Digital Twin journey
          </p>
        </div>
        <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-xs font-medium text-zinc-300">
          {scenario.scenario_id}
        </span>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 px-4 pb-2 pt-4">
        <div role="group" aria-label="Map visualization mode" className="inline-flex rounded-xl border border-white/10 bg-white/5 p-1">
          {([
            { value: "interactive", label: "Interactive map" },
            { value: "simulation", label: "Simulation view" },
          ] as const).map(({ value, label }) => (
            <button
              key={value}
              type="button"
              aria-pressed={mapView === value}
              onClick={() => setMapView(value)}
              className={[
                "rounded-lg px-4 py-2.5 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white",
                mapView === value
                  ? "bg-[#F6534D] text-white"
                  : "text-zinc-300 hover:bg-white/10 hover:text-white",
              ].join(" ")}
            >
              {label}
            </button>
          ))}
        </div>
        <span className="text-xs text-zinc-400" aria-live="polite">
          {mapView === "interactive" ? "Geographic context · illustrative route" : "Schematic curved-road simulation"}
        </span>
      </div>

      <div className="p-4 pt-2">
        {mapView === "interactive" ? (
          <LogisticsMap scenarioId={scenario.scenario_id} progress={playback.progress} />
        ) : (
          <MovingVehicle scenarioId={scenario.scenario_id} progress={playback.progress} />
        )}
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-white/10 px-5 py-4">
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={playback.togglePlayback}
            aria-label={playback.isPlaying ? "Pause synchronized playback" : "Play synchronized playback"}
            className="rounded-xl bg-[#F6534D] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#E4443E] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
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
            className="rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm font-medium text-zinc-200 transition hover:bg-white/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
          >
            Restart
          </button>
        </div>

        <div role="group" aria-label="Playback speed" className="flex flex-wrap items-center gap-2">
          <span className="mr-2 text-xs text-zinc-400">Playback speed</span>
          {([0.5, 1, 2] as const).map((speed) => (
            <button
              key={speed}
              type="button"
              onClick={() => playback.setSpeed(speed)}
              aria-pressed={playback.speed === speed}
              className={[
                "rounded-lg px-3 py-2 text-xs font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white",
                playback.speed === speed
                  ? "bg-[#F6534D] text-white"
                  : "bg-white/5 text-zinc-300 hover:bg-white/10",
              ].join(" ")}
            >
              {speed}×
            </button>
          ))}
        </div>
      </div>

      <div className="px-5 pb-4">
        <div
          role="progressbar"
          aria-label="Simulation playback progress"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(playback.progress * 100)}
          className="h-1.5 overflow-hidden rounded-full bg-white/10"
        >
          <div className="h-full rounded-full bg-[#F6534D]" style={{ width: `${playback.progress * 100}%` }} />
        </div>
        <div className="mt-2 flex items-center justify-between text-xs text-zinc-400">
          <span>{playback.currentStage.label}</span>
          <span>{Math.round(playback.progress * 100)}%</span>
        </div>
      </div>

      <p className="border-t border-white/10 px-5 py-3 text-xs leading-5 text-zinc-400">
        Both views use the same playback clock. Routes, vehicle positions and timing are illustrative,
        not measured GPS data or experimental evidence. The interactive view uses real map tiles,
        but its route is not verified against the road network. Research outcomes come from the
        DARA-DT scenario response.
      </p>
    </section>
  );
}
