"""Global evidence-uncertainty assurance policy for EXP-009.

This module implements the system-wide uncertainty baseline used in
Experiment 009.

The policy deliberately ignores decision relevance. If any runtime evidence
item is stale, missing, or conflicting, autonomous authority is deferred.

This provides the conservative global baseline against which entity-filtered
and decision-dependency-conditioned assurance mechanisms are compared.

Physical ground truth is never used by this policy.
"""

from __future__ import annotations

from collections.abc import Iterable

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


class GlobalEvidenceUncertaintyPolicy:
    """Apply system-wide evidence-quality assurance."""

    _UNCERTAIN_STATUSES = {
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    }

    def evaluate(
        self,
        evidence: Iterable[RuntimeEvidence],
        decision_id: str = "exp009",
    ) -> AssuranceDecision:
        """Evaluate system-wide runtime evidence quality.

        Any stale, missing, or conflicting observation causes DEFER,
        regardless of whether that observation is relevant to the pending
        decision.

        This behaviour is intentional for EXP-009 because this policy is the
        global uncertainty baseline.

        Physical ground truth is never used.
        """

        evidence_items = tuple(evidence)

        uncertain_items = [
            item
            for item in evidence_items
            if item.status in self._UNCERTAIN_STATUSES
        ]

        if uncertain_items:
            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "System-wide runtime evidence contains "
                    f"{len(uncertain_items)} uncertain observation(s)."
                ),
                relevant_divergence_count=0,
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason="No uncertain runtime evidence detected.",
            relevant_divergence_count=0,
        )
