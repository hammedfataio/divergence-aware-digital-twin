import LogisticsMap from "../workspace/LogisticsMap";
import { situationLabel } from "../control/OperationsControl";

interface VehicleTrackingViewProps {
  scenarioId: string;
}

export default function VehicleTrackingView({
  scenarioId,
}: VehicleTrackingViewProps) {
  return (
    <section className="space-y-5">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">
          Vehicle Tracking
        </h2>
        <p className="mt-2 text-sm text-slate-500">
          Explore the simulated journey of a physical vehicle
          alongside its digital twin.
        </p>
        <div className="mt-4 rounded-xl bg-blue-50 p-4">
          <p className="text-xs font-medium text-blue-700">
            Current Operation
          </p>
          <p className="mt-1 font-semibold text-blue-900">
            {situationLabel(scenarioId)}
          </p>
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 px-5 py-4">
          <h3 className="font-semibold text-slate-900">
            Vehicle and Digital Twin Map
          </h3>
          <p className="mt-1 text-xs text-slate-500">
            Illustrative locations only. No live GPS telemetry.
          </p>
        </div>
        <LogisticsMap
          scenarioId={scenarioId}
          progress={0}
          className="h-[600px] w-full"
        />
      </div>
    </section>
  );
}
