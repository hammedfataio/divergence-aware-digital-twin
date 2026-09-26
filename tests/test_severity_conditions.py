"""Tests for EXP-004 divergence severity conditions."""

from dara_dt.experiments.severity_conditions import (
    SeverityCondition,
    build_severity_conditions,
)


def test_build_severity_conditions_returns_seven_conditions() -> None:
    """EXP-004 should contain the seven predefined severity conditions."""

    conditions = build_severity_conditions()

    assert len(conditions) == 7
    assert tuple(condition.name for condition in conditions) == (
        "S0",
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",
    )


def test_divergence_magnitude_is_absolute_capacity_difference() -> None:
    """Magnitude should measure the physical-digital capacity difference."""

    condition = SeverityCondition(
        name="test",
        twin_capacity=10,
        physical_capacity=7,
        order_demand=5,
    )

    assert condition.divergence_magnitude == 3


def test_no_divergence_has_zero_magnitude() -> None:
    """S0 should represent the synchronised physical-digital state."""

    condition = build_severity_conditions()[0]

    assert condition.name == "S0"
    assert condition.divergence_magnitude == 0
    assert condition.physically_valid is True


def test_conditions_s0_to_s4_remain_physically_valid() -> None:
    """Capacity remains sufficient through the decision boundary."""

    conditions = build_severity_conditions()

    for condition in conditions[:5]:
        assert condition.physically_valid is True


def test_conditions_s5_and_s6_are_physically_invalid() -> None:
    """Capacity below order demand should invalidate the assignment."""

    conditions = build_severity_conditions()

    for condition in conditions[5:]:
        assert condition.physically_valid is False


def test_s4_is_valid_at_exact_capacity_boundary() -> None:
    """Physical capacity equal to demand should remain valid."""

    condition = build_severity_conditions()[4]

    assert condition.name == "S4"
    assert condition.physical_capacity == 5
    assert condition.order_demand == 5
    assert condition.divergence_magnitude == 5
    assert condition.physically_valid is True


def test_s5_crosses_decision_validity_boundary() -> None:
    """S5 should be the first condition that invalidates the assignment."""

    condition = build_severity_conditions()[5]

    assert condition.name == "S5"
    assert condition.physical_capacity == 4
    assert condition.order_demand == 5
    assert condition.divergence_magnitude == 6
    assert condition.physically_valid is False


def test_magnitude_increases_across_conditions() -> None:
    """Severity conditions should have monotonically increasing magnitude."""

    conditions = build_severity_conditions()

    magnitudes = tuple(
        condition.divergence_magnitude
        for condition in conditions
    )

    assert magnitudes == (0, 1, 3, 4, 5, 6, 8)
    assert list(magnitudes) == sorted(magnitudes)
