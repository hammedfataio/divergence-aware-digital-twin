"""Tests for the EXP-008 cross-dependency evidence-aware DARA policy."""

import pytest

from dara_dt.assurance.divergence_evidence_policy import (
    DivergenceEvidencePolicy,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


@pytest.fixture
def policy() -> DivergenceEvidencePolicy:
    """Return a fresh DARA-DT evidence-aware policy."""

    return DivergenceEvidencePolicy()


def make_evidence(
    dependency: str,
    observed_value,
    status: EvidenceStatus = EvidenceStatus.AVAILABLE,
) -> RuntimeEvidence:
    """Create deterministic runtime evidence for policy tests."""

    return RuntimeEvidence(
        source="test_sensor",
        dependency=dependency,
        observed_value=observed_value,
        status=status,
        timestamp=10.0,
        confidence=1.0,
    )


# ---------------------------------------------------------------------------
# Capacity
# ---------------------------------------------------------------------------


def test_capacity_allows_valid_reliable_evidence(policy):
    """Reliable capacity above demand should preserve autonomy."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    result = policy.evaluate_capacity(
        decision_id="CAP-001",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.decision_id == "CAP-001"
    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 1


def test_capacity_allows_synchronised_valid_state(policy):
    """No divergence and sufficient capacity should allow execution."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=10.0,
    )

    result = policy.evaluate_capacity(
        decision_id="CAP-002",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 0


def test_capacity_defers_invalid_reliable_evidence(policy):
    """Reliable capacity below demand should prevent autonomous execution."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=4.0,
    )

    result = policy.evaluate_capacity(
        decision_id="CAP-003",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.authority == AuthorityState.DEFER
    assert result.relevant_divergence_count == 1


def test_capacity_restricts_exact_decision_boundary(policy):
    """Capacity exactly equal to demand should restrict authority."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=5.0,
    )

    result = policy.evaluate_capacity(
        decision_id="CAP-004",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.authority == AuthorityState.RESTRICT
    assert result.relevant_divergence_count == 1


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_capacity_defers_uncertain_evidence(policy, status):
    """Stale, missing and conflicting capacity evidence must defer."""

    observed_value = (
        None if status == EvidenceStatus.MISSING else 8.0
    )

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=observed_value,
        status=status,
    )

    result = policy.evaluate_capacity(
        decision_id="CAP-005",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_capacity_rejects_wrong_dependency(policy):
    """Capacity evaluation must reject unrelated evidence."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="operational",
    )

    with pytest.raises(ValueError):
        policy.evaluate_capacity(
            decision_id="CAP-006",
            evidence=evidence,
            twin_capacity=10.0,
            required_demand=5.0,
        )


def test_capacity_rejects_non_numeric_twin_capacity(policy):
    """Digital Twin capacity must be numeric."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    with pytest.raises(ValueError):
        policy.evaluate_capacity(
            decision_id="CAP-007",
            evidence=evidence,
            twin_capacity="ten",
            required_demand=5.0,
        )


def test_capacity_rejects_non_numeric_demand(policy):
    """Decision demand must be numeric."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    with pytest.raises(ValueError):
        policy.evaluate_capacity(
            decision_id="CAP-008",
            evidence=evidence,
            twin_capacity=10.0,
            required_demand="five",
        )


def test_capacity_non_numeric_runtime_value_defers(policy):
    """Malformed runtime capacity evidence must not authorise execution."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value="unknown",
    )

    result = policy.evaluate_capacity(
        decision_id="CAP-009",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.authority == AuthorityState.DEFER


# ---------------------------------------------------------------------------
# Operational status
# ---------------------------------------------------------------------------


def test_status_allows_operational_reliable_evidence(policy):
    """Operational evidence satisfying the requirement should allow."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="operational",
    )

    result = policy.evaluate_status(
        decision_id="STATUS-001",
        evidence=evidence,
        twin_status="operational",
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 0


def test_status_allows_valid_divergent_state(policy):
    """A Twin mismatch can remain valid for the decision requirement."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="operational",
    )

    result = policy.evaluate_status(
        decision_id="STATUS-002",
        evidence=evidence,
        twin_status="maintenance_due",
        required_status="operational",
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 1


def test_status_defers_broken_vehicle(policy):
    """Reliable broken-down evidence should prevent execution."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="broken_down",
    )

    result = policy.evaluate_status(
        decision_id="STATUS-003",
        evidence=evidence,
        twin_status="operational",
    )

    assert result.authority == AuthorityState.DEFER
    assert result.relevant_divergence_count == 1


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_status_defers_uncertain_evidence(policy, status):
    """Uncertain operational-status evidence should defer."""

    observed_value = (
        None
        if status == EvidenceStatus.MISSING
        else "operational"
    )

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value=observed_value,
        status=status,
    )

    result = policy.evaluate_status(
        decision_id="STATUS-004",
        evidence=evidence,
        twin_status="operational",
    )

    assert result.authority == AuthorityState.DEFER


def test_status_rejects_wrong_dependency(policy):
    """Status evaluation must reject evidence for another dependency."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    with pytest.raises(ValueError):
        policy.evaluate_status(
            decision_id="STATUS-005",
            evidence=evidence,
            twin_status="operational",
        )


def test_status_rejects_invalid_twin_state(policy):
    """Digital Twin status must be a non-empty string."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="operational",
    )

    with pytest.raises(ValueError):
        policy.evaluate_status(
            decision_id="STATUS-006",
            evidence=evidence,
            twin_status="",
        )


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def test_availability_allows_reliable_available_vehicle(policy):
    """Reliable available state should preserve autonomy."""

    evidence = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    result = policy.evaluate_availability(
        decision_id="AVAIL-001",
        evidence=evidence,
        twin_available=True,
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 0


def test_availability_defers_unavailable_vehicle(policy):
    """Reliable unavailable state should prevent execution."""

    evidence = make_evidence(
        dependency="vehicle.available",
        observed_value=False,
    )

    result = policy.evaluate_availability(
        decision_id="AVAIL-002",
        evidence=evidence,
        twin_available=True,
    )

    assert result.authority == AuthorityState.DEFER
    assert result.relevant_divergence_count == 1


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_availability_defers_uncertain_evidence(policy, status):
    """Uncertain availability evidence should defer."""

    observed_value = (
        None if status == EvidenceStatus.MISSING else True
    )

    evidence = make_evidence(
        dependency="vehicle.available",
        observed_value=observed_value,
        status=status,
    )

    result = policy.evaluate_availability(
        decision_id="AVAIL-003",
        evidence=evidence,
        twin_available=True,
    )

    assert result.authority == AuthorityState.DEFER


def test_availability_rejects_wrong_dependency(policy):
    """Availability evaluation must reject unrelated evidence."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    with pytest.raises(ValueError):
        policy.evaluate_availability(
            decision_id="AVAIL-004",
            evidence=evidence,
            twin_available=True,
        )


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------


def test_location_allows_permitted_reliable_location(policy):
    """Reliable permitted location should preserve autonomy."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="near_depot",
    )

    result = policy.evaluate_location(
        decision_id="LOC-001",
        evidence=evidence,
        twin_location="depot",
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 1


def test_location_allows_synchronised_permitted_location(policy):
    """Synchronized permitted location should allow execution."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    result = policy.evaluate_location(
        decision_id="LOC-002",
        evidence=evidence,
        twin_location="depot",
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 0


def test_location_defers_remote_vehicle(policy):
    """Reliable location outside permitted set should prevent execution."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="remote_site",
    )

    result = policy.evaluate_location(
        decision_id="LOC-003",
        evidence=evidence,
        twin_location="depot",
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.relevant_divergence_count == 1


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_location_defers_uncertain_evidence(policy, status):
    """Uncertain location evidence should defer."""

    observed_value = (
        None if status == EvidenceStatus.MISSING else "depot"
    )

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value=observed_value,
        status=status,
    )

    result = policy.evaluate_location(
        decision_id="LOC-004",
        evidence=evidence,
        twin_location="depot",
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER


def test_location_rejects_empty_permitted_locations(policy):
    """At least one permitted location must be supplied."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    with pytest.raises(ValueError):
        policy.evaluate_location(
            decision_id="LOC-005",
            evidence=evidence,
            twin_location="depot",
            permitted_locations=(),
        )


# ---------------------------------------------------------------------------
# Combined location + availability
# ---------------------------------------------------------------------------


def test_combined_location_availability_allows_valid_dispatch(policy):
    """Valid reliable location and availability should allow execution."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="near_depot",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    result = policy.evaluate_location_availability(
        decision_id="DISPATCH-001",
        location_evidence=location,
        availability_evidence=availability,
        twin_location="depot",
        twin_available=True,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.relevant_divergence_count == 1


def test_combined_location_availability_defers_remote_vehicle(policy):
    """Remote reliable location should invalidate dispatch."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="remote_site",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    result = policy.evaluate_location_availability(
        decision_id="DISPATCH-002",
        location_evidence=location,
        availability_evidence=availability,
        twin_location="depot",
        twin_available=True,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.relevant_divergence_count == 1


def test_combined_location_availability_defers_unavailable_vehicle(policy):
    """Unavailable vehicle should invalidate dispatch."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=False,
    )

    result = policy.evaluate_location_availability(
        decision_id="DISPATCH-003",
        location_evidence=location,
        availability_evidence=availability,
        twin_location="depot",
        twin_available=True,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.relevant_divergence_count == 1


def test_combined_counts_two_relevant_divergences(policy):
    """Location and availability divergence should both be represented."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="remote_site",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=False,
    )

    result = policy.evaluate_location_availability(
        decision_id="DISPATCH-004",
        location_evidence=location,
        availability_evidence=availability,
        twin_location="depot",
        twin_available=True,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.relevant_divergence_count == 2


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_combined_defers_uncertain_location(policy, status):
    """Uncertain location should defer despite reliable availability."""

    location_value = (
        None if status == EvidenceStatus.MISSING else "depot"
    )

    location = make_evidence(
        dependency="vehicle.location",
        observed_value=location_value,
        status=status,
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    result = policy.evaluate_location_availability(
        decision_id="DISPATCH-005",
        location_evidence=location,
        availability_evidence=availability,
        twin_location="depot",
        twin_available=True,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_combined_defers_uncertain_availability(policy, status):
    """Uncertain availability should defer despite reliable location."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    availability_value = (
        None if status == EvidenceStatus.MISSING else True
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=availability_value,
        status=status,
    )

    result = policy.evaluate_location_availability(
        decision_id="DISPATCH-006",
        location_evidence=location,
        availability_evidence=availability,
        twin_location="depot",
        twin_available=True,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER


def test_combined_rejects_wrong_location_dependency(policy):
    """Combined evaluation must validate location evidence."""

    location = make_evidence(
        dependency="vehicle.status",
        observed_value="operational",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    with pytest.raises(ValueError):
        policy.evaluate_location_availability(
            decision_id="DISPATCH-007",
            location_evidence=location,
            availability_evidence=availability,
            twin_location="depot",
            twin_available=True,
            permitted_locations=("depot",),
        )


def test_combined_rejects_wrong_availability_dependency(policy):
    """Combined evaluation must validate availability evidence."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    availability = make_evidence(
        dependency="vehicle.capacity",
        observed_value=10.0,
    )

    with pytest.raises(ValueError):
        policy.evaluate_location_availability(
            decision_id="DISPATCH-008",
            location_evidence=location,
            availability_evidence=availability,
            twin_location="depot",
            twin_available=True,
            permitted_locations=("depot",),
        )


# ---------------------------------------------------------------------------
# Scientific-integrity checks
# ---------------------------------------------------------------------------


def test_reliable_divergence_does_not_automatically_trigger_intervention(
    policy,
):
    """DARA must condition divergence on decision validity."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    result = policy.evaluate_capacity(
        decision_id="SCI-001",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.relevant_divergence_count == 1
    assert result.authority == AuthorityState.ALLOW


def test_same_divergence_can_produce_different_authority(policy):
    """Decision requirement must influence the assurance result."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=7.0,
    )

    valid_result = policy.evaluate_capacity(
        decision_id="SCI-002A",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    invalid_result = policy.evaluate_capacity(
        decision_id="SCI-002B",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=8.0,
    )

    assert valid_result.relevant_divergence_count == 1
    assert invalid_result.relevant_divergence_count == 1

    assert valid_result.authority == AuthorityState.ALLOW
    assert invalid_result.authority == AuthorityState.DEFER


def test_uncertain_evidence_never_authorises_execution(policy):
    """Evidence-quality uncertainty must not silently become ALLOW."""

    for status in (
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ):
        observed_value = (
            None if status == EvidenceStatus.MISSING else 10.0
        )

        evidence = make_evidence(
            dependency="vehicle.capacity",
            observed_value=observed_value,
            status=status,
        )

        result = policy.evaluate_capacity(
            decision_id=f"SCI-{status.value}",
            evidence=evidence,
            twin_capacity=10.0,
            required_demand=5.0,
        )

        assert result.authority != AuthorityState.ALLOW


def test_policy_result_preserves_decision_id(policy):
    """Assurance output must remain traceable to the AI decision."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    result = policy.evaluate_capacity(
        decision_id="TRACE-001",
        evidence=evidence,
        twin_capacity=10.0,
        required_demand=5.0,
    )

    assert result.decision_id == "TRACE-001"
