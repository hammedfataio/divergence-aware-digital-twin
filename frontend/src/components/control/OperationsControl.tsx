import { AlertCircle, LoaderCircle, Play } from "lucide-react";

interface OperationsControlProps {
  scenarios: string[];
  selectedScenario: string;
  runningScenario: boolean;
  error: string | null;
  onScenarioChange: (scenarioId: string) => void;
  onRunScenario: () => void;
}

const titles: Record<string, string> = {
  "F0-A": "Normal Vehicle Assignment",
  "F0-B": "Assignment Constraint Detected",
  "F0-C": "Outdated Operational Information",
  "F0-D": "Missing Operational Information",
  "F0-E": "Conflicting Operational Information",
  "F0-F": "Repeated Normal Operation",
  "F1-A": "Vehicle Breakdown",
  "F1-B": "Vehicle Capacity Changed",
  "F1-C": "Vehicle No Longer Available",
  "F1-D": "Vehicle Breakdown with Outdated Information",
  "F1-E": "Vehicle Breakdown with Missing Information",
  "F1-F": "Vehicle Breakdown with Conflicting Information",
  "F2-A": "Location Issue Elsewhere",
  "F2-B": "Capacity Issue Elsewhere",
  "F2-C": "Vehicle Status Issue Elsewhere",
  "F2-D": "Unrelated Issue with Outdated Information",
  "F2-E": "Unrelated Issue with Missing Information",
  "F2-F": "Unrelated Issue with Conflicting Information",
  "F3-A": "Breakdown May Affect Another Assignment",
  "F3-B": "Unavailable Vehicle May Affect Recovery",
  "F3-C": "Vehicle Location May Delay Recovery",
  "F3-D": "Knock-on Risk with Outdated Information",
  "F3-E": "Knock-on Risk with Missing Information",
  "F3-F": "Knock-on Risk with Conflicting Information",
  "F4-A": "Breakdown May Affect Multiple Vehicles",
  "F4-B": "Breakdown May Affect Capacity and Recovery",
  "F4-C": "Location Issue May Affect Timing and Deadline",
  "F4-D": "Multiple Risks with Outdated Information",
  "F4-E": "Multiple Risks with Missing Information",
  "F4-F": "Multiple Risks with Conflicting Information",
};

const families: Record<string, string> = {
  F0: "Normal Operations",
  F1: "Current Decision Issue",
  F2: "Issue Elsewhere",
  F3: "Knock-on Risk",
  F4: "Multiple Risks",
};

export function situationLabel(id: string): string {
  return titles[id] ?? "Operational Situation";
}

export default function OperationsControl({
  scenarios,
  selectedScenario,
  runningScenario,
  error,
  onScenarioChange,
  onRunScenario,
}: OperationsControlProps) {
  const selectedFamily = selectedScenario.split("-")[0];
  const familyOptions = [...new Set(
    scenarios.map((id) => id.split("-")[0])
  )];

  const filtered = scenarios.filter(
    (id) => id.startsWith(selectedFamily + "-")
  );

  return (
    <section
      id="operations"
      aria-label="Operational controls"
      className="border-b border-slate-200 bg-white px-5 py-5"
    >
      <div className="mb-4">
        <h3 className="text-sm font-bold text-slate-900">
          Operational Controls
        </h3>
        <p className="mt-1 text-xs text-slate-500">
          Choose a simulated situation and run its operational assessment.
        </p>
      </div>

      <div className="grid gap-3 md:grid-cols-[1fr_1.5fr_auto]">
        <label className="block">
          <span className="mb-1.5 block text-xs font-medium text-slate-600">
            Situation category
          </span>
          <select
            value={selectedFamily}
            disabled={runningScenario}
            onChange={(event) => {
              const next = scenarios.find(
                (id) => id.startsWith(event.target.value + "-")
              );
              if (next) onScenarioChange(next);
            }}
            className="h-11 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-800"
          >
            {familyOptions.map((family) => (
              <option key={family} value={family}>
                {families[family] ?? "Operations"}
              </option>
            ))}
          </select>
        </label>

        <label className="block">
          <span className="mb-1.5 block text-xs font-medium text-slate-600">
            Situation
          </span>
          <select
            value={selectedScenario}
            disabled={runningScenario}
            onChange={(event) => onScenarioChange(event.target.value)}
            className="h-11 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-800"
          >
            {filtered.map((id) => (
              <option key={id} value={id}>
                {situationLabel(id)}
              </option>
            ))}
          </select>
        </label>

        <button
          type="button"
          disabled={!selectedScenario || runningScenario}
          onClick={onRunScenario}
          className="flex h-11 items-center justify-center gap-2 self-end rounded-lg bg-blue-600 px-5 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {runningScenario ? (
            <LoaderCircle size={16} className="animate-spin" />
          ) : (
            <Play size={16} />
          )}
          {runningScenario ? "Running..." : "Run Situation"}
        </button>
      </div>

      {error && (
        <div
          role="alert"
          className="mt-4 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700"
        >
          <AlertCircle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </section>
  );
}
