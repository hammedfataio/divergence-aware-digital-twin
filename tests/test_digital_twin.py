"""Tests for the DARA-DT Digital Twin."""

import pytest

from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


def create_environment() -> LogisticsEnvironment:
    """Create a small physical environment for testing."""
    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_14",
            capacity=40,
        )
    )

    environment.add_order(
        Order(
            order_id="order_42",
            location="node_21",
            demand=20,
            deadline=180,
        )
    )

    return environment


def test_twin_synchronises_with_physical_state():
    environment = create_environment()
    twin = DigitalTwin()

    twin.synchronise(environment.physical_state())

    vehicle = twin.get_vehicle("vehicle_07")

    assert vehicle["status"] == "operational"
    assert vehicle["available"] is True
    assert vehicle["location"] == "node_14"


def test_physical_change_does_not_automatically_change_twin():
    environment = create_environment()
    twin = DigitalTwin()

    twin.synchronise(environment.physical_state())

    physical_vehicle = environment.get_vehicle("vehicle_07")
    physical_vehicle.mark_broken_down()

    physical_state = environment.physical_state()
    twin_vehicle = twin.get_vehicle("vehicle_07")

    assert physical_state["vehicles"]["vehicle_07"]["status"] == "broken_down"
    assert physical_state["vehicles"]["vehicle_07"]["available"] is False

    assert twin_vehicle["status"] == "operational"
    assert twin_vehicle["available"] is True


def test_twin_can_be_resynchronised():
    environment = create_environment()
    twin = DigitalTwin()

    twin.synchronise(environment.physical_state())

    environment.get_vehicle("vehicle_07").mark_broken_down()

    twin.synchronise(environment.physical_state())

    vehicle = twin.get_vehicle("vehicle_07")

    assert vehicle["status"] == "broken_down"
    assert vehicle["available"] is False


def test_twin_vehicle_can_be_updated_independently():
    environment = create_environment()
    twin = DigitalTwin()

    twin.synchronise(environment.physical_state())

    twin.update_vehicle(
        "vehicle_07",
        location="node_20",
    )

    assert twin.get_vehicle("vehicle_07")["location"] == "node_20"

    assert (
        environment.get_vehicle("vehicle_07").location
        == "node_14"
    )


def test_unknown_twin_vehicle_raises_error():
    twin = DigitalTwin()

    with pytest.raises(KeyError):
        twin.get_vehicle("vehicle_999")
