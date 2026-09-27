"""Independent physical decision-validity evaluation for DARA-DT.

Physical validity is evaluated from physical state only and remains
independent from runtime assurance behaviour.

The validator supports the existing logistics feasibility rules and
optionally evaluates dispatch-location compatibility when an experiment
defines an explicit set of permitted physical locations.
"""

from collections.abc import Collection
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
        permitted_vehicle_locations: Collection[str] | None = None,
    ) -> DecisionValidity:
        """Determine whether a decision is physically valid.

        Args:
            decision:
                Proposed logistics decision.

            physical_state:
                Independent physical-system state used as experimental
                ground truth.

            permitted_vehicle_locations:
                Optional experiment-defined set of physical locations from
                which the selected vehicle is permitted to execute the
                assignment.

                When omitted, location compatibility is not evaluated.
                This preserves the semantics of experiments that pre-date
                the explicit location-validity condition introduced for
                EXP-007.
        """

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

        if permitted_vehicle_locations is not None:
            permitted = frozenset(permitted_vehicle_locations)

            if not permitted:
                raise ValueError(
                    "At least one permitted vehicle location is required "
                    "when location compatibility is evaluated."
                )

            if any(
                not isinstance(location, str)
                for location in permitted
            ):
                raise ValueError(
                    "Permitted vehicle locations must be strings."
                )

            if vehicle["location"] not in permitted:
                return DecisionValidity(
                    decision_id=decision.decision_id,
                    valid=False,
                    reason=(
                        "Selected vehicle is outside the physical "
                        "locations permitted for this assignment."
                    ),
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
        permitted_vehicle_locations: Collection[str] | None = None,
    ) -> GroundTruth:
        """Convert independent physical validity into an intervention label."""

        validity = self.validate(
            decision=decision,
            physical_state=physical_state,
            permitted_vehicle_locations=permitted_vehicle_locations,
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
