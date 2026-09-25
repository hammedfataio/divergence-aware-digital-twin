"""Digital Twin state representation for DARA-DT."""

from copy import deepcopy
from typing import Any


class DigitalTwin:
    """Maintains a digital representation of the physical logistics system."""

    def __init__(self) -> None:
        self._state: dict[str, Any] = {
            "time": 0.0,
            "vehicles": {},
            "orders": {},
        }

    @property
    def state(self) -> dict[str, Any]:
        """Return a copy of the current Digital Twin state."""
        return deepcopy(self._state)

    def synchronise(self, physical_state: dict[str, Any]) -> None:
        """Synchronise the Digital Twin with a physical-state snapshot."""
        self._state = deepcopy(physical_state)

    def update_vehicle(
        self,
        vehicle_id: str,
        **updates: Any,
    ) -> None:
        """Update selected attributes of a vehicle in the Digital Twin."""
        if vehicle_id not in self._state["vehicles"]:
            raise KeyError(
                f"Unknown vehicle '{vehicle_id}' in Digital Twin."
            )

        self._state["vehicles"][vehicle_id].update(updates)

    def update_order(
        self,
        order_id: str,
        **updates: Any,
    ) -> None:
        """Update selected attributes of an order in the Digital Twin."""
        if order_id not in self._state["orders"]:
            raise KeyError(
                f"Unknown order '{order_id}' in Digital Twin."
            )

        self._state["orders"][order_id].update(updates)

    def get_vehicle(self, vehicle_id: str) -> dict[str, Any]:
        """Return a copy of a vehicle's Digital Twin state."""
        try:
            return deepcopy(self._state["vehicles"][vehicle_id])
        except KeyError as exc:
            raise KeyError(
                f"Unknown vehicle '{vehicle_id}' in Digital Twin."
            ) from exc

    def get_order(self, order_id: str) -> dict[str, Any]:
        """Return a copy of an order's Digital Twin state."""
        try:
            return deepcopy(self._state["orders"][order_id])
        except KeyError as exc:
            raise KeyError(
                f"Unknown order '{order_id}' in Digital Twin."
            ) from exc
