"""Tests for EXP-004 divergence-severity experiment."""

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.severity_experiment import (
    run_severity_experiment,
)


def test_severity_experiment_runs_all_conditions() -> None:
    """EXP-004 should execute S0 through S6."""

    results = run_severity_experiment()

    assert len(results) == 7
    assert tuple(result.condition for result in results) == (
        "S0",
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",
    )


def test_severity_magnitudes_match_experimental_design() -> None:
    """Executed conditions should preserve predefined magnitudes."""

    results = run_severity_experiment()

    assert tuple(
        result.divergence_magnitude
        for result in results
    ) == (0, 1, 3, 4, 5, 6, 8)


def test_physical_validity_crosses_boundary_between_s4_and_s5() -> None:
    """The physical decision should become invalid only after S4."""

    results = run_severity_experiment()

    assert tuple(
        result.physically_valid
        for result in results
    ) == (
        True,
        True,
        True,
        True,
        True,
        False,
        False,
    )


def test_s0_contains_no_divergence() -> None:
    """The synchronized baseline should contain no detected divergence."""

    result = run_severity_experiment()[0]

    assert result.condition == "S0"
    assert result.divergence_count == 0
    assert result.relevant_count == 0


def test_capacity_divergence_is_decision_relevant() -> None:
    """Capacity divergence should affect the vehicle-assignment decision."""

    results = run_severity_experiment()

    for result in results[1:]:
        assert result.divergence_count >= 1
        assert result.relevant_count >= 1


def test_no_assurance_misses_invalid_decisions() -> None:
    """No assurance should miss intervention at S5 and S6."""

    results = run_severity_experiment()

    assert results[5].no_assurance == AssuranceOutcome.MISSED_INTERVENTION
    assert results[6].no_assurance == AssuranceOutcome.MISSED_INTERVENTION


def test_global_divergence_false_intervenes_before_boundary() -> None:
    """Global divergence should over-intervene on valid divergent states."""

    results = run_severity_experiment()

    for result in results[1:5]:
        assert (
            result.global_divergence
            == AssuranceOutcome.FALSE_INTERVENTION
        )


def test_magnitude_threshold_matches_capacity_boundary() -> None:
    """Threshold five should separate valid and invalid capacity states."""

    results = run_severity_experiment(
        magnitude_threshold=5.0
    )

    for result in results[:5]:
        assert (
            result.magnitude_threshold
            == AssuranceOutcome.CORRECT_NON_INTERVENTION
        )

    for result in results[5:]:
        assert (
            result.magnitude_threshold
            == AssuranceOutcome.TRUE_INTERVENTION
        )


def test_dara_relevance_policy_exposes_expected_limitation() -> None:
    """Relevance alone should over-intervene before validity is lost.

    This is intentionally a diagnostic test. The current DARA-DT policy
    defers on any decision-relevant divergence, even when that divergence
    has not yet invalidated the physical decision.
    """

    results = run_severity_experiment()

    for result in results[1:5]:
        assert result.dara_dt == AssuranceOutcome.FALSE_INTERVENTION

    for result in results[5:]:
        assert result.dara_dt == AssuranceOutcome.TRUE_INTERVENTION


def test_s4_and_s5_capture_critical_decision_boundary() -> None:
    """S4 and S5 should isolate the validity-boundary transition."""

    results = run_severity_experiment()

    s4 = results[4]
    s5 = results[5]

    assert s4.divergence_magnitude == 5
    assert s4.physically_valid is True

    assert s5.divergence_magnitude == 6
    assert s5.physically_valid is False
