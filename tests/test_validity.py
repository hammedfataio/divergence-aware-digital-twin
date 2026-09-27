"""Tests for independent physical decision-validity evaluation."""

import pytest

from dara_dt.decision.model import Decision
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.experiments.ground_truth import InterventionLabel


def make_decision() -> Decision:
    """Create a standard vehicle-assignment decision."""

    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_01",
        order_id="order_01",
        timestamp=0.0,
    )


def make_physical_state(
    *,
    capacity: float = 10.0,
    available: bool = True,
    status: str = "operational",
    location: str = "depot",
    demand: float = 5.0,
    order_status: str = "waiting",
) -> dict:
    """Create controlled physical state for validity tests."""

    return {
        "vehicles": {
            "vehicle_01": {
                "vehicle_id": "vehicle_01",
                "capacity": capacity,
                "available": available,
                "status": status,
                "location": location,
            }
        },
        "orders": {
            "order_01": {
                "order_id": "order_01",
                "demand": demand,
                "status": order_status,
                "location": "customer",
            }
        },
    }


def test_valid_physical_decision_requires_no_intervention() -> None:
    """A feasible physical assignment should remain valid."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(),
    )

    assert (
        ground_truth.label
        == InterventionLabel.DO_NOT_INTERVENE
    )


def test_broken_vehicle_requires_intervention() -> None:
    """A physically broken vehicle should invalidate the assignment."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            status="broken_down",
        ),
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_unavailable_vehicle_requires_intervention() -> None:
    """A physically unavailable vehicle should invalidate assignment."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            available=False,
        ),
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_insufficient_capacity_requires_intervention() -> None:
    """Insufficient physical capacity should invalidate assignment."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            capacity=4.0,
            demand=5.0,
        ),
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_exact_capacity_boundary_remains_valid() -> None:
    """Capacity equal to demand should remain physically feasible."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            capacity=5.0,
            demand=5.0,
        ),
    )

    assert (
        ground_truth.label
        == InterventionLabel.DO_NOT_INTERVENE
    )


def test_non_waiting_order_requires_intervention() -> None:
    """An order already being processed should not be reassigned."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            order_status="assigned",
        ),
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_missing_vehicle_is_invalid() -> None:
    """Decision should be invalid when selected vehicle does not exist."""

    validator = PhysicalDecisionValidator()

    physical_state = make_physical_state()
    del physical_state["vehicles"]["vehicle_01"]

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=physical_state,
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_missing_order_is_invalid() -> None:
    """Decision should be invalid when selected order does not exist."""

    validator = PhysicalDecisionValidator()

    physical_state = make_physical_state()
    del physical_state["orders"]["order_01"]

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=physical_state,
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


# ---------------------------------------------------------------------------
# EXP-007 location compatibility
# ---------------------------------------------------------------------------


def test_permitted_physical_location_remains_valid() -> None:
    """A vehicle at a permitted dispatch location should remain valid."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            location="depot",
        ),
        permitted_vehicle_locations={
            "depot",
            "near_depot",
        },
    )

    assert (
        ground_truth.label
        == InterventionLabel.DO_NOT_INTERVENE
    )


def test_alternative_permitted_location_remains_valid() -> None:
    """A divergent but permitted location should remain feasible."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            location="near_depot",
        ),
        permitted_vehicle_locations={
            "depot",
            "near_depot",
        },
    )

    assert (
        ground_truth.label
        == InterventionLabel.DO_NOT_INTERVENE
    )


def test_remote_physical_location_requires_intervention() -> None:
    """A vehicle outside permitted dispatch locations is invalid."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            location="remote_site",
        ),
        permitted_vehicle_locations={
            "depot",
            "near_depot",
        },
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_location_constraint_is_optional_for_earlier_experiments() -> None:
    """Existing experiments should retain their previous semantics.

    Without an explicit permitted-location rule, location should not
    independently invalidate the decision.
    """

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            location="remote_site",
        ),
    )

    assert (
        ground_truth.label
        == InterventionLabel.DO_NOT_INTERVENE
    )


def test_empty_permitted_location_set_is_rejected() -> None:
    """Explicit location validation requires a non-empty rule."""

    validator = PhysicalDecisionValidator()

    with pytest.raises(
        ValueError,
        match="At least one permitted vehicle location is required",
    ):
        validator.ground_truth(
            decision=make_decision(),
            physical_state=make_physical_state(),
            permitted_vehicle_locations=set(),
        )


def test_non_string_permitted_location_is_rejected() -> None:
    """Permitted locations must use explicit string identifiers."""

    validator = PhysicalDecisionValidator()

    with pytest.raises(
        ValueError,
        match="Permitted vehicle locations must be strings.",
    ):
        validator.ground_truth(
            decision=make_decision(),
            physical_state=make_physical_state(),
            permitted_vehicle_locations={
                "depot",
                123,
            },
        )


def test_location_does_not_override_other_invalidity() -> None:
    """Permitted location must not hide another physical failure."""

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=make_decision(),
        physical_state=make_physical_state(
            location="depot",
            status="broken_down",
        ),
        permitted_vehicle_locations={
            "depot",
            "near_depot",
        },
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_validate_returns_location_failure_reason() -> None:
    """Location-invalid decisions should retain an explicit reason."""

    validator = PhysicalDecisionValidator()

    validity = validator.validate(
        decision=make_decision(),
        physical_state=make_physical_state(
            location="remote_site",
        ),
        permitted_vehicle_locations={
            "depot",
            "near_depot",
        },
    )

    assert validity.valid is False
    assert "outside" in validity.reason.lower()
    assert "location" in validity.reason.lower()
