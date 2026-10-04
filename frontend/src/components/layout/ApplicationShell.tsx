import type { ReactNode } from "react";

interface ApplicationShellProps {
  children: ReactNode;
}

const navigationItems = [
  {
    label: "Control Centre",
    shortLabel: "C",
    active: true,
  },
  {
    label: "AI Decisions",
    shortLabel: "AI",
    active: false,
  },
  {
    label: "Research",
    shortLabel: "R",
    active: false,
  },
];

function ApplicationShell({
  children,
}: ApplicationShellProps) {
  return (
    <div className="dara-app">
      <aside className="dara-sidebar">
        <div className="dara-sidebar-brand">
          <div
            className="dara-brand-mark"
            aria-hidden="true"
          >
            DT
          </div>

          <span className="dara-brand-tooltip">
            DARA-DT
          </span>
        </div>

        <nav
          className="dara-sidebar-navigation"
          aria-label="Primary navigation"
        >
          {navigationItems.map((item) => (
            <button
              key={item.label}
              className={
                item.active
                  ? "dara-nav-button dara-nav-button-active"
                  : "dara-nav-button"
              }
              type="button"
              aria-label={item.label}
              title={item.label}
            >
              <span aria-hidden="true">
                {item.shortLabel}
              </span>
            </button>
          ))}
        </nav>

        <div className="dara-sidebar-footer">
          <button
            className="dara-nav-button"
            type="button"
            aria-label="Settings"
            title="Settings"
          >
            <span aria-hidden="true">⚙</span>
          </button>
        </div>
      </aside>

      <div className="dara-main">
        <header className="dara-topbar">
          <div className="dara-product-identity">
            <div className="dara-product-title-row">
              <span className="dara-product-name">
                DARA-DT
              </span>

              <span className="dara-product-separator">
                /
              </span>

              <span className="dara-product-area">
                Autonomous Logistics Trust Centre
              </span>
            </div>

            <p className="dara-product-subtitle">
              Real-time supervision of AI decisions
              and digital-twin reliability
            </p>
          </div>

          <div className="dara-topbar-actions">
            <div
              className="dara-system-health"
              title="DARA-DT research service connected"
            >
              <span
                className="dara-system-health-dot"
                aria-hidden="true"
              />

              <span>System healthy</span>
            </div>

            <div className="dara-research-reference">
              <span>Research</span>
              <strong>EXP-010</strong>
            </div>

            <button
              className="dara-icon-action"
              type="button"
              aria-label="Notifications"
              title="Notifications"
            >
              <span aria-hidden="true">●</span>
            </button>

            <div className="dara-user">
              <div
                className="dara-user-avatar"
                aria-hidden="true"
              >
                FH
              </div>

              <div className="dara-user-copy">
                <strong>Operator</strong>
                <span>Control Centre</span>
              </div>
            </div>
          </div>
        </header>

        <main className="dara-workspace">
          {children}
        </main>
      </div>
    </div>
  );
}

export default ApplicationShell;
