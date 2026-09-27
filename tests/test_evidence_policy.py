"""Tests for the EXP-006 evidence-aware assurance policy."""

import pytest

from dara_dt.assurance.evidence_policy import EvidenceAwareDecisionPolicy
from dara_dt.assurance.model import AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence


def _decision() -> Decision:
    """Create a controlled vehicle-assignment decision."""

    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_001",
        order_id="order_001",
        timestamp=10.0,
    )


def _evidence(
    *,
    value,
    status: EvidenceStatus = EvidenceStatus.AVAILABLE,
    dependency: str = "vehicle.capacity",
) -> RuntimeEvidence:
    """Create controlled runtime evidence."""

    return RuntimeEvidence(
        source="capacity_sensor",
        dependency=dependency,
        observed_value=value,
        timestamp=10.0,
        status=status,
    )


def test_capacity_above_demand_allows_execution() -> None:
    """Evidence above the requirement should preserve autonomy."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[_evidence(value=9)],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True


def test_capacity_below_demand_defers_execution() -> None:
    """Evidence below the requirement should trigger intervention."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[_evidence(value=7)],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER
    assert result.autonomous_execution_allowed is False


def test_capacity_at_boundary_restricts_execution() -> None:
    """Exact boundary evidence should restrict autonomous authority."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[_evidence(value=8)],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.RESTRICT


def test_missing_evidence_defers_execution() -> None:
    """Missing decision evidence should trigger conservative intervention."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[
            _evidence(
                value=None,
                status=EvidenceStatus.MISSING,
            )
        ],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_stale_evidence_defers_execution() -> None:
    """Explicitly stale evidence should not permit autonomous execution."""

    policy = EvidenceAwareDecisionPolicy()

    evidence = RuntimeEvidence(
        source="capacity_sensor",
        dependency="vehicle.capacity",
        observed_value=10,
        timestamp=2.0,
        status=EvidenceStatus.STALE,
    )

    result = policy.evaluate(
        decision=_decision(),
        evidence=[evidence],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_conflicting_evidence_defers_execution() -> None:
    """Conflicting observations should trigger conservative intervention."""

    policy = EvidenceAwareDecisionPolicy()

    evidence = [
        RuntimeEvidence(
            source="sensor_a",
            dependency="vehicle.capacity",
            observed_value=6,
            timestamp=10.0,
            status=EvidenceStatus.CONFLICTING,
        ),
        RuntimeEvidence(
            source="sensor_b",
            dependency="vehicle.capacity",
            observed_value=9,
            timestamp=10.0,
            status=EvidenceStatus.CONFLICTING,
        ),
    ]

    result = policy.evaluate(
        decision=_decision(),
        evidence=evidence,
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_empty_evidence_defers_execution() -> None:
    """Absence of runtime evidence should trigger intervention."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_irrelevant_evidence_does_not_authorise_decision() -> None:
    """Evidence for another dependency cannot justify capacity safety."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[
            _evidence(
                value="depot",
                dependency="vehicle.location",
            )
        ],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_multiple_available_sources_use_conservative_capacity() -> None:
    """The lowest usable capacity should govern when sources are available."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[
            _evidence(value=10),
            RuntimeEvidence(
                source="capacity_sensor_b",
                dependency="vehicle.capacity",
                observed_value=7,
                timestamp=10.0,
            ),
        ],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_negative_demand_is_rejected() -> None:
    """Demand cannot be negative."""

    policy = EvidenceAwareDecisionPolicy()

    with pytest.raises(
        ValueError,
        match="Demand must not be negative",
    ):
        policy.evaluate(
            decision=_decision(),
            evidence=[_evidence(value=9)],
            demand=-1,
            current_time=10.0,
        )


def test_non_numeric_demand_is_rejected() -> None:
    """Decision demand must be numeric."""

    policy = EvidenceAwareDecisionPolicy()

    with pytest.raises(
        TypeError,
        match="Demand must be numeric",
    ):
        policy.evaluate(
            decision=_decision(),
            evidence=[_evidence(value=9)],
            demand="eight",
            current_time=10.0,
        )


def test_non_numeric_capacity_evidence_defers() -> None:
    """Non-numeric capacity evidence must not authorise execution."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[_evidence(value="unknown")],
        demand=8,
        current_time=10.0,
    )

    assert result.authority == AuthorityState.DEFER


def test_result_preserves_decision_id() -> None:
    """Assurance output must remain traceable to the proposed decision."""

    policy = EvidenceAwareDecisionPolicy()
    decision = _decision()

    result = policy.evaluate(
        decision=decision,
        evidence=[_evidence(value=9)],
        demand=8,
        current_time=10.0,
    )

    assert result.decision_id == decision.decision_id


def test_allow_has_zero_relevant_divergence_count() -> None:
    """An allowed decision should expose the policy's non-intervention state."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[_evidence(value=9)],
        demand=8,
        current_time=10.0,
    )

    assert result.relevant_divergence_count == 0


def test_uncertain_evidence_records_intervention_state() -> None:
    """Evidence uncertainty should be represented as an intervention."""

    policy = EvidenceAwareDecisionPolicy()

    result = policy.evaluate(
        decision=_decision(),
        evidence=[],
        demand=8,
        current_time=10.0,
    )

    assert result.relevant_divergence_count == 1
