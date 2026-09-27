"""Tests for the DARA-DT decision-impact-aware assurance policy."""

import pytest

from dara_dt.assurance.impact_policy import DecisionImpactPolicy
from dara_dt.assurance.model import AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.impact.model import DecisionImpact, ImpactState


def make_decision(decision_id: str = "decision_001") -> Decision:
    """Create a logistics decision using the repository Decision API."""

    return Decision(
        decision_id=decision_id,
        action="assign_vehicle",
        vehicle_id="vehicle_001",
        order_id="order_001",
        timestamp=0.0,
    )


def make_impact(
    state: ImpactState,
    decision_id: str = "decision_001",
    margin: float | None = None,
) -> DecisionImpact:
    """Create a decision-impact result for policy tests."""

    return DecisionImpact(
        decision_id=decision_id,
        dependency="vehicle.capacity",
        impact_state=state,
        estimated_margin=margin,
        evidence=(),
        reason="Test impact.",
    )


def test_no_impact_allows_autonomous_execution() -> None:
    """No material impact should preserve autonomous authority."""

    policy = DecisionImpactPolicy()
    decision = make_decision()

    result = policy.evaluate(
        decision,
        make_impact(
            ImpactState.NO_IMPACT,
            margin=5.0,
        ),
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True


def test_reduced_margin_still_allows_execution() -> None:
    """Reduced but positive margin should not trigger intervention."""

    policy = DecisionImpactPolicy()
    decision = make_decision()

    result = policy.evaluate(
        decision,
        make_impact(
            ImpactState.MARGIN_REDUCED,
            margin=2.0,
        ),
    )

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True


def test_boundary_restricts_autonomous_authority() -> None:
    """A decision at its estimated boundary should be restricted."""

    policy = DecisionImpactPolicy()
    decision = make_decision()

    result = policy.evaluate(
        decision,
        make_impact(
            ImpactState.BOUNDARY,
            margin=0.0,
        ),
    )

    assert result.authority == AuthorityState.RESTRICT
    assert result.autonomous_execution_allowed is False


def test_invalidating_impact_defers_decision() -> None:
    """An invalidating impact should prevent autonomous execution."""

    policy = DecisionImpactPolicy()
    decision = make_decision()

    result = policy.evaluate(
        decision,
        make_impact(
            ImpactState.INVALIDATING,
            margin=-1.0,
        ),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.autonomous_execution_allowed is False


def test_uncertain_impact_defers_decision() -> None:
    """Insufficient runtime evidence should trigger conservative deferral."""

    policy = DecisionImpactPolicy()
    decision = make_decision()

    result = policy.evaluate(
        decision,
        make_impact(
            ImpactState.UNCERTAIN,
            margin=None,
        ),
    )

    assert result.authority == AuthorityState.DEFER
    assert result.autonomous_execution_allowed is False


def test_policy_rejects_impact_from_different_decision() -> None:
    """Impact evidence must belong to the decision being evaluated."""

    policy = DecisionImpactPolicy()

    decision = make_decision(
        decision_id="decision_001",
    )

    impact = make_impact(
        ImpactState.INVALIDATING,
        decision_id="decision_999",
        margin=-1.0,
    )

    with pytest.raises(
        ValueError,
        match="Decision impact does not belong",
    ):
        policy.evaluate(
            decision,
            impact,
        )


@pytest.mark.parametrize(
    ("state", "expected_authority"),
    [
        (
            ImpactState.NO_IMPACT,
            AuthorityState.ALLOW,
        ),
        (
            ImpactState.MARGIN_REDUCED,
            AuthorityState.ALLOW,
        ),
        (
            ImpactState.BOUNDARY,
            AuthorityState.RESTRICT,
        ),
        (
            ImpactState.INVALIDATING,
            AuthorityState.DEFER,
        ),
        (
            ImpactState.UNCERTAIN,
            AuthorityState.DEFER,
        ),
    ],
)
def test_all_impact_states_have_explicit_authority(
    state: ImpactState,
    expected_authority: AuthorityState,
) -> None:
    """Every defined impact state should map to an authority state."""

    policy = DecisionImpactPolicy()
    decision = make_decision()

    result = policy.evaluate(
        decision,
        make_impact(state),
    )

    assert result.authority == expected_authority
