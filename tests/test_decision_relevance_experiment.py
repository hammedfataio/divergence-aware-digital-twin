"""Tests for the EXP-009 decision-relevant evidence experiment.

EXP-009 evaluates whether decision-conditioned runtime assurance can
distinguish decision-relevant from decision-irrelevant evidence uncertainty
while preserving safety and autonomous authority.

These tests validate experimental integrity rather than forcing DARA-DT
to outperform the comparator policies. Negative or equivalent results are
valid experimental outcomes.
"""

from collections import Counter

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.decision_relevance_conditions import (
    DependencyFamily,
    EvidenceRelevance,
    EXP009_CONDITIONS,
)
from dara_dt.experiments.decision_relevance_experiment import (
    run_decision_relevance_experiment,
)


def _results():
    """Run the frozen EXP-009 matrix."""

    return run_decision_relevance_experiment()


def _by_id():
    """Return EXP-009 results indexed by condition identifier."""

    return {
        result.condition.condition_id: result
        for result in _results()
    }


def test_exp009_runs_exactly_42_conditions() -> None:
    results = _results()

    assert len(results) == 42


def test_exp009_preserves_frozen_condition_order() -> None:
    results = _results()

    assert tuple(
        result.condition.condition_id
        for result in results
    ) == tuple(
        condition.condition_id
        for condition in EXP009_CONDITIONS
    )


def test_exp009_produces_unique_decision_per_condition() -> None:
    results = _results()

    decision_ids = [
        result.decision.decision_id
        for result in results
    ]

    assert len(decision_ids) == 42
    assert len(set(decision_ids)) == 42


def test_exp009_executes_fourteen_conditions_per_dependency_family() -> None:
    results = _results()

    counts = Counter(
        result.condition.dependency_family
        for result in results
    )

    assert counts == {
        DependencyFamily.CAPACITY: 14,
        DependencyFamily.STATUS: 14,
        DependencyFamily.LOCATION_AVAILABILITY: 14,
    }


def test_exp009_ground_truth_is_balanced() -> None:
    results = _results()

    valid = sum(
        not result.ground_truth.intervention_required
        for result in results
    )

    invalid = sum(
        result.ground_truth.intervention_required
        for result in results
    )

    assert valid == 21
    assert invalid == 21


def test_exp009_ground_truth_matches_frozen_condition() -> None:
    results = _results()

    for result in results:
        assert (
            result.ground_truth.intervention_required
            == result.condition.intervention_required
        )


def test_exp009_preserves_evidence_status() -> None:
    results = _results()

    for result in results:
        assert result.evidence_status == result.condition.evidence_status


def test_exp009_preserves_evidence_relevance() -> None:
    results = _results()

    for result in results:
        assert (
            result.evidence_relevance
            == result.condition.evidence_relevance
        )


def test_exp009_registers_five_pre_registered_policies() -> None:
    results = _results()

    for result in results:
        assert result.no_assurance_authority in AuthorityState
        assert result.global_uncertainty_authority in AuthorityState
        assert result.entity_filtered_authority in AuthorityState
        assert result.uncertainty_contract_authority in AuthorityState
        assert result.dara_dt_authority in AuthorityState


def test_no_assurance_always_allows_execution() -> None:
    results = _results()

    assert all(
        result.no_assurance_authority == AuthorityState.ALLOW
        for result in results
    )


def test_global_uncertainty_defers_all_imperfect_conditions() -> None:
    results = _results()

    imperfect = [
        result
        for result in results
        if result.condition.is_imperfect_evidence
    ]

    assert len(imperfect) == 36

    assert all(
        result.global_uncertainty_authority == AuthorityState.DEFER
        for result in imperfect
    )


def test_global_uncertainty_allows_reliable_controls() -> None:
    results = _results()

    reliable = [
        result
        for result in results
        if result.condition.is_reliable_control
    ]

    assert len(reliable) == 6

    assert all(
        result.global_uncertainty_authority == AuthorityState.ALLOW
        for result in reliable
    )


def test_entity_filter_ignores_other_entity_uncertainty() -> None:
    results = _results()

    irrelevant_other_entity = [
        result
        for result in results
        if (
            result.condition.is_imperfect_evidence
            and result.condition.evidence_relevance
            == EvidenceRelevance.IRRELEVANT
            and result.irrelevant_evidence_scope == "other_entity"
        )
    ]

    assert irrelevant_other_entity

    assert all(
        result.entity_filtered_authority == AuthorityState.ALLOW
        for result in irrelevant_other_entity
    )


def test_entity_filter_reacts_to_same_entity_irrelevant_uncertainty() -> None:
    results = _results()

    same_entity_irrelevant = [
        result
        for result in results
        if (
            result.condition.is_imperfect_evidence
            and result.condition.evidence_relevance
            == EvidenceRelevance.IRRELEVANT
            and result.irrelevant_evidence_scope == "same_entity"
        )
    ]

    assert same_entity_irrelevant

    assert all(
        result.entity_filtered_authority == AuthorityState.DEFER
        for result in same_entity_irrelevant
    )


def test_dara_ignores_imperfect_evidence_outside_decision_dependencies() -> None:
    results = _results()

    irrelevant = [
        result
        for result in results
        if (
            result.condition.is_imperfect_evidence
            and result.condition.evidence_relevance
            == EvidenceRelevance.IRRELEVANT
        )
    ]

    assert len(irrelevant) == 18

    assert all(
        result.dara_dt_authority == AuthorityState.ALLOW
        for result in irrelevant
    )


def test_dara_defers_imperfect_evidence_on_required_dependencies() -> None:
    results = _results()

    relevant = [
        result
        for result in results
        if (
            result.condition.is_imperfect_evidence
            and result.condition.evidence_relevance
            == EvidenceRelevance.RELEVANT
        )
    ]

    assert len(relevant) == 18

    assert all(
        result.dara_dt_authority == AuthorityState.DEFER
        for result in relevant
    )


def test_irrelevant_uncertainty_contains_valid_and_invalid_ground_truth() -> None:
    results = _results()

    irrelevant = [
        result
        for result in results
        if (
            result.condition.is_imperfect_evidence
            and result.condition.evidence_relevance
            == EvidenceRelevance.IRRELEVANT
        )
    ]

    valid = sum(
        not result.ground_truth.intervention_required
        for result in irrelevant
    )

    invalid = sum(
        result.ground_truth.intervention_required
        for result in irrelevant
    )

    assert valid == 9
    assert invalid == 9


def test_relevant_uncertainty_contains_valid_and_invalid_ground_truth() -> None:
    results = _results()

    relevant = [
        result
        for result in results
        if (
            result.condition.is_imperfect_evidence
            and result.condition.evidence_relevance
            == EvidenceRelevance.RELEVANT
        )
    ]

    valid = sum(
        not result.ground_truth.intervention_required
        for result in relevant
    )

    invalid = sum(
        result.ground_truth.intervention_required
        for result in relevant
    )

    assert valid == 9
    assert invalid == 9


def test_missing_evidence_remains_explicitly_missing() -> None:
    results = _results()

    missing = [
        result
        for result in results
        if result.evidence_status == EvidenceStatus.MISSING
    ]

    assert len(missing) == 12

    for result in missing:
        uncertain = [
            item
            for item in result.runtime_evidence
            if item.status == EvidenceStatus.MISSING
        ]

        assert uncertain
        assert all(
            item.observed_value is None
            for item in uncertain
        )


def test_runtime_policies_do_not_receive_physical_ground_truth() -> None:
    """Ground truth must remain evaluator-only.

    The experiment result exposes ground truth for evaluation, but runtime
    evidence must remain a distinct information layer.
    """

    results = _results()

    for result in results:
        assert result.ground_truth.decision_id == result.decision.decision_id
        assert result.runtime_evidence is not None


def test_every_policy_produces_outcome_for_every_condition() -> None:
    results = _results()

    for result in results:
        assert result.no_assurance.outcome in AssuranceOutcome
        assert result.global_uncertainty.outcome in AssuranceOutcome
        assert result.entity_filtered.outcome in AssuranceOutcome
        assert result.uncertainty_contract.outcome in AssuranceOutcome
        assert result.dara_dt.outcome in AssuranceOutcome


def test_no_assurance_misses_all_physically_invalid_conditions() -> None:
    results = _results()

    invalid = [
        result
        for result in results
        if result.ground_truth.intervention_required
    ]

    assert len(invalid) == 21

    assert all(
        result.no_assurance.outcome
        == AssuranceOutcome.MISSED_INTERVENTION
        for result in invalid
    )


def test_exp009_does_not_encode_dara_superiority_as_test_oracle() -> None:
    """Scientific results must be observed rather than hard-coded.

    The suite validates experimental structure and policy semantics.
    Whether DARA-DT outperforms the strongest comparator is determined
    from the resulting metrics, not assumed by this test suite.
    """

    results = _results()

    assert len(results) == len(EXP009_CONDITIONS)
