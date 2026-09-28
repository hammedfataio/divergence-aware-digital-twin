"""Tests for the EXP-009 global evidence-uncertainty baseline."""

from dara_dt.assurance.global_evidence_policy import (
    GlobalEvidenceUncertaintyPolicy,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.evidence.model import (
    EvidenceStatus,
    RuntimeEvidence,
)


def _evidence(
    dependency: str,
    value: object,
    status: EvidenceStatus = EvidenceStatus.AVAILABLE,
) -> RuntimeEvidence:
    """Create runtime evidence for policy tests."""

    return RuntimeEvidence(
        source="test_sensor",
        dependency=dependency,
        observed_value=value,
        timestamp=10.0,
        status=status,
    )


def test_global_policy_allows_when_all_evidence_is_available() -> None:
    policy = GlobalEvidenceUncertaintyPolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence("vehicle_2.status", "operational"),
        _evidence("vehicle_8.status", "operational"),
    ]

    result = policy.evaluate(evidence)

    assert result.state == AuthorityState.ALLOW


def test_global_policy_defers_on_stale_evidence() -> None:
    policy = GlobalEvidenceUncertaintyPolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_8.status",
            "operational",
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(evidence)

    assert result.state == AuthorityState.DEFER


def test_global_policy_defers_on_missing_evidence() -> None:
    policy = GlobalEvidenceUncertaintyPolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        RuntimeEvidence(
            source="test_sensor",
            dependency="vehicle_8.status",
            observed_value=None,
            timestamp=10.0,
            status=EvidenceStatus.MISSING,
        ),
    ]

    result = policy.evaluate(evidence)

    assert result.state == AuthorityState.DEFER


def test_global_policy_defers_on_conflicting_evidence() -> None:
    policy = GlobalEvidenceUncertaintyPolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_8.status",
            "maintenance_due",
            EvidenceStatus.CONFLICTING,
        ),
    ]

    result = policy.evaluate(evidence)

    assert result.state == AuthorityState.DEFER


def test_global_policy_reacts_to_irrelevant_uncertainty() -> None:
    """Global policy must not perform decision relevance filtering."""

    policy = GlobalEvidenceUncertaintyPolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_8.status",
            "operational",
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(evidence)

    # Vehicle 8 may be irrelevant to a Vehicle 2 decision, but the global
    # baseline intentionally reacts to uncertainty anywhere in the system.
    assert result.state == AuthorityState.DEFER


def test_global_policy_defers_if_one_of_many_items_is_uncertain() -> None:
    policy = GlobalEvidenceUncertaintyPolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence("vehicle_2.status", "operational"),
        _evidence("vehicle_8.capacity", 20),
        _evidence(
            "vehicle_9.location",
            "depot_b",
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(evidence)

    assert result.state == AuthorityState.DEFER


def test_global_policy_allows_empty_evidence_collection() -> None:
    """The policy reacts to observed uncertainty, not absence of a collection."""

    policy = GlobalEvidenceUncertaintyPolicy()

    result = policy.evaluate([])

    assert result.state == AuthorityState.ALLOW


def test_global_policy_does_not_require_physical_ground_truth() -> None:
    """The public policy interface must operate only on runtime evidence."""

    policy = GlobalEvidenceUncertaintyPolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
    ]

    result = policy.evaluate(evidence)

    assert result.state == AuthorityState.ALLOW
