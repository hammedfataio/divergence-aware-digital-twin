"""Runtime assurance policy for DARA-DT."""

from dara_dt.assurance.model import (
    AssuranceDecision,
    AuthorityState,
)
from dara_dt.decision.model import Decision
from dara_dt.divergence.relevance import RelevanceResult


class DivergenceAwarePolicy:
    """Apply a basic divergence-aware runtime assurance policy."""

    def evaluate(
        self,
        decision: Decision,
        relevance: RelevanceResult,
    ) -> AssuranceDecision:
        """Determine the permitted authority for a proposed decision."""

        relevant_count = len(relevance.relevant)

        if relevant_count == 0:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.ALLOW,
                reason="No decision-relevant divergence detected.",
                relevant_divergence_count=0,
            )

        return AssuranceDecision(
            decision_id=decision.decision_id,
            authority=AuthorityState.DEFER,
            reason=(
                "Decision-relevant physical-digital divergence "
                "detected."
            ),
            relevant_divergence_count=relevant_count,
        )
