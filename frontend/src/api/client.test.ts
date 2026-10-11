import { afterEach, describe, expect, it, vi } from "vitest";
import { getHealth, getScenarios, runScenario } from "./client";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("DARA-DT API Client", () => {
  it("retrieves backend health information", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "ok" }),
    });

    vi.stubGlobal("fetch", mockFetch);

    const result = await getHealth();

    expect(result.status).toBe("ok");
    expect(mockFetch).toHaveBeenCalledWith(
      "/health",
      expect.any(Object),
    );
  });

  it("retrieves available scenarios", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ["F0-A", "F1-A", "F2-A", "F3-A", "F4-A"],
    });

    vi.stubGlobal("fetch", mockFetch);

    const result = await getScenarios();

    expect(result).toHaveLength(5);
  });

  it.each(["F0-A", "F1-A", "F2-A", "F3-A", "F4-A"])(
    "runs scenario %s through the API",
    async (scenarioId) => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ scenario_id: scenarioId }),
      });

      vi.stubGlobal("fetch", mockFetch);

      const result = await runScenario(scenarioId);

      expect(result.scenario_id).toBe(scenarioId);
      expect(mockFetch).toHaveBeenCalledWith(
        `/api/scenarios/${scenarioId}/run`,
        expect.objectContaining({ method: "POST" }),
      );
    },
  );
});
