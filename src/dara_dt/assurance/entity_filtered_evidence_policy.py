"""Entity-filtered evidence-uncertainty baseline for EXP-009.

This policy provides an intermediate comparator between global evidence
uncertainty and decision-dependency-conditioned assurance.

The policy considers evidence uncertainty only when the evidence belongs
to the entity selected by the pending decision. It deliberately does not
reason about which dependency of that entity is relevant to the decision.

This makes it suitable for testing whether any advantage of DARA-DT can
be explained by simple entity filtering alone.
"""

from collections.abc import Iterable

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


class EntityFilteredEvidencePolicy:
    """React to uncertain evidence associated with the selected entity."""

    _UNCERTAIN_STATUSES = {
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    }

    def evaluate(
        self,
        evidence: Iterable[RuntimeEvidence],
        selected_entity: str,
        decision_id: str = "exp009",
    ) -> AssuranceDecision:
        """Evaluate evidence uncertainty for the selected entity.

        Parameters
        ----------
        evidence:
            Runtime evidence visible to the assurance mechanism.
        selected_entity:
            Entity used by the pending decision, for example ``vehicle_2``.
        decision_id:
            Identifier of the pending decision.

        Returns
        -------
        AssuranceDecision
            DEFER when uncertain evidence belongs to the selected entity.
            Otherwise ALLOW.

        Notes
        -----
        Filtering is intentionally performed at entity level only.

        For example, if the selected entity is ``vehicle_2``, uncertainty
        in ``vehicle_2.status`` causes DEFER even when the pending decision
        only depends on ``vehicle_2.capacity``.

        Evidence concerning ``vehicle_8`` is ignored for a decision using
        ``vehicle_2``.

        Physical ground truth is not used.
        """

        if not selected_entity:
            raise ValueError("selected_entity must be a non-empty string")

        selected_evidence = [
            item
            for item in evidence
            if self._entity_from_dependency(item.dependency) == selected_entity
        ]

        uncertain = [
            item
            for item in selected_evidence
            if item.status in self._UNCERTAIN_STATUSES
        ]

        if uncertain:
            statuses = sorted({item.status.value for item in uncertain})

            return AssuranceDecision(
                decision_id=decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Uncertain runtime evidence exists for selected entity "
                    f"{selected_entity}: {', '.join(statuses)}."
                ),
                relevant_divergence_count=0,
            )

        return AssuranceDecision(
            decision_id=decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "No uncertain runtime evidence observed for selected entity "
                f"{selected_entity}."
            ),
            relevant_divergence_count=0,
        )

    @staticmethod
    def _entity_from_dependency(dependency: str) -> str:
        """Extract the exact entity component from a dependency identifier.

        Examples
        --------
        ``vehicle_2.capacity`` -> ``vehicle_2``

        ``vehicle_20.status`` -> ``vehicle_20``

        Exact extraction prevents accidental prefix matching such as
        ``vehicle_2`` matching ``vehicle_20``.
        """

        return dependency.split(".", maxsplit=1)[0]
