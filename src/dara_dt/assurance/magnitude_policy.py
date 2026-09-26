"""Magnitude-based assurance policy for DARA-DT experiments.

This module provides a baseline assurance strategy that decides whether to
intervene using only the magnitude of detected physical-digital divergence.

Decision relevance is intentionally ignored so that this policy can serve as
a baseline for evaluating whether decision-relevant assurance provides useful
information beyond divergence magnitude alone.
"""

from dataclasses import dataclass

from dara_dt.assurance.model import (
    AssuranceDecision,
    AuthorityState,
)
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence


@dataclass(frozen=True)
class MagnitudeAssurancePolicy:
    """Intervene when numeric divergence exceeds a fixed threshold."""

    threshold: float

    def decide(
        self,
        decision: Decision,
        divergences: list[Divergence],
    ) -> AssuranceDecision:
        """Return an assurance decision using divergence magnitude alone."""

        measurable_magnitudes = tuple(
            magnitude
            for divergence in divergences
            if (magnitude := self._magnitude(divergence)) is not None
        )

        exceeds_threshold = any(
            magnitude > self.threshold
            for magnitude in measurable_magnitudes
        )

        if exceeds_threshold:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.DEFER,
                reason=(
                    "Numeric physical-digital divergence exceeds "
                    f"the fixed threshold of {self.threshold}."
                ),
                relevant_divergence_count=0,
            )

        return AssuranceDecision(
            decision_id=decision.decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "No numeric physical-digital divergence exceeds "
                f"the fixed threshold of {self.threshold}."
            ),
            relevant_divergence_count=0,
        )

    @staticmethod
    def _magnitude(divergence: Divergence) -> float | None:
        """Return absolute numeric divergence magnitude when measurable."""

        physical = divergence.physical_value
        twin = divergence.twin_value

        if isinstance(physical, bool) or isinstance(twin, bool):
            return None

        if not isinstance(physical, (int, float)):
            return None

        if not isinstance(twin, (int, float)):
            return None

        return abs(float(twin) - float(physical))
