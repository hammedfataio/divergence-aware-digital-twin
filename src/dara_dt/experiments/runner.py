"""Controlled experimental scenario execution for DARA-DT."""

from dara_dt.divergence.injector import DivergenceInjector
from dara_dt.experiments.scenarios import ScenarioType
from dara_dt.twin.digital_twin import DigitalTwin


class ScenarioRunner:
    """Apply controlled divergence scenarios to a Digital Twin."""

    def __init__(self, injector: DivergenceInjector) -> None:
        self.injector = injector

    def apply(
        self,
        scenario: ScenarioType,
        twin: DigitalTwin,
        vehicle_id: str,
    ) -> None:
        """Apply a controlled scenario to the Digital Twin."""

        if scenario == ScenarioType.D0_SYNCHRONISED:
            return

        if scenario == ScenarioType.D2_STATE:
            self.injector.vehicle_state(
                twin=twin,
                vehicle_id=vehicle_id,
                variable="location",
                value="divergent_location",
            )
            return

        if scenario == ScenarioType.D3_OPERATIONAL:
            self.injector.vehicle_state(
                twin=twin,
                vehicle_id=vehicle_id,
                variable="status",
                value="broken_down",
            )
            return

        raise NotImplementedError(
            f"Scenario '{scenario.value}' is not implemented yet."
        )
