"""Integration test for the end-to-end stale Digital Twin experiment."""

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.breakdown_experiment import (
    run_breakdown_experiment,
)
from dara_dt.experiments.ground_truth import InterventionLabel


def test_breakdown_experiment_detects_unsafe_decision():
    """DARA-DT should intervene in the stale-Twin breakdown scenario."""

    result = run_breakdown_experiment()

    assert result.event.physical_status == "broken_down"
    assert result.event.twin_status == "operational"

    assert len(result.divergences) == 2

    paths = {
        divergence.path
        for divergence in result.divergences
    }

    assert "vehicles.vehicle_07.status" in paths
    assert "vehicles.vehicle_07.available" in paths

    assert result.relevance.has_relevant_divergence is True
    assert len(result.relevance.relevant) == 2

    assert result.assurance.authority == AuthorityState.DEFER
    assert result.assurance.autonomous_execution_allowed is False

    assert (
        result.ground_truth.label
        == InterventionLabel.INTERVENE
    )

    assert (
        result.outcome.outcome
        == AssuranceOutcome.TRUE_INTERVENTION
    )


def test_breakdown_ground_truth_is_independent():
    """Physical state should independently establish invalidity."""

    result = run_breakdown_experiment()

    assert result.ground_truth.intervention_required is True

    assert (
        "physically"
        in result.ground_truth.reason.lower()
    )
