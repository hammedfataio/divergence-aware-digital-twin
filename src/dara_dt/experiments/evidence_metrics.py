"""Aggregate metrics for EXP-006 imperfect runtime evidence.

This module evaluates assurance performance across the controlled
EXP-006 evidence conditions.

The experiment compares:

B1 — decision-relevance assurance
B2 — deterministic decision-impact assurance with perfect evidence
P1 — evidence-aware assurance operating on imperfect runtime evidence

Metrics are calculated against independent physical ground truth.
"""

from dataclasses import dataclass

from dara_dt.experiments.evidence_experiment import (
    EvidenceExperimentResult,
    run_evidence_experiment,
)


TRUE_INTERVENTION = "true_intervention"
FALSE_INTERVENTION = "false_intervention"
MISSED_INTERVENTION = "missed_intervention"
CORRECT_NON_INTERVENTION = "correct_non_intervention"


@dataclass(frozen=True)
class EvidencePolicyMetrics:
    """Aggregate assurance metrics for one policy."""

    policy: str
    conditions: int

    true_interventions: int
    false_interventions: int
    missed_interventions: int
    correct_non_interventions: int

    accuracy: float
    precision: float
    recall: float
    false_intervention_rate: float
    missed_intervention_rate: float
    autonomy_availability: float


def _safe_divide(
    numerator: int,
    denominator: int,
) -> float:
    """Safely divide two integers."""

    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_policy_metrics(
    policy: str,
    outcomes: tuple[str, ...],
) -> EvidencePolicyMetrics:
    """Calculate aggregate metrics for one assurance policy."""

    true_interventions = outcomes.count(TRUE_INTERVENTION)
    false_interventions = outcomes.count(FALSE_INTERVENTION)
    missed_interventions = outcomes.count(MISSED_INTERVENTION)
    correct_non_interventions = outcomes.count(
        CORRECT_NON_INTERVENTION
    )

    conditions = len(outcomes)

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

    valid_conditions = (
        false_interventions
        + correct_non_interventions
    )

    accuracy = _safe_divide(
        correct,
        conditions,
    )

    precision = _safe_divide(
        true_interventions,
        interventions,
    )

    recall = _safe_divide(
        true_interventions,
        required_interventions,
    )

    false_intervention_rate = _safe_divide(
        false_interventions,
        valid_conditions,
    )

    missed_intervention_rate = _safe_divide(
        missed_interventions,
        required_interventions,
    )

    # Autonomous execution remains available when assurance
    # correctly or incorrectly allows the AI-generated decision.
    #
    # Therefore:
    #
    # autonomy availability =
    #     correct non-interventions + missed interventions
    #
    # divided by all experimental conditions.
    autonomy_availability = _safe_divide(
        correct_non_interventions
        + missed_interventions,
        conditions,
    )

    return EvidencePolicyMetrics(
        policy=policy,
        conditions=conditions,
        true_interventions=true_interventions,
        false_interventions=false_interventions,
        missed_interventions=missed_interventions,
        correct_non_interventions=correct_non_interventions,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        false_intervention_rate=false_intervention_rate,
        missed_intervention_rate=missed_intervention_rate,
        autonomy_availability=autonomy_availability,
    )


def _extract_outcome_values(
    results: tuple[EvidenceExperimentResult, ...],
    attribute: str,
) -> tuple[str, ...]:
    """Extract outcome values from experiment results."""

    return tuple(
        getattr(result, attribute).outcome.value
        for result in results
    )


def calculate_exp006_metrics(
) -> tuple[EvidencePolicyMetrics, ...]:
    """Calculate aggregate metrics for all EXP-006 policies."""

    results = run_evidence_experiment()

    relevance_outcomes = _extract_outcome_values(
        results,
        "relevance_outcome",
    )

    deterministic_impact_outcomes = _extract_outcome_values(
        results,
        "deterministic_impact_outcome",
    )

    evidence_aware_outcomes = _extract_outcome_values(
        results,
        "evidence_aware_outcome",
    )

    return (
        calculate_policy_metrics(
            policy="decision_relevance",
            outcomes=relevance_outcomes,
        ),
        calculate_policy_metrics(
            policy="deterministic_impact",
            outcomes=deterministic_impact_outcomes,
        ),
        calculate_policy_metrics(
            policy="evidence_aware_impact",
            outcomes=evidence_aware_outcomes,
        ),
    )


def _format_rate(value: float) -> str:
    """Format a rate to three decimal places."""

    return f"{value:.3f}"


def main() -> None:
    """Run EXP-006 and print aggregate policy metrics."""

    metrics = calculate_exp006_metrics()

    print(
        "policy",
        "conditions",
        "TI",
        "FI",
        "MI",
        "CNI",
        "accuracy",
        "precision",
        "recall",
        "FI_rate",
        "MI_rate",
        "autonomy",
    )

    for metric in metrics:
        print(
            metric.policy,
            metric.conditions,
            metric.true_interventions,
            metric.false_interventions,
            metric.missed_interventions,
            metric.correct_non_interventions,
            _format_rate(metric.accuracy),
            _format_rate(metric.precision),
            _format_rate(metric.recall),
            _format_rate(metric.false_intervention_rate),
            _format_rate(metric.missed_intervention_rate),
            _format_rate(metric.autonomy_availability),
        )


if __name__ == "__main__":
    main()
