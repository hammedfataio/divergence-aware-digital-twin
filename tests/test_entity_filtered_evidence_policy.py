"""Tests for the EXP-009 entity-filtered evidence-uncertainty baseline."""

from dara_dt.assurance.entity_filtered_evidence_policy import (
    EntityFilteredEvidencePolicy,
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
    """Create runtime evidence for entity-filtered policy tests."""

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


def test_entity_policy_allows_when_selected_entity_evidence_is_available() -> None:
    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence("vehicle_2.status", "operational"),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.ALLOW


def test_entity_policy_defers_on_selected_entity_stale_evidence() -> None:
    policy = EntityFilteredEvidencePolicy()

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
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.DEFER


def test_entity_policy_defers_on_selected_entity_missing_evidence() -> None:
    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _missing("vehicle_2.status"),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.DEFER


def test_entity_policy_defers_on_selected_entity_conflicting_evidence() -> None:
    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_2.status",
            "maintenance_due",
            EvidenceStatus.CONFLICTING,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.DEFER


def test_entity_policy_ignores_uncertainty_on_other_entity() -> None:
    """Uncertainty outside the selected entity must not trigger intervention."""

    policy = EntityFilteredEvidencePolicy()

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
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.ALLOW


def test_entity_policy_uses_exact_entity_matching() -> None:
    """vehicle_2 must not accidentally match vehicle_20."""

    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence(
            "vehicle_20.status",
            "operational",
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.ALLOW


def test_entity_policy_reacts_to_same_entity_irrelevant_dependency() -> None:
    """P2 filters by entity, not by the pending decision dependency.

    A stale status observation for vehicle_2 must still cause DEFER even
    when the useful evidence for the pending decision is vehicle_2.capacity.

    This limitation distinguishes the entity-filtered baseline from the
    decision-dependency-conditioned DARA-DT policy.
    """

    policy = EntityFilteredEvidencePolicy()

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
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.DEFER


def test_entity_policy_allows_available_selected_entity_with_stale_other_entity() -> None:
    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
        _evidence("vehicle_2.status", "operational"),
        _evidence(
            "vehicle_8.capacity",
            20,
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.ALLOW


def test_entity_policy_allows_when_selected_entity_has_no_evidence() -> None:
    """P2 reacts to observed uncertainty rather than inventing missing data."""

    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence(
            "vehicle_8.status",
            "operational",
            EvidenceStatus.STALE,
        ),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.ALLOW


def test_entity_policy_preserves_decision_id() -> None:
    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
        decision_id="decision_exp009_001",
    )

    assert result.decision_id == "decision_exp009_001"


def test_entity_policy_does_not_require_physical_ground_truth() -> None:
    """The public interface must use runtime evidence and entity identity only."""

    policy = EntityFilteredEvidencePolicy()

    evidence = [
        _evidence("vehicle_2.capacity", 10),
    ]

    result = policy.evaluate(
        evidence=evidence,
        selected_entity="vehicle_2",
    )

    assert result.authority == AuthorityState.ALLOW
