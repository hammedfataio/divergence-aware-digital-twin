
import {
  createContext,
  useContext,
  type ReactNode,
} from "react";

import {
  useScenarioPlayback,
  type ScenarioPlaybackState,
} from "./useScenarioPlayback";

import type { ScenarioResponse } from "../types/api";

interface SharedScenarioPlaybackProviderProps {
  scenario: ScenarioResponse;
  children: ReactNode;
}

const SharedScenarioPlaybackContext =
  createContext<ScenarioPlaybackState | null>(null);

/**
 * Owns exactly one playback clock for the current scenario.
 *
 * Both the vehicle journey and the research workspace
 * consume this same state through useSharedScenarioPlayback.
 */
export function SharedScenarioPlaybackProvider({
  scenario,
  children,
}: SharedScenarioPlaybackProviderProps) {
  const playback = useScenarioPlayback(scenario);

  return (
    <SharedScenarioPlaybackContext.Provider value={playback}>
      {children}
    </SharedScenarioPlaybackContext.Provider>
  );
}

/**
 * Returns the shared playback state.
 *
 * A missing provider is a programming error. We fail
 * explicitly instead of silently creating a second clock.
 */
export function useSharedScenarioPlayback():
  ScenarioPlaybackState {
  const playback = useContext(
    SharedScenarioPlaybackContext,
  );

  if (playback === null) {
    throw new Error(
      "useSharedScenarioPlayback must be used inside " +
        "SharedScenarioPlaybackProvider.",
    );
  }

  return playback;
}
