"""Order model for the DARA-DT logistics simulation."""

from dataclasses import dataclass


@dataclass
class Order:
    """Represents a customer order in the physical logistics system."""

    order_id: str
    location: str
    demand: float
    deadline: float
    status: str = "waiting"

    def assign(self) -> None:
        """Mark the order as assigned."""
        if self.status != "waiting":
            raise ValueError(
                f"Order {self.order_id} cannot be assigned "
                f"from status '{self.status}'."
            )

        self.status = "assigned"

    def complete(self) -> None:
        """Mark the order as completed."""
        if self.status != "assigned":
            raise ValueError(
                f"Order {self.order_id} cannot be completed "
                f"from status '{self.status}'."
            )

        self.status = "completed"
