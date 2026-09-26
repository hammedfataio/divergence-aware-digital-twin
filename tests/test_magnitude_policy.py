"""Tests for the magnitude-based assurance baseline."""

from dara_dt.assurance.magnitude_policy import MagnitudeAssurancePolicy
from dara_dt.assurance.model import AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence


def make_decision() -> Decision:
    """Create a controlled decision for assurance-policy testing."""

    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        parameters={
            "vehicle_id": "vehicle_00",
            "order_id": "order_00",
        },
        timestamp=1.0,
    )


def make_divergence(
    physical_value: object,
    twin_value: object,
) -> Divergence:
    """Create a controlled capacity divergence."""

    return Divergence(
        path="vehicles.vehicle_00.capacity",
        physical_value=physical_value,
        twin_value=twin_value,
    )


def test_no_divergence_allows_decision() -> None:
    """No detected divergence should allow autonomous execution."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    result = policy.decide(make_decision(), [])

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True


def test_magnitude_below_threshold_allows_decision() -> None:
    """Magnitude below the threshold should not trigger intervention."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    result = policy.decide(
        make_decision(),
        [make_divergence(physical_value=7, twin_value=10)],
    )

    assert result.authority == AuthorityState.ALLOW


def test_magnitude_equal_to_threshold_allows_decision() -> None:
    """The baseline should use a strict greater-than threshold."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    result = policy.decide(
        make_decision(),
        [make_divergence(physical_value=5, twin_value=10)],
    )

    assert result.authority == AuthorityState.ALLOW


def test_magnitude_above_threshold_defers_decision() -> None:
    """Magnitude above the threshold should trigger intervention."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    result = policy.decide(
        make_decision(),
        [make_divergence(physical_value=4, twin_value=10)],
    )

    assert result.authority == AuthorityState.DEFER
    assert result.autonomous_execution_allowed is False


def test_absolute_difference_is_used() -> None:
    """Magnitude should be independent of divergence direction."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    result = policy.decide(
        make_decision(),
        [make_divergence(physical_value=16, twin_value=10)],
    )

    assert result.authority == AuthorityState.DEFER


def test_any_numeric_divergence_above_threshold_defers() -> None:
    """One sufficiently large numeric divergence should trigger intervention."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    divergences = [
        make_divergence(physical_value=9, twin_value=10),
        make_divergence(physical_value=3, twin_value=10),
    ]

    result = policy.decide(make_decision(), divergences)

    assert result.authority == AuthorityState.DEFER


def test_boolean_divergence_is_not_numeric_magnitude() -> None:
    """Boolean state changes should not be interpreted as numeric severity."""

    policy = MagnitudeAssurancePolicy(threshold=0)

    result = policy.decide(
        make_decision(),
        [make_divergence(physical_value=False, twin_value=True)],
    )

    assert result.authority == AuthorityState.ALLOW


def test_non_numeric_divergence_is_ignored() -> None:
    """Categorical divergence should not create numeric severity."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    result = policy.decide(
        make_decision(),
        [
            make_divergence(
                physical_value="broken_down",
                twin_value="operational",
            )
        ],
    )

    assert result.authority == AuthorityState.ALLOW


def test_result_preserves_decision_id() -> None:
    """Assurance output should remain associated with its input decision."""

    policy = MagnitudeAssurancePolicy(threshold=5)
    decision = make_decision()

    result = policy.decide(decision, [])

    assert result.decision_id == decision.decision_id
