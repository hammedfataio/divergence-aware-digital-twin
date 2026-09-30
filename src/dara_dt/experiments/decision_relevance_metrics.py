"""Aggregate metrics and falsification tests for EXP-009.

EXP-009 evaluates whether decision-conditioned runtime assurance can
distinguish decision-relevant from decision-irrelevant evidence uncertainty
while preserving autonomous authority without increasing unsafe missed
interventions.

The frozen experiment compares five primary policies:

P0 - No Assurance
P1 - Global Evidence Uncertainty
P2 - Entity-Filtered Evidence Uncertainty
P3 - Uncertainty-Aware Runtime Contract
P4 - DARA-DT Decision-Conditioned Assurance

The module reports:

1. aggregate binary assurance performance;
2. autonomy availability;
3. authority-state distributions;
4. performance by evidence status;
5. performance by dependency family;
6. performance by evidence relevance; and
7. the six pre-registered EXP-009 kill tests.

The metrics layer does not assume that DARA-DT must outperform a comparator.
Triggered kill tests are valid experimental results and must be reported
without retrospective alteration of the frozen experiment.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.decision_relevance_conditions import (
    DependencyFamily,
    EvidenceRelevance,
)
from dara_dt.experiments.decision_relevance_experiment import (
    DecisionRelevanceExperimentResult,
    run_decision_relevance_experiment,
)


POLICIES = (
    "no_assurance",
    "global_uncertainty",
    "entity_filtered",
    "uncertainty_contract",
    "dara_dt",
)


@dataclass(frozen=True)
class DecisionRelevancePolicyMetrics:
    """Aggregate binary assurance metrics for one EXP-009 policy."""

    policy: str
    conditions: int

    true_interventions: int
    false_interventions: int
    missed_interventions: int
    correct_non_interventions: int

    accuracy: float
    precision: float
    recall: float
    false_intervention_rate: float
    missed_intervention_rate: float
    autonomy_availability: float


@dataclass(frozen=True)
class AuthorityDistribution:
    """Authority-state distribution for one EXP-009 policy."""

    policy: str
    conditions: int

    allow: int
    restrict: int
    defer: int
    fallback: int

    allow_rate: float
    restrict_rate: float
    defer_rate: float
    fallback_rate: float


@dataclass(frozen=True)
class GroupedPolicyMetrics:
    """Policy metrics within one controlled EXP-009 subgroup."""

    group: str
    value: str
    metrics: DecisionRelevancePolicyMetrics


class KillTestStatus(str, Enum):
    """Outcome of a pre-registered falsification test."""

    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"


@dataclass(frozen=True)
class KillTestResult:
    """Result of one EXP-009 pre-registered kill test."""

    kill_test: str
    name: str
    status: KillTestStatus
    evidence: str


def _safe_divide(
    numerator: int,
    denominator: int,
) -> float:
    """Return a ratio while safely handling zero denominators."""

    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_policy_metrics(
    policy: str,
    outcomes: tuple[AssuranceOutcome, ...],
) -> DecisionRelevancePolicyMetrics:
    """Calculate binary assurance metrics for one policy."""

    true_interventions = outcomes.count(
        AssuranceOutcome.TRUE_INTERVENTION
    )

    false_interventions = outcomes.count(
        AssuranceOutcome.FALSE_INTERVENTION
    )

    missed_interventions = outcomes.count(
        AssuranceOutcome.MISSED_INTERVENTION
    )

    correct_non_interventions = outcomes.count(
        AssuranceOutcome.CORRECT_NON_INTERVENTION
    )

    conditions = len(outcomes)

    correct = (
        true_interventions
        + correct_non_interventions
    )

    interventions = (
        true_interventions
        + false_interventions
    )

    required_interventions = (
        true_interventions
        + missed_interventions
    )

    valid_conditions = (
        false_interventions
        + correct_non_interventions
    )

    autonomous_executions = (
        missed_interventions
        + correct_non_interventions
    )

    return DecisionRelevancePolicyMetrics(
        policy=policy,
        conditions=conditions,
        true_interventions=true_interventions,
        false_interventions=false_interventions,
        missed_interventions=missed_interventions,
        correct_non_interventions=correct_non_interventions,
        accuracy=_safe_divide(
            correct,
            conditions,
        ),
        precision=_safe_divide(
            true_interventions,
            interventions,
        ),
        recall=_safe_divide(
            true_interventions,
            required_interventions,
        ),
        false_intervention_rate=_safe_divide(
            false_interventions,
            valid_conditions,
        ),
        missed_intervention_rate=_safe_divide(
            missed_interventions,
            required_interventions,
        ),
        autonomy_availability=_safe_divide(
            autonomous_executions,
            conditions,
        ),
    )


def _extract_outcomes(
    results: tuple[DecisionRelevanceExperimentResult, ...],
    policy: str,
) -> tuple[AssuranceOutcome, ...]:
    """Extract binary assurance outcomes for one primary policy."""

    return tuple(
        getattr(result, policy).outcome
        for result in results
    )


def _authority_attribute(policy: str) -> str:
    """Return the experiment-result authority attribute for a policy."""

    return f"{policy}_authority"


def _extract_authorities(
    results: tuple[DecisionRelevanceExperimentResult, ...],
    policy: str,
) -> tuple[AuthorityState, ...]:
    """Extract authority states for one primary policy."""

    attribute = _authority_attribute(policy)

    return tuple(
        getattr(result, attribute)
        for result in results
    )


def calculate_authority_distribution(
    policy: str,
    authorities: tuple[AuthorityState, ...],
) -> AuthorityDistribution:
    """Calculate authority-state frequencies for one policy."""

    conditions = len(authorities)

    allow = authorities.count(AuthorityState.ALLOW)
    restrict = authorities.count(AuthorityState.RESTRICT)
    defer = authorities.count(AuthorityState.DEFER)
    fallback = authorities.count(AuthorityState.FALLBACK)

    return AuthorityDistribution(
        policy=policy,
        conditions=conditions,
        allow=allow,
        restrict=restrict,
        defer=defer,
        fallback=fallback,
        allow_rate=_safe_divide(
            allow,
            conditions,
        ),
        restrict_rate=_safe_divide(
            restrict,
            conditions,
        ),
        defer_rate=_safe_divide(
            defer,
            conditions,
        ),
        fallback_rate=_safe_divide(
            fallback,
            conditions,
        ),
    )


def calculate_exp009_metrics(
    results: tuple[DecisionRelevanceExperimentResult, ...] | None = None,
) -> tuple[DecisionRelevancePolicyMetrics, ...]:
    """Calculate aggregate metrics for all five frozen EXP-009 policies."""

    if results is None:
        results = run_decision_relevance_experiment()

    return tuple(
        calculate_policy_metrics(
            policy=policy,
            outcomes=_extract_outcomes(
                results,
                policy,
            ),
        )
        for policy in POLICIES
    )


def calculate_exp009_authority_distributions(
    results: tuple[DecisionRelevanceExperimentResult, ...] | None = None,
) -> tuple[AuthorityDistribution, ...]:
    """Calculate authority-state distributions for all primary policies."""

    if results is None:
        results = run_decision_relevance_experiment()

    return tuple(
        calculate_authority_distribution(
            policy=policy,
            authorities=_extract_authorities(
                results,
                policy,
            ),
        )
        for policy in POLICIES
    )


def _calculate_grouped_metrics(
    *,
    results: tuple[DecisionRelevanceExperimentResult, ...],
    group: str,
    values: tuple[object, ...],
    value_getter,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate primary-policy metrics across controlled subgroups."""

    grouped: list[GroupedPolicyMetrics] = []

    for value in values:
        subset = tuple(
            result
            for result in results
            if value_getter(result) == value
        )

        value_text = getattr(
            value,
            "value",
            str(value),
        )

        for policy in POLICIES:
            grouped.append(
                GroupedPolicyMetrics(
                    group=group,
                    value=value_text,
                    metrics=calculate_policy_metrics(
                        policy=policy,
                        outcomes=_extract_outcomes(
                            subset,
                            policy,
                        ),
                    ),
                )
            )

    return tuple(grouped)


def calculate_metrics_by_evidence_status(
    results: tuple[DecisionRelevanceExperimentResult, ...] | None = None,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate metrics for each runtime evidence-quality state."""

    if results is None:
        results = run_decision_relevance_experiment()

    return _calculate_grouped_metrics(
        results=results,
        group="evidence_status",
        values=(
            EvidenceStatus.AVAILABLE,
            EvidenceStatus.STALE,
            EvidenceStatus.MISSING,
            EvidenceStatus.CONFLICTING,
        ),
        value_getter=lambda result: result.evidence_status,
    )


def calculate_metrics_by_dependency_family(
    results: tuple[DecisionRelevanceExperimentResult, ...] | None = None,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate metrics for each controlled dependency family."""

    if results is None:
        results = run_decision_relevance_experiment()

    return _calculate_grouped_metrics(
        results=results,
        group="dependency_family",
        values=(
            DependencyFamily.CAPACITY,
            DependencyFamily.STATUS,
            DependencyFamily.LOCATION_AVAILABILITY,
        ),
        value_getter=lambda result: result.condition.dependency_family,
    )


def calculate_metrics_by_evidence_relevance(
    results: tuple[DecisionRelevanceExperimentResult, ...] | None = None,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate metrics for relevant and irrelevant imperfect evidence.

    Reliable controls are intentionally excluded because evidence relevance
    is not an experimental variable for those six control conditions.
    """

    if results is None:
        results = run_decision_relevance_experiment()

    imperfect_results = tuple(
        result
        for result in results
        if result.condition.is_imperfect_evidence
    )

    return _calculate_grouped_metrics(
        results=imperfect_results,
        group="evidence_relevance",
        values=(
            EvidenceRelevance.RELEVANT,
            EvidenceRelevance.IRRELEVANT,
        ),
        value_getter=lambda result: result.evidence_relevance,
    )


def _metrics_lookup(
    results: tuple[DecisionRelevanceExperimentResult, ...],
) -> dict[str, DecisionRelevancePolicyMetrics]:
    """Return aggregate metrics indexed by policy name."""

    return {
        metric.policy: metric
        for metric in calculate_exp009_metrics(results)
    }


def _same_safety(
    left: DecisionRelevancePolicyMetrics,
    right: DecisionRelevancePolicyMetrics,
) -> bool:
    """Return whether two policies have equal missed-intervention safety."""

    return (
        left.missed_interventions
        == right.missed_interventions
    )


def _same_safety_autonomy_tradeoff(
    left: DecisionRelevancePolicyMetrics,
    right: DecisionRelevancePolicyMetrics,
) -> bool:
    """Return whether two policies have equal safety/autonomy outcomes."""

    return (
        left.missed_interventions
        == right.missed_interventions
        and left.false_interventions
        == right.false_interventions
        and left.autonomy_availability
        == right.autonomy_availability
    )


def _kill_test_a(
    results: tuple[DecisionRelevanceExperimentResult, ...],
) -> KillTestResult:
    """Kill Test A — No Autonomy Advantage."""

    metrics = _metrics_lookup(results)

    dara = metrics["dara_dt"]
    contract = metrics["uncertainty_contract"]

    triggered = (
        _same_safety(dara, contract)
        and dara.autonomy_availability
        <= contract.autonomy_availability
    )

    if triggered:
        evidence = (
            "DARA-DT does not provide greater autonomy availability than "
            "the uncertainty-aware runtime contract while maintaining "
            "equivalent missed-intervention safety. The autonomy-preservation "
            "claim is therefore not supported by this matrix."
        )
    else:
        evidence = (
            "DARA-DT provides a measurable autonomy difference relative to "
            "the uncertainty-aware runtime contract without an equivalent "
            "loss of missed-intervention safety in the frozen matrix."
        )

    return KillTestResult(
        kill_test="A",
        name="No Autonomy Advantage",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=evidence,
    )


def _kill_test_b(
    results: tuple[DecisionRelevanceExperimentResult, ...],
) -> KillTestResult:
    """Kill Test B — Safety Degradation."""

    metrics = _metrics_lookup(results)

    dara = metrics["dara_dt"]
    contract = metrics["uncertainty_contract"]

    autonomy_gain = (
        dara.autonomy_availability
        > contract.autonomy_availability
    )

    safety_degradation = (
        dara.missed_interventions
        > contract.missed_interventions
    )

    triggered = (
        autonomy_gain
        and safety_degradation
    )

    if triggered:
        evidence = (
            "DARA-DT preserves additional autonomous execution relative to "
            "the uncertainty-aware runtime contract but also increases "
            "missed required interventions. The additional autonomy cannot "
            "be interpreted as an assurance improvement."
        )
    else:
        evidence = (
            "The frozen matrix does not show DARA-DT gaining autonomy over "
            "the uncertainty-aware runtime contract by accepting a higher "
            "missed-intervention count."
        )

    return KillTestResult(
        kill_test="B",
        name="Safety Degradation",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=evidence,
    )


def _kill_test_c(
    results: tuple[DecisionRelevanceExperimentResult, ...],
) -> KillTestResult:
    """Kill Test C — Runtime Contract Equivalence."""

    metrics = _metrics_lookup(results)

    dara = metrics["dara_dt"]
    contract = metrics["uncertainty_contract"]

    triggered = _same_safety_autonomy_tradeoff(
        dara,
        contract,
    )

    if triggered:
        evidence = (
            "The uncertainty-aware runtime contract matches DARA-DT on "
            "missed interventions, false interventions, and autonomy "
            "availability across the frozen matrix. The stronger DARA-DT "
            "contribution claim is therefore weakened by runtime-contract "
            "equivalence."
        )
    else:
        evidence = (
            "DARA-DT and the uncertainty-aware runtime contract do not have "
            "the same safety/autonomy trade-off across the frozen matrix."
        )

    return KillTestResult(
        kill_test="C",
        name="Runtime Contract Equivalence",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=evidence,
    )


def _family_policy_metrics(
    results: tuple[DecisionRelevanceExperimentResult, ...],
    family: DependencyFamily,
    policy: str,
) -> DecisionRelevancePolicyMetrics:
    """Return one policy's metrics within one dependency family."""

    subset = tuple(
        result
        for result in results
        if result.condition.dependency_family == family
    )

    return calculate_policy_metrics(
        policy=policy,
        outcomes=_extract_outcomes(
            subset,
            policy,
        ),
    )


def _has_tradeoff_advantage(
    candidate: DecisionRelevancePolicyMetrics,
    comparator: DecisionRelevancePolicyMetrics,
) -> bool:
    """Return whether candidate improves autonomy without worse safety."""

    return (
        candidate.autonomy_availability
        > comparator.autonomy_availability
        and candidate.missed_interventions
        <= comparator.missed_interventions
    )


def _kill_test_d(
    results: tuple[DecisionRelevanceExperimentResult, ...],
) -> KillTestResult:
    """Kill Test D — Capacity-Only Effect."""

    family_advantage: dict[DependencyFamily, bool] = {}

    for family in (
        DependencyFamily.CAPACITY,
        DependencyFamily.STATUS,
        DependencyFamily.LOCATION_AVAILABILITY,
    ):
        dara = _family_policy_metrics(
            results,
            family,
            "dara_dt",
        )

        contract = _family_policy_metrics(
            results,
            family,
            "uncertainty_contract",
        )

        family_advantage[family] = _has_tradeoff_advantage(
            dara,
            contract,
        )

    capacity_only = (
        family_advantage[DependencyFamily.CAPACITY]
        and not family_advantage[DependencyFamily.STATUS]
        and not family_advantage[
            DependencyFamily.LOCATION_AVAILABILITY
        ]
    )

    if capacity_only:
        evidence = (
            "A DARA-DT safety/autonomy advantage over the uncertainty-aware "
            "runtime contract appears for capacity but does not reproduce "
            "for status or location/availability. Framework-level "
            "generalisation must therefore be narrowed."
        )
    else:
        advantage_count = sum(
            family_advantage.values()
        )

        evidence = (
            "The frozen dependency-family analysis does not show an "
            "advantage confined exclusively to capacity. "
            f"DARA-DT shows the defined trade-off advantage in "
            f"{advantage_count} of 3 dependency families."
        )

    return KillTestResult(
        kill_test="D",
        name="Capacity-Only Effect",
        status=(
            KillTestStatus.TRIGGERED
            if capacity_only
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=evidence,
    )


def _kill_test_e(
    results: tuple[DecisionRelevanceExperimentResult, ...],
) -> KillTestResult:
    """Kill Test E — Evidence Privilege.

    All primary policies are evaluated from the same condition-level runtime
    evidence collection. Policies may select the subset relevant to their
    mechanism, but DARA-DT is not supplied hidden physical ground truth or a
    separate privileged evidence source.
    """

    evidence_present = all(
        result.runtime_evidence
        for result in results
    )

    decision_ids_match = all(
        result.ground_truth.decision_id
        == result.decision.decision_id
        for result in results
    )

    triggered = not (
        evidence_present
        and decision_ids_match
    )

    if triggered:
        evidence = (
            "The experiment cannot establish evidence parity for every "
            "condition. The DARA-DT comparison must therefore be treated as "
            "invalid until evidence access is corrected."
        )
    else:
        evidence = (
            "All 42 conditions expose a shared runtime-evidence collection "
            "to the experiment. DARA-DT receives no physical ground truth "
            "and no separate privileged evidence source; physical validity "
            "is used only by the evaluator."
        )

    return KillTestResult(
        kill_test="E",
        name="Evidence Privilege",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=evidence,
    )


def _kill_test_f(
    results: tuple[DecisionRelevanceExperimentResult, ...],
) -> KillTestResult:
    """Kill Test F — Trivial Entity Filtering."""

    metrics = _metrics_lookup(results)

    dara = metrics["dara_dt"]
    entity = metrics["entity_filtered"]

    triggered = _same_safety_autonomy_tradeoff(
        dara,
        entity,
    )

    if triggered:
        evidence = (
            "Entity-filtered uncertainty matches DARA-DT on missed "
            "interventions, false interventions, and autonomy availability. "
            "The observed benefit therefore cannot be attributed to richer "
            "decision-dependency reasoning."
        )
    else:
        evidence = (
            "Entity filtering does not reproduce the complete DARA-DT "
            "safety/autonomy trade-off across the frozen matrix. The "
            "observed behaviour is therefore not explained by entity "
            "filtering alone."
        )

    return KillTestResult(
        kill_test="F",
        name="Trivial Entity Filtering",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=evidence,
    )


def calculate_exp009_kill_tests(
    results: tuple[DecisionRelevanceExperimentResult, ...] | None = None,
) -> tuple[KillTestResult, ...]:
    """Evaluate all six pre-registered EXP-009 falsification tests."""

    if results is None:
        results = run_decision_relevance_experiment()

    return (
        _kill_test_a(results),
        _kill_test_b(results),
        _kill_test_c(results),
        _kill_test_d(results),
        _kill_test_e(results),
        _kill_test_f(results),
    )


def _format_rate(value: float) -> str:
    """Format a metric rate to three decimal places."""

    return f"{value:.3f}"


def _print_policy_metrics(
    metrics: tuple[DecisionRelevancePolicyMetrics, ...],
) -> None:
    """Print aggregate EXP-009 assurance metrics."""

    print("\nAggregate assurance metrics")
    print("=" * 118)

    print(
        f"{'policy':<23}"
        f"{'N':>5}"
        f"{'TI':>6}"
        f"{'FI':>6}"
        f"{'MI':>6}"
        f"{'CNI':>6}"
        f"{'accuracy':>11}"
        f"{'precision':>11}"
        f"{'recall':>10}"
        f"{'FI_rate':>10}"
        f"{'MI_rate':>10}"
        f"{'autonomy':>11}"
    )

    for metric in metrics:
        print(
            f"{metric.policy:<23}"
            f"{metric.conditions:>5}"
            f"{metric.true_interventions:>6}"
            f"{metric.false_interventions:>6}"
            f"{metric.missed_interventions:>6}"
            f"{metric.correct_non_interventions:>6}"
            f"{_format_rate(metric.accuracy):>11}"
            f"{_format_rate(metric.precision):>11}"
            f"{_format_rate(metric.recall):>10}"
            f"{_format_rate(metric.false_intervention_rate):>10}"
            f"{_format_rate(metric.missed_intervention_rate):>10}"
            f"{_format_rate(metric.autonomy_availability):>11}"
        )


def _print_authority_distributions(
    distributions: tuple[AuthorityDistribution, ...],
) -> None:
    """Print EXP-009 authority-state distributions."""

    print("\nAuthority-state distributions")
    print("=" * 82)

    print(
        f"{'policy':<23}"
        f"{'N':>5}"
        f"{'ALLOW':>9}"
        f"{'RESTRICT':>11}"
        f"{'DEFER':>9}"
        f"{'FALLBACK':>11}"
    )

    for distribution in distributions:
        print(
            f"{distribution.policy:<23}"
            f"{distribution.conditions:>5}"
            f"{distribution.allow:>9}"
            f"{distribution.restrict:>11}"
            f"{distribution.defer:>9}"
            f"{distribution.fallback:>11}"
        )


def _print_grouped_metrics(
    title: str,
    grouped: tuple[GroupedPolicyMetrics, ...],
) -> None:
    """Print grouped EXP-009 metrics."""

    print(f"\n{title}")
    print("=" * 118)

    print(
        f"{'group':<24}"
        f"{'policy':<23}"
        f"{'N':>5}"
        f"{'TI':>6}"
        f"{'FI':>6}"
        f"{'MI':>6}"
        f"{'CNI':>6}"
        f"{'accuracy':>11}"
        f"{'recall':>10}"
        f"{'autonomy':>11}"
    )

    for item in grouped:
        metric = item.metrics

        print(
            f"{item.value:<24}"
            f"{metric.policy:<23}"
            f"{metric.conditions:>5}"
            f"{metric.true_interventions:>6}"
            f"{metric.false_interventions:>6}"
            f"{metric.missed_interventions:>6}"
            f"{metric.correct_non_interventions:>6}"
            f"{_format_rate(metric.accuracy):>11}"
            f"{_format_rate(metric.recall):>10}"
            f"{_format_rate(metric.autonomy_availability):>11}"
        )


def _print_kill_tests(
    kill_tests: tuple[KillTestResult, ...],
) -> None:
    """Print pre-registered EXP-009 falsification results."""

    print("\nPre-registered kill tests")
    print("=" * 90)

    for result in kill_tests:
        print(
            f"Kill Test {result.kill_test} — "
            f"{result.name}: {result.status.value}"
        )
        print(f"  {result.evidence}")


def main() -> None:
    """Run EXP-009 and print publication-oriented results."""

    results = run_decision_relevance_experiment()

    aggregate = calculate_exp009_metrics(results)

    authority = calculate_exp009_authority_distributions(
        results
    )

    by_evidence = calculate_metrics_by_evidence_status(
        results
    )

    by_dependency = calculate_metrics_by_dependency_family(
        results
    )

    by_relevance = calculate_metrics_by_evidence_relevance(
        results
    )

    kill_tests = calculate_exp009_kill_tests(
        results
    )

    print(
        "\nEXP-009 — Decision-Relevant Evidence Uncertainty"
    )

    _print_policy_metrics(
        aggregate
    )

    _print_authority_distributions(
        authority
    )

    _print_grouped_metrics(
        "Metrics by evidence status",
        by_evidence,
    )

    _print_grouped_metrics(
        "Metrics by dependency family",
        by_dependency,
    )

    _print_grouped_metrics(
        "Metrics by evidence relevance",
        by_relevance,
    )

    _print_kill_tests(
        kill_tests
    )


if __name__ == "__main__":
    main()
