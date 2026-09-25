"""Tests for DARA-DT runtime assurance outcome evaluation."""

import pytest

from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome, OutcomeEvaluator
from dara_dt.experiments.ground_truth import (
    GroundTruth,
    InterventionLabel,
)


def create_assurance(authority: AuthorityState) -> AssuranceDecision:
    """Create an assurance decision for testing."""
    return AssuranceDecision(
        decision_id="decision_001",
        authority=authority,
        reason="Test assurance decision.",
        relevant_divergence_count=1,
    )


def create_ground_truth(
    label: InterventionLabel,
) -> GroundTruth:
    """Create a ground-truth label for testing."""
    return GroundTruth(
        decision_id="decision_001",
        label=label,
        reason="Test ground truth.",
    )


def test_true_intervention():
    evaluator = OutcomeEvaluator()

    result = evaluator.evaluate(
        create_ground_truth(InterventionLabel.INTERVENE),
        create_assurance(AuthorityState.DEFER),
    )

    assert result.outcome == AssuranceOutcome.TRUE_INTERVENTION


def test_false_intervention():
    evaluator = OutcomeEvaluator()

    result = evaluator.evaluate(
        create_ground_truth(InterventionLabel.DO_NOT_INTERVENE),
        create_assurance(AuthorityState.DEFER),
    )

    assert result.outcome == AssuranceOutcome.FALSE_INTERVENTION


def test_missed_intervention():
    evaluator = OutcomeEvaluator()

    result = evaluator.evaluate(
        create_ground_truth(InterventionLabel.INTERVENE),
        create_assurance(AuthorityState.ALLOW),
    )

    assert result.outcome == AssuranceOutcome.MISSED_INTERVENTION


def test_correct_non_intervention():
    evaluator = OutcomeEvaluator()

    result = evaluator.evaluate(
        create_ground_truth(InterventionLabel.DO_NOT_INTERVENE),
        create_assurance(AuthorityState.ALLOW),
    )

    assert (
        result.outcome
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )


def test_mismatched_decision_ids_raise_error():
    evaluator = OutcomeEvaluator()

    ground_truth = GroundTruth(
        decision_id="decision_001",
        label=InterventionLabel.INTERVENE,
        reason="Test ground truth.",
    )

    assurance = AssuranceDecision(
        decision_id="decision_999",
        authority=AuthorityState.DEFER,
        reason="Test assurance decision.",
        relevant_divergence_count=1,
    )

    with pytest.raises(ValueError):
        evaluator.evaluate(
            ground_truth,
            assurance,
        )
