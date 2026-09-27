"""Controlled evidence-quality conditions for EXP-006.

The conditions in this module separate physical ground truth from the
runtime evidence available to the assurance mechanism.

They are deterministic by design. This allows changes in assurance
behaviour to be attributed to evidence quality rather than randomness.
"""

from dataclasses import dataclass
from enum import Enum


class EvidenceConditionType(str, Enum):
    """Controlled forms of runtime-evidence quality."""

    ACCURATE = "accurate"
    NOISY = "noisy"
    STALE = "stale"
    MISSING = "missing"
    CONFLICTING = "conflicting"


@dataclass(frozen=True)
class EvidenceCondition:
    """One controlled EXP-006 evidence condition."""

    condition_id: str
    description: str
    twin_capacity: float
    physical_capacity: float
    demand: float
    evidence_type: EvidenceConditionType
    observed_capacity: float | None
    secondary_observed_capacity: float | None = None
    observation_timestamp: float = 10.0
    evaluation_timestamp: float = 10.0
    confidence: float | None = None

    @property
    def physical_margin(self) -> float:
        """Return the true physical decision-validity margin."""

        return self.physical_capacity - self.demand

    @property
    def physical_valid(self) -> bool:
        """Return whether the decision is valid in physical reality."""

        return self.physical_margin >= 0

    @property
    def evidence_error(self) -> float | None:
        """Return observation error when a single observation exists."""

        if self.observed_capacity is None:
            return None

        return self.observed_capacity - self.physical_capacity

    @property
    def evidence_age(self) -> float:
        """Return the age of the runtime observation."""

        return self.evaluation_timestamp - self.observation_timestamp


def build_evidence_conditions() -> tuple[EvidenceCondition, ...]:
    """Build the deterministic EXP-006 evidence matrix."""

    return (
        EvidenceCondition(
            condition_id="E0",
            description="Accurate evidence for an invalid decision.",
            twin_capacity=10,
            physical_capacity=6,
            demand=8,
            evidence_type=EvidenceConditionType.ACCURATE,
            observed_capacity=6,
        ),
        EvidenceCondition(
            condition_id="E1",
            description=(
                "Small observation error preserves invalid classification."
            ),
            twin_capacity=10,
            physical_capacity=6,
            demand=8,
            evidence_type=EvidenceConditionType.NOISY,
            observed_capacity=7,
            confidence=0.9,
        ),
        EvidenceCondition(
            condition_id="E2",
            description=(
                "Observation error moves invalid decision to boundary."
            ),
            twin_capacity=10,
            physical_capacity=6,
            demand=8,
            evidence_type=EvidenceConditionType.NOISY,
            observed_capacity=8,
            confidence=0.8,
        ),
        EvidenceCondition(
            condition_id="E3",
            description=(
                "Observation error makes invalid decision appear valid."
            ),
            twin_capacity=10,
            physical_capacity=6,
            demand=8,
            evidence_type=EvidenceConditionType.NOISY,
            observed_capacity=9,
            confidence=0.7,
        ),
        EvidenceCondition(
            condition_id="E4",
            description=(
                "Stale pre-change observation hides invalid physical state."
            ),
            twin_capacity=10,
            physical_capacity=6,
            demand=8,
            evidence_type=EvidenceConditionType.STALE,
            observed_capacity=10,
            observation_timestamp=2.0,
            evaluation_timestamp=10.0,
        ),
        EvidenceCondition(
            condition_id="E5",
            description="Required runtime capacity evidence is missing.",
            twin_capacity=10,
            physical_capacity=6,
            demand=8,
            evidence_type=EvidenceConditionType.MISSING,
            observed_capacity=None,
        ),
        EvidenceCondition(
            condition_id="E6",
            description=(
                "Conflicting sources report invalid and valid capacities."
            ),
            twin_capacity=10,
            physical_capacity=6,
            demand=8,
            evidence_type=EvidenceConditionType.CONFLICTING,
            observed_capacity=6,
            secondary_observed_capacity=9,
        ),
        EvidenceCondition(
            condition_id="E7",
            description=(
                "Accurate evidence confirms a physically valid decision."
            ),
            twin_capacity=10,
            physical_capacity=9,
            demand=8,
            evidence_type=EvidenceConditionType.ACCURATE,
            observed_capacity=9,
        ),
        EvidenceCondition(
            condition_id="E8",
            description=(
                "Negative observation error makes valid decision appear invalid."
            ),
            twin_capacity=10,
            physical_capacity=9,
            demand=8,
            evidence_type=EvidenceConditionType.NOISY,
            observed_capacity=7,
            confidence=0.8,
        ),
        EvidenceCondition(
            condition_id="E9",
            description=(
                "Same positive error remains safe with a larger true margin."
            ),
            twin_capacity=12,
            physical_capacity=10,
            demand=6,
            evidence_type=EvidenceConditionType.NOISY,
            observed_capacity=11,
            confidence=0.9,
        ),
        EvidenceCondition(
            condition_id="E10",
            description=(
                "Same positive error hides invalidity near a tight boundary."
            ),
            twin_capacity=8,
            physical_capacity=6,
            demand=7,
            evidence_type=EvidenceConditionType.NOISY,
            observed_capacity=7,
            confidence=0.9,
        ),
        EvidenceCondition(
            condition_id="E11",
            description=(
                "Old observation matches Twin but not current physical state."
            ),
            twin_capacity=10,
            physical_capacity=7,
            demand=8,
            evidence_type=EvidenceConditionType.STALE,
            observed_capacity=10,
            observation_timestamp=1.0,
            evaluation_timestamp=10.0,
        ),
    )
