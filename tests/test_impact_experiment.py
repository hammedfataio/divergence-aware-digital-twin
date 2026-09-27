"""Tests for EXP-005 decision-impact-aware assurance experiment."""

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.impact_experiment import (
    run_impact_experiment,
)


def results_by_name():
    """Return EXP-005 results indexed by condition name."""

    return {
        result.condition.name: result
        for result in run_impact_experiment()
    }


def test_experiment_runs_all_conditions() -> None:
    """EXP-005 should execute all I0-I14 conditions."""

    results = run_impact_experiment()

    assert len(results) == 15


def test_synchronised_condition_has_no_divergence() -> None:
    """I0 should remain fully synchronised."""

    result = results_by_name()["I0_synchronised"]

    assert result.divergence_count == 0
    assert result.relevant_divergence_count == 0
    assert result.estimated_margin == 5.0
    assert result.impact_state == "no_impact"


def test_same_divergence_has_different_decision_impact() -> None:
    """Equal divergence magnitude can produce different decision impacts."""

    results = results_by_name()

    valid = results["I7_same_divergence_valid"]
    invalid = results["I8_same_divergence_invalid"]

    assert valid.condition.divergence_magnitude == 3
    assert invalid.condition.divergence_magnitude == 3

    assert valid.estimated_margin == 2.0
    assert invalid.estimated_margin == -1.0

    assert valid.impact_state == "margin_reduced"
    assert invalid.impact_state == "invalidating"


def test_same_divergence_has_different_physical_validity() -> None:
    """Equal divergence does not imply equal decision validity."""

    results = results_by_name()

    valid = results["I7_same_divergence_valid"]
    invalid = results["I8_same_divergence_invalid"]

    assert valid.condition.physically_valid is True
    assert invalid.condition.physically_valid is False


def test_global_divergence_false_intervenes_on_valid_change() -> None:
    """Global divergence assurance should expose unnecessary intervention."""

    result = results_by_name()["I7_same_divergence_valid"]

    assert (
        result.global_divergence.outcome
        == AssuranceOutcome.FALSE_INTERVENTION
    )


def test_relevance_only_policy_false_intervenes_on_valid_change() -> None:
    """Decision relevance alone should not establish invalidity."""

    result = results_by_name()["I7_same_divergence_valid"]

    assert (
        result.decision_relevance.outcome
        == AssuranceOutcome.FALSE_INTERVENTION
    )


def test_impact_policy_allows_valid_reduced_margin() -> None:
    """Impact-aware assurance should preserve valid autonomous execution."""

    result = results_by_name()["I7_same_divergence_valid"]

    assert (
        result.decision_impact.outcome
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )


def test_impact_policy_intervenes_on_invalid_decision() -> None:
    """Impact-aware assurance should intervene after validity is crossed."""

    result = results_by_name()["I8_same_divergence_invalid"]

    assert (
        result.decision_impact.outcome
        == AssuranceOutcome.TRUE_INTERVENTION
    )


def test_no_assurance_misses_invalid_decision() -> None:
    """No assurance should expose the unsafe autonomous baseline."""

    result = results_by_name()["I8_same_divergence_invalid"]

    assert (
        result.no_assurance.outcome
        == AssuranceOutcome.MISSED_INTERVENTION
    )


def test_fixed_magnitude_cannot_distinguish_equal_divergence() -> None:
    """A fixed magnitude rule sees I7 and I8 identically."""

    results = results_by_name()

    valid = results["I7_same_divergence_valid"]
    invalid = results["I8_same_divergence_invalid"]

    assert (
        valid.fixed_magnitude.assurance.authority
        == invalid.fixed_magnitude.assurance.authority
    )


def test_impact_policy_distinguishes_equal_divergence() -> None:
    """Decision impact should produce different authority decisions."""

    results = results_by_name()

    valid = results["I7_same_divergence_valid"]
    invalid = results["I8_same_divergence_invalid"]

    assert (
        valid.decision_impact.assurance.authority
        == AuthorityState.ALLOW
    )

    assert (
        invalid.decision_impact.assurance.authority
        == AuthorityState.DEFER
    )


def test_changed_boundary_is_decision_specific() -> None:
    """The same assurance logic should follow changing decision boundaries."""

    results = results_by_name()

    boundary = results["I11_tight_boundary"]
    invalid = results["I12_tight_invalid"]

    assert boundary.estimated_margin == 0.0
    assert invalid.estimated_margin == -1.0

    assert boundary.impact_state == "boundary"
    assert invalid.impact_state == "invalidating"


def test_large_system_boundary_is_preserved() -> None:
    """Decision-impact analysis should work at a different capacity scale."""

    results = results_by_name()

    valid = results["I13_large_system_valid"]
    invalid = results["I14_large_system_invalid"]

    assert valid.estimated_margin == 1.0
    assert invalid.estimated_margin == -1.0

    assert valid.impact_state == "margin_reduced"
    assert invalid.impact_state == "invalidating"
