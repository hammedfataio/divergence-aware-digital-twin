"""Tests for decision-relevant divergence scenarios."""

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.relevant_scenarios import (
    run_all_relevant_scenarios,
    run_availability_divergence,
    run_capacity_divergence,
    run_status_divergence,
)


def _assert_relevant_intervention(result):
    """Validate expected behaviour for relevant divergence."""

    assert result.divergence_count >= 1
    assert result.relevant_count >= 1

    assert (
        result.no_assurance
        == AssuranceOutcome.MISSED_INTERVENTION
    )

    assert (
        result.global_divergence
        == AssuranceOutcome.TRUE_INTERVENTION
    )

    assert (
        result.dara_dt
        == AssuranceOutcome.TRUE_INTERVENTION
    )


def test_status_divergence():
    """Status divergence should require intervention."""

    result = run_status_divergence()

    assert result.scenario == "relevant_vehicle_status"

    _assert_relevant_intervention(result)


def test_capacity_divergence():
    """Capacity divergence should require intervention."""

    result = run_capacity_divergence()

    assert result.scenario == "relevant_vehicle_capacity"

    _assert_relevant_intervention(result)


def test_availability_divergence():
    """Availability divergence should require intervention."""

    result = run_availability_divergence()

    assert (
        result.scenario
        == "relevant_vehicle_availability"
    )

    _assert_relevant_intervention(result)


def test_all_relevant_scenarios():
    """All controlled relevant scenarios should execute."""

    results = run_all_relevant_scenarios()

    assert len(results) == 3

    names = {
        result.scenario
        for result in results
    }

    assert names == {
        "relevant_vehicle_status",
        "relevant_vehicle_capacity",
        "relevant_vehicle_availability",
    }


def test_all_scenarios_are_decision_relevant():
    """Every scenario must affect a decision dependency."""

    for result in run_all_relevant_scenarios():
        assert result.relevant_count > 0
