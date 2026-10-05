import type { ReactNode } from "react";
import {
  Bell,
  BrainCircuit,
  ChevronDown,
  CircleHelp,
  FlaskConical,
  LayoutDashboard,
  Settings,
  ShieldCheck,
  Truck,
  Wifi,
} from "lucide-react";

interface ApplicationShellProps {
  children: ReactNode;
}

interface NavigationItem {
  label: string;
  icon: typeof LayoutDashboard;
  active?: boolean;
}

const primaryNavigation: NavigationItem[] = [
  {
    label: "Control Centre",
    icon: LayoutDashboard,
    active: true,
  },
  {
    label: "Fleet",
    icon: Truck,
  },
  {
    label: "AI Decisions",
    icon: BrainCircuit,
  },
  {
    label: "Research",
    icon: FlaskConical,
  },
];

const secondaryNavigation: NavigationItem[] = [
  {
    label: "Help",
    icon: CircleHelp,
  },
  {
    label: "Settings",
    icon: Settings,
  },
];

function BrandMark() {
  return (
    <div className="relative grid size-10 place-items-center rounded-xl border border-violet-400/15 bg-violet-500/10 shadow-[0_0_30px_rgba(139,92,246,0.08)]">
      <div className="grid grid-cols-3 gap-[3px]">
        <span className="size-[5px] rounded-[2px] bg-violet-300" />
        <span className="size-[5px] rounded-[2px] bg-violet-400" />
        <span className="size-[5px] rounded-[2px] bg-violet-300" />
        <span className="size-[5px] rounded-[2px] bg-violet-500" />
        <span className="size-[5px] rounded-[2px] bg-white" />
        <span className="size-[5px] rounded-[2px] bg-violet-500" />
        <span className="size-[5px] rounded-[2px] bg-violet-300" />
        <span className="size-[5px] rounded-[2px] bg-violet-400" />
        <span className="size-[5px] rounded-[2px] bg-violet-300" />
      </div>

      <div className="absolute inset-0 rounded-xl ring-1 ring-inset ring-white/[0.025]" />
    </div>
  );
}

function NavigationButton({
  item,
}: {
  item: NavigationItem;
}) {
  const Icon = item.icon;

  return (
    <button
      type="button"
      aria-label={item.label}
      title={item.label}
      className={[
        "group relative grid size-10 place-items-center rounded-xl",
        "transition-all duration-200",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400",
        item.active
          ? "bg-violet-500/12 text-violet-300 shadow-[inset_0_0_0_1px_rgba(139,92,246,0.16)]"
          : "text-zinc-500 hover:bg-white/[0.045] hover:text-zinc-200",
      ].join(" ")}
    >
      {item.active ? (
        <span className="absolute -left-[13px] h-5 w-[3px] rounded-r-full bg-violet-400 shadow-[0_0_12px_rgba(167,139,250,0.65)]" />
      ) : null}

      <Icon
        size={19}
        strokeWidth={1.8}
        aria-hidden="true"
      />

      <span className="pointer-events-none absolute left-14 z-50 hidden whitespace-nowrap rounded-md border border-white/10 bg-zinc-900 px-2.5 py-1.5 text-xs font-medium text-zinc-200 shadow-xl group-hover:block">
        {item.label}
      </span>
    </button>
  );
}

function ApplicationShell({
  children,
}: ApplicationShellProps) {
  return (
    <div className="min-h-screen bg-[#090b0f] text-zinc-100">
      {/* =====================================================
          SIDEBAR
          ===================================================== */}
      <aside className="fixed inset-y-0 left-0 z-50 hidden w-[72px] flex-col items-center border-r border-white/[0.055] bg-[#0b0d12] px-3 py-4 md:flex">
        <div
          aria-label="DARA-DT"
          title="DARA-DT"
        >
          <BrandMark />
        </div>

        <div className="my-5 h-px w-8 bg-white/[0.06]" />

        <nav
          className="flex w-full flex-col items-center gap-2"
          aria-label="Primary navigation"
        >
          {primaryNavigation.map((item) => (
            <NavigationButton
              key={item.label}
              item={item}
            />
          ))}
        </nav>

        <div className="mt-auto flex w-full flex-col items-center gap-2">
          {secondaryNavigation.map((item) => (
            <NavigationButton
              key={item.label}
              item={item}
            />
          ))}

          <div className="my-2 h-px w-8 bg-white/[0.06]" />

          <div
            className="grid size-9 place-items-center"
            title="Runtime connected"
            aria-label="Runtime connected"
          >
            <span className="relative flex size-2.5">
              <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-20" />
              <span className="relative inline-flex size-2.5 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.5)]" />
            </span>
          </div>
        </div>
      </aside>

      {/* =====================================================
          APPLICATION
          ===================================================== */}
      <div className="min-h-screen md:pl-[72px]">
        {/* ===================================================
            TOP BAR
            =================================================== */}
        <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b border-white/[0.055] bg-[#090b0f]/90 px-4 backdrop-blur-xl sm:px-6 lg:px-8">
          <div className="flex min-w-0 items-center gap-3">
            <div className="md:hidden">
              <BrandMark />
            </div>

            <div className="flex min-w-0 items-center gap-3">
              <span className="hidden text-[13px] font-semibold tracking-[-0.01em] text-zinc-100 sm:block">
                DARA-DT
              </span>

              <span className="hidden h-4 w-px bg-white/[0.08] sm:block" />

              <button
                type="button"
                className="flex min-w-0 items-center gap-1.5 rounded-lg px-2 py-1.5 text-sm text-zinc-400 transition-colors hover:bg-white/[0.04] hover:text-zinc-200"
              >
                <span className="truncate">
                  Control Centre
                </span>

                <ChevronDown
                  size={13}
                  strokeWidth={1.8}
                  className="shrink-0 text-zinc-600"
                />
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            {/* Runtime status */}
            <div className="hidden items-center gap-2.5 rounded-lg border border-white/[0.06] bg-white/[0.025] px-3 py-2 lg:flex">
              <span className="relative flex size-2">
                <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-20" />
                <span className="relative inline-flex size-2 rounded-full bg-emerald-400" />
              </span>

              <div className="flex flex-col leading-none">
                <span className="text-[11px] font-medium text-zinc-300">
                  System healthy
                </span>

                <span className="mt-1 text-[9px] text-zinc-600">
                  Runtime connected
                </span>
              </div>
            </div>

            {/* Research trace */}
            <div
              className="hidden items-center gap-2 rounded-lg border border-violet-400/10 bg-violet-400/[0.045] px-3 py-2 xl:flex"
              title="Frozen research programme EXP-010"
            >
              <FlaskConical
                size={14}
                strokeWidth={1.8}
                className="text-violet-400"
              />

              <div className="flex flex-col leading-none">
                <span className="text-[9px] uppercase tracking-[0.12em] text-zinc-600">
                  Research
                </span>

                <span className="mt-1 text-[11px] font-medium text-zinc-300">
                  EXP-010
                </span>
              </div>
            </div>

            {/* Notifications */}
            <button
              type="button"
              aria-label="Notifications"
              title="Notifications"
              className="relative grid size-9 place-items-center rounded-lg text-zinc-500 transition-colors hover:bg-white/[0.045] hover:text-zinc-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400"
            >
              <Bell
                size={18}
                strokeWidth={1.8}
              />

              <span className="absolute right-[8px] top-[7px] size-1.5 rounded-full bg-violet-400 ring-2 ring-[#090b0f]" />
            </button>

            <div className="hidden h-6 w-px bg-white/[0.07] sm:block" />

            {/* Operator */}
            <button
              type="button"
              aria-label="Operator menu"
              className="flex items-center gap-2.5 rounded-lg p-1 transition-colors hover:bg-white/[0.035] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400"
            >
              <div className="grid size-8 shrink-0 place-items-center rounded-lg border border-white/[0.08] bg-gradient-to-br from-zinc-700 to-zinc-800 text-[10px] font-semibold text-zinc-200">
                FH
              </div>

              <div className="hidden text-left leading-none sm:block">
                <span className="block text-[11px] font-medium text-zinc-300">
                  Operator
                </span>

                <span className="mt-1 block text-[9px] text-zinc-600">
                  Control Centre
                </span>
              </div>

              <ChevronDown
                size={13}
                strokeWidth={1.8}
                className="hidden text-zinc-600 sm:block"
              />
            </button>
          </div>
        </header>

        {/* ===================================================
            PAGE
            =================================================== */}
        <main>
          {/* Page heading */}
          <section className="border-b border-white/[0.045]">
            <div className="mx-auto flex w-full max-w-[1600px] flex-col gap-5 px-4 py-7 sm:px-6 lg:flex-row lg:items-end lg:justify-between lg:px-8 lg:py-8">
              <div className="min-w-0">
                <div className="mb-2.5 flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-violet-400">
                  <ShieldCheck
                    size={14}
                    strokeWidth={1.9}
                  />
                  AI Supervision
                </div>

                <h1 className="max-w-4xl text-[24px] font-semibold leading-tight tracking-[-0.025em] text-zinc-50 sm:text-[28px]">
                  Autonomous Logistics Control Centre
                </h1>

                <p className="mt-2 max-w-3xl text-[13px] leading-6 text-zinc-500 sm:text-sm">
                  See what the autonomous system wants to do,
                  whether its information can be trusted, and
                  when human attention is required.
                </p>
              </div>

              <div className="flex shrink-0 items-center gap-3">
                <div className="flex items-center gap-2 rounded-lg border border-emerald-400/10 bg-emerald-400/[0.045] px-3 py-2">
                  <Wifi
                    size={14}
                    strokeWidth={1.8}
                    className="text-emerald-400"
                  />

                  <div className="leading-none">
                    <span className="block text-[9px] font-semibold uppercase tracking-[0.12em] text-zinc-600">
                      Operations
                    </span>

                    <span className="mt-1 block text-[11px] font-medium text-emerald-300">
                      Live monitoring
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Workspace */}
          <div className="relative">
            {/* Very subtle ambient background */}
            <div
              aria-hidden="true"
              className="pointer-events-none absolute inset-x-0 top-0 h-[420px] overflow-hidden"
            >
              <div className="absolute left-[20%] top-[-260px] size-[520px] rounded-full bg-violet-500/[0.035] blur-[120px]" />
              <div className="absolute right-[10%] top-[-300px] size-[500px] rounded-full bg-blue-500/[0.025] blur-[120px]" />
            </div>

            <div className="relative mx-auto w-full max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default ApplicationShell;