"""Tests for EXP-008 aggregate and grouped metrics."""

import pytest

from dara_dt.assurance.model import AuthorityState
from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.cross_dependency_conditions import DependencyFamily
from dara_dt.experiments.imperfect_evidence_experiment import (
    run_imperfect_evidence_experiment,
)
from dara_dt.experiments.imperfect_evidence_metrics import (
    POLICIES,
    calculate_authority_distribution,
    calculate_exp008_authority_distributions,
    calculate_exp008_metrics,
    calculate_metrics_by_dependency_family,
    calculate_metrics_by_evidence_status,
    calculate_policy_metrics,
)


@pytest.fixture(scope="module")
def results():
    """Execute the frozen 24-condition EXP-008 matrix once."""

    return run_imperfect_evidence_experiment()


@pytest.fixture(scope="module")
def aggregate(results):
    """Return aggregate policy metrics."""

    return calculate_exp008_metrics(results)


@pytest.fixture(scope="module")
def authority(results):
    """Return authority-state distributions."""

    return calculate_exp008_authority_distributions(results)


@pytest.fixture(scope="module")
def by_evidence(results):
    """Return metrics grouped by evidence status."""

    return calculate_metrics_by_evidence_status(results)


@pytest.fixture(scope="module")
def by_dependency(results):
    """Return metrics grouped by dependency family."""

    return calculate_metrics_by_dependency_family(results)


def metric_for(metrics, policy):
    """Return aggregate metrics for one policy."""

    for metric in metrics:
        if metric.policy == policy:
            return metric

    raise AssertionError(f"Unknown policy: {policy}")


def authority_for(distributions, policy):
    """Return authority distribution for one policy."""

    for distribution in distributions:
        if distribution.policy == policy:
            return distribution

    raise AssertionError(f"Unknown policy: {policy}")


def grouped_metric(grouped, value, policy):
    """Return one grouped metric result."""

    for item in grouped:
        if (
            item.value == value
            and item.metrics.policy == policy
        ):
            return item.metrics

    raise AssertionError(
        f"Unknown grouped metric: value={value!r}, policy={policy!r}"
    )


# ---------------------------------------------------------------------------
# Policy registration
# ---------------------------------------------------------------------------


def test_exp008_registers_five_policies():
    assert POLICIES == (
        "no_assurance",
        "global_divergence",
        "direct_contract",
        "uncertainty_contract",
        "dara_dt",
    )


def test_aggregate_contains_all_five_policies(aggregate):
    assert tuple(metric.policy for metric in aggregate) == POLICIES


def test_each_aggregate_policy_uses_24_conditions(aggregate):
    assert all(
        metric.conditions == 24
        for metric in aggregate
    )


# ---------------------------------------------------------------------------
# Aggregate outcome accounting
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "policy",
    POLICIES,
)
def test_outcome_counts_sum_to_24(aggregate, policy):
    metric = metric_for(aggregate, policy)

    total = (
        metric.true_interventions
        + metric.false_interventions
        + metric.missed_interventions
        + metric.correct_non_interventions
    )

    assert total == 24


def test_no_assurance_aggregate_counts(aggregate):
    metric = metric_for(
        aggregate,
        "no_assurance",
    )

    assert metric.true_interventions == 0
    assert metric.false_interventions == 0
    assert metric.missed_interventions == 12
    assert metric.correct_non_interventions == 12

    assert metric.accuracy == pytest.approx(0.5)
    assert metric.precision == pytest.approx(0.0)
    assert metric.recall == pytest.approx(0.0)
    assert metric.false_intervention_rate == pytest.approx(0.0)
    assert metric.missed_intervention_rate == pytest.approx(1.0)
    assert metric.autonomy_availability == pytest.approx(1.0)


def test_uncertainty_contract_aggregate_counts(aggregate):
    metric = metric_for(
        aggregate,
        "uncertainty_contract",
    )

    assert metric.true_interventions == 12
    assert metric.false_interventions == 9
    assert metric.missed_interventions == 0
    assert metric.correct_non_interventions == 3

    assert metric.accuracy == pytest.approx(15 / 24)
    assert metric.precision == pytest.approx(12 / 21)
    assert metric.recall == pytest.approx(1.0)
    assert metric.false_intervention_rate == pytest.approx(9 / 12)
    assert metric.missed_intervention_rate == pytest.approx(0.0)
    assert metric.autonomy_availability == pytest.approx(3 / 24)


def test_dara_dt_aggregate_counts(aggregate):
    metric = metric_for(
        aggregate,
        "dara_dt",
    )

    assert metric.true_interventions == 12
    assert metric.false_interventions == 9
    assert metric.missed_interventions == 0
    assert metric.correct_non_interventions == 3

    assert metric.accuracy == pytest.approx(15 / 24)
    assert metric.precision == pytest.approx(12 / 21)
    assert metric.recall == pytest.approx(1.0)
    assert metric.false_intervention_rate == pytest.approx(9 / 12)
    assert metric.missed_intervention_rate == pytest.approx(0.0)
    assert metric.autonomy_availability == pytest.approx(3 / 24)


def test_dara_and_uncertainty_contract_have_equal_binary_metrics(
    aggregate,
):
    contract = metric_for(
        aggregate,
        "uncertainty_contract",
    )

    dara = metric_for(
        aggregate,
        "dara_dt",
    )

    assert dara.true_interventions == contract.true_interventions
    assert dara.false_interventions == contract.false_interventions
    assert dara.missed_interventions == contract.missed_interventions
    assert (
        dara.correct_non_interventions
        == contract.correct_non_interventions
    )

    assert dara.accuracy == pytest.approx(contract.accuracy)
    assert dara.precision == pytest.approx(contract.precision)
    assert dara.recall == pytest.approx(contract.recall)

    assert dara.false_intervention_rate == pytest.approx(
        contract.false_intervention_rate
    )

    assert dara.missed_intervention_rate == pytest.approx(
        contract.missed_intervention_rate
    )

    assert dara.autonomy_availability == pytest.approx(
        contract.autonomy_availability
    )


# ---------------------------------------------------------------------------
# Metric mathematics
# ---------------------------------------------------------------------------


def test_precision_denominator_is_all_interventions(aggregate):
    metric = metric_for(
        aggregate,
        "dara_dt",
    )

    expected = (
        metric.true_interventions
        / (
            metric.true_interventions
            + metric.false_interventions
        )
    )

    assert metric.precision == pytest.approx(expected)


def test_recall_denominator_is_required_interventions(aggregate):
    metric = metric_for(
        aggregate,
        "dara_dt",
    )

    expected = (
        metric.true_interventions
        / (
            metric.true_interventions
            + metric.missed_interventions
        )
    )

    assert metric.recall == pytest.approx(expected)


def test_false_intervention_rate_uses_valid_conditions(aggregate):
    metric = metric_for(
        aggregate,
        "dara_dt",
    )

    expected = (
        metric.false_interventions
        / (
            metric.false_interventions
            + metric.correct_non_interventions
        )
    )

    assert metric.false_intervention_rate == pytest.approx(expected)


def test_missed_intervention_rate_uses_invalid_conditions(aggregate):
    metric = metric_for(
        aggregate,
        "no_assurance",
    )

    expected = (
        metric.missed_interventions
        / (
            metric.true_interventions
            + metric.missed_interventions
        )
    )

    assert metric.missed_intervention_rate == pytest.approx(expected)


def test_autonomy_availability_matches_allow_outcomes(aggregate):
    metric = metric_for(
        aggregate,
        "dara_dt",
    )

    expected = (
        metric.missed_interventions
        + metric.correct_non_interventions
    ) / metric.conditions

    assert metric.autonomy_availability == pytest.approx(expected)


# ---------------------------------------------------------------------------
# Authority-state distributions
# ---------------------------------------------------------------------------


def test_authority_distribution_contains_all_policies(authority):
    assert tuple(
        distribution.policy
        for distribution in authority
    ) == POLICIES


@pytest.mark.parametrize(
    "policy",
    POLICIES,
)
def test_authority_counts_sum_to_24(authority, policy):
    distribution = authority_for(
        authority,
        policy,
    )

    assert (
        distribution.allow
        + distribution.restrict
        + distribution.defer
        + distribution.fallback
    ) == 24


def test_no_assurance_always_allows(authority):
    distribution = authority_for(
        authority,
        "no_assurance",
    )

    assert distribution.allow == 24
    assert distribution.restrict == 0
    assert distribution.defer == 0
    assert distribution.fallback == 0

    assert distribution.allow_rate == pytest.approx(1.0)


def test_uncertainty_contract_authority_distribution(authority):
    distribution = authority_for(
        authority,
        "uncertainty_contract",
    )

    # Three reliable valid cases are allowed.
    # Three reliable invalid cases are restricted.
    # Eighteen stale/missing/conflicting cases are deferred.
    assert distribution.allow == 3
    assert distribution.restrict == 3
    assert distribution.defer == 18
    assert distribution.fallback == 0

    assert distribution.allow_rate == pytest.approx(3 / 24)
    assert distribution.restrict_rate == pytest.approx(3 / 24)
    assert distribution.defer_rate == pytest.approx(18 / 24)


def test_dara_authority_distribution(authority):
    distribution = authority_for(
        authority,
        "dara_dt",
    )

    # DARA-DT allows the three reliable valid cases and defers the
    # remaining 21 conditions, including reliable-invalid cases.
    assert distribution.allow == 3
    assert distribution.restrict == 0
    assert distribution.defer == 21
    assert distribution.fallback == 0

    assert distribution.allow_rate == pytest.approx(3 / 24)
    assert distribution.defer_rate == pytest.approx(21 / 24)


def test_authority_semantics_differ_despite_binary_equivalence(
    authority,
):
    contract = authority_for(
        authority,
        "uncertainty_contract",
    )

    dara = authority_for(
        authority,
        "dara_dt",
    )

    assert contract.allow == dara.allow == 3

    assert contract.restrict == 3
    assert dara.restrict == 0

    assert contract.defer == 18
    assert dara.defer == 21


# ---------------------------------------------------------------------------
# Evidence-status breakdown
# ---------------------------------------------------------------------------


def test_evidence_breakdown_contains_20_rows(by_evidence):
    assert len(by_evidence) == 20


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.AVAILABLE.value,
        EvidenceStatus.STALE.value,
        EvidenceStatus.MISSING.value,
        EvidenceStatus.CONFLICTING.value,
    ],
)
def test_each_evidence_group_contains_five_policies(
    by_evidence,
    status,
):
    policies = {
        item.metrics.policy
        for item in by_evidence
        if item.value == status
    }

    assert policies == set(POLICIES)


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.AVAILABLE.value,
        EvidenceStatus.STALE.value,
        EvidenceStatus.MISSING.value,
        EvidenceStatus.CONFLICTING.value,
    ],
)
def test_each_evidence_policy_group_has_six_conditions(
    by_evidence,
    status,
):
    for policy in POLICIES:
        metric = grouped_metric(
            by_evidence,
            status,
            policy,
        )

        assert metric.conditions == 6


def test_dara_reliable_evidence_metrics(by_evidence):
    metric = grouped_metric(
        by_evidence,
        EvidenceStatus.AVAILABLE.value,
        "dara_dt",
    )

    assert metric.true_interventions == 3
    assert metric.false_interventions == 0
    assert metric.missed_interventions == 0
    assert metric.correct_non_interventions == 3

    assert metric.accuracy == pytest.approx(1.0)
    assert metric.precision == pytest.approx(1.0)
    assert metric.recall == pytest.approx(1.0)
    assert metric.autonomy_availability == pytest.approx(0.5)


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.STALE.value,
        EvidenceStatus.MISSING.value,
        EvidenceStatus.CONFLICTING.value,
    ],
)
def test_dara_imperfect_evidence_is_conservative(
    by_evidence,
    status,
):
    metric = grouped_metric(
        by_evidence,
        status,
        "dara_dt",
    )

    assert metric.true_interventions == 3
    assert metric.false_interventions == 3
    assert metric.missed_interventions == 0
    assert metric.correct_non_interventions == 0

    assert metric.accuracy == pytest.approx(0.5)
    assert metric.precision == pytest.approx(0.5)
    assert metric.recall == pytest.approx(1.0)
    assert metric.false_intervention_rate == pytest.approx(1.0)
    assert metric.missed_intervention_rate == pytest.approx(0.0)
    assert metric.autonomy_availability == pytest.approx(0.0)


@pytest.mark.parametrize(
    "status",
    [
        EvidenceStatus.AVAILABLE.value,
        EvidenceStatus.STALE.value,
        EvidenceStatus.MISSING.value,
        EvidenceStatus.CONFLICTING.value,
    ],
)
def test_dara_and_uncertainty_contract_match_by_evidence_status(
    by_evidence,
    status,
):
    contract = grouped_metric(
        by_evidence,
        status,
        "uncertainty_contract",
    )

    dara = grouped_metric(
        by_evidence,
        status,
        "dara_dt",
    )

    assert (
        dara.true_interventions
        == contract.true_interventions
    )

    assert (
        dara.false_interventions
        == contract.false_interventions
    )

    assert (
        dara.missed_interventions
        == contract.missed_interventions
    )

    assert (
        dara.correct_non_interventions
        == contract.correct_non_interventions
    )

    assert dara.accuracy == pytest.approx(contract.accuracy)
    assert dara.recall == pytest.approx(contract.recall)
    assert dara.autonomy_availability == pytest.approx(
        contract.autonomy_availability
    )


# ---------------------------------------------------------------------------
# Dependency-family breakdown
# ---------------------------------------------------------------------------


def test_dependency_breakdown_contains_15_rows(by_dependency):
    assert len(by_dependency) == 15


@pytest.mark.parametrize(
    "family",
    [
        DependencyFamily.CAPACITY.value,
        DependencyFamily.STATUS.value,
        DependencyFamily.LOCATION_AVAILABILITY.value,
    ],
)
def test_each_dependency_group_contains_five_policies(
    by_dependency,
    family,
):
    policies = {
        item.metrics.policy
        for item in by_dependency
        if item.value == family
    }

    assert policies == set(POLICIES)


@pytest.mark.parametrize(
    "family",
    [
        DependencyFamily.CAPACITY.value,
        DependencyFamily.STATUS.value,
        DependencyFamily.LOCATION_AVAILABILITY.value,
    ],
)
def test_each_dependency_policy_group_has_eight_conditions(
    by_dependency,
    family,
):
    for policy in POLICIES:
        metric = grouped_metric(
            by_dependency,
            family,
            policy,
        )

        assert metric.conditions == 8


@pytest.mark.parametrize(
    "family",
    [
        DependencyFamily.CAPACITY.value,
        DependencyFamily.STATUS.value,
        DependencyFamily.LOCATION_AVAILABILITY.value,
    ],
)
def test_dara_dependency_family_metrics_are_consistent(
    by_dependency,
    family,
):
    metric = grouped_metric(
        by_dependency,
        family,
        "dara_dt",
    )

    assert metric.true_interventions == 4
    assert metric.false_interventions == 3
    assert metric.missed_interventions == 0
    assert metric.correct_non_interventions == 1

    assert metric.accuracy == pytest.approx(5 / 8)
    assert metric.precision == pytest.approx(4 / 7)
    assert metric.recall == pytest.approx(1.0)
    assert metric.false_intervention_rate == pytest.approx(3 / 4)
    assert metric.missed_intervention_rate == pytest.approx(0.0)
    assert metric.autonomy_availability == pytest.approx(1 / 8)


@pytest.mark.parametrize(
    "family",
    [
        DependencyFamily.CAPACITY.value,
        DependencyFamily.STATUS.value,
        DependencyFamily.LOCATION_AVAILABILITY.value,
    ],
)
def test_dara_and_uncertainty_contract_match_by_dependency_family(
    by_dependency,
    family,
):
    contract = grouped_metric(
        by_dependency,
        family,
        "uncertainty_contract",
    )

    dara = grouped_metric(
        by_dependency,
        family,
        "dara_dt",
    )

    assert (
        dara.true_interventions
        == contract.true_interventions
    )

    assert (
        dara.false_interventions
        == contract.false_interventions
    )

    assert (
        dara.missed_interventions
        == contract.missed_interventions
    )

    assert (
        dara.correct_non_interventions
        == contract.correct_non_interventions
    )

    assert dara.accuracy == pytest.approx(contract.accuracy)
    assert dara.precision == pytest.approx(contract.precision)
    assert dara.recall == pytest.approx(contract.recall)
    assert dara.autonomy_availability == pytest.approx(
        contract.autonomy_availability
    )


# ---------------------------------------------------------------------------
# Lower-level metric helpers
# ---------------------------------------------------------------------------


def test_calculate_policy_metrics_handles_empty_input():
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


def test_calculate_authority_distribution_handles_empty_input():
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


# ---------------------------------------------------------------------------
# Research-integrity / falsification checks
# ---------------------------------------------------------------------------


def test_exp008_kill_test_e_is_visible_in_aggregate_metrics(aggregate):
    """The stronger DARA claim is not supported by binary metrics."""

    contract = metric_for(
        aggregate,
        "uncertainty_contract",
    )

    dara = metric_for(
        aggregate,
        "dara_dt",
    )

    assert dara.accuracy == pytest.approx(contract.accuracy)
    assert dara.precision == pytest.approx(contract.precision)
    assert dara.recall == pytest.approx(contract.recall)
    assert dara.false_intervention_rate == pytest.approx(
        contract.false_intervention_rate
    )
    assert dara.missed_intervention_rate == pytest.approx(
        contract.missed_intervention_rate
    )
    assert dara.autonomy_availability == pytest.approx(
        contract.autonomy_availability
    )


def test_exp008_preserves_authority_semantic_difference(authority):
    """Binary equivalence must not be reported as identical authority."""

    contract = authority_for(
        authority,
        "uncertainty_contract",
    )

    dara = authority_for(
        authority,
        "dara_dt",
    )

    assert contract.restrict == 3
    assert dara.restrict == 0

    assert contract.defer == 18
    assert dara.defer == 21


def test_exp008_cross_dependency_result_is_not_capacity_only(
    by_dependency,
):
    """The observed DARA pattern appears across all three dependencies."""

    for family in (
        DependencyFamily.CAPACITY.value,
        DependencyFamily.STATUS.value,
        DependencyFamily.LOCATION_AVAILABILITY.value,
    ):
        metric = grouped_metric(
            by_dependency,
            family,
            "dara_dt",
        )

        assert metric.true_interventions == 4
        assert metric.missed_interventions == 0
        assert metric.recall == pytest.approx(1.0)
