import { act, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";

const api = vi.hoisted(() => ({
  getHealth: vi.fn(),
  getProjectStatus: vi.fn(),
  getScenarios: vi.fn(),
  runScenario: vi.fn(),
}));

vi.mock("./api/client", () => ({
  ApiError: class ApiError extends Error {},
  ...api,
}));

vi.mock("./components/control/DaraView", () => ({
  default: () => <div data-testid="dara-screen">DARA dashboard content</div>,
}));

vi.mock("./components/tracking/VehicleTrackingView", () => ({
  default: () => <div data-testid="tracking-screen">Vehicle tracking content</div>,
}));

vi.mock("./components/operations/OperationsView", () => ({
  default: ({ onRunScenario }: { onRunScenario: () => void }) => (
    <div data-testid="operations-screen">
      <button onClick={onRunScenario}>Run test simulation</button>
    </div>
  ),
}));

vi.mock("./components/safety/AISafetyView", () => ({
  default: ({ scenario }: { scenario: { scenario_id: string } | null }) => (
    <div data-testid="safety-screen">
      {scenario ? `Assessment: ${scenario.scenario_id}` : "No assessment"}
    </div>
  ),
}));

const routes = [
  ["#dara-view", "dara-screen", "DARA View"],
  ["#vehicle-tracking", "tracking-screen", "Vehicle Tracking"],
  ["#operations", "operations-screen", "Operations"],
  ["#ai-safety", "safety-screen", "AI Safety"],
] as const;

function navigate(hash: string) {
  act(() => {
    window.history.pushState(null, "", hash);
    window.dispatchEvent(new Event("hashchange"));
  });
}

beforeEach(() => {
  window.history.replaceState(null, "", "#dara-view");

  api.getHealth.mockResolvedValue({
    status: "ok",
    service: "DARA-DT",
    version: "0.1.0",
  });

  api.getProjectStatus.mockResolvedValue({
    project: "DARA-DT",
    full_name: "Divergence-Aware Runtime Assurance Digital Twin",
    research_domain: "Trustworthy AI",
    experimental_domain: "Dynamic Logistics",
    experiments_completed: 0,
    experiments_total: 0,
    experimental_programme_complete: false,
    contribution_status: "in progress",
    current_stage: "simulation",
  });

  api.getScenarios.mockResolvedValue(["F0-A", "F1-A"]);

  api.runScenario.mockResolvedValue({
    scenario_id: "F0-A",
    description: "Normal Vehicle Assignment",
    physical_state: { timestamp: 0, entities: [] },
    twin_state: { timestamp: 0, entities: [] },
    divergences: [],
    ai_decision: {
      decision_id: "decision_001",
      action: "continue_route",
      vehicle_id: "vehicle_07",
      order_id: "order_01",
      dependencies: [],
    },
    runtime_evidence: [],
    propagation: [],
    assurance_results: [
      {
        policy: "DARA-DT",
        authority: "allow",
        intervene: false,
        reason: "No intervention required",
        relevant_divergence_count: 0,
      },
    ],
    ground_truth: {
      intervention_required: false,
      reason: "Normal operation",
    },
    evaluations: {},
  });
});

afterEach(() => {
  window.history.replaceState(null, "", window.location.pathname);
  vi.clearAllMocks();
});

describe("DARA-DT application integration", () => {
  it.each(routes)(
    "renders the correct screen for %s",
    async (hash, testId, label) => {
      window.history.replaceState(null, "", hash);

      render(<App />);

      await waitFor(() => {
        expect(screen.getByTestId(testId)).toBeInTheDocument();
      });

      const navigation = screen.getByRole("navigation", {
        name: "Main navigation",
      });

      const activeLink = Array.from(
        navigation.querySelectorAll("a"),
      ).find((link) => link.textContent?.includes(label));

      expect(activeLink).toHaveAttribute("aria-current", "page");
    },
  );

  it("switches between the four screens", async () => {
    render(<App />);

    await screen.findByTestId("dara-screen");

    for (const [hash, testId] of routes.slice(1)) {
      navigate(hash);
      expect(screen.getByTestId(testId)).toBeInTheDocument();
    }
  });

  it("preserves the simulation result across navigation", async () => {
    navigate("#operations");

    render(<App />);

    await screen.findByTestId("operations-screen");

    act(() => {
      screen.getByRole("button", {
        name: "Run test simulation",
      }).click();
    });

    await waitFor(() => {
      expect(api.runScenario).toHaveBeenCalledWith("F0-A");
    });

    navigate("#ai-safety");

    await waitFor(() => {
      expect(screen.getByText("Assessment: F0-A")).toBeInTheDocument();
    });
  });
});
