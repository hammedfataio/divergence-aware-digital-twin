"""Tests for physical–digital divergence detection."""

from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.simulation.environment import LogisticsEnvironment
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

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    return environment, twin


def test_no_divergence_when_states_are_synchronised():
    environment, twin = create_system()

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    assert divergences == []


def test_detector_finds_vehicle_breakdown_divergence():
    environment, twin = create_system()

    environment.get_vehicle("vehicle_07").mark_broken_down()

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    paths = {divergence.path for divergence in divergences}

    assert "vehicles.vehicle_07.status" in paths
    assert "vehicles.vehicle_07.available" in paths


def test_detector_records_physical_and_twin_values():
    environment, twin = create_system()

    environment.get_vehicle("vehicle_07").mark_broken_down()

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    status_divergence = next(
        divergence
        for divergence in divergences
        if divergence.path == "vehicles.vehicle_07.status"
    )

    assert status_divergence.physical_value == "broken_down"
    assert status_divergence.twin_value == "operational"


def test_detector_finds_location_divergence():
    environment, twin = create_system()

    environment.get_vehicle("vehicle_07").location = "node_20"

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    paths = {divergence.path for divergence in divergences}

    assert "vehicles.vehicle_07.location" in paths


def test_resynchronisation_removes_divergence():
    environment, twin = create_system()

    environment.get_vehicle("vehicle_07").mark_broken_down()

    detector = DivergenceDetector()

    before = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    assert len(before) > 0

    twin.synchronise(environment.physical_state())

    after = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    assert after == []
