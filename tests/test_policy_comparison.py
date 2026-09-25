"""Tests for comparative assurance-policy evaluation."""

from dara_dt.assurance.model import AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.ground_truth import (
    GroundTruth,
    InterventionLabel,
)
from dara_dt.experiments.policy_comparison import compare_policies


def make_decision() -> Decision:
    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=0.0,
    )


def test_relevant_divergence_distinguishes_no_assurance():
    """Relevant unsafe divergence should trigger B1 and DARA-DT."""

    decision = make_decision()

    divergences = [
        Divergence(
            entity_type="vehicles",
            entity_id="vehicle_07",
            variable="status",
            physical_value="broken_down",
            twin_value="operational",
        )
    ]

    ground_truth = GroundTruth(
        decision_id=decision.decision_id,
        label=InterventionLabel.INTERVENE,
        reason="Selected physical vehicle is broken down.",
    )

    result = compare_policies(
        decision,
        divergences,
        ground_truth,
    )

    assert (
        result.no_assurance.outcome
        == AssuranceOutcome.MISSED_INTERVENTION
    )

    assert (
        result.global_divergence.outcome
        == AssuranceOutcome.TRUE_INTERVENTION
    )

    assert (
        result.dara_dt.outcome
        == AssuranceOutcome.TRUE_INTERVENTION
    )


def test_irrelevant_divergence_distinguishes_global_policy():
    """Irrelevant divergence should not unnecessarily stop autonomy."""

    decision = make_decision()

    divergences = [
        Divergence(
            entity_type="vehicles",
            entity_id="vehicle_03",
            variable="status",
            physical_value="broken_down",
            twin_value="operational",
        ),
        Divergence(
            entity_type="vehicles",
            entity_id="vehicle_04",
            variable="location",
            physical_value="node_04",
            twin_value="node_99",
        ),
    ]

    ground_truth = GroundTruth(
        decision_id=decision.decision_id,
        label=InterventionLabel.DO_NOT_INTERVENE,
        reason="Divergence does not affect the selected vehicle.",
    )

    result = compare_policies(
        decision,
        divergences,
        ground_truth,
    )

    assert (
        result.no_assurance.outcome
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )

    assert (
        result.global_divergence.outcome
        == AssuranceOutcome.FALSE_INTERVENTION
    )

    assert (
        result.dara_dt.outcome
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )
