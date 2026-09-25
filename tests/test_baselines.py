"""Tests for baseline runtime assurance policies."""

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.model import AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence


def create_decision() -> Decision:
    """Create a logistics decision for baseline testing."""
    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=125.0,
    )


def create_divergence() -> Divergence:
    """Create a physical-digital divergence for testing."""
    return Divergence(
        entity_type="vehicles",
        entity_id="vehicle_03",
        variable="status",
        physical_value="broken_down",
        twin_value="operational",
    )


def test_no_assurance_allows_without_divergence():
    policy = NoAssurancePolicy()

    result = policy.evaluate(
        create_decision(),
        [],
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True


def test_no_assurance_allows_despite_divergence():
    policy = NoAssurancePolicy()

    result = policy.evaluate(
        create_decision(),
        [create_divergence()],
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True


def test_any_divergence_allows_when_synchronised():
    policy = AnyDivergencePolicy()

    result = policy.evaluate(
        create_decision(),
        [],
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True


def test_any_divergence_defers_when_divergence_exists():
    policy = AnyDivergencePolicy()

    result = policy.evaluate(
        create_decision(),
        [create_divergence()],
    )

    assert result.authority == AuthorityState.DEFER
    assert result.autonomous_execution_allowed is False


def test_any_divergence_counts_detected_divergence():
    policy = AnyDivergencePolicy()

    divergences = [
        create_divergence(),
        Divergence(
            entity_type="vehicles",
            entity_id="vehicle_07",
            variable="location",
            physical_value="node_14",
            twin_value="node_30",
        ),
    ]

    result = policy.evaluate(
        create_decision(),
        divergences,
    )

    assert result.relevant_divergence_count == 2
