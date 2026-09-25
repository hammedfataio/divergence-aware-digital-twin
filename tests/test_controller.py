"""Tests for the Digital Twin logistics decision controller."""

import pytest

from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


def create_twin() -> DigitalTwin:
    """Create a Digital Twin with vehicles and one customer order."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_01",
            location="node_01",
            capacity=3.0,
        )
    )

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_07",
            capacity=10.0,
        )
    )

    environment.add_order(
        Order(
            order_id="order_42",
            location="node_20",
            demand=5.0,
            deadline=200.0,
        )
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    return twin


def test_controller_selects_eligible_vehicle():
    twin = create_twin()

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_42",
        timestamp=125.0,
        decision_id="decision_001",
    )

    assert decision.vehicle_id == "vehicle_07"
    assert decision.order_id == "order_42"
    assert decision.action == "assign_vehicle"


def test_controller_uses_digital_twin_not_physical_system():
    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_07",
            capacity=10.0,
        )
    )

    environment.add_order(
        Order(
            order_id="order_42",
            location="node_20",
            demand=5.0,
            deadline=200.0,
        )
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    environment.get_vehicle(
        "vehicle_07"
    ).mark_broken_down()

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_42",
        timestamp=125.0,
        decision_id="decision_002",
    )

    assert decision.vehicle_id == "vehicle_07"


def test_controller_rejects_when_no_vehicle_has_capacity():
    twin = create_twin()

    twin.update_vehicle(
        "vehicle_07",
        capacity=4.0,
    )

    controller = LogisticsDecisionController()

    with pytest.raises(ValueError):
        controller.assign_vehicle(
            twin=twin,
            order_id="order_42",
            timestamp=125.0,
            decision_id="decision_003",
        )


def test_controller_rejects_unknown_order():
    twin = create_twin()

    controller = LogisticsDecisionController()

    with pytest.raises(ValueError):
        controller.assign_vehicle(
            twin=twin,
            order_id="order_missing",
            timestamp=125.0,
            decision_id="decision_004",
        )
