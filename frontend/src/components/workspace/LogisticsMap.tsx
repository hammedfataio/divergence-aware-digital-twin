
import { useId } from "react";

type Family = "F0" | "F1" | "F2" | "F3" | "F4";

interface LogisticsMapProps {
  scenarioId: string;
  progress: number;
  className?: string;
}

/**
 * DARA-DT M7.11
 *
 * Illustrative logistics journey visualization.
 *
 * IMPORTANT:
 * - Road geometry is fictional.
 * - Vehicle movement is deterministic.
 * - Positions are not GPS coordinates.
 * - Visual separation is not measured divergence.
 * - Assurance decisions come from backend research results.
 */

const TRUCK_ICON = "/icons/dump-truck.png";

const route: Array<[number, number]> = [
  [70, 265],
  [130, 250],
  [185, 219],
  [245, 224],
  [305, 186],
  [360, 178],
  [421, 149],
  [480, 139],
  [540, 110],
  [606, 100],
  [684, 68],
];

const road =
  "M70 265 Q116 258 185 219 Q220 205 245 224 Q276 242 305 186 Q330 164 360 178 Q387 187 421 149 Q448 128 480 139 Q508 146 540 110 Q562 92 606 100 Q644 104 684 68";

const familyLabels: Record<Family, string> = {
  F0: "Normal operations",
  F1: "Direct operational issue",
  F2: "Issue outside active decision",
  F3: "One knock-on effect",
  F4: "Multiple knock-on effects",
};

function clamp(value: number): number {
  return Number.isFinite(value)
    ? Math.max(0, Math.min(1, value))
    : 0;
}

function familyOf(scenarioId: string): Family {
  const prefix = scenarioId.split("-")[0].toUpperCase();

  if (
    prefix === "F1" ||
    prefix === "F2" ||
    prefix === "F3" ||
    prefix === "F4"
  ) {
    return prefix;
  }

  return "F0";
}

/**
 * Returns an illustrative point along the route.
 *
 * This is visual animation, not geographic routing.
 */
function interpolate(progress: number): [number, number] {
  const position = clamp(progress) * (route.length - 1);

  const index = Math.min(
    route.length - 2,
    Math.floor(position),
  );

  const fraction = position - index;

  const start = route[index];
  const end = route[index + 1];

  return [
    start[0] + (end[0] - start[0]) * fraction,
    start[1] + (end[1] - start[1]) * fraction,
  ];
}

/**
 * Scenario-specific illustrative movement.
 *
 * These thresholds are visual storytelling parameters.
 * They must not be interpreted as empirical measurements.
 */
function getJourneyProgress(
  scenarioId: string,
  progress: number,
) {
  const family = familyOf(scenarioId);

  const time = clamp(progress);
  const twin = clamp(time * 1.15);

  const physical =
    family === "F1"
      ? Math.min(twin, 0.34)
      : family === "F3"
        ? Math.min(twin, 0.58)
        : family === "F4"
          ? Math.min(twin, 0.45)
          : twin;

  return {
    family,
    time,
    physical,
    twin,
    separated: Math.abs(physical - twin) > 0.015,
  };
}

export default function LogisticsMap({
  scenarioId,
  progress,
  className = "",
}: LogisticsMapProps) {
  const id = useId().replace(/:/g, "");

  const journey = getJourneyProgress(
    scenarioId,
    progress,
  );

  const [px, py] = interpolate(journey.physical);
  const [tx, ty] = interpolate(journey.twin);

  const routePoints = route
    .map(([x, y]) => `${x},${y}`)
    .join(" ");

  return (
    <section
      aria-label="DARA-DT illustrated logistics journey"
      className={`flex h-full min-h-[600px] min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-700 bg-slate-950 text-white ${className}`}
    >
      {/* MAP HEADER */}
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 px-5 py-5">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-widest text-cyan-300">
            Journey Map
          </p>

          <h3 className="mt-2 text-2xl font-semibold">
            Vehicle and Digital Twin
          </h3>

          <p className="mt-2 text-sm text-slate-300">
            {scenarioId} ·{" "}
            {familyLabels[journey.family]} ·{" "}
            {Math.round(journey.time * 100)}% played
          </p>
        </div>

        <span className="rounded-full border border-amber-400/40 bg-amber-400/10 px-4 py-2 text-sm font-medium text-amber-200">
          Simulated journey
        </span>
      </header>

      {/* MAP CANVAS */}
      <div className="relative min-h-[380px] flex-1 overflow-hidden bg-[#e7eee9]">
        <svg
          viewBox="0 0 760 315"
          preserveAspectRatio="xMidYMid meet"
          role="img"
          aria-label={`Illustrative journey for ${scenarioId}. Physical vehicle at ${Math.round(journey.physical * 100)} percent and Digital Twin at ${Math.round(journey.twin * 100)} percent of the fictional route. ${journey.separated ? "Illustrated positions differ." : "Illustrated positions aligned."}`}
          className="absolute inset-0 h-full w-full"
        >
          <defs>
            <pattern
              id={`${id}-grid`}
              width="52"
              height="52"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M52 0H0V52"
                fill="none"
                stroke="#d2ddd6"
                strokeWidth="1"
              />
            </pattern>

            <filter
              id={`${id}-shadow`}
              x="-50%"
              y="-50%"
              width="200%"
              height="200%"
            >
              <feDropShadow
                dx="0"
                dy="2"
                stdDeviation="3"
                floodColor="#1f2937"
                floodOpacity="0.22"
              />
            </filter>
          </defs>

          {/* BACKGROUND */}
          <rect
            width="760"
            height="315"
            fill="#e7eee9"
          />

          <rect
            width="760"
            height="315"
            fill={`url(#${id}-grid)`}
            opacity="0.4"
          />

          {/* GREEN AREAS */}
          <path
            d="M15 110 Q85 82 125 123 T220 134 L205 190 Q130 201 60 172Z"
            fill="#d4e8d6"
            opacity="0.8"
          />

          <path
            d="M500 198 Q595 174 742 215 L760 315H475Z"
            fill="#d4e8d6"
            opacity="0.8"
          />

          {/* WATER FEATURE */}
          <path
            d="M675 260 Q725 240 760 259V315H650Z"
            fill="#b5dfe9"
            opacity="0.8"
          />

          {/* STREET NETWORK */}
          <g
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path
              d="M0 70 Q125 28 240 70 T480 58 T760 95"
              stroke="#c4d1c8"
              strokeWidth="33"
            />

            <path
              d="M0 70 Q125 28 240 70 T480 58 T760 95"
              stroke="white"
              strokeWidth="29"
            />

            <path
              d="M135 -20 Q145 85 174 145 T200 335"
              stroke="#c4d1c8"
              strokeWidth="28"
            />

            <path
              d="M135 -20 Q145 85 174 145 T200 335"
              stroke="white"
              strokeWidth="24"
            />

            <path
              d="M390 -20 Q348 70 370 150 T420 335"
              stroke="#c4d1c8"
              strokeWidth="29"
            />

            <path
              d="M390 -20 Q348 70 370 150 T420 335"
              stroke="white"
              strokeWidth="25"
            />

            <path
              d="M620 -20 Q590 95 627 173 T655 335"
              stroke="#c4d1c8"
              strokeWidth="30"
            />

            <path
              d="M620 -20 Q590 95 627 173 T655 335"
              stroke="white"
              strokeWidth="26"
            />

            <path
              d="M-20 248 Q130 211 225 256 T470 249 T780 252"
              stroke="#c4d1c8"
              strokeWidth="28"
            />

            <path
              d="M-20 248 Q130 211 225 256 T470 249 T780 252"
              stroke="white"
              strokeWidth="24"
            />

            {/* MAIN ROUTE ROAD */}
            <path
              d={road}
              stroke="#d0dcd3"
              strokeWidth="35"
            />

            <path
              d={road}
              stroke="white"
              strokeWidth="29"
            />

            {/* PLANNED ROUTE */}
            <polyline
              points={routePoints}
              stroke="#d7e2fb"
              strokeWidth="10"
            />

            <polyline
              points={routePoints}
              stroke="#3257e8"
              strokeWidth="5"
              strokeDasharray="3 11"
            />
          </g>

          {/* DEPOT */}
          <g transform="translate(70 265)">
            <circle
              r="11"
              fill="#1e293b"
              stroke="white"
              strokeWidth="3"
            />

            <rect
              x="-6"
              y="16"
              width="57"
              height="23"
              rx="8"
              fill="white"
            />

            <text
              x="22"
              y="32"
              textAnchor="middle"
              fill="#334155"
              fontSize="13"
              fontWeight="700"
            >
              Depot
            </text>
          </g>

          {/* DESTINATION */}
          <g transform="translate(684 68)">
            <circle
              r="17"
              fill="#ef4444"
              fillOpacity="0.14"
            />

            <circle
              r="10"
              fill="#dc2626"
              stroke="white"
              strokeWidth="3"
            />

            <rect
              x="-50"
              y="-42"
              width="100"
              height="25"
              rx="9"
              fill="white"
            />

            <text
              y="-25"
              textAnchor="middle"
              fill="#7f1d1d"
              fontSize="13"
              fontWeight="700"
            >
              Destination
            </text>
          </g>

          {/* DIGITAL TWIN MARKER */}
          {journey.separated && (
            <g
              transform={`translate(${tx} ${ty})`}
              filter={`url(#${id}-shadow)`}
            >
              <circle
                r="18"
                fill="#2563eb"
                fillOpacity="0.15"
              />

              <circle
                r="14"
                fill="#2563eb"
                stroke="white"
                strokeWidth="3"
              />

              <text
                y="4"
                textAnchor="middle"
                fontSize="11"
                fill="white"
                fontWeight="700"
              >
                DT
              </text>
            </g>
          )}

          {/* PHYSICAL VEHICLE — CUSTOM BLUE DUMP TRUCK */}
          <g
            transform={`translate(${px} ${py})`}
            filter={`url(#${id}-shadow)`}
          >
            {/* Subtle highlight behind vehicle */}
            <circle
              r="29"
              fill="#3b82f6"
              fillOpacity="0.12"
            />

            <circle
              r="23"
              fill="white"
              fillOpacity="0.75"
            />

            {/* User-provided truck image */}
            <image
              href={TRUCK_ICON}
              x="-27"
              y="-27"
              width="54"
              height="54"
              preserveAspectRatio="xMidYMid meet"
            />
          </g>
        </svg>
      </div>

      {/* MAP LEGEND */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-t border-white/10 px-5 py-4">
        <div className="flex flex-wrap gap-x-6 gap-y-3 text-sm text-slate-200">
          <span className="inline-flex items-center gap-2">
            <img
              src={TRUCK_ICON}
              alt=""
              className="h-6 w-6 object-contain"
            />
            Physical vehicle
          </span>

          <span className="inline-flex items-center gap-2">
            <span
              aria-hidden="true"
              className="text-lg text-blue-400"
            >
              ●
            </span>
            Digital Twin
          </span>

          <span className="inline-flex items-center gap-2">
            <span
              aria-hidden="true"
              className="text-lg text-blue-400"
            >
              ┄
            </span>
            Planned route
          </span>
        </div>

        <span
          role="status"
          className={`text-sm font-medium ${
            journey.separated
              ? "text-amber-200"
              : "text-emerald-300"
          }`}
        >
          {journey.separated
            ? "Illustrated positions differ"
            : "Illustrated positions aligned"}
        </span>
      </div>

      {/* RESEARCH INTEGRITY DISCLAIMER */}
      <p className="border-t border-white/10 px-5 py-4 text-sm leading-6 text-slate-300">
        Fictional road geometry and deterministic playback.
        This visualization does not represent a real geographic
        map, verified route, live GPS, measured telemetry or
        experimental results. DARA-DT research decisions are
        determined by the scenario response, not by the
        illustrated vehicle positions.
      </p>
    </section>
  );
}
