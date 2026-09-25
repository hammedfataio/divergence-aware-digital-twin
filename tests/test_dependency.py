"""Tests for decision dependency mapping."""

import pytest

from dara_dt.decision.dependency import DependencyMapper
from dara_dt.decision.model import Decision


def create_assignment_decision() -> Decision:
    """Create a vehicle-assignment decision for testing."""
    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=125.0,
    )


def test_assignment_decision_contains_vehicle_dependencies():
    decision = create_assignment_decision()
    mapper = DependencyMapper()

    dependencies = mapper.dependencies(decision)

    assert "vehicles.vehicle_07.location" in dependencies
    assert "vehicles.vehicle_07.capacity" in dependencies
    assert "vehicles.vehicle_07.available" in dependencies
    assert "vehicles.vehicle_07.status" in dependencies


def test_assignment_decision_contains_order_dependencies():
    decision = create_assignment_decision()
    mapper = DependencyMapper()

    dependencies = mapper.dependencies(decision)

    assert "orders.order_42.location" in dependencies
    assert "orders.order_42.demand" in dependencies
    assert "orders.order_42.deadline" in dependencies
    assert "orders.order_42.status" in dependencies


def test_dependency_mapper_uses_selected_entities():
    decision = Decision(
        decision_id="decision_002",
        action="assign_vehicle",
        vehicle_id="vehicle_99",
        order_id="order_88",
        timestamp=200.0,
    )

    mapper = DependencyMapper()

    dependencies = mapper.dependencies(decision)

    assert "vehicles.vehicle_99.status" in dependencies
    assert "orders.order_88.demand" in dependencies

    assert "vehicles.vehicle_07.status" not in dependencies
    assert "orders.order_42.demand" not in dependencies


def test_unsupported_decision_action_raises_error():
    decision = Decision(
        decision_id="decision_003",
        action="unsupported_action",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=125.0,
    )

    mapper = DependencyMapper()

    with pytest.raises(ValueError):
        mapper.dependencies(decision)
