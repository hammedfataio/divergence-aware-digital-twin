"""Magnitude-based assurance policy for DARA-DT experiments.

This module provides a baseline assurance strategy that decides whether to
intervene using only the magnitude of detected physical-digital divergence.

It deliberately ignores decision relevance. This allows experiments to test
whether decision-relevant assurance provides useful information beyond a
simple divergence-severity threshold.
"""

from dataclasses import dataclass

from dara_dt.assurance.model import AssuranceAction
from dara_dt.divergence.detector import Divergence


@dataclass(frozen=True)
class MagnitudeAssurancePolicy:
    """Intervene when divergence magnitude exceeds a fixed threshold."""

    threshold: float

    def decide(
        self,
        divergences: list[Divergence],
    ) -> AssuranceAction:
        """Return an assurance action from divergence magnitude alone.

        The policy defers when at least one detected divergence has a numeric
        magnitude strictly greater than the configured threshold.

        Decision dependencies and decision relevance are intentionally not
        considered by this baseline.
        """

        for divergence in divergences:
            magnitude = self._magnitude(divergence)

            if magnitude is not None and magnitude > self.threshold:
                return AssuranceAction.DEFER

        return AssuranceAction.ALLOW

    @staticmethod
    def _magnitude(divergence: Divergence) -> float | None:
        """Return numeric absolute divergence magnitude when measurable."""

        physical = divergence.physical_value
        twin = divergence.twin_value

        if isinstance(physical, bool) or isinstance(twin, bool):
            return None

        if not isinstance(physical, (int, float)):
            return None

        if not isinstance(twin, (int, float)):
            return None

        return abs(float(twin) - float(physical))
