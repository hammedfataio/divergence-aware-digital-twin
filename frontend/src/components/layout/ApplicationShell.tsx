import { useActiveView } from "../../hooks/useActiveView";
import type { ReactNode } from "react";
import {
  Activity,
  Bell,
  ChevronDown,
  CircleHelp,
  LayoutDashboard,
  MapPinned,
  Route,
  Settings2,
  ShieldCheck,
  Truck,
} from "lucide-react";

interface ApplicationShellProps {
  children: ReactNode;
}

const navigation = [
  {
    label: "DARA View",
    icon: LayoutDashboard,
    href: "#dara-view",
  },
  {
    label: "Vehicle Tracking",
    icon: Truck,
    href: "#vehicle-tracking",
  },
  {
    label: "Operations",
    icon: Route,
    href: "#operations",
  },
  {
    label: "AI Safety",
    icon: ShieldCheck,
    href: "#ai-safety",
  },
];

export default function ApplicationShell({
  children,
}: ApplicationShellProps) {
  const currentActiveView = useActiveView();
  const activeView = "#" + currentActiveView;

  const currentView =
    navigation.find((item) => item.href === activeView) ??
    navigation[0];

  return (
    <div className="min-h-screen bg-[#f5f7fa] text-slate-900">
      <header className="sticky top-0 z-50 border-b border-slate-200 bg-white">
        <div className="flex min-h-[68px] items-center justify-between gap-4 px-4 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="grid size-10 place-items-center rounded-xl bg-blue-600 text-white">
              <Truck size={21} strokeWidth={2} />
            </div>

            <div>
              <div className="text-lg font-extrabold tracking-tight">
                DARA-DT
              </div>
              <div className="text-[11px] text-slate-500">
                AI Logistics Intelligence
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="hidden items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-800 sm:inline-flex">
              <Activity size={13} />
              Simulation Mode
            </span>

            <span className="hidden text-slate-400 sm:inline">
              <CircleHelp size={18} />
            </span>

            <span className="hidden text-slate-400 sm:inline">
              <Bell size={18} />
            </span>

            <div className="flex items-center gap-2 border-l border-slate-200 pl-3">
              <div className="grid size-9 place-items-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">
                DT
              </div>
              <ChevronDown size={14} className="text-slate-400" />
            </div>
          </div>
        </div>
      </header>

      <div className="flex min-h-[calc(100vh-68px)]">
        <aside className="hidden w-[220px] shrink-0 border-r border-slate-200 bg-white lg:block">
          <div className="sticky top-[68px] flex min-h-[calc(100vh-68px)] flex-col p-4">
            <div className="px-3 pb-3 pt-5 text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
              Workspace
            </div>

            <nav className="space-y-1" aria-label="Main navigation">
              {navigation.map((item) => {
                const Icon = item.icon;

                return (
                  <a
                    key={item.label}
                    href={item.href}
                    
                    aria-current={activeView === item.href ? "page" : undefined}
                    className={[
                      "flex items-center gap-3 rounded-xl px-3 py-3 text-[13px] font-medium transition-colors",
                      activeView === item.href
                        ? "bg-blue-50 font-semibold text-blue-700"
                        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900",
                    ].join(" ")}
                  >
                    <Icon size={18} strokeWidth={1.9} />
                    {item.label}
                  </a>
                );
              })}
            </nav>

            <div className="mt-auto space-y-3 border-t border-slate-100 pt-5">
              <div className="flex items-center gap-3 px-3 text-sm text-slate-500">
                <Settings2 size={17} />
                <span>Dashboard Settings</span>
              </div>

              <div className="rounded-xl border border-blue-100 bg-blue-50 p-3">
                <div className="flex items-center gap-2 text-xs font-semibold text-blue-800">
                  <MapPinned size={15} />
                  Demo Environment
                </div>
                <p className="mt-2 text-[11px] leading-5 text-blue-700">
                  Vehicle journeys are simulated. Map markers do not
                  represent live GPS tracking.
                </p>
              </div>
            </div>
          </div>
        </aside>

        <main id="dara-view" className="min-w-0 flex-1">
          <div className="border-b border-slate-200 bg-white px-5 py-6 sm:px-8">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="mb-2 text-xs font-medium text-slate-500">
                  Dashboard / {currentView.label}
                </div>

                <h1 className="text-2xl font-bold tracking-tight text-slate-950">
                  {currentView.label}
                </h1>

                <p className="mt-2 text-sm text-slate-500">
                  Monitor simulated fleet journeys, vehicle status and
                  AI-assisted operational decisions.
                </p>
              </div>

              <span className="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-medium text-slate-600">
                <Activity size={14} className="text-emerald-600" />
                DARA Dashboard
              </span>
            </div>
          </div>

          <div className="min-w-0 px-4 py-5 sm:px-6 lg:px-8">
            {children}
          </div>

          <footer className="border-t border-slate-200 px-5 py-5 text-xs text-slate-500 sm:px-8">
            DARA-DT Fleet Intelligence · Simulation environment · No live vehicle telemetry
          </footer>
        </main>
      </div>
    </div>
  );
}
