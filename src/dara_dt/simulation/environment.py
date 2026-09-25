"""Physical logistics simulation environment for DARA-DT."""

from dataclasses import dataclass, field

import simpy

from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle


@dataclass
class LogisticsEnvironment:
    """Maintains the authoritative physical state of the logistics system."""

    env: simpy.Environment = field(default_factory=simpy.Environment)
    vehicles: dict[str, Vehicle] = field(default_factory=dict)
    orders: dict[str, Order] = field(default_factory=dict)

    @property
    def time(self) -> float:
        """Return the current simulation time."""
        return float(self.env.now)

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Add a vehicle to the physical environment."""
        if vehicle.vehicle_id in self.vehicles:
            raise ValueError(
                f"Vehicle '{vehicle.vehicle_id}' already exists."
            )

        self.vehicles[vehicle.vehicle_id] = vehicle

    def add_order(self, order: Order) -> None:
        """Add an order to the physical environment."""
        if order.order_id in self.orders:
            raise ValueError(
                f"Order '{order.order_id}' already exists."
            )

        self.orders[order.order_id] = order

    def get_vehicle(self, vehicle_id: str) -> Vehicle:
        """Return a vehicle by identifier."""
        try:
            return self.vehicles[vehicle_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown vehicle '{vehicle_id}'."
            ) from exc

    def get_order(self, order_id: str) -> Order:
        """Return an order by identifier."""
        try:
            return self.orders[order_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown order '{order_id}'."
            ) from exc

    def advance(self, duration: float) -> None:
        """Advance simulation time by the specified duration."""
        if duration < 0:
            raise ValueError("Simulation duration cannot be negative.")

        self.env.run(until=self.env.now + duration)

    def physical_state(self) -> dict:
        """Return a snapshot of the authoritative physical state."""
        return {
            "time": self.time,
            "vehicles": {
                vehicle_id: {
                    "location": vehicle.location,
                    "capacity": vehicle.capacity,
                    "available": vehicle.available,
                    "status": vehicle.status,
                }
                for vehicle_id, vehicle in self.vehicles.items()
            },
            "orders": {
                order_id: {
                    "location": order.location,
                    "demand": order.demand,
                    "deadline": order.deadline,
                    "status": order.status,
                }
                for order_id, order in self.orders.items()
            },
        }
