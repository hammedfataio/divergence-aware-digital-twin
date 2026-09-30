"""Tests for EXP-009 decision-relevance metrics.

These tests verify metric calculation and the pre-registered EXP-009 kill
tests without encoding DARA-DT as the expected winner.

EXP-009 asks whether decision-conditioned runtime assurance provides useful
assurance information beyond simpler global uncertainty, entity filtering,
and uncertainty-aware runtime contracts.
"""

from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.decision_relevance_conditions import (
    DependencyFamily,
    EvidenceRelevance,
)
from dara_dt.experiments.decision_relevance_experiment import (
    run_decision_relevance_experiment,
)
from dara_dt.experiments.decision_relevance_metrics import (
    POLICIES,
    KillTestStatus,
    calculate_exp009_authority_distributions,
    calculate_exp009_kill_tests,
    calculate_exp009_metrics,
    calculate_metrics_by_dependency_family,
    calculate_metrics_by_evidence_relevance,
    calculate_metrics_by_evidence_status,
)


def _results():
    return run_decision_relevance_experiment()


def _metrics_by_policy():
    return {
        metric.policy: metric
        for metric in calculate_exp009_metrics(_results())
    }


def _authority_by_policy():
    return {
        distribution.policy: distribution
        for distribution
        in calculate_exp009_authority_distributions(_results())
    }


def _kill_tests_by_id():
    return {
        result.kill_test: result
        for result in calculate_exp009_kill_tests(_results())
    }


def test_exp009_registers_five_primary_policies() -> None:
    assert POLICIES == (
        "no_assurance",
        "global_uncertainty",
        "entity_filtered",
        "uncertainty_contract",
        "dara_dt",
    )


def test_exp009_aggregate_contains_all_primary_policies() -> None:
    metrics = calculate_exp009_metrics(_results())

    assert len(metrics) == 5

    assert {
        metric.policy
        for metric in metrics
    } == set(POLICIES)


def test_every_policy_uses_all_42_conditions() -> None:
    metrics = calculate_exp009_metrics(_results())

    assert all(
        metric.conditions == 42
        for metric in metrics
    )


def test_every_policy_outcome_counts_sum_to_42() -> None:
    metrics = calculate_exp009_metrics(_results())

    for metric in metrics:
        total = (
            metric.true_interventions
            + metric.false_interventions
            + metric.missed_interventions
            + metric.correct_non_interventions
        )

        assert total == 42


def test_no_assurance_metrics_match_ground_truth_balance() -> None:
    metrics = _metrics_by_policy()["no_assurance"]

    assert metrics.true_interventions == 0
    assert metrics.false_interventions == 0
    assert metrics.missed_interventions == 21
    assert metrics.correct_non_interventions == 21

    assert metrics.accuracy == 0.5
    assert metrics.recall == 0.0
    assert metrics.false_intervention_rate == 0.0
    assert metrics.missed_intervention_rate == 1.0
    assert metrics.autonomy_availability == 1.0


def test_global_uncertainty_intervenes_on_all_36_imperfect_conditions() -> None:
    metrics = _metrics_by_policy()["global_uncertainty"]

    assert (
        metrics.true_interventions
        + metrics.false_interventions
    ) >= 36


def test_authority_distribution_contains_all_primary_policies() -> None:
    distributions = calculate_exp009_authority_distributions(
        _results()
    )

    assert len(distributions) == 5

    assert {
        distribution.policy
        for distribution in distributions
    } == set(POLICIES)


def test_authority_counts_sum_to_42() -> None:
    distributions = calculate_exp009_authority_distributions(
        _results()
    )

    for distribution in distributions:
        total = (
            distribution.allow
            + distribution.restrict
            + distribution.defer
            + distribution.fallback
        )

        assert total == 42


def test_no_assurance_authority_is_always_allow() -> None:
    distribution = _authority_by_policy()["no_assurance"]

    assert distribution.allow == 42
    assert distribution.restrict == 0
    assert distribution.defer == 0
    assert distribution.fallback == 0
    assert distribution.allow_rate == 1.0


def test_evidence_status_breakdown_contains_twenty_rows() -> None:
    grouped = calculate_metrics_by_evidence_status(
        _results()
    )

    assert len(grouped) == 20


def test_each_evidence_status_contains_five_policies() -> None:
    grouped = calculate_metrics_by_evidence_status(
        _results()
    )

    for status in (
        EvidenceStatus.AVAILABLE,
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ):
        subset = [
            item
            for item in grouped
            if item.value == status.value
        ]

        assert len(subset) == 5

        assert {
            item.metrics.policy
            for item in subset
        } == set(POLICIES)


def test_available_evidence_group_contains_six_conditions_per_policy() -> None:
    grouped = calculate_metrics_by_evidence_status(
        _results()
    )

    available = [
        item
        for item in grouped
        if item.value == EvidenceStatus.AVAILABLE.value
    ]

    assert all(
        item.metrics.conditions == 6
        for item in available
    )


def test_each_imperfect_status_contains_twelve_conditions_per_policy() -> None:
    grouped = calculate_metrics_by_evidence_status(
        _results()
    )

    for status in (
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    ):
        subset = [
            item
            for item in grouped
            if item.value == status.value
        ]

        assert all(
            item.metrics.conditions == 12
            for item in subset
        )


def test_dependency_breakdown_contains_fifteen_rows() -> None:
    grouped = calculate_metrics_by_dependency_family(
        _results()
    )

    assert len(grouped) == 15


def test_each_dependency_family_contains_five_policies() -> None:
    grouped = calculate_metrics_by_dependency_family(
        _results()
    )

    for family in (
        DependencyFamily.CAPACITY,
        DependencyFamily.STATUS,
        DependencyFamily.LOCATION_AVAILABILITY,
    ):
        subset = [
            item
            for item in grouped
            if item.value == family.value
        ]

        assert len(subset) == 5

        assert {
            item.metrics.policy
            for item in subset
        } == set(POLICIES)


def test_each_dependency_family_contains_fourteen_conditions_per_policy() -> None:
    grouped = calculate_metrics_by_dependency_family(
        _results()
    )

    for family in (
        DependencyFamily.CAPACITY,
        DependencyFamily.STATUS,
        DependencyFamily.LOCATION_AVAILABILITY,
    ):
        subset = [
            item
            for item in grouped
            if item.value == family.value
        ]

        assert all(
            item.metrics.conditions == 14
            for item in subset
        )


def test_evidence_relevance_breakdown_contains_ten_rows() -> None:
    grouped = calculate_metrics_by_evidence_relevance(
        _results()
    )

    assert len(grouped) == 10


def test_relevance_breakdown_contains_five_policies_per_group() -> None:
    grouped = calculate_metrics_by_evidence_relevance(
        _results()
    )

    for relevance in (
        EvidenceRelevance.RELEVANT,
        EvidenceRelevance.IRRELEVANT,
    ):
        subset = [
            item
            for item in grouped
            if item.value == relevance.value
        ]

        assert len(subset) == 5

        assert {
            item.metrics.policy
            for item in subset
        } == set(POLICIES)


def test_each_imperfect_relevance_group_contains_eighteen_conditions() -> None:
    grouped = calculate_metrics_by_evidence_relevance(
        _results()
    )

    for relevance in (
        EvidenceRelevance.RELEVANT,
        EvidenceRelevance.IRRELEVANT,
    ):
        subset = [
            item
            for item in grouped
            if item.value == relevance.value
        ]

        assert all(
            item.metrics.conditions == 18
            for item in subset
        )


def test_kill_test_evaluation_contains_six_registered_tests() -> None:
    kill_tests = calculate_exp009_kill_tests(
        _results()
    )

    assert len(kill_tests) == 6

    assert {
        result.kill_test
        for result in kill_tests
    } == {
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
    }


def test_every_kill_test_has_explicit_status() -> None:
    kill_tests = calculate_exp009_kill_tests(
        _results()
    )

    for result in kill_tests:
        assert result.status in KillTestStatus


def test_kill_test_a_is_evaluated_from_autonomy_advantage() -> None:
    result = _kill_tests_by_id()["A"]

    assert result.name == "No Autonomy Advantage"

    assert result.status in {
        KillTestStatus.TRIGGERED,
        KillTestStatus.NOT_TRIGGERED,
    }


def test_kill_test_b_is_evaluated_from_safety_degradation() -> None:
    result = _kill_tests_by_id()["B"]

    assert result.name == "Safety Degradation"

    assert result.status in {
        KillTestStatus.TRIGGERED,
        KillTestStatus.NOT_TRIGGERED,
    }


def test_kill_test_c_is_evaluated_from_runtime_contract_equivalence() -> None:
    result = _kill_tests_by_id()["C"]

    assert result.name == "Runtime Contract Equivalence"

    assert result.status in {
        KillTestStatus.TRIGGERED,
        KillTestStatus.NOT_TRIGGERED,
    }


def test_kill_test_d_is_evaluated_across_dependency_families() -> None:
    result = _kill_tests_by_id()["D"]

    assert result.name == "Capacity-Only Effect"

    assert result.status in {
        KillTestStatus.TRIGGERED,
        KillTestStatus.NOT_TRIGGERED,
    }


def test_kill_test_e_is_evaluated_from_runtime_information_only() -> None:
    result = _kill_tests_by_id()["E"]

    assert result.name == "Evidence Privilege"

    assert result.status in {
        KillTestStatus.TRIGGERED,
        KillTestStatus.NOT_TRIGGERED,
    }


def test_kill_test_f_is_evaluated_against_entity_filtering() -> None:
    result = _kill_tests_by_id()["F"]

    assert result.name == "Trivial Entity Filtering"

    assert result.status in {
        KillTestStatus.TRIGGERED,
        KillTestStatus.NOT_TRIGGERED,
    }


def test_kill_test_results_contain_explanatory_evidence() -> None:
    kill_tests = calculate_exp009_kill_tests(
        _results()
    )

    for result in kill_tests:
        assert result.evidence
        assert isinstance(result.evidence, str)


def test_metrics_do_not_require_expected_dara_superiority() -> None:
    """The metrics layer must report results rather than encode a winner."""

    metrics = calculate_exp009_metrics(
        _results()
    )

    assert len(metrics) == len(POLICIES)
