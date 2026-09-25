"""Tests for controlled physical-digital divergence injection."""

from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.injector import DivergenceInjector
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


def create_system():
    """Create a synchronised physical system and Digital Twin."""
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

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    return environment, twin


def test_vehicle_location_divergence_can_be_injected():
    environment, twin = create_system()

    injector = DivergenceInjector()
    detector = DivergenceDetector()

    injector.vehicle_state(
        twin=twin,
        vehicle_id="vehicle_07",
        variable="location",
        value="node_30",
    )

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    paths = {divergence.path for divergence in divergences}

    assert "vehicles.vehicle_07.location" in paths


def test_injection_does_not_change_physical_state():
    environment, twin = create_system()

    injector = DivergenceInjector()

    injector.vehicle_state(
        twin=twin,
        vehicle_id="vehicle_07",
        variable="location",
        value="node_30",
    )

    assert environment.get_vehicle("vehicle_07").location == "node_14"
    assert twin.get_vehicle("vehicle_07")["location"] == "node_30"


def test_operational_divergence_can_be_injected():
    environment, twin = create_system()

    injector = DivergenceInjector()
    detector = DivergenceDetector()

    injector.vehicle_state(
        twin=twin,
        vehicle_id="vehicle_07",
        variable="status",
        value="broken_down",
    )

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    status_divergence = next(
        divergence
        for divergence in divergences
        if divergence.path == "vehicles.vehicle_07.status"
    )

    assert status_divergence.physical_value == "operational"
    assert status_divergence.twin_value == "broken_down"


def test_order_divergence_can_be_injected():
    environment, twin = create_system()

    injector = DivergenceInjector()
    detector = DivergenceDetector()

    injector.order_state(
        twin=twin,
        order_id="order_42",
        variable="demand",
        value=35,
    )

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    paths = {divergence.path for divergence in divergences}

    assert "orders.order_42.demand" in paths
