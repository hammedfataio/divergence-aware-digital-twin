import AISafetyPanel from "../control/AISafetyPanel";
import { situationLabel } from "../control/OperationsControl";
import type { ScenarioResponse } from "../../types/api";

interface Props {
  scenario: ScenarioResponse | null;
  scenarioId: string;
}

export default function AISafetyView({
  scenario,
  scenarioId,
}: Props) {
  return (
    <section className="space-y-5">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">
          AI Safety & Decision Assurance
        </h2>
        <p className="mt-2 text-sm text-slate-500">
          Review AI recommendations, system differences,
          supporting evidence and safety assessments.
        </p>
        <p className="mt-4 text-sm font-medium text-blue-700">
          {situationLabel(scenarioId)}
        </p>
      </div>

      {scenario ? (
        <AISafetyPanel scenario={scenario} />
      ) : (
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <h3 className="font-semibold text-slate-900">
            No simulation result yet
          </h3>
          <p className="mt-2 text-sm text-slate-500">
            Go to Operations, select a situation and run
            the simulation to review its safety results here.
          </p>
        </div>
      )}
    </section>
  );
}
