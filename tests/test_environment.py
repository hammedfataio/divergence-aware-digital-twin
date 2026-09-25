"""Tests for the physical logistics simulation environment."""

import pytest

from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle


def test_environment_starts_at_zero():
    environment = LogisticsEnvironment()

    assert environment.time == 0.0


def test_vehicle_can_be_added():
    environment = LogisticsEnvironment()

    vehicle = Vehicle(
        vehicle_id="vehicle_01",
        location="node_01",
        capacity=40,
    )

    environment.add_vehicle(vehicle)

    assert environment.get_vehicle("vehicle_01") is vehicle


def test_order_can_be_added():
    environment = LogisticsEnvironment()

    order = Order(
        order_id="order_01",
        location="node_05",
        demand=20,
        deadline=120,
    )

    environment.add_order(order)

    assert environment.get_order("order_01") is order


def test_simulation_time_advances():
    environment = LogisticsEnvironment()

    environment.advance(10)

    assert environment.time == 10.0


def test_negative_time_raises_error():
    environment = LogisticsEnvironment()

    with pytest.raises(ValueError):
        environment.advance(-1)


def test_duplicate_vehicle_is_rejected():
    environment = LogisticsEnvironment()

    vehicle = Vehicle(
        vehicle_id="vehicle_01",
        location="node_01",
        capacity=40,
    )

    environment.add_vehicle(vehicle)

    with pytest.raises(ValueError):
        environment.add_vehicle(vehicle)


def test_physical_state_snapshot():
    environment = LogisticsEnvironment()

    vehicle = Vehicle(
        vehicle_id="vehicle_07",
        location="node_14",
        capacity=40,
    )

    order = Order(
        order_id="order_42",
        location="node_21",
        demand=20,
        deadline=180,
    )

    environment.add_vehicle(vehicle)
    environment.add_order(order)

    state = environment.physical_state()

    assert state["time"] == 0.0
    assert state["vehicles"]["vehicle_07"]["status"] == "operational"
    assert state["vehicles"]["vehicle_07"]["available"] is True
    assert state["orders"]["order_42"]["status"] == "waiting"


def test_physical_state_reflects_vehicle_breakdown():
    environment = LogisticsEnvironment()

    vehicle = Vehicle(
        vehicle_id="vehicle_07",
        location="node_14",
        capacity=40,
    )

    environment.add_vehicle(vehicle)

    vehicle.mark_broken_down()

    state = environment.physical_state()

    assert state["vehicles"]["vehicle_07"]["status"] == "broken_down"
    assert state["vehicles"]["vehicle_07"]["available"] is False
