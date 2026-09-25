"""Quantitative runtime assurance metrics for DARA-DT."""

from dataclasses import dataclass

from dara_dt.evaluation.outcomes import AssuranceOutcome


@dataclass(frozen=True)
class AssuranceMetrics:
    """Aggregated runtime assurance evaluation metrics."""

    true_interventions: int
    false_interventions: int
    missed_interventions: int
    correct_non_interventions: int
    precision: float
    recall: float
    false_intervention_rate: float
    missed_intervention_rate: float
    accuracy: float


def _safe_divide(numerator: int, denominator: int) -> float:
    """Return zero when a metric denominator is zero."""
    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_assurance_metrics(
    outcomes: list[AssuranceOutcome],
) -> AssuranceMetrics:
    """Calculate aggregate metrics from assurance outcomes."""

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

    precision = _safe_divide(
        true_interventions,
        true_interventions + false_interventions,
    )

    recall = _safe_divide(
        true_interventions,
        true_interventions + missed_interventions,
    )

    false_intervention_rate = _safe_divide(
        false_interventions,
        false_interventions + correct_non_interventions,
    )

    missed_intervention_rate = _safe_divide(
        missed_interventions,
        true_interventions + missed_interventions,
    )

    accuracy = _safe_divide(
        true_interventions + correct_non_interventions,
        total,
    )

    return AssuranceMetrics(
        true_interventions=true_interventions,
        false_interventions=false_interventions,
        missed_interventions=missed_interventions,
        correct_non_interventions=correct_non_interventions,
        precision=precision,
        recall=recall,
        false_intervention_rate=false_intervention_rate,
        missed_intervention_rate=missed_intervention_rate,
        accuracy=accuracy,
    )
