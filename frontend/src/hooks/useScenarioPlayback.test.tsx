import { act, renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useScenarioPlayback } from "./useScenarioPlayback";
import type { ScenarioResponse } from "../types/api";

function createTestScenario(
  scenarioId: string,
  hasDecisionEffect = false,
): ScenarioResponse {
  return {
    scenario_id: scenarioId,
    divergences: hasDecisionEffect
      ? [
          {
            decision_relevant: true,
            decision_impacting: true,
          },
        ]
      : [],
    propagation: [],
  } as unknown as ScenarioResponse;
}

describe("DARA-DT Scenario Playback", () => {
  const scenarios = [
    "F0-A",
    "F1-A",
    "F2-A",
    "F3-A",
    "F4-A",
  ];

  it.each(scenarios)(
    "reveals the Trust Check at the trust stage for %s",
    (scenarioId) => {
      const { result } = renderHook(() =>
        useScenarioPlayback(
          createTestScenario(scenarioId),
        ),
      );

      // Initial stage: Trust Check must be hidden.
      expect(result.current.currentStage.id).toBe("observe");
      expect(result.current.showTrustResult).toBe(false);

      // Trace stage: Trust Check must remain hidden.
      act(() => {
        result.current.goToStage("trace");
      });

      expect(result.current.currentStage.id).toBe("trace");
      expect(result.current.showTrustResult).toBe(false);

      // Trust stage: Trust Check becomes visible.
      act(() => {
        result.current.goToStage("trust");
      });

      expect(result.current.currentStage.id).toBe("trust");
      expect(result.current.showTrustResult).toBe(true);
    },
  );

  it("reveals decision effects at the trace stage", () => {
    const { result } = renderHook(() =>
      useScenarioPlayback(
        createTestScenario("F3-A", true),
      ),
    );

    expect(result.current.hasDecisionEffect).toBe(true);
    expect(result.current.showDecisionTrace).toBe(false);

    act(() => {
      result.current.goToStage("trace");
    });

    expect(result.current.showDecisionTrace).toBe(true);
  });

  it("hides the Trust Check when playback restarts", () => {
    const { result } = renderHook(() =>
      useScenarioPlayback(
        createTestScenario("F0-A"),
      ),
    );

    act(() => {
      result.current.goToStage("trust");
    });

    expect(result.current.showTrustResult).toBe(true);

    act(() => {
      result.current.restart();
    });

    expect(result.current.currentStage.id).toBe("observe");
    expect(result.current.showTrustResult).toBe(false);
  });
});