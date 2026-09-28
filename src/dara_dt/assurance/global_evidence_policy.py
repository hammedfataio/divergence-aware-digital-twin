"""Global evidence-quality assurance policy for EXP-009.

This policy intentionally does not perform entity filtering or
decision-dependency reasoning.

It represents a system-level conservative baseline:

- if all supplied runtime evidence is available, autonomous execution is
  allowed;
- if any supplied runtime evidence is stale, missing, or conflicting,
  autonomous execution is deferred.

The policy never receives physical ground truth.
"""

from __future__ import annotations

from collections.abc import Iterable

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


class GlobalEvidenceUncertaintyPolicy:
    """React conservatively to uncertainty anywhere in runtime evidence."""

    _UNCERTAIN_STATUSES = {
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    }

    def evaluate(
        self,
        evidence: Iterable[RuntimeEvidence],
    ) -> AssuranceDecision:
        """Evaluate system-wide runtime evidence quality.

        Any stale, missing, or conflicting observation causes DEFER,
        regardless of whether that observation is relevant to the pending
        decision.

        This behaviour is deliberate: EXP-009 uses this policy as the global
        uncertainty baseline against which entity filtering and
        decision-conditioned reasoning are compared.
        """

        evidence_items = tuple(evidence)

        uncertain_items = [
            item
            for item in evidence_items
            if item.status in self._UNCERTAIN_STATUSES
        ]

        if uncertain_items:
            return AssuranceDecision(
                state=AuthorityState.DEFER,
                reason=(
                    "System-wide runtime evidence contains "
                    f"{len(uncertain_items)} uncertain observation(s)."
                ),
            )

        return AssuranceDecision(
            state=AuthorityState.ALLOW,
            reason="No uncertain runtime evidence detected.",
        )
