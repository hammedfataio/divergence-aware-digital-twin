"""Frozen experimental conditions for EXP-009.

EXP-009 investigates whether decision-conditioned runtime assurance can
distinguish decision-relevant from decision-irrelevant evidence uncertainty.

The experimental design is frozen before execution:

    3 dependency families
    × 3 imperfect evidence states
    × 2 relevance states
    × 2 physical-validity states
    = 36 imperfect-evidence conditions

plus:

    3 dependency families
    × 2 reliable controls
    = 6 reliable controls

Total = 42 conditions.

Physical ground truth represented by ``physically_valid`` is evaluator-only
information and must never be exposed to runtime assurance policies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from dara_dt.evidence.model import EvidenceStatus


class DependencyFamily(str, Enum):
    """Decision-dependency families evaluated by EXP-009."""

    CAPACITY = "capacity"
    STATUS = "status"
    LOCATION_AVAILABILITY = "location_availability"


class EvidenceRelevance(str, Enum):
    """Whether uncertain evidence affects the pending decision."""

    RELEVANT = "relevant"
    IRRELEVANT = "irrelevant"


@dataclass(frozen=True)
class DecisionRelevanceCondition:
    """One frozen EXP-009 experimental condition.

    ``physically_valid`` is ground-truth information used only by the
    independent evaluator.

    ``evidence_relevance`` identifies whether the uncertain evidence belongs
    to a dependency required by the pending decision.

    Reliable controls are always labelled RELEVANT because relevance is not
    the experimental variable for those control conditions.
    """

    condition_id: str
    dependency_family: DependencyFamily
    evidence_status: EvidenceStatus
    evidence_relevance: EvidenceRelevance
    physically_valid: bool

    @property
    def intervention_required(self) -> bool:
        """Return evaluator-only intervention requirement."""

        return not self.physically_valid

    @property
    def is_reliable_control(self) -> bool:
        """Return whether this condition is a reliable control."""

        return self.evidence_status == EvidenceStatus.AVAILABLE

    @property
    def is_imperfect_evidence(self) -> bool:
        """Return whether runtime evidence quality is imperfect."""

        return self.evidence_status in {
            EvidenceStatus.STALE,
            EvidenceStatus.MISSING,
            EvidenceStatus.CONFLICTING,
        }


def _reliable_controls(
    prefix: str,
    dependency_family: DependencyFamily,
) -> list[DecisionRelevanceCondition]:
    """Create the two reliable controls for one dependency family."""

    return [
        DecisionRelevanceCondition(
            condition_id=f"{prefix}-R-V",
            dependency_family=dependency_family,
            evidence_status=EvidenceStatus.AVAILABLE,
            evidence_relevance=EvidenceRelevance.RELEVANT,
            physically_valid=True,
        ),
        DecisionRelevanceCondition(
            condition_id=f"{prefix}-R-I",
            dependency_family=dependency_family,
            evidence_status=EvidenceStatus.AVAILABLE,
            evidence_relevance=EvidenceRelevance.RELEVANT,
            physically_valid=False,
        ),
    ]


def _imperfect_conditions(
    prefix: str,
    dependency_family: DependencyFamily,
    evidence_code: str,
    evidence_status: EvidenceStatus,
) -> list[DecisionRelevanceCondition]:
    """Create the four relevance/validity combinations for one evidence state."""

    return [
        DecisionRelevanceCondition(
            condition_id=f"{prefix}-{evidence_code}-REL-V",
            dependency_family=dependency_family,
            evidence_status=evidence_status,
            evidence_relevance=EvidenceRelevance.RELEVANT,
            physically_valid=True,
        ),
        DecisionRelevanceCondition(
            condition_id=f"{prefix}-{evidence_code}-REL-I",
            dependency_family=dependency_family,
            evidence_status=evidence_status,
            evidence_relevance=EvidenceRelevance.RELEVANT,
            physically_valid=False,
        ),
        DecisionRelevanceCondition(
            condition_id=f"{prefix}-{evidence_code}-IRR-V",
            dependency_family=dependency_family,
            evidence_status=evidence_status,
            evidence_relevance=EvidenceRelevance.IRRELEVANT,
            physically_valid=True,
        ),
        DecisionRelevanceCondition(
            condition_id=f"{prefix}-{evidence_code}-IRR-I",
            dependency_family=dependency_family,
            evidence_status=evidence_status,
            evidence_relevance=EvidenceRelevance.IRRELEVANT,
            physically_valid=False,
        ),
    ]


def _dependency_conditions(
    prefix: str,
    dependency_family: DependencyFamily,
) -> list[DecisionRelevanceCondition]:
    """Create all 14 frozen conditions for one dependency family."""

    conditions = _reliable_controls(
        prefix=prefix,
        dependency_family=dependency_family,
    )

    conditions.extend(
        _imperfect_conditions(
            prefix=prefix,
            dependency_family=dependency_family,
            evidence_code="S",
            evidence_status=EvidenceStatus.STALE,
        )
    )

    conditions.extend(
        _imperfect_conditions(
            prefix=prefix,
            dependency_family=dependency_family,
            evidence_code="M",
            evidence_status=EvidenceStatus.MISSING,
        )
    )

    conditions.extend(
        _imperfect_conditions(
            prefix=prefix,
            dependency_family=dependency_family,
            evidence_code="C",
            evidence_status=EvidenceStatus.CONFLICTING,
        )
    )

    return conditions


def build_exp009_conditions() -> tuple[DecisionRelevanceCondition, ...]:
    """Return the complete frozen 42-condition EXP-009 matrix."""

    conditions: list[DecisionRelevanceCondition] = []

    conditions.extend(
        _dependency_conditions(
            prefix="CAP",
            dependency_family=DependencyFamily.CAPACITY,
        )
    )

    conditions.extend(
        _dependency_conditions(
            prefix="STATUS",
            dependency_family=DependencyFamily.STATUS,
        )
    )

    conditions.extend(
        _dependency_conditions(
            prefix="LOC",
            dependency_family=DependencyFamily.LOCATION_AVAILABILITY,
        )
    )

    return tuple(conditions)


EXP009_CONDITIONS = build_exp009_conditions()
