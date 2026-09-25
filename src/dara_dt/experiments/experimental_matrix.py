"""Controlled experimental matrix for DARA-DT evaluation."""

from dataclasses import dataclass

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.count_policy_experiment import (
    run_count_policy_experiment,
)
from dara_dt.experiments.relevant_scenarios import (
    run_all_relevant_scenarios,
)


@dataclass(frozen=True)
class ExperimentalMatrixRow:
    """One controlled condition in the experimental matrix."""

    condition: str
    divergence_count: int
    relevant_count: int
    no_assurance: AssuranceOutcome
    global_divergence: AssuranceOutcome
    dara_dt: AssuranceOutcome


@dataclass(frozen=True)
class ExperimentalMatrix:
    """Complete controlled experimental matrix."""

    rows: tuple[ExperimentalMatrixRow, ...]


def run_experimental_matrix() -> ExperimentalMatrix:
    """Execute the current controlled DARA-DT experimental matrix."""

    rows: list[ExperimentalMatrixRow] = []

    # ---------------------------------------------------------
    # Decision-irrelevant divergence conditions
    # ---------------------------------------------------------
    #
    # These conditions vary the number of physical-digital
    # mismatches while ensuring that none of the mismatches
    # affect variables required by the selected decision.
    #
    # This tests whether an assurance policy reacts merely to
    # the presence/amount of divergence rather than to its
    # relevance to the decision being executed.
    # ---------------------------------------------------------

    for divergence_count in (1, 5, 10, 25):
        result = run_count_policy_experiment(
            divergence_count
        )

        rows.append(
            ExperimentalMatrixRow(
                condition=f"irrelevant_{divergence_count}",
                divergence_count=result.divergence_count,
                relevant_count=result.relevant_count,
                no_assurance=result.no_assurance,
                global_divergence=result.global_divergence,
                dara_dt=result.dara_dt,
            )
        )

    # ---------------------------------------------------------
    # Decision-relevant divergence conditions
    # ---------------------------------------------------------
    #
    # These scenarios introduce stale Digital Twin information
    # affecting variables that the current vehicle-assignment
    # decision directly depends on.
    #
    # Current controlled scenarios:
    #   1. vehicle operational status
    #   2. vehicle capacity
    #   3. vehicle availability
    # ---------------------------------------------------------

    for result in run_all_relevant_scenarios():
        rows.append(
            ExperimentalMatrixRow(
                condition=result.scenario,
                divergence_count=result.divergence_count,
                relevant_count=result.relevant_count,
                no_assurance=result.no_assurance,
                global_divergence=result.global_divergence,
                dara_dt=result.dara_dt,
            )
        )

    return ExperimentalMatrix(
        rows=tuple(rows)
    )
