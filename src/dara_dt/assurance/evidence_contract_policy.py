"""Evidence-aware runtime-contract baseline for EXP-008.

This module provides a stronger runtime-contract comparator for EXP-008.

The policy evaluates direct decision requirements using runtime evidence,
while explicitly accounting for evidence quality.

AVAILABLE evidence:
    Evaluate the direct runtime contract.

STALE, MISSING, or CONFLICTING evidence:
    Do not assume the observation represents current physical reality.
    Defer autonomous execution.

The policy does not receive physical ground truth. Physical ground truth
remains reserved for independent experimental evaluation.

This comparator is deliberately strong. If it reproduces the behaviour of
DARA-DT with less reasoning complexity, the claimed additional contribution
of DARA-DT must be reconsidered.
"""

from collections.abc import Collection
from dataclasses import dataclass
from enum import Enum
from typing import Any

from dara_dt.assurance.contract_policy import (
    ContractDecision,
    RuntimeContractPolicy,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


class EvidenceContractState(str, Enum):
    """Outcome state for an evidence-aware runtime contract."""

    SATISFIED = "satisfied"
    VIOLATED = "violated"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class EvidenceContractResult:
    """Result produced by the evidence-aware contract comparator."""

    decision_id: str
    dependency: str
    authority: AuthorityState
    state: EvidenceContractState
    observed_value: Any
    required_value: Any
    evidence_status: EvidenceStatus
    reason: str

    @property
    def intervene(self) -> bool:
        """Return whether unrestricted autonomous execution is prevented."""

        return self.authority != AuthorityState.ALLOW

    @property
    def autonomous_execution_allowed(self) -> bool:
        """Return whether unrestricted autonomous execution is permitted."""

        return self.authority == AuthorityState.ALLOW


class EvidenceAwareRuntimeContractPolicy:
    """Evaluate runtime contracts while respecting evidence quality.

    AVAILABLE evidence is passed to the existing direct runtime-contract
    implementation.

    STALE, MISSING, and CONFLICTING evidence are treated as insufficient
    for unrestricted autonomous execution and therefore produce DEFER.

    Physical ground truth must never be supplied to this policy.
    """

    def __init__(self) -> None:
        """Initialise the direct runtime-contract evaluator."""

        self._contract = RuntimeContractPolicy()

    def evaluate_capacity(
        self,
        decision_id: str,
        evidence: RuntimeEvidence,
        required_demand: float,
    ) -> EvidenceContractResult:
        """Evaluate an evidence-aware vehicle-capacity contract."""

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.capacity",
        )

        uncertain = self._uncertain_result(
            decision_id=decision_id,
            evidence=evidence,
            required_value=required_demand,
        )

        if uncertain is not None:
            return uncertain

        contract = self._contract.evaluate_capacity(
            decision_id=decision_id,
            observed_capacity=evidence.observed_value,
            required_demand=required_demand,
        )

        return self._from_contract(
            decision_id=decision_id,
            evidence=evidence,
            contract_decision=contract.decision,
            dependency=contract.dependency,
            observed_value=contract.observed_value,
            required_value=contract.required_value,
            reason=contract.reason,
        )

    def evaluate_status(
        self,
        decision_id: str,
        evidence: RuntimeEvidence,
        required_status: str = "operational",
    ) -> EvidenceContractResult:
        """Evaluate an evidence-aware operational-status contract."""

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.status",
        )

        uncertain = self._uncertain_result(
            decision_id=decision_id,
            evidence=evidence,
            required_value=required_status,
        )

        if uncertain is not None:
            return uncertain

        contract = self._contract.evaluate_status(
            decision_id=decision_id,
            observed_status=evidence.observed_value,
            required_status=required_status,
        )

        return self._from_contract(
            decision_id=decision_id,
            evidence=evidence,
            contract_decision=contract.decision,
            dependency=contract.dependency,
            observed_value=contract.observed_value,
            required_value=contract.required_value,
            reason=contract.reason,
        )

    def evaluate_availability(
        self,
        decision_id: str,
        evidence: RuntimeEvidence,
        required_available: bool = True,
    ) -> EvidenceContractResult:
        """Evaluate an evidence-aware vehicle-availability contract."""

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.available",
        )

        uncertain = self._uncertain_result(
            decision_id=decision_id,
            evidence=evidence,
            required_value=required_available,
        )

        if uncertain is not None:
            return uncertain

        contract = self._contract.evaluate_availability(
            decision_id=decision_id,
            observed_available=evidence.observed_value,
            required_available=required_available,
        )

        return self._from_contract(
            decision_id=decision_id,
            evidence=evidence,
            contract_decision=contract.decision,
            dependency=contract.dependency,
            observed_value=contract.observed_value,
            required_value=contract.required_value,
            reason=contract.reason,
        )

    def evaluate_location(
        self,
        decision_id: str,
        evidence: RuntimeEvidence,
        permitted_locations: Collection[str],
    ) -> EvidenceContractResult:
        """Evaluate an evidence-aware vehicle-location contract."""

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.location",
        )

        permitted = self._validated_locations(permitted_locations)

        uncertain = self._uncertain_result(
            decision_id=decision_id,
            evidence=evidence,
            required_value=permitted,
        )

        if uncertain is not None:
            return uncertain

        contract = self._contract.evaluate_location(
            decision_id=decision_id,
            observed_location=evidence.observed_value,
            permitted_locations=permitted,
        )

        return self._from_contract(
            decision_id=decision_id,
            evidence=evidence,
            contract_decision=contract.decision,
            dependency=contract.dependency,
            observed_value=contract.observed_value,
            required_value=contract.required_value,
            reason=contract.reason,
        )

    def evaluate_location_availability(
        self,
        decision_id: str,
        location_evidence: RuntimeEvidence,
        availability_evidence: RuntimeEvidence,
        permitted_locations: Collection[str],
        required_available: bool = True,
    ) -> EvidenceContractResult:
        """Evaluate combined location and availability requirements.

        Both observations must be AVAILABLE before the direct contract is
        evaluated.

        If either observation is stale, missing, or conflicting, autonomous
        execution is deferred.
        """

        self._require_dependency(
            evidence=location_evidence,
            expected_dependency="vehicle.location",
        )

        self._require_dependency(
            evidence=availability_evidence,
            expected_dependency="vehicle.available",
        )

        if not isinstance(required_available, bool):
            raise ValueError(
                "Required availability must be boolean."
            )

        permitted = self._validated_locations(permitted_locations)

        required_value = {
            "permitted_locations": permitted,
            "required_available": required_available,
        }

        uncertain_evidence = [
            evidence
            for evidence in (
                location_evidence,
                availability_evidence,
            )
            if evidence.status != EvidenceStatus.AVAILABLE
        ]

        if uncertain_evidence:
            statuses = tuple(
                evidence.status.value
                for evidence in uncertain_evidence
            )

            return EvidenceContractResult(
                decision_id=decision_id,
                dependency="vehicle.location_availability",
                authority=AuthorityState.DEFER,
                state=EvidenceContractState.UNCERTAIN,
                observed_value={
                    "location": location_evidence.observed_value,
                    "available": availability_evidence.observed_value,
                },
                required_value=required_value,
                evidence_status=self._combined_status(
                    location_evidence=location_evidence,
                    availability_evidence=availability_evidence,
                ),
                reason=(
                    "Combined dispatch contract cannot be evaluated "
                    "with sufficient confidence because one or more "
                    "runtime observations are uncertain: "
                    f"{', '.join(statuses)}."
                ),
            )

        contract = self._contract.evaluate_location_availability(
            decision_id=decision_id,
            observed_location=location_evidence.observed_value,
            observed_available=availability_evidence.observed_value,
            permitted_locations=permitted,
            required_available=required_available,
        )

        return self._from_contract(
            decision_id=decision_id,
            evidence=location_evidence,
            contract_decision=contract.decision,
            dependency=contract.dependency,
            observed_value=contract.observed_value,
            required_value=contract.required_value,
            reason=contract.reason,
        )

    def _uncertain_result(
        self,
        decision_id: str,
        evidence: RuntimeEvidence,
        required_value: Any,
    ) -> EvidenceContractResult | None:
        """Return a conservative result when evidence is uncertain.

        AVAILABLE evidence returns None so that the caller can evaluate
        the direct execution contract.
        """

        if evidence.status == EvidenceStatus.AVAILABLE:
            return None

        return EvidenceContractResult(
            decision_id=decision_id,
            dependency=evidence.dependency,
            authority=AuthorityState.DEFER,
            state=EvidenceContractState.UNCERTAIN,
            observed_value=evidence.observed_value,
            required_value=required_value,
            evidence_status=evidence.status,
            reason=(
                "Direct execution contract deferred because runtime "
                f"evidence is {evidence.status.value}."
            ),
        )

    @staticmethod
    def _from_contract(
        decision_id: str,
        evidence: RuntimeEvidence,
        contract_decision: ContractDecision,
        dependency: str,
        observed_value: Any,
        required_value: Any,
        reason: str,
    ) -> EvidenceContractResult:
        """Convert a direct contract result into an evidence-aware result."""

        if contract_decision == ContractDecision.ALLOW:
            return EvidenceContractResult(
                decision_id=decision_id,
                dependency=dependency,
                authority=AuthorityState.ALLOW,
                state=EvidenceContractState.SATISFIED,
                observed_value=observed_value,
                required_value=required_value,
                evidence_status=evidence.status,
                reason=reason,
            )

        return EvidenceContractResult(
            decision_id=decision_id,
            dependency=dependency,
            authority=AuthorityState.RESTRICT,
            state=EvidenceContractState.VIOLATED,
            observed_value=observed_value,
            required_value=required_value,
            evidence_status=evidence.status,
            reason=reason,
        )

    @staticmethod
    def _require_dependency(
        evidence: RuntimeEvidence,
        expected_dependency: str,
    ) -> None:
        """Ensure evidence represents the dependency being evaluated."""

        if evidence.dependency != expected_dependency:
            raise ValueError(
                "Runtime evidence dependency does not match the "
                "contract requirement: "
                f"expected {expected_dependency!r}, "
                f"received {evidence.dependency!r}."
            )

    @staticmethod
    def _validated_locations(
        permitted_locations: Collection[str],
    ) -> tuple[str, ...]:
        """Validate and normalise permitted dispatch locations."""

        permitted = tuple(permitted_locations)

        if not permitted:
            raise ValueError(
                "At least one permitted dispatch location is required."
            )

        if any(
            not isinstance(location, str)
            for location in permitted
        ):
            raise ValueError(
                "Permitted dispatch locations must be strings."
            )

        return tuple(sorted(set(permitted)))

    @staticmethod
    def _combined_status(
        location_evidence: RuntimeEvidence,
        availability_evidence: RuntimeEvidence,
    ) -> EvidenceStatus:
        """Return the strongest uncertainty state across two observations."""

        statuses = {
            location_evidence.status,
            availability_evidence.status,
        }

        if EvidenceStatus.MISSING in statuses:
            return EvidenceStatus.MISSING

        if EvidenceStatus.CONFLICTING in statuses:
            return EvidenceStatus.CONFLICTING

        if EvidenceStatus.STALE in statuses:
            return EvidenceStatus.STALE

        return EvidenceStatus.AVAILABLE
