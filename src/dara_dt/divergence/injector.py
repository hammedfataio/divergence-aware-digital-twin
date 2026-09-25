"""Controlled physical-digital divergence injection for DARA-DT."""

from typing import Any

from dara_dt.twin.digital_twin import DigitalTwin


class DivergenceInjector:
    """Inject controlled divergence into a Digital Twin."""

    def vehicle_state(
        self,
        twin: DigitalTwin,
        vehicle_id: str,
        variable: str,
        value: Any,
    ) -> None:
        """Inject divergence into a vehicle state variable."""
        twin.update_vehicle(
            vehicle_id,
            **{variable: value},
        )

    def order_state(
        self,
        twin: DigitalTwin,
        order_id: str,
        variable: str,
        value: Any,
    ) -> None:
        """Inject divergence into an order state variable."""
        twin.update_order(
            order_id,
            **{variable: value},
        )
