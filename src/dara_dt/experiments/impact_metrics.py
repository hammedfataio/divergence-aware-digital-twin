"""Aggregate policy metrics for EXP-005.

This module calculates quantitative assurance metrics across the
controlled EXP-005 decision-impact conditions.

The metrics are derived from experimental outcomes rather than being
hard-coded for any particular policy.
"""

from dataclasses import dataclass

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.impact_experiment import (
    ImpactExperimentResult,
    run_impact_experiment,
)


@dataclass(frozen=True)
class ImpactPolicyMetrics:
    """Aggregate assurance metrics for one policy."""

    policy: str
    total_conditions: int
    true_interventions: int
    false_interventions: int
    missed_interventions: int
    correct_non_interventions: int
    assurance_accuracy: float
    intervention_precision: float
    intervention_recall: float
    autonomy_availability: float


def _safe_ratio(
    numerator: int,
    denominator: int,
) -> float:
    """Return a ratio while safely handling a zero denominator."""

    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_policy_metrics(
    policy: str,
    outcomes: tuple[AssuranceOutcome, ...],
) -> ImpactPolicyMetrics:
    """Calculate aggregate metrics for one assurance policy."""

    true_interventions = outcomes.count(
        AssuranceOutcome.TRUE_INTERVENTION
    )
    false_interventions = outcomes.count(
        AssuranceOutcome.FALSE_INTERVENTION
    )
    missed_interventions = outcomes.count(
        AssuranceOutcome.MISSED_INTERVENTION
    )
    correct_non_interventions = outcomes.count(
        AssuranceOutcome.CORRECT_NON_INTERVENTION
    )

    total = len(outcomes)

    correct = (
        true_interventions
        + correct_non_interventions
    )

    interventions = (
        true_interventions
        + false_interventions
    )

    required_interventions = (
        true_interventions
        + missed_interventions
    )

    autonomous_executions = (
        missed_interventions
        + correct_non_interventions
    )

    return ImpactPolicyMetrics(
        policy=policy,
        total_conditions=total,
        true_interventions=true_interventions,
        false_interventions=false_interventions,
        missed_interventions=missed_interventions,
        correct_non_interventions=correct_non_interventions,
        assurance_accuracy=_safe_ratio(
            correct,
            total,
        ),
        intervention_precision=_safe_ratio(
            true_interventions,
            interventions,
        ),
        intervention_recall=_safe_ratio(
            true_interventions,
            required_interventions,
        ),
        autonomy_availability=_safe_ratio(
            autonomous_executions,
            total,
        ),
    )


def _extract_outcomes(
    results: tuple[ImpactExperimentResult, ...],
    attribute: str,
) -> tuple[AssuranceOutcome, ...]:
    """Extract assurance outcomes from experiment results."""

    return tuple(
        getattr(result, attribute).outcome
        for result in results
    )


def calculate_impact_metrics(
    results: tuple[ImpactExperimentResult, ...] | None = None,
) -> tuple[ImpactPolicyMetrics, ...]:
    """Calculate metrics for all EXP-005 assurance policies."""

    if results is None:
        results = run_impact_experiment()

    policies = (
        ("no_assurance", "no_assurance"),
        ("global_divergence", "global_divergence"),
        ("fixed_magnitude", "fixed_magnitude"),
        ("decision_relevance", "decision_relevance"),
        ("decision_impact", "decision_impact"),
    )

    return tuple(
        calculate_policy_metrics(
            policy=policy_name,
            outcomes=_extract_outcomes(
                results,
                attribute,
            ),
        )
        for policy_name, attribute in policies
    )


if __name__ == "__main__":
    for metrics in calculate_impact_metrics():
        print(
            metrics.policy,
            {
                "conditions": metrics.total_conditions,
                "TI": metrics.true_interventions,
                "FI": metrics.false_interventions,
                "MI": metrics.missed_interventions,
                "CNI": metrics.correct_non_interventions,
                "accuracy": round(
                    metrics.assurance_accuracy,
                    3,
                ),
                "precision": round(
                    metrics.intervention_precision,
                    3,
                ),
                "recall": round(
                    metrics.intervention_recall,
                    3,
                ),
                "autonomy_availability": round(
                    metrics.autonomy_availability,
                    3,
                ),
            },
        )
