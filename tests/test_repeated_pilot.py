"""Repeated controlled evaluation for the DARA-DT pilot."""

from dataclasses import dataclass

from dara_dt.evaluation.metrics import (
    AssuranceMetrics,
    calculate_assurance_metrics,
)
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.bc_pilot import run_bc_pilot


@dataclass(frozen=True)
class RepeatedPilotResult:
    """Aggregated outcomes from repeated B-vs-C pilot runs."""

    repetitions: int
    no_assurance: AssuranceMetrics
    global_divergence: AssuranceMetrics
    dara_dt: AssuranceMetrics


def run_repeated_pilot(
    repetitions: int = 100,
) -> RepeatedPilotResult:
    """Execute the deterministic B-vs-C pilot repeatedly."""

    if repetitions <= 0:
        raise ValueError(
            "repetitions must be greater than zero"
        )

    no_assurance_outcomes: list[AssuranceOutcome] = []
    global_divergence_outcomes: list[AssuranceOutcome] = []
    dara_dt_outcomes: list[AssuranceOutcome] = []

    for _ in range(repetitions):
        pilot = run_bc_pilot()

        for condition in (
            pilot.condition_b,
            pilot.condition_c,
        ):
            no_assurance_outcomes.append(
                condition.policy_results.no_assurance.outcome
            )

            global_divergence_outcomes.append(
                condition.policy_results.global_divergence.outcome
            )

            dara_dt_outcomes.append(
                condition.policy_results.dara_dt.outcome
            )

    return RepeatedPilotResult(
        repetitions=repetitions,
        no_assurance=calculate_assurance_metrics(
            no_assurance_outcomes
        ),
        global_divergence=calculate_assurance_metrics(
            global_divergence_outcomes
        ),
        dara_dt=calculate_assurance_metrics(
            dara_dt_outcomes
        ),
    )
