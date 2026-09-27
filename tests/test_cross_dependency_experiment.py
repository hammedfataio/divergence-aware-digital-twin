"""Tests for EXP-007 cross-dependency experiment execution."""

from collections import Counter

from dara_dt.experiments.cross_dependency_experiment import (
    run_cross_dependency_condition,
    run_cross_dependency_experiment,
)
from dara_dt.experiments.cross_dependency_conditions import (
    DependencyFamily,
    build_cross_dependency_conditions,
)
from dara_dt.experiments.ground_truth import (
    InterventionLabel,
)


def test_exp007_runs_all_registered_conditions() -> None:
    """The experiment should execute all 12 pre-registered conditions."""

    results = run_cross_dependency_experiment()

    assert len(results) == 12


def test_exp007_preserves_condition_order() -> None:
    """Results should follow the registered experimental order."""

    results = run_cross_dependency_experiment()

    assert [
        result.condition.condition_id
        for result in results
    ] == [
        condition.condition_id
        for condition in build_cross_dependency_conditions()
    ]


def test_each_dependency_family_is_executed_four_times() -> None:
    """Each dependency family should contain four cases."""

    results = run_cross_dependency_experiment()

    counts = Counter(
        result.condition.family
        for result in results
    )

    assert counts == {
        DependencyFamily.CAPACITY: 4,
        DependencyFamily.STATUS: 4,
        DependencyFamily.LOCATION_AVAILABILITY: 4,
    }


def test_cap3_requires_intervention_ground_truth() -> None:
    """CAP-3 should be physically invalid."""

    condition = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }["CAP-3"]

    result = run_cross_dependency_condition(condition)

    assert (
        result.ground_truth.label
        == InterventionLabel.INTERVENE
    )


def test_status3_requires_intervention_ground_truth() -> None:
    """STATUS-3 should be physically invalid."""

    condition = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }["STATUS-3"]

    result = run_cross_dependency_condition(condition)

    assert (
        result.ground_truth.label
        == InterventionLabel.INTERVENE
    )


def test_location3_requires_intervention_ground_truth() -> None:
    """LOC-3 should be physically invalid."""

    condition = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }["LOC-3"]

    result = run_cross_dependency_condition(condition)

    assert (
        result.ground_truth.label
        == InterventionLabel.INTERVENE
    )


def test_valid_cases_are_not_marked_invalid() -> None:
    """Relevant divergence does not automatically mean invalidity."""

    valid_ids = [
        "CAP-2",
        "STATUS-2",
        "LOC-2",
    ]

    conditions = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }

    for condition_id in valid_ids:
        result = run_cross_dependency_condition(
            conditions[condition_id]
        )

        assert (
            result.ground_truth.label
            == InterventionLabel.DO_NOT_INTERVENE
        )


def test_irrelevant_divergence_cases_contain_divergence() -> None:
    """C1 cases should still contain detectable divergence."""

    conditions = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }

    for condition_id in (
        "CAP-1",
        "STATUS-1",
        "LOC-1",
    ):
        result = run_cross_dependency_condition(
            conditions[condition_id]
        )

        assert result.divergence_count > 0


def test_relevant_divergence_is_detected() -> None:
    """C2 and C3 cases should contain decision-relevant divergence."""

    conditions = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }

    for condition_id in (
        "CAP-2",
        "CAP-3",
        "STATUS-2",
        "STATUS-3",
        "LOC-2",
        "LOC-3",
    ):
        result = run_cross_dependency_condition(
            conditions[condition_id]
        )

        assert (
            result.relevant_divergence_count
            >= 1
        )


def test_runtime_contract_produces_results() -> None:
    """The contract baseline should execute for every condition."""

    results = run_cross_dependency_experiment()

    for result in results:
        assert result.contract_dependency
        assert isinstance(
            result.contract_satisfied,
            bool,
        )


def test_decision_impact_produces_results() -> None:
    """DARA-DT impact reasoning should execute for every condition."""

    results = run_cross_dependency_experiment()

    for result in results:
        assert result.impact_dependency
        assert result.impact_state


def test_exp007_keeps_policy_comparison_complete() -> None:
    """All five assurance strategies should produce outcomes."""

    results = run_cross_dependency_experiment()

    for result in results:
        assert result.no_assurance.outcome
        assert result.global_divergence.outcome
        assert result.decision_relevance.outcome
        assert result.decision_impact.outcome
        assert result.runtime_contract.outcome


def test_cap3_decision_impact_invalidates() -> None:
    """Capacity failure should be identified by impact reasoning."""

    condition = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }["CAP-3"]

    result = run_cross_dependency_condition(condition)

    assert (
        result.impact_state
        == "invalidating"
    )


def test_status3_decision_impact_invalidates() -> None:
    """Status failure should be identified by impact reasoning."""

    condition = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }["STATUS-3"]

    result = run_cross_dependency_condition(condition)

    assert (
        result.impact_state
        == "invalidating"
    )


def test_loc3_decision_impact_invalidates() -> None:
    """Location failure should be identified by impact reasoning."""

    condition = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }["LOC-3"]

    result = run_cross_dependency_condition(condition)

    assert (
        result.impact_state
        == "invalidating"
    )


def test_loc2_remains_valid_despite_location_difference() -> None:
    """Permitted location movement should not become invalid."""

    condition = {
        item.condition_id: item
        for item in build_cross_dependency_conditions()
    }["LOC-2"]

    result = run_cross_dependency_condition(condition)

    assert (
        result.ground_truth.label
        == InterventionLabel.DO_NOT_INTERVENE
    )

    assert result.impact_state != "invalidating"
