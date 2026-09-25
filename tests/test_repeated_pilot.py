"""Tests for repeated DARA-DT pilot evaluation."""

import pytest

from dara_dt.experiments.repeated_pilot import run_repeated_pilot


def test_repeated_pilot_aggregates_all_conditions():
    """Each repetition should evaluate both B and C."""

    result = run_repeated_pilot(repetitions=10)

    assert result.repetitions == 10

    # Each repetition contains two decisions:
    # Condition B and Condition C.
    expected_total = 20

    for metrics in (
        result.no_assurance,
        result.global_divergence,
        result.dara_dt,
    ):
        observed_total = (
            metrics.true_interventions
            + metrics.false_interventions
            + metrics.missed_interventions
            + metrics.correct_non_interventions
        )

        assert observed_total == expected_total


def test_no_assurance_repeated_outcomes():
    """No assurance should miss C but correctly allow B."""

    result = run_repeated_pilot(repetitions=10)

    metrics = result.no_assurance

    assert metrics.true_interventions == 0
    assert metrics.false_interventions == 0
    assert metrics.missed_interventions == 10
    assert metrics.correct_non_interventions == 10


def test_global_divergence_repeated_outcomes():
    """Global divergence should intervene in both B and C."""

    result = run_repeated_pilot(repetitions=10)

    metrics = result.global_divergence

    assert metrics.true_interventions == 10
    assert metrics.false_interventions == 10
    assert metrics.missed_interventions == 0
    assert metrics.correct_non_interventions == 0


def test_dara_dt_repeated_outcomes():
    """DARA-DT should distinguish B from C."""

    result = run_repeated_pilot(repetitions=10)

    metrics = result.dara_dt

    assert metrics.true_interventions == 10
    assert metrics.false_interventions == 0
    assert metrics.missed_interventions == 0
    assert metrics.correct_non_interventions == 10


def test_repeated_pilot_rejects_zero_repetitions():
    """Zero repetitions should be rejected."""

    with pytest.raises(
        ValueError,
        match="repetitions must be greater than zero",
    ):
        run_repeated_pilot(repetitions=0)


def test_repeated_pilot_rejects_negative_repetitions():
    """Negative repetitions should be rejected."""

    with pytest.raises(
        ValueError,
        match="repetitions must be greater than zero",
    ):
        run_repeated_pilot(repetitions=-1)
