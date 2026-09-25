"""Evaluation of runtime assurance outcomes for DARA-DT."""

from dataclasses import dataclass
from enum import Enum

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.experiments.ground_truth import GroundTruth


class AssuranceOutcome(str, Enum):
    """Possible outcomes of an assurance decision."""

    TRUE_INTERVENTION = "true_intervention"
    FALSE_INTERVENTION = "false_intervention"
    MISSED_INTERVENTION = "missed_intervention"
    CORRECT_NON_INTERVENTION = "correct_non_intervention"


@dataclass(frozen=True)
class OutcomeResult:
    """Comparison between ground truth and assurance behaviour."""

    decision_id: str
    outcome: AssuranceOutcome


class OutcomeEvaluator:
    """Compare runtime assurance decisions against ground truth."""

    def evaluate(
        self,
        ground_truth: GroundTruth,
        assurance: AssuranceDecision,
    ) -> OutcomeResult:
        """Classify the outcome of an assurance decision."""

        if ground_truth.decision_id != assurance.decision_id:
            raise ValueError(
                "Ground truth and assurance decision IDs do not match."
            )

        intervention_required = ground_truth.intervention_required

        intervened = assurance.authority != AuthorityState.ALLOW

        if intervention_required and intervened:
            outcome = AssuranceOutcome.TRUE_INTERVENTION

        elif not intervention_required and intervened:
            outcome = AssuranceOutcome.FALSE_INTERVENTION

        elif intervention_required and not intervened:
            outcome = AssuranceOutcome.MISSED_INTERVENTION

        else:
            outcome = AssuranceOutcome.CORRECT_NON_INTERVENTION

        return OutcomeResult(
            decision_id=assurance.decision_id,
            outcome=outcome,
        )
