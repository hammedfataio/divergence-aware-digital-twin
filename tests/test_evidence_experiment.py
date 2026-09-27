"""Tests for EXP-006 imperfect-runtime-evidence experiment."""

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import OutcomeType
from dara_dt.experiments.evidence_experiment import (
    run_evidence_experiment,
)


def _results_by_id():
    """Return EXP-006 results indexed by condition identifier."""

    return {
        result.condition.condition_id: result
        for result in run_evidence_experiment()
    }


def test_experiment_runs_all_twelve_conditions() -> None:
    """EXP-006 should execute the complete evidence matrix."""

    results = run_evidence_experiment()

    assert len(results) == 12


def test_every_condition_produces_runtime_evidence() -> None:
    """Every condition should expose its runtime evidence to the policy."""

    for result in run_evidence_experiment():
        assert len(result.runtime_evidence) >= 1


def test_e0_accurate_invalid_evidence_triggers_intervention() -> None:
    """Accurate evidence should identify the physically invalid decision."""

    result = _results_by_id()["E0"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.TRUE_INTERVENTION
    )


def test_e3_misleading_evidence_can_hide_invalidity() -> None:
    """Available but misleading evidence should expose a missed intervention."""

    result = _results_by_id()["E3"]

    assert result.condition.physical_valid is False
    assert result.condition.observed_capacity > result.condition.demand
    assert result.evidence_aware_assurance.authority == AuthorityState.ALLOW
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.MISSED_INTERVENTION
    )


def test_e4_stale_evidence_causes_conservative_intervention() -> None:
    """Explicitly stale evidence should prevent unsafe autonomous execution."""

    result = _results_by_id()["E4"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.TRUE_INTERVENTION
    )


def test_e5_missing_evidence_causes_conservative_intervention() -> None:
    """Missing evidence should cause the evidence-aware policy to defer."""

    result = _results_by_id()["E5"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.TRUE_INTERVENTION
    )


def test_e6_conflicting_evidence_causes_conservative_intervention() -> None:
    """Conflicting evidence should cause the evidence-aware policy to defer."""

    result = _results_by_id()["E6"]

    assert result.condition.physical_valid is False
    assert len(result.runtime_evidence) == 2
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.TRUE_INTERVENTION
    )


def test_e7_accurate_valid_evidence_preserves_autonomy() -> None:
    """Accurate evidence for a valid decision should allow execution."""

    result = _results_by_id()["E7"]

    assert result.condition.physical_valid is True
    assert result.evidence_aware_assurance.authority == AuthorityState.ALLOW
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.CORRECT_NON_INTERVENTION
    )


def test_e8_bad_evidence_can_create_false_intervention() -> None:
    """Misleading evidence should expose false-intervention risk."""

    result = _results_by_id()["E8"]

    assert result.condition.physical_valid is True
    assert result.condition.observed_capacity < result.condition.demand
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.FALSE_INTERVENTION
    )


def test_e9_larger_margin_tolerates_observation_error() -> None:
    """A larger decision margin should remain autonomous under mild error."""

    result = _results_by_id()["E9"]

    assert result.condition.physical_valid is True
    assert result.evidence_aware_assurance.authority == AuthorityState.ALLOW
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.CORRECT_NON_INTERVENTION
    )


def test_e10_boundary_error_prevents_unsafe_execution() -> None:
    """Boundary evidence should restrict a physically invalid decision."""

    result = _results_by_id()["E10"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.RESTRICT
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.TRUE_INTERVENTION
    )


def test_e11_stale_twin_matching_evidence_does_not_authorise() -> None:
    """Old evidence agreeing with the Twin should still be treated as stale."""

    result = _results_by_id()["E11"]

    assert result.condition.physical_valid is False
    assert (
        result.condition.observed_capacity
        == result.condition.twin_capacity
    )
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert (
        result.evidence_aware_outcome.outcome
        == OutcomeType.TRUE_INTERVENTION
    )


def test_e3_exposes_limit_of_available_but_incorrect_evidence() -> None:
    """Evidence awareness cannot detect every plausible incorrect observation."""

    result = _results_by_id()["E3"]

    assert result.evidence_aware_assurance.autonomous_execution_allowed
    assert result.condition.physical_valid is False


def test_e4_and_e11_show_value_of_evidence_quality_metadata() -> None:
    """Staleness metadata should change authority despite apparently safe values."""

    results = _results_by_id()

    for condition_id in ("E4", "E11"):
        result = results[condition_id]

        assert result.condition.observed_capacity >= result.condition.demand
        assert result.evidence_aware_assurance.authority == AuthorityState.DEFER


def test_ground_truth_remains_independent_of_runtime_evidence() -> None:
    """Opposite evidence errors must not alter physical validity labels."""

    results = _results_by_id()

    # E3 looks safe but is physically invalid.
    assert results["E3"].condition.physical_valid is False
    assert (
        results["E3"].condition.observed_capacity
        >= results["E3"].condition.demand
    )

    # E8 looks unsafe but is physically valid.
    assert results["E8"].condition.physical_valid is True
    assert (
        results["E8"].condition.observed_capacity
        < results["E8"].condition.demand
    )
