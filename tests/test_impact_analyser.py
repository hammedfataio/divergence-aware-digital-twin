"""Tests for the DARA-DT decision-impact analyser."""

import pytest

from dara_dt.impact.analyser import DecisionImpactAnalyser
from dara_dt.impact.model import ImpactEvidence, ImpactState


def make_capacity_evidence(
    observed_capacity: float,
    twin_capacity: float = 10,
) -> ImpactEvidence:
    """Create capacity evidence for impact-analysis tests."""

    return ImpactEvidence(
        source="vehicle_sensor",
        variable="capacity",
        observed_value=observed_capacity,
        twin_value=twin_capacity,
    )


def test_equal_capacity_has_no_impact() -> None:
    """Matching observed and Twin capacity should not reduce margin."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_capacity(
        decision_id="decision_001",
        dependency="vehicle.capacity",
        required_demand=5,
        evidence=make_capacity_evidence(
            observed_capacity=10,
            twin_capacity=10,
        ),
    )

    assert impact.impact_state == ImpactState.NO_IMPACT
    assert impact.estimated_margin == 5.0
    assert impact.invalidating is False


def test_reduced_capacity_reduces_margin_without_invalidating() -> None:
    """Relevant divergence may reduce margin while remaining feasible."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_capacity(
        decision_id="decision_002",
        dependency="vehicle.capacity",
        required_demand=5,
        evidence=make_capacity_evidence(observed_capacity=7),
    )

    assert impact.impact_state == ImpactState.MARGIN_REDUCED
    assert impact.estimated_margin == 2.0
    assert impact.invalidating is False


def test_capacity_equal_to_demand_is_boundary() -> None:
    """Observed capacity equal to demand should identify the boundary."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_capacity(
        decision_id="decision_003",
        dependency="vehicle.capacity",
        required_demand=5,
        evidence=make_capacity_evidence(observed_capacity=5),
    )

    assert impact.impact_state == ImpactState.BOUNDARY
    assert impact.estimated_margin == 0.0
    assert impact.requires_attention is True


def test_capacity_below_demand_is_invalidating() -> None:
    """Observed capacity below demand should invalidate the decision."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_capacity(
        decision_id="decision_004",
        dependency="vehicle.capacity",
        required_demand=5,
        evidence=make_capacity_evidence(observed_capacity=4),
    )

    assert impact.impact_state == ImpactState.INVALIDATING
    assert impact.estimated_margin == -1.0
    assert impact.invalidating is True


def test_same_divergence_can_have_different_decision_impact() -> None:
    """Decision impact should depend on the decision requirement.

    Both cases use the same Twin capacity and observed capacity.
    Only the order demand changes.
    """

    analyser = DecisionImpactAnalyser()

    evidence = make_capacity_evidence(
        observed_capacity=7,
        twin_capacity=10,
    )

    low_demand = analyser.analyse_capacity(
        decision_id="decision_low",
        dependency="vehicle.capacity",
        required_demand=5,
        evidence=evidence,
    )

    high_demand = analyser.analyse_capacity(
        decision_id="decision_high",
        dependency="vehicle.capacity",
        required_demand=8,
        evidence=evidence,
    )

    assert low_demand.impact_state == ImpactState.MARGIN_REDUCED
    assert low_demand.estimated_margin == 2.0

    assert high_demand.impact_state == ImpactState.INVALIDATING
    assert high_demand.estimated_margin == -1.0


def test_different_boundaries_are_decision_specific() -> None:
    """Validity boundaries should move when decision demand changes."""

    analyser = DecisionImpactAnalyser()

    first = analyser.analyse_capacity(
        decision_id="decision_005",
        dependency="vehicle.capacity",
        required_demand=5,
        evidence=make_capacity_evidence(
            observed_capacity=5,
            twin_capacity=10,
        ),
    )

    second = analyser.analyse_capacity(
        decision_id="decision_006",
        dependency="vehicle.capacity",
        required_demand=8,
        evidence=make_capacity_evidence(
            observed_capacity=8,
            twin_capacity=10,
        ),
    )

    assert first.impact_state == ImpactState.BOUNDARY
    assert first.estimated_margin == 0.0

    assert second.impact_state == ImpactState.BOUNDARY
    assert second.estimated_margin == 0.0


def test_uncertain_impact_is_explicit() -> None:
    """Insufficient evidence should remain explicitly uncertain."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.uncertain(
        decision_id="decision_007",
        dependency="vehicle.status",
        reason="No current status observation is available.",
    )

    assert impact.impact_state == ImpactState.UNCERTAIN
    assert impact.estimated_margin is None
    assert impact.uncertain is True
    assert impact.requires_attention is True


def test_non_numeric_observed_capacity_is_rejected() -> None:
    """Capacity analysis should reject non-numeric runtime evidence."""

    analyser = DecisionImpactAnalyser()

    evidence = ImpactEvidence(
        source="vehicle_sensor",
        variable="capacity",
        observed_value="unknown",
        twin_value=10,
    )

    with pytest.raises(
        ValueError,
        match="Observed capacity evidence must be numeric.",
    ):
        analyser.analyse_capacity(
            decision_id="decision_008",
            dependency="vehicle.capacity",
            required_demand=5,
            evidence=evidence,
        )


def test_non_numeric_demand_is_rejected() -> None:
    """Capacity analysis should reject invalid demand evidence."""

    analyser = DecisionImpactAnalyser()

    with pytest.raises(
        ValueError,
        match="Required demand must be numeric.",
    ):
        analyser.analyse_capacity(
            decision_id="decision_009",
            dependency="vehicle.capacity",
            required_demand="five",  # type: ignore[arg-type]
            evidence=make_capacity_evidence(observed_capacity=7),
        )
