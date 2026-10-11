import { describe, expect, it } from "vitest";
import { authorityPresentation } from "./authorityPresentation";
import type { Authority } from "../types/api";

describe("DARA-DT authority presentation", () => {
  it.each([
    ["allow", "APPROVED", "AI can proceed"],
    ["restrict", "LIMITED", "Proceed within restrictions"],
    ["defer", "WAITING", "More reliable information is needed"],
    ["fallback", "SAFE MODE", "Use backup behaviour"],
  ] as const)(
    "maps %s to %s",
    (authority, expectedLabel, expectedDescription) => {
      const result = authorityPresentation(authority as Authority);

      expect(result.label).toBe(expectedLabel);
      expect(result.description).toBe(expectedDescription);
      expect(result.action).toBeTruthy();
      expect(result.textClass).toBeTruthy();
      expect(result.borderClass).toBeTruthy();
      expect(result.backgroundClass).toBeTruthy();
      expect(result.glowClass).toBeTruthy();
    },
  );
});
