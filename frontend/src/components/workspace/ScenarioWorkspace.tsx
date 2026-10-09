
import MovingVehicle from "./MovingVehicle";
import ScenarioWorkspaceLegacy from "./ScenarioWorkspaceLegacy";

import type { ScenarioResponse } from "../../types/api";
import { useScenarioPlayback } from "../../hooks/useScenarioPlayback";

interface ScenarioWorkspaceProps {
  scenario: ScenarioResponse;
}

export default function ScenarioWorkspace({
  scenario,
}: ScenarioWorkspaceProps) {
  return (
    <div className="space-y-5">
      <ScenarioMovementView scenario={scenario} />

      <ScenarioWorkspaceLegacy scenario={scenario} />
    </div>
  );
}

function ScenarioMovementView({
  scenario,
}: ScenarioWorkspaceProps) {
  const playback = useScenarioPlayback(scenario);

  return (
    <section className="overflow-hidden rounded-2xl border border-white/10 bg-[#0C0F14]">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-[#F6534D]">
            M5F.1 · Logistics Simulation
          </p>

          <h2 className="mt-1 text-xl font-semibold text-white">
            Vehicle Movement
          </h2>

          <p className="mt-1 text-sm text-zinc-400">
            Physical vehicle and Digital Twin journey
          </p>
        </div>

        <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-xs font-medium text-zinc-300">
          {scenario.scenario_id}
        </span>
      </div>

      <div className="p-4">
        <MovingVehicle
          scenarioId={scenario.scenario_id}
          progress={playback.progress}
        />
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-white/10 px-5 py-4">
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={playback.togglePlayback}
            className="rounded-xl bg-[#F6534D] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#E4443E]"
          >
            {playback.isPlaying ? "Pause journey" : "Play journey"}
          </button>

          <button
            type="button"
            onClick={playback.restart}
            className="rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm font-medium text-zinc-200 transition hover:bg-white/10"
          >
            Restart
          </button>
        </div>

        <div className="flex items-center gap-2">
          <span className="mr-2 text-xs text-zinc-500">
            Playback speed
          </span>

          {([0.5, 1, 2] as const).map((speed) => (
            <button
              key={speed}
              type="button"
              onClick={() => playback.setSpeed(speed)}
              aria-pressed={playback.speed === speed}
              className={[
                "rounded-lg px-3 py-2 text-xs font-semibold transition",
                playback.speed === speed
                  ? "bg-[#F6534D] text-white"
                  : "bg-white/5 text-zinc-400 hover:bg-white/10",
              ].join(" ")}
            >
              {speed}×
            </button>
          ))}
        </div>
      </div>

      <div className="px-5 pb-4">
        <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
          <div
            className="h-full rounded-full bg-[#F6534D]"
            style={{
              width: `${playback.progress * 100}%`,
            }}
          />
        </div>

        <div className="mt-2 flex items-center justify-between text-xs text-zinc-500">
          <span>{playback.currentStage.label}</span>
          <span>{Math.round(playback.progress * 100)}%</span>
        </div>
      </div>

      <p className="border-t border-white/10 px-5 py-3 text-xs leading-5 text-zinc-500">
        Illustrative scenario playback. Vehicle positions and
        movement timing are schematic, not measured GPS data.
        Research decisions remain supplied by the existing
        DARA-DT backend.
      </p>
    </section>
  );
}
