"""Tests for the core physical logistics models."""

import pytest

from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle


def test_vehicle_can_serve_valid_demand():
    vehicle = Vehicle(
        vehicle_id="vehicle_01",
        location="node_01",
        capacity=40,
    )

    assert vehicle.can_serve(20) is True


def test_vehicle_cannot_serve_demand_above_capacity():
    vehicle = Vehicle(
        vehicle_id="vehicle_01",
        location="node_01",
        capacity=10,
    )

    assert vehicle.can_serve(20) is False


def test_broken_vehicle_cannot_serve_order():
    vehicle = Vehicle(
        vehicle_id="vehicle_01",
        location="node_01",
        capacity=40,
    )

    vehicle.mark_broken_down()

    assert vehicle.status == "broken_down"
    assert vehicle.available is False
    assert vehicle.can_serve(20) is False


def test_order_can_be_assigned():
    order = Order(
        order_id="order_01",
        location="node_05",
        demand=20,
        deadline=120,
    )

    order.assign()

    assert order.status == "assigned"


def test_assigned_order_can_be_completed():
    order = Order(
        order_id="order_01",
        location="node_05",
        demand=20,
        deadline=120,
    )

    order.assign()
    order.complete()

    assert order.status == "completed"


def test_waiting_order_cannot_be_completed():
    order = Order(
        order_id="order_01",
        location="node_05",
        demand=20,
        deadline=120,
    )

    with pytest.raises(ValueError):
        order.complete()
