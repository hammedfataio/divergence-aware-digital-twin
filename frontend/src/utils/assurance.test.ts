import { describe, expect, it } from "vitest";

import { selectPrimaryAssurance } from "./assurance";
import type { AssuranceResult } from "../types/api";

function makeResult(
  policy: string,
): AssuranceResult {
  return {
    policy,
  } as AssuranceResult;
}

describe("DARA-DT assurance selection", () => {
  it("selects DARA-DT over a baseline policy", () => {
    const results = [
      makeResult("dara-dt"),
      makeResult("baseline"),
    ];

    expect(selectPrimaryAssurance(results)).toBe(results[0]);
  });

  it("selects DARA-DT regardless of policy order", () => {
    const results = [
      makeResult("baseline"),
      makeResult("DARA-DT"),
      makeResult("alternative"),
    ];

    expect(selectPrimaryAssurance(results)).toBe(results[1]);
  });

  it("falls back to the last result when DARA-DT is absent", () => {
    const results = [
      makeResult("baseline"),
      makeResult("alternative"),
    ];

    expect(selectPrimaryAssurance(results)).toBe(results[1]);
  });

  it("returns null for an empty result list", () => {
    expect(selectPrimaryAssurance([])).toBeNull();
  });
});
