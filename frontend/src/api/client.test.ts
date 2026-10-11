
import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, getHealth, getScenarios, runScenario } from "./client";

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
  vi.restoreAllMocks();
});

describe("DARA-DT Research API client", () => {
  it("requests the backend health endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        status: "ok",
        service: "DARA-DT Research API",
        version: "0.1.0",
      }),
    });

    globalThis.fetch = fetchMock;

    const result = await getHealth();

    expect(result.status).toBe("ok");
    expect(fetchMock).toHaveBeenCalledWith(
      "/health",
      expect.objectContaining({
        headers: expect.objectContaining({
          Accept: "application/json",
        }),
      }),
    );
  });

  it("retrieves the available scenarios", async () => {
    const scenarios = ["F0-A", "F1-A", "F2-A", "F3-A", "F4-A"];

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => scenarios,
    });

    await expect(getScenarios()).resolves.toEqual(scenarios);
  });

  it.each(["F0-A", "F1-A", "F2-A", "F3-A", "F4-A"])(
    "sends a POST request for scenario %s",
    async (scenarioId) => {
      const response = {
        scenario_id: scenarioId,
        assurance_results: [],
      };

      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => response,
      });

      globalThis.fetch = fetchMock;

      const result = await runScenario(scenarioId);

      expect(result.scenario_id).toBe(scenarioId);
      expect(fetchMock).toHaveBeenCalledWith(
        `/api/scenarios/${scenarioId}/run`,
        expect.objectContaining({
          method: "POST",
        }),
      );
    },
  );

  it("encodes scenario identifiers safely", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ scenario_id: "F0/A" }),
    });

    globalThis.fetch = fetchMock;

    await runScenario("F0/A");

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/scenarios/F0%2FA/run",
      expect.any(Object),
    );
  });

  it("reports backend errors correctly", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
      json: async () => ({
        detail: "Scenario not found",
      }),
    });

    await expect(runScenario("UNKNOWN")).rejects.toMatchObject({
      name: "ApiError",
      message: "Scenario not found",
      status: 404,
    });
  });

  it("handles non-JSON backend errors", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => {
        throw new SyntaxError("Invalid JSON");
      },
    });

    await expect(getScenarios()).rejects.toBeInstanceOf(ApiError);
  });

  it("propagates network failures", async () => {
    globalThis.fetch = vi.fn().mockRejectedValue(
      new TypeError("Failed to fetch"),
    );

    await expect(getScenarios()).rejects.toThrow("Failed to fetch");
  });
});
