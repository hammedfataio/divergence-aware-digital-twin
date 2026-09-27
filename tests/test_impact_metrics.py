"""Tests for EXP-005 aggregate policy metrics."""

import pytest

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.impact_metrics import (
    calculate_impact_metrics,
    calculate_policy_metrics,
)


def metrics_by_policy():
    """Return EXP-005 metrics indexed by policy name."""

    return {
        metrics.policy: metrics
        for metrics in calculate_impact_metrics()
    }


def test_calculate_policy_metrics_counts_outcomes() -> None:
    """Outcome categories should be counted correctly."""

    outcomes = (
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.FALSE_INTERVENTION,
        AssuranceOutcome.MISSED_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
    )

    metrics = calculate_policy_metrics(
        policy="test_policy",
        outcomes=outcomes,
    )

    assert metrics.total_conditions == 5
    assert metrics.true_interventions == 2
    assert metrics.false_interventions == 1
    assert metrics.missed_interventions == 1
    assert metrics.correct_non_interventions == 1


def test_calculate_policy_metrics_accuracy() -> None:
    """Accuracy should include correct interventions and non-interventions."""

    outcomes = (
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.FALSE_INTERVENTION,
        AssuranceOutcome.MISSED_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
    )

    metrics = calculate_policy_metrics(
        policy="test_policy",
        outcomes=outcomes,
    )

    assert metrics.assurance_accuracy == pytest.approx(3 / 5)


def test_calculate_policy_metrics_precision() -> None:
    """Precision should measure correctness among interventions."""

    outcomes = (
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.FALSE_INTERVENTION,
    )

    metrics = calculate_policy_metrics(
        policy="test_policy",
        outcomes=outcomes,
    )

    assert metrics.intervention_precision == pytest.approx(2 / 3)


def test_calculate_policy_metrics_recall() -> None:
    """Recall should measure detected required interventions."""

    outcomes = (
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.MISSED_INTERVENTION,
    )

    metrics = calculate_policy_metrics(
        policy="test_policy",
        outcomes=outcomes,
    )

    assert metrics.intervention_recall == pytest.approx(2 / 3)


def test_autonomy_availability_counts_non_interventions() -> None:
    """Autonomy availability should measure autonomous executions."""

    outcomes = (
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.FALSE_INTERVENTION,
        AssuranceOutcome.MISSED_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
    )

    metrics = calculate_policy_metrics(
        policy="test_policy",
        outcomes=outcomes,
    )

    assert metrics.autonomy_availability == pytest.approx(2 / 4)


def test_zero_denominator_is_handled_safely() -> None:
    """Undefined precision and recall should safely return zero."""

    metrics = calculate_policy_metrics(
        policy="empty",
        outcomes=(),
    )

    assert metrics.total_conditions == 0
    assert metrics.assurance_accuracy == 0.0
    assert metrics.intervention_precision == 0.0
    assert metrics.intervention_recall == 0.0
    assert metrics.autonomy_availability == 0.0


def test_exp005_contains_five_policies() -> None:
    """EXP-005 should evaluate all five assurance strategies."""

    metrics = calculate_impact_metrics()

    assert len(metrics) == 5

    assert {
        result.policy
        for result in metrics
    } == {
        "no_assurance",
        "global_divergence",
        "fixed_magnitude",
        "decision_relevance",
        "decision_impact",
    }


def test_every_policy_covers_all_fifteen_conditions() -> None:
    """Every policy should be evaluated on the same conditions."""

    for metrics in calculate_impact_metrics():
        assert metrics.total_conditions == 15


def test_outcome_counts_sum_to_total() -> None:
    """Each condition must belong to exactly one outcome category."""

    for metrics in calculate_impact_metrics():
        total = (
            metrics.true_interventions
            + metrics.false_interventions
            + metrics.missed_interventions
            + metrics.correct_non_interventions
        )

        assert total == metrics.total_conditions


def test_decision_impact_reduces_false_interventions() -> None:
    """Impact-aware assurance should improve on relevance-only over-intervention."""

    metrics = metrics_by_policy()

    assert (
        metrics["decision_impact"].false_interventions
        < metrics["decision_relevance"].false_interventions
    )


def test_decision_impact_preserves_required_interventions() -> None:
    """Impact-aware assurance should not miss invalid decisions."""

    metrics = metrics_by_policy()

    assert metrics["decision_impact"].missed_interventions == 0


def test_equal_divergence_result_is_reflected_in_metrics() -> None:
    """Impact-aware assurance should outperform fixed magnitude on misses."""

    metrics = metrics_by_policy()

    assert (
        metrics["decision_impact"].missed_interventions
        < metrics["fixed_magnitude"].missed_interventions
    )
