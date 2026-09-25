"""Controlled generator for decision-relevance experiments."""

from dara_dt.decision.model import Decision
from dara_dt.divergence.injector import DivergenceInjector
from dara_dt.experiments.relevance_conditions import RelevanceCondition
from dara_dt.twin.digital_twin import DigitalTwin


class RelevanceConditionGenerator:
    """Generate controlled B and C experimental conditions."""

    def __init__(self, injector: DivergenceInjector) -> None:
        self.injector = injector

    def apply(
        self,
        condition: RelevanceCondition,
        twin: DigitalTwin,
        decision: Decision,
    ) -> None:
        """Apply the requested experimental condition."""

        if condition == (
            RelevanceCondition.B_HIGH_DIVERGENCE_LOW_RELEVANCE
        ):
            self._apply_condition_b(twin, decision)
            return

        if condition == (
            RelevanceCondition.C_LOW_DIVERGENCE_HIGH_RELEVANCE
        ):
            self._apply_condition_c(twin, decision)
            return

        raise ValueError(
            f"Unsupported relevance condition: {condition}"
        )

    def _apply_condition_b(
        self,
        twin: DigitalTwin,
        decision: Decision,
    ) -> None:
        """Inject multiple divergences unrelated to the decision."""

        unrelated_vehicle_ids = [
            vehicle_id
            for vehicle_id in twin.state["vehicles"]
            if vehicle_id != decision.vehicle_id
        ]

        if len(unrelated_vehicle_ids) < 2:
            raise ValueError(
                "Condition B requires at least two unrelated vehicles."
            )

        self.injector.vehicle_state(
            twin=twin,
            vehicle_id=unrelated_vehicle_ids[0],
            variable="location",
            value="divergent_location",
        )

        self.injector.vehicle_state(
            twin=twin,
            vehicle_id=unrelated_vehicle_ids[1],
            variable="status",
            value="broken_down",
        )

    def _apply_condition_c(
        self,
        twin: DigitalTwin,
        decision: Decision,
    ) -> None:
        """Inject one divergence directly relevant to the decision."""

        self.injector.vehicle_state(
            twin=twin,
            vehicle_id=decision.vehicle_id,
            variable="status",
            value="broken_down",
        )
