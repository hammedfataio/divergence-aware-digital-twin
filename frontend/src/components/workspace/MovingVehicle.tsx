
import { useId } from "react";
import { AlertTriangle, MapPin } from "lucide-react";

type ScenarioFamily = "F0" | "F1" | "F2" | "F3" | "F4";

interface MovingVehicleProps {
  scenarioId: string;
  progress: number;
  className?: string;
}

type Point = {
  x: number;
  y: number;
};

type VehiclePoint = Point & {
  angle: number;
};

const TRUCK_ICON = "/icons/dump-truck.png";

const ORANGE = "#F97316";
const ORANGE_DARK = "#EA580C";
const TWIN_BLUE = "#1976B9";

const clamp = (n: number): number =>
  Number.isFinite(n)
    ? Math.max(0, Math.min(1, n))
    : 0;

const getFamily = (id: string): ScenarioFamily => {
  const family = id.slice(0, 2).toUpperCase();

  return family === "F1" ||
    family === "F2" ||
    family === "F3" ||
    family === "F4"
    ? family
    : "F0";
};

/**
 * DARA-DT M7.12
 *
 * Curved-road logistics simulation.
 *
 * Scientific integrity:
 * - Road geometry is fictional.
 * - Movement is deterministic.
 * - Vehicle positions are illustrative.
 * - Separation is not measured divergence.
 * - Backend scenario results determine assurance decisions.
 */

const ROUTE_PATH =
  "M 82 340 C 117 337, 142 325, 160 295 S 188 237, 224 226 C 264 214, 294 218, 318 182 S 364 126, 401 135 C 438 143, 468 117, 485 93 S 535 70, 572 66";

const ROADS = [
  "M -20 350 C 110 360 155 320 190 267 S 300 205 335 165 S 470 90 665 45",
  "M -20 260 C 115 240 165 265 245 218 S 380 165 650 140",
  "M -10 155 C 110 130 180 155 265 115 S 450 55 650 20",
  "M 30 -20 C 55 110 82 205 45 395",
  "M 130 -20 C 150 80 120 160 175 235 S 190 330 205 410",
  "M 260 -20 C 250 95 300 160 265 230 S 295 330 320 410",
  "M 420 -20 C 395 95 445 165 415 235 S 440 340 455 410",
  "M 550 -20 C 535 90 565 190 530 255 S 550 335 580 410",
  "M -20 75 C 125 90 210 40 315 75 S 490 95 665 105",
  "M -20 390 C 135 390 240 365 365 340 S 515 295 665 310",
];

const BEZIERS: [
  Point,
  Point,
  Point,
  Point
][] = [
  [
    { x: 82, y: 340 },
    { x: 117, y: 337 },
    { x: 142, y: 325 },
    { x: 160, y: 295 },
  ],
  [
    { x: 160, y: 295 },
    { x: 178, y: 265 },
    { x: 188, y: 237 },
    { x: 224, y: 226 },
  ],
  [
    { x: 224, y: 226 },
    { x: 264, y: 214 },
    { x: 294, y: 218 },
    { x: 318, y: 182 },
  ],
  [
    { x: 318, y: 182 },
    { x: 342, y: 146 },
    { x: 364, y: 126 },
    { x: 401, y: 135 },
  ],
  [
    { x: 401, y: 135 },
    { x: 438, y: 143 },
    { x: 468, y: 117 },
    { x: 485, y: 93 },
  ],
  [
    { x: 485, y: 93 },
    { x: 502, y: 69 },
    { x: 535, y: 70 },
    { x: 572, y: 66 },
  ],
];

function bezier(
  [a, b, c, d]: [Point, Point, Point, Point],
  t: number,
): Point {
  const s = 1 - t;

  return {
    x:
      s * s * s * a.x +
      3 * s * s * t * b.x +
      3 * s * t * t * c.x +
      t * t * t * d.x,

    y:
      s * s * s * a.y +
      3 * s * s * t * b.y +
      3 * s * t * t * c.y +
      t * t * t * d.y,
  };
}

/**
 * Sample the fictional route for approximately
 * distance-based vehicle movement.
 */
const samples: Point[] = BEZIERS.flatMap(
  (segment, index) =>
    Array.from(
      { length: 41 },
      (_, i) => bezier(segment, i / 40),
    ).filter((_, i) => index === 0 || i > 0),
);

const distances = samples.map((point, index) =>
  index === 0
    ? 0
    : Math.hypot(
        point.x - samples[index - 1].x,
        point.y - samples[index - 1].y,
      ),
);

const cumulative: number[] = [];

let runningDistance = 0;

for (const distance of distances) {
  runningDistance += distance;
  cumulative.push(runningDistance);
}

const totalLength = cumulative[cumulative.length - 1];

function pointAt(progress: number): VehiclePoint {
  const target = clamp(progress) * totalLength;

  let index = cumulative.findIndex(
    (distance) => distance >= target,
  );

  if (index < 1) {
    index = 1;
  }

  const a = samples[index - 1];
  const b = samples[index];

  const segmentLength =
    cumulative[index] - cumulative[index - 1];

  const ratio =
    segmentLength > 0
      ? (target - cumulative[index - 1]) /
        segmentLength
      : 0;

  return {
    x: a.x + (b.x - a.x) * ratio,
    y: a.y + (b.y - a.y) * ratio,
    angle:
      (Math.atan2(
        b.y - a.y,
        b.x - a.x,
      ) *
        180) /
      Math.PI,
  };
}

/**
 * Scenario-specific visual movement.
 *
 * Thresholds are illustration parameters,
 * not research measurements.
 */
function movementPositions(
  family: ScenarioFamily,
  progress: number,
) {
  const time = clamp(progress);
  const normal = clamp(time * 1.15);

  switch (family) {
    case "F1":
      return {
        physical: Math.min(normal, 0.34),
        twin: normal,
        eventActive: time >= 0.3,
      };

    case "F3":
      return {
        physical: Math.min(normal, 0.58),
        twin: normal,
        eventActive: time >= 0.52,
      };

    case "F4":
      return {
        physical: Math.min(normal, 0.45),
        twin: normal,
        eventActive: time >= 0.4,
      };

    case "F2":
      return {
        physical: normal,
        twin: normal,
        eventActive: time >= 0.35,
      };

    default:
      return {
        physical: normal,
        twin: normal,
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

  const state = movementPositions(
    family,
    progress,
  );

  const physical = pointAt(state.physical);
  const twin = pointAt(state.twin);

  const separated =
    Math.abs(state.physical - state.twin) > 0.025;

  const interrupted =
    state.eventActive &&
    (family === "F1" ||
      family === "F3" ||
      family === "F4");

  const id = useId().replace(/:/g, "");

  return (
    <section
      className={`flex h-full min-h-[600px] min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-200 bg-[#F7F8F5] ${className}`}
      aria-label="Illustrative curved-road vehicle simulation"
    >
      {/* HEADER */}
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 bg-white px-5 py-4">
        <div>
          <h2 className="text-base font-semibold text-[#172B31]">
            Operational Journey
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Scenario {scenarioId} · Curved-road route
            simulation
          </p>
        </div>

        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            interrupted
              ? "bg-amber-100 text-amber-800"
              : "bg-emerald-100 text-emerald-800"
          }`}
        >
          {interrupted
            ? "Movement interrupted"
            : "Journey simulation"}
        </span>
      </header>

      {/* MAP */}
      <div className="flex min-h-0 flex-1 items-center justify-center p-3 sm:p-5">
        <svg
          viewBox="0 0 640 400"
          preserveAspectRatio="xMidYMid meet"
          className="block h-auto max-h-full w-full"
          role="img"
          aria-label={`Illustrative physical vehicle ${Math.round(
            state.physical * 100,
          )} percent along route; Digital Twin ${Math.round(
            state.twin * 100,
          )} percent`}
        >
          <defs>
            <pattern
              id={`${id}-blocks`}
              width="44"
              height="44"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M44 0H0V44"
                fill="none"
                stroke="#D7DFDA"
                strokeWidth="1"
              />
            </pattern>

            <filter
              id={`${id}-truck-shadow`}
              x="-50%"
              y="-50%"
              width="200%"
              height="200%"
            >
              <feDropShadow
                dx="0"
                dy="3"
                stdDeviation="3"
                floodColor="#172B31"
                floodOpacity="0.3"
              />
            </filter>
          </defs>

          {/* BACKGROUND */}
          <rect
            width="640"
            height="400"
            rx="14"
            fill="#E9EEEA"
          />

          <rect
            width="640"
            height="400"
            rx="14"
            fill={`url(#${id}-blocks)`}
            opacity=".55"
          />

          {/* LANDSCAPE */}
          <path
            d="M20 290 Q85 280 115 320 L90 400 H0 V320Z M485 210 Q535 175 620 205 L640 260 L550 285Z"
            fill="#CDE6C4"
          />

          {/* ROADS */}
          {ROADS.map((road, index) => (
            <g key={index}>
              <path
                d={road}
                fill="none"
                stroke="#D1D9D4"
                strokeWidth="24"
                strokeLinecap="round"
              />

              <path
                d={road}
                fill="none"
                stroke="#FFFFFF"
                strokeWidth="19"
                strokeLinecap="round"
              />
            </g>
          ))}

          {/* MAIN ROUTE */}
          <path
            d={ROUTE_PATH}
            fill="none"
            stroke="#B3C1BA"
            strokeWidth="15"
            strokeLinecap="round"
          />

          <path
            d={ROUTE_PATH}
            fill="none"
            stroke="#FFFFFF"
            strokeWidth="11"
            strokeLinecap="round"
          />

          {/* PLANNED ROUTE */}
          <path
            d={ROUTE_PATH}
            fill="none"
            stroke={TWIN_BLUE}
            strokeWidth="4"
            strokeDasharray="1 13"
            strokeLinecap="round"
          />

          {/* PHYSICAL ROUTE PROGRESS — ORANGE */}
          <path
            d={ROUTE_PATH}
            fill="none"
            stroke={ORANGE}
            strokeWidth="5"
            strokeLinecap="round"
            pathLength="100"
            strokeDasharray={`${state.physical * 100} 100`}
            opacity=".9"
          />

          {/* DEPOT */}
          <g transform="translate(82 340)">
            <circle
              r="13"
              fill="#172B31"
              stroke="white"
              strokeWidth="4"
            />

            <text
              x="-4"
              y="-23"
              fontSize="13"
              fontWeight="600"
              fill="#172B31"
            >
              Depot
            </text>
          </g>

          {/* DESTINATION */}
          <g transform="translate(572 66)">
            <MapPin
              x={-17}
              y={-35}
              width={34}
              height={34}
              color={ORANGE_DARK}
              fill={ORANGE}
              stroke="white"
              strokeWidth={1.5}
            />

            <text
              x="-4"
              y="22"
              textAnchor="middle"
              fontSize="12"
              fontWeight="600"
              fill="#172B31"
            >
              Order
            </text>
          </g>

          {/* DIGITAL TWIN */}
          {separated && (
            <g
              transform={`translate(${twin.x} ${twin.y})`}
            >
              <circle
                r="20"
                fill={TWIN_BLUE}
                fillOpacity=".12"
                stroke={TWIN_BLUE}
                strokeWidth="2"
                strokeDasharray="5 4"
              />

              <circle
                r="8"
                fill={TWIN_BLUE}
                stroke="white"
                strokeWidth="2"
              />

              <text
                y="-28"
                textAnchor="middle"
                fontSize="12"
                fontWeight="700"
                fill={TWIN_BLUE}
              >
                Twin
              </text>
            </g>
          )}

          {/* ORANGE PHYSICAL TRUCK */}
          <g
            transform={`translate(${physical.x} ${physical.y})`}
            filter={`url(#${id}-truck-shadow)`}
          >
            {/* Visual highlight */}
            <circle
              r="27"
              fill={ORANGE}
              fillOpacity=".15"
            />

            <circle
              r="22"
              fill="white"
              fillOpacity=".8"
            />

            {/*
              Keep the truck artwork horizontal so that
              its detailed side profile remains readable
              as it travels around the curved route.
            */}
            <image
              href={TRUCK_ICON}
              x="-32"
              y="-19"
              width="64"
              height="38"
              preserveAspectRatio="xMidYMid meet"
            />
          </g>

          {/* POSITION SEPARATION NOTICE */}
          {separated && (
            <g>
              <rect
                x="176"
                y="15"
                width="288"
                height="32"
                rx="16"
                fill="#FFF0D8"
                stroke="#E6B86D"
              />

              <text
                x="320"
                y="35"
                textAnchor="middle"
                fontSize="12"
                fontWeight="600"
                fill="#8C4C08"
              >
                Physical and Twin positions differ
              </text>
            </g>
          )}

          {/* SCENARIO EVENT */}
          {state.eventActive && family !== "F0" && (
            <g>
              <rect
                x="170"
                y="355"
                width="300"
                height="32"
                rx="12"
                fill="#FFF0D8"
                stroke="#E6B86D"
              />

              <text
                x="320"
                y="375"
                textAnchor="middle"
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
        </svg>
      </div>

      {/* LEGEND */}
      <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 bg-white px-5 py-3 text-xs text-[#172B31]">
        <div className="flex flex-wrap items-center gap-4">
          <span className="inline-flex items-center gap-2">
            <img
              src={TRUCK_ICON}
              alt=""
              className="h-5 w-8 object-contain"
            />
            Physical vehicle
          </span>

          <span className="inline-flex items-center gap-2">
            <span className="h-3 w-3 rounded-full bg-[#1976B9]" />
            Digital Twin
          </span>

          <span className="inline-flex items-center gap-2">
            <span className="h-1 w-5 rounded-full border-t-4 border-dotted border-[#1976B9]" />
            Planned route
          </span>
        </div>

        {interrupted && (
          <span className="inline-flex items-center gap-1 font-medium text-amber-700">
            <AlertTriangle size={14} />
            Review operational event
          </span>
        )}
      </footer>

      {/* RESEARCH DISCLAIMER */}
      <p className="bg-white px-5 pb-4 text-xs leading-5 text-slate-500">
        Fictional road geometry and deterministic movement
        only. This is not a real map, GPS track, measured
        experimental telemetry or measured divergence.
        Backend research results determine assurance
        decisions.
      </p>
    </section>
  );
}
