"""Decision dependency mapping for DARA-DT."""

from dara_dt.decision.model import Decision


class DependencyMapper:
    """Maps a logistics decision to the state variables it depends on."""

    def dependencies(self, decision: Decision) -> set[str]:
        """Return the state-variable dependencies for a decision."""

        if decision.action == "assign_vehicle":
            return {
                f"vehicles.{decision.vehicle_id}.location",
                f"vehicles.{decision.vehicle_id}.capacity",
                f"vehicles.{decision.vehicle_id}.available",
                f"vehicles.{decision.vehicle_id}.status",
                f"orders.{decision.order_id}.location",
                f"orders.{decision.order_id}.demand",
                f"orders.{decision.order_id}.deadline",
                f"orders.{decision.order_id}.status",
            }

        raise ValueError(
            f"Unsupported decision action '{decision.action}'."
        )
