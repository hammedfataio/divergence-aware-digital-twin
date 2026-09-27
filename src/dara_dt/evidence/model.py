"""Runtime evidence models for DARA-DT.

This module represents observations available to the runtime assurance
mechanism.

Runtime evidence is intentionally kept separate from physical ground truth
and Digital Twin state. This separation allows experiments to investigate
how noisy, stale, missing, or otherwise uncertain observations affect
decision-impact-aware assurance.
"""

from dataclasses import dataclass
from enum import Enum
from numbers import Real
from typing import Any


class EvidenceStatus(str, Enum):
    """Availability and quality state of runtime evidence."""

    AVAILABLE = "available"
    MISSING = "missing"
    STALE = "stale"
    CONFLICTING = "conflicting"


@dataclass(frozen=True)
class RuntimeEvidence:
    """Observation available to the runtime assurance mechanism.

    Attributes:
        source:
            Identifier for the source that produced the observation.
        dependency:
            Decision dependency represented by the evidence.
        observed_value:
            Value observed by the runtime evidence source. Missing evidence
            may use ``None``.
        timestamp:
            Simulation time at which the observation was produced.
        confidence:
            Optional confidence associated with the observation.
        status:
            Current evidence-quality status.
    """

    source: str
    dependency: str
    observed_value: Any
    timestamp: float
    confidence: float | None = None
    status: EvidenceStatus = EvidenceStatus.AVAILABLE

    def __post_init__(self) -> None:
        """Validate evidence metadata."""

        if not self.source:
            raise ValueError("Evidence source must not be empty.")

        if not self.dependency:
            raise ValueError("Evidence dependency must not be empty.")

        if not isinstance(self.timestamp, Real):
            raise TypeError("Evidence timestamp must be numeric.")

        if self.timestamp < 0:
            raise ValueError("Evidence timestamp must not be negative.")

        if self.confidence is not None:
            if not isinstance(self.confidence, Real):
                raise TypeError("Evidence confidence must be numeric.")

            if not 0.0 <= float(self.confidence) <= 1.0:
                raise ValueError(
                    "Evidence confidence must be between 0 and 1."
                )

        if (
            self.status == EvidenceStatus.MISSING
            and self.observed_value is not None
        ):
            raise ValueError(
                "Missing evidence must not contain an observed value."
            )

        if (
            self.status != EvidenceStatus.MISSING
            and self.observed_value is None
        ):
            raise ValueError(
                "Available evidence must contain an observed value."
            )

    @property
    def is_available(self) -> bool:
        """Return whether an observation value is available."""

        return (
            self.status != EvidenceStatus.MISSING
            and self.observed_value is not None
        )

    def age_at(self, current_time: float) -> float:
        """Return evidence age at the supplied simulation time."""

        if not isinstance(current_time, Real):
            raise TypeError("Current time must be numeric.")

        if current_time < self.timestamp:
            raise ValueError(
                "Current time must not precede the evidence timestamp."
            )

        return float(current_time - self.timestamp)
