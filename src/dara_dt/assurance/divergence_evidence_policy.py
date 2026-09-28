"""Decision-conditioned evidence-aware assurance for EXP-008.

This module extends DARA-DT runtime assurance across the dependency
families evaluated in EXP-008:

- vehicle capacity;
- vehicle operational status;
- vehicle location and availability.

The policy deliberately separates runtime evidence from physical ground
truth. It may use:

- Digital Twin state;
- decision requirements;
- runtime evidence and its quality metadata.

It must never use the experimental physical ground-truth state.

EXP-008 uses this policy to test whether decision-conditioned
physical-digital divergence provides useful runtime-assurance
information beyond simpler runtime-contract mechanisms when evidence is
reliable, stale, missing, or conflicting.
"""

from collections.abc import Collection
from numbers import Real
from typing import Any

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


class DivergenceEvidencePolicy:
    """Evidence-aware DARA-DT policy for cross-dependency assurance."""

    def evaluate_capacity(
        self,
        *,
        decision_id: str,
        evidence: RuntimeEvidence,
        twin_capacity: float,
        required_demand: float,
    ) -> AssuranceDecision:
        """Evaluate capacity using decision-conditioned divergence.

        Reliable evidence is compared with both the Digital Twin state
        and the decision-specific demand requirement.

        Uncertain evidence produces DEFER rather than treating the
        observation as physical ground truth.
        """

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.capacity",
        )

        uncertain = self._uncertain_decision(
            decision_id=decision_id,
            evidence=(evidence,),
            dependency_description="vehicle capacity",
        )

        if uncertain is not None:
            return uncertain

        if (
            isinstance(twin_capacity, bool)
            or not isinstance(twin_capacity, Real)
        ):
            raise ValueError("Digital Twin capacity must be numeric.")

        if (
            isinstance(required_demand, bool)
            or not isinstance(required_demand, Real)
        ):
            raise ValueError("Required demand must be numeric.")

        observed_capacity = evidence.observed_value

        if (
            isinstance(observed_capacity, bool)
            or not isinstance(observed_capacity, Real)
        ):
            return self._defer(
                decision_id=decision_id,
                reason="Capacity evidence is not numeric.",
            )

        observed_capacity = float(observed_capacity)
        twin_capacity = float(twin_capacity)
        required_demand = float(required_demand)

        divergence_exists = observed_capacity != twin_capacity
        observed_margin = observed_capacity - required_demand

        if observed_margin < 0:
            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Decision-conditioned runtime evidence indicates "
                    "that observed vehicle capacity is below the "
                    "decision requirement."
                ),
                relevant_divergence_count=int(divergence_exists),
            )

        if observed_margin == 0:
            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.RESTRICT,
                reason=(
                    "Decision-conditioned runtime evidence places "
                    "vehicle capacity exactly at the decision boundary."
                ),
                relevant_divergence_count=int(divergence_exists),
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "Observed vehicle capacity remains above the "
                "decision-specific demand requirement."
            ),
            relevant_divergence_count=int(divergence_exists),
        )

    def evaluate_status(
        self,
        *,
        decision_id: str,
        evidence: RuntimeEvidence,
        twin_status: str,
        required_status: str = "operational",
    ) -> AssuranceDecision:
        """Evaluate operational status using runtime evidence."""

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.status",
        )

        uncertain = self._uncertain_decision(
            decision_id=decision_id,
            evidence=(evidence,),
            dependency_description="vehicle operational status",
        )

        if uncertain is not None:
            return uncertain

        if not isinstance(twin_status, str) or not twin_status:
            raise ValueError(
                "Digital Twin status must be a non-empty string."
            )

        if not isinstance(required_status, str) or not required_status:
            raise ValueError(
                "Required status must be a non-empty string."
            )

        observed_status = evidence.observed_value

        if not isinstance(observed_status, str):
            return self._defer(
                decision_id=decision_id,
                reason="Operational-status evidence is not a string.",
            )

        divergence_exists = observed_status != twin_status

        if observed_status != required_status:
            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Decision-conditioned runtime evidence indicates "
                    "that the vehicle does not satisfy the required "
                    f"operational state '{required_status}'."
                ),
                relevant_divergence_count=int(divergence_exists),
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "Observed operational status satisfies the "
                "decision-specific requirement."
            ),
            relevant_divergence_count=int(divergence_exists),
        )

    def evaluate_availability(
        self,
        *,
        decision_id: str,
        evidence: RuntimeEvidence,
        twin_available: bool,
        required_available: bool = True,
    ) -> AssuranceDecision:
        """Evaluate vehicle availability using runtime evidence."""

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.available",
        )

        uncertain = self._uncertain_decision(
            decision_id=decision_id,
            evidence=(evidence,),
            dependency_description="vehicle availability",
        )

        if uncertain is not None:
            return uncertain

        if not isinstance(twin_available, bool):
            raise ValueError(
                "Digital Twin availability must be boolean."
            )

        if not isinstance(required_available, bool):
            raise ValueError(
                "Required availability must be boolean."
            )

        observed_available = evidence.observed_value

        if not isinstance(observed_available, bool):
            return self._defer(
                decision_id=decision_id,
                reason="Availability evidence is not boolean.",
            )

        divergence_exists = observed_available != twin_available

        if observed_available != required_available:
            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Decision-conditioned runtime evidence indicates "
                    "that vehicle availability does not satisfy the "
                    "decision requirement."
                ),
                relevant_divergence_count=int(divergence_exists),
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "Observed vehicle availability satisfies the "
                "decision-specific requirement."
            ),
            relevant_divergence_count=int(divergence_exists),
        )

    def evaluate_location(
        self,
        *,
        decision_id: str,
        evidence: RuntimeEvidence,
        twin_location: str,
        permitted_locations: Collection[str],
    ) -> AssuranceDecision:
        """Evaluate location compatibility using runtime evidence."""

        self._require_dependency(
            evidence=evidence,
            expected_dependency="vehicle.location",
        )

        permitted = self._validated_locations(permitted_locations)

        uncertain = self._uncertain_decision(
            decision_id=decision_id,
            evidence=(evidence,),
            dependency_description="vehicle location",
        )

        if uncertain is not None:
            return uncertain

        if not isinstance(twin_location, str) or not twin_location:
            raise ValueError(
                "Digital Twin location must be a non-empty string."
            )

        observed_location = evidence.observed_value

        if not isinstance(observed_location, str):
            return self._defer(
                decision_id=decision_id,
                reason="Location evidence is not a string.",
            )

        divergence_exists = observed_location != twin_location

        if observed_location not in permitted:
            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Decision-conditioned runtime evidence places the "
                    "vehicle outside the permitted decision locations."
                ),
                relevant_divergence_count=int(divergence_exists),
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "Observed vehicle location remains compatible with "
                "the decision-specific location requirement."
            ),
            relevant_divergence_count=int(divergence_exists),
        )

    def evaluate_location_availability(
        self,
        *,
        decision_id: str,
        location_evidence: RuntimeEvidence,
        availability_evidence: RuntimeEvidence,
        twin_location: str,
        twin_available: bool,
        permitted_locations: Collection[str],
        required_available: bool = True,
    ) -> AssuranceDecision:
        """Evaluate combined location and availability dependencies."""

        self._require_dependency(
            evidence=location_evidence,
            expected_dependency="vehicle.location",
        )

        self._require_dependency(
            evidence=availability_evidence,
            expected_dependency="vehicle.available",
        )

        permitted = self._validated_locations(permitted_locations)

        if not isinstance(twin_location, str) or not twin_location:
            raise ValueError(
                "Digital Twin location must be a non-empty string."
            )

        if not isinstance(twin_available, bool):
            raise ValueError(
                "Digital Twin availability must be boolean."
            )

        if not isinstance(required_available, bool):
            raise ValueError(
                "Required availability must be boolean."
            )

        uncertain = self._uncertain_decision(
            decision_id=decision_id,
            evidence=(
                location_evidence,
                availability_evidence,
            ),
            dependency_description=(
                "vehicle location and availability"
            ),
        )

        if uncertain is not None:
            return uncertain

        observed_location = location_evidence.observed_value
        observed_available = availability_evidence.observed_value

        if not isinstance(observed_location, str):
            return self._defer(
                decision_id=decision_id,
                reason="Location evidence is not a string.",
            )

        if not isinstance(observed_available, bool):
            return self._defer(
                decision_id=decision_id,
                reason="Availability evidence is not boolean.",
            )

        location_divergence = observed_location != twin_location
        availability_divergence = (
            observed_available != twin_available
        )

        relevant_divergence_count = sum(
            (
                int(location_divergence),
                int(availability_divergence),
            )
        )

        location_valid = observed_location in permitted
        availability_valid = (
            observed_available == required_available
        )

        if not location_valid or not availability_valid:
            failed_requirements: list[str] = []

            if not location_valid:
                failed_requirements.append("location")

            if not availability_valid:
                failed_requirements.append("availability")

            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Decision-conditioned runtime evidence indicates "
                    "that the dispatch decision violates: "
                    f"{', '.join(failed_requirements)}."
                ),
                relevant_divergence_count=relevant_divergence_count,
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "Observed location and availability satisfy the "
                "decision-specific dispatch requirements."
            ),
            relevant_divergence_count=relevant_divergence_count,
        )

    def _uncertain_decision(
        self,
        *,
        decision_id: str,
        evidence: tuple[RuntimeEvidence, ...],
        dependency_description: str,
    ) -> AssuranceDecision | None:
        """Return DEFER when required runtime evidence is uncertain."""

        if not evidence:
            return self._defer(
                decision_id=decision_id,
                reason=(
                    "No runtime evidence is available for the "
                    f"{dependency_description} dependency."
                ),
            )

        statuses = tuple(item.status for item in evidence)

        if EvidenceStatus.MISSING in statuses:
            return self._defer(
                decision_id=decision_id,
                reason=(
                    "Required runtime evidence is missing for the "
                    f"{dependency_description} dependency."
                ),
            )

        if EvidenceStatus.CONFLICTING in statuses:
            return self._defer(
                decision_id=decision_id,
                reason=(
                    "Runtime evidence is conflicting for the "
                    f"{dependency_description} dependency."
                ),
            )

        if EvidenceStatus.STALE in statuses:
            return self._defer(
                decision_id=decision_id,
                reason=(
                    "Runtime evidence is stale for the "
                    f"{dependency_description} dependency."
                ),
            )

        if any(
            item.status != EvidenceStatus.AVAILABLE
            for item in evidence
        ):
            return self._defer(
                decision_id=decision_id,
                reason=(
                    "Runtime evidence quality is insufficient for "
                    f"the {dependency_description} dependency."
                ),
            )

        return None

    @staticmethod
    def _require_dependency(
        *,
        evidence: RuntimeEvidence,
        expected_dependency: str,
    ) -> None:
        """Require evidence to describe the expected dependency."""

        if evidence.dependency != expected_dependency:
            raise ValueError(
                "Evidence dependency mismatch: expected "
                f"'{expected_dependency}', received "
                f"'{evidence.dependency}'."
            )

    @staticmethod
    def _validated_locations(
        permitted_locations: Collection[str],
    ) -> tuple[str, ...]:
        """Validate and normalise permitted locations."""

        permitted = tuple(permitted_locations)

        if not permitted:
            raise ValueError(
                "At least one permitted location is required."
            )

        if any(
            not isinstance(location, str) or not location
            for location in permitted
        ):
            raise ValueError(
                "Permitted locations must be non-empty strings."
            )

        return permitted

    @staticmethod
    def _defer(
        *,
        decision_id: str,
        reason: str,
    ) -> AssuranceDecision:
        """Return conservative authority under runtime uncertainty."""

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.DEFER,
            reason=reason,
            relevant_divergence_count=1,
        )
