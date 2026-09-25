"""Ground-truth labels for DARA-DT assurance experiments."""

from dataclasses import dataclass
from enum import Enum


class InterventionLabel(str, Enum):
    """Ground-truth requirement for runtime intervention."""

    INTERVENE = "intervene"
    DO_NOT_INTERVENE = "do_not_intervene"


@dataclass(frozen=True)
class GroundTruth:
    """Ground-truth label for an experimental decision."""

    decision_id: str
    label: InterventionLabel
    reason: str

    @property
    def intervention_required(self) -> bool:
        """Return whether runtime intervention is required."""
        return self.label == InterventionLabel.INTERVENE
