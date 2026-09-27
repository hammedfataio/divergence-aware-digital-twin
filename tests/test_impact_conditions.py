"""Tests for EXP-005 decision-impact experimental conditions."""

from dara_dt.experiments.impact_conditions import (
    build_impact_conditions,
)


def test_builds_fifteen_controlled_conditions() -> None:
    """EXP-005 should contain the complete I0-I14 condition set."""

    conditions = build_impact_conditions()

    assert len(conditions) == 15


def test_synchronised_condition_has_no_divergence() -> None:
    """I0 should represent a synchronised physical-digital state."""

    condition = build_impact_conditions()[0]

    assert condition.name == "I0_synchronised"
    assert condition.divergence_magnitude == 0
    assert condition.physical_margin == 5
    assert condition.physically_valid is True


def test_exact_capacity_boundary_remains_physically_valid() -> None:
    """I4 should sit exactly at the physical validity boundary."""

    condition = build_impact_conditions()[4]

    assert condition.name == "I4_boundary"
    assert condition.physical_margin == 0
    assert condition.physically_valid is True


def test_crossing_capacity_boundary_is_invalid() -> None:
    """I5 should cross from feasible to physically invalid."""

    condition = build_impact_conditions()[5]

    assert condition.name == "I5_invalid"
    assert condition.physical_margin == -1
    assert condition.physically_valid is False


def test_same_divergence_can_produce_different_validity() -> None:
    """Equal divergence magnitude must not imply equal decision impact."""

    conditions = build_impact_conditions()

    valid = conditions[7]
    invalid = conditions[8]

    assert valid.divergence_magnitude == 3
    assert invalid.divergence_magnitude == 3

    assert valid.physical_margin == 2
    assert invalid.physical_margin == -1

    assert valid.physically_valid is True
    assert invalid.physically_valid is False


def test_tight_boundary_changes_with_decision_requirement() -> None:
    """Decision validity should follow the specific demand boundary."""

    conditions = build_impact_conditions()

    boundary = conditions[11]
    invalid = conditions[12]

    assert boundary.physical_margin == 0
    assert boundary.physically_valid is True

    assert invalid.physical_margin == -1
    assert invalid.physically_valid is False


def test_large_system_uses_its_own_decision_boundary() -> None:
    """Larger-capacity conditions should retain decision-specific validity."""

    conditions = build_impact_conditions()

    valid = conditions[13]
    invalid = conditions[14]

    assert valid.physical_margin == 1
    assert valid.physically_valid is True

    assert invalid.physical_margin == -1
    assert invalid.physically_valid is False


def test_physical_validity_is_defined_by_margin() -> None:
    """Every condition should derive validity from its physical margin."""

    for condition in build_impact_conditions():
        assert condition.physically_valid == (
            condition.physical_margin >= 0
        )


def test_condition_names_are_unique() -> None:
    """Each controlled condition should have a unique identifier."""

    conditions = build_impact_conditions()
    names = [condition.name for condition in conditions]

    assert len(names) == len(set(names))
