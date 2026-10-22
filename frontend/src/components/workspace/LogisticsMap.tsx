import { useEffect, useMemo, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

type Point = [number, number];

interface LogisticsMapProps {
  scenarioId: string;
  progress: number;
  className?: string;
}

// Illustrative coordinates only. Not live GPS or measured telemetry.
// Coordinates are stored as [longitude, latitude].
const ROUTE: Point[] = [
  [-0.1538, 51.5155],
  [-0.1473, 51.5170],
  [-0.1414, 51.5162],
  [-0.1352, 51.5142],
  [-0.1281, 51.5131],
  [-0.1211, 51.5117],
  [-0.1148, 51.5089],
  [-0.1076, 51.5074],
  [-0.1001, 51.5062],
];

// Decorative simulated fleet positions, independent of scenario playback.
const STATIC_FLEET: { id: string; area: string; point: Point }[] = [
  { id: "Fleet 02", area: "Paddington", point: [-0.1750, 51.5154] },
  { id: "Fleet 03", area: "Camden", point: [-0.1426, 51.5392] },
  { id: "Fleet 04", area: "King's Cross", point: [-0.1234, 51.5308] },
  { id: "Fleet 05", area: "Shoreditch", point: [-0.0755, 51.5246] },
  { id: "Fleet 06", area: "Waterloo", point: [-0.1130, 51.5031] },
  { id: "Fleet 07", area: "Victoria", point: [-0.1445, 51.4952] },
];

const clamp = (value: number): number =>
  Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : 0;

function journeyPosition(scenarioId: string, progress: number) {
  const family = scenarioId.split("-")[0].toUpperCase();
  const twin = clamp(progress * 1.15);

  const physical =
    family === "F1"
      ? Math.min(twin, 0.34)
      : family === "F3"
        ? Math.min(twin, 0.58)
        : family === "F4"
          ? Math.min(twin, 0.45)
          : twin;

  return {
    physical,
    twin,
    separated: Math.abs(physical - twin) > 0.015,
  };
}

function interpolate(progress: number): Point {
  const position = clamp(progress) * (ROUTE.length - 1);
  const index = Math.min(ROUTE.length - 2, Math.floor(position));
  const fraction = position - index;

  return [
    ROUTE[index][0] +
      (ROUTE[index + 1][0] - ROUTE[index][0]) * fraction,
    ROUTE[index][1] +
      (ROUTE[index + 1][1] - ROUTE[index][1]) * fraction,
  ];
}

function truckAngle(progress: number): number {
  const index = Math.min(
    ROUTE.length - 2,
    Math.floor(clamp(progress) * (ROUTE.length - 1))
  );
  const a = ROUTE[index];
  const b = ROUTE[index + 1];
  const dx = (b[0] - a[0]) * Math.cos(((a[1] + b[1]) / 2) * Math.PI / 180);
  const dy = b[1] - a[1];

  return Math.atan2(dy, dx) * 180 / Math.PI;
}

function orientTruck(marker: L.Marker, progress: number): void {
  const symbol = marker.getElement()?.querySelector<HTMLElement>(
    ".dara-truck-symbol"
  );
  if (!symbol) return;

  // The truck emoji artwork normally points left.
  symbol.style.display = "inline-block";
  symbol.style.transform = "none";
  symbol.title = `Route heading: ${Math.round(truckAngle(progress))}°`;
}

function latLng(point: Point): L.LatLngTuple {
  return [point[1], point[0]];
}

function vehicleIcon(
  label: string,
  color: string,
  symbol: string
): L.DivIcon {
  return L.divIcon({
    className: "dara-vehicle-marker",
    html: `
      <div
        title="${label}"
        style="
          display:flex;
          align-items:center;
          justify-content:center;
          width:40px;
          height:40px;
          border:3px solid #ffffff;
          border-radius:13px;
          background:${color};
          color:white;
          font-size:19px;
          font-weight:700;
          box-shadow:0 4px 16px rgba(15,23,42,.28);
        "
      ><span class="dara-truck-symbol">${
        symbol === "🚚"
          ? '<svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h11v11H3z"/><path d="M14 10h4l3 4v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>'
          : symbol
      }</span></div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 20],
  });
}

export default function LogisticsMap({
  scenarioId,
  progress,
  className = "",
}: LogisticsMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<L.Map | null>(null);
  const physicalRef = useRef<L.Marker | null>(null);
  const twinRef = useRef<L.Marker | null>(null);
  const journeyRef = useRef(journeyPosition(scenarioId, progress));

  const [selected, setSelected] = useState<"physical" | "twin">(
    "physical"
  );
  const [mapError, setMapError] = useState(false);

  const journey = useMemo(
    () => journeyPosition(scenarioId, progress),
    [scenarioId, progress]
  );

  journeyRef.current = journey;

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let map: L.Map | null = null;

    try {
      map = L.map(container, {
        center: [51.512, -0.128],
        zoom: 12,
        zoomControl: false,
        scrollWheelZoom: true,
      });

      mapRef.current = map;

      L.control.zoom({ position: "topright" }).addTo(map);

      const tiles = L.tileLayer(
        "https://a.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png",
        {
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a> | <a href="https://www.openstreetmap.fr/">OpenStreetMap France</a>',
          maxZoom: 19,
        }
      );

      tiles.addTo(map);

      const routeCoordinates = ROUTE.map(latLng);

      L.polyline(routeCoordinates, {
        color: "#ffffff",
        weight: 10,
        opacity: 0.95,
        lineCap: "round",
        lineJoin: "round",
      }).addTo(map);

      L.polyline(routeCoordinates, {
        color: "#2563eb",
        weight: 5,
        opacity: 0.9,
        lineCap: "round",
        lineJoin: "round",
        dashArray: "1 0",
      }).addTo(map);

      L.circleMarker(latLng(ROUTE[0]), {
        radius: 9,
        color: "#ffffff",
        weight: 3,
        fillColor: "#16a34a",
        fillOpacity: 1,
      })
        .addTo(map)
        .bindPopup("Illustrative dispatch depot");

      L.circleMarker(latLng(ROUTE[ROUTE.length - 1]), {
        radius: 9,
        color: "#ffffff",
        weight: 3,
        fillColor: "#7c3aed",
        fillOpacity: 1,
      })
        .addTo(map)
        .bindPopup("Illustrative delivery destination");

      // Stationary fleet markers are visual context only.
      // They do not participate in simulation or assurance calculations.
      STATIC_FLEET.forEach(({ id, area, point }) => {
        L.marker(latLng(point), {
          icon: vehicleIcon(id, "#64748b", "🚚"),
          zIndexOffset: 100,
        })
          .addTo(map!)
          .bindPopup(
            `<strong>${id}</strong><br/>${area}<br/>Simulated stationary vehicle`
          );
      });

      const physical = L.marker(
        latLng(interpolate(journeyRef.current.physical)),
        {
          icon: vehicleIcon("Physical vehicle", "#ef4444", "🚚"),
          zIndexOffset: 1000,
        }
      )
        .addTo(map)
        .bindPopup("Physical vehicle — simulated position");

      const twin = L.marker(
        latLng(interpolate(journeyRef.current.twin)),
        {
          icon: L.divIcon({
            ...vehicleIcon("Digital twin", "#2563eb", "◆").options,
            iconAnchor: [52, 20],
          }),
          zIndexOffset: 900,
        }
      )
        .addTo(map)
        .bindPopup("Digital twin — illustrative estimated position");

      physicalRef.current = physical;
      twinRef.current = twin;

      // Display the twin marker only when positions diverge.
      if (!journeyRef.current.separated) {
        twin.setOpacity(0);
      }

      map.fitBounds(L.latLngBounds([...routeCoordinates, ...STATIC_FLEET.map(({ point }) => latLng(point))]), {
        padding: [55, 55],
        maxZoom: 14,
        animate: false,
      });

      // Helps Leaflet calculate dimensions inside responsive panels.
      requestAnimationFrame(() => {
        const activeMap = mapRef.current;
        if (activeMap && activeMap === map) {
          activeMap.invalidateSize();
        }
      });
    } catch (error) {
      console.error("DARA-DT Leaflet map initialization failed:", error);
      setMapError(true);

      if (map) {
        map.remove();
      }
      mapRef.current = null;
    }

    return () => {
      physicalRef.current = null;
      twinRef.current = null;

      if (map) {
        map.remove();
      }

      mapRef.current = null;
    };
  }, []);

  useEffect(() => {
    physicalRef.current?.setLatLng(
      latLng(interpolate(journey.physical))
    );

    twinRef.current?.setLatLng(
      latLng(interpolate(journey.twin))
    );

    // Visibility is a presentation choice, not a simulation change.
    twinRef.current?.setOpacity(journey.separated ? 1 : 0);

    if (physicalRef.current) {
      orientTruck(physicalRef.current, journey.physical);
    }
  }, [journey.physical, journey.twin]);

  function focusVehicle(which: "physical" | "twin") {
    setSelected(which);

    const position =
      which === "physical" ? journey.physical : journey.twin;

    mapRef.current?.flyTo(latLng(interpolate(position)), 14, {
      duration: 0.6,
    });
  }

  function resetView() {
    if (!mapRef.current) return;

    mapRef.current.fitBounds(
      L.latLngBounds([...ROUTE.map(latLng), ...STATIC_FLEET.map(({ point }) => latLng(point))]),
      {
        padding: [55, 55],
        maxZoom: 14,
        animate: true,
      }
    );
  }

  return (
    <section
      aria-label="DARA-DT interactive logistics map"
      className={`flex h-full min-h-[520px] min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white text-slate-900 ${className}`}
    >
      <header className="flex items-center justify-end border-b border-slate-200 bg-white px-4 py-2">
        <span className="rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-800">
          Simulated locations · Not GPS
        </span>
      </header>

      <div className="relative min-h-[430px] flex-1 bg-slate-100">
        <div
          ref={containerRef}
          className="absolute inset-0 z-0"
          aria-label="Interactive illustrative London logistics route"
        />

        {mapError && (
          <div className="absolute inset-0 z-[600] flex items-center justify-center bg-slate-100 p-6">
            <div className="max-w-sm rounded-xl border border-red-200 bg-white p-5 text-center shadow-sm">
              <p className="font-semibold text-slate-900">
                Map could not be initialized
              </p>
              <p className="mt-2 text-sm text-slate-600">
                Refresh the page. If this persists, check the
                browser console for the map initialization error.
              </p>
            </div>
          </div>
        )}

        <div className="pointer-events-none absolute left-4 top-4 z-[500] max-w-[260px]">
          <div className="pointer-events-auto rounded-xl border border-slate-200 bg-white/95 p-3 shadow-lg backdrop-blur-sm">
            <p className="mb-3 text-xs font-bold uppercase tracking-wider text-slate-500">
              Vehicle tracking
            </p>

            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => focusVehicle("physical")}
                aria-pressed={selected === "physical"}
                className={`rounded-lg px-3 py-2 text-xs font-semibold transition ${
                  selected === "physical"
                    ? "bg-red-500 text-white"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                🚚 Physical
              </button>

              <button
                type="button"
                onClick={() => focusVehicle("twin")}
                aria-pressed={selected === "twin"}
                className={`rounded-lg px-3 py-2 text-xs font-semibold transition ${
                  selected === "twin"
                    ? "bg-blue-600 text-white"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                ◆ Twin
              </button>
            </div>

            <div className="mt-3 space-y-1.5 text-xs text-slate-600">
              <p>
                Physical:{" "}
                <strong className="text-slate-900">
                  {Math.round(journey.physical * 100)}%
                </strong>
              </p>
              <p>
                Digital twin:{" "}
                <strong className="text-slate-900">
                  {Math.round(journey.twin * 100)}%
                </strong>
              </p>
              <p
                className={
                  journey.separated
                    ? "font-semibold text-amber-700"
                    : "text-emerald-700"
                }
              >
                {journey.separated
                  ? "Illustrative position divergence"
                  : "Illustrative positions aligned"}
              </p>
            </div>

            <button
              type="button"
              onClick={resetView}
              className="mt-3 w-full rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
            >
              Show full route
            </button>
          </div>
        </div>

        <div className="pointer-events-none absolute bottom-6 left-4 z-[500]">
          <div className="rounded-lg border border-slate-200 bg-white/95 px-3 py-2 text-[11px] text-slate-600 shadow-sm">
            Simulated journey · London
          </div>
        </div>
      </div>

      <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 bg-white px-5 py-3">
        <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600">
          <span>
            <span className="mr-1.5 text-red-500">●</span>
            Physical vehicle
          </span>
          <span>
            <span className="mr-1.5 text-blue-600">◆</span>
            Digital twin
          </span>
          <span>
            <span className="mr-1.5 text-slate-500">●</span>
            Static fleet · simulated
          </span>
          <span>
            <span className="mr-1.5 text-green-600">●</span>
            Depot
          </span>
          <span>
            <span className="mr-1.5 text-purple-600">●</span>
            Destination
          </span>
        </div>
        <span className="text-[11px] text-slate-400">
          Not operational telemetry
        </span>
      </footer>
    </section>
  );
}
