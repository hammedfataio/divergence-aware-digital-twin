import type { ReactNode } from "react";

interface ApplicationShellProps {
  children: ReactNode;
}

function ApplicationShell({
  children,
}: ApplicationShellProps) {
  return (
    <div className="application-shell">
      <header className="application-header">
        <div>
          <p>DARA-DT</p>

          <h1>
            Divergence-Aware Runtime Assurance
            for AI-Driven Digital Twins
          </h1>

          <p>Research Control Centre</p>
        </div>
      </header>

      <main className="application-content">
        {children}
      </main>
    </div>
  );
}

export default ApplicationShell;
