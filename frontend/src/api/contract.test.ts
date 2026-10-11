import { afterEach, describe, expect, it, vi } from "vitest";

import { runScenario } from "./client";
import { selectPrimaryAssurance } from "../utils/assurance";
import { authorityPresentation } from "../utils/authorityPresentation";

import fixtures from "../test/fixtures/exp010_api_responses.json";
import type { ScenarioResponse } from "../types/api";

const responses = fixtures as Record<string, ScenarioResponse>;

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("DARA-DT EXP-010 API contract", () => {
  it.each([
    ["F0-A", "allow", "APPROVED", false],
    ["F1-A", "restrict", "LIMITED", true],
    ["F2-A", "allow", "APPROVED", false],
    ["F3-A", "restrict", "LIMITED", true],
    ["F4-A", "restrict", "LIMITED", true],
  ] as const)(
    "%s maps real API response to %s",
    async (
      scenarioId,
      expectedAuthority,
      expectedLabel,
      expectedIntervention,
    ) => {
      const fixture = responses[scenarioId];

      expect(fixture).toBeDefined();

      const fetchMock = vi.fn().mockResolvedValue(
        new Response(JSON.stringify(fixture), {
          status: 200,
          headers: {
            "Content-Type": "application/json",
          },
        }),
      );

      vi.stubGlobal("fetch", fetchMock);

      const scenario = await runScenario(scenarioId);

      expect(fetchMock).toHaveBeenCalledWith(
        `/api/scenarios/${scenarioId}/run`,
        expect.objectContaining({
          method: "POST",
        }),
      );

      expect(scenario.scenario_id).toBe(scenarioId);

      const assurance = selectPrimaryAssurance(
        scenario.assurance_results,
      );

      expect(assurance).not.toBeNull();
      expect(assurance?.authority).toBe(expectedAuthority);
      expect(assurance?.intervene).toBe(expectedIntervention);

      if (!assurance) {
        throw new Error("Missing primary assurance result");
      }

      const presentation = authorityPresentation(
        assurance.authority,
      );

      expect(presentation.label).toBe(expectedLabel);

      expect(
        scenario.ground_truth?.intervention_required,
      ).toBe(expectedIntervention);
    },
  );
});
