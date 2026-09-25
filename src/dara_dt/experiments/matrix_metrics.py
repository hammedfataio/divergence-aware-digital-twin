"""Aggregate assurance metrics for the controlled experimental matrix."""

from dataclasses import dataclass

from dara_dt.evaluation.metrics import (
    AssuranceMetrics,
    calculate_assurance_metrics,
)
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.experimental_matrix import (
    run_experimental_matrix,
)


@dataclass(frozen=True)
class PolicyMetrics:
    """Aggregate metrics for one assurance policy."""

    policy: str
    metrics: AssuranceMetrics


@dataclass(frozen=True)
class MatrixMetricsResult:
    """Aggregate metrics for all policies in the matrix."""

    condition_count: int
    policies: tuple[PolicyMetrics, ...]


def _collect_outcomes(
    policy: str,
) -> list[AssuranceOutcome]:
    """Collect outcomes for one policy from the experimental matrix."""

    matrix = run_experimental_matrix()

    if policy == "no_assurance":
        return [
            row.no_assurance
            for row in matrix.rows
        ]

    if policy == "global_divergence":
        return [
            row.global_divergence
            for row in matrix.rows
        ]

    if policy == "dara_dt":
        return [
            row.dara_dt
            for row in matrix.rows
        ]

    raise ValueError(
        f"Unknown assurance policy: {policy}"
    )


def run_matrix_metrics() -> MatrixMetricsResult:
    """Calculate aggregate assurance metrics for the matrix."""

    matrix = run_experimental_matrix()

    policy_names = (
        "no_assurance",
        "global_divergence",
        "dara_dt",
    )

    results = []

    for policy in policy_names:
        outcomes = _collect_outcomes(policy)

        metrics = calculate_assurance_metrics(
            outcomes
        )

        results.append(
            PolicyMetrics(
                policy=policy,
                metrics=metrics,
            )
        )

    return MatrixMetricsResult(
        condition_count=len(matrix.rows),
        policies=tuple(results),
    )
