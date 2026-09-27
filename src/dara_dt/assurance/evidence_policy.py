"""Evidence-aware runtime assurance policy for EXP-006.

This policy extends decision-impact-aware assurance by explicitly
considering the quality of runtime evidence.

The policy does not have access to physical ground truth. It reasons
only from the evidence available at runtime and the decision boundary.
"""

from collections.abc import Sequence
from numbers import Real

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


class EvidenceAwareDecisionPolicy:
    """Regulate autonomous authority using runtime evidence quality."""

    def evaluate(
        self,
        *,
        decision: Decision,
        evidence: Sequence[RuntimeEvidence],
        demand: Real,
        current_time: float,
    ) -> AssuranceDecision:
        """Evaluate whether autonomous execution should be permitted."""

        if not isinstance(demand, Real):
            raise TypeError("Demand must be numeric.")

        if demand < 0:
            raise ValueError("Demand must not be negative.")

        if not evidence:
            return self._defer(
                decision,
                "No runtime evidence is available.",
            )

        relevant_evidence = [
            item
            for item in evidence
            if item.dependency == "vehicle.capacity"
        ]

        if not relevant_evidence:
            return self._defer(
                decision,
                "No capacity evidence is available for the decision.",
            )

        if any(
            item.status == EvidenceStatus.MISSING
            for item in relevant_evidence
        ):
            return self._defer(
                decision,
                "Required capacity evidence is missing.",
            )

        if any(
            item.status == EvidenceStatus.STALE
            for item in relevant_evidence
        ):
            return self._defer(
                decision,
                "Capacity evidence is stale.",
            )

        if any(
            item.status == EvidenceStatus.CONFLICTING
            for item in relevant_evidence
        ):
            return self._defer(
                decision,
                "Capacity evidence is conflicting.",
            )

        observed_values = [
            item.observed_value
            for item in relevant_evidence
            if item.is_available
        ]

        if not observed_values:
            return self._defer(
                decision,
                "No usable capacity observation is available.",
            )

        if any(
            not isinstance(value, Real)
            for value in observed_values
        ):
            return self._defer(
                decision,
                "Capacity evidence is not numeric.",
            )

        minimum_observed_capacity = min(observed_values)

        if minimum_observed_capacity < demand:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Runtime evidence indicates insufficient "
                    "physical capacity."
                ),
                relevant_divergence_count=1,
            )

        if minimum_observed_capacity == demand:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.RESTRICT,
                reason=(
                    "Runtime evidence places the decision at the "
                    "capacity boundary."
                ),
                relevant_divergence_count=1,
            )

        return AssuranceDecision(
            decision_id=decision.decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "Runtime evidence indicates capacity remains above "
                "the decision requirement."
            ),
            relevant_divergence_count=0,
        )

    @staticmethod
    def _defer(
        decision: Decision,
        reason: str,
    ) -> AssuranceDecision:
        """Return a conservative decision under evidence uncertainty."""

        return AssuranceDecision(
            decision_id=decision.decision_id,
            authority=AuthorityState.DEFER,
            reason=reason,
            relevant_divergence_count=1,
        )
