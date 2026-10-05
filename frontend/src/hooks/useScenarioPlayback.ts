import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import type { ScenarioResponse } from "../types/api";


/* -------------------------------------------------------------------------- */
/* Types                                                                      */
/* -------------------------------------------------------------------------- */

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

  stages: PlaybackStage[];
  currentStage: PlaybackStage;
  currentStageIndex: number;

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

  hasDivergence: boolean;
  hasDecisionEffect: boolean;
  hasPropagation: boolean;

  play: () => void;
  pause: () => void;
  restart: () => void;
  togglePlayback: () => void;

  setSpeed: (speed: PlaybackSpeed) => void;

  goToStage: (
    stageId: PlaybackStageId,
  ) => void;
}


/* -------------------------------------------------------------------------- */
/* Playback configuration                                                     */
/* -------------------------------------------------------------------------- */

const PLAYBACK_STAGES: PlaybackStage[] = [
  {
    id: "observe",
    label: "Observe Operation",
    shortLabel: "Observe",
    description:
      "Observe the real-world logistics operation and its Digital Twin representation.",
    durationMs: 1800,
  },

  {
    id: "event",
    label: "Operational Event",
    shortLabel: "Event",
    description:
      "Reveal the operational condition represented by the selected research scenario.",
    durationMs: 1800,
  },

  {
    id: "compare",
    label: "Compare States",
    shortLabel: "Compare",
    description:
      "Compare the real-world system state with the Digital Twin state.",
    durationMs: 2000,
  },

  {
    id: "trace",
    label: "Trace Decision Effect",
    shortLabel: "Trace",
    description:
      "Trace whether the observed condition affects the AI recommendation or propagates through connected decisions.",
    durationMs: 2400,
  },

  {
    id: "trust",
    label: "DARA-DT Trust Check",
    shortLabel: "Trust",
    description:
      "Reveal the runtime-assurance authority returned for the AI recommendation.",
    durationMs: 2200,
  },
];


const TICK_INTERVAL_MS = 40;


/* -------------------------------------------------------------------------- */
/* Utility functions                                                          */
/* -------------------------------------------------------------------------- */

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
  const startTimes: number[] = [];

  let elapsed = 0;

  for (const stage of stages) {
    startTimes.push(elapsed);

    elapsed += stage.durationMs;
  }

  return startTimes;
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
  stageStartTimes: number[],
): number {
  for (
    let index = stages.length - 1;
    index >= 0;
    index -= 1
  ) {
    if (
      elapsedMs >= stageStartTimes[index]
    ) {
      return index;
    }
  }

  return 0;
}


/* -------------------------------------------------------------------------- */
/* Hook                                                                       */
/* -------------------------------------------------------------------------- */

export function useScenarioPlayback(
  scenario: ScenarioResponse,
): ScenarioPlaybackState {
  const [status, setStatus] =
    useState<PlaybackStatus>("idle");

  const [elapsedMs, setElapsedMs] =
    useState(0);

  const [speed, setPlaybackSpeed] =
    useState<PlaybackSpeed>(1);


  const animationFrameRef =
    useRef<number | null>(null);

  const previousTimestampRef =
    useRef<number | null>(null);

  const accumulatedSinceCommitRef =
    useRef(0);


  /* ------------------------------------------------------------------------ */
  /* Static playback calculations                                             */
  /* ------------------------------------------------------------------------ */

  const stages = PLAYBACK_STAGES;


  const stageStartTimes = useMemo(
    () => getStageStartTimes(stages),
    [stages],
  );


  const totalDurationMs = useMemo(
    () => getTotalDuration(stages),
    [stages],
  );


  /* ------------------------------------------------------------------------ */
  /* Scenario-derived research facts                                          */
  /* ------------------------------------------------------------------------ */

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


  /* ------------------------------------------------------------------------ */
  /* Current playback position                                                */
  /* ------------------------------------------------------------------------ */

  const currentStageIndex =
    getStageIndexForElapsedTime(
      elapsedMs,
      stages,
      stageStartTimes,
    );


  const currentStage =
    stages[currentStageIndex];


  const currentStageStartMs =
    stageStartTimes[currentStageIndex];


  const currentStageElapsedMs =
    elapsedMs - currentStageStartMs;


  const stageProgress = clamp(
    currentStageElapsedMs /
      currentStage.durationMs,
    0,
    1,
  );


  const progress = clamp(
    elapsedMs / totalDurationMs,
    0,
    1,
  );


  /* ------------------------------------------------------------------------ */
  /* Status helpers                                                           */
  /* ------------------------------------------------------------------------ */

  const isIdle =
    status === "idle";

  const isPlaying =
    status === "playing";

  const isPaused =
    status === "paused";

  const isComplete =
    status === "complete";


  /* ------------------------------------------------------------------------ */
  /* Stage visibility                                                         */
  /* ------------------------------------------------------------------------ */

  const stageReached = useCallback(
    (
      stageId: PlaybackStageId,
    ): boolean => {
      const targetIndex =
        stages.findIndex(
          (stage) =>
            stage.id === stageId,
        );

      if (targetIndex < 0) {
        return false;
      }

      return (
        currentStageIndex >= targetIndex
      );
    },
    [
      currentStageIndex,
      stages,
    ],
  );


  /*
   * These values control WHAT the visualisation
   * is allowed to reveal at each playback stage.
   *
   * Scientific outcomes are always derived from
   * ScenarioResponse.
   *
   * The playback layer only controls WHEN those
   * already-computed outcomes become visible.
   */

  const showOperationalWorld =
    stageReached("observe");


  const showScenarioEvent =
    stageReached("event");


  const showComparison =
    stageReached("compare");


  const showMismatch =
    showComparison &&
    hasDivergence;


  const showDecisionTrace =
    stageReached("trace") &&
    hasDecisionEffect;


  const showPropagation =
    stageReached("trace") &&
    hasPropagation;


  const showTrustResult =
    stageReached("trust");


  /* ------------------------------------------------------------------------ */
  /* Playback actions                                                         */
  /* ------------------------------------------------------------------------ */

  const play = useCallback(() => {
    setStatus(
      (currentStatus) => {
        if (
          currentStatus === "complete"
        ) {
          setElapsedMs(0);
        }

        return "playing";
      },
    );
  }, []);


  const pause = useCallback(() => {
    setStatus(
      (currentStatus) => {
        if (
          currentStatus !== "playing"
        ) {
          return currentStatus;
        }

        return "paused";
      },
    );
  }, []);


  const restart = useCallback(() => {
    previousTimestampRef.current =
      null;

    accumulatedSinceCommitRef.current =
      0;

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
    }, [
      pause,
      play,
      status,
    ]);


  const setSpeed = useCallback(
    (
      nextSpeed: PlaybackSpeed,
    ) => {
      setPlaybackSpeed(nextSpeed);
    },
    [],
  );


  const goToStage = useCallback(
    (
      stageId: PlaybackStageId,
    ) => {
      const stageIndex =
        stages.findIndex(
          (stage) =>
            stage.id === stageId,
        );

      if (stageIndex < 0) {
        return;
      }

      previousTimestampRef.current =
        null;

      accumulatedSinceCommitRef.current =
        0;

      setElapsedMs(
        stageStartTimes[stageIndex],
      );

      setStatus("paused");
    },
    [
      stageStartTimes,
      stages,
    ],
  );


  /* ------------------------------------------------------------------------ */
  /* Reset when scenario changes                                              */
  /* ------------------------------------------------------------------------ */

  useEffect(() => {
    previousTimestampRef.current =
      null;

    accumulatedSinceCommitRef.current =
      0;

    setElapsedMs(0);
    setStatus("idle");
    setPlaybackSpeed(1);
  }, [scenario.scenario_id]);


  /* ------------------------------------------------------------------------ */
  /* Playback clock                                                           */
  /* ------------------------------------------------------------------------ */

  useEffect(() => {
    if (status !== "playing") {
      previousTimestampRef.current =
        null;

      accumulatedSinceCommitRef.current =
        0;

      if (
        animationFrameRef.current !==
        null
      ) {
        window.cancelAnimationFrame(
          animationFrameRef.current,
        );

        animationFrameRef.current =
          null;
      }

      return;
    }


    function tick(timestamp: number) {
      if (
        previousTimestampRef.current ===
        null
      ) {
        previousTimestampRef.current =
          timestamp;
      }


      const rawDelta =
        timestamp -
        previousTimestampRef.current;


      previousTimestampRef.current =
        timestamp;


      const scaledDelta =
        rawDelta * speed;


      accumulatedSinceCommitRef.current +=
        scaledDelta;


      if (
        accumulatedSinceCommitRef.current >=
        TICK_INTERVAL_MS
      ) {
        const committedDelta =
          accumulatedSinceCommitRef.current;


        accumulatedSinceCommitRef.current =
          0;


        setElapsedMs(
          (currentElapsed) => {
            const nextElapsed =
              currentElapsed +
              committedDelta;


            if (
              nextElapsed >=
              totalDurationMs
            ) {
              previousTimestampRef.current =
                null;

              setStatus("complete");

              return totalDurationMs;
            }


            return nextElapsed;
          },
        );
      }


      animationFrameRef.current =
        window.requestAnimationFrame(
          tick,
        );
    }


    animationFrameRef.current =
      window.requestAnimationFrame(
        tick,
      );


    return () => {
      if (
        animationFrameRef.current !==
        null
      ) {
        window.cancelAnimationFrame(
          animationFrameRef.current,
        );

        animationFrameRef.current =
          null;
      }


      previousTimestampRef.current =
        null;

      accumulatedSinceCommitRef.current =
        0;
    };
  }, [
    speed,
    status,
    totalDurationMs,
  ]);


  /* ------------------------------------------------------------------------ */
  /* Public API                                                               */
  /* ------------------------------------------------------------------------ */

  return {
    status,

    stages,
    currentStage,
    currentStageIndex,

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

    hasDivergence,
    hasDecisionEffect,
    hasPropagation,

    play,
    pause,
    restart,
    togglePlayback,

    setSpeed,

    goToStage,
  };
}