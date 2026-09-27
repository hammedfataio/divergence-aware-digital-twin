"""Decision-impact models for DARA-DT.

This module defines the data structures used to represent the estimated
effect of decision-relevant physical-digital divergence on an
AI-generated decision.

The models intentionally separate decision impact from physical
ground-truth validation. Ground truth belongs to the evaluation layer,
not to the runtime assurance policy.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ImpactState(str, Enum):
    """Possible runtime impact states for decision-relevant divergence."""

    NO_IMPACT = "no_impact"
    MARGIN_REDUCED = "margin_reduced"
    BOUNDARY = "boundary"
    INVALIDATING = "invalidating"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class ImpactEvidence:
    """Runtime evidence used when estimating decision impact.

    Attributes:
        source:
            Origin of the runtime evidence.

        variable:
            State variable described by the evidence.

        observed_value:
            Value available from the runtime evidence source.

        twin_value:
            Value represented by the Digital Twin.
    """

    source: str
    variable: str
    observed_value: Any
    twin_value: Any


@dataclass(frozen=True)
class DecisionImpact:
    """Estimated impact of divergence on a specific decision.

    Attributes:
        decision_id:
            Identifier of the AI-generated decision being assessed.

        dependency:
            Decision dependency affected by the divergence.

        impact_state:
            Estimated effect of the divergence on the decision.

        estimated_margin:
            Decision-specific runtime margin when a meaningful numeric
            margin can be estimated. None is used when the dependency
            does not support a numeric margin.

        evidence:
            Runtime evidence supporting the impact estimate.

        reason:
            Human-readable explanation of the impact classification.
    """

    decision_id: str
    dependency: str
    impact_state: ImpactState
    estimated_margin: float | None
    evidence: tuple[ImpactEvidence, ...]
    reason: str

    @property
    def invalidating(self) -> bool:
        """Return whether the estimated impact invalidates the decision."""

        return self.impact_state == ImpactState.INVALIDATING

    @property
    def uncertain(self) -> bool:
        """Return whether available evidence is insufficient."""

        return self.impact_state == ImpactState.UNCERTAIN

    @property
    def requires_attention(self) -> bool:
        """Return whether runtime assurance should examine the impact."""

        return self.impact_state in {
            ImpactState.BOUNDARY,
            ImpactState.INVALIDATING,
            ImpactState.UNCERTAIN,
        }
