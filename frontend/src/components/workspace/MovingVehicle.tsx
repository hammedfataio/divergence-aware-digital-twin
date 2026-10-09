
import { useId } from "react";
import { AlertTriangle, Truck } from "lucide-react";

type ScenarioFamily = "F0" | "F1" | "F2" | "F3" | "F4";

interface MovingVehicleProps {
  scenarioId: string;
  progress: number;
  className?: string;
}

function clamp(value: number): number {
  return Math.max(0, Math.min(1, value));
}

function getFamily(scenarioId: string): ScenarioFamily {
  const family = scenarioId.slice(0, 2).toUpperCase();

  if (
    family === "F0" ||
    family === "F1" ||
    family === "F2" ||
    family === "F3" ||
    family === "F4"
  ) {
    return family;
  }

  return "F0";
}

function movementPositions(
  family: ScenarioFamily,
  progress: number,
) {
  const time = clamp(progress);

  // Deterministic illustration, not measured telemetry.
  const normalPosition = clamp(time * 1.15);

  switch (family) {
    case "F1":
      return {
        physical: Math.min(normalPosition, 0.34),
        twin: normalPosition,
        eventActive: time >= 0.3,
      };

    case "F3":
      return {
        physical: Math.min(normalPosition, 0.58),
        twin: normalPosition,
        eventActive: time >= 0.52,
      };

    case "F4":
      return {
        physical: Math.min(normalPosition, 0.45),
        twin: normalPosition,
        eventActive: time >= 0.4,
      };

    case "F2":
      return {
        physical: normalPosition,
        twin: normalPosition,
        eventActive: time >= 0.35,
      };

    default:
      return {
        physical: normalPosition,
        twin: normalPosition,
        eventActive: false,
      };
  }
}

export default function MovingVehicle({
  scenarioId,
  progress,
  className = "",
}: MovingVehicleProps) {
  const family = getFamily(scenarioId);
  const positions = movementPositions(family, progress);

  const physicalX = 55 + positions.physical * 530;
  const twinX = 55 + positions.twin * 530;

  const isSeparated =
    Math.abs(positions.physical - positions.twin) > 0.025;

  const isInterrupted =
    positions.eventActive &&
    (family === "F1" || family === "F3" || family === "F4");

  const routeId = useId().replace(/:/g, "");

  return (
    <section
      className={`overflow-hidden rounded-2xl border border-slate-200 bg-[#F7F8F5] ${className}`}
      aria-label="Schematic vehicle simulation"
    >
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 bg-white px-5 py-4">
        <div>
          <h2 className="text-base font-semibold text-[#172B31]">
            Operational Journey
          </h2>
          <p className="mt-1 text-xs text-slate-500">
            Scenario {scenarioId} · Illustrative route playback
          </p>
        </div>

        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            isInterrupted
              ? "bg-amber-100 text-amber-800"
              : "bg-emerald-100 text-emerald-800"
          }`}
        >
          {isInterrupted
            ? "Movement interrupted"
            : "Journey in progress"}
        </span>
      </header>

      <div className="px-4 py-6">
        <svg
          viewBox="0 0 640 245"
          className="h-auto w-full"
          role="img"
          aria-label={
            `Physical vehicle at ${Math.round(
              positions.physical * 100,
            )}% of illustrative route; Digital Twin at ${Math.round(
              positions.twin * 100,
            )}%`
          }
        >
          <defs>
            <pattern
              id={`${routeId}-grid`}
              width="38"
              height="38"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M38 0H0V38"
                fill="none"
                stroke="#DDE5E1"
                strokeWidth="1"
              />
            </pattern>
          </defs>

          <rect
            width="640"
            height="245"
            rx="16"
            fill={`url(#${routeId}-grid)`}
          />

          {/* Schematic roads */}
          <path
            d="M0 75H640M0 177H640"
            stroke="#FFFFFF"
            strokeWidth="17"
          />
          <path
            d="M155 0V245M440 0V245"
            stroke="#FFFFFF"
            strokeWidth="15"
          />

          {/* Route */}
          <path
            d="M55 130H585"
            stroke="#FFFFFF"
            strokeWidth="20"
            strokeLinecap="round"
          />
          <path
            d="M55 130H585"
            stroke="#CFD9D4"
            strokeWidth="12"
            strokeLinecap="round"
          />
          <path
            d={`M55 130H${physicalX}`}
            stroke="#F6534D"
            strokeWidth="8"
            strokeLinecap="round"
          />

          {/* Origin */}
          <circle
            cx="55"
            cy="130"
            r="15"
            fill="#172B31"
            stroke="white"
            strokeWidth="4"
          />
          <text
            x="55"
            y="166"
            textAnchor="middle"
            fontSize="13"
            fontWeight="600"
            fill="#172B31"
          >
            Origin
          </text>

          {/* Destination */}
          <circle
            cx="585"
            cy="130"
            r="15"
            fill="#F6534D"
            stroke="white"
            strokeWidth="4"
          />
          <text
            x="585"
            y="166"
            textAnchor="middle"
            fontSize="13"
            fontWeight="600"
            fill="#172B31"
          >
            Order
          </text>

          {/* Digital Twin shadow */}
          <g transform={`translate(${twinX}, 87)`}>
            <circle
              r="19"
              fill="#1976B9"
              fillOpacity="0.15"
              stroke="#1976B9"
              strokeWidth="2"
              strokeDasharray="4 4"
            />
            <rect
              x="-12"
              y="-8"
              width="24"
              height="16"
              rx="5"
              fill="#1976B9"
            />
            <text
              y="-27"
              textAnchor="middle"
              fontSize="12"
              fontWeight="600"
              fill="#1976B9"
            >
              Twin
            </text>
          </g>

          {/* Physical vehicle */}
          <g transform={`translate(${physicalX}, 130)`}>
            <circle
              r="27"
              fill="#F6534D"
              fillOpacity="0.17"
            />
            <circle
              r="19"
              fill="#F6534D"
              stroke="#FFFFFF"
              strokeWidth="4"
            />
            <path
              d="M-11 -7H3L10 0V8H-11Z"
              fill="none"
              stroke="white"
              strokeWidth="2"
              strokeLinejoin="round"
            />
            <circle cx="-6" cy="9" r="2.5" fill="white" />
            <circle cx="6" cy="9" r="2.5" fill="white" />
          </g>

          {/* Event marker */}
          {positions.eventActive && family !== "F0" && (
            <g transform="translate(330 205)">
              <rect
                x="-118"
                y="-17"
                width="236"
                height="34"
                rx="12"
                fill="#FFF0D8"
                stroke="#E6B86D"
              />
              <text
                textAnchor="middle"
                y="5"
                fontSize="12"
                fontWeight="600"
                fill="#8C4C08"
              >
                {family === "F2"
                  ? "Issue outside active decision"
                  : family === "F4"
                    ? "Multiple effects under review"
                    : family === "F3"
                      ? "Knock-on risk under review"
                      : "Direct operational issue"}
              </text>
            </g>
          )}

          {isSeparated && (
            <text
              x="320"
              y="31"
              textAnchor="middle"
              fontSize="13"
              fontWeight="600"
              fill="#B76A12"
            >
              Reality and Twin positions differ
            </text>
          )}
        </svg>
      </div>

      <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 bg-white px-5 py-4">
        <div className="flex flex-wrap items-center gap-4 text-xs text-[#172B31]">
          <span className="inline-flex items-center gap-2">
            <Truck size={15} className="text-[#F6534D]" />
            Physical vehicle
          </span>

          <span className="inline-flex items-center gap-2">
            <span className="h-3 w-3 rounded-full bg-[#1976B9]" />
            Digital Twin
          </span>
        </div>

        {isInterrupted && (
          <span className="inline-flex items-center gap-1 text-xs font-medium text-amber-700">
            <AlertTriangle size={14} />
            Review operational event
          </span>
        )}
      </footer>

      <p className="px-5 pb-4 text-xs text-slate-500">
        Demonstration geometry only. Positions and event timing
        illustrate scenario behaviour; they are not measured
        GPS coordinates or experimental telemetry.
      </p>
    </section>
  );
}
