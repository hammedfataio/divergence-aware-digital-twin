"""Tests for the EXP-007 runtime-contract assurance baseline."""

import pytest

from dara_dt.assurance.contract_policy import (
    ContractDecision,
    RuntimeContractPolicy,
)


# ---------------------------------------------------------------------------
# Capacity contract
# ---------------------------------------------------------------------------


def test_capacity_contract_allows_sufficient_capacity() -> None:
    """Capacity contract should allow a physically feasible decision."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_capacity(
        decision_id="capacity_001",
        observed_capacity=7,
        required_demand=5,
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True
    assert result.intervene is False
    assert result.dependency == "vehicle.capacity"


def test_capacity_contract_allows_exact_boundary() -> None:
    """Capacity equal to demand remains physically feasible."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_capacity(
        decision_id="capacity_002",
        observed_capacity=5,
        required_demand=5,
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True
    assert result.intervene is False


def test_capacity_contract_intervenes_below_demand() -> None:
    """Insufficient observed capacity should require intervention."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_capacity(
        decision_id="capacity_003",
        observed_capacity=4,
        required_demand=5,
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.satisfied is False
    assert result.intervene is True


def test_capacity_contract_rejects_non_numeric_capacity() -> None:
    """Capacity evidence must be numeric."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="Observed capacity must be numeric.",
    ):
        policy.evaluate_capacity(
            decision_id="capacity_004",
            observed_capacity="unknown",  # type: ignore[arg-type]
            required_demand=5,
        )


def test_capacity_contract_rejects_boolean_capacity() -> None:
    """Boolean values must not be accepted as numeric capacity."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="Observed capacity must be numeric.",
    ):
        policy.evaluate_capacity(
            decision_id="capacity_005",
            observed_capacity=True,
            required_demand=5,
        )


def test_capacity_contract_rejects_non_numeric_demand() -> None:
    """Demand must be numeric."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="Required demand must be numeric.",
    ):
        policy.evaluate_capacity(
            decision_id="capacity_006",
            observed_capacity=10,
            required_demand="five",  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# Operational-status contract
# ---------------------------------------------------------------------------


def test_status_contract_allows_operational_vehicle() -> None:
    """Required operational state should allow autonomous execution."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_status(
        decision_id="status_001",
        observed_status="operational",
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True
    assert result.intervene is False
    assert result.dependency == "vehicle.status"


def test_status_contract_intervenes_for_broken_vehicle() -> None:
    """Broken-down selected vehicle should violate the contract."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_status(
        decision_id="status_002",
        observed_status="broken_down",
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.satisfied is False
    assert result.intervene is True


def test_status_contract_supports_explicit_required_state() -> None:
    """Status contract should compare against the supplied requirement."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_status(
        decision_id="status_003",
        observed_status="ready",
        required_status="ready",
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True


def test_status_contract_rejects_non_string_observation() -> None:
    """Operational status should use explicit string states."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="Observed operational status must be a string.",
    ):
        policy.evaluate_status(
            decision_id="status_004",
            observed_status=False,  # type: ignore[arg-type]
        )


def test_status_contract_rejects_empty_required_state() -> None:
    """Required status cannot be empty."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="Required operational status must be a non-empty string.",
    ):
        policy.evaluate_status(
            decision_id="status_005",
            observed_status="operational",
            required_status="",
        )


# ---------------------------------------------------------------------------
# Availability contract
# ---------------------------------------------------------------------------


def test_availability_contract_allows_available_vehicle() -> None:
    """Available selected vehicle should satisfy the contract."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_availability(
        decision_id="availability_001",
        observed_available=True,
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True
    assert result.intervene is False
    assert result.dependency == "vehicle.available"


def test_availability_contract_intervenes_when_unavailable() -> None:
    """Unavailable selected vehicle should require intervention."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_availability(
        decision_id="availability_002",
        observed_available=False,
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.satisfied is False
    assert result.intervene is True


def test_availability_contract_supports_false_requirement() -> None:
    """Availability contract should respect an explicit false requirement."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_availability(
        decision_id="availability_003",
        observed_available=False,
        required_available=False,
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True


def test_availability_contract_rejects_non_boolean_observation() -> None:
    """Availability evidence must be boolean."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="Observed availability must be boolean.",
    ):
        policy.evaluate_availability(
            decision_id="availability_004",
            observed_available="yes",  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# Location contract
# ---------------------------------------------------------------------------


def test_location_contract_allows_permitted_location() -> None:
    """Vehicle inside the permitted set should satisfy the contract."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location(
        decision_id="location_001",
        observed_location="depot",
        permitted_locations={"depot", "near_depot"},
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True
    assert result.intervene is False
    assert result.dependency == "vehicle.location"


def test_location_contract_allows_alternative_permitted_location() -> None:
    """A different but permitted physical location should remain valid."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location(
        decision_id="location_002",
        observed_location="near_depot",
        permitted_locations={"depot", "near_depot"},
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True


def test_location_contract_intervenes_outside_permitted_set() -> None:
    """Incompatible physical location should violate the contract."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location(
        decision_id="location_003",
        observed_location="remote_site",
        permitted_locations={"depot", "near_depot"},
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.satisfied is False
    assert result.intervene is True


def test_location_contract_rejects_empty_permitted_set() -> None:
    """Location contract requires an explicit compatibility rule."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="At least one permitted dispatch location is required.",
    ):
        policy.evaluate_location(
            decision_id="location_004",
            observed_location="depot",
            permitted_locations=set(),
        )


def test_location_contract_rejects_non_string_location() -> None:
    """Location evidence must use string identifiers."""

    policy = RuntimeContractPolicy()

    with pytest.raises(
        ValueError,
        match="Observed location must be a string.",
    ):
        policy.evaluate_location(
            decision_id="location_005",
            observed_location=123,  # type: ignore[arg-type]
            permitted_locations={"depot"},
        )


# ---------------------------------------------------------------------------
# Combined location / availability contract
# ---------------------------------------------------------------------------


def test_combined_contract_allows_valid_dispatch() -> None:
    """Both location and availability must satisfy the contract."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location_availability(
        decision_id="combined_001",
        observed_location="near_depot",
        observed_available=True,
        permitted_locations={"depot", "near_depot"},
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.satisfied is True
    assert result.intervene is False
    assert result.dependency == "vehicle.location_availability"


def test_combined_contract_intervenes_for_bad_location() -> None:
    """Bad location should invalidate the combined contract."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location_availability(
        decision_id="combined_002",
        observed_location="remote_site",
        observed_available=True,
        permitted_locations={"depot", "near_depot"},
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.satisfied is False
    assert result.intervene is True
    assert "location" in result.reason


def test_combined_contract_intervenes_when_unavailable() -> None:
    """Unavailability should invalidate the combined contract."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location_availability(
        decision_id="combined_003",
        observed_location="depot",
        observed_available=False,
        permitted_locations={"depot", "near_depot"},
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.satisfied is False
    assert result.intervene is True
    assert "availability" in result.reason


def test_combined_contract_reports_both_failed_conditions() -> None:
    """Both contract failures should remain visible in the result."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location_availability(
        decision_id="combined_004",
        observed_location="remote_site",
        observed_available=False,
        permitted_locations={"depot", "near_depot"},
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.satisfied is False
    assert "location" in result.reason
    assert "availability" in result.reason


def test_combined_contract_records_observed_runtime_state() -> None:
    """Contract result should preserve the evidence used for its decision."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_location_availability(
        decision_id="combined_005",
        observed_location="depot",
        observed_available=True,
        permitted_locations={"depot", "near_depot"},
    )

    assert result.observed_value == {
        "location": "depot",
        "available": True,
    }

    assert result.required_value == {
        "permitted_locations": ("depot", "near_depot"),
        "required_available": True,
    }


# ---------------------------------------------------------------------------
# Result semantics
# ---------------------------------------------------------------------------


def test_allow_result_does_not_request_intervention() -> None:
    """ALLOW should map consistently to no intervention."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_capacity(
        decision_id="result_001",
        observed_capacity=10,
        required_demand=5,
    )

    assert result.decision == ContractDecision.ALLOW
    assert result.intervene is False


def test_intervene_result_requests_intervention() -> None:
    """INTERVENE should map consistently to runtime intervention."""

    policy = RuntimeContractPolicy()

    result = policy.evaluate_capacity(
        decision_id="result_002",
        observed_capacity=2,
        required_demand=5,
    )

    assert result.decision == ContractDecision.INTERVENE
    assert result.intervene is True
