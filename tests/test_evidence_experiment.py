"""Tests for EXP-006 imperfect-runtime-evidence experiment."""

from dara_dt.assurance.model import AuthorityState
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

    assert len(run_evidence_experiment()) == 12


def test_every_condition_produces_runtime_evidence() -> None:
    """Every condition should expose runtime evidence."""

    for result in run_evidence_experiment():
        assert len(result.runtime_evidence) >= 1


def test_e0_accurate_invalid_evidence_triggers_intervention() -> None:
    """Accurate evidence should identify a physically invalid decision."""

    result = _results_by_id()["E0"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert result.evidence_aware_outcome.outcome.value == "true_intervention"


def test_e3_misleading_evidence_can_hide_invalidity() -> None:
    """Incorrect but usable evidence can hide physical invalidity."""

    result = _results_by_id()["E3"]

    assert result.condition.physical_valid is False
    assert result.condition.observed_capacity > result.condition.demand
    assert result.evidence_aware_assurance.authority == AuthorityState.ALLOW
    assert result.evidence_aware_outcome.outcome.value == "missed_intervention"


def test_e4_stale_evidence_causes_conservative_intervention() -> None:
    """Stale evidence should prevent unsafe autonomous execution."""

    result = _results_by_id()["E4"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert result.evidence_aware_outcome.outcome.value == "true_intervention"


def test_e5_missing_evidence_causes_conservative_intervention() -> None:
    """Missing evidence should cause conservative deferral."""

    result = _results_by_id()["E5"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert result.evidence_aware_outcome.outcome.value == "true_intervention"


def test_e6_conflicting_evidence_causes_conservative_intervention() -> None:
    """Conflicting evidence should cause conservative deferral."""

    result = _results_by_id()["E6"]

    assert result.condition.physical_valid is False
    assert len(result.runtime_evidence) == 2
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert result.evidence_aware_outcome.outcome.value == "true_intervention"


def test_e7_accurate_valid_evidence_preserves_autonomy() -> None:
    """Accurate evidence for a valid decision should preserve autonomy."""

    result = _results_by_id()["E7"]

    assert result.condition.physical_valid is True
    assert result.evidence_aware_assurance.authority == AuthorityState.ALLOW
    assert (
        result.evidence_aware_outcome.outcome.value
        == "correct_non_intervention"
    )


def test_e8_bad_evidence_can_create_false_intervention() -> None:
    """Incorrect evidence can create an unnecessary intervention."""

    result = _results_by_id()["E8"]

    assert result.condition.physical_valid is True
    assert result.condition.observed_capacity < result.condition.demand
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert result.evidence_aware_outcome.outcome.value == "false_intervention"


def test_e9_larger_margin_tolerates_observation_error() -> None:
    """A larger decision margin should tolerate the controlled error."""

    result = _results_by_id()["E9"]

    assert result.condition.physical_valid is True
    assert result.evidence_aware_assurance.authority == AuthorityState.ALLOW
    assert (
        result.evidence_aware_outcome.outcome.value
        == "correct_non_intervention"
    )


def test_e10_boundary_error_prevents_unsafe_execution() -> None:
    """Boundary evidence should restrict a physically invalid decision."""

    result = _results_by_id()["E10"]

    assert result.condition.physical_valid is False
    assert result.evidence_aware_assurance.authority == AuthorityState.RESTRICT
    assert result.evidence_aware_outcome.outcome.value == "true_intervention"


def test_e11_stale_twin_matching_evidence_does_not_authorise() -> None:
    """Old evidence agreeing with the Twin must still be treated as stale."""

    result = _results_by_id()["E11"]

    assert result.condition.physical_valid is False
    assert result.condition.observed_capacity == result.condition.twin_capacity
    assert result.evidence_aware_assurance.authority == AuthorityState.DEFER
    assert result.evidence_aware_outcome.outcome.value == "true_intervention"


def test_e3_exposes_limit_of_available_but_incorrect_evidence() -> None:
    """Evidence awareness cannot detect every plausible incorrect observation."""

    result = _results_by_id()["E3"]

    assert result.evidence_aware_assurance.autonomous_execution_allowed
    assert result.condition.physical_valid is False


def test_e4_and_e11_show_value_of_evidence_quality_metadata() -> None:
    """Staleness metadata should matter despite apparently safe values."""

    results = _results_by_id()

    for condition_id in ("E4", "E11"):
        result = results[condition_id]

        assert result.condition.observed_capacity >= result.condition.demand
        assert result.evidence_aware_assurance.authority == AuthorityState.DEFER


def test_ground_truth_remains_independent_of_runtime_evidence() -> None:
    """Runtime evidence must not alter physical ground-truth validity."""

    results = _results_by_id()

    # E3 appears safe from runtime evidence but is physically invalid.
    assert results["E3"].condition.physical_valid is False
    assert (
        results["E3"].condition.observed_capacity
        >= results["E3"].condition.demand
    )

    # E8 appears unsafe from runtime evidence but is physically valid.
    assert results["E8"].condition.physical_valid is True
    assert (
        results["E8"].condition.observed_capacity
        < results["E8"].condition.demand
    )
