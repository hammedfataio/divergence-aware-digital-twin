"""Decision model for the DARA-DT research prototype."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    """Represents a proposed logistics decision."""

    decision_id: str
    action: str
    vehicle_id: str
    order_id: str
    timestamp: float
