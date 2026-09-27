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


def make_status_evidence(
    observed_status: str,
    twin_status: str = "operational",
) -> ImpactEvidence:
    """Create operational-status evidence."""

    return ImpactEvidence(
        source="vehicle_sensor",
        variable="status",
        observed_value=observed_status,
        twin_value=twin_status,
    )


def make_availability_evidence(
    observed_available: bool,
    twin_available: bool = True,
) -> ImpactEvidence:
    """Create vehicle-availability evidence."""

    return ImpactEvidence(
        source="vehicle_sensor",
        variable="available",
        observed_value=observed_available,
        twin_value=twin_available,
    )


def make_location_evidence(
    observed_location: str,
    twin_location: str = "depot",
) -> ImpactEvidence:
    """Create vehicle-location evidence."""

    return ImpactEvidence(
        source="vehicle_sensor",
        variable="location",
        observed_value=observed_location,
        twin_value=twin_location,
    )


# ---------------------------------------------------------------------------
# Capacity
# ---------------------------------------------------------------------------


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
    """Relevant capacity divergence may reduce margin and remain feasible."""

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
    """Decision impact should depend on the decision requirement."""

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


# ---------------------------------------------------------------------------
# Operational status
# ---------------------------------------------------------------------------


def test_matching_operational_status_has_no_impact() -> None:
    """Matching operational state should not affect the decision."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_status(
        decision_id="status_001",
        dependency="vehicle.status",
        evidence=make_status_evidence(
            observed_status="operational",
            twin_status="operational",
        ),
    )

    assert impact.impact_state == ImpactState.NO_IMPACT
    assert impact.invalidating is False


def test_broken_down_vehicle_invalidates_status_dependency() -> None:
    """A broken-down selected vehicle should invalidate the decision."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_status(
        decision_id="status_002",
        dependency="vehicle.status",
        evidence=make_status_evidence(
            observed_status="broken_down",
            twin_status="operational",
        ),
    )

    assert impact.impact_state == ImpactState.INVALIDATING
    assert impact.invalidating is True
    assert impact.requires_attention is True


def test_status_divergence_can_remain_valid() -> None:
    """A Twin mismatch need not invalidate the required operational state."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_status(
        decision_id="status_003",
        dependency="vehicle.status",
        evidence=make_status_evidence(
            observed_status="operational",
            twin_status="maintenance_due",
        ),
    )

    assert impact.impact_state == ImpactState.MARGIN_REDUCED
    assert impact.invalidating is False


def test_non_string_status_evidence_is_rejected() -> None:
    """Operational-status evidence should use explicit string states."""

    analyser = DecisionImpactAnalyser()

    evidence = ImpactEvidence(
        source="vehicle_sensor",
        variable="status",
        observed_value=False,
        twin_value="operational",
    )

    with pytest.raises(
        ValueError,
        match="Observed operational-status evidence must be a string.",
    ):
        analyser.analyse_status(
            decision_id="status_004",
            dependency="vehicle.status",
            evidence=evidence,
        )


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def test_matching_available_state_has_no_impact() -> None:
    """Matching availability should leave the decision unaffected."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_availability(
        decision_id="availability_001",
        dependency="vehicle.available",
        evidence=make_availability_evidence(
            observed_available=True,
            twin_available=True,
        ),
    )

    assert impact.impact_state == ImpactState.NO_IMPACT
    assert impact.invalidating is False


def test_unavailable_vehicle_invalidates_decision() -> None:
    """Physical unavailability should invalidate a required assignment."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_availability(
        decision_id="availability_002",
        dependency="vehicle.available",
        evidence=make_availability_evidence(
            observed_available=False,
            twin_available=True,
        ),
    )

    assert impact.impact_state == ImpactState.INVALIDATING
    assert impact.invalidating is True


def test_availability_divergence_can_remain_valid() -> None:
    """Twin disagreement need not invalidate physical availability."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_availability(
        decision_id="availability_003",
        dependency="vehicle.available",
        evidence=make_availability_evidence(
            observed_available=True,
            twin_available=False,
        ),
    )

    assert impact.impact_state == ImpactState.MARGIN_REDUCED
    assert impact.invalidating is False


def test_non_boolean_availability_is_rejected() -> None:
    """Availability evidence must use boolean values."""

    analyser = DecisionImpactAnalyser()

    evidence = ImpactEvidence(
        source="vehicle_sensor",
        variable="available",
        observed_value="yes",
        twin_value=True,
    )

    with pytest.raises(
        ValueError,
        match="Observed availability evidence must be boolean.",
    ):
        analyser.analyse_availability(
            decision_id="availability_004",
            dependency="vehicle.available",
            evidence=evidence,
        )


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------


def test_matching_permitted_location_has_no_impact() -> None:
    """Matching location inside the permitted set should have no impact."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_location(
        decision_id="location_001",
        dependency="vehicle.location",
        evidence=make_location_evidence(
            observed_location="depot",
            twin_location="depot",
        ),
        permitted_locations={"depot", "near_depot"},
    )

    assert impact.impact_state == ImpactState.NO_IMPACT
    assert impact.invalidating is False


def test_divergent_but_permitted_location_remains_valid() -> None:
    """Location divergence may remain compatible with dispatch."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_location(
        decision_id="location_002",
        dependency="vehicle.location",
        evidence=make_location_evidence(
            observed_location="near_depot",
            twin_location="depot",
        ),
        permitted_locations={"depot", "near_depot"},
    )

    assert impact.impact_state == ImpactState.MARGIN_REDUCED
    assert impact.invalidating is False


def test_location_outside_permitted_set_invalidates_decision() -> None:
    """An incompatible physical location should invalidate dispatch."""

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_location(
        decision_id="location_003",
        dependency="vehicle.location",
        evidence=make_location_evidence(
            observed_location="remote_site",
            twin_location="depot",
        ),
        permitted_locations={"depot", "near_depot"},
    )

    assert impact.impact_state == ImpactState.INVALIDATING
    assert impact.invalidating is True


def test_empty_permitted_location_set_is_rejected() -> None:
    """Location analysis requires an explicit compatibility rule."""

    analyser = DecisionImpactAnalyser()

    with pytest.raises(
        ValueError,
        match="At least one permitted dispatch location is required.",
    ):
        analyser.analyse_location(
            decision_id="location_004",
            dependency="vehicle.location",
            evidence=make_location_evidence(
                observed_location="depot",
                twin_location="depot",
            ),
            permitted_locations=set(),
        )


def test_non_string_location_evidence_is_rejected() -> None:
    """Location evidence should use explicit location identifiers."""

    analyser = DecisionImpactAnalyser()

    evidence = ImpactEvidence(
        source="vehicle_sensor",
        variable="location",
        observed_value=123,
        twin_value="depot",
    )

    with pytest.raises(
        ValueError,
        match="Observed location evidence must be a string.",
    ):
        analyser.analyse_location(
            decision_id="location_005",
            dependency="vehicle.location",
            evidence=evidence,
            permitted_locations={"depot"},
        )


# ---------------------------------------------------------------------------
# Shared validation
# ---------------------------------------------------------------------------


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
    """Capacity analysis should reject invalid demand."""

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
