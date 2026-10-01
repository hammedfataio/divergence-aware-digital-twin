"""Metrics, subgroup analysis, and kill tests for EXP-010.

EXP-010 tests whether explicit physical-digital divergence propagation
provides runtime-assurance information beyond a strong dependency-aware
composed runtime contract.

Five policies are compared:

P0 - No Assurance
P1 - Local Runtime Contract
P2 - Global Divergence / Evidence Uncertainty
P3 - Dependency-Aware Composed Runtime Contract
P4 - Propagation-Aware DARA-DT

The metrics layer reports:

1. binary assurance performance;
2. autonomy availability;
3. authority-state distributions;
4. family-level performance;
5. evidence-quality performance;
6. propagation-specific performance;
7. P3/P4 equivalence;
8. the ten preregistered EXP-010 kill tests.

The implementation does not assume that DARA-DT must outperform P3.
A null/equivalence result is a valid experimental outcome.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.divergence_propagation_conditions import (
    PropagationEvidenceStatus,
    PropagationFamily,
)
from dara_dt.experiments.divergence_propagation_experiment import (
    DivergencePropagationExperimentResult,
    run_exp010,
)


POLICIES = (
    "no_assurance",
    "local_contract",
    "global_assurance",
    "composed_contract",
    "dara_dt",
)


_AUTHORITY_ATTRIBUTES = {
    "no_assurance": "no_assurance_authority",
    "local_contract": "local_contract_authority",
    "global_assurance": "global_authority",
    "composed_contract": "composed_contract_authority",
    "dara_dt": "dara_dt_authority",
}


@dataclass(frozen=True, slots=True)
class PropagationPolicyMetrics:
    """Aggregate binary assurance metrics for one EXP-010 policy."""

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


@dataclass(frozen=True, slots=True)
class AuthorityDistribution:
    """Authority-state distribution for one EXP-010 policy."""

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


@dataclass(frozen=True, slots=True)
class GroupedPolicyMetrics:
    """Policy metrics within one controlled EXP-010 subgroup."""

    group: str
    value: str
    metrics: PropagationPolicyMetrics


@dataclass(frozen=True, slots=True)
class PropagationSummary:
    """Summary of propagation structure in the frozen matrix."""

    conditions: int
    divergent_conditions: int
    propagating_conditions: int
    non_propagating_divergence_conditions: int
    compound_propagation_conditions: int

    propagating_interventions_required: int
    non_propagating_interventions_required: int


@dataclass(frozen=True, slots=True)
class ComparatorEquivalence:
    """Direct P3/P4 comparison across the frozen matrix."""

    conditions: int
    authority_matches: int
    outcome_matches: int
    authority_match_rate: float
    outcome_match_rate: float

    fully_authority_equivalent: bool
    fully_outcome_equivalent: bool


class KillTestStatus(str, Enum):
    """Status of one preregistered EXP-010 kill test."""

    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"
    NOT_EVALUABLE = "not_evaluable"


@dataclass(frozen=True, slots=True)
class KillTestResult:
    """Result of one preregistered EXP-010 kill test."""

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


def _extract_outcomes(
    results: tuple[DivergencePropagationExperimentResult, ...],
    policy: str,
) -> tuple[AssuranceOutcome, ...]:
    """Extract binary assurance outcomes for one policy."""

    return tuple(
        getattr(result, policy).outcome
        for result in results
    )


def _extract_authorities(
    results: tuple[DivergencePropagationExperimentResult, ...],
    policy: str,
) -> tuple[AuthorityState, ...]:
    """Extract authority states for one policy."""

    try:
        attribute = _AUTHORITY_ATTRIBUTES[policy]
    except KeyError as exc:
        raise KeyError(
            f"Unknown EXP-010 policy: {policy}"
        ) from exc

    return tuple(
        getattr(result, attribute)
        for result in results
    )


def calculate_policy_metrics(
    policy: str,
    outcomes: tuple[AssuranceOutcome, ...],
) -> PropagationPolicyMetrics:
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

    return PropagationPolicyMetrics(
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


def calculate_exp010_metrics(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> tuple[PropagationPolicyMetrics, ...]:
    """Calculate aggregate metrics for all five EXP-010 policies."""

    if results is None:
        results = run_exp010()

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


def calculate_exp010_authority_distributions(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> tuple[AuthorityDistribution, ...]:
    """Calculate authority distributions for all EXP-010 policies."""

    if results is None:
        results = run_exp010()

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
    results: tuple[DivergencePropagationExperimentResult, ...],
    group: str,
    values: tuple[object, ...],
    value_getter,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate policy metrics across controlled subgroups."""

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


def calculate_metrics_by_family(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate policy performance for each frozen family."""

    if results is None:
        results = run_exp010()

    return _calculate_grouped_metrics(
        results=results,
        group="propagation_family",
        values=(
            PropagationFamily.SYNCHRONISED_CONTROL,
            PropagationFamily.DIRECT_DIVERGENCE,
            PropagationFamily.UPSTREAM_NON_PROPAGATING,
            PropagationFamily.UPSTREAM_PROPAGATING,
            PropagationFamily.COMPOUND_PROPAGATING,
        ),
        value_getter=lambda result: result.condition.family,
    )


def calculate_metrics_by_evidence_status(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> tuple[GroupedPolicyMetrics, ...]:
    """Calculate performance for each evidence-quality state."""

    if results is None:
        results = run_exp010()

    return _calculate_grouped_metrics(
        results=results,
        group="evidence_status",
        values=(
            PropagationEvidenceStatus.AVAILABLE,
            PropagationEvidenceStatus.STALE,
            PropagationEvidenceStatus.MISSING,
            PropagationEvidenceStatus.CONFLICTING,
        ),
        value_getter=lambda result: result.condition.evidence_status,
    )


def calculate_propagation_summary(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> PropagationSummary:
    """Summarise divergence and propagation structure."""

    if results is None:
        results = run_exp010()

    divergent = tuple(
        result
        for result in results
        if result.propagation.has_divergence
    )

    propagating = tuple(
        result
        for result in results
        if result.propagation.is_propagating
    )

    non_propagating = tuple(
        result
        for result in divergent
        if not result.propagation.is_propagating
    )

    compound = tuple(
        result
        for result in results
        if result.propagation.is_compound
    )

    return PropagationSummary(
        conditions=len(results),
        divergent_conditions=len(divergent),
        propagating_conditions=len(propagating),
        non_propagating_divergence_conditions=len(
            non_propagating
        ),
        compound_propagation_conditions=len(compound),
        propagating_interventions_required=sum(
            result.ground_truth.intervention_required
            for result in propagating
        ),
        non_propagating_interventions_required=sum(
            result.ground_truth.intervention_required
            for result in non_propagating
        ),
    )


def calculate_p3_p4_equivalence(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> ComparatorEquivalence:
    """Calculate direct equal-evidence P3/P4 equivalence."""

    if results is None:
        results = run_exp010()

    authority_matches = sum(
        result.p3_p4_authority_equivalent
        for result in results
    )

    outcome_matches = sum(
        result.p3_p4_outcome_equivalent
        for result in results
    )

    conditions = len(results)

    return ComparatorEquivalence(
        conditions=conditions,
        authority_matches=authority_matches,
        outcome_matches=outcome_matches,
        authority_match_rate=_safe_divide(
            authority_matches,
            conditions,
        ),
        outcome_match_rate=_safe_divide(
            outcome_matches,
            conditions,
        ),
        fully_authority_equivalent=(
            authority_matches == conditions
        ),
        fully_outcome_equivalent=(
            outcome_matches == conditions
        ),
    )


def _metrics_lookup(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> dict[str, PropagationPolicyMetrics]:
    """Return aggregate metrics indexed by policy."""

    return {
        metric.policy: metric
        for metric in calculate_exp010_metrics(results)
    }


def _same_primary_performance(
    left: PropagationPolicyMetrics,
    right: PropagationPolicyMetrics,
) -> bool:
    """Return whether two policies have identical binary performance."""

    return (
        left.true_interventions
        == right.true_interventions
        and left.false_interventions
        == right.false_interventions
        and left.missed_interventions
        == right.missed_interventions
        and left.correct_non_interventions
        == right.correct_non_interventions
        and left.autonomy_availability
        == right.autonomy_availability
    )


def _error_count(
    metrics: PropagationPolicyMetrics,
) -> int:
    """Return total binary assurance errors."""

    return (
        metrics.false_interventions
        + metrics.missed_interventions
    )


def _family_results(
    results: tuple[DivergencePropagationExperimentResult, ...],
    family: PropagationFamily,
) -> tuple[DivergencePropagationExperimentResult, ...]:
    """Return results belonging to one frozen family."""

    return tuple(
        result
        for result in results
        if result.condition.family is family
    )


def _kill_test_a(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test A — Composed Contract Equivalence."""

    equivalence = calculate_p3_p4_equivalence(results)

    triggered = (
        equivalence.fully_outcome_equivalent
        and equivalence.fully_authority_equivalent
    )

    return KillTestResult(
        kill_test="A",
        name="Composed Contract Equivalence",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "P3 reproduces P4 authority and binary assurance outcomes "
            "across the complete frozen matrix; DARA-DT differentiation "
            "is therefore not established."
            if triggered
            else
            "P3 and P4 differ on at least one frozen condition, so full "
            "composed-contract equivalence is not observed."
        ),
    )


def _kill_test_b(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test B — Local Contract Strawman."""

    metrics = _metrics_lookup(results)

    local = metrics["local_contract"]
    composed = metrics["composed_contract"]
    dara = metrics["dara_dt"]

    dara_better_than_local = (
        _error_count(dara)
        < _error_count(local)
    )

    dara_matches_composed = _same_primary_performance(
        dara,
        composed,
    )

    triggered = (
        dara_better_than_local
        and dara_matches_composed
    )

    return KillTestResult(
        kill_test="B",
        name="Local Contract Strawman",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "P4 improves on the local P1 contract but does not "
            "differentiate from the stronger P3 composed contract. "
            "Any apparent advantage over P1 cannot support a strong "
            "DARA-DT-specific claim."
            if triggered
            else
            "The frozen matrix does not satisfy the complete local-contract "
            "strawman trigger."
        ),
    )


def _kill_test_c(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test C — No Divergence-Specific Value."""

    equivalence = calculate_p3_p4_equivalence(results)

    triggered = (
        equivalence.fully_authority_equivalent
        and equivalence.fully_outcome_equivalent
    )

    return KillTestResult(
        kill_test="C",
        name="No Divergence-Specific Value",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "P3 uses the same composed dependencies and observable evidence "
            "without P4's explicit divergence-propagation provenance, yet "
            "produces identical authority and binary outcomes. Explicit "
            "divergence origin therefore adds no demonstrated decision-level "
            "assurance value in this frozen matrix."
            if triggered
            else
            "P4 produces at least one decision-level difference from P3, "
            "so divergence-specific value cannot be rejected by this test."
        ),
    )


def _kill_test_d(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test D — No Propagation Requirement."""

    downstream = (
        _family_results(
            results,
            PropagationFamily.UPSTREAM_PROPAGATING,
        )
        + _family_results(
            results,
            PropagationFamily.COMPOUND_PROPAGATING,
        )
    )

    local_detects_all = all(
        result.local_contract.outcome
        is AssuranceOutcome.TRUE_INTERVENTION
        for result in downstream
    )

    return KillTestResult(
        kill_test="D",
        name="No Propagation Requirement",
        status=(
            KillTestStatus.TRIGGERED
            if local_detects_all
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "All downstream invalidations are detected by the local "
            "pending-decision contract. Explicit propagation reasoning is "
            "therefore unnecessary for these frozen downstream cases."
            if local_detects_all
            else
            "At least one downstream invalidation is not detected by the "
            "local pending-decision contract, so the frozen matrix contains "
            "a genuine cross-dependency assurance requirement."
        ),
    )


def _kill_test_e(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test E — Evidence Privilege."""

    parity = all(
        result.evidence_parity_preserved
        for result in results
    )

    return KillTestResult(
        kill_test="E",
        name="Evidence Privilege",
        status=(
            KillTestStatus.NOT_TRIGGERED
            if parity
            else KillTestStatus.TRIGGERED
        ),
        evidence=(
            "P3 and P4 preserve the preregistered observable-evidence "
            "parity invariant across all conditions."
            if parity
            else
            "At least one condition violates P3/P4 evidence parity; "
            "comparative differentiation claims from affected conditions "
            "are invalid."
        ),
    )


def _kill_test_f(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test F — Hard-Coded Scenario Advantage."""

    requirements_available_to_both = all(
        result.evidence_parity_preserved
        for result in results
    )

    p3_matches_p4 = (
        calculate_p3_p4_equivalence(
            results
        ).fully_outcome_equivalent
    )

    triggered = (
        not requirements_available_to_both
        and not p3_matches_p4
    )

    return KillTestResult(
        kill_test="F",
        name="Hard-Coded Scenario Advantage",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "P4 obtains a comparative difference while equivalent runtime "
            "knowledge is not preserved for P3. The affected comparison is "
            "not suitable for framework-level claims."
            if triggered
            else
            "The runner preserves equal observable evidence for P3 and P4, "
            "and the strong comparator is not denied the composed dependency "
            "knowledge used for decision evaluation. No comparative P4 "
            "advantage is produced by asymmetric evidence access."
        ),
    )


def _kill_test_g(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test G — Safety Degradation."""

    metrics = _metrics_lookup(results)

    p3 = metrics["composed_contract"]
    p4 = metrics["dara_dt"]

    autonomy_gain = (
        p4.autonomy_availability
        > p3.autonomy_availability
    )

    safety_degradation = (
        p4.missed_interventions
        > p3.missed_interventions
    )

    triggered = (
        autonomy_gain
        and safety_degradation
    )

    return KillTestResult(
        kill_test="G",
        name="Safety Degradation",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "P4 gains autonomy relative to P3 only while increasing missed "
            "required interventions. The autonomy gain is therefore not an "
            "assurance improvement."
            if triggered
            else
            "The frozen matrix does not show P4 gaining autonomy over P3 "
            "through increased missed required interventions."
        ),
    )


def _kill_test_h(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test H — Global Conservatism Only."""

    metrics = _metrics_lookup(results)

    global_policy = metrics["global_assurance"]
    p3 = metrics["composed_contract"]
    p4 = metrics["dara_dt"]

    p4_better_than_global = (
        _error_count(p4)
        < _error_count(global_policy)
    )

    p3_matches_p4 = _same_primary_performance(
        p3,
        p4,
    )

    triggered = (
        p4_better_than_global
        and p3_matches_p4
    )

    return KillTestResult(
        kill_test="H",
        name="Global Conservatism Only",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "P4 improves on global divergence/uncertainty handling, but "
            "the strong P3 composed contract matches P4. The result supports "
            "decision-sensitive assurance rather than a DARA-DT-specific "
            "performance contribution."
            if triggered
            else
            "The complete global-conservatism-only trigger is not observed "
            "in the frozen matrix."
        ),
    )


def _kill_test_i(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test I — Propagation Overreach."""

    non_propagating = _family_results(
        results,
        PropagationFamily.UPSTREAM_NON_PROPAGATING,
    )

    false_interventions = sum(
        result.dara_dt.outcome
        is AssuranceOutcome.FALSE_INTERVENTION
        for result in non_propagating
    )

    triggered = false_interventions > 0

    return KillTestResult(
        kill_test="I",
        name="Propagation Overreach",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            f"P4 produces {false_interventions} false intervention(s) in "
            "the upstream non-propagating F2 family. The propagation "
            "mechanism therefore overreaches in at least one physically "
            "unaffected downstream case."
            if triggered
            else
            "P4 produces no false interventions in the F2 upstream "
            "non-propagating family, supporting selective propagation."
        ),
    )


def _kill_test_j(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> KillTestResult:
    """Kill Test J — Compound-Dependency Collapse."""

    compound = _family_results(
        results,
        PropagationFamily.COMPOUND_PROPAGATING,
    )

    same_authority = all(
        result.composed_contract_authority
        is result.dara_dt_authority
        for result in compound
    )

    same_outcome = all(
        result.composed_contract.outcome
        is result.dara_dt.outcome
        for result in compound
    )

    triggered = (
        same_authority
        and same_outcome
    )

    return KillTestResult(
        kill_test="J",
        name="Compound-Dependency Collapse",
        status=(
            KillTestStatus.TRIGGERED
            if triggered
            else KillTestStatus.NOT_TRIGGERED
        ),
        evidence=(
            "P3 and P4 produce identical authority and binary assurance "
            "outcomes across every F4 compound condition. Explicit compound "
            "propagation therefore adds no decision-level distinction beyond "
            "the composed dependency checks in this matrix."
            if triggered
            else
            "At least one F4 compound condition differentiates P4 from P3."
        ),
    )


def calculate_exp010_kill_tests(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> tuple[KillTestResult, ...]:
    """Evaluate all ten preregistered EXP-010 kill tests."""

    if results is None:
        results = run_exp010()

    return (
        _kill_test_a(results),
        _kill_test_b(results),
        _kill_test_c(results),
        _kill_test_d(results),
        _kill_test_e(results),
        _kill_test_f(results),
        _kill_test_g(results),
        _kill_test_h(results),
        _kill_test_i(results),
        _kill_test_j(results),
    )


@dataclass(frozen=True, slots=True)
class Exp010Report:
    """Complete quantitative EXP-010 analysis."""

    policy_metrics: tuple[PropagationPolicyMetrics, ...]
    authority_distributions: tuple[AuthorityDistribution, ...]
    family_metrics: tuple[GroupedPolicyMetrics, ...]
    evidence_status_metrics: tuple[GroupedPolicyMetrics, ...]
    propagation_summary: PropagationSummary
    p3_p4_equivalence: ComparatorEquivalence
    kill_tests: tuple[KillTestResult, ...]


def build_exp010_report(
    results: tuple[DivergencePropagationExperimentResult, ...]
    | None = None,
) -> Exp010Report:
    """Build the complete reproducible EXP-010 metrics report."""

    if results is None:
        results = run_exp010()

    return Exp010Report(
        policy_metrics=calculate_exp010_metrics(
            results
        ),
        authority_distributions=(
            calculate_exp010_authority_distributions(
                results
            )
        ),
        family_metrics=calculate_metrics_by_family(
            results
        ),
        evidence_status_metrics=(
            calculate_metrics_by_evidence_status(
                results
            )
        ),
        propagation_summary=(
            calculate_propagation_summary(
                results
            )
        ),
        p3_p4_equivalence=(
            calculate_p3_p4_equivalence(
                results
            )
        ),
        kill_tests=calculate_exp010_kill_tests(
            results
        ),
    )
