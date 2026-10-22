import OperationsControl, {
  situationLabel,
} from "../control/OperationsControl";

type Props = React.ComponentProps<typeof OperationsControl>;

export default function OperationsView(props: Props) {
  return (
    <section className="space-y-5">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">
          Operations Management
        </h2>
        <p className="mt-2 text-sm text-slate-500">
          Select an operational situation and run a simulation
          to evaluate the vehicle's response.
        </p>
      </div>


      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-xs font-medium text-slate-500">
            Available Situations
          </p>
          <p className="mt-3 text-3xl font-bold text-slate-900">
            {props.scenarios.length}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Configured simulation situations
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-xs font-medium text-slate-500">
            Simulation Focus
          </p>
          <p className="mt-3 text-lg font-bold text-slate-900">
            Vehicle and Digital Twin
          </p>
          <p className="mt-1 text-xs text-slate-500">
            One assessed vehicle and its digital counterpart
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-xs font-medium text-slate-500">
            Execution Status
          </p>
          <p className="mt-3 text-lg font-bold text-slate-900">
            {props.runningScenario
              ? "Running"
              : props.error
                ? "Action Required"
                : "Ready"}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {props.runningScenario
              ? "Processing the selected situation"
              : props.error
                ? "Review the execution error below"
                : "Ready to run a simulation"}
          </p>
        </div>
      </div>

      <OperationsControl {...props} />

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <p className="text-xs font-medium text-slate-500">
          Selected Operation
        </p>
        <p className="mt-2 text-lg font-semibold text-slate-900">
          {situationLabel(props.selectedScenario)}
        </p>
        <p className="mt-3 text-sm text-slate-500">
          Run the selected situation above, then review its
          assessment and supporting evidence in AI Safety.
        </p>
        <a
          href="#ai-safety"
          className="mt-4 inline-flex items-center rounded-lg border border-blue-200 bg-blue-50 px-4 py-2.5 text-sm font-semibold text-blue-700 hover:bg-blue-100"
        >
          Open AI Safety →
        </a>
        <p className="mt-3 text-xs text-slate-500">
          Results are available after a successful simulation run.
        </p>
      </div>
    </section>
  );
}
