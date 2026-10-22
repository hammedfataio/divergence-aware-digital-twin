import { useEffect, useState } from "react";

export type ActiveView =
  | "dara-view"
  | "vehicle-tracking"
  | "operations"
  | "ai-safety";

const validViews: ActiveView[] = [
  "dara-view",
  "vehicle-tracking",
  "operations",
  "ai-safety",
];

function readView(): ActiveView {
  const hash = window.location.hash.slice(1);
  return validViews.includes(hash as ActiveView)
    ? (hash as ActiveView)
    : "dara-view";
}

export function useActiveView(): ActiveView {
  const [view, setView] = useState(readView);

  useEffect(() => {
    const update = () => setView(readView());

    window.addEventListener("hashchange", update);
    return () => window.removeEventListener("hashchange", update);
  }, []);

  return view;
}
