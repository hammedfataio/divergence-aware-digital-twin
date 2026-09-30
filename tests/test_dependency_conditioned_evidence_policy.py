"""Tests for the EXP-009 decision-dependency-conditioned uncertainty policy.

These tests define the behaviour required to distinguish dependency-level
reasoning from both global evidence uncertainty and simple entity filtering.

The policy must react to uncertainty affecting dependencies required by the
pending decision while ignoring uncertainty outside those dependencies.
"""

from dara_dt.assurance.dependency_conditioned_evidence_policy import (
    DependencyConditionedEvidencePolicy,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


def _evidence(
    dependency: str,
    value: object,
    status: EvidenceStatus = EvidenceStatus.AVAILABLE,
) -> RuntimeEvidence:
    """Create runtime evidence for dependency-conditioned policy tests."""

    return RuntimeEvidence(
        source="test_sensor",
        dependency=dependency,
        observed_value=value,
        timestamp=10.0,
        status=status,
    )


def _missing(dependency: str) -> RuntimeEvidence:
    """Create missing runtime evidence."""

    return RuntimeEvidence(
        source="test_sensor",
        dependency=dependency,
        observed_value=None,
        timestamp=10.0,
        status=EvidenceStatus.MISSING,
    )


def test_policy_allows_when_required_dependency_is_available() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.ALLOW


def test_policy_defers_when_required_dependency_is_stale() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence(
            "vehicle_2.capacity",
            10,
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.DEFER


def test_policy_defers_when_required_dependency_is_missing() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _missing("vehicle_2.capacity"),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.DEFER


def test_policy_defers_when_required_dependency_is_conflicting() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence(
            "vehicle_2.capacity",
            10,
            EvidenceStatus.CONFLICTING,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.DEFER


def test_policy_ignores_uncertainty_on_other_entity() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_8.status",
            "operational",
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.ALLOW


def test_policy_ignores_same_entity_irrelevant_dependency() -> None:
    """This is the key distinction from the entity-filtered baseline."""

    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_2.status",
            "operational",
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.ALLOW


def test_policy_defers_if_one_of_multiple_required_dependencies_is_uncertain() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.location", "depot"),
        _evidence(
            "vehicle_2.available",
            True,
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={
            "vehicle_2.location",
            "vehicle_2.available",
        },
    )

    assert result.authority == AuthorityState.DEFER


def test_policy_allows_when_all_multiple_required_dependencies_are_available() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.location", "depot"),
        _evidence("vehicle_2.available", True),
        _evidence(
            "vehicle_2.status",
            "operational",
            EvidenceStatus.CONFLICTING,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={
            "vehicle_2.location",
            "vehicle_2.available",
        },
    )

    assert result.authority == AuthorityState.ALLOW


def test_policy_uses_exact_dependency_matching() -> None:
    """vehicle_2.capacity must not accidentally match vehicle_20.capacity."""

    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_20.capacity",
            4,
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.ALLOW


def test_policy_preserves_decision_id() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
        decision_id="decision_exp009_001",
    )

    assert result.decision_id == "decision_exp009_001"


def test_policy_rejects_empty_required_dependencies() -> None:
    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
    ]

    try:
        policy.evaluate(
            evidence=evidence,
            required_dependencies=set(),
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty required_dependencies should raise ValueError"
        )


def test_policy_does_not_require_physical_ground_truth() -> None:
    """Runtime assurance must not receive hidden physical truth."""

    policy = DependencyConditionedEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_8.status",
            "broken_down",
            EvidenceStatus.CONFLICTING,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        required_dependencies={"vehicle_2.capacity"},
    )

    assert result.authority == AuthorityState.ALLOW
