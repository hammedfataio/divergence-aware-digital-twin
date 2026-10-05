import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  CircleDot,
  GitBranch,
  Layers3,
  LoaderCircle,
  Radio,
  ShieldAlert,
  Sparkles,
} from "lucide-react";


interface ScenarioControlProps {
  scenarios: string[];
  selectedScenario: string;
  runningScenario: boolean;
  error: string | null;
  onScenarioChange: (scenarioId: string) => void;
  onRunScenario: () => void;
}


interface SituationFamily {
  id: string;
  shortLabel: string;
  title: string;
  description: string;
  icon: typeof CheckCircle2;
  accent: string;
  activeAccent: string;
  dot: string;
}


interface SituationPresentation {
  title: string;
  description: string;
  context: string;
}


const situationFamilies: SituationFamily[] = [
  {
    id: "F0",
    shortLabel: "NORMAL",
    title: "Normal Operations",
    description: "Everything is operating as expected.",
    icon: CheckCircle2,
    accent: "text-emerald-400",
    activeAccent:
      "border-emerald-400/20 bg-emerald-400/[0.07] shadow-[inset_0_0_0_1px_rgba(52,211,153,0.04)]",
    dot: "bg-emerald-400",
  },
  {
    id: "F1",
    shortLabel: "CURRENT ISSUE",
    title: "Current Decision Issue",
    description: "A problem directly affects this AI decision.",
    icon: ShieldAlert,
    accent: "text-red-400",
    activeAccent:
      "border-red-400/20 bg-red-400/[0.07] shadow-[inset_0_0_0_1px_rgba(248,113,113,0.04)]",
    dot: "bg-red-400",
  },
  {
    id: "F2",
    shortLabel: "ELSEWHERE",
    title: "Issue Elsewhere",
    description: "A problem exists, but this decision is unaffected.",
    icon: CircleDot,
    accent: "text-blue-400",
    activeAccent:
      "border-blue-400/20 bg-blue-400/[0.07] shadow-[inset_0_0_0_1px_rgba(96,165,250,0.04)]",
    dot: "bg-blue-400",
  },
  {
    id: "F3",
    shortLabel: "KNOCK-ON",
    title: "Knock-on Risk",
    description: "A problem may propagate into this decision.",
    icon: GitBranch,
    accent: "text-amber-400",
    activeAccent:
      "border-amber-400/20 bg-amber-400/[0.07] shadow-[inset_0_0_0_1px_rgba(251,191,36,0.04)]",
    dot: "bg-amber-400",
  },
  {
    id: "F4",
    shortLabel: "MULTIPLE",
    title: "Multiple Risks",
    description: "Several connected effects may be involved.",
    icon: Layers3,
    accent: "text-violet-400",
    activeAccent:
      "border-violet-400/20 bg-violet-400/[0.07] shadow-[inset_0_0_0_1px_rgba(167,139,250,0.04)]",
    dot: "bg-violet-400",
  },
];


const situations: Record<string, SituationPresentation> = {
  "F0-A": {
    title: "Normal Vehicle Assignment",
    description:
      "The operation is synchronized and the information needed for the vehicle assignment is available.",
    context: "Information available",
  },
  "F0-B": {
    title: "Assignment Constraint Detected",
    description:
      "The real operation and digital twin agree, but an operational constraint may prevent the planned assignment.",
    context: "Operational constraint",
  },
  "F0-C": {
    title: "Outdated Operational Information",
    description:
      "The operation is synchronized, but some information being used to check the assignment may be outdated.",
    context: "Outdated information",
  },
  "F0-D": {
    title: "Missing Operational Information",
    description:
      "The operation is synchronized, but some information needed to verify the assignment is unavailable.",
    context: "Missing information",
  },
  "F0-E": {
    title: "Conflicting Operational Information",
    description:
      "The operation is synchronized, but available information does not agree.",
    context: "Conflicting information",
  },
  "F0-F": {
    title: "Repeated Normal Operation",
    description:
      "A repeated normal operating situation used to check that DARA-DT behaves consistently.",
    context: "Information available",
  },

  "F1-A": {
    title: "Vehicle Breakdown",
    description:
      "Vehicle A has failed in the real world while its digital record still shows it as operational.",
    context: "Vehicle status mismatch",
  },
  "F1-B": {
    title: "Vehicle Capacity Changed",
    description:
      "Vehicle A has less real-world capacity than the digital twin currently reports.",
    context: "Vehicle capacity mismatch",
  },
  "F1-C": {
    title: "Vehicle No Longer Available",
    description:
      "Vehicle A is unavailable in the real operation while its digital record still shows it as available.",
    context: "Vehicle availability mismatch",
  },
  "F1-D": {
    title: "Vehicle Breakdown with Outdated Information",
    description:
      "Vehicle A has failed and some supporting operational information is also outdated.",
    context: "Breakdown + outdated information",
  },
  "F1-E": {
    title: "Vehicle Breakdown with Missing Information",
    description:
      "Vehicle A has failed and some supporting information needed to check the decision is missing.",
    context: "Breakdown + missing information",
  },
  "F1-F": {
    title: "Vehicle Breakdown with Conflicting Information",
    description:
      "Vehicle A has failed while available information about the operation conflicts.",
    context: "Breakdown + conflicting information",
  },

  "F2-A": {
    title: "Location Issue Elsewhere",
    description:
      "Vehicle A is in a different location from its digital record, but the issue does not affect the current AI recommendation.",
    context: "No effect on current decision",
  },
  "F2-B": {
    title: "Capacity Issue Elsewhere",
    description:
      "Vehicle A's capacity differs from its digital record, but the issue does not affect the current AI recommendation.",
    context: "No effect on current decision",
  },
  "F2-C": {
    title: "Vehicle Status Issue Elsewhere",
    description:
      "Vehicle A's real-world status differs from its digital record, but the current AI recommendation does not depend on it.",
    context: "No effect on current decision",
  },
  "F2-D": {
    title: "Unrelated Issue with Outdated Information",
    description:
      "A location issue exists elsewhere and does not affect the current recommendation, while some information is outdated.",
    context: "Unrelated + outdated information",
  },
  "F2-E": {
    title: "Unrelated Issue with Missing Information",
    description:
      "A location issue exists elsewhere and does not affect the current recommendation, while some information is missing.",
    context: "Unrelated + missing information",
  },
  "F2-F": {
    title: "Unrelated Issue with Conflicting Information",
    description:
      "A location issue exists elsewhere and does not affect the current recommendation, while some information conflicts.",
    context: "Unrelated + conflicting information",
  },

  "F3-A": {
    title: "Breakdown May Affect Another Assignment",
    description:
      "Vehicle A has broken down. DARA-DT will check whether this changes the resources needed for another AI-managed assignment.",
    context: "Possible knock-on effect",
  },
  "F3-B": {
    title: "Unavailable Vehicle May Affect Recovery",
    description:
      "Vehicle A is unavailable. DARA-DT will check whether this affects resources needed elsewhere in the operation.",
    context: "Possible knock-on effect",
  },
  "F3-C": {
    title: "Vehicle Location May Delay Recovery",
    description:
      "Vehicle A is somewhere different from its digital record. This may affect the timing assumed by another decision.",
    context: "Possible timing effect",
  },
  "F3-D": {
    title: "Knock-on Risk with Outdated Information",
    description:
      "A vehicle failure may affect another decision while some supporting operational information is outdated.",
    context: "Knock-on risk + outdated information",
  },
  "F3-E": {
    title: "Knock-on Risk with Missing Information",
    description:
      "A vehicle failure may affect another decision while some supporting operational information is unavailable.",
    context: "Knock-on risk + missing information",
  },
  "F3-F": {
    title: "Knock-on Risk with Conflicting Information",
    description:
      "A vehicle failure may affect another decision while available operational information conflicts.",
    context: "Knock-on risk + conflicting information",
  },

  "F4-A": {
    title: "Breakdown May Affect Multiple Vehicles",
    description:
      "Vehicle A has failed and the disruption may affect the availability or assignment of other vehicles.",
    context: "Multiple connected effects",
  },
  "F4-B": {
    title: "Breakdown May Affect Capacity and Recovery",
    description:
      "Vehicle A has failed and the disruption may affect both available capacity and recovery demand.",
    context: "Multiple connected effects",
  },
  "F4-C": {
    title: "Location Issue May Affect Timing and Deadline",
    description:
      "Vehicle A's real location differs from its digital record and may affect both recovery timing and an order deadline.",
    context: "Multiple timing effects",
  },
  "F4-D": {
    title: "Multiple Risks with Outdated Information",
    description:
      "A vehicle failure may affect several connected operations while some supporting information is outdated.",
    context: "Multiple risks + outdated information",
  },
  "F4-E": {
    title: "Multiple Risks with Missing Information",
    description:
      "A vehicle failure may affect several connected operations while some supporting information is missing.",
    context: "Multiple risks + missing information",
  },
  "F4-F": {
    title: "Multiple Risks with Conflicting Information",
    description:
      "A vehicle failure may affect several connected operations while available information conflicts.",
    context: "Multiple risks + conflicting information",
  },
};


function getFamilyId(scenarioId: string): string {
  return scenarioId.split("-")[0] ?? "";
}


function ScenarioControl({
  scenarios,
  selectedScenario,
  runningScenario,
  error,
  onScenarioChange,
  onRunScenario,
}: ScenarioControlProps) {
  const selectedFamilyId = getFamilyId(selectedScenario);

  const selectedFamily =
    situationFamilies.find(
      (family) => family.id === selectedFamilyId,
    ) ?? situationFamilies[0];

  const selectedSituation =
    situations[selectedScenario];

  const familyScenarios = scenarios.filter(
    (scenarioId) =>
      getFamilyId(scenarioId) === selectedFamily.id,
  );


  function handleFamilyChange(familyId: string) {
    const firstScenario = scenarios.find(
      (scenarioId) =>
        getFamilyId(scenarioId) === familyId,
    );

    if (firstScenario) {
      onScenarioChange(firstScenario);
    }
  }


  const SelectedFamilyIcon = selectedFamily.icon;


  return (
    <section
      aria-labelledby="operational-situation-title"
      className="overflow-hidden rounded-2xl border border-white/[0.055] bg-[#0c0f14]"
    >
      {/* =====================================================
          TOP STRIP
          ===================================================== */}
      <div className="flex flex-col gap-4 border-b border-white/[0.05] px-4 py-4 sm:px-5 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex min-w-0 items-center gap-3">
          <div className="grid size-9 shrink-0 place-items-center rounded-xl border border-violet-400/10 bg-violet-400/[0.055]">
            <Radio
              size={17}
              strokeWidth={1.8}
              className="text-violet-400"
            />
          </div>

          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
              <h2
                id="operational-situation-title"
                className="text-[13px] font-semibold text-zinc-200"
              >
                Operational Situation
              </h2>

              <span className="hidden text-zinc-800 sm:inline">
                /
              </span>

              <span className="text-[10px] text-zinc-600">
                Choose what happens in the logistics system
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 text-[10px] text-zinc-600">
          <Sparkles
            size={12}
            strokeWidth={1.8}
            className="text-violet-500"
          />
          <span>
            {scenarios.length} research-backed situations
          </span>
        </div>
      </div>


      {scenarios.length === 0 ? (
        <div className="px-5 py-6 text-sm text-zinc-500">
          No operational situations are currently available.
        </div>
      ) : (
        <>
          {/* =================================================
              FIVE VISUAL STORY FAMILIES
              ================================================= */}
          <div className="grid grid-cols-2 gap-px bg-white/[0.04] sm:grid-cols-3 xl:grid-cols-5">
            {situationFamilies.map((family) => {
              const active =
                family.id === selectedFamily.id;

              const Icon = family.icon;

              return (
                <button
                  key={family.id}
                  type="button"
                  disabled={runningScenario}
                  onClick={() => {
                    handleFamilyChange(family.id);
                  }}
                  className={[
                    "group relative min-h-[94px] bg-[#0c0f14] px-4 py-4 text-left",
                    "transition-all duration-200",
                    "hover:bg-white/[0.025]",
                    "disabled:cursor-not-allowed disabled:opacity-50",
                    active
                      ? family.activeAccent
                      : "border-transparent",
                  ].join(" ")}
                >
                  {active ? (
                    <span
                      className={[
                        "absolute inset-x-0 bottom-0 h-[2px]",
                        family.dot,
                      ].join(" ")}
                    />
                  ) : null}

                  <div className="flex items-start justify-between gap-3">
                    <div
                      className={[
                        "grid size-8 shrink-0 place-items-center rounded-lg",
                        "border border-white/[0.055] bg-white/[0.025]",
                        active
                          ? family.accent
                          : "text-zinc-600 group-hover:text-zinc-400",
                      ].join(" ")}
                    >
                      <Icon
                        size={16}
                        strokeWidth={1.8}
                      />
                    </div>

                    <span
                      className={[
                        "size-1.5 rounded-full",
                        active
                          ? family.dot
                          : "bg-zinc-800",
                      ].join(" ")}
                    />
                  </div>

                  <div className="mt-3">
                    <span
                      className={[
                        "block text-[9px] font-semibold uppercase tracking-[0.12em]",
                        active
                          ? family.accent
                          : "text-zinc-700",
                      ].join(" ")}
                    >
                      {family.shortLabel}
                    </span>

                    <strong
                      className={[
                        "mt-1 block truncate text-[12px] font-medium",
                        active
                          ? "text-zinc-200"
                          : "text-zinc-500 group-hover:text-zinc-300",
                      ].join(" ")}
                    >
                      {family.title}
                    </strong>
                  </div>
                </button>
              );
            })}
          </div>


          {/* =================================================
              SELECTED STORY
              ================================================= */}
          <div className="grid gap-4 p-4 sm:p-5 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center">
            <div className="flex min-w-0 items-start gap-3">
              <div
                className={[
                  "mt-0.5 grid size-10 shrink-0 place-items-center rounded-xl",
                  "border border-white/[0.055] bg-white/[0.025]",
                  selectedFamily.accent,
                ].join(" ")}
              >
                <SelectedFamilyIcon
                  size={19}
                  strokeWidth={1.8}
                />
              </div>

              <div className="min-w-0">
                <div className="mb-1.5 flex flex-wrap items-center gap-2">
                  <span
                    className={[
                      "text-[9px] font-semibold uppercase tracking-[0.14em]",
                      selectedFamily.accent,
                    ].join(" ")}
                  >
                    {selectedFamily.title}
                  </span>

                  <span className="text-zinc-800">
                    •
                  </span>

                  <span className="text-[9px] font-medium text-zinc-700">
                    EXP-010 / {selectedScenario}
                  </span>
                </div>

                <h3 className="truncate text-[15px] font-semibold tracking-[-0.01em] text-zinc-100">
                  {selectedSituation?.title ??
                    selectedScenario}
                </h3>

                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <span
                    className={[
                      "inline-flex items-center gap-1.5 rounded-full border border-white/[0.055]",
                      "bg-white/[0.025] px-2.5 py-1 text-[10px] text-zinc-500",
                    ].join(" ")}
                  >
                    <span
                      className={[
                        "size-1.5 rounded-full",
                        selectedFamily.dot,
                      ].join(" ")}
                    />

                    {selectedSituation?.context ??
                      "Operational situation"}
                  </span>

                  <span className="hidden text-[10px] text-zinc-700 xl:inline">
                    {selectedFamily.description}
                  </span>
                </div>
              </div>
            </div>


            {/* ===============================================
                ACTION AREA
                =============================================== */}
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
              <div className="relative min-w-[240px]">
                <select
                  id="scenario-select"
                  aria-label="Choose operational situation"
                  value={selectedScenario}
                  disabled={runningScenario}
                  onChange={(event) => {
                    onScenarioChange(
                      event.target.value,
                    );
                  }}
                  className={[
                    "h-10 w-full appearance-none rounded-xl",
                    "border border-white/[0.07] bg-[#101319]",
                    "pl-3 pr-9 text-[11px] font-medium text-zinc-300",
                    "transition-colors",
                    "hover:border-white/[0.12]",
                    "focus:border-violet-400/30 focus:ring-2 focus:ring-violet-400/10",
                    "disabled:cursor-not-allowed disabled:opacity-50",
                  ].join(" ")}
                >
                  {familyScenarios.map(
                    (scenarioId) => (
                      <option
                        key={scenarioId}
                        value={scenarioId}
                      >
                        {scenarioId} —{" "}
                        {situations[scenarioId]
                          ?.title ?? scenarioId}
                      </option>
                    ),
                  )}
                </select>

                <ChevronDown
                  size={14}
                  strokeWidth={1.8}
                  aria-hidden="true"
                  className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-zinc-600"
                />
              </div>

              <button
                type="button"
                disabled={
                  !selectedScenario ||
                  runningScenario
                }
                onClick={onRunScenario}
                className={[
                  "group inline-flex h-10 shrink-0 items-center justify-center gap-2 rounded-xl",
                  "bg-violet-500 px-4 text-[11px] font-semibold text-white",
                  "shadow-[0_8px_30px_rgba(124,58,237,0.16)]",
                  "transition-all duration-200",
                  "hover:bg-violet-400 hover:shadow-[0_10px_34px_rgba(124,58,237,0.22)]",
                  "active:scale-[0.985]",
                  "disabled:cursor-not-allowed disabled:bg-violet-500/40 disabled:text-white/50 disabled:shadow-none",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400",
                ].join(" ")}
              >
                {runningScenario ? (
                  <>
                    <LoaderCircle
                      size={14}
                      strokeWidth={2}
                      className="animate-spin"
                    />
                    Checking
                  </>
                ) : (
                  <>
                    Run Situation
                    <ArrowRight
                      size={14}
                      strokeWidth={2}
                      className="transition-transform duration-200 group-hover:translate-x-0.5"
                    />
                  </>
                )}
              </button>
            </div>
          </div>


          {/* =================================================
              ERROR — ONLY WHEN NEEDED
              ================================================= */}
          {error ? (
            <div
              role="alert"
              className="mx-4 mb-4 flex items-start gap-2.5 rounded-xl border border-red-400/10 bg-red-400/[0.04] px-3.5 py-3 sm:mx-5 sm:mb-5"
            >
              <AlertCircle
                size={15}
                strokeWidth={1.8}
                className="mt-0.5 shrink-0 text-red-400"
              />

              <div>
                <span className="block text-[10px] font-semibold text-red-300">
                  Situation could not be checked
                </span>

                <span className="mt-1 block text-[10px] leading-5 text-zinc-500">
                  {error}
                </span>
              </div>
            </div>
          ) : null}
        </>
      )}
    </section>
  );
}


export default ScenarioControl;