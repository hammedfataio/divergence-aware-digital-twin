"""Controlled runtime evidence generation for EXP-006.

This module creates runtime evidence independently from experimental
ground truth. It allows controlled degradation of observations while
preserving the physical system state used by the evaluator.

No randomness is introduced at this stage. Evidence corruption is
explicit and reproducible so that experimental conditions can be
compared directly.
"""

from numbers import Real

from dara_dt.evidence.model import (
    EvidenceStatus,
    RuntimeEvidence,
)


class EvidenceGenerator:
    """Generate controlled runtime evidence for assurance experiments."""

    def accurate(
        self,
        *,
        dependency: str,
        physical_value: Real,
        timestamp: float,
        source: str = "runtime_monitor",
    ) -> RuntimeEvidence:
        """Generate evidence matching the physical state."""

        return RuntimeEvidence(
            source=source,
            dependency=dependency,
            observed_value=physical_value,
            timestamp=timestamp,
            confidence=1.0,
            status=EvidenceStatus.AVAILABLE,
        )

    def noisy(
        self,
        *,
        dependency: str,
        physical_value: Real,
        error: Real,
        timestamp: float,
        source: str = "runtime_monitor",
        confidence: float | None = None,
    ) -> RuntimeEvidence:
        """Generate evidence with a controlled additive observation error."""

        if not isinstance(physical_value, Real):
            raise TypeError("Physical value must be numeric.")

        if not isinstance(error, Real):
            raise TypeError("Evidence error must be numeric.")

        observed_value = physical_value + error

        return RuntimeEvidence(
            source=source,
            dependency=dependency,
            observed_value=observed_value,
            timestamp=timestamp,
            confidence=confidence,
            status=EvidenceStatus.AVAILABLE,
        )

    def stale(
        self,
        *,
        dependency: str,
        stale_value: Real,
        observation_timestamp: float,
        source: str = "runtime_monitor",
        confidence: float | None = None,
    ) -> RuntimeEvidence:
        """Generate an explicitly stale observation."""

        return RuntimeEvidence(
            source=source,
            dependency=dependency,
            observed_value=stale_value,
            timestamp=observation_timestamp,
            confidence=confidence,
            status=EvidenceStatus.STALE,
        )

    def missing(
        self,
        *,
        dependency: str,
        timestamp: float,
        source: str = "runtime_monitor",
    ) -> RuntimeEvidence:
        """Generate explicit missing runtime evidence."""

        return RuntimeEvidence(
            source=source,
            dependency=dependency,
            observed_value=None,
            timestamp=timestamp,
            confidence=None,
            status=EvidenceStatus.MISSING,
        )

    def conflicting(
        self,
        *,
        dependency: str,
        first_value: Real,
        second_value: Real,
        timestamp: float,
        first_source: str = "runtime_monitor_a",
        second_source: str = "runtime_monitor_b",
        confidence: float | None = None,
    ) -> tuple[RuntimeEvidence, RuntimeEvidence]:
        """Generate two conflicting observations for one dependency."""

        if first_value == second_value:
            raise ValueError(
                "Conflicting evidence requires different observed values."
            )

        first = RuntimeEvidence(
            source=first_source,
            dependency=dependency,
            observed_value=first_value,
            timestamp=timestamp,
            confidence=confidence,
            status=EvidenceStatus.CONFLICTING,
        )

        second = RuntimeEvidence(
            source=second_source,
            dependency=dependency,
            observed_value=second_value,
            timestamp=timestamp,
            confidence=confidence,
            status=EvidenceStatus.CONFLICTING,
        )

        return first, second
