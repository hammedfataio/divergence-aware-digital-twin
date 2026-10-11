import type { AssuranceResult } from "../types/api";

export function selectPrimaryAssurance(
  results: AssuranceResult[],
): AssuranceResult | null {
  if (results.length === 0) {
    return null;
  }

  const daraResult = results.find((result) =>
    result.policy.toLowerCase().includes("dara"),
  );

  return daraResult ?? results[results.length - 1];
}
