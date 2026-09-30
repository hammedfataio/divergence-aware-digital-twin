"""Tests for the EXP-010 propagation-aware DARA-DT assurance policy."""

from __future__ import annotations

import pytest

from dara_dt.assurance.composed_contract_policy import (
    ContractEvaluation,
    DependencyAwareComposedContractPolicy,
    DependencyRequirement,
    exp010_d2_requirements,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.assurance.propagation_policy import (
    PropagationAwareAssurancePolicy,
    PropagationEvaluation,
    contract_evaluation_to_propagation,
)
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence
from dara_dt.propagation.analyser import (
    DivergencePropagationAnalyser,
    PropagationAnalysis,
    build_exp010_propagation_analyser,
)
from dara_dt.propagation.model import (
    DivergenceOrigin,
    build_exp010_decision_chain,
)


def make_evidence(
    dependency: str,
    value: object,
    *,
    status: EvidenceStatus = EvidenceStatus.AVAILABLE,
    timestamp: float = 1.0,
) -> RuntimeEvidence:
    """Create runtime evidence using the project evidence API."""

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
    """Create fully satisfying evidence for all requirements."""

    return {
        requirement.dependency: make_evidence(
            requirement.dependency,
            requirement.expected_value,
        )
        for requirement in requirements
    }


def build_analyser() -> DivergencePropagationAnalyser:
    """Return the frozen EXP-010 propagation analyser."""

    return build_exp010_propagation_analyser(
        build_exp010_decision_chain()
    )


def status_propagation_to_d2() -> PropagationAnalysis:
    """Create Vehicle A status propagation analysis for D2."""

    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    return analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )


def capacity_non_propagation_to_d2() -> PropagationAnalysis:
    """Create an F2-style upstream non-propagating analysis."""

    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="capacity",
        physical_value=7,
        twin_value=10,
    )

    return analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )


def synchronised_analysis_for_d2() -> PropagationAnalysis:
    """Create analysis where physical and Twin states agree."""

    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="operational",
        twin_value="operational",
    )

    return analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )


def test_synchronised_valid_state_allows() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=synchronised_analysis_for_d2(),
    )

    assert result.assurance.authority is AuthorityState.ALLOW
    assert not result.intervene
    assert result.violated_dependencies == frozenset()
    assert result.uncertain_dependencies == frozenset()


def test_known_requirement_violation_restricts() -> None:
    policy = PropagationAwareAssurancePolicy()

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
        propagation=status_propagation_to_d2(),
    )

    assert result.assurance.authority is AuthorityState.RESTRICT
    assert result.intervene

    assert "recovery_resource_available" in (
        result.violated_dependencies
    )


def test_propagation_relevant_stale_evidence_defers() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["recovery_resource_available"] = make_evidence(
        "recovery_resource_available",
        True,
        status=EvidenceStatus.STALE,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert result.assurance.authority is AuthorityState.DEFER

    assert "recovery_resource_available" in (
        result.uncertain_dependencies
    )


def test_propagation_relevant_missing_evidence_defers() -> None:
    policy = PropagationAwareAssurancePolicy()

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
        propagation=status_propagation_to_d2(),
    )

    assert result.assurance.authority is AuthorityState.DEFER

    assert "recovery_resource_available" in (
        result.uncertain_dependencies
    )


def test_propagation_relevant_conflicting_evidence_defers() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["recovery_resource_available"] = make_evidence(
        "recovery_resource_available",
        True,
        status=EvidenceStatus.CONFLICTING,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert result.assurance.authority is AuthorityState.DEFER


def test_absent_propagation_relevant_evidence_defers() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    del evidence["recovery_resource_available"]

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert result.assurance.authority is AuthorityState.DEFER

    assert "recovery_resource_available" in (
        result.uncertain_dependencies
    )


def test_non_propagating_divergence_does_not_automatically_intervene() -> None:
    """F2-style divergence must not collapse into divergence=unsafe."""

    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=capacity_non_propagation_to_d2(),
    )

    assert not result.propagation.is_propagating
    assert result.assurance.authority is AuthorityState.ALLOW
    assert not result.intervene


def test_propagation_alone_does_not_force_intervention() -> None:
    """Reliable satisfying evidence may preserve autonomous authority."""

    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert result.propagation.is_propagating
    assert result.assurance.authority is AuthorityState.ALLOW


def test_unrelated_uncertainty_does_not_force_dara_defer() -> None:
    """P4 conditions uncertainty on propagation relevance."""

    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["vehicle_B.capacity_sufficient"] = make_evidence(
        "vehicle_B.capacity_sufficient",
        True,
        status=EvidenceStatus.STALE,
    )

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert (
        "vehicle_B.capacity_sufficient"
        not in result.propagation_affected_dependencies
    )

    assert result.assurance.authority is AuthorityState.ALLOW


def test_unrelated_known_violation_still_restricts() -> None:
    """A known required violation remains actionable even if not propagated."""

    policy = PropagationAwareAssurancePolicy()

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
        propagation=status_propagation_to_d2(),
    )

    assert result.assurance.authority is AuthorityState.RESTRICT
    assert "vehicle_B.status" in result.violated_dependencies


def test_propagation_analysis_must_match_pending_decision() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    wrong_analysis = analyser.analyse(
        origin=origin,
        pending_decision_id="D3",
    )

    with pytest.raises(
        ValueError,
        match="does not correspond",
    ):
        policy.evaluate(
            decision_id="D2",
            requirements=requirements,
            evidence=evidence,
            propagation=wrong_analysis,
        )


def test_propagation_affected_dependencies_are_reported() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert "recovery_resource_available" in (
        result.propagation_affected_dependencies
    )

    assert "vehicle_C.available" in (
        result.propagation_affected_dependencies
    )


def test_p3_and_p4_receive_identical_evidence_mapping() -> None:
    """Core EXP-010 fairness invariant."""

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    p3 = DependencyAwareComposedContractPolicy()
    p4 = PropagationAwareAssurancePolicy()

    p3_result = p3.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    p4_result = p4.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert set(evidence) == {
        requirement.dependency
        for requirement in requirements
    }

    assert p3_result.assurance.authority is AuthorityState.ALLOW
    assert p4_result.assurance.authority is AuthorityState.ALLOW


def test_p3_and_p4_agree_on_known_shared_violation() -> None:
    """Both policies should detect an observable contract violation."""

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["recovery_resource_available"] = make_evidence(
        "recovery_resource_available",
        False,
    )

    p3 = DependencyAwareComposedContractPolicy()
    p4 = PropagationAwareAssurancePolicy()

    p3_result = p3.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    p4_result = p4.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert p3_result.assurance.authority is AuthorityState.RESTRICT
    assert p4_result.assurance.authority is AuthorityState.RESTRICT


def test_p3_and_p4_can_differ_on_irrelevant_uncertainty() -> None:
    """The experiment is allowed to expose semantic differences.

    P3 treats uncertainty in any required contract dependency as grounds
    for deferral. P4 conditions uncertain evidence on the observed
    propagation path.
    """

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    evidence["vehicle_B.capacity_sufficient"] = make_evidence(
        "vehicle_B.capacity_sufficient",
        True,
        status=EvidenceStatus.STALE,
    )

    p3 = DependencyAwareComposedContractPolicy()
    p4 = PropagationAwareAssurancePolicy()

    p3_result = p3.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
    )

    p4_result = p4.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=status_propagation_to_d2(),
    )

    assert p3_result.assurance.authority is AuthorityState.DEFER
    assert p4_result.assurance.authority is AuthorityState.ALLOW


def test_no_propagation_with_satisfying_evidence_allows() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=synchronised_analysis_for_d2(),
    )

    assert result.assurance.authority is AuthorityState.ALLOW


def test_relevant_divergence_count_reflects_affected_dependencies() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)

    propagation = status_propagation_to_d2()

    result = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=propagation,
    )

    assert (
        result.assurance.relevant_divergence_count
        == len(propagation.affected_dependencies)
    )


def test_contract_evaluation_translation_satisfied() -> None:
    assert (
        contract_evaluation_to_propagation(
            ContractEvaluation.SATISFIED
        )
        is PropagationEvaluation.SATISFIED
    )


def test_contract_evaluation_translation_violated() -> None:
    assert (
        contract_evaluation_to_propagation(
            ContractEvaluation.VIOLATED
        )
        is PropagationEvaluation.VIOLATED
    )


def test_contract_evaluation_translation_uncertain() -> None:
    assert (
        contract_evaluation_to_propagation(
            ContractEvaluation.UNCERTAIN
        )
        is PropagationEvaluation.UNCERTAIN
    )


def test_policy_result_is_deterministic() -> None:
    policy = PropagationAwareAssurancePolicy()

    requirements = exp010_d2_requirements()
    evidence = evidence_for_requirements(requirements)
    propagation = status_propagation_to_d2()

    first = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=propagation,
    )

    second = policy.evaluate(
        decision_id="D2",
        requirements=requirements,
        evidence=evidence,
        propagation=propagation,
    )

    assert first == second
