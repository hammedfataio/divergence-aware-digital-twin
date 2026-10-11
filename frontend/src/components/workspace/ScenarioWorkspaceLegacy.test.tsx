import { act, render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import type { ScenarioResponse } from "../../types/api";
import {
  SharedScenarioPlaybackProvider,
  useSharedScenarioPlayback,
} from "../../hooks/SharedScenarioPlayback";

import ScenarioWorkspaceLegacy from "./ScenarioWorkspaceLegacy";

let advanceToTrust: (() => void) | undefined;
let restartPlayback: (() => void) | undefined;

function PlaybackController() {
  const playback = useSharedScenarioPlayback();

  advanceToTrust = () => playback.goToStage("trust");
  restartPlayback = () => playback.restart();

  return null;
}

function createScenario(
  scenarioId: string,
  authority: "allow" | "restrict",
): ScenarioResponse {
  return {
    scenario_id: scenarioId,
    description: `Integration test scenario ${scenarioId}`,
    physical_state: {
      timestamp: 0,
      entities: [],
    },
    twin_state: {
      timestamp: 0,
      entities: [],
    },
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
        authority,
        intervene: authority !== "allow",
        reason: "Integration test assurance decision",
        relevant_divergence_count: 0,
      },
    ],
    ground_truth: {
      intervention_required: authority !== "allow",
      reason: "Integration test ground truth",
    },
    evaluations: {},
  };
}

function renderDashboard(scenario: ScenarioResponse) {
  advanceToTrust = undefined;
  restartPlayback = undefined;

  return render(
    <SharedScenarioPlaybackProvider scenario={scenario}>
      <PlaybackController />
      <ScenarioWorkspaceLegacy scenario={scenario} />
    </SharedScenarioPlaybackProvider>,
  );
}


function getTrustCheckPanel(): HTMLElement {
  const heading = screen.getByText("DARA-DT Trust Check");

  const panel = heading.closest("aside");

  if (!panel) {
    throw new Error("DARA-DT Trust Check panel not found");
  }

  return panel;
}

describe("DARA-DT rendered dashboard assurance", () => {
  it.each([
    ["F0-A", "allow", "APPROVED"],
    ["F1-A", "restrict", "LIMITED"],
    ["F2-A", "allow", "APPROVED"],
    ["F3-A", "restrict", "LIMITED"],
    ["F4-A", "restrict", "LIMITED"],
  ] as const)(
    "%s displays %s at the Trust stage",
    (scenarioId, authority, expectedLabel) => {
      renderDashboard(createScenario(scenarioId, authority));

      expect(within(getTrustCheckPanel()).getByText("Trust result pending")).toBeTruthy();
      expect(within(getTrustCheckPanel()).queryByText(expectedLabel)).toBeNull();

      expect(advanceToTrust).toBeDefined();

      act(() => {
        advanceToTrust?.();
      });

      expect(within(getTrustCheckPanel()).getByText(expectedLabel)).toBeTruthy();
      expect(within(getTrustCheckPanel()).queryByText("Trust result pending")).toBeNull();
    },
  );

  it("hides the assurance decision after playback restarts", () => {
    renderDashboard(createScenario("F0-A", "allow"));

    act(() => {
      advanceToTrust?.();
    });

    expect(within(getTrustCheckPanel()).getByText("APPROVED")).toBeTruthy();

    act(() => {
      restartPlayback?.();
    });

    expect(within(getTrustCheckPanel()).getByText("Trust result pending")).toBeTruthy();
    expect(within(getTrustCheckPanel()).queryByText("APPROVED")).toBeNull();
  });
});
