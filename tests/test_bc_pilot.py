"""Tests for the controlled B-vs-C DARA-DT pilot."""

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.bc_pilot import run_bc_pilot


def test_condition_b_high_divergence_low_relevance():
    """DARA-DT should ignore divergence unrelated to the decision."""

    result = run_bc_pilot()
    condition = result.condition_b

    assert condition.condition == "B_HIGH_DIVERGENCE_LOW_RELEVANCE"
    assert condition.divergence_count == 2

    assert (
        condition.policy_results.no_assurance.outcome
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )

    assert (
        condition.policy_results.global_divergence.outcome
        == AssuranceOutcome.FALSE_INTERVENTION
    )

    assert (
        condition.policy_results.dara_dt.outcome
        == AssuranceOutcome.CORRECT_NON_INTERVENTION
    )


def test_condition_c_low_divergence_high_relevance():
    """DARA-DT should intervene when stale state affects the decision."""

    result = run_bc_pilot()
    condition = result.condition_c

    assert condition.condition == "C_LOW_DIVERGENCE_HIGH_RELEVANCE"

    # Breakdown creates status and availability mismatches.
    assert condition.divergence_count == 2

    assert (
        condition.policy_results.no_assurance.outcome
        == AssuranceOutcome.MISSED_INTERVENTION
    )

    assert (
        condition.policy_results.global_divergence.outcome
        == AssuranceOutcome.TRUE_INTERVENTION
    )

    assert (
        condition.policy_results.dara_dt.outcome
        == AssuranceOutcome.TRUE_INTERVENTION
    )
