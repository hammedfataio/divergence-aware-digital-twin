"""Tests for the magnitude-based assurance baseline."""

from dara_dt.assurance.magnitude_policy import MagnitudeAssurancePolicy
from dara_dt.assurance.model import AssuranceAction
from dara_dt.divergence.detector import Divergence


def make_divergence(
    physical_value: object,
    twin_value: object,
) -> Divergence:
    """Create a controlled divergence for policy testing."""

    return Divergence(
        path="vehicles.vehicle_00.capacity",
        physical_value=physical_value,
        twin_value=twin_value,
    )


def test_no_divergence_allows_decision() -> None:
    """No detected divergence should not trigger intervention."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    assert policy.decide([]) == AssuranceAction.ALLOW


def test_magnitude_below_threshold_allows_decision() -> None:
    """A magnitude below the threshold should be allowed."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    divergences = [
        make_divergence(
            physical_value=7,
            twin_value=10,
        )
    ]

    assert policy.decide(divergences) == AssuranceAction.ALLOW


def test_magnitude_equal_to_threshold_allows_decision() -> None:
    """The baseline uses a strict greater-than threshold."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    divergences = [
        make_divergence(
            physical_value=5,
            twin_value=10,
        )
    ]

    assert policy.decide(divergences) == AssuranceAction.ALLOW


def test_magnitude_above_threshold_defers_decision() -> None:
    """A magnitude above the threshold should trigger intervention."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    divergences = [
        make_divergence(
            physical_value=4,
            twin_value=10,
        )
    ]

    assert policy.decide(divergences) == AssuranceAction.DEFER


def test_absolute_difference_is_used() -> None:
    """Magnitude should be independent of divergence direction."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    divergences = [
        make_divergence(
            physical_value=16,
            twin_value=10,
        )
    ]

    assert policy.decide(divergences) == AssuranceAction.DEFER


def test_any_divergence_above_threshold_triggers_intervention() -> None:
    """One sufficiently large divergence should trigger the baseline."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    divergences = [
        make_divergence(
            physical_value=9,
            twin_value=10,
        ),
        make_divergence(
            physical_value=3,
            twin_value=10,
        ),
    ]

    assert policy.decide(divergences) == AssuranceAction.DEFER


def test_boolean_divergence_is_not_treated_as_numeric_magnitude() -> None:
    """Boolean state changes should not be interpreted as 0/1 magnitudes."""

    policy = MagnitudeAssurancePolicy(threshold=0)

    divergences = [
        make_divergence(
            physical_value=False,
            twin_value=True,
        )
    ]

    assert policy.decide(divergences) == AssuranceAction.ALLOW


def test_non_numeric_divergence_is_ignored_by_magnitude_policy() -> None:
    """Categorical divergence has no numeric magnitude for this baseline."""

    policy = MagnitudeAssurancePolicy(threshold=5)

    divergences = [
        make_divergence(
            physical_value="broken_down",
            twin_value="operational",
        )
    ]

    assert policy.decide(divergences) == AssuranceAction.ALLOW
