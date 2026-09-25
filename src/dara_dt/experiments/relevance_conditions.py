"""Decision-relevance conditions for DARA-DT experiments."""

from dataclasses import dataclass
from enum import Enum


class RelevanceCondition(str, Enum):
    """Experimental conditions for decision-relevance evaluation."""

    B_HIGH_DIVERGENCE_LOW_RELEVANCE = "B"
    C_LOW_DIVERGENCE_HIGH_RELEVANCE = "C"


@dataclass(frozen=True)
class ConditionDefinition:
    """Definition of a decision-relevance experimental condition."""

    condition: RelevanceCondition
    name: str
    description: str
    expected_intervention: bool


CONDITIONS = {
    RelevanceCondition.B_HIGH_DIVERGENCE_LOW_RELEVANCE:
        ConditionDefinition(
            condition=(
                RelevanceCondition.B_HIGH_DIVERGENCE_LOW_RELEVANCE
            ),
            name="High divergence, low decision relevance",
            description=(
                "Multiple physical-digital divergences exist, "
                "but none affect variables required by the "
                "current decision."
            ),
            expected_intervention=False,
        ),

    RelevanceCondition.C_LOW_DIVERGENCE_HIGH_RELEVANCE:
        ConditionDefinition(
            condition=(
                RelevanceCondition.C_LOW_DIVERGENCE_HIGH_RELEVANCE
            ),
            name="Low divergence, high decision relevance",
            description=(
                "A small number of physical-digital divergences "
                "directly affect variables required by the "
                "current decision."
            ),
            expected_intervention=True,
        ),
}
