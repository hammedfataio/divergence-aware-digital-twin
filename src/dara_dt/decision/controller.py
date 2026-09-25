"""Logistics decision controller for DARA-DT experiments."""

from dara_dt.decision.model import Decision
from dara_dt.twin.digital_twin import DigitalTwin


class LogisticsDecisionController:
    """Generate vehicle-assignment decisions from Digital Twin state."""

    def assign_vehicle(
        self,
        twin: DigitalTwin,
        order_id: str,
        timestamp: float,
        decision_id: str,
    ) -> Decision:
        """Select an eligible vehicle using the Digital Twin state."""

        orders = twin.state["orders"]
        vehicles = twin.state["vehicles"]

        if order_id not in orders:
            raise ValueError(
                f"Order {order_id} does not exist in the Digital Twin."
            )

        order = orders[order_id]

        eligible_vehicles = []

        for vehicle_id, vehicle in vehicles.items():
            if (
                vehicle["available"]
                and vehicle["status"] == "operational"
                and vehicle["capacity"] >= order["demand"]
            ):
                eligible_vehicles.append(vehicle_id)

        if not eligible_vehicles:
            raise ValueError(
                f"No eligible vehicle available for order {order_id}."
            )

        selected_vehicle_id = sorted(eligible_vehicles)[0]

        return Decision(
            decision_id=decision_id,
            action="assign_vehicle",
            vehicle_id=selected_vehicle_id,
            order_id=order_id,
            timestamp=timestamp,
        )
