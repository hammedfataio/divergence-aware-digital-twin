"""Independent physical decision-validity evaluation for DARA-DT."""

from dataclasses import dataclass

from dara_dt.decision.model import Decision
from dara_dt.experiments.ground_truth import (
    GroundTruth,
    InterventionLabel,
)


@dataclass(frozen=True)
class DecisionValidity:
    """Result of evaluating a decision against physical ground truth."""

    decision_id: str
    valid: bool
    reason: str


class PhysicalDecisionValidator:
    """Evaluate decisions using physical state only."""

    def validate(
        self,
        decision: Decision,
        physical_state: dict,
    ) -> DecisionValidity:
        """Determine whether a decision is physically valid."""

        if decision.action != "assign_vehicle":
            raise ValueError(
                f"Unsupported decision action: {decision.action}"
            )

        vehicles = physical_state["vehicles"]
        orders = physical_state["orders"]

        if decision.vehicle_id not in vehicles:
            return DecisionValidity(
                decision_id=decision.decision_id,
                valid=False,
                reason="Selected vehicle does not exist physically.",
            )

        if decision.order_id not in orders:
            return DecisionValidity(
                decision_id=decision.decision_id,
                valid=False,
                reason="Selected order does not exist physically.",
            )

        vehicle = vehicles[decision.vehicle_id]
        order = orders[decision.order_id]

        if not vehicle["available"]:
            return DecisionValidity(
                decision_id=decision.decision_id,
                valid=False,
                reason="Selected vehicle is physically unavailable.",
            )

        if vehicle["status"] != "operational":
            return DecisionValidity(
                decision_id=decision.decision_id,
                valid=False,
                reason="Selected vehicle is not physically operational.",
            )

        if vehicle["capacity"] < order["demand"]:
            return DecisionValidity(
                decision_id=decision.decision_id,
                valid=False,
                reason="Selected vehicle has insufficient capacity.",
            )

        if order["status"] != "waiting":
            return DecisionValidity(
                decision_id=decision.decision_id,
                valid=False,
                reason="Selected order is not awaiting assignment.",
            )

        return DecisionValidity(
            decision_id=decision.decision_id,
            valid=True,
            reason="Decision is valid in the physical system.",
        )

    def ground_truth(
        self,
        decision: Decision,
        physical_state: dict,
    ) -> GroundTruth:
        """Convert physical validity into an intervention label."""

        validity = self.validate(
            decision,
            physical_state,
        )

        label = (
            InterventionLabel.DO_NOT_INTERVENE
            if validity.valid
            else InterventionLabel.INTERVENE
        )

        return GroundTruth(
            decision_id=decision.decision_id,
            label=label,
            reason=validity.reason,
        )
