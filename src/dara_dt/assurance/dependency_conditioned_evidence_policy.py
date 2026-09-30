"""Decision-dependency-conditioned evidence uncertainty for EXP-009.

This policy evaluates runtime evidence uncertainty relative to the exact
state dependencies required by a pending AI-generated decision.

It is intentionally more selective than:

1. global evidence uncertainty, which reacts to uncertainty anywhere; and
2. entity-filtered uncertainty, which reacts to uncertainty anywhere on
   the selected entity.

The policy does not use physical ground truth. It only reasons over the
runtime evidence supplied to it and the dependencies declared for the
pending decision.
"""

from collections.abc import Iterable, Set

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


class DependencyConditionedEvidencePolicy:
    """Condition uncertainty handling on exact decision dependencies."""

    _UNCERTAIN_STATUSES = {
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    }

    def evaluate(
        self,
        evidence: Iterable[RuntimeEvidence],
        required_dependencies: Set[str],
        decision_id: str = "exp009",
    ) -> AssuranceDecision:
        """Evaluate uncertainty affecting the pending decision.

        Parameters
        ----------
        evidence:
            Runtime evidence visible to the assurance mechanism.
        required_dependencies:
            Exact state dependencies required by the pending decision,
            for example ``{"vehicle_2.capacity"}``.
        decision_id:
            Identifier of the pending decision.

        Returns
        -------
        AssuranceDecision
            DEFER when uncertain evidence affects at least one required
            dependency. Otherwise ALLOW.

        Notes
        -----
        Dependency matching is exact.

        Therefore uncertainty in ``vehicle_2.status`` does not affect a
        decision requiring only ``vehicle_2.capacity``.

        Likewise, ``vehicle_20.capacity`` does not match
        ``vehicle_2.capacity``.

        Physical ground truth is deliberately unavailable to this policy.
        """

        if not required_dependencies:
            raise ValueError(
                "required_dependencies must contain at least one dependency"
            )

        required = set(required_dependencies)

        uncertain_required_evidence = [
            item
            for item in evidence
            if item.dependency in required
            and item.status in self._UNCERTAIN_STATUSES
        ]

        if uncertain_required_evidence:
            affected_dependencies = sorted(
                {
                    item.dependency
                    for item in uncertain_required_evidence
                }
            )

            statuses = sorted(
                {
                    item.status.value
                    for item in uncertain_required_evidence
                }
            )

            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Uncertain runtime evidence affects required decision "
                    "dependencies: "
                    f"{', '.join(affected_dependencies)} "
                    f"(status: {', '.join(statuses)})."
                ),
                relevant_divergence_count=0,
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "No uncertain runtime evidence affects the required "
                "decision dependencies."
            ),
            relevant_divergence_count=0,
        )
