import { useId } from "react";

type Family = "F0" | "F1" | "F2" | "F3" | "F4";

interface LogisticsMapProps {
  scenarioId: string;
  progress: number;
  className?: string;
}

// Illustration only: these are SVG positions, not real GPS coordinates.
const route: Array<[number, number]> = [
  [65, 330],
  [150, 310],
  [215, 260],
  [290, 270],
  [350, 205],
  [440, 195],
  [520, 130],
  [650, 105],
  [735, 65],
];

function clamp(value: number): number {
  return Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : 0;
}

function familyOf(scenarioId: string): Family {
  const prefix = scenarioId.slice(0, 2).toUpperCase();
  return prefix === "F1" || prefix === "F2" || prefix === "F3" || prefix === "F4"
    ? prefix
    : "F0";
}

function interpolate(progress: number): [number, number] {
  const position = clamp(progress) * (route.length - 1);
  const index = Math.min(route.length - 2, Math.floor(position));
  const fraction = position - index;
  const start = route[index];
  const end = route[index + 1];
  return [
    start[0] + (end[0] - start[0]) * fraction,
    start[1] + (end[1] - start[1]) * fraction,
  ];
}

export default function LogisticsMap({
  scenarioId,
  progress,
  className = "",
}: LogisticsMapProps) {
  const id = useId().replace(/:/g, "");
  const time = clamp(progress);
  const family = familyOf(scenarioId);
  const twinProgress = clamp(time * 1.15);
  const physicalProgress =
    family === "F1"
      ? Math.min(twinProgress, 0.34)
      : family === "F3"
        ? Math.min(twinProgress, 0.58)
        : family === "F4"
          ? Math.min(twinProgress, 0.45)
          : twinProgress;

  const [px, py] = interpolate(physicalProgress);
  const [tx, ty] = interpolate(twinProgress);
  const separated = Math.abs(physicalProgress - twinProgress) > 0.015;
  const routePoints = route.map(([x, y]) => `${x},${y}`).join(" ");

  return (
    <section
      className={`overflow-hidden rounded-2xl border border-slate-700 bg-slate-950 text-white ${className}`}
      aria-label="Illustrative logistics map"
    >
      <header className="flex flex-wrap items-start justify-between gap-3 px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-cyan-300">
            M7 · Logistics map prototype
          </p>
          <h2 className="mt-1 text-xl font-semibold">Vehicle and Digital Twin</h2>
          <p className="mt-1 text-sm text-slate-300">
            Scenario {scenarioId} · Playback {Math.round(time * 100)}%
          </p>
        </div>
        <span className="rounded-full border border-amber-400/40 px-3 py-1 text-xs text-amber-200">
          Illustrative positions
        </span>
      </header>

      <div className="relative bg-[#e7ede8]">
        <svg
          viewBox="0 0 800 400"
          role="img"
          aria-label={`Illustrative street network showing physical vehicle and digital twin for ${scenarioId}. Playback ${Math.round(time * 100)} percent.`}
          className="block h-auto w-full"
        >
          <defs>
            <pattern id={`${id}-grid`} width="44" height="44" patternUnits="userSpaceOnUse">
              <path d="M44 0H0V44" fill="none" stroke="#d2ded6" strokeWidth="1" />
            </pattern>
          </defs>
          <rect width="800" height="400" fill="#e7ede8" />
          <rect width="800" height="400" fill={`url(#${id}-grid)`} opacity="0.6" />
          <path d="M0 105 Q100 80 190 120 T410 110 T800 150" fill="none" stroke="#ffffff" strokeWidth="34" />
          <path d="M0 105 Q100 80 190 120 T410 110 T800 150" fill="none" stroke="#c4d0c7" strokeWidth="1.5" />
          <path d="M100 0 Q125 110 165 180 T200 400" fill="none" stroke="#ffffff" strokeWidth="30" />
          <path d="M360 0 Q320 90 350 190 T425 400" fill="none" stroke="#ffffff" strokeWidth="30" />
          <path d="M600 0 Q565 125 600 225 T660 400" fill="none" stroke="#ffffff" strokeWidth="30" />
          <path d="M0 300 Q150 275 250 310 T500 295 T800 310" fill="none" stroke="#ffffff" strokeWidth="28" />
          <path d="M40 370 Q150 325 215 270 Q245 240 290 270 Q320 285 350 205 Q375 175 440 195 Q480 205 520 130 Q550 100 650 105 Q700 100 760 45" fill="none" stroke="#ffffff" strokeWidth="32" strokeLinecap="round" strokeLinejoin="round" />
          <polyline points={routePoints} fill="none" stroke="#2563eb" strokeWidth="5" strokeDasharray="5 11" strokeLinecap="round" strokeLinejoin="round" />
          <circle cx="65" cy="330" r="11" fill="#0f172a" stroke="white" strokeWidth="3" />
          <text x="82" y="352" fill="#0f172a" fontSize="15" fontWeight="700">Depot</text>
          <circle cx="735" cy="65" r="12" fill="#ef4444" stroke="white" strokeWidth="4" />
          <text x="685" y="42" fill="#7f1d1d" fontSize="15" fontWeight="700">Destination</text>
          {separated && (
            <g transform={`translate(${tx} ${ty})`}>
              <circle r="15" fill="#2563eb" stroke="white" strokeWidth="3" />
              <text y="5" textAnchor="middle" fontSize="11" fill="white" fontWeight="700">DT</text>
            </g>
          )}
          <g transform={`translate(${px} ${py})`}>
            <circle r="19" fill="#ef4444" fillOpacity="0.16" />
            <circle r="12" fill="#dc2626" stroke="white" strokeWidth="3" />
            <path d="M-6 -3H4V4H-6Z M4 -1H8L11 3V4H4Z" fill="white" />
          </g>
        </svg>
      </div>

      <div className="flex flex-wrap gap-x-5 gap-y-2 px-5 py-3 text-xs text-slate-200">
        <span><span aria-hidden="true" className="mr-2 text-red-400">●</span>Physical vehicle</span>
        <span><span aria-hidden="true" className="mr-2 text-blue-400">●</span>Digital Twin</span>
        <span><span aria-hidden="true" className="mr-2 text-blue-400">┄</span>Illustrative route</span>
      </div>
      <p className="border-t border-slate-700 px-5 py-3 text-xs leading-relaxed text-slate-300">
        Fictional road illustration and deterministic playback. Not a geographic map,
        road-verified route, live GPS track, measured telemetry, or experimental evidence.
        The interactive geographic map will be enabled after an authorised tile provider is configured.
      </p>
    </section>
  );
}
