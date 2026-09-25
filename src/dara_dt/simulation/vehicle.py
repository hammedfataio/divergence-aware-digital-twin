"""Vehicle model for the DARA-DT logistics simulation."""

from dataclasses import dataclass


@dataclass
class Vehicle:
    """Represents a vehicle in the physical logistics system."""

    vehicle_id: str
    location: str
    capacity: float
    available: bool = True
    status: str = "operational"

    def can_serve(self, demand: float) -> bool:
        """Return True when the vehicle can serve the requested demand."""
        return (
            self.available
            and self.status == "operational"
            and self.capacity >= demand
        )

    def mark_broken_down(self) -> None:
        """Mark the vehicle as unavailable because of a breakdown."""
        self.status = "broken_down"
        self.available = False
