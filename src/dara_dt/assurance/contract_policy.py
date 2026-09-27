"""Runtime-contract assurance baseline for DARA-DT.

This module provides a deliberately strong comparator for EXP-007.

Unlike DARA-DT, the runtime-contract baseline does not reason through:

    physical-digital divergence
        -> decision relevance
        -> decision impact

Instead, it directly evaluates whether runtime evidence satisfies the
execution conditions required by the proposed logistics decision.

This distinction is important for the DARA-DT novelty evaluation. If
direct runtime contracts provide equivalent assurance behaviour with less
reasoning complexity, the incremental value of explicit divergence-aware
reasoning must be reconsidered.
"""

from collections.abc import Collection
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ContractDecision(str, Enum):
    """Runtime-contract decision."""

    ALLOW = "allow"
    INTERVENE = "intervene"


@dataclass(frozen=True)
class ContractResult:
    """Result returned by a runtime-contract check."""

    decision_id: str
    dependency: str
    decision: ContractDecision
    satisfied: bool
    observed_value: Any
    required_value: Any
    reason: str

    @property
    def intervene(self) -> bool:
        """Return whether runtime intervention is required."""

        return self.decision == ContractDecision.INTERVENE


class RuntimeContractPolicy:
    """Evaluate direct execution contracts from runtime evidence.

    The policy deliberately avoids explicit physical-digital divergence
    reasoning. It asks only whether the currently observed state satisfies
    the operational condition required for execution.

    Ground truth must remain separate from the evidence supplied here.
    """

    def evaluate_capacity(
        self,
        decision_id: str,
        observed_capacity: float,
        required_demand: float,
    ) -> ContractResult:
        """Evaluate the capacity execution contract."""

        self._require_numeric(
            observed_capacity,
            "Observed capacity",
        )
        self._require_numeric(
            required_demand,
            "Required demand",
        )

        satisfied = float(observed_capacity) >= float(required_demand)

        if satisfied:
            return ContractResult(
                decision_id=decision_id,
                dependency="vehicle.capacity",
                decision=ContractDecision.ALLOW,
                satisfied=True,
                observed_value=observed_capacity,
                required_value=required_demand,
                reason=(
                    "Observed vehicle capacity satisfies the demand "
                    "required by the proposed decision."
                ),
            )

        return ContractResult(
            decision_id=decision_id,
            dependency="vehicle.capacity",
            decision=ContractDecision.INTERVENE,
            satisfied=False,
            observed_value=observed_capacity,
            required_value=required_demand,
            reason=(
                "Observed vehicle capacity is below the demand required "
                "by the proposed decision."
            ),
        )

    def evaluate_status(
        self,
        decision_id: str,
        observed_status: str,
        required_status: str = "operational",
    ) -> ContractResult:
        """Evaluate the operational-status execution contract."""

        if not isinstance(observed_status, str):
            raise ValueError(
                "Observed operational status must be a string."
            )

        if not isinstance(required_status, str) or not required_status:
            raise ValueError(
                "Required operational status must be a non-empty string."
            )

        satisfied = observed_status == required_status

        if satisfied:
            return ContractResult(
                decision_id=decision_id,
                dependency="vehicle.status",
                decision=ContractDecision.ALLOW,
                satisfied=True,
                observed_value=observed_status,
                required_value=required_status,
                reason=(
                    "Observed vehicle status satisfies the operational "
                    "state required by the proposed decision."
                ),
            )

        return ContractResult(
            decision_id=decision_id,
            dependency="vehicle.status",
            decision=ContractDecision.INTERVENE,
            satisfied=False,
            observed_value=observed_status,
            required_value=required_status,
            reason=(
                "Observed vehicle status does not satisfy the operational "
                "state required by the proposed decision."
            ),
        )

    def evaluate_availability(
        self,
        decision_id: str,
        observed_available: bool,
        required_available: bool = True,
    ) -> ContractResult:
        """Evaluate the vehicle-availability execution contract."""

        if not isinstance(observed_available, bool):
            raise ValueError(
                "Observed availability must be boolean."
            )

        if not isinstance(required_available, bool):
            raise ValueError(
                "Required availability must be boolean."
            )

        satisfied = observed_available is required_available

        if satisfied:
            return ContractResult(
                decision_id=decision_id,
                dependency="vehicle.available",
                decision=ContractDecision.ALLOW,
                satisfied=True,
                observed_value=observed_available,
                required_value=required_available,
                reason=(
                    "Observed vehicle availability satisfies the "
                    "condition required by the proposed decision."
                ),
            )

        return ContractResult(
            decision_id=decision_id,
            dependency="vehicle.available",
            decision=ContractDecision.INTERVENE,
            satisfied=False,
            observed_value=observed_available,
            required_value=required_available,
            reason=(
                "Observed vehicle availability does not satisfy the "
                "condition required by the proposed decision."
            ),
        )

    def evaluate_location(
        self,
        decision_id: str,
        observed_location: str,
        permitted_locations: Collection[str],
    ) -> ContractResult:
        """Evaluate the location-compatibility execution contract."""

        if not isinstance(observed_location, str):
            raise ValueError(
                "Observed location must be a string."
            )

        permitted = frozenset(permitted_locations)

        if not permitted:
            raise ValueError(
                "At least one permitted dispatch location is required."
            )

        if any(not isinstance(location, str) for location in permitted):
            raise ValueError(
                "Permitted dispatch locations must be strings."
            )

        satisfied = observed_location in permitted

        if satisfied:
            return ContractResult(
                decision_id=decision_id,
                dependency="vehicle.location",
                decision=ContractDecision.ALLOW,
                satisfied=True,
                observed_value=observed_location,
                required_value=tuple(sorted(permitted)),
                reason=(
                    "Observed vehicle location satisfies the permitted "
                    "dispatch-location contract."
                ),
            )

        return ContractResult(
            decision_id=decision_id,
            dependency="vehicle.location",
            decision=ContractDecision.INTERVENE,
            satisfied=False,
            observed_value=observed_location,
            required_value=tuple(sorted(permitted)),
            reason=(
                "Observed vehicle location is outside the permitted "
                "dispatch locations for the proposed decision."
            ),
        )

    def evaluate_location_availability(
        self,
        decision_id: str,
        observed_location: str,
        observed_available: bool,
        permitted_locations: Collection[str],
        required_available: bool = True,
    ) -> ContractResult:
        """Evaluate the combined location-and-availability contract.

        Both conditions must be satisfied for autonomous execution.
        """

        if not isinstance(observed_location, str):
            raise ValueError(
                "Observed location must be a string."
            )

        if not isinstance(observed_available, bool):
            raise ValueError(
                "Observed availability must be boolean."
            )

        if not isinstance(required_available, bool):
            raise ValueError(
                "Required availability must be boolean."
            )

        permitted = frozenset(permitted_locations)

        if not permitted:
            raise ValueError(
                "At least one permitted dispatch location is required."
            )

        if any(not isinstance(location, str) for location in permitted):
            raise ValueError(
                "Permitted dispatch locations must be strings."
            )

        location_satisfied = observed_location in permitted
        availability_satisfied = (
            observed_available is required_available
        )

        satisfied = location_satisfied and availability_satisfied

        required_value = {
            "permitted_locations": tuple(sorted(permitted)),
            "required_available": required_available,
        }

        observed_value = {
            "location": observed_location,
            "available": observed_available,
        }

        if satisfied:
            return ContractResult(
                decision_id=decision_id,
                dependency="vehicle.location_availability",
                decision=ContractDecision.ALLOW,
                satisfied=True,
                observed_value=observed_value,
                required_value=required_value,
                reason=(
                    "Observed vehicle location and availability satisfy "
                    "the execution contract for the proposed decision."
                ),
            )

        failed_conditions: list[str] = []

        if not location_satisfied:
            failed_conditions.append("location")

        if not availability_satisfied:
            failed_conditions.append("availability")

        return ContractResult(
            decision_id=decision_id,
            dependency="vehicle.location_availability",
            decision=ContractDecision.INTERVENE,
            satisfied=False,
            observed_value=observed_value,
            required_value=required_value,
            reason=(
                "Observed runtime state violates the following execution "
                f"contract conditions: {', '.join(failed_conditions)}."
            ),
        )

    @staticmethod
    def _require_numeric(
        value: Any,
        label: str,
    ) -> None:
        """Validate numeric contract inputs without accepting booleans."""

        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise ValueError(f"{label} must be numeric.")
