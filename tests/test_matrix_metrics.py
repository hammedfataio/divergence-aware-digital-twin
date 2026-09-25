"""Tests for aggregate experimental-matrix assurance metrics."""

from dara_dt.experiments.matrix_metrics import (
    run_matrix_metrics,
)


def _metrics_by_policy():
    """Return aggregate metrics indexed by policy name."""

    result = run_matrix_metrics()

    return {
        item.policy: item.metrics
        for item in result.policies
    }


def test_matrix_metrics_cover_all_conditions():
    """Metrics should aggregate all seven controlled conditions."""

    result = run_matrix_metrics()

    assert result.condition_count == 7
    assert len(result.policies) == 3


def test_no_assurance_metrics():
    """No assurance should miss all required interventions."""

    metrics = _metrics_by_policy()["no_assurance"]

    assert metrics.true_interventions == 0
    assert metrics.false_interventions == 0
    assert metrics.missed_interventions == 3
    assert metrics.correct_non_interventions == 4

    assert metrics.recall == 0.0
    assert metrics.missed_intervention_rate == 1.0
    assert metrics.accuracy == 4 / 7


def test_global_divergence_metrics():
    """Global divergence should intervene on every detected mismatch."""

    metrics = _metrics_by_policy()["global_divergence"]

    assert metrics.true_interventions == 3
    assert metrics.false_interventions == 4
    assert metrics.missed_interventions == 0
    assert metrics.correct_non_interventions == 0

    assert metrics.precision == 3 / 7
    assert metrics.recall == 1.0
    assert metrics.false_intervention_rate == 1.0
    assert metrics.accuracy == 3 / 7


def test_dara_dt_metrics():
    """DARA-DT should classify all current controlled cases correctly."""

    metrics = _metrics_by_policy()["dara_dt"]

    assert metrics.true_interventions == 3
    assert metrics.false_interventions == 0
    assert metrics.missed_interventions == 0
    assert metrics.correct_non_interventions == 4

    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.false_intervention_rate == 0.0
    assert metrics.missed_intervention_rate == 0.0
    assert metrics.accuracy == 1.0
