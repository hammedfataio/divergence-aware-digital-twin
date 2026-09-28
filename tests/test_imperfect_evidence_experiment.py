"""Tests for EXP-008 imperfect-evidence contract comparison.

These tests preserve the registered EXP-008 experimental design and verify
that physical ground truth, Digital Twin state and runtime evidence remain
separate information layers.

The tests deliberately do not require DARA-DT and the uncertainty-aware
runtime contract to produce identical authority states. EXP-008 evaluates
that relationship empirically rather than assuming equivalence in advance.
"""

from collections import Counter

import pytest

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.cross_dependency_conditions import DependencyFamily
from dara_dt.experiments.imperfect_evidence_experiment import (
    _build_physical_state,
    _build_runtime_evidence,
    _runtime_divergences,
    run_imperfect_evidence_experiment,
)
from dara_dt.experiments.imperfect_evidence_conditions import (
    build_imperfect_evidence_conditions,
)


@pytest.fixture(scope="module")
def conditions():
    """Return the frozen EXP-008 condition matrix."""

    return build_imperfect_evidence_conditions()


@pytest.fixture(scope="module")
def results():
    """Execute the complete EXP-008 matrix once."""

    return run_imperfect_evidence_experiment()


def by_id(items, condition_id):
    """Return a condition or result identified by condition_id."""

    for item in items:
        condition = getattr(item, "condition", item)

        if condition.condition_id == condition_id:
            return item

    raise AssertionError(f"Unknown condition: {condition_id}")


# ---------------------------------------------------------------------------
# Matrix execution
# ---------------------------------------------------------------------------


def test_exp008_runs_exactly_24_conditions(results):
    assert len(results) == 24


def test_exp008_preserves_registered_condition_order(conditions, results):
    assert [
        result.condition.condition_id for result in results
    ] == [
        condition.condition_id for condition in conditions
    ]


def test_each_condition_produces_unique_decision(results):
    decision_ids = [result.decision.decision_id for result in results]

    assert len(decision_ids) == len(set(decision_ids))


def test_each_dependency_family_runs_eight_times(results):
    counts = Counter(result.condition.family for result in results)

    assert counts == {
        DependencyFamily.CAPACITY: 8,
        DependencyFamily.STATUS: 8,
        DependencyFamily.LOCATION_AVAILABILITY: 8,
    }


def test_each_evidence_status_runs_six_times(results):
    counts = Counter(result.evidence_status for result in results)

    assert counts == {
        EvidenceStatus.AVAILABLE: 6,
        EvidenceStatus.STALE: 6,
        EvidenceStatus.MISSING: 6,
        EvidenceStatus.CONFLICTING: 6,
    }


# ---------------------------------------------------------------------------
# Independent physical ground truth
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-R0",
        "CAP-S0",
        "CAP-M0",
        "CAP-C0",
        "STATUS-R0",
        "STATUS-S0",
        "STATUS-M0",
        "STATUS-C0",
        "LOC-R0",
        "LOC-S0",
        "LOC-M0",
        "LOC-C0",
    ],
)
def test_zero_conditions_are_physically_valid(results, condition_id):
    result = by_id(results, condition_id)

    assert result.ground_truth.intervention_required is False


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-R1",
        "CAP-S1",
        "CAP-M1",
        "CAP-C1",
        "STATUS-R1",
        "STATUS-S1",
        "STATUS-M1",
        "STATUS-C1",
        "LOC-R1",
        "LOC-S1",
        "LOC-M1",
        "LOC-C1",
    ],
)
def test_one_conditions_require_intervention(results, condition_id):
    result = by_id(results, condition_id)

    assert result.ground_truth.intervention_required is True


def test_ground_truth_contains_twelve_valid_and_twelve_invalid(results):
    required = sum(
        result.ground_truth.intervention_required
        for result in results
    )

    assert required == 12


def test_physical_state_uses_physical_capacity(conditions):
    condition = by_id(conditions, "CAP-S1")

    physical_state = _build_physical_state(condition)

    assert (
        physical_state["vehicles"]["vehicle_01"]["capacity"]
        == condition.physical_value
    )

    assert (
        physical_state["vehicles"]["vehicle_01"]["capacity"]
        != condition.primary_evidence_value
    )


def test_physical_state_uses_physical_status(conditions):
    condition = by_id(conditions, "STATUS-S1")

    physical_state = _build_physical_state(condition)

    assert (
        physical_state["vehicles"]["vehicle_01"]["status"]
        == condition.physical_value
    )

    assert (
        physical_state["vehicles"]["vehicle_01"]["status"]
        != condition.primary_evidence_value
    )


def test_physical_state_uses_physical_location_and_availability(conditions):
    condition = by_id(conditions, "LOC-S1")

    physical_state = _build_physical_state(condition)
    vehicle = physical_state["vehicles"]["vehicle_01"]

    physical_location, physical_available = condition.physical_value

    assert vehicle["location"] == physical_location
    assert vehicle["available"] == physical_available


# ---------------------------------------------------------------------------
# Runtime evidence construction
# ---------------------------------------------------------------------------


def test_capacity_runtime_evidence_uses_registered_observation(conditions):
    condition = by_id(conditions, "CAP-R0")

    evidence = _build_runtime_evidence(condition)

    assert len(evidence) == 1
    assert evidence[0].dependency == "vehicle.capacity"
    assert evidence[0].observed_value == condition.primary_evidence_value
    assert evidence[0].status == EvidenceStatus.AVAILABLE


def test_status_runtime_evidence_uses_registered_observation(conditions):
    condition = by_id(conditions, "STATUS-R0")

    evidence = _build_runtime_evidence(condition)

    assert len(evidence) == 1
    assert evidence[0].dependency == "vehicle.status"
    assert evidence[0].observed_value == condition.primary_evidence_value


def test_location_runtime_evidence_contains_two_dependencies(conditions):
    condition = by_id(conditions, "LOC-R0")

    evidence = _build_runtime_evidence(condition)

    assert len(evidence) == 2

    dependencies = {item.dependency for item in evidence}

    assert dependencies == {
        "vehicle.location",
        "vehicle.available",
    }


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-M0",
        "CAP-M1",
        "STATUS-M0",
        "STATUS-M1",
        "LOC-M0",
        "LOC-M1",
    ],
)
def test_missing_conditions_expose_no_runtime_value(
    conditions,
    condition_id,
):
    condition = by_id(conditions, condition_id)

    evidence = _build_runtime_evidence(condition)

    assert all(
        item.status == EvidenceStatus.MISSING
        for item in evidence
    )

    assert all(
        item.observed_value is None
        for item in evidence
    )


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-S0",
        "CAP-S1",
        "STATUS-S0",
        "STATUS-S1",
        "LOC-S0",
        "LOC-S1",
    ],
)
def test_stale_conditions_remain_explicitly_stale(
    conditions,
    condition_id,
):
    condition = by_id(conditions, condition_id)

    evidence = _build_runtime_evidence(condition)

    assert all(
        item.status == EvidenceStatus.STALE
        for item in evidence
    )


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-C0",
        "CAP-C1",
        "STATUS-C0",
        "STATUS-C1",
        "LOC-C0",
        "LOC-C1",
    ],
)
def test_conflicting_conditions_remain_explicitly_conflicting(
    conditions,
    condition_id,
):
    condition = by_id(conditions, condition_id)

    evidence = _build_runtime_evidence(condition)

    assert all(
        item.status == EvidenceStatus.CONFLICTING
        for item in evidence
    )


# ---------------------------------------------------------------------------
# Runtime-observable divergence
# ---------------------------------------------------------------------------


def test_missing_evidence_does_not_create_observed_divergence(conditions):
    condition = by_id(conditions, "CAP-M1")

    evidence = _build_runtime_evidence(condition)

    divergences = _runtime_divergences(
        condition=condition,
        evidence=evidence,
    )

    assert divergences == []


def test_runtime_divergence_uses_evidence_not_physical_truth(conditions):
    """Runtime mismatch must reflect visible evidence, not hidden truth."""

    condition = by_id(conditions, "CAP-S1")

    evidence = _build_runtime_evidence(condition)

    divergences = _runtime_divergences(
        condition=condition,
        evidence=evidence,
    )

    assert condition.physical_value == 4.0
    assert condition.primary_evidence_value == 8.0
    assert condition.twin_value == 10.0

    assert condition.physical_value != condition.primary_evidence_value
    assert condition.primary_evidence_value != condition.twin_value

    assert len(divergences) == 1
    assert divergences[0].physical_value == 8.0
    assert divergences[0].twin_value == 10.0


def test_runtime_divergence_can_exist_when_physical_state_is_valid(
    conditions,
):
    """Adverse stale evidence can create an apparent Twin mismatch."""

    condition = by_id(conditions, "CAP-S0")

    evidence = _build_runtime_evidence(condition)

    divergences = _runtime_divergences(
        condition=condition,
        evidence=evidence,
    )

    assert condition.physical_value >= condition.order_demand
    assert len(divergences) == 1


def test_stale_evidence_can_understate_true_physical_divergence(conditions):
    """Observed divergence need not equal the hidden physical divergence."""

    condition = by_id(conditions, "CAP-S1")

    evidence = _build_runtime_evidence(condition)

    divergences = _runtime_divergences(
        condition=condition,
        evidence=evidence,
    )

    assert len(divergences) == 1

    observed_difference = abs(
        divergences[0].physical_value
        - divergences[0].twin_value
    )

    true_physical_difference = abs(
        condition.physical_value
        - condition.twin_value
    )

    assert observed_difference == 2.0
    assert true_physical_difference == 6.0
    assert observed_difference < true_physical_difference


# ---------------------------------------------------------------------------
# Reliable evidence
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-R0",
        "STATUS-R0",
        "LOC-R0",
    ],
)
def test_reliable_valid_conditions_preserve_autonomy(
    results,
    condition_id,
):
    result = by_id(results, condition_id)

    assert result.uncertainty_contract_authority == AuthorityState.ALLOW
    assert result.dara_dt_authority == AuthorityState.ALLOW


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-R1",
        "STATUS-R1",
        "LOC-R1",
    ],
)
def test_reliable_invalid_conditions_trigger_intervention(
    results,
    condition_id,
):
    result = by_id(results, condition_id)

    assert (
        result.uncertainty_contract_authority
        != AuthorityState.ALLOW
    )

    assert result.dara_dt_authority != AuthorityState.ALLOW


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-R1",
        "STATUS-R1",
        "LOC-R1",
    ],
)
def test_reliable_invalid_conditions_expose_authority_difference(
    results,
    condition_id,
):
    """Both intervene, but their authority response is not identical."""

    result = by_id(results, condition_id)

    assert (
        result.uncertainty_contract_authority
        == AuthorityState.RESTRICT
    )

    assert result.dara_dt_authority == AuthorityState.DEFER


# ---------------------------------------------------------------------------
# Imperfect evidence behaviour
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-S0",
        "CAP-S1",
        "STATUS-S0",
        "STATUS-S1",
        "LOC-S0",
        "LOC-S1",
        "CAP-M0",
        "CAP-M1",
        "STATUS-M0",
        "STATUS-M1",
        "LOC-M0",
        "LOC-M1",
        "CAP-C0",
        "CAP-C1",
        "STATUS-C0",
        "STATUS-C1",
        "LOC-C0",
        "LOC-C1",
    ],
)
def test_uncertainty_aware_contract_defers_imperfect_evidence(
    results,
    condition_id,
):
    result = by_id(results, condition_id)

    assert (
        result.uncertainty_contract_authority
        == AuthorityState.DEFER
    )


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-S0",
        "CAP-S1",
        "STATUS-S0",
        "STATUS-S1",
        "LOC-S0",
        "LOC-S1",
        "CAP-M0",
        "CAP-M1",
        "STATUS-M0",
        "STATUS-M1",
        "LOC-M0",
        "LOC-M1",
        "CAP-C0",
        "CAP-C1",
        "STATUS-C0",
        "STATUS-C1",
        "LOC-C0",
        "LOC-C1",
    ],
)
def test_dara_dt_defers_imperfect_evidence(
    results,
    condition_id,
):
    result = by_id(results, condition_id)

    assert result.dara_dt_authority == AuthorityState.DEFER


# ---------------------------------------------------------------------------
# Kill Test E
# ---------------------------------------------------------------------------


def test_kill_test_e_compares_all_24_conditions(results):
    comparisons = [
        (
            result.uncertainty_contract_authority,
            result.dara_dt_authority,
        )
        for result in results
    ]

    assert len(comparisons) == 24


def test_uncertainty_contract_and_dara_have_same_binary_intervention(
    results,
):
    """Kill Test E compares intervention behaviour without forcing
    identical authority-state semantics.
    """

    assert all(
        (
            result.uncertainty_contract_authority
            == AuthorityState.ALLOW
        )
        == (
            result.dara_dt_authority
            == AuthorityState.ALLOW
        )
        for result in results
    )


def test_authority_states_differ_only_on_reliable_invalid_cases(results):
    differences = {
        result.condition.condition_id
        for result in results
        if (
            result.uncertainty_contract_authority
            != result.dara_dt_authority
        )
    }

    assert differences == {
        "CAP-R1",
        "STATUS-R1",
        "LOC-R1",
    }


# ---------------------------------------------------------------------------
# Outcome evaluation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "policy_name",
    [
        "no_assurance",
        "global_divergence",
        "direct_contract",
        "uncertainty_contract",
        "dara_dt",
    ],
)
def test_every_policy_produces_outcome_for_all_conditions(
    results,
    policy_name,
):
    outcomes = [
        getattr(result, policy_name)
        for result in results
    ]

    assert len(outcomes) == 24

    assert all(
        outcome.outcome in {
            AssuranceOutcome.TRUE_INTERVENTION,
            AssuranceOutcome.FALSE_INTERVENTION,
            AssuranceOutcome.MISSED_INTERVENTION,
            AssuranceOutcome.CORRECT_NON_INTERVENTION,
        }
        for outcome in outcomes
    )


def test_no_assurance_misses_all_invalid_conditions(results):
    missed = sum(
        result.no_assurance.outcome
        == AssuranceOutcome.MISSED_INTERVENTION
        for result in results
    )

    assert missed == 12


def test_uncertainty_contract_has_no_missed_interventions(results):
    missed = sum(
        result.uncertainty_contract.outcome
        == AssuranceOutcome.MISSED_INTERVENTION
        for result in results
    )

    assert missed == 0


def test_dara_dt_has_no_missed_interventions(results):
    missed = sum(
        result.dara_dt.outcome
        == AssuranceOutcome.MISSED_INTERVENTION
        for result in results
    )

    assert missed == 0


def test_uncertainty_contract_false_interventions_are_explicit(results):
    false_interventions = sum(
        result.uncertainty_contract.outcome
        == AssuranceOutcome.FALSE_INTERVENTION
        for result in results
    )

    # Valid stale, missing and conflicting cases are conservatively
    # deferred. This exposes the autonomy cost of uncertain evidence.
    assert false_interventions == 9


def test_dara_dt_false_interventions_are_explicit(results):
    false_interventions = sum(
        result.dara_dt.outcome
        == AssuranceOutcome.FALSE_INTERVENTION
        for result in results
    )

    assert false_interventions == 9


def test_uncertainty_contract_and_dara_have_identical_binary_outcomes(
    results,
):
    assert all(
        result.uncertainty_contract.outcome
        == result.dara_dt.outcome
        for result in results
    )


# ---------------------------------------------------------------------------
# Scientific-integrity checks
# ---------------------------------------------------------------------------


def test_stale_evidence_can_hide_true_degree_of_physical_divergence(
    results,
):
    result = by_id(results, "CAP-S1")

    assert result.ground_truth.intervention_required is True

    # Physical capacity is 4 while the Twin says 10, but runtime evidence
    # reports 8. The runtime layer therefore sees a smaller mismatch than
    # actually exists.
    assert result.condition.physical_value == 4.0
    assert result.condition.primary_evidence_value == 8.0
    assert result.condition.twin_value == 10.0
    assert result.runtime_divergence_count == 1


def test_stale_evidence_can_create_false_runtime_mismatch(results):
    result = by_id(results, "CAP-S0")

    assert result.ground_truth.intervention_required is False
    assert result.runtime_divergence_count == 1


def test_missing_evidence_is_not_silently_treated_as_physical_truth(
    results,
):
    result = by_id(results, "CAP-M1")

    assert result.ground_truth.intervention_required is True
    assert result.runtime_divergence_count == 0
    assert result.dara_dt_authority == AuthorityState.DEFER


def test_same_imperfect_policy_trades_autonomy_for_safety(results):
    valid = by_id(results, "CAP-S0")
    invalid = by_id(results, "CAP-S1")

    assert valid.dara_dt_authority == AuthorityState.DEFER
    assert invalid.dara_dt_authority == AuthorityState.DEFER

    assert (
        valid.dara_dt.outcome
        == AssuranceOutcome.FALSE_INTERVENTION
    )

    assert (
        invalid.dara_dt.outcome
        == AssuranceOutcome.TRUE_INTERVENTION
    )


def test_exp008_preserves_falsification_result(results):
    """The fair simpler comparator matches DARA-DT at the binary
    intervention level in the frozen 24-condition EXP-008 matrix.

    This result must be preserved rather than engineering an artificial
    performance advantage for DARA-DT.
    """

    assert all(
        result.uncertainty_contract.outcome
        == result.dara_dt.outcome
        for result in results
    )


def test_exp008_does_not_hide_authority_semantic_difference(results):
    """Binary equivalence must not be misreported as identical authority."""

    differences = [
        result
        for result in results
        if (
            result.uncertainty_contract_authority
            != result.dara_dt_authority
        )
    ]

    assert len(differences) == 3

    assert {
        result.condition.condition_id
        for result in differences
    } == {
        "CAP-R1",
        "STATUS-R1",
        "LOC-R1",
    }

    assert all(
        result.uncertainty_contract_authority
        == AuthorityState.RESTRICT
        for result in differences
    )

    assert all(
        result.dara_dt_authority
        == AuthorityState.DEFER
        for result in differences
    )
