"""Runtime assurance models for DARA-DT."""

from dataclasses import dataclass
from enum import Enum


class AuthorityState(str, Enum):
    """Permitted autonomy states for an AI-generated decision."""

    ALLOW = "allow"
    RESTRICT = "restrict"
    DEFER = "defer"
    FALLBACK = "fallback"


@dataclass(frozen=True)
class AssuranceDecision:
    """Runtime assurance decision for a proposed AI action."""

    decision_id: str
    authority: AuthorityState
    reason: str
    relevant_divergence_count: int

    @property
    def autonomous_execution_allowed(self) -> bool:
        """Return whether unrestricted autonomous execution is permitted."""
        return self.authority == AuthorityState.ALLOW
