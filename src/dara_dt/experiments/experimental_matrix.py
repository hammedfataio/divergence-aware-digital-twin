"""Combined experimental matrix for DARA-DT evaluation."""

from dataclasses import dataclass

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.count_policy_experiment import (
    run_count_policy_experiment,
)
from dara_dt.experiments.relevant_policy_experiment import (
    run_relevant_policy_experiment,
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
    """Complete controlled DARA-DT experimental matrix."""

    rows: tuple[ExperimentalMatrixRow, ...]


def run_experimental_matrix() -> ExperimentalMatrix:
    """Execute the current controlled experimental matrix."""

    rows: list[ExperimentalMatrixRow] = []

    # Decision-irrelevant divergence conditions.
    for divergence_count in (1, 5, 10, 25):
        result = run_count_policy_experiment(
            divergence_count
        )

        rows.append(
            ExperimentalMatrixRow(
                condition=(
                    f"irrelevant_{divergence_count}"
                ),
                divergence_count=result.divergence_count,
                relevant_count=result.relevant_count,
                no_assurance=result.no_assurance,
                global_divergence=result.global_divergence,
                dara_dt=result.dara_dt,
            )
        )

    # Decision-relevant stale-Twin breakdown condition.
    relevant = run_relevant_policy_experiment()

    rows.append(
        ExperimentalMatrixRow(
            condition="relevant_breakdown",
            divergence_count=relevant.divergence_count,
            relevant_count=relevant.relevant_count,
            no_assurance=relevant.no_assurance,
            global_divergence=relevant.global_divergence,
            dara_dt=relevant.dara_dt,
        )
    )

    return ExperimentalMatrix(
        rows=tuple(rows)
    )
