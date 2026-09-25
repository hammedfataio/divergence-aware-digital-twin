"""Tests for decision-relevant policy comparison."""

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.relevant_policy_experiment import (
    run_relevant_policy_experiment,
)


def test_relevant_divergence_is_detected():
    """Breakdown should create decision-relevant divergence."""

    result = run_relevant_policy_experiment()

    assert result.selected_vehicle_id == "vehicle_00"
    assert result.divergence_count == 2
    assert result.relevant_count == 2


def test_no_assurance_misses_required_intervention():
    """No assurance should allow the invalid physical decision."""

    result = run_relevant_policy_experiment()

    assert (
        result.no_assurance
        == AssuranceOutcome.MISSED_INTERVENTION
    )


def test_global_divergence_intervenes_correctly():
    """Global divergence should intervene in this relevant case."""

    result = run_relevant_policy_experiment()

    assert (
        result.global_divergence
        == AssuranceOutcome.TRUE_INTERVENTION
    )


def test_dara_dt_intervenes_on_relevant_divergence():
    """DARA-DT should intervene when divergence affects the decision."""

    result = run_relevant_policy_experiment()

    assert (
        result.dara_dt
        == AssuranceOutcome.TRUE_INTERVENTION
    )
