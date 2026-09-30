"""Tests for the strong EXP-010 composed runtime-contract comparator."""

from __future__ import annotations

import pytest

from dara_dt.assurance.composed_contract_policy import (
    ContractEvaluation,
    DependencyAwareComposedContractPolicy,
    DependencyRequirement,
    exp010_d1_requirements,
    exp010_d2_requirements,
    exp010_d3_requirements,
    exp010_requirements_for_decision,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


def make_evidence(
    dependency: str,
    value: object,
    *,
    status: EvidenceStatus = EvidenceStatus.AVAILABLE,
    timestamp: float = 1.0,
) -> RuntimeEvidence:
    """Create runtime evidence using the project's evidence API."""

    observed_value = (
        None
        if status is EvidenceStatus.MISSING
        else value
    )

    return RuntimeEvidence(
        source="exp010_test",
        dependency=dependency,
        observed_value=observed_value,
        timestamp=timestamp,
        status=status,
    )


def evidence_for_requirements(
    requirements: tuple[DependencyRequirement, ...],
) -> dict[str, RuntimeEvidence]:
    """Create fully satisfying evidence for a contract."""

    return {
        requirement.dependency: make_evidence(
            requirement.dependency,
            requirement.expected_value,
        )
        for requirement in requirements
    }


def test_satisfied_contract_allows_autonomy() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.ALLOW
    assert not result.intervene
    assert result.violated_dependencies == frozenset()
    assert result.uncertain_dependencies == frozenset()

    assert result.satisfied_dependencies == frozenset(
        requirement.dependency
        for requirement in requirements
    )


def test_known_contract_violation_restricts_autonomy() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["recovery_resource_available"] = make_evidence(
        "recovery_resource_available",
        False,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT
    assert result.intervene

    assert result.violated_dependencies == frozenset(
        {"recovery_resource_available"}
    )


def test_missing_required_evidence_defers() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["recovery_resource_available"] = make_evidence(
        "recovery_resource_available",
        True,
        status=EvidenceStatus.MISSING,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.DEFER
    assert result.intervene

    assert result.uncertain_dependencies == frozenset(
        {"recovery_resource_available"}
    )


def test_stale_required_evidence_defers() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["recovery_timing_valid"] = make_evidence(
        "recovery_timing_valid",
        True,
        status=EvidenceStatus.STALE,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.DEFER

    assert result.uncertain_dependencies == frozenset(
        {"recovery_timing_valid"}
    )


def test_conflicting_required_evidence_defers() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["upstream_assignment_assumptions_valid"] = make_evidence(
        "upstream_assignment_assumptions_valid",
        True,
        status=EvidenceStatus.CONFLICTING,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.DEFER

    assert result.uncertain_dependencies == frozenset(
        {"upstream_assignment_assumptions_valid"}
    )


def test_absent_required_evidence_defers() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    del evidence["vehicle_C.available"]

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.DEFER

    assert result.uncertain_dependencies == frozenset(
        {"vehicle_C.available"}
    )


def test_violation_takes_precedence_over_uncertainty() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["recovery_resource_available"] = make_evidence(
        "recovery_resource_available",
        False,
    )

    evidence["recovery_timing_valid"] = make_evidence(
        "recovery_timing_valid",
        True,
        status=EvidenceStatus.STALE,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT

    assert result.violated_dependencies == frozenset(
        {"recovery_resource_available"}
    )

    assert result.uncertain_dependencies == frozenset(
        {"recovery_timing_valid"}
    )


def test_direct_vehicle_b_violation_is_detected() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["vehicle_B.status"] = make_evidence(
        "vehicle_B.status",
        "failed",
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT
    assert "vehicle_B.status" in result.violated_dependencies


def test_cross_entity_vehicle_c_violation_is_detected() -> None:
    """The strong comparator must be allowed to inspect Vehicle C."""

    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["vehicle_C.available"] = make_evidence(
        "vehicle_C.available",
        False,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT

    assert result.violated_dependencies == frozenset(
        {"vehicle_C.available"}
    )


def test_upstream_assumption_violation_is_detected() -> None:
    """The comparator must not be limited to local Vehicle B state."""

    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["upstream_assignment_assumptions_valid"] = make_evidence(
        "upstream_assignment_assumptions_valid",
        False,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT

    assert "upstream_assignment_assumptions_valid" in (
        result.violated_dependencies
    )


def test_downstream_assignment_violation_is_detected() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["vehicle_B.assignment_valid"] = make_evidence(
        "vehicle_B.assignment_valid",
        False,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT

    assert "vehicle_B.assignment_valid" in (
        result.violated_dependencies
    )


def test_multiple_violations_are_reported() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["vehicle_C.available"] = make_evidence(
        "vehicle_C.available",
        False,
    )

    evidence["recovery_resource_available"] = make_evidence(
        "recovery_resource_available",
        False,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT

    assert result.violated_dependencies == frozenset(
        {
            "vehicle_C.available",
            "recovery_resource_available",
        }
    )


def test_available_but_wrong_value_is_violation_not_uncertainty() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirement = DependencyRequirement(
        dependency="system.ready",
        expected_value=True,
        description="System must be ready.",
    )

    evidence = {
        "system.ready": make_evidence(
            "system.ready",
            False,
            status=EvidenceStatus.AVAILABLE,
        )
    }

    result = policy.evaluate(
        decision_id="D-test",
        requirements=(requirement,),
        evidence=evidence,
    )

    assert result.assurance.authority is AuthorityState.RESTRICT
    assert result.violated_dependencies == frozenset({"system.ready"})
    assert result.uncertain_dependencies == frozenset()


def test_evidence_dependency_mismatch_is_rejected() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirement = DependencyRequirement(
        dependency="system.ready",
        expected_value=True,
        description="System must be ready.",
    )

    evidence = {
        "system.ready": make_evidence(
            "different.dependency",
            True,
        )
    }

    with pytest.raises(
        ValueError,
        match="does not match contract requirement",
    ):
        policy.evaluate(
            decision_id="D-test",
            requirements=(requirement,),
            evidence=evidence,
        )


def test_empty_contract_allows() -> None:
    policy = DependencyAwareComposedContractPolicy()

    result = policy.evaluate(
        decision_id="D-test",
        requirements=(),
        evidence={},
    )

    assert result.assurance.authority is AuthorityState.ALLOW
    assert not result.intervene


def test_d1_contract_contains_expected_requirements() -> None:
    requirements = exp010_d1_requirements()

    dependencies = {
        requirement.dependency
        for requirement in requirements
    }

    assert dependencies == {
        "vehicle_A.status",
        "vehicle_A.available",
        "vehicle_A.capacity_sufficient",
        "order_O1.waiting",
    }


def test_d2_contract_contains_strong_cross_decision_requirements() -> None:
    """EXP-010 P3 must be a genuinely strong comparator."""

    requirements = exp010_d2_requirements()

    dependencies = {
        requirement.dependency
        for requirement in requirements
    }

    assert {
        "vehicle_B.status",
        "vehicle_B.available",
        "vehicle_B.capacity_sufficient",
        "order_O2.waiting",
        "order_O2.deadline_valid",
        "recovery_resource_available",
        "recovery_timing_valid",
        "upstream_assignment_assumptions_valid",
        "vehicle_C.available",
        "vehicle_B.assignment_valid",
    } == dependencies


def test_d3_contract_contains_recovery_requirements() -> None:
    requirements = exp010_d3_requirements()

    dependencies = {
        requirement.dependency
        for requirement in requirements
    }

    assert dependencies == {
        "vehicle_C.status",
        "vehicle_C.available",
        "vehicle_C.capacity_sufficient",
        "recovery_demand_supported",
        "upstream_failure_state_known",
    }


def test_requirement_lookup_returns_d1_contract() -> None:
    assert (
        exp010_requirements_for_decision("D1")
        == exp010_d1_requirements()
    )


def test_requirement_lookup_returns_d2_contract() -> None:
    assert (
        exp010_requirements_for_decision("D2")
        == exp010_d2_requirements()
    )


def test_requirement_lookup_returns_d3_contract() -> None:
    assert (
        exp010_requirements_for_decision("D3")
        == exp010_d3_requirements()
    )


def test_unknown_exp010_decision_is_rejected() -> None:
    with pytest.raises(
        KeyError,
        match="Unknown EXP-010 decision",
    ):
        exp010_requirements_for_decision("D99")


def test_deterministic_contract_result() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    first = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    second = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    assert first == second


def test_evaluation_details_record_satisfied_requirement() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirement = DependencyRequirement(
        dependency="system.ready",
        expected_value=True,
        description="System must be ready.",
    )

    evidence = {
        "system.ready": make_evidence(
            "system.ready",
            True,
        )
    }

    result = policy.evaluate(
        decision_id="D-test",
        requirements=(requirement,),
        evidence=evidence,
    )

    assert len(result.evaluations) == 1

    evaluation = result.evaluations[0]

    assert (
        evaluation.evaluation
        is ContractEvaluation.SATISFIED
    )

    assert evaluation.evidence is not None
    assert evaluation.evidence.observed_value is True


def test_evaluation_details_record_uncertain_requirement() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirement = DependencyRequirement(
        dependency="system.ready",
        expected_value=True,
        description="System must be ready.",
    )

    result = policy.evaluate(
        decision_id="D-test",
        requirements=(requirement,),
        evidence={},
    )

    evaluation = result.evaluations[0]

    assert (
        evaluation.evaluation
        is ContractEvaluation.UNCERTAIN
    )

    assert evaluation.evidence is None


def test_evaluation_details_record_violated_requirement() -> None:
    policy = DependencyAwareComposedContractPolicy()

    requirement = DependencyRequirement(
        dependency="system.ready",
        expected_value=True,
        description="System must be ready.",
    )

    evidence = {
        "system.ready": make_evidence(
            "system.ready",
            False,
        )
    }

    result = policy.evaluate(
        decision_id="D-test",
        requirements=(requirement,),
        evidence=evidence,
    )

    evaluation = result.evaluations[0]

    assert (
        evaluation.evaluation
        is ContractEvaluation.VIOLATED
    )

    assert evaluation.evidence is not None
    assert evaluation.evidence.observed_value is False
