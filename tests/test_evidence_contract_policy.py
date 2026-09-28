"""Tests for the evidence-aware runtime-contract baseline."""

import pytest

from dara_dt.assurance.evidence_contract_policy import (
    EvidenceAwareRuntimeContractPolicy,
    EvidenceContractState,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


@pytest.fixture
def policy() -> EvidenceAwareRuntimeContractPolicy:
    """Return a fresh evidence-aware contract policy."""

    return EvidenceAwareRuntimeContractPolicy()


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
        observed_at=10.0,
        confidence=1.0,
    )


# ---------------------------------------------------------------------------
# Capacity
# ---------------------------------------------------------------------------


def test_capacity_contract_allows_sufficient_available_evidence(policy):
    """Reliable evidence satisfying capacity must preserve autonomy."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    result = policy.evaluate_capacity(
        decision_id="D-001",
        evidence=evidence,
        required_demand=5.0,
    )

    assert result.decision_id == "D-001"
    assert result.authority == AuthorityState.ALLOW
    assert result.state == EvidenceContractState.SATISFIED
    assert result.evidence_status == EvidenceStatus.AVAILABLE
    assert not result.intervene
    assert result.autonomous_execution_allowed


def test_capacity_contract_restricts_insufficient_available_evidence(policy):
    """Reliable evidence violating capacity must restrict execution."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=4.0,
    )

    result = policy.evaluate_capacity(
        decision_id="D-002",
        evidence=evidence,
        required_demand=5.0,
    )

    assert result.decision_id == "D-002"
    assert result.authority == AuthorityState.RESTRICT
    assert result.state == EvidenceContractState.VIOLATED
    assert result.intervene
    assert not result.autonomous_execution_allowed


def test_capacity_contract_allows_exact_boundary(policy):
    """Capacity equal to demand remains contract-satisfying."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=5.0,
    )

    result = policy.evaluate_capacity(
        decision_id="D-003",
        evidence=evidence,
        required_demand=5.0,
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.state == EvidenceContractState.SATISFIED


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_capacity_contract_defers_uncertain_evidence(
    policy,
    status,
):
    """Uncertain capacity evidence must not authorise execution."""

    observed_value = None if status == EvidenceStatus.MISSING else 8.0

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=observed_value,
        status=status,
    )

    result = policy.evaluate_capacity(
        decision_id="D-004",
        evidence=evidence,
        required_demand=5.0,
    )

    assert result.decision_id == "D-004"
    assert result.authority == AuthorityState.DEFER
    assert result.state == EvidenceContractState.UNCERTAIN
    assert result.evidence_status == status
    assert result.intervene
    assert not result.autonomous_execution_allowed


# ---------------------------------------------------------------------------
# Operational status
# ---------------------------------------------------------------------------


def test_status_contract_allows_operational_available_evidence(policy):
    """Reliable operational evidence must satisfy the status contract."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="operational",
    )

    result = policy.evaluate_status(
        decision_id="D-005",
        evidence=evidence,
    )

    assert result.decision_id == "D-005"
    assert result.authority == AuthorityState.ALLOW
    assert result.state == EvidenceContractState.SATISFIED
    assert not result.intervene


def test_status_contract_restricts_broken_vehicle(policy):
    """Reliable broken-down evidence must violate the status contract."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="broken_down",
    )

    result = policy.evaluate_status(
        decision_id="D-006",
        evidence=evidence,
    )

    assert result.authority == AuthorityState.RESTRICT
    assert result.state == EvidenceContractState.VIOLATED
    assert result.intervene


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_status_contract_defers_uncertain_evidence(
    policy,
    status,
):
    """Uncertain operational-status evidence must produce DEFER."""

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
        decision_id="D-007",
        evidence=evidence,
    )

    assert result.authority == AuthorityState.DEFER
    assert result.state == EvidenceContractState.UNCERTAIN
    assert result.evidence_status == status


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def test_availability_contract_allows_available_vehicle(policy):
    """Reliable True availability must satisfy the contract."""

    evidence = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    result = policy.evaluate_availability(
        decision_id="D-008",
        evidence=evidence,
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.state == EvidenceContractState.SATISFIED


def test_availability_contract_restricts_unavailable_vehicle(policy):
    """Reliable False availability must violate the contract."""

    evidence = make_evidence(
        dependency="vehicle.available",
        observed_value=False,
    )

    result = policy.evaluate_availability(
        decision_id="D-009",
        evidence=evidence,
    )

    assert result.authority == AuthorityState.RESTRICT
    assert result.state == EvidenceContractState.VIOLATED


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_availability_contract_defers_uncertain_evidence(
    policy,
    status,
):
    """Uncertain availability evidence must produce DEFER."""

    observed_value = None if status == EvidenceStatus.MISSING else True

    evidence = make_evidence(
        dependency="vehicle.available",
        observed_value=observed_value,
        status=status,
    )

    result = policy.evaluate_availability(
        decision_id="D-010",
        evidence=evidence,
    )

    assert result.authority == AuthorityState.DEFER
    assert result.state == EvidenceContractState.UNCERTAIN


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------


def test_location_contract_allows_permitted_location(policy):
    """Reliable evidence inside the permitted set must allow execution."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="near_depot",
    )

    result = policy.evaluate_location(
        decision_id="D-011",
        evidence=evidence,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.state == EvidenceContractState.SATISFIED


def test_location_contract_restricts_remote_location(policy):
    """Reliable evidence outside the permitted set must restrict."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="remote_site",
    )

    result = policy.evaluate_location(
        decision_id="D-012",
        evidence=evidence,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.RESTRICT
    assert result.state == EvidenceContractState.VIOLATED


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_location_contract_defers_uncertain_evidence(
    policy,
    status,
):
    """Uncertain location evidence must produce DEFER."""

    observed_value = (
        None
        if status == EvidenceStatus.MISSING
        else "depot"
    )

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value=observed_value,
        status=status,
    )

    result = policy.evaluate_location(
        decision_id="D-013",
        evidence=evidence,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.state == EvidenceContractState.UNCERTAIN


# ---------------------------------------------------------------------------
# Combined location + availability
# ---------------------------------------------------------------------------


def test_combined_contract_allows_valid_dispatch(policy):
    """Reliable valid location and availability must preserve autonomy."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    result = policy.evaluate_location_availability(
        decision_id="D-014",
        location_evidence=location,
        availability_evidence=availability,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.decision_id == "D-014"
    assert result.authority == AuthorityState.ALLOW
    assert result.state == EvidenceContractState.SATISFIED


def test_combined_contract_restricts_invalid_location(policy):
    """Reliable remote location must violate the dispatch contract."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="remote_site",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    result = policy.evaluate_location_availability(
        decision_id="D-015",
        location_evidence=location,
        availability_evidence=availability,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.RESTRICT
    assert result.state == EvidenceContractState.VIOLATED


def test_combined_contract_restricts_unavailable_vehicle(policy):
    """Reliable unavailable state must violate the dispatch contract."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=False,
    )

    result = policy.evaluate_location_availability(
        decision_id="D-016",
        location_evidence=location,
        availability_evidence=availability,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.RESTRICT
    assert result.state == EvidenceContractState.VIOLATED


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_combined_contract_defers_uncertain_location(
    policy,
    status,
):
    """Uncertain location must defer even when availability is reliable."""

    location_value = (
        None
        if status == EvidenceStatus.MISSING
        else "depot"
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
        decision_id="D-017",
        location_evidence=location,
        availability_evidence=availability,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.state == EvidenceContractState.UNCERTAIN
    assert result.evidence_status == status


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ],
)
def test_combined_contract_defers_uncertain_availability(
    policy,
    status,
):
    """Uncertain availability must defer even when location is reliable."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    availability_value = (
        None
        if status == EvidenceStatus.MISSING
        else True
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=availability_value,
        status=status,
    )

    result = policy.evaluate_location_availability(
        decision_id="D-018",
        location_evidence=location,
        availability_evidence=availability,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.state == EvidenceContractState.UNCERTAIN
    assert result.evidence_status == status


def test_combined_status_prioritises_missing(policy):
    """Missing evidence is the strongest combined uncertainty state."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value=None,
        status=EvidenceStatus.MISSING,
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
        status=EvidenceStatus.STALE,
    )

    result = policy.evaluate_location_availability(
        decision_id="D-019",
        location_evidence=location,
        availability_evidence=availability,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.evidence_status == EvidenceStatus.MISSING


def test_combined_status_prioritises_conflict_over_stale(policy):
    """Conflict takes precedence over staleness when neither is missing."""

    location = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
        status=EvidenceStatus.CONFLICTING,
    )

    availability = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
        status=EvidenceStatus.STALE,
    )

    result = policy.evaluate_location_availability(
        decision_id="D-020",
        location_evidence=location,
        availability_evidence=availability,
        permitted_locations=("depot", "near_depot"),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.evidence_status == EvidenceStatus.CONFLICTING


# ---------------------------------------------------------------------------
# Integrity and validation
# ---------------------------------------------------------------------------


def test_result_preserves_decision_id(policy):
    """The comparator must preserve the evaluated decision identifier."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    result = policy.evaluate_capacity(
        decision_id="DECISION-XYZ",
        evidence=evidence,
        required_demand=5.0,
    )

    assert result.decision_id == "DECISION-XYZ"


def test_wrong_capacity_dependency_is_rejected(policy):
    """Capacity contracts must reject evidence for another dependency."""

    evidence = make_evidence(
        dependency="vehicle.status",
        observed_value="operational",
    )

    with pytest.raises(ValueError):
        policy.evaluate_capacity(
            decision_id="D-021",
            evidence=evidence,
            required_demand=5.0,
        )


def test_wrong_status_dependency_is_rejected(policy):
    """Status contracts must reject capacity evidence."""

    evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    with pytest.raises(ValueError):
        policy.evaluate_status(
            decision_id="D-022",
            evidence=evidence,
        )


def test_wrong_location_dependency_is_rejected(policy):
    """Location contracts must reject evidence for another dependency."""

    evidence = make_evidence(
        dependency="vehicle.available",
        observed_value=True,
    )

    with pytest.raises(ValueError):
        policy.evaluate_location(
            decision_id="D-023",
            evidence=evidence,
            permitted_locations=("depot",),
        )


def test_empty_permitted_location_set_is_rejected(policy):
    """A location contract requires at least one permitted location."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    with pytest.raises(ValueError):
        policy.evaluate_location(
            decision_id="D-024",
            evidence=evidence,
            permitted_locations=(),
        )


def test_non_string_permitted_location_is_rejected(policy):
    """Permitted locations must be represented by strings."""

    evidence = make_evidence(
        dependency="vehicle.location",
        observed_value="depot",
    )

    with pytest.raises(ValueError):
        policy.evaluate_location(
            decision_id="D-025",
            evidence=evidence,
            permitted_locations=("depot", 123),
        )


def test_result_intervention_property_matches_authority(policy):
    """Intervention property must correspond to autonomous authority."""

    valid_evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
    )

    invalid_evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=4.0,
    )

    uncertain_evidence = make_evidence(
        dependency="vehicle.capacity",
        observed_value=8.0,
        status=EvidenceStatus.STALE,
    )

    allow_result = policy.evaluate_capacity(
        decision_id="D-026",
        evidence=valid_evidence,
        required_demand=5.0,
    )

    restrict_result = policy.evaluate_capacity(
        decision_id="D-027",
        evidence=invalid_evidence,
        required_demand=5.0,
    )

    defer_result = policy.evaluate_capacity(
        decision_id="D-028",
        evidence=uncertain_evidence,
        required_demand=5.0,
    )

    assert allow_result.intervene is False
    assert allow_result.autonomous_execution_allowed is True

    assert restrict_result.intervene is True
    assert restrict_result.autonomous_execution_allowed is False

    assert defer_result.intervene is True
    assert defer_result.autonomous_execution_allowed is False
