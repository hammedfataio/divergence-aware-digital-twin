"""Realistic stale Digital Twin scenarios for DARA-DT experiments."""

from dataclasses import dataclass

from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class StaleTwinEvent:
    """Record of a physical event not yet reflected in the Digital Twin."""

    vehicle_id: str
    event_type: str
    physical_status: str
    twin_status: str
    event_time: float


class StaleTwinScenario:
    """Generate realistic physical-world changes with a stale Digital Twin."""

    def vehicle_breakdown(
        self,
        environment: LogisticsEnvironment,
        twin: DigitalTwin,
        vehicle_id: str,
    ) -> StaleTwinEvent:
        """
        Break down a physical vehicle without synchronising the Digital Twin.

        This represents delayed, lost, or unavailable telemetry where the
        physical system changes but the Digital Twin temporarily retains
        an outdated operational state.
        """

        vehicle = environment.get_vehicle(vehicle_id)

        twin_vehicle = twin.get_vehicle(vehicle_id)

        if twin_vehicle["status"] != "operational":
            raise ValueError(
                "Digital Twin vehicle must initially be operational."
            )

        vehicle.mark_broken_down()

        return StaleTwinEvent(
            vehicle_id=vehicle_id,
            event_type="vehicle_breakdown",
            physical_status=vehicle.status,
            twin_status=twin_vehicle["status"],
            event_time=environment.time,
        )
