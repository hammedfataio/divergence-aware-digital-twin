"""Tests for the controlled divergence-count experiment."""

import pytest

from dara_dt.experiments.divergence_count import (
    run_irrelevant_divergence_count,
)


@pytest.mark.parametrize(
    "divergence_count",
    [1, 5, 10, 25],
)
def test_irrelevant_divergence_count_is_controlled(
    divergence_count: int,
):
    """Injected divergence count should equal detected count."""

    result = run_irrelevant_divergence_count(
        divergence_count
    )

    assert result.injected_count == divergence_count
    assert result.detected_count == divergence_count


@pytest.mark.parametrize(
    "divergence_count",
    [1, 5, 10, 25],
)
def test_irrelevant_divergence_remains_decision_irrelevant(
    divergence_count: int,
):
    """Increasing unrelated divergence must not create relevance."""

    result = run_irrelevant_divergence_count(
        divergence_count
    )

    assert result.relevant_count == 0
    assert result.selected_vehicle_id == "vehicle_00"


def test_divergence_count_rejects_zero():
    """Zero is outside the experiment definition."""

    with pytest.raises(
        ValueError,
        match="divergence_count must be at least 1",
    ):
        run_irrelevant_divergence_count(0)


def test_divergence_count_rejects_negative_value():
    """Negative divergence counts must be rejected."""

    with pytest.raises(
        ValueError,
        match="divergence_count must be at least 1",
    ):
        run_irrelevant_divergence_count(-1)
