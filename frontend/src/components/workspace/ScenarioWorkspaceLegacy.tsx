import { useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  Bot,
  Box,
  Check,
  CheckCircle2,
  ChevronRight,
  CircleDot,
  GitBranch,
  Info,
  Network,
  Pause,
  Play,
  Radio,
  RefreshCw,
  RotateCcw,
  Route,
  ShieldCheck,
  Truck,
  Warehouse,
  XCircle,
  Zap,
} from "lucide-react";

import { useSharedScenarioPlayback } from "../../hooks/SharedScenarioPlayback";
import type {
  AssuranceResult,
  Authority,
  EvidenceStatus,
  ScenarioResponse,
} from "../../types/api";

interface ScenarioWorkspaceProps {
  scenario: ScenarioResponse;
}

interface AuthorityPresentation {
  label: string;
  description: string;
  action: string;
  textClass: string;
  borderClass: string;
  backgroundClass: string;
  glowClass: string;
}

interface EvidencePresentation {
  label: string;
  dotClass: string;
  textClass: string;
  icon: typeof CheckCircle2;
}

type StoryNode =
  | "real"
  | "vehicle"
  | "mismatch"
  | "twin"
  | "propagation"
  | "decision"
  | "assurance";

function humanize(value: string): string {
  return value
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function authorityPresentation(
  authority: Authority,
): AuthorityPresentation {
  switch (authority) {
    case "allow":
      return {
        label: "APPROVED",
        description: "AI can proceed",
        action: "No human action required",
        textClass: "text-emerald-300",
        borderClass: "border-emerald-400/20",
        backgroundClass: "bg-emerald-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(52,211,153,0.10)]",
      };
    case "restrict":
      return {
        label: "LIMITED",
        description: "Proceed within restrictions",
        action: "Operator awareness required",
        textClass: "text-amber-300",
        borderClass: "border-amber-400/20",
        backgroundClass: "bg-amber-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(251,191,36,0.10)]",
      };
    case "defer":
      return {
        label: "WAITING",
        description: "More reliable information is needed",
        action: "Review information before proceeding",
        textClass: "text-orange-300",
        borderClass: "border-orange-400/20",
        backgroundClass: "bg-orange-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(251,146,60,0.10)]",
      };
    case "fallback":
      return {
        label: "SAFE MODE",
        description: "Use backup behaviour",
        action: "AI decision replaced by fallback behaviour",
        textClass: "text-red-300",
        borderClass: "border-red-400/20",
        backgroundClass: "bg-red-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(248,113,113,0.10)]",
      };
  }
}

function evidencePresentation(
  status: EvidenceStatus,
): EvidencePresentation {
  switch (status) {
    case "available":
      return {
        label: "Verified",
        dotClass: "bg-emerald-400",
        textClass: "text-emerald-300",
        icon: CheckCircle2,
      };
    case "stale":
      return {
        label: "Outdated",
        dotClass: "bg-amber-400",
        textClass: "text-amber-300",
        icon: AlertTriangle,
      };
    case "missing":
      return {
        label: "Missing",
        dotClass: "bg-orange-400",
        textClass: "text-orange-300",
        icon: AlertTriangle,
      };
    case "conflicting":
      return {
        label: "Conflicting",
        dotClass: "bg-red-400",
        textClass: "text-red-300",
        icon: XCircle,
      };
  }
}

function selectPrimaryAssurance(
  results: AssuranceResult[],
): AssuranceResult | null {
  if (results.length === 0) return null;

  const daraResult = results.find((result) =>
    result.policy.toLowerCase().includes("dara"),
  );

  return daraResult ?? results[results.length - 1];
}

function getFamilyId(scenarioId: string): string {
  return scenarioId.split("-")[0] ?? "";
}

function familyStory(familyId: string): {
  label: string;
  description: string;
  accent: string;
} {
  switch (familyId) {
    case "F0":
      return {
        label: "NORMAL OPERATIONS",
        description: "System synchronized",
        accent: "text-emerald-400",
      };
    case "F1":
      return {
        label: "CURRENT DECISION ISSUE",
        description: "Mismatch reaches this decision",
        accent: "text-red-400",
      };
    case "F2":
      return {
        label: "ISSUE ELSEWHERE",
        description: "Mismatch isolated from this decision",
        accent: "text-blue-400",
      };
    case "F3":
      return {
        label: "KNOCK-ON RISK",
        description: "Connected effect reaches this decision",
        accent: "text-amber-400",
      };
    case "F4":
      return {
        label: "MULTIPLE RISKS",
        description: "Several connected effects detected",
        accent: "text-violet-400",
      };
    default:
      return {
        label: "OPERATIONAL SITUATION",
        description: "Runtime scenario",
        accent: "text-violet-400",
      };
  }
}

function ScenarioWorkspace({
  scenario,
}: ScenarioWorkspaceProps) {
  const [selectedNode, setSelectedNode] =
    useState<StoryNode | null>(null);
  const [showExplanation, setShowExplanation] =
    useState(false);

  const playback = useSharedScenarioPlayback();

  const primaryAssurance = selectPrimaryAssurance(
    scenario.assurance_results,
  );

  const trustPresentation = primaryAssurance
    ? authorityPresentation(primaryAssurance.authority)
    : null;

  const familyId = getFamilyId(scenario.scenario_id);
  const story = familyStory(familyId);

  const relevantDivergences = scenario.divergences.filter(
    (divergence) => divergence.decision_relevant === true,
  );

  const impactingDivergences = scenario.divergences.filter(
    (divergence) => divergence.decision_impacting === true,
  );

  const propagatingRecords = scenario.propagation.filter(
    (record) => record.propagating,
  );

  const vehicleId =
    scenario.ai_decision.vehicle_id ?? "Assigned vehicle";
  const orderId =
    scenario.ai_decision.order_id ?? "Current order";
  const action = humanize(scenario.ai_decision.action);

  const mismatchAffectsDecision =
    impactingDivergences.length > 0;
  const hasMultipleEffects =
    scenario.divergences.length > 1 ||
    propagatingRecords.length > 1;
  const selectedDivergence =
    scenario.divergences[0] ?? null;

  const showMismatch =
    playback.showMismatch && playback.hasDivergence;

  // The AI recommendation exists in every scenario, including F0 and F2.
  // Reveal the AI node when the playback reaches Trace, while keeping
  // decision-effect highlighting separate and research-driven.
  const traceStageReached =
    playback.currentStage.id === "trace" ||
    playback.currentStage.id === "trust" ||
    playback.isComplete;

  const showTrace = traceStageReached;
  const showDecisionEffectTrace = playback.showDecisionTrace;
  const showPropagation = playback.showPropagation;
  const showTrust = playback.showTrustResult;
  const showComparison = playback.showComparison;
  const showEvent = playback.showScenarioEvent;

  function nodeButtonClass(
    node: StoryNode,
    extra = "",
    visible = true,
  ): string {
    return [
      "group absolute z-20 text-left transition-all duration-500",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400",
      visible
        ? "translate-y-0 opacity-100"
        : "pointer-events-none translate-y-3 opacity-0",
      selectedNode === node
        ? "scale-[1.03]"
        : "hover:scale-[1.02]",
      extra,
    ].join(" ");
  }

  return (
    <section className="space-y-4">
      {/* PLAYBACK CONTROL CENTRE */}
      <section className="overflow-hidden rounded-2xl border border-white/[0.06] bg-[#0c0f14]">
        <div className="flex flex-col gap-4 p-4 lg:flex-row lg:items-center">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={playback.togglePlayback}
              className="grid size-10 place-items-center rounded-xl border border-violet-400/20 bg-violet-400/[0.08] text-violet-300 transition hover:bg-violet-400/[0.14]"
              aria-label={playback.isPlaying ? "Pause playback" : "Play playback"}
            >
              {playback.isPlaying ? (
                <Pause size={17} fill="currentColor" />
              ) : (
                <Play size={17} fill="currentColor" />
              )}
            </button>

            <button
              type="button"
              onClick={playback.restart}
              className="grid size-10 place-items-center rounded-xl border border-white/[0.06] bg-white/[0.025] text-zinc-500 transition hover:bg-white/[0.05] hover:text-zinc-200"
              aria-label="Restart playback"
            >
              <RotateCcw size={16} />
            </button>
          </div>

          <div className="min-w-0 flex-1">
            <div className="mb-2 flex items-center justify-between gap-3">
              <div>
                <span className="text-[8px] font-semibold uppercase tracking-[0.14em] text-violet-400">
                  Runtime Playback
                </span>
                <strong className="ml-2 text-[11px] font-medium text-zinc-300">
                  {playback.currentStage.label}
                </strong>
              </div>

              <span className="text-[9px] tabular-nums text-zinc-600">
                {Math.round(playback.progress * 100)}%
              </span>
            </div>

            <div className="relative h-1 overflow-hidden rounded-full bg-white/[0.05]">
              <div
                className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-blue-400 via-violet-400 to-emerald-400 transition-[width] duration-75"
                style={{ width: `${playback.progress * 100}%` }}
              />
            </div>

            <div className="mt-3 grid grid-cols-5 gap-1">
              {playback.stages.map((stage, index) => {
                const reached =
                  index <= playback.currentStageIndex;

                return (
                  <button
                    key={stage.id}
                    type="button"
                    onClick={() => playback.goToStage(stage.id)}
                    className={[
                      "rounded-lg px-2 py-2 text-center transition",
                      index === playback.currentStageIndex
                        ? "bg-violet-400/[0.08] text-violet-300"
                        : reached
                          ? "text-zinc-400 hover:bg-white/[0.025]"
                          : "text-zinc-700 hover:bg-white/[0.02]",
                    ].join(" ")}
                  >
                    <span className="block text-[8px] font-semibold uppercase tracking-[0.08em]">
                      {stage.shortLabel}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex items-center gap-1 rounded-xl border border-white/[0.05] bg-black/10 p-1">
            {([0.5, 1, 2] as const).map((speed) => (
              <button
                key={speed}
                type="button"
                onClick={() => playback.setSpeed(speed)}
                className={[
                  "rounded-lg px-2.5 py-1.5 text-[9px] font-semibold transition",
                  playback.speed === speed
                    ? "bg-white/[0.07] text-zinc-200"
                    : "text-zinc-600 hover:text-zinc-300",
                ].join(" ")}
              >
                {speed}×
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* MAIN OPERATIONAL STORY */}
      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_330px]">
        {/* DIGITAL TWIN HERO */}
        <section className="relative min-h-[590px] overflow-hidden rounded-2xl border border-white/[0.055] bg-[#0b0e13]">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0"
          >
            <div className="absolute left-[12%] top-[15%] size-[380px] rounded-full bg-blue-500/[0.035] blur-[100px]" />
            <div className="absolute bottom-[4%] right-[8%] size-[420px] rounded-full bg-violet-500/[0.045] blur-[110px]" />
            <div
              className="absolute inset-0 opacity-[0.028]"
              style={{
                backgroundImage:
                  "linear-gradient(rgba(255,255,255,0.7) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.7) 1px, transparent 1px)",
                backgroundSize: "44px 44px",
              }}
            />
          </div>

          <header className="relative z-30 flex flex-col gap-4 border-b border-white/[0.05] px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="flex items-center gap-2 text-[9px] font-semibold uppercase tracking-[0.15em] text-zinc-600">
                <Radio
                  size={12}
                  strokeWidth={2}
                  className={
                    playback.isPlaying
                      ? "animate-pulse text-emerald-400"
                      : "text-zinc-600"
                  }
                />
                Digital Twin Runtime
              </div>

              <div className="mt-1.5 flex flex-wrap items-center gap-2">
                <h2 className="text-[16px] font-semibold tracking-[-0.015em] text-zinc-100">
                  Operational System View
                </h2>
                <span className="text-zinc-800">/</span>
                <span
                  className={[
                    "text-[9px] font-semibold tracking-[0.08em]",
                    story.accent,
                  ].join(" ")}
                >
                  {story.label}
                </span>
              </div>
            </div>

            <div className="inline-flex w-fit items-center gap-2 rounded-full border border-white/[0.06] bg-white/[0.025] px-3 py-1.5">
              <span
                className={[
                  "size-1.5 rounded-full",
                  playback.isPlaying
                    ? "animate-pulse bg-emerald-400"
                    : playback.isComplete
                      ? "bg-violet-400"
                      : "bg-zinc-600",
                ].join(" ")}
              />
              <span className="text-[9px] font-medium text-zinc-400">
                {playback.isIdle
                  ? "Ready to simulate"
                  : playback.isPlaying
                    ? "Simulation running"
                    : playback.isComplete
                      ? "Playback complete"
                      : "Playback paused"}
              </span>
            </div>
          </header>

          <div className="relative min-h-[510px] overflow-hidden">
            <div className="absolute left-5 top-5 z-20">
              <span className="text-[9px] font-semibold uppercase tracking-[0.14em] text-zinc-700">
                {playback.currentStage.shortLabel}
              </span>
              <p className="mt-1 max-w-[390px] text-[11px] text-zinc-500">
                {playback.currentStage.description}
              </p>
            </div>

            {/* CONNECTION NETWORK */}
            <svg
              viewBox="0 0 900 510"
              preserveAspectRatio="none"
              aria-hidden="true"
              className="pointer-events-none absolute inset-0 size-full"
            >
              <defs>
                <linearGradient
                  id="normal-flow"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="0"
                >
                  <stop
                    offset="0%"
                    stopColor="rgb(96 165 250)"
                    stopOpacity="0.15"
                  />
                  <stop
                    offset="100%"
                    stopColor="rgb(139 92 246)"
                    stopOpacity="0.65"
                  />
                </linearGradient>

                <linearGradient
                  id="alert-flow"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="0"
                >
                  <stop
                    offset="0%"
                    stopColor="rgb(251 191 36)"
                    stopOpacity="0.35"
                  />
                  <stop
                    offset="100%"
                    stopColor="rgb(248 113 113)"
                    stopOpacity="0.9"
                  />
                </linearGradient>

                <filter id="soft-glow">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              </defs>

              {playback.showOperationalWorld ? (
                <>
                  <path
                    d="M120 170 C205 170 220 170 295 170"
                    fill="none"
                    stroke="url(#normal-flow)"
                    strokeWidth="2"
                    strokeDasharray="5 7"
                  />
                  <path
                    d="M430 170 C500 170 530 170 600 170"
                    fill="none"
                    stroke="url(#normal-flow)"
                    strokeWidth="2"
                    strokeDasharray="5 7"
                  />
                </>
              ) : null}

              {showComparison ? (
                <path
                  d="M365 195 C365 240 365 255 365 305"
                  fill="none"
                  stroke={
                    showMismatch
                      ? "url(#alert-flow)"
                      : "url(#normal-flow)"
                  }
                  strokeWidth={showMismatch ? "3" : "2"}
                  strokeDasharray={showMismatch ? "7 5" : "5 7"}
                  filter={
                    showMismatch ? "url(#soft-glow)" : undefined
                  }
                />
              ) : null}

              {showTrace ? (
                <>
                  <path
                    d="M435 340 C515 340 545 325 610 300"
                    fill="none"
                    stroke={
                      showDecisionEffectTrace ||
                      playback.hasPropagation
                        ? "url(#alert-flow)"
                        : "url(#normal-flow)"
                    }
                    strokeWidth={
                      showDecisionEffectTrace ||
                      playback.hasPropagation
                        ? "3"
                        : "2"
                    }
                    strokeDasharray="7 6"
                    filter={
                      showDecisionEffectTrace ||
                      playback.hasPropagation
                        ? "url(#soft-glow)"
                        : undefined
                    }
                  />
                  <path
                    d="M670 195 C670 225 670 240 670 265"
                    fill="none"
                    stroke="url(#normal-flow)"
                    strokeWidth="2"
                    strokeDasharray="5 7"
                  />
                </>
              ) : null}

              {showTrust ? (
                <path
                  d="M735 300 C790 300 805 330 820 365"
                  fill="none"
                  stroke="url(#normal-flow)"
                  strokeWidth="2.5"
                  strokeDasharray="6 6"
                />
              ) : null}

              {showPropagation ? (
                <>
                  <path
                    d="M365 340 C460 415 570 420 665 360"
                    fill="none"
                    stroke="url(#alert-flow)"
                    strokeWidth="3"
                    strokeDasharray="8 5"
                    filter="url(#soft-glow)"
                  />
                  <circle
                    cx="500"
                    cy="405"
                    r="4"
                    fill="rgb(251 191 36)"
                    opacity="0.85"
                  >
                    <animate
                      attributeName="opacity"
                      values="0.25;1;0.25"
                      dur="1.2s"
                      repeatCount="indefinite"
                    />
                  </circle>
                </>
              ) : null}

              {showPropagation && hasMultipleEffects ? (
                <path
                  d="M365 340 C445 445 610 465 760 405"
                  fill="none"
                  stroke="rgb(167 139 250)"
                  strokeOpacity="0.45"
                  strokeWidth="2"
                  strokeDasharray="4 8"
                />
              ) : null}
            </svg>

            {/* REAL WORLD */}
            <button
              type="button"
              onClick={() =>
                setSelectedNode(
                  selectedNode === "real" ? null : "real",
                )
              }
              className={nodeButtonClass(
                "real",
                "left-[4%] top-[19%]",
                playback.showOperationalWorld,
              )}
            >
              <div className="flex items-center gap-3 rounded-2xl border border-blue-400/10 bg-[#10151c]/95 px-3.5 py-3 shadow-[0_12px_35px_rgba(0,0,0,0.24)] backdrop-blur">
                <div className="grid size-10 place-items-center rounded-xl border border-blue-400/10 bg-blue-400/[0.07] text-blue-400">
                  <Warehouse size={19} strokeWidth={1.7} />
                </div>
                <div>
                  <span className="block text-[8px] font-semibold uppercase tracking-[0.13em] text-blue-400/70">
                    Real World
                  </span>
                  <strong className="mt-1 block text-[11px] font-medium text-zinc-200">
                    Live Operations
                  </strong>
                </div>
              </div>
            </button>

            {/* VEHICLE */}
            <button
              type="button"
              onClick={() =>
                setSelectedNode(
                  selectedNode === "vehicle" ? null : "vehicle",
                )
              }
              className={nodeButtonClass(
                "vehicle",
                "left-[31%] top-[19%]",
                playback.showOperationalWorld,
              )}
            >
              <div
                className={[
                  "relative flex items-center gap-3 rounded-2xl border px-3.5 py-3 shadow-[0_12px_35px_rgba(0,0,0,0.25)] backdrop-blur transition-colors duration-500",
                  showMismatch
                    ? "border-amber-400/25 bg-amber-400/[0.075]"
                    : "border-emerald-400/12 bg-[#10151c]/95",
                ].join(" ")}
              >
                {showMismatch ? (
                  <span className="absolute -right-1.5 -top-1.5 flex size-4">
                    <span className="absolute inline-flex size-full animate-ping rounded-full bg-amber-400 opacity-20" />
                    <span className="relative grid size-4 place-items-center rounded-full border-2 border-[#0b0e13] bg-amber-400">
                      <AlertTriangle
                        size={8}
                        strokeWidth={3}
                        className="text-black"
                      />
                    </span>
                  </span>
                ) : null}

                <div
                  className={[
                    "grid size-11 place-items-center rounded-xl border",
                    showMismatch
                      ? "border-amber-400/15 bg-amber-400/[0.08] text-amber-300"
                      : "border-emerald-400/10 bg-emerald-400/[0.06] text-emerald-400",
                  ].join(" ")}
                >
                  <Truck size={21} strokeWidth={1.7} />
                </div>

                <div className="min-w-[90px]">
                  <span className="block text-[8px] font-semibold uppercase tracking-[0.13em] text-zinc-600">
                    Vehicle
                  </span>
                  <strong className="mt-1 block max-w-[120px] truncate text-[11px] font-medium text-zinc-100">
                    {humanize(vehicleId)}
                  </strong>
                  <span
                    className={[
                      "mt-1 block text-[9px]",
                      showMismatch
                        ? "text-amber-300"
                        : "text-emerald-400/80",
                    ].join(" ")}
                  >
                    {showMismatch
                      ? "Mismatch detected"
                      : "State observed"}
                  </span>
                </div>
              </div>
            </button>

            {/* ORDER */}
            <div
              className={[
                "absolute left-[66%] top-[19%] z-20 transition-all duration-500",
                playback.showOperationalWorld
                  ? "translate-y-0 opacity-100"
                  : "translate-y-3 opacity-0",
              ].join(" ")}
            >
              <div className="flex items-center gap-3 rounded-2xl border border-violet-400/10 bg-[#10151c]/95 px-3.5 py-3 shadow-[0_12px_35px_rgba(0,0,0,0.24)] backdrop-blur">
                <div className="grid size-10 place-items-center rounded-xl border border-violet-400/10 bg-violet-400/[0.06] text-violet-400">
                  <Box size={19} strokeWidth={1.7} />
                </div>
                <div>
                  <span className="block text-[8px] font-semibold uppercase tracking-[0.13em] text-zinc-600">
                    Order
                  </span>
                  <strong className="mt-1 block max-w-[120px] truncate text-[11px] font-medium text-zinc-200">
                    {humanize(orderId)}
                  </strong>
                </div>
              </div>
            </div>

            {/* EVENT */}
            {showEvent && !showComparison ? (
              <div className="absolute left-[37%] top-[45%] z-30 -translate-x-1/2 animate-pulse">
                <div className="flex items-center gap-2 rounded-full border border-blue-400/15 bg-blue-400/[0.06] px-3 py-1.5 text-[9px] font-medium text-blue-300 backdrop-blur">
                  <Activity size={11} />
                  Operational event observed
                </div>
              </div>
            ) : null}

            {/* COMPARISON */}
            {showComparison ? (
              <div className="absolute left-[37%] top-[45%] z-30 -translate-x-1/2">
                {showMismatch ? (
                  <button
                    type="button"
                    onClick={() =>
                      setSelectedNode(
                        selectedNode === "mismatch" ? null : "mismatch",
                      )
                    }
                    className={[
                      "flex items-center gap-2 rounded-full border border-amber-400/20 bg-[#17130c]/95 px-3 py-1.5 shadow-[0_0_30px_rgba(251,191,36,0.08)] backdrop-blur transition",
                      "hover:border-amber-300/35 hover:bg-amber-400/[0.10] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-300/50",
                      selectedNode === "mismatch" ? "ring-1 ring-amber-300/40" : "",
                    ].join(" ")}
                    aria-label="Inspect real-world and Digital Twin mismatch"
                  >
                    <AlertTriangle
                      size={12}
                      strokeWidth={2}
                      className="text-amber-400"
                    />
                    <span className="text-[9px] font-semibold text-amber-200">
                      Reality ≠ Twin
                    </span>
                  </button>
                ) : (
                  <div className="flex items-center gap-2 rounded-full border border-emerald-400/10 bg-[#0d1713]/90 px-3 py-1.5 backdrop-blur">
                    <Check
                      size={11}
                      strokeWidth={2.5}
                      className="text-emerald-400"
                    />
                    <span className="text-[9px] font-medium text-emerald-300/80">
                      Synchronized
                    </span>
                  </div>
                )}
              </div>
            ) : null}

            {/* DIGITAL TWIN */}
            <button
              type="button"
              onClick={() =>
                setSelectedNode(
                  selectedNode === "twin" ? null : "twin",
                )
              }
              className={nodeButtonClass(
                "twin",
                "left-[31%] top-[60%]",
                showComparison,
              )}
            >
              <div
                className={[
                  "flex items-center gap-3 rounded-2xl border px-3.5 py-3 shadow-[0_12px_35px_rgba(0,0,0,0.25)] backdrop-blur",
                  showMismatch
                    ? "border-amber-400/20 bg-[#15130f]/95"
                    : "border-cyan-400/12 bg-[#0e1519]/95",
                ].join(" ")}
              >
                <div
                  className={[
                    "grid size-11 place-items-center rounded-xl border",
                    showMismatch
                      ? "border-amber-400/15 bg-amber-400/[0.07] text-amber-300"
                      : "border-cyan-400/10 bg-cyan-400/[0.06] text-cyan-400",
                  ].join(" ")}
                >
                  <RefreshCw
                    size={21}
                    strokeWidth={1.7}
                    className={playback.isPlaying ? "animate-spin [animation-duration:3s]" : ""}
                  />
                </div>
                <div>
                  <span className="block text-[8px] font-semibold uppercase tracking-[0.13em] text-zinc-600">
                    Digital Twin
                  </span>
                  <strong className="mt-1 block text-[11px] font-medium text-zinc-100">
                    {showMismatch ? "State differs" : "Synchronized"}
                  </strong>
                  <span className="mt-1 block text-[9px] text-zinc-600">
                    Digital representation
                  </span>
                </div>
              </div>
            </button>

            {/* TRACE SIGNAL */}
            {showTrace ? (
              showPropagation ? (
                <div className="absolute bottom-[14%] left-[51%] z-30">
                  <button
                    type="button"
                    onClick={() =>
                      setSelectedNode(
                        selectedNode === "propagation" ? null : "propagation",
                      )
                    }
                    className={[
                      "flex items-center gap-2 rounded-full border border-amber-400/15 bg-amber-400/[0.055] px-3 py-1.5 backdrop-blur transition",
                      "hover:border-amber-300/30 hover:bg-amber-400/[0.10] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-300/50",
                      selectedNode === "propagation" ? "ring-1 ring-amber-300/40" : "",
                    ].join(" ")}
                    aria-label="Inspect knock-on effect"
                  >
                    <GitBranch
                      size={12}
                      strokeWidth={2}
                      className="text-amber-400"
                    />
                    <span className="text-[9px] font-medium text-amber-200">
                      Knock-on effect
                    </span>
                    <ArrowRight
                      size={11}
                      className="text-amber-500"
                    />
                  </button>
                </div>
              ) : playback.hasDivergence &&
                !mismatchAffectsDecision ? (
                <div className="absolute bottom-[14%] left-[49%] z-30">
                  <button
                    type="button"
                    onClick={() =>
                      setSelectedNode(
                        selectedNode === "propagation" ? null : "propagation",
                      )
                    }
                    className={[
                      "flex items-center gap-2 rounded-full border border-blue-400/12 bg-blue-400/[0.045] px-3 py-1.5 backdrop-blur transition",
                      "hover:border-blue-300/25 hover:bg-blue-400/[0.08] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-300/40",
                      selectedNode === "propagation" ? "ring-1 ring-blue-300/30" : "",
                    ].join(" ")}
                    aria-label="Inspect isolated issue"
                  >
                    <CircleDot
                      size={12}
                      className="text-blue-400"
                    />
                    <span className="text-[9px] font-medium text-blue-300">
                      Issue isolated
                    </span>
                  </button>
                </div>
              ) : null
            ) : null}

            {/* AI */}
            <button
              type="button"
              onClick={() =>
                setSelectedNode(
                  selectedNode === "decision" ? null : "decision",
                )
              }
              className={nodeButtonClass(
                "decision",
                "left-[66%] top-[54%]",
                showTrace,
              )}
            >
              <div
                className={[
                  "flex items-center gap-3 rounded-2xl border px-3.5 py-3 shadow-[0_12px_35px_rgba(0,0,0,0.28)] backdrop-blur",
                  mismatchAffectsDecision || showPropagation
                    ? "border-amber-400/20 bg-amber-400/[0.055]"
                    : "border-violet-400/15 bg-[#12101a]/95",
                ].join(" ")}
              >
                <div className="grid size-11 place-items-center rounded-xl border border-violet-400/15 bg-violet-400/[0.08] text-violet-300">
                  <Bot size={21} strokeWidth={1.7} />
                </div>
                <div>
                  <span className="block text-[8px] font-semibold uppercase tracking-[0.13em] text-violet-400/70">
                    AI Recommendation
                  </span>
                  <strong className="mt-1 block max-w-[150px] truncate text-[11px] font-medium text-zinc-100">
                    {action}
                  </strong>
                  <span className="mt-1 block text-[9px] text-zinc-600">
                    {showTrust
                      ? "Trust check complete"
                      : "Awaiting trust check"}
                  </span>
                </div>
              </div>
            </button>

            {/* DARA-DT */}
            <button
              type="button"
              onClick={() =>
                setSelectedNode(
                  selectedNode === "assurance"
                    ? null
                    : "assurance",
                )
              }
              className={nodeButtonClass(
                "assurance",
                "bottom-[7%] right-[4%]",
                showTrust,
              )}
            >
              <div
                className={[
                  "relative min-w-[175px] rounded-2xl border p-3.5 backdrop-blur",
                  trustPresentation
                    ? trustPresentation.borderClass
                    : "border-white/[0.07]",
                  trustPresentation
                    ? trustPresentation.backgroundClass
                    : "bg-white/[0.025]",
                  trustPresentation
                    ? trustPresentation.glowClass
                    : "",
                ].join(" ")}
              >
                <div className="flex items-center gap-2">
                  <div
                    className={[
                      "grid size-9 place-items-center rounded-xl border border-white/[0.06] bg-black/15",
                      trustPresentation?.textClass ??
                        "text-zinc-500",
                    ].join(" ")}
                  >
                    <ShieldCheck size={18} strokeWidth={1.8} />
                  </div>
                  <div>
                    <span className="block text-[8px] font-semibold uppercase tracking-[0.13em] text-zinc-600">
                      DARA-DT
                    </span>
                    <strong className="mt-0.5 block text-[10px] font-medium text-zinc-200">
                      AI Trust Check
                    </strong>
                  </div>
                </div>

                <div
                  className={[
                    "mt-3 text-[15px] font-bold tracking-[0.03em]",
                    trustPresentation?.textClass ??
                      "text-zinc-500",
                  ].join(" ")}
                >
                  {trustPresentation?.label ?? "NO RESULT"}
                </div>
              </div>
            </button>

            {/* INTERACTIVE OBJECT INSPECTOR */}
            {selectedNode ? (
              <div className="absolute bottom-4 left-4 z-40 w-[min(390px,calc(100%-2rem))] rounded-2xl border border-white/[0.08] bg-[#0f1218]/95 p-4 shadow-2xl backdrop-blur-xl">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <span className="text-[8px] font-semibold uppercase tracking-[0.14em] text-violet-400">
                      Object Inspector
                    </span>
                    <strong className="mt-1 block truncate text-[12px] font-semibold text-zinc-100">
                      {selectedNode === "real" && "Real-World Operations"}
                      {selectedNode === "vehicle" && humanize(vehicleId)}
                      {selectedNode === "mismatch" && "Reality vs Digital Twin"}
                      {selectedNode === "twin" && "Digital Twin"}
                      {selectedNode === "propagation" &&
                        (showPropagation ? "Knock-on Effect" : "Issue Isolation")}
                      {selectedNode === "decision" && "AI Recommendation"}
                      {selectedNode === "assurance" && "DARA-DT Trust Check"}
                    </strong>
                  </div>
                  <button
                    type="button"
                    aria-label="Close object inspector"
                    onClick={() => setSelectedNode(null)}
                    className="grid size-7 shrink-0 place-items-center rounded-lg border border-white/[0.05] bg-white/[0.025] text-zinc-600 transition hover:bg-white/[0.05] hover:text-zinc-200"
                  >
                    ×
                  </button>
                </div>

                <div className="mt-3 border-t border-white/[0.05] pt-3">
                  {selectedNode === "real" ? (
                    <div className="space-y-3">
                      <p className="text-[10px] leading-5 text-zinc-400">
                        The physical logistics state represented by this frozen research scenario.
                        DARA-DT compares this state with its Digital Twin before judging the AI recommendation.
                      </p>
                      <div className="grid grid-cols-2 gap-2">
                        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5">
                          <span className="block text-[8px] uppercase tracking-[0.12em] text-zinc-700">
                            Scenario
                          </span>
                          <strong className="mt-1 block text-[10px] text-zinc-300">
                            {scenario.scenario_id}
                          </strong>
                        </div>
                        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5">
                          <span className="block text-[8px] uppercase tracking-[0.12em] text-zinc-700">
                            Mismatches
                          </span>
                          <strong className="mt-1 block text-[10px] text-zinc-300">
                            {scenario.divergences.length}
                          </strong>
                        </div>
                      </div>
                    </div>
                  ) : null}

                  {selectedNode === "vehicle" ? (
                    <div className="space-y-3">
                      <p className="text-[10px] leading-5 text-zinc-400">
                        {showMismatch
                          ? "DARA-DT has detected a difference involving this vehicle."
                          : "This vehicle is currently represented consistently across the real-world and Digital Twin states."}
                      </p>
                      <div className="flex flex-wrap gap-2">
                        <span className="rounded-full border border-white/[0.06] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-400">
                          {humanize(vehicleId)}
                        </span>
                        <span className={[
                          "rounded-full border px-2.5 py-1 text-[9px]",
                          showMismatch
                            ? "border-amber-400/15 bg-amber-400/[0.05] text-amber-300"
                            : "border-emerald-400/12 bg-emerald-400/[0.04] text-emerald-300",
                        ].join(" ")}>
                          {showMismatch ? "Mismatch detected" : "State aligned"}
                        </span>
                      </div>
                    </div>
                  ) : null}

                  {selectedNode === "mismatch" ? (
                    <div className="space-y-3">
                      {selectedDivergence ? (
                        <>
                          <div className="grid grid-cols-2 gap-2">
                            <div className="rounded-xl border border-blue-400/10 bg-blue-400/[0.035] p-2.5">
                              <span className="block text-[8px] uppercase tracking-[0.12em] text-blue-400/70">
                                Real World
                              </span>
                              <strong className="mt-1 block break-words text-[10px] text-zinc-200">
                                {String(selectedDivergence.physical_value)}
                              </strong>
                            </div>
                            <div className="rounded-xl border border-violet-400/10 bg-violet-400/[0.035] p-2.5">
                              <span className="block text-[8px] uppercase tracking-[0.12em] text-violet-400/70">
                                Digital Twin
                              </span>
                              <strong className="mt-1 block break-words text-[10px] text-zinc-200">
                                {String(selectedDivergence.twin_value)}
                              </strong>
                            </div>
                          </div>
                          <div className="rounded-xl border border-amber-400/12 bg-amber-400/[0.04] p-3">
                            <span className="block text-[8px] uppercase tracking-[0.12em] text-amber-400/70">
                              Variable
                            </span>
                            <strong className="mt-1 block text-[10px] text-amber-200">
                              {humanize(selectedDivergence.variable)}
                            </strong>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            <span className={[
                              "rounded-full border px-2.5 py-1 text-[9px]",
                              selectedDivergence.decision_relevant
                                ? "border-red-400/15 bg-red-400/[0.05] text-red-300"
                                : "border-blue-400/12 bg-blue-400/[0.04] text-blue-300",
                            ].join(" ")}>
                              {selectedDivergence.decision_relevant
                                ? "Affects information used by AI"
                                : "Not required by this AI decision"}
                            </span>
                            <span className={[
                              "rounded-full border px-2.5 py-1 text-[9px]",
                              selectedDivergence.decision_impacting
                                ? "border-amber-400/15 bg-amber-400/[0.05] text-amber-300"
                                : "border-white/[0.06] bg-white/[0.025] text-zinc-500",
                            ].join(" ")}>
                              {selectedDivergence.decision_impacting
                                ? "Could change recommendation"
                                : "No direct decision impact"}
                            </span>
                          </div>
                        </>
                      ) : (
                        <p className="text-[10px] leading-5 text-zinc-500">
                          No divergence record is present in this scenario.
                        </p>
                      )}
                    </div>
                  ) : null}

                  {selectedNode === "twin" ? (
                    <div className="space-y-3">
                      <p className="text-[10px] leading-5 text-zinc-400">
                        {showMismatch
                          ? "The Digital Twin differs from the represented physical state. The mismatch is evaluated for decision relevance and impact before authority is assigned."
                          : "The Digital Twin currently agrees with the represented physical state."}
                      </p>
                      <div className="flex items-center gap-2 rounded-xl border border-white/[0.05] bg-white/[0.02] p-3">
                        <RefreshCw size={14} className={showMismatch ? "text-amber-300" : "text-cyan-400"} />
                        <span className="text-[10px] text-zinc-300">
                          {showMismatch ? "State comparison: different" : "State comparison: synchronized"}
                        </span>
                      </div>
                    </div>
                  ) : null}

                  {selectedNode === "propagation" ? (
                    <div className="space-y-3">
                      <p className="text-[10px] leading-5 text-zinc-400">
                        {showPropagation
                          ? "The mismatch has a research-backed propagation relationship into the current decision context."
                          : "A mismatch exists, but the research model does not propagate it into the current AI recommendation."}
                      </p>
                      <div className="grid grid-cols-3 gap-2">
                        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5 text-center">
                          <strong className="block text-[13px] text-zinc-200">
                            {scenario.divergences.length}
                          </strong>
                          <span className="mt-1 block text-[7px] uppercase tracking-[0.10em] text-zinc-700">
                            Mismatch
                          </span>
                        </div>
                        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5 text-center">
                          <strong className="block text-[13px] text-zinc-200">
                            {impactingDivergences.length}
                          </strong>
                          <span className="mt-1 block text-[7px] uppercase tracking-[0.10em] text-zinc-700">
                            Affects AI
                          </span>
                        </div>
                        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5 text-center">
                          <strong className="block text-[13px] text-zinc-200">
                            {propagatingRecords.length}
                          </strong>
                          <span className="mt-1 block text-[7px] uppercase tracking-[0.10em] text-zinc-700">
                            Knock-on
                          </span>
                        </div>
                      </div>
                      {propagatingRecords.length > 0 ? (
                        <div className="space-y-2">
                          {propagatingRecords.slice(0, 3).map((record, index) => (
                            <div
                              key={`${record.source_decision}-${record.target_decision}-${index}`}
                              className="rounded-xl border border-amber-400/10 bg-amber-400/[0.035] p-2.5"
                            >
                              <span className="block text-[8px] uppercase tracking-[0.11em] text-amber-400/70">
                                Propagation {index + 1}
                              </span>
                              <span className="mt-1 block text-[9px] leading-4 text-zinc-400">
                                {humanize(record.affected_dependency ?? "Unknown dependency")}
                              </span>
                            </div>
                          ))}
                        </div>
                      ) : null}
                    </div>
                  ) : null}

                  {selectedNode === "decision" ? (
                    <div className="space-y-3">
                      <p className="text-[10px] leading-5 text-zinc-400">
                        The AI recommends <span className="font-medium text-violet-300">{action}</span>.
                        DARA-DT checks whether the information supporting this recommendation remains trustworthy enough to grant authority.
                      </p>
                      <div className="grid grid-cols-2 gap-2">
                        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5">
                          <span className="block text-[8px] uppercase tracking-[0.12em] text-zinc-700">
                            Vehicle
                          </span>
                          <strong className="mt-1 block text-[10px] text-zinc-300">
                            {humanize(vehicleId)}
                          </strong>
                        </div>
                        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5">
                          <span className="block text-[8px] uppercase tracking-[0.12em] text-zinc-700">
                            Order
                          </span>
                          <strong className="mt-1 block text-[10px] text-zinc-300">
                            {humanize(orderId)}
                          </strong>
                        </div>
                      </div>
                      <div>
                        <span className="text-[8px] uppercase tracking-[0.12em] text-zinc-700">
                          Information used by AI
                        </span>
                        <div className="mt-2 flex flex-wrap gap-1.5">
                          {scenario.ai_decision.dependencies.slice(0, 6).map((dependency, index) => (
                            <span
                              key={`${dependency.dependency}-${index}`}
                              className="rounded-full border border-violet-400/10 bg-violet-400/[0.04] px-2 py-1 text-[8px] text-violet-300/80"
                            >
                              {humanize(dependency.dependency)}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : null}

                  {selectedNode === "assurance" ? (
                    <div className="space-y-3">
                      <div className={[
                        "rounded-xl border p-3",
                        trustPresentation?.borderClass ?? "border-white/[0.05]",
                        trustPresentation?.backgroundClass ?? "bg-white/[0.02]",
                      ].join(" ")}>
                        <span className="block text-[8px] uppercase tracking-[0.12em] text-zinc-600">
                          AI Permission
                        </span>
                        <strong className={[
                          "mt-1 block text-[15px]",
                          trustPresentation?.textClass ?? "text-zinc-300",
                        ].join(" ")}>
                          {trustPresentation?.label ?? "PENDING"}
                        </strong>
                        <span className="mt-1 block text-[9px] text-zinc-400">
                          {trustPresentation?.description ?? "Trust result not yet available"}
                        </span>
                      </div>
                      <p className="text-[10px] leading-5 text-zinc-400">
                        {primaryAssurance?.reason ?? "DARA-DT has not revealed the assurance result yet."}
                      </p>
                      <div className="flex flex-wrap gap-2">
                        <span className="rounded-full border border-white/[0.06] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-500">
                          {relevantDivergences.length} decision-relevant
                        </span>
                        <span className="rounded-full border border-white/[0.06] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-500">
                          {impactingDivergences.length} decision-impacting
                        </span>
                        <span className="rounded-full border border-white/[0.06] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-500">
                          {scenario.assurance_results.length} methods evaluated
                        </span>
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            ) : null}
          </div>
        </section>

        {/* AI RECOMMENDATION + TRUST */}
        <aside className="flex flex-col overflow-hidden rounded-2xl border border-white/[0.055] bg-[#0c0f14]">
          <div className="border-b border-white/[0.05] p-5">
            <div className="flex items-center justify-between">
              <span className="text-[9px] font-semibold uppercase tracking-[0.14em] text-violet-400">
                AI Wants To
              </span>
              <div className="grid size-8 place-items-center rounded-lg border border-violet-400/10 bg-violet-400/[0.055] text-violet-400">
                <Bot size={16} strokeWidth={1.8} />
              </div>
            </div>

            <h2 className="mt-3 text-[20px] font-semibold leading-tight tracking-[-0.025em] text-zinc-100">
              {showTrace ? action : "Analysing recommendation…"}
            </h2>

            <div className="mt-5 flex items-center gap-2">
              <div className="min-w-0 flex-1 rounded-xl border border-white/[0.055] bg-white/[0.025] p-3">
                <Truck size={16} className="text-blue-400" />
                <span className="mt-2 block text-[8px] uppercase tracking-[0.12em] text-zinc-700">
                  Vehicle
                </span>
                <strong className="mt-1 block truncate text-[11px] font-medium text-zinc-300">
                  {humanize(vehicleId)}
                </strong>
              </div>

              <ArrowRight
                size={14}
                className="shrink-0 text-violet-400"
              />

              <div className="min-w-0 flex-1 rounded-xl border border-white/[0.055] bg-white/[0.025] p-3">
                <Box size={16} className="text-violet-400" />
                <span className="mt-2 block text-[8px] uppercase tracking-[0.12em] text-zinc-700">
                  Order
                </span>
                <strong className="mt-1 block truncate text-[11px] font-medium text-zinc-300">
                  {humanize(orderId)}
                </strong>
              </div>
            </div>
          </div>

          <div className="flex flex-1 flex-col p-5">
            <div className="flex items-center gap-2">
              <ShieldCheck
                size={14}
                strokeWidth={1.9}
                className="text-zinc-500"
              />
              <span className="text-[9px] font-semibold uppercase tracking-[0.14em] text-zinc-600">
                DARA-DT Trust Check
              </span>
            </div>

            {showTrust &&
            trustPresentation &&
            primaryAssurance ? (
              <>
                <div
                  className={[
                    "mt-4 rounded-2xl border p-5",
                    trustPresentation.borderClass,
                    trustPresentation.backgroundClass,
                    trustPresentation.glowClass,
                  ].join(" ")}
                >
                  <div
                    className={[
                      "grid size-12 place-items-center rounded-2xl border border-white/[0.07] bg-black/15",
                      trustPresentation.textClass,
                    ].join(" ")}
                  >
                    {primaryAssurance.authority === "allow" ? (
                      <Check size={24} strokeWidth={2.2} />
                    ) : primaryAssurance.authority ===
                      "fallback" ? (
                      <RefreshCw size={22} strokeWidth={1.8} />
                    ) : (
                      <AlertTriangle size={22} strokeWidth={1.8} />
                    )}
                  </div>

                  <div
                    className={[
                      "mt-4 text-[22px] font-bold tracking-[0.02em]",
                      trustPresentation.textClass,
                    ].join(" ")}
                  >
                    {trustPresentation.label}
                  </div>

                  <p className="mt-1 text-[12px] font-medium text-zinc-300">
                    {trustPresentation.description}
                  </p>

                  <div className="mt-4 h-px bg-white/[0.06]" />

                  <div className="mt-4 flex items-start gap-2">
                    <Activity
                      size={13}
                      className="mt-0.5 shrink-0 text-zinc-600"
                    />
                    <span className="text-[10px] leading-5 text-zinc-500">
                      {trustPresentation.action}
                    </span>
                  </div>
                </div>

                <div className="mt-4 grid grid-cols-3 gap-2">
                  <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5 text-center">
                    <strong className="block text-[17px] font-semibold text-amber-300">
                      {scenario.divergences.length}
                    </strong>
                    <span className="mt-1 block text-[8px] uppercase tracking-[0.08em] text-zinc-700">
                      Mismatch
                    </span>
                  </div>
                  <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5 text-center">
                    <strong className="block text-[17px] font-semibold text-red-300">
                      {impactingDivergences.length}
                    </strong>
                    <span className="mt-1 block text-[8px] uppercase tracking-[0.08em] text-zinc-700">
                      Affects AI
                    </span>
                  </div>
                  <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-2.5 text-center">
                    <strong className="block text-[17px] font-semibold text-violet-300">
                      {propagatingRecords.length}
                    </strong>
                    <span className="mt-1 block text-[8px] uppercase tracking-[0.08em] text-zinc-700">
                      Knock-on
                    </span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    setShowExplanation(!showExplanation)
                  }
                  className="mt-auto flex w-full items-center justify-between rounded-xl border border-white/[0.06] bg-white/[0.025] px-3.5 py-3 text-left transition-all hover:border-violet-400/15 hover:bg-violet-400/[0.04]"
                >
                  <span className="flex items-center gap-2 text-[10px] font-medium text-zinc-400">
                    <Info
                      size={14}
                      className="text-violet-400"
                    />
                    Why this decision?
                  </span>
                  <ChevronRight
                    size={14}
                    className={[
                      "text-zinc-600 transition-transform",
                      showExplanation ? "rotate-90" : "",
                    ].join(" ")}
                  />
                </button>
              </>
            ) : (
              <div className="mt-4 flex flex-1 flex-col justify-center rounded-2xl border border-dashed border-white/[0.07] bg-white/[0.018] p-5 text-center">
                <div className="mx-auto grid size-12 place-items-center rounded-2xl border border-violet-400/10 bg-violet-400/[0.04] text-violet-400">
                  <Activity
                    size={20}
                    className={
                      playback.isPlaying ? "animate-pulse" : ""
                    }
                  />
                </div>
                <strong className="mt-4 block text-sm text-zinc-300">
                  Trust result pending
                </strong>
                <p className="mt-2 text-[10px] leading-5 text-zinc-600">
                  Run the playback through Compare and Trace. DARA-DT
                  reveals AI permission at the Trust stage.
                </p>
              </div>
            )}
          </div>
        </aside>
      </div>

      {/* PROGRESSIVE EXPLANATION */}
      {showExplanation &&
      showTrust &&
      primaryAssurance ? (
        <section className="overflow-hidden rounded-2xl border border-violet-400/10 bg-violet-400/[0.025]">
          <div className="grid gap-0 lg:grid-cols-[220px_minmax(0,1fr)]">
            <div className="border-b border-white/[0.05] p-5 lg:border-b-0 lg:border-r">
              <div className="grid size-9 place-items-center rounded-xl border border-violet-400/10 bg-violet-400/[0.06] text-violet-400">
                <Network size={17} strokeWidth={1.8} />
              </div>
              <span className="mt-4 block text-[9px] font-semibold uppercase tracking-[0.14em] text-violet-400">
                Decision Explanation
              </span>
              <h3 className="mt-1 text-[13px] font-semibold text-zinc-200">
                Why DARA-DT decided this
              </h3>
            </div>

            <div className="p-5">
              <p className="max-w-4xl text-[11px] leading-6 text-zinc-400">
                {primaryAssurance.reason}
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                <span className="rounded-full border border-white/[0.055] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-600">
                  {relevantDivergences.length} decision-relevant
                </span>
                <span className="rounded-full border border-white/[0.055] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-600">
                  {impactingDivergences.length} decision-impacting
                </span>
                <span className="rounded-full border border-white/[0.055] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-600">
                  {propagatingRecords.length} propagating
                </span>
                <span className="rounded-full border border-white/[0.055] bg-white/[0.025] px-2.5 py-1 text-[9px] text-zinc-600">
                  {scenario.assurance_results.length} methods evaluated
                </span>
              </div>
            </div>
          </div>
        </section>
      ) : null}

      {/* INFORMATION HEALTH + DECISION STORY */}
      <div className="grid gap-4 lg:grid-cols-2">
        <section className="rounded-2xl border border-white/[0.055] bg-[#0c0f14] p-5">
          <header className="flex items-center justify-between">
            <div>
              <span className="text-[9px] font-semibold uppercase tracking-[0.14em] text-zinc-600">
                Information Health
              </span>
              <h3 className="mt-1 text-[13px] font-semibold text-zinc-200">
                What the AI can trust
              </h3>
            </div>
            <Activity
              size={17}
              strokeWidth={1.7}
              className="text-zinc-600"
            />
          </header>

          {showEvent && scenario.runtime_evidence.length > 0 ? (
            <div className="mt-4 grid gap-2 sm:grid-cols-2">
              {scenario.runtime_evidence
                .slice(0, 6)
                .map((evidence, index) => {
                  const presentation =
                    evidencePresentation(evidence.status);
                  const EvidenceIcon = presentation.icon;

                  return (
                    <div
                      key={`${evidence.source}-${evidence.dependency}-${index}`}
                      className="group flex items-center gap-3 rounded-xl border border-white/[0.045] bg-white/[0.018] p-3"
                    >
                      <div
                        className={[
                          "grid size-8 shrink-0 place-items-center rounded-lg border border-white/[0.05] bg-black/10",
                          presentation.textClass,
                        ].join(" ")}
                      >
                        <EvidenceIcon
                          size={14}
                          strokeWidth={1.8}
                        />
                      </div>
                      <div className="min-w-0 flex-1">
                        <strong className="block truncate text-[10px] font-medium text-zinc-300">
                          {humanize(evidence.dependency)}
                        </strong>
                        <div className="mt-1 flex items-center gap-1.5">
                          <span
                            className={[
                              "size-1.5 rounded-full",
                              presentation.dotClass,
                            ].join(" ")}
                          />
                          <span
                            className={[
                              "text-[9px]",
                              presentation.textClass,
                            ].join(" ")}
                          >
                            {presentation.label}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
            </div>
          ) : (
            <div className="mt-4 rounded-xl border border-dashed border-white/[0.06] p-5 text-center text-[10px] text-zinc-600">
              Information appears as the operational event is observed.
            </div>
          )}
        </section>

        <section className="rounded-2xl border border-white/[0.055] bg-[#0c0f14] p-5">
          <header className="flex items-center justify-between">
            <div>
              <span className="text-[9px] font-semibold uppercase tracking-[0.14em] text-zinc-600">
                Decision Path
              </span>
              <h3 className="mt-1 text-[13px] font-semibold text-zinc-200">
                What just happened
              </h3>
            </div>
            <Route
              size={17}
              strokeWidth={1.7}
              className="text-zinc-600"
            />
          </header>

          <div className="mt-7 grid grid-cols-5 items-start">
            {playback.stages.map((stage, index) => {
              const reached =
                index <= playback.currentStageIndex;
              const active =
                index === playback.currentStageIndex;

              return (
                <button
                  key={stage.id}
                  type="button"
                  onClick={() => playback.goToStage(stage.id)}
                  className="relative flex flex-col items-center text-center"
                >
                  {index > 0 ? (
                    <span
                      className={[
                        "absolute right-1/2 top-[17px] h-px w-full",
                        reached
                          ? "bg-violet-400/35"
                          : "bg-white/[0.05]",
                      ].join(" ")}
                    />
                  ) : null}

                  <span
                    className={[
                      "relative z-10 grid size-9 place-items-center rounded-xl border transition-all",
                      active
                        ? "border-violet-400/25 bg-violet-400/[0.10] text-violet-300 shadow-[0_0_25px_rgba(139,92,246,0.10)]"
                        : reached
                          ? "border-emerald-400/10 bg-emerald-400/[0.04] text-emerald-400"
                          : "border-white/[0.05] bg-[#0c0f14] text-zinc-700",
                    ].join(" ")}
                  >
                    {stage.id === "observe" ? (
                      <Truck size={14} />
                    ) : stage.id === "event" ? (
                      <Activity size={14} />
                    ) : stage.id === "compare" ? (
                      <RefreshCw size={14} />
                    ) : stage.id === "trace" ? (
                      <GitBranch size={14} />
                    ) : (
                      <ShieldCheck size={14} />
                    )}
                  </span>

                  <span
                    className={[
                      "mt-2 text-[8px] font-medium",
                      active
                        ? "text-violet-300"
                        : reached
                          ? "text-zinc-500"
                          : "text-zinc-700",
                    ].join(" ")}
                  >
                    {stage.shortLabel}
                  </span>
                </button>
              );
            })}
          </div>

          {showTrust ? (
            <div
              className={[
                "mt-6 flex items-start gap-3 rounded-xl border p-3.5",
                mismatchAffectsDecision
                  ? "border-amber-400/10 bg-amber-400/[0.035]"
                  : "border-emerald-400/10 bg-emerald-400/[0.03]",
              ].join(" ")}
            >
              {mismatchAffectsDecision ? (
                <Zap
                  size={15}
                  className="mt-0.5 shrink-0 text-amber-400"
                />
              ) : (
                <CheckCircle2
                  size={15}
                  className="mt-0.5 shrink-0 text-emerald-400"
                />
              )}

              <span className="text-[10px] leading-5 text-zinc-500">
                {!playback.hasDivergence
                  ? "Real-world and Digital Twin states agree."
                  : mismatchAffectsDecision
                    ? playback.hasPropagation
                      ? "A mismatch has a connected effect that could change this AI decision."
                      : "A mismatch directly affects information used by this AI decision."
                    : "A mismatch exists, but it does not currently affect this AI decision."}
              </span>
            </div>
          ) : (
            <div className="mt-6 rounded-xl border border-dashed border-white/[0.05] p-3.5 text-center text-[9px] text-zinc-700">
              Follow the playback to reveal the decision outcome.
            </div>
          )}
        </section>
      </div>

      {/* RESEARCH TRACEABILITY */}
      <footer className="flex flex-col gap-2 border-t border-white/[0.04] px-1 pt-3 text-[9px] text-zinc-700 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <CircleDot size={10} />
          <span>Research traceability</span>
          <span className="text-zinc-800">/</span>
          <strong className="font-medium text-zinc-600">
            EXP-010 / {scenario.scenario_id}
          </strong>
        </div>

        <span>
          {scenario.assurance_results.length} assurance methods evaluated
        </span>
      </footer>
    </section>
  );
}

export default ScenarioWorkspace;
