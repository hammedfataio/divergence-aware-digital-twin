"""Aggregate metrics for EXP-008 imperfect-evidence assurance.

EXP-008 evaluates five runtime-assurance strategies across a controlled
24-condition matrix spanning:

- capacity,
- operational status,
- location / availability,

under:

- reliable,
- stale,
- missing,
- conflicting runtime evidence.

Metrics are calculated against independent physical ground truth.

The module reports:

1. aggregate binary assurance performance,
2. autonomy availability,
3. authority-state distributions,
4. performance by evidence condition,
5. performance by dependency family.

Physical ground truth is used only by the experiment evaluator. This metrics
module consumes completed experimental outcomes and does not expose physical
truth to runtime assurance policies.
"""

from dataclasses import dataclass

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.cross_dependency_conditions import DependencyFamily
from dara_dt.experiments.imperfect_evidence_experiment import (
    ImperfectEvidenceExperimentResult,
    run_imperfect_evidence_experiment,
)


POLICIES = (
    "no_assurance",
    "global_divergence",
    "direct_contract",
    "uncertainty_contract",
    "dara_dt",
)


@dataclass(frozen=True)
class ImperfectEvidencePolicyMetrics:
    """Aggregate binary assurance metrics for one policy."""

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
    """Authority-state distribution for one assurance policy."""

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
    """Metrics for one policy within one experimental subgroup."""

    group: str
    value: str
    metrics: ImperfectEvidencePolicyMetrics


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
) -> ImperfectEvidencePolicyMetrics:
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

    return ImperfectEvidencePolicyMetrics(
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
    results: tuple[ImperfectEvidenceExperimentResult, ...],
    policy: str,
) -> tuple[AssuranceOutcome, ...]:
    """Extract binary assurance outcomes for one policy."""

    return tuple(
        getattr(result, policy).outcome
        for result in results
    )


def _authority_attribute(policy: str) -> str:
    """Return the result attribute containing a policy's authority state."""

    return f"{policy}_authority"


def _extract_authorities(
    results: tuple[ImperfectEvidenceExperimentResult, ...],
    policy: str,
) -> tuple[AuthorityState, ...]:
    """Extract authority states for one policy."""

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


def calculate_exp008_metrics(
    results: tuple[ImperfectEvidenceExperimentResult, ...] | None = None,
) -> tuple[ImperfectEvidencePolicyMetrics, ...]:
    """Calculate aggregate EXP-008 metrics for all five policies."""

    if results is None:
        results = run_imperfect_evidence_experiment()

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


def calculate_exp008_authority_distributions(
    results: tuple[ImperfectEvidenceExperimentResult, ...] | None = None,
) -> tuple[AuthorityDistribution, ...]:
    """Calculate authority-state distributions for all policies."""

    if results is None:
        results = run_imperfect_evidence_experiment()

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
    results: tuple[ImperfectEvidenceExperimentResult, ...],
    group: str,
    values: tuple[object, ...],
    value_getter,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate policy metrics across controlled experimental groups."""

    grouped: list[GroupedPolicyMetrics] = []

    for value in values:
        subset = tuple(
            result
            for result in results
            if value_getter(result) == value
        )

        value_text = getattr(value, "value", str(value))

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
    results: tuple[ImperfectEvidenceExperimentResult, ...] | None = None,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate policy metrics for each runtime evidence status."""

    if results is None:
        results = run_imperfect_evidence_experiment()

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
    results: tuple[ImperfectEvidenceExperimentResult, ...] | None = None,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate policy metrics for each decision-dependency family."""

    if results is None:
        results = run_imperfect_evidence_experiment()

    return _calculate_grouped_metrics(
        results=results,
        group="dependency_family",
        values=(
            DependencyFamily.CAPACITY,
            DependencyFamily.STATUS,
            DependencyFamily.LOCATION_AVAILABILITY,
        ),
        value_getter=lambda result: result.condition.family,
    )


def _format_rate(value: float) -> str:
    """Format a metric rate to three decimal places."""

    return f"{value:.3f}"


def _print_policy_metrics(
    metrics: tuple[ImperfectEvidencePolicyMetrics, ...],
) -> None:
    """Print aggregate binary assurance metrics."""

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
    """Print authority-state distributions."""

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
    """Print grouped binary assurance metrics."""

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


def main() -> None:
    """Run EXP-008 and print publication-oriented metrics."""

    results = run_imperfect_evidence_experiment()

    aggregate = calculate_exp008_metrics(results)

    authority = calculate_exp008_authority_distributions(results)

    by_evidence = calculate_metrics_by_evidence_status(results)

    by_dependency = calculate_metrics_by_dependency_family(results)

    print("\nEXP-008 — Imperfect Evidence Contract Comparison")

    _print_policy_metrics(aggregate)

    _print_authority_distributions(authority)

    _print_grouped_metrics(
        "Metrics by evidence status",
        by_evidence,
    )

    _print_grouped_metrics(
        "Metrics by dependency family",
        by_dependency,
    )


if __name__ == "__main__":
    main()
