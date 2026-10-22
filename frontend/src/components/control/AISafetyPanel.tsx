import { ShieldCheck, AlertTriangle } from "lucide-react";
import type { ScenarioResponse } from "../../types/api";

interface Props {
  scenario: ScenarioResponse | null;
}

const label = (value: string) =>
  value.replace(/[_-]/g, " ").trim();

export default function AISafetyPanel({ scenario }: Props) {
  return (
    <section id="ai-safety" className="border-t border-slate-200 bg-white p-5">
      <div className="flex items-center gap-2">
        <ShieldCheck size={19} className="text-blue-600" />
        <h3 className="text-base font-bold text-slate-900">
          AI Safety & Decisions
        </h3>
      </div>

      {!scenario ? (
        <p className="mt-3 text-sm text-slate-500">
          Run an operational situation to view its decision and safety results.
        </p>
      ) : (
        <div className="mt-4 grid gap-4 lg:grid-cols-3">
          <article className="rounded-xl border border-slate-200 p-4">
            <p className="text-xs text-slate-500">Proposed AI Action</p>
            <p className="mt-2 font-semibold capitalize text-slate-900">
              {label(scenario.ai_decision.action)}
            </p>
            <p className="mt-2 text-xs text-slate-600">
              Vehicle: {scenario.ai_decision.vehicle_id ?? "Not specified"}
            </p>
            <p className="text-xs text-slate-600">
              Order: {scenario.ai_decision.order_id ?? "Not specified"}
            </p>
          </article>

          <article className="rounded-xl border border-slate-200 p-4">
            <p className="text-xs text-slate-500">System Comparison</p>
            <p className="mt-2 text-2xl font-bold text-slate-900">
              {scenario.divergences.length}
            </p>
            <p className="text-xs text-slate-600">
              Recorded state differences
            </p>
            <p className="mt-2 text-xs text-slate-600">
              {scenario.divergences.filter(
                (item) => item.decision_relevant === true
              ).length} marked decision-relevant
            </p>
          </article>

          <article className="rounded-xl border border-slate-200 p-4">
            <p className="text-xs text-slate-500">Supporting Evidence</p>
            <p className="mt-2 text-2xl font-bold text-slate-900">
              {scenario.runtime_evidence.length}
            </p>
            <p className="text-xs text-slate-600">
              Evidence records returned
            </p>
          </article>

          <div className="lg:col-span-3">
            <h4 className="mb-3 text-sm font-bold text-slate-900">
              Safety Assessments
            </h4>
            <div className="grid gap-3 md:grid-cols-2">
              {scenario.assurance_results.map((item, index) => (
                <article
                  key={`${item.policy}-${index}`}
                  className="rounded-xl border border-slate-200 p-4"
                >
                  <div className="flex items-center gap-2">
                    {item.intervene && (
                      <AlertTriangle size={16} className="text-amber-600" />
                    )}
                    <p className="text-sm font-semibold capitalize text-slate-900">
                      {item.policy === "No Assurance"
                        ? "Baseline — No Additional Safety Controls"
                        : label(item.policy)}
                    </p>
                  </div>
                  <p className="mt-2 text-sm text-slate-700">
                    {item.intervene
                      ? "Intervention recommended"
                      : "No intervention recommended"}
                  </p>
                  <p className="mt-1 text-xs text-slate-600">
                    Authority: {label(String(item.authority))}
                  </p>
                  <p className="mt-2 text-xs text-slate-600">
                    {item.policy === "No Assurance" &&
                    item.reason === "EXP-010 P0 applies no runtime assurance."
                      ? "This assessment does not apply additional runtime safety checks."
                      : item.reason}
                  </p>
                </article>
              ))}
            </div>
            {scenario.assurance_results.length === 0 && (
              <p className="text-sm text-slate-500">
                No safety assessment results returned.
              </p>
            )}
          </div>
        </div>
      )}

      <p className="mt-4 text-xs text-slate-500">
        Simulation only. Decisions and assessments do not confirm
        real-world execution or live vehicle telemetry.
      </p>
    </section>
  );
}
