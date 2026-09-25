"""Tests for policy comparison across divergence counts."""

import pytest

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.count_policy_experiment import (
    run_count_policy_experiment,
)


@pytest.mark.parametrize(
    "divergence_count",
    [1, 5, 10, 25],
)
def test_divergence_count_is_preserved(
    divergence_count: int,
):
    """Experiment should create the requested number of mismatches."""

    result = run_count_policy_experiment(
        divergence_count
    )

    assert result.divergence_count == divergence_count
    assert result.relevant_count == 0


@pytest.mark.parametrize(
    "divergence_count",
    [1, 5, 10, 25],
)
def test_no_assurance_correctly_allows_irrelevant_divergence(
    divergence_count: int,
):
    """No assurance allows the physically valid decision."""

    result = run_count_policy_experiment(
        divergence_count
    )

    assert (
        result.no_assurance
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )


@pytest.mark.parametrize(
    "divergence_count",
    [1, 5, 10, 25],
)
def test_global_divergence_false_intervention(
    divergence_count: int,
):
    """Global divergence intervenes despite decision irrelevance."""

    result = run_count_policy_experiment(
        divergence_count
    )

    assert (
        result.global_divergence
        == AssuranceOutcome.FALSE_INTERVENTION
    )


@pytest.mark.parametrize(
    "divergence_count",
    [1, 5, 10, 25],
)
def test_dara_dt_allows_irrelevant_divergence(
    divergence_count: int,
):
    """DARA-DT should ignore divergence unrelated to the decision."""

    result = run_count_policy_experiment(
        divergence_count
    )

    assert (
        result.dara_dt
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )


def test_count_policy_experiment_rejects_zero():
    """Zero divergence is outside this experiment."""

    with pytest.raises(
        ValueError,
        match="divergence_count must be at least 1",
    ):
        run_count_policy_experiment(0)


def test_count_policy_experiment_rejects_negative_value():
    """Negative divergence counts must be rejected."""

    with pytest.raises(
        ValueError,
        match="divergence_count must be at least 1",
    ):
        run_count_policy_experiment(-1)
