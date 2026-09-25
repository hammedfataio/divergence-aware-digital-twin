"""Tests for DARA-DT runtime assurance metrics."""

import pytest

from dara_dt.evaluation.metrics import calculate_assurance_metrics
from dara_dt.evaluation.outcomes import AssuranceOutcome


def test_metrics_are_calculated_correctly():
    outcomes = [
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.FALSE_INTERVENTION,
        AssuranceOutcome.MISSED_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
    ]

    metrics = calculate_assurance_metrics(outcomes)

    assert metrics.true_interventions == 2
    assert metrics.false_interventions == 1
    assert metrics.missed_interventions == 1
    assert metrics.correct_non_interventions == 2

    assert metrics.precision == pytest.approx(2 / 3)
    assert metrics.recall == pytest.approx(2 / 3)
    assert metrics.false_intervention_rate == pytest.approx(1 / 3)
    assert metrics.missed_intervention_rate == pytest.approx(1 / 3)
    assert metrics.accuracy == pytest.approx(4 / 6)


def test_perfect_assurance_has_perfect_metrics():
    outcomes = [
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
    ]

    metrics = calculate_assurance_metrics(outcomes)

    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.false_intervention_rate == 0.0
    assert metrics.missed_intervention_rate == 0.0
    assert metrics.accuracy == 1.0


def test_empty_outcomes_are_handled_safely():
    metrics = calculate_assurance_metrics([])

    assert metrics.true_interventions == 0
    assert metrics.false_interventions == 0
    assert metrics.missed_interventions == 0
    assert metrics.correct_non_interventions == 0

    assert metrics.precision == 0.0
    assert metrics.recall == 0.0
    assert metrics.false_intervention_rate == 0.0
    assert metrics.missed_intervention_rate == 0.0
    assert metrics.accuracy == 0.0


def test_all_missed_interventions():
    outcomes = [
        AssuranceOutcome.MISSED_INTERVENTION,
        AssuranceOutcome.MISSED_INTERVENTION,
    ]

    metrics = calculate_assurance_metrics(outcomes)

    assert metrics.recall == 0.0
    assert metrics.missed_intervention_rate == 1.0
    assert metrics.accuracy == 0.0
