"""Tests for controlled DARA-DT experimental scenarios."""

import pytest

from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.injector import DivergenceInjector
from dara_dt.experiments.runner import ScenarioRunner
from dara_dt.experiments.scenarios import ScenarioType
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


def test_d0_remains_synchronised():
    environment, twin = create_system()

    runner = ScenarioRunner(DivergenceInjector())
    detector = DivergenceDetector()

    runner.apply(
        ScenarioType.D0_SYNCHRONISED,
        twin,
        "vehicle_07",
    )

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    assert divergences == []


def test_d2_creates_location_divergence():
    environment, twin = create_system()

    runner = ScenarioRunner(DivergenceInjector())
    detector = DivergenceDetector()

    runner.apply(
        ScenarioType.D2_STATE,
        twin,
        "vehicle_07",
    )

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    paths = {divergence.path for divergence in divergences}

    assert "vehicles.vehicle_07.location" in paths


def test_d3_creates_operational_divergence():
    environment, twin = create_system()

    runner = ScenarioRunner(DivergenceInjector())
    detector = DivergenceDetector()

    runner.apply(
        ScenarioType.D3_OPERATIONAL,
        twin,
        "vehicle_07",
    )

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    paths = {divergence.path for divergence in divergences}

    assert "vehicles.vehicle_07.status" in paths


def test_unimplemented_scenario_raises_error():
    _, twin = create_system()

    runner = ScenarioRunner(DivergenceInjector())

    with pytest.raises(NotImplementedError):
        runner.apply(
            ScenarioType.D1_TEMPORAL,
            twin,
            "vehicle_07",
        )
