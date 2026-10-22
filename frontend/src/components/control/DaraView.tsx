import { Activity, Diamond, MapPinned, Truck, Play, Pause, RotateCcw } from "lucide-react";
import LogisticsMap from "../workspace/LogisticsMap";
import OperationsControl from "./OperationsControl";
import { situationLabel } from "./OperationsControl";
import AISafetyPanel from "./AISafetyPanel";
import { useScenarioPlayback } from "../../hooks/useScenarioPlayback";
import type { ScenarioResponse } from "../../types/api";

interface DaraViewProps {
  scenarios: string[];
  selectedScenario: string;
  runningScenario: boolean;
  error: string | null;
  onScenarioChange: (scenarioId: string) => void;
  onRunScenario: () => void;
  scenarioId: string;
  progress?: number;
  scenario?: ScenarioResponse | null;
}

export default function DaraView({
  scenarios,
  selectedScenario,
  runningScenario,
  error,
  onScenarioChange,
  onRunScenario,
  scenarioId,
  progress = 0,
  scenario = null,
}: DaraViewProps) {
  const activeScenario = scenarioId || "F0-A";

  const controls = {
    scenarios,
    selectedScenario,
    runningScenario,
    error,
    onScenarioChange,
    onRunScenario,
  };

  return scenario ? (
    <DaraViewWithPlayback
      controls={controls}
      key={scenario.scenario_id}
      scenario={scenario}
    />
  ) : (
    <DaraViewLayout
      scenario={null}
      controls={controls}
      scenarioId={activeScenario}
      progress={progress}
    />
  );
}

function DaraViewWithPlayback({
  controls,
  scenario,
}: {
  scenario: ScenarioResponse;
  controls: OperationsControlProps;
}) {
  const playback = useScenarioPlayback(scenario);

  return (
    <DaraViewLayout
      scenario={scenario}
      controls={controls}
      scenarioId={scenario.scenario_id}
      progress={playback.progress}
      playback={playback}
    />
  );
}

type OperationsControlProps =
  React.ComponentProps<typeof OperationsControl>;

type PlaybackControls = ReturnType<typeof useScenarioPlayback>;

function DaraViewLayout({
  controls,
  scenario,
  scenarioId,
  progress,
  playback,
}: {
  controls: OperationsControlProps;
  scenario: ScenarioResponse | null;
  scenarioId: string;
  progress: number;
  playback?: PlaybackControls;
}) {
  const activeScenario = scenarioId;

  return (
    <section
      id="dara-workspace"
      className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
    >
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 px-5 py-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            DARA View
          </h2>
          <p className="mt-1 text-xs text-slate-500">
            Digital twin operations and vehicle monitoring
          </p>
        </div>

        <span className="inline-flex items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-800">
          <Activity size={13} />
          Simulation Mode
        </span>
      </header>

      <OperationsControl {...controls} />

      <div className="grid lg:grid-cols-[300px_minmax(0,1fr)]">
        <aside className="border-b border-slate-200 lg:border-b-0 lg:border-r">
          <div className="border-b border-slate-100 p-5">
            <h3 className="text-sm font-bold text-slate-900">
              Vehicle Overview
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              One simulated vehicle and its digital twin
            </p>
          </div>

          <div className="space-y-3 p-4">
            <a href="#vehicle-tracking" className="block rounded-xl border border-slate-200 p-4 transition hover:border-blue-300 hover:bg-blue-50 focus-visible:outline-2 focus-visible:outline-blue-600">
              <div className="flex items-center gap-3">
                <div className="grid size-10 place-items-center rounded-lg bg-emerald-50 text-emerald-700">
                  <Truck size={19} />
                </div>
                <div>
                  <div className="text-sm font-semibold text-slate-900">
                    Physical Vehicle
                  </div>
                  <div className="text-xs text-slate-500">
                    Simulated physical-system state
                  </div>
                </div>
              </div>
            </a>

            <a href="#vehicle-tracking" className="block rounded-xl border border-slate-200 p-4 transition hover:border-blue-300 hover:bg-blue-50 focus-visible:outline-2 focus-visible:outline-blue-600">
              <div className="flex items-center gap-3">
                <div className="grid size-10 place-items-center rounded-lg bg-blue-50 text-blue-700">
                  <Diamond size={19} />
                </div>
                <div>
                  <div className="text-sm font-semibold text-slate-900">
                    Digital Twin
                  </div>
                  <div className="text-xs text-slate-500">
                    Modelled vehicle state
                  </div>
                </div>
              </div>
            </a>

            <a href="#operations" className="block rounded-xl border border-blue-100 bg-blue-50 p-4 transition hover:border-blue-400 hover:bg-blue-100 focus-visible:outline-2 focus-visible:outline-blue-600">
              <div className="flex items-center gap-2 text-sm font-semibold text-blue-800">
                <MapPinned size={16} />
                Operational Situation
              </div>
              <p className="mt-2 text-sm font-medium text-blue-700">
                {situationLabel(activeScenario)}
              </p>
              <p className="mt-2 text-xs leading-5 text-blue-700">
                Vehicle positions are illustrative, not live GPS data.
              </p>
            </a>
          </div>
        </aside>

        <div className="min-w-0">
          <div className="border-b border-slate-200 px-5 py-4">
            <h3 className="text-sm font-bold text-slate-900">
              Interactive Journey Map
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Illustrative London journey
            </p>
          </div>

          {playback && (
            <div className="border-b border-slate-200 bg-white px-5 py-4">
              <div className="flex flex-wrap items-center gap-3">
                <button
                  type="button"
                  onClick={playback.togglePlayback}
                  className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
                >
                  {playback.isPlaying ? (
                    <Pause size={16} />
                  ) : (
                    <Play size={16} />
                  )}
                  {playback.isPlaying ? "Pause" : playback.isComplete ? "Replay" : "Play"}
                </button>

                <button
                  type="button"
                  onClick={playback.restart}
                  className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50"
                >
                  <RotateCcw size={15} />
                  Restart
                </button>

                <div className="ml-auto flex items-center gap-2">
                  <span className="text-xs text-slate-500">Speed</span>
                  {([0.5, 1, 2] as const).map((speed) => (
                    <button
                      key={speed}
                      type="button"
                      onClick={() => playback.setSpeed(speed)}
                      aria-pressed={playback.speed === speed}
                      className={
                        playback.speed === speed
                          ? "rounded-md bg-blue-50 px-2 py-1.5 text-xs font-semibold text-blue-700"
                          : "rounded-md px-2 py-1.5 text-xs text-slate-500 hover:bg-slate-50"
                      }
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
                className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100"
              >
                <div
                  className="h-full rounded-full bg-blue-600 transition-[width]"
                  style={{ width: `${playback.progress * 100}%` }}
                />
              </div>

              <div className="mt-2 flex justify-between text-xs text-slate-500">
                <span>{playback.currentStage.shortLabel}</span>
                <span>{Math.round(playback.progress * 100)}%</span>
              </div>
            </div>
          )}

          <div className="min-h-[540px]">
            <LogisticsMap
              scenarioId={activeScenario}
              progress={progress}
              className="h-[540px] w-full"
            />
          </div>
        </div>
      </div>
      <AISafetyPanel scenario={scenario} />
    </section>
  );
}
