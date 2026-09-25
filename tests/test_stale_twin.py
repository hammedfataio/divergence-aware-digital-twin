"""Tests for realistic stale Digital Twin scenarios."""

from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.experiments.stale_twin import StaleTwinScenario
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


def create_system():
    """Create a synchronised physical system and Digital Twin."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_07",
            capacity=10.0,
        )
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    return environment, twin


def test_breakdown_changes_physical_vehicle_only():
    environment, twin = create_system()

    scenario = StaleTwinScenario()

    scenario.vehicle_breakdown(
        environment,
        twin,
        "vehicle_07",
    )

    physical_vehicle = environment.get_vehicle("vehicle_07")
    twin_vehicle = twin.get_vehicle("vehicle_07")

    assert physical_vehicle.status == "broken_down"
    assert physical_vehicle.available is False

    assert twin_vehicle["status"] == "operational"
    assert twin_vehicle["available"] is True


def test_breakdown_event_records_physical_twin_mismatch():
    environment, twin = create_system()

    scenario = StaleTwinScenario()

    event = scenario.vehicle_breakdown(
        environment,
        twin,
        "vehicle_07",
    )

    assert event.vehicle_id == "vehicle_07"
    assert event.event_type == "vehicle_breakdown"
    assert event.physical_status == "broken_down"
    assert event.twin_status == "operational"


def test_stale_twin_breakdown_creates_detectable_divergence():
    environment, twin = create_system()

    scenario = StaleTwinScenario()

    scenario.vehicle_breakdown(
        environment,
        twin,
        "vehicle_07",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    paths = {
        divergence.path
        for divergence in divergences
    }

    assert "vehicles.vehicle_07.status" in paths
    assert "vehicles.vehicle_07.available" in paths


def test_resynchronisation_removes_breakdown_divergence():
    environment, twin = create_system()

    scenario = StaleTwinScenario()

    scenario.vehicle_breakdown(
        environment,
        twin,
        "vehicle_07",
    )

    twin.synchronise(
        environment.physical_state()
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    assert divergences == []
