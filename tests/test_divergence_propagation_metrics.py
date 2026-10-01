"""Tests for EXP-010 divergence-propagation metrics.

The tests validate quantitative accounting, subgroup analysis,
authority distributions, P3/P4 equivalence, and the preregistered
kill-test framework.

The suite intentionally accepts a null/equivalence result between the
strong dependency-aware composed runtime contract (P3) and
propagation-aware DARA-DT (P4).
"""

from __future__ import annotations

import pytest

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.divergence_propagation_experiment import (
    run_exp010,
)
from dara_dt.experiments.divergence_propagation_metrics import (
    POLICIES,
    KillTestStatus,
    build_exp010_report,
    calculate_authority_distribution,
    calculate_exp010_authority_distributions,
    calculate_exp010_kill_tests,
    calculate_exp010_metrics,
    calculate_metrics_by_evidence_status,
    calculate_metrics_by_family,
    calculate_p3_p4_equivalence,
    calculate_policy_metrics,
    calculate_propagation_summary,
)


@pytest.fixture(scope="module")
def results():
    """Execute the frozen EXP-010 matrix once."""

    return run_exp010()


@pytest.fixture(scope="module")
def metrics(results):
    """Calculate aggregate policy metrics once."""

    return calculate_exp010_metrics(results)


@pytest.fixture(scope="module")
def metrics_by_policy(metrics):
    """Index aggregate metrics by policy name."""

    return {
        metric.policy: metric
        for metric in metrics
    }


@pytest.fixture(scope="module")
def report(results):
    """Build the complete EXP-010 report once."""

    return build_exp010_report(results)


def test_exp010_registers_exactly_five_primary_policies() -> None:
    """EXP-010 must preserve the frozen five-policy comparison."""

    assert POLICIES == (
        "no_assurance",
        "local_contract",
        "global_assurance",
        "composed_contract",
        "dara_dt",
    )


def test_exp010_metrics_contains_all_primary_policies(metrics) -> None:
    """Every frozen comparator must appear exactly once."""

    assert len(metrics) == 5

    assert {
        metric.policy
        for metric in metrics
    } == set(POLICIES)


def test_every_policy_uses_all_30_conditions(metrics) -> None:
    """No policy may be evaluated on a reduced matrix."""

    assert all(
        metric.conditions == 30
        for metric in metrics
    )


def test_outcome_counts_sum_to_30_for_every_policy(metrics) -> None:
    """TI/FI/MI/CNI accounting must cover the complete matrix."""

    for metric in metrics:
        assert (
            metric.true_interventions
            + metric.false_interventions
            + metric.missed_interventions
            + metric.correct_non_interventions
            == 30
        )


def test_no_assurance_metrics_match_frozen_ground_truth(
    metrics_by_policy,
) -> None:
    """P0 must miss all 19 required interventions."""

    metric = metrics_by_policy["no_assurance"]

    assert metric.true_interventions == 0
    assert metric.false_interventions == 0
    assert metric.missed_interventions == 19
    assert metric.correct_non_interventions == 11

    assert metric.accuracy == pytest.approx(
        11 / 30
    )

    assert metric.precision == 0.0
    assert metric.recall == 0.0

    assert metric.false_intervention_rate == 0.0
    assert metric.missed_intervention_rate == 1.0
    assert metric.autonomy_availability == 1.0


def test_metric_accuracy_matches_outcome_counts(metrics) -> None:
    """Accuracy must be derived directly from TI + CNI."""

    for metric in metrics:
        expected = (
            metric.true_interventions
            + metric.correct_non_interventions
        ) / metric.conditions

        assert metric.accuracy == pytest.approx(
            expected
        )


def test_metric_precision_matches_outcome_counts(metrics) -> None:
    """Precision must use TI / (TI + FI)."""

    for metric in metrics:
        denominator = (
            metric.true_interventions
            + metric.false_interventions
        )

        expected = (
            metric.true_interventions / denominator
            if denominator
            else 0.0
        )

        assert metric.precision == pytest.approx(
            expected
        )


def test_metric_recall_matches_outcome_counts(metrics) -> None:
    """Recall must use TI / (TI + MI)."""

    for metric in metrics:
        denominator = (
            metric.true_interventions
            + metric.missed_interventions
        )

        expected = (
            metric.true_interventions / denominator
            if denominator
            else 0.0
        )

        assert metric.recall == pytest.approx(
            expected
        )


def test_false_intervention_rate_matches_valid_cases(metrics) -> None:
    """FI rate must use FI / (FI + CNI)."""

    for metric in metrics:
        denominator = (
            metric.false_interventions
            + metric.correct_non_interventions
        )

        expected = (
            metric.false_interventions / denominator
            if denominator
            else 0.0
        )

        assert metric.false_intervention_rate == pytest.approx(
            expected
        )


def test_missed_intervention_rate_matches_invalid_cases(metrics) -> None:
    """MI rate must use MI / (TI + MI)."""

    for metric in metrics:
        denominator = (
            metric.true_interventions
            + metric.missed_interventions
        )

        expected = (
            metric.missed_interventions / denominator
            if denominator
            else 0.0
        )

        assert metric.missed_intervention_rate == pytest.approx(
            expected
        )


def test_autonomy_availability_matches_allow_outcomes(metrics) -> None:
    """Autonomy is available for MI + CNI outcomes."""

    for metric in metrics:
        expected = (
            metric.missed_interventions
            + metric.correct_non_interventions
        ) / metric.conditions

        assert metric.autonomy_availability == pytest.approx(
            expected
        )


def test_policy_metric_helper_handles_empty_outcomes() -> None:
    """Metric calculation must safely handle an empty subgroup."""

    metric = calculate_policy_metrics(
        policy="empty",
        outcomes=(),
    )

    assert metric.conditions == 0
    assert metric.true_interventions == 0
    assert metric.false_interventions == 0
    assert metric.missed_interventions == 0
    assert metric.correct_non_interventions == 0

    assert metric.accuracy == 0.0
    assert metric.precision == 0.0
    assert metric.recall == 0.0
    assert metric.false_intervention_rate == 0.0
    assert metric.missed_intervention_rate == 0.0
    assert metric.autonomy_availability == 0.0


def test_authority_distribution_contains_all_policies(results) -> None:
    """Authority reporting must cover all five policies."""

    distributions = (
        calculate_exp010_authority_distributions(
            results
        )
    )

    assert len(distributions) == 5

    assert {
        distribution.policy
        for distribution in distributions
    } == set(POLICIES)


def test_authority_counts_sum_to_30(results) -> None:
    """Every policy must produce one authority state per condition."""

    distributions = (
        calculate_exp010_authority_distributions(
            results
        )
    )

    for distribution in distributions:
        assert (
            distribution.allow
            + distribution.restrict
            + distribution.defer
            + distribution.fallback
            == 30
        )


def test_authority_rates_sum_to_one(results) -> None:
    """Authority-state proportions must form a complete distribution."""

    distributions = (
        calculate_exp010_authority_distributions(
            results
        )
    )

    for distribution in distributions:
        assert (
            distribution.allow_rate
            + distribution.restrict_rate
            + distribution.defer_rate
            + distribution.fallback_rate
        ) == pytest.approx(1.0)


def test_no_assurance_authority_is_always_allow(results) -> None:
    """P0 must preserve unconditional autonomous authority."""

    distributions = (
        calculate_exp010_authority_distributions(
            results
        )
    )

    distribution = next(
        item
        for item in distributions
        if item.policy == "no_assurance"
    )

    assert distribution.allow == 30
    assert distribution.restrict == 0
    assert distribution.defer == 0
    assert distribution.fallback == 0

    assert distribution.allow_rate == 1.0


def test_authority_distribution_helper_handles_empty_input() -> None:
    """Authority calculation must safely handle an empty subgroup."""

    distribution = calculate_authority_distribution(
        policy="empty",
        authorities=(),
    )

    assert distribution.conditions == 0
    assert distribution.allow == 0
    assert distribution.restrict == 0
    assert distribution.defer == 0
    assert distribution.fallback == 0

    assert distribution.allow_rate == 0.0
    assert distribution.restrict_rate == 0.0
    assert distribution.defer_rate == 0.0
    assert distribution.fallback_rate == 0.0


def test_family_metrics_contains_five_families(results) -> None:
    """The five frozen propagation families must be represented."""

    grouped = calculate_metrics_by_family(
        results
    )

    assert len(grouped) == 25

    values = {
        item.value
        for item in grouped
    }

    assert values == {
        "F0",
        "F1",
        "F2",
        "F3",
        "F4",
    }


def test_every_family_contains_six_conditions_per_policy(results) -> None:
    """Each frozen family contains exactly six conditions."""

    grouped = calculate_metrics_by_family(
        results
    )

    assert all(
        item.metrics.conditions == 6
        for item in grouped
    )


def test_family_metrics_contains_all_policies(results) -> None:
    """Each family must evaluate all five comparators."""

    grouped = calculate_metrics_by_family(
        results
    )

    for family in {
        "F0",
        "F1",
        "F2",
        "F3",
        "F4",
    }:
        policies = {
            item.metrics.policy
            for item in grouped
            if item.value == family
        }

        assert policies == set(POLICIES)


def test_evidence_status_metrics_preserve_frozen_counts(results) -> None:
    """Evidence subgroups must preserve the 15/5/5/5 design."""

    grouped = calculate_metrics_by_evidence_status(
        results
    )

    expected_counts = {
        "available": 15,
        "stale": 5,
        "missing": 5,
        "conflicting": 5,
    }

    for status, expected in expected_counts.items():
        status_metrics = [
            item.metrics
            for item in grouped
            if item.value == status
        ]

        assert len(status_metrics) == 5

        assert all(
            metric.conditions == expected
            for metric in status_metrics
        )


def test_evidence_status_metrics_contains_20_rows(results) -> None:
    """Four evidence states × five policies = twenty rows."""

    grouped = calculate_metrics_by_evidence_status(
        results
    )

    assert len(grouped) == 20


def test_propagation_summary_uses_complete_matrix(results) -> None:
    """Propagation summary must account for all 30 conditions."""

    summary = calculate_propagation_summary(
        results
    )

    assert summary.conditions == 30


def test_propagation_summary_detects_propagating_families(results) -> None:
    """F3 and F4 provide the twelve propagating conditions."""

    summary = calculate_propagation_summary(
        results
    )

    assert summary.propagating_conditions == 12
    assert summary.compound_propagation_conditions == 6


def test_propagation_summary_detects_non_propagating_divergence(results) -> None:
    """The summary must retain non-propagating divergence controls."""

    summary = calculate_propagation_summary(
        results
    )

    assert (
        summary.non_propagating_divergence_conditions
        > 0
    )


def test_all_propagating_conditions_require_intervention(results) -> None:
    """Frozen F3/F4 propagation cases are physically invalid."""

    summary = calculate_propagation_summary(
        results
    )

    assert (
        summary.propagating_interventions_required
        == summary.propagating_conditions
    )


def test_non_propagating_divergence_contains_no_required_intervention(
    results,
) -> None:
    """Non-propagating divergence must remain a valid control."""

    summary = calculate_propagation_summary(
        results
    )

    assert (
        summary.non_propagating_interventions_required
        == 0
    )


def test_p3_p4_equivalence_uses_all_30_conditions(results) -> None:
    """Equal-evidence comparison must cover the complete matrix."""

    equivalence = calculate_p3_p4_equivalence(
        results
    )

    assert equivalence.conditions == 30


def test_p3_p4_are_fully_authority_equivalent(results) -> None:
    """Current frozen matrix produces complete authority equivalence."""

    equivalence = calculate_p3_p4_equivalence(
        results
    )

    assert equivalence.authority_matches == 30
    assert equivalence.authority_match_rate == 1.0
    assert equivalence.fully_authority_equivalent


def test_p3_p4_are_fully_outcome_equivalent(results) -> None:
    """Current frozen matrix produces complete binary equivalence."""

    equivalence = calculate_p3_p4_equivalence(
        results
    )

    assert equivalence.outcome_matches == 30
    assert equivalence.outcome_match_rate == 1.0
    assert equivalence.fully_outcome_equivalent


def test_p3_p4_aggregate_metrics_are_identical(
    metrics_by_policy,
) -> None:
    """Equal-evidence P3/P4 comparison must retain the observed tie."""

    p3 = metrics_by_policy["composed_contract"]
    p4 = metrics_by_policy["dara_dt"]

    assert p3.true_interventions == p4.true_interventions
    assert p3.false_interventions == p4.false_interventions
    assert p3.missed_interventions == p4.missed_interventions
    assert (
        p3.correct_non_interventions
        == p4.correct_non_interventions
    )

    assert p3.accuracy == p4.accuracy
    assert p3.precision == p4.precision
    assert p3.recall == p4.recall

    assert (
        p3.false_intervention_rate
        == p4.false_intervention_rate
    )

    assert (
        p3.missed_intervention_rate
        == p4.missed_intervention_rate
    )

    assert (
        p3.autonomy_availability
        == p4.autonomy_availability
    )


def test_kill_test_suite_contains_exactly_ten_tests(results) -> None:
    """EXP-010 must evaluate preregistered kill tests A-J."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    assert len(kill_tests) == 10


def test_kill_test_identifiers_are_a_through_j(results) -> None:
    """Kill-test identifiers must remain stable."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    assert tuple(
        test.kill_test
        for test in kill_tests
    ) == tuple("ABCDEFGHIJ")


def test_every_kill_test_has_explanatory_evidence(results) -> None:
    """A kill-test result must remain interpretable."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    for kill_test in kill_tests:
        assert kill_test.name
        assert kill_test.evidence


def test_kill_test_a_triggers_on_p3_p4_equivalence(results) -> None:
    """Full composed-contract equivalence triggers Kill Test A."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    test_a = next(
        test
        for test in kill_tests
        if test.kill_test == "A"
    )

    assert test_a.status is KillTestStatus.TRIGGERED


def test_kill_test_c_triggers_when_divergence_provenance_adds_no_outcome_value(
    results,
) -> None:
    """Current P3/P4 equivalence triggers divergence-value test C."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    test_c = next(
        test
        for test in kill_tests
        if test.kill_test == "C"
    )

    assert test_c.status is KillTestStatus.TRIGGERED


def test_evidence_privilege_kill_test_does_not_trigger(results) -> None:
    """Equal observable evidence must protect comparative validity."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    test_e = next(
        test
        for test in kill_tests
        if test.kill_test == "E"
    )

    assert test_e.status is KillTestStatus.NOT_TRIGGERED


def test_safety_degradation_kill_test_does_not_trigger(results) -> None:
    """P4 must not gain autonomy by increasing missed interventions."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    test_g = next(
        test
        for test in kill_tests
        if test.kill_test == "G"
    )

    assert test_g.status is KillTestStatus.NOT_TRIGGERED


def test_propagation_overreach_kill_test_does_not_trigger(results) -> None:
    """DARA-DT must not intervene falsely on F2 propagation controls."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    test_i = next(
        test
        for test in kill_tests
        if test.kill_test == "I"
    )

    assert test_i.status is KillTestStatus.NOT_TRIGGERED


def test_compound_dependency_equivalence_triggers_kill_test_j(
    results,
) -> None:
    """P3/P4 equivalence in F4 triggers compound-collapse test J."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    test_j = next(
        test
        for test in kill_tests
        if test.kill_test == "J"
    )

    assert test_j.status is KillTestStatus.TRIGGERED


def test_kill_test_statuses_are_valid_enum_members(results) -> None:
    """Every kill test must return a declared status."""

    kill_tests = calculate_exp010_kill_tests(
        results
    )

    for kill_test in kill_tests:
        assert kill_test.status in {
            KillTestStatus.TRIGGERED,
            KillTestStatus.NOT_TRIGGERED,
            KillTestStatus.NOT_EVALUABLE,
        }


def test_report_contains_five_policy_metrics(report) -> None:
    """Complete report must expose aggregate policy metrics."""

    assert len(report.policy_metrics) == 5


def test_report_contains_five_authority_distributions(report) -> None:
    """Complete report must expose authority distributions."""

    assert len(report.authority_distributions) == 5


def test_report_contains_25_family_metric_rows(report) -> None:
    """Five families × five policies must be reported."""

    assert len(report.family_metrics) == 25


def test_report_contains_20_evidence_status_rows(report) -> None:
    """Four evidence states × five policies must be reported."""

    assert len(report.evidence_status_metrics) == 20


def test_report_contains_propagation_summary(report) -> None:
    """Complete report must retain propagation-specific evidence."""

    assert report.propagation_summary.conditions == 30


def test_report_contains_p3_p4_equivalence(report) -> None:
    """Complete report must explicitly expose comparator equivalence."""

    assert (
        report.p3_p4_equivalence.conditions
        == 30
    )


def test_report_contains_all_ten_kill_tests(report) -> None:
    """Complete report must expose all preregistered kill tests."""

    assert len(report.kill_tests) == 10


def test_report_does_not_encode_dara_as_required_winner(report) -> None:
    """A valid EXP-010 report must support the observed null result."""

    assert (
        report.p3_p4_equivalence.fully_authority_equivalent
    )

    assert (
        report.p3_p4_equivalence.fully_outcome_equivalent
    )


def test_direct_metric_calculation_known_example() -> None:
    """Metric equations are verified independently of EXP-010."""

    outcomes = (
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.TRUE_INTERVENTION,
        AssuranceOutcome.FALSE_INTERVENTION,
        AssuranceOutcome.MISSED_INTERVENTION,
        AssuranceOutcome.CORRECT_NON_INTERVENTION,
    )

    metric = calculate_policy_metrics(
        policy="example",
        outcomes=outcomes,
    )

    assert metric.conditions == 5

    assert metric.true_interventions == 2
    assert metric.false_interventions == 1
    assert metric.missed_interventions == 1
    assert metric.correct_non_interventions == 1

    assert metric.accuracy == pytest.approx(
        3 / 5
    )

    assert metric.precision == pytest.approx(
        2 / 3
    )

    assert metric.recall == pytest.approx(
        2 / 3
    )

    assert metric.false_intervention_rate == pytest.approx(
        1 / 2
    )

    assert metric.missed_intervention_rate == pytest.approx(
        1 / 3
    )

    assert metric.autonomy_availability == pytest.approx(
        2 / 5
    )


def test_direct_authority_distribution_known_example() -> None:
    """Authority equations are verified independently of EXP-010."""

    authorities = (
        AuthorityState.ALLOW,
        AuthorityState.ALLOW,
        AuthorityState.RESTRICT,
        AuthorityState.DEFER,
        AuthorityState.FALLBACK,
    )

    distribution = calculate_authority_distribution(
        policy="example",
        authorities=authorities,
    )

    assert distribution.conditions == 5

    assert distribution.allow == 2
    assert distribution.restrict == 1
    assert distribution.defer == 1
    assert distribution.fallback == 1

    assert distribution.allow_rate == pytest.approx(
        2 / 5
    )

    assert distribution.restrict_rate == pytest.approx(
        1 / 5
    )

    assert distribution.defer_rate == pytest.approx(
        1 / 5
    )

    assert distribution.fallback_rate == pytest.approx(
        1 / 5
    )
