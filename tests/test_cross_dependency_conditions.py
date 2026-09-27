"""Tests for the pre-registered EXP-007 condition matrix."""

from collections import Counter

from dara_dt.experiments.cross_dependency_conditions import (
    DependencyFamily,
    build_cross_dependency_conditions,
)


def test_exp007_contains_exactly_twelve_conditions() -> None:
    """EXP-007 should contain the pre-registered 12-condition matrix."""

    conditions = build_cross_dependency_conditions()

    assert len(conditions) == 12


def test_condition_ids_are_unique() -> None:
    """Every EXP-007 condition must have a stable unique identifier."""

    conditions = build_cross_dependency_conditions()

    condition_ids = [condition.condition_id for condition in conditions]

    assert len(condition_ids) == len(set(condition_ids))


def test_condition_ids_match_pre_registered_matrix() -> None:
    """Condition identifiers should not drift after pre-registration."""

    conditions = build_cross_dependency_conditions()

    assert [condition.condition_id for condition in conditions] == [
        "CAP-0",
        "CAP-1",
        "CAP-2",
        "CAP-3",
        "STATUS-0",
        "STATUS-1",
        "STATUS-2",
        "STATUS-3",
        "LOC-0",
        "LOC-1",
        "LOC-2",
        "LOC-3",
    ]


def test_each_dependency_family_has_four_conditions() -> None:
    """The matrix should contain four cases per dependency family."""

    conditions = build_cross_dependency_conditions()

    counts = Counter(condition.family for condition in conditions)

    assert counts == {
        DependencyFamily.CAPACITY: 4,
        DependencyFamily.STATUS: 4,
        DependencyFamily.LOCATION_AVAILABILITY: 4,
    }


def test_zero_conditions_have_no_divergence() -> None:
    """C0 cases should represent synchronized system and Twin state."""

    conditions = build_cross_dependency_conditions()

    zero_conditions = [
        condition
        for condition in conditions
        if condition.condition_id.endswith("-0")
    ]

    assert len(zero_conditions) == 3

    for condition in zero_conditions:
        assert condition.has_selected_vehicle_divergence is False
        assert condition.has_unrelated_vehicle_divergence is False
        assert condition.has_any_divergence is False


def test_one_conditions_contain_only_irrelevant_divergence() -> None:
    """C1 cases should contain divergence only on an unrelated vehicle."""

    conditions = build_cross_dependency_conditions()

    one_conditions = [
        condition
        for condition in conditions
        if condition.condition_id.endswith("-1")
    ]

    assert len(one_conditions) == 3

    for condition in one_conditions:
        assert condition.has_selected_vehicle_divergence is False
        assert condition.has_unrelated_vehicle_divergence is True
        assert condition.has_any_divergence is True


def test_two_conditions_contain_selected_dependency_divergence() -> None:
    """C2 cases should contain decision-relevant divergence."""

    conditions = build_cross_dependency_conditions()

    two_conditions = [
        condition
        for condition in conditions
        if condition.condition_id.endswith("-2")
    ]

    assert len(two_conditions) == 3

    for condition in two_conditions:
        assert condition.has_selected_vehicle_divergence is True
        assert condition.has_unrelated_vehicle_divergence is False
        assert condition.has_any_divergence is True


def test_three_conditions_contain_selected_dependency_divergence() -> None:
    """C3 cases should contain decision-relevant divergence."""

    conditions = build_cross_dependency_conditions()

    three_conditions = [
        condition
        for condition in conditions
        if condition.condition_id.endswith("-3")
    ]

    assert len(three_conditions) == 3

    for condition in three_conditions:
        assert condition.has_selected_vehicle_divergence is True
        assert condition.has_unrelated_vehicle_divergence is False
        assert condition.has_any_divergence is True


def test_capacity_control_is_physically_valid() -> None:
    """CAP-0 should satisfy the physical capacity requirement."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["CAP-0"]

    assert condition.physical_selected_value >= condition.order_demand


def test_capacity_irrelevant_case_keeps_selected_vehicle_valid() -> None:
    """CAP-1 should alter only an unrelated vehicle."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["CAP-1"]

    assert condition.physical_selected_value >= condition.order_demand
    assert (
        condition.physical_selected_value
        == condition.twin_selected_value
    )


def test_capacity_relevant_but_valid_case_remains_feasible() -> None:
    """CAP-2 should diverge without invalidating the assignment."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["CAP-2"]

    assert (
        condition.physical_selected_value
        != condition.twin_selected_value
    )
    assert condition.physical_selected_value >= condition.order_demand


def test_capacity_invalid_case_is_physically_infeasible() -> None:
    """CAP-3 should cross the physical capacity-validity boundary."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["CAP-3"]

    assert (
        condition.physical_selected_value
        != condition.twin_selected_value
    )
    assert condition.physical_selected_value < condition.order_demand


def test_status_control_is_operational() -> None:
    """STATUS-0 should satisfy the required physical status."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["STATUS-0"]

    assert condition.physical_selected_value == condition.required_status


def test_status_irrelevant_case_keeps_selected_vehicle_operational() -> None:
    """STATUS-1 should change only the unrelated vehicle."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["STATUS-1"]

    assert condition.physical_selected_value == condition.required_status
    assert (
        condition.physical_selected_value
        == condition.twin_selected_value
    )


def test_status_relevant_but_valid_case_remains_operational() -> None:
    """STATUS-2 should diverge while remaining physically valid."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["STATUS-2"]

    assert (
        condition.physical_selected_value
        != condition.twin_selected_value
    )
    assert condition.physical_selected_value == condition.required_status


def test_status_invalid_case_is_not_operational() -> None:
    """STATUS-3 should violate the required operational state."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["STATUS-3"]

    assert (
        condition.physical_selected_value
        != condition.twin_selected_value
    )
    assert condition.physical_selected_value != condition.required_status


def test_location_control_is_available_and_permitted() -> None:
    """LOC-0 should satisfy both location and availability requirements."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["LOC-0"]

    location, available = condition.physical_selected_value

    assert available is condition.required_available
    assert location in condition.permitted_locations


def test_location_irrelevant_case_keeps_selected_vehicle_valid() -> None:
    """LOC-1 should alter only an unrelated vehicle."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["LOC-1"]

    location, available = condition.physical_selected_value

    assert (
        condition.physical_selected_value
        == condition.twin_selected_value
    )
    assert available is condition.required_available
    assert location in condition.permitted_locations


def test_location_relevant_but_valid_case_remains_dispatchable() -> None:
    """LOC-2 should diverge without invalidating dispatch."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["LOC-2"]

    location, available = condition.physical_selected_value

    assert (
        condition.physical_selected_value
        != condition.twin_selected_value
    )
    assert available is condition.required_available
    assert location in condition.permitted_locations


def test_location_invalid_case_is_not_dispatchable() -> None:
    """LOC-3 should violate physical dispatch requirements."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    condition = conditions["LOC-3"]

    location, available = condition.physical_selected_value

    assert (
        condition.physical_selected_value
        != condition.twin_selected_value
    )

    assert (
        available is not condition.required_available
        or location not in condition.permitted_locations
    )


def test_only_three_conditions_are_physically_invalid() -> None:
    """The matrix should contain one invalid case per dependency family."""

    conditions = {
        condition.condition_id: condition
        for condition in build_cross_dependency_conditions()
    }

    invalid_ids: list[str] = []

    for condition_id, condition in conditions.items():
        if condition.family == DependencyFamily.CAPACITY:
            invalid = (
                condition.physical_selected_value
                < condition.order_demand
            )

        elif condition.family == DependencyFamily.STATUS:
            invalid = (
                condition.physical_selected_value
                != condition.required_status
            )

        else:
            location, available = condition.physical_selected_value

            invalid = (
                available is not condition.required_available
                or location not in condition.permitted_locations
            )

        if invalid:
            invalid_ids.append(condition_id)

    assert invalid_ids == [
        "CAP-3",
        "STATUS-3",
        "LOC-3",
    ]
