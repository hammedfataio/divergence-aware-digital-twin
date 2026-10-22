import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { useActiveView } from "./useActiveView";

function navigate(hash: string) {
  act(() => {
    window.location.hash = hash;
    window.dispatchEvent(new Event("hashchange"));
  });
}

afterEach(() => {
  window.history.replaceState(null, "", window.location.pathname);
});

describe("DARA-DT navigation", () => {
  it.each([
    ["#dara-view", "dara-view"],
    ["#vehicle-tracking", "vehicle-tracking"],
    ["#operations", "operations"],
    ["#ai-safety", "ai-safety"],
  ])("opens %s", (hash, expected) => {
    window.history.replaceState(null, "", hash);
    const { result } = renderHook(() => useActiveView());
    expect(result.current).toBe(expected);
  });

  it("defaults to DARA View for unknown routes", () => {
    window.history.replaceState(null, "", "#unknown");
    const { result } = renderHook(() => useActiveView());
    expect(result.current).toBe("dara-view");
  });

  it("updates when navigation changes", () => {
    window.history.replaceState(null, "", "#dara-view");
    const { result } = renderHook(() => useActiveView());

    navigate("#operations");
    expect(result.current).toBe("operations");

    navigate("#ai-safety");
    expect(result.current).toBe("ai-safety");

    navigate("#vehicle-tracking");
    expect(result.current).toBe("vehicle-tracking");

    navigate("#dara-view");
    expect(result.current).toBe("dara-view");
  });
});
