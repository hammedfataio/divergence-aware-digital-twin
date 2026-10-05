import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import type { ScenarioResponse } from "../types/api";


export type PlaybackStageId =
  | "observe"
  | "event"
  | "compare"
  | "trace"
  | "trust";


export type PlaybackStatus =
  | "idle"
  | "playing"
  | "paused"
  | "complete";


export type PlaybackSpeed = 0.5 | 1 | 2;


export interface PlaybackStage {
  id: PlaybackStageId;
  label: string;
  shortLabel: string;
  description: string;
  durationMs: number;
}


export interface ScenarioPlaybackState {
  status: PlaybackStatus;
  currentStage: PlaybackStage;
  currentStageIndex: number;
  stages: PlaybackStage[];

  progress: number;
  stageProgress: number;

  elapsedMs: number;
  totalDurationMs: number;

  speed: PlaybackSpeed;

  isIdle: boolean;
  isPlaying: boolean;
  isPaused: boolean;
  isComplete: boolean;

  showOperationalWorld: boolean;
  showScenarioEvent: boolean;
  showComparison: boolean;
  showMismatch: boolean;
  showDecisionTrace: boolean;
  showPropagation: boolean;
  showTrustResult: boolean;

  play: () => void;
  pause: () => void;
  restart: () => void;
  togglePlayback: () => void;
  setSpeed: (speed: PlaybackSpeed) => void;
  goToStage: (stageId: PlaybackStageId) => void;
}


const STAGES: PlaybackStage[] = [
  {
    id: "observe",
    label: "Observe",
    shortLabel: "Observe",
    description:
      "Observe the real-world operation and its Digital Twin.",
    durationMs: 1800,
  },
  {
    id: "event",
    label: "Operational Event",
    shortLabel: "Event",
    description:
      "Reveal the operational condition represented by this scenario.",
    durationMs: 1800,
  },
  {
    id: "compare",
    label: "Compare States",
    shortLabel: "Compare",
    description:
      "Compare the real-world state with the Digital Twin.",
    durationMs: 2000,
  },
  {
    id: "trace",
    label: "Trace Decision Effect",
    shortLabel: "Trace",
    description:
      "Trace whether the observed condition affects the AI recommendation.",
    durationMs: 2400,
  },
  {
    id: "trust",
    label: "DARA-DT Trust Check",
    shortLabel: "Trust",
    description:
      "Reveal the runtime-assurance authority for the AI recommendation.",
    durationMs: 2200,
  },
];


const TICK_INTERVAL_MS = 50;


function clamp(
  value: number,
  minimum: number,
  maximum: number,
): number {
  return Math.min(
    Math.max(value, minimum),
    maximum,
  );
}


function getStageStartTimes(
  stages: PlaybackStage[],
): number[] {
  const starts: number[] = [];

  let elapsed = 0;

  for (const stage of stages) {
    starts.push(elapsed);
    elapsed += stage.durationMs;
  }

  return starts;
}


function getTotalDuration(
  stages: PlaybackStage[],
): number {
  return stages.reduce(
    (total, stage) =>
      total + stage.durationMs,
    0,
  );
}


function getStageIndexForElapsedTime(
  elapsedMs: number,
  stages: PlaybackStage[],
  stageStarts: number[],
): number {
  for (
    let index = stages.length - 1;
    index >= 0;
    index -= 1
  ) {
    if (elapsedMs >= stageStarts[index]) {
      return index;
    }
  }

  return 0;
}


export function useScenarioPlayback(
  scenario: ScenarioResponse,
): ScenarioPlaybackState {
  const [status, setStatus] =
    useState<PlaybackStatus>("idle");

  const [elapsedMs, setElapsedMs] =
    useState(0);

  const [speed, setPlaybackSpeed] =
    useState<PlaybackSpeed>(1);


  const previousTimestampRef =
    useRef<number | null>(null);


  const stages = STAGES;


  const stageStarts = useMemo(
    () => getStageStartTimes(stages),
    [stages],
  );


  const totalDurationMs = useMemo(
    () => getTotalDuration(stages),
    [stages],
  );


  const currentStageIndex =
    getStageIndexForElapsedTime(
      elapsedMs,
      stages,
      stageStarts,
    );


  const currentStage =
    stages[currentStageIndex];


  const currentStageStart =
    stageStarts[currentStageIndex];


  const currentStageElapsed =
    elapsedMs - currentStageStart;


  const stageProgress = clamp(
    currentStageElapsed /
      currentStage.durationMs,
    0,
    1,
  );


  const progress = clamp(
    elapsedMs / totalDurationMs,
    0,
    1,
  );


  const isIdle = status === "idle";
  const isPlaying = status === "playing";
  const isPaused = status === "paused";
  const isComplete = status === "complete";


  const stageReached = useCallback(
    (stageId: PlaybackStageId): boolean => {
      const targetIndex = stages.findIndex(
        (stage) => stage.id === stageId,
      );

      return (
        targetIndex >= 0 &&
        currentStageIndex >= targetIndex
      );
    },
    [currentStageIndex, stages],
  );


  const hasDivergence =
    scenario.divergences.length > 0;


  const hasDecisionEffect =
    scenario.divergences.some(
      (divergence) =>
        divergence.decision_relevant ||
        divergence.decision_impacting,
    );


  const hasPropagation =
    scenario.propagation.some(
      (record) => record.propagating,
    );


  /*
   * Playback visibility is intentionally derived from
   * ScenarioResponse.
   *
   * The animation layer does not invent scientific outcomes.
   * It only controls when already-computed research evidence
   * becomes visible to the user.
   */

  const showOperationalWorld =
    stageReached("observe");

  const showScenarioEvent =
    stageReached("event");

  const showComparison =
    stageReached("compare");

  const showMismatch =
    showComparison && hasDivergence;

  const showDecisionTrace =
    stageReached("trace") &&
    hasDecisionEffect;

  const showPropagation =
    stageReached("trace") &&
    hasPropagation;

  const showTrustResult =
    stageReached("trust");


  const play = useCallback(() => {
    setStatus((currentStatus) => {
      if (currentStatus === "complete") {
        setElapsedMs(0);
      }

      return "playing";
    });
  }, []);


  const pause = useCallback(() => {
    setStatus((currentStatus) =>
      currentStatus === "playing"
        ? "paused"
        : currentStatus,
    );
  }, []);


  const restart = useCallback(() => {
    previousTimestampRef.current = null;
    setElapsedMs(0);
    setStatus("playing");
  }, []);


  const togglePlayback =
    useCallback(() => {
      if (status === "playing") {
        pause();
        return;
      }

      play();
    }, [pause, play, status]);


  const setSpeed = useCallback(
    (nextSpeed: PlaybackSpeed) => {
      setPlaybackSpeed(nextSpeed);
    },
    [],
  );


  const goToStage = useCallback(
    (stageId: PlaybackStageId) => {
      const stageIndex = stages.findIndex(
        (stage) => stage.id === stageId,
      );

      if (stageIndex < 0) {
        return;
      }

      previousTimestampRef.current = null;

      setElapsedMs(stageStarts[stageIndex]);

      setStatus(
        stageIndex === stages.length - 1
          ? "paused"
          : "paused",
      );
    },
    [stageStarts, stages],
  );


  /*
   * Reset playback whenever the backend returns a
   * different research scenario.
   */
  useEffect(() => {
    previousTimestampRef.current = null;
    setElapsedMs(0);
    setStatus("idle");
    setPlaybackSpeed(1);
  }, [scenario.scenario_id]);


  /*
   * Playback clock.
   *
   * requestAnimationFrame gives the UI smooth progression,
   * while TICK_INTERVAL_MS prevents unnecessary React state
   * updates on every browser frame.
   */
  useEffect(() => {
    if (status !== "playing") {
      previousTimestampRef.current = null;
      return;
    }

    let animationFrameId = 0;
    let lastCommittedElapsed = elapsedMs;


    function tick(timestamp: number) {
      if (
        previousTimestampRef.current === null
      ) {
        previousTimestampRef.current =
          timestamp;
      }

      const delta =
        timestamp -
        previousTimestampRef.current;

      previousTimestampRef.current =
        timestamp;


      if (
        delta > 0 &&
        timestamp - lastCommittedElapsed >=
          TICK_INTERVAL_MS
      ) {
        setElapsedMs((currentElapsed) => {
          const nextElapsed =
            currentElapsed +
            delta * speed;

          if (
            nextElapsed >= totalDurationMs
          ) {
            previousTimestampRef.current =
              null;

            setStatus("complete");

            return totalDurationMs;
          }

          return nextElapsed;
        });

        lastCommittedElapsed = timestamp;
      }

      animationFrameId =
        window.requestAnimationFrame(tick);
    }


    animationFrameId =
      window.requestAnimationFrame(tick);


    return () => {
      window.cancelAnimationFrame(
        animationFrameId,
      );

      previousTimestampRef.current = null;
    };
  }, [
    elapsedMs,
    speed,
    status,
    totalDurationMs,
  ]);


  return {
    status,
    currentStage,
    currentStageIndex,
    stages,

    progress,
    stageProgress,

    elapsedMs,
    totalDurationMs,

    speed,

    isIdle,
    isPlaying,
    isPaused,
    isComplete,

    showOperationalWorld,
    showScenarioEvent,
    showComparison,
    showMismatch,
    showDecisionTrace,
    showPropagation,
    showTrustResult,

    play,
    pause,
    restart,
    togglePlayback,
    setSpeed,
    goToStage,
  };
}
