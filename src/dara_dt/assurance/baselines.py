"""Baseline runtime assurance policies for DARA-DT experiments."""

from dara_dt.assurance.model import (
    AssuranceDecision,
    AuthorityState,
)
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence


class NoAssurancePolicy:
    """Baseline B0: never intervene in an AI-generated decision."""

    def evaluate(
        self,
        decision: Decision,
        divergences: list[Divergence],
    ) -> AssuranceDecision:
        """Always permit autonomous execution."""
        return AssuranceDecision(
            decision_id=decision.decision_id,
            authority=AuthorityState.ALLOW,
            reason="Baseline B0 applies no runtime assurance.",
            relevant_divergence_count=0,
        )


class AnyDivergencePolicy:
    """Baseline B1: intervene whenever any divergence is detected."""

    def evaluate(
        self,
        decision: Decision,
        divergences: list[Divergence],
    ) -> AssuranceDecision:
        """Defer whenever at least one divergence exists."""

        if not divergences:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.ALLOW,
                reason="No physical-digital divergence detected.",
                relevant_divergence_count=0,
            )

        return AssuranceDecision(
            decision_id=decision.decision_id,
            authority=AuthorityState.DEFER,
            reason="Physical-digital divergence detected.",
            relevant_divergence_count=len(divergences),
        )
