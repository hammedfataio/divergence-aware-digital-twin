"""Decision-impact-aware runtime assurance policy for DARA-DT.

This policy regulates autonomous authority using estimated decision
impact rather than physical-digital divergence magnitude alone.

Experimental ground-truth validity is intentionally excluded from this
policy. The policy operates only on runtime decision-impact evidence.
"""

from dara_dt.assurance.model import (
    AssuranceDecision,
    AuthorityState,
)
from dara_dt.decision.model import Decision
from dara_dt.impact.model import DecisionImpact, ImpactState


class DecisionImpactPolicy:
    """Apply decision-impact-aware runtime assurance."""

    def evaluate(
        self,
        decision: Decision,
        impact: DecisionImpact,
    ) -> AssuranceDecision:
        """Determine permitted authority from estimated decision impact."""

        if impact.decision_id != decision.decision_id:
            raise ValueError(
                "Decision impact does not belong to the supplied decision."
            )

        if impact.impact_state == ImpactState.NO_IMPACT:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.ALLOW,
                reason=(
                    "Runtime evidence indicates no material impact "
                    "on the proposed decision."
                ),
                relevant_divergence_count=0,
            )

        if impact.impact_state == ImpactState.MARGIN_REDUCED:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.ALLOW,
                reason=(
                    "Decision margin is reduced, but runtime evidence "
                    "indicates that the proposed decision remains feasible."
                ),
                relevant_divergence_count=1,
            )

        if impact.impact_state == ImpactState.BOUNDARY:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.RESTRICT,
                reason=(
                    "Runtime evidence places the proposed decision "
                    "at its estimated validity boundary."
                ),
                relevant_divergence_count=1,
            )

        if impact.impact_state == ImpactState.INVALIDATING:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Runtime evidence indicates that divergence "
                    "materially invalidates the proposed decision."
                ),
                relevant_divergence_count=1,
            )

        if impact.impact_state == ImpactState.UNCERTAIN:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Available runtime evidence is insufficient to "
                    "determine whether autonomous execution is safe."
                ),
                relevant_divergence_count=1,
            )

        raise ValueError(
            f"Unsupported decision-impact state: {impact.impact_state!r}"
        )
