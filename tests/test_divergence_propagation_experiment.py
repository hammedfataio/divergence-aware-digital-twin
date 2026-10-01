"""Tests for the EXP-010 divergence-propagation experiment runner.

These tests protect the scientific design of EXP-010 rather than
requiring a preferred experimental result.

The suite verifies that:

- the frozen 30-condition matrix executes completely;
- condition ordering and identifiers are preserved;
- physical ground truth remains evaluator-only;
- P0 always allows autonomous execution;
- P3 and P4 use the same observable runtime evidence;
- P3 is not deliberately weakened relative to P4;
- propagation depends on runtime decision context;
- non-propagating upstream divergence remains distinguishable from
  propagating divergence;
- P3/P4 equivalence is accepted as a legitimate result.

The tests deliberately do not assert that DARA-DT must outperform the
strong dependency-aware composed runtime contract.
"""

from __future__ import annotations

from collections import Counter

import pytest

from dara_dt.assurance.model import AuthorityState
from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.divergence_propagation_conditions import (
    EXP010_CONDITIONS,
    PropagationEvidenceStatus,
    PropagationGroundTruth,
    condition_by_id,
)
from dara_dt.experiments.divergence_propagation_experiment import (
    DivergencePropagationExperimentResult,
    p3_p4_evidence_parity,
    run_condition,
    run_exp010,
)
from dara_dt.experiments.ground_truth import InterventionLabel


@pytest.fixture(scope="module")
def results() -> tuple[DivergencePropagationExperimentResult, ...]:
    """Execute EXP-010 once for module-level assertions."""

    return run_exp010()


def _result_by_id(
    results: tuple[DivergencePropagationExperimentResult, ...],
    condition_id: str,
) -> DivergencePropagationExperimentResult:
    """Return one executed result by frozen condition identifier."""

    return next(
        result
        for result in results
        if result.condition.condition_id == condition_id
    )


def test_exp010_executes_exactly_30_conditions(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """The complete frozen matrix must execute."""

    assert len(results) == 30


def test_exp010_executes_every_frozen_condition_once(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """No frozen condition may be omitted or duplicated."""

    executed_ids = [
        result.condition.condition_id
        for result in results
    ]

    frozen_ids = [
        condition.condition_id
        for condition in EXP010_CONDITIONS
    ]

    assert executed_ids == frozen_ids
    assert len(set(executed_ids)) == 30


def test_result_preserves_original_condition_object(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Each result must retain its frozen experimental condition."""

    for result, condition in zip(
        results,
        EXP010_CONDITIONS,
        strict=True,
    ):
        assert result.condition is condition


def test_ground_truth_distribution_remains_frozen(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """EXP-010 must preserve the preregistered 19/11 split."""

    counts = Counter(
        result.ground_truth.label
        for result in results
    )

    assert counts[InterventionLabel.INTERVENE] == 19
    assert counts[InterventionLabel.DO_NOT_INTERVENE] == 11


def test_ground_truth_matches_each_frozen_condition(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Runner ground truth must reproduce the frozen matrix."""

    for result in results:
        expected = (
            InterventionLabel.INTERVENE
            if result.condition.ground_truth
            is PropagationGroundTruth.INTERVENE
            else InterventionLabel.DO_NOT_INTERVENE
        )

        assert result.ground_truth.label is expected


def test_ground_truth_decision_id_matches_pending_decision(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Outcome evaluation must compare the same pending decision."""

    for result in results:
        assert (
            result.ground_truth.decision_id
            == result.condition.pending_decision
        )


def test_p0_always_allows_autonomous_execution(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """No Assurance is the unconditional autonomy baseline."""

    assert all(
        result.no_assurance_authority is AuthorityState.ALLOW
        for result in results
    )


def test_p0_misses_every_required_intervention(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """P0 must expose unsafe non-intervention where truth requires action."""

    missed = sum(
        result.no_assurance.outcome
        is AssuranceOutcome.MISSED_INTERVENTION
        for result in results
    )

    correct_non_intervention = sum(
        result.no_assurance.outcome
        is AssuranceOutcome.CORRECT_NON_INTERVENTION
        for result in results
    )

    assert missed == 19
    assert correct_non_intervention == 11


def test_runtime_evidence_covers_composed_requirements(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Every P3/P4 requirement must have a runtime evidence entry."""

    for result in results:
        required_dependencies = {
            requirement.dependency
            for requirement in result.requirements
        }

        evidence_dependencies = {
            evidence.dependency
            for evidence in result.runtime_evidence
        }

        assert evidence_dependencies == required_dependencies


def test_runtime_evidence_dependencies_are_unique(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """The shared P3/P4 evidence mapping must be unambiguous."""

    for result in results:
        dependencies = [
            evidence.dependency
            for evidence in result.runtime_evidence
        ]

        assert len(dependencies) == len(set(dependencies))


def test_p1_requirements_are_subset_of_p3_requirements(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Local contract P1 must remain weaker than composed P3."""

    for result in results:
        local = {
            requirement.dependency
            for requirement in result.local_requirements
        }

        composed = {
            requirement.dependency
            for requirement in result.requirements
        }

        assert local
        assert local <= composed


def test_p3_p4_evidence_parity_is_preserved(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Every executed condition must preserve the parity invariant."""

    assert all(
        p3_p4_evidence_parity(result)
        for result in results
    )


def test_p3_p4_authority_equivalence_is_measured_not_assumed(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Equivalence must be exposed as an observed result property."""

    for result in results:
        assert result.p3_p4_authority_equivalent == (
            result.composed_contract_authority
            is result.dara_dt_authority
        )


def test_p3_p4_outcome_equivalence_is_measured_not_assumed(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Binary outcome equivalence must be calculated transparently."""

    for result in results:
        assert result.p3_p4_outcome_equivalent == (
            result.composed_contract.outcome
            is result.dara_dt.outcome
        )


def test_p3_and_p4_are_equivalent_on_current_frozen_matrix(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Record the current equal-evidence EXP-010 result.

    Under the present frozen matrix and strong composed comparator,
    explicit propagation provenance does not change authority or binary
    assurance outcome.

    This is a scientifically valid result and must not be altered merely
    to manufacture DARA-DT superiority.
    """

    assert all(
        result.p3_p4_authority_equivalent
        for result in results
    )

    assert all(
        result.p3_p4_outcome_equivalent
        for result in results
    )


def test_f0_contains_no_physical_digital_propagation(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Synchronised controls must not manufacture propagation."""

    f0_results = [
        result
        for result in results
        if result.condition.condition_id.startswith("F0-")
    ]

    assert len(f0_results) == 6

    assert all(
        not result.propagation.has_divergence
        for result in f0_results
    )

    assert all(
        not result.propagation.is_propagating
        for result in f0_results
    )


def test_f2_upstream_divergence_remains_non_propagating(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """F2 is the critical negative control for propagation."""

    f2_results = [
        result
        for result in results
        if result.condition.condition_id.startswith("F2-")
    ]

    assert len(f2_results) == 6

    assert all(
        result.propagation.has_divergence
        for result in f2_results
    )

    assert all(
        not result.propagation.is_propagating
        for result in f2_results
    )


@pytest.mark.parametrize(
    "condition_id",
    [
        "F3-A",
        "F3-B",
        "F3-C",
        "F3-D",
        "F3-E",
        "F3-F",
    ],
)
def test_f3_activates_preregistered_propagation(
    results: tuple[DivergencePropagationExperimentResult, ...],
    condition_id: str,
) -> None:
    """F3 conditions must activate a downstream propagation path."""

    result = _result_by_id(
        results,
        condition_id,
    )

    assert result.propagation.has_divergence
    assert result.propagation.is_propagating
    assert result.propagation.has_matching_rule
    assert result.propagation.affected_dependencies


@pytest.mark.parametrize(
    "condition_id",
    [
        "F4-A",
        "F4-B",
        "F4-C",
        "F4-D",
        "F4-E",
        "F4-F",
    ],
)
def test_f4_activates_compound_propagation(
    results: tuple[DivergencePropagationExperimentResult, ...],
    condition_id: str,
) -> None:
    """F4 must exercise compound cross-dependency propagation."""

    result = _result_by_id(
        results,
        condition_id,
    )

    assert result.propagation.has_divergence
    assert result.propagation.is_propagating
    assert result.propagation.is_compound
    assert result.propagation.has_matching_rule


def test_same_status_divergence_changes_with_runtime_context(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """The same origin may propagate only when recovery context is active."""

    non_propagating = _result_by_id(
        results,
        "F2-C",
    )

    propagating = _result_by_id(
        results,
        "F3-A",
    )

    assert (
        non_propagating.condition.divergence_origin
        == propagating.condition.divergence_origin
    )

    assert (
        non_propagating.condition.divergence_variable
        == propagating.condition.divergence_variable
    )

    assert non_propagating.propagation.has_divergence
    assert propagating.propagation.has_divergence

    assert not non_propagating.propagation.is_propagating
    assert propagating.propagation.is_propagating


@pytest.mark.parametrize(
    (
        "condition_id",
        "expected_status",
    ),
    [
        ("F0-C", EvidenceStatus.STALE),
        ("F0-D", EvidenceStatus.MISSING),
        ("F0-E", EvidenceStatus.CONFLICTING),
    ],
)
def test_synchronised_controls_can_have_imperfect_evidence_without_divergence(
    results: tuple[DivergencePropagationExperimentResult, ...],
    condition_id: str,
    expected_status: EvidenceStatus,
) -> None:
    """Evidence quality and physical-digital divergence remain separate."""

    result = _result_by_id(
        results,
        condition_id,
    )

    assert not result.propagation.has_divergence

    assert any(
        evidence.status is expected_status
        for evidence in result.runtime_evidence
    )


@pytest.mark.parametrize(
    (
        "condition_id",
        "expected_status",
    ),
    [
        ("F3-D", EvidenceStatus.STALE),
        ("F3-E", EvidenceStatus.MISSING),
        ("F3-F", EvidenceStatus.CONFLICTING),
    ],
)
def test_propagating_conditions_preserve_imperfect_evidence_status(
    results: tuple[DivergencePropagationExperimentResult, ...],
    condition_id: str,
    expected_status: EvidenceStatus,
) -> None:
    """Propagation and evidence uncertainty must coexist when preregistered."""

    result = _result_by_id(
        results,
        condition_id,
    )

    assert result.propagation.is_propagating

    assert any(
        evidence.status is expected_status
        for evidence in result.runtime_evidence
    )


def test_available_evidence_conditions_do_not_manufacture_uncertainty(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """AVAILABLE matrix rows must remain runtime-evidence available."""

    for result in results:
        if (
            result.condition.evidence_status
            is PropagationEvidenceStatus.AVAILABLE
        ):
            assert all(
                evidence.status is EvidenceStatus.AVAILABLE
                for evidence in result.runtime_evidence
            )


def test_global_policy_intervenes_on_irrelevant_f2_divergence(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """P2 must expose the cost of treating all divergence globally."""

    for result in results:
        if result.condition.condition_id.startswith("F2-"):
            assert result.global_authority is not AuthorityState.ALLOW


def test_f2_ground_truth_requires_no_intervention(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """F2 remains the frozen non-propagating valid control family."""

    for result in results:
        if result.condition.condition_id.startswith("F2-"):
            assert (
                result.condition.ground_truth
                is PropagationGroundTruth.DO_NOT_INTERVENE
            )


def test_f3_ground_truth_requires_intervention(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """All preregistered F3 propagation cases are invalid."""

    for result in results:
        if result.condition.condition_id.startswith("F3-"):
            assert (
                result.condition.ground_truth
                is PropagationGroundTruth.INTERVENE
            )


def test_f4_ground_truth_requires_intervention(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """All preregistered F4 compound propagation cases are invalid."""

    for result in results:
        if result.condition.condition_id.startswith("F4-"):
            assert (
                result.condition.ground_truth
                is PropagationGroundTruth.INTERVENE
            )


def test_single_condition_execution_is_deterministic() -> None:
    """Controlled EXP-010 execution must be reproducible."""

    condition = condition_by_id("F3-A")

    first = run_condition(condition)
    second = run_condition(condition)

    assert first.condition == second.condition
    assert first.ground_truth == second.ground_truth
    assert first.runtime_evidence == second.runtime_evidence

    assert (
        first.no_assurance_authority
        is second.no_assurance_authority
    )

    assert (
        first.local_contract_authority
        is second.local_contract_authority
    )

    assert (
        first.global_authority
        is second.global_authority
    )

    assert (
        first.composed_contract_authority
        is second.composed_contract_authority
    )

    assert (
        first.dara_dt_authority
        is second.dara_dt_authority
    )

    assert (
        first.composed_contract.outcome
        is second.composed_contract.outcome
    )

    assert (
        first.dara_dt.outcome
        is second.dara_dt.outcome
    )


def test_complete_experiment_is_deterministic(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """Repeated matrix execution must preserve experimental results."""

    repeated = run_exp010()

    assert len(repeated) == len(results)

    for first, second in zip(
        results,
        repeated,
        strict=True,
    ):
        assert (
            first.condition.condition_id
            == second.condition.condition_id
        )

        assert first.runtime_evidence == second.runtime_evidence

        assert (
            first.no_assurance_authority
            is second.no_assurance_authority
        )

        assert (
            first.local_contract_authority
            is second.local_contract_authority
        )

        assert (
            first.global_authority
            is second.global_authority
        )

        assert (
            first.composed_contract_authority
            is second.composed_contract_authority
        )

        assert (
            first.dara_dt_authority
            is second.dara_dt_authority
        )

        assert (
            first.composed_contract.outcome
            is second.composed_contract.outcome
        )

        assert (
            first.dara_dt.outcome
            is second.dara_dt.outcome
        )


def test_exp010_does_not_require_dara_superiority(
    results: tuple[DivergencePropagationExperimentResult, ...],
) -> None:
    """The experiment must remain capable of supporting the null result.

    The current frozen matrix yields P3/P4 equivalence. This assertion
    protects that result from being retrospectively changed merely to
    create an apparent DARA-DT advantage.
    """

    p3_authority = [
        result.composed_contract_authority
        for result in results
    ]

    p4_authority = [
        result.dara_dt_authority
        for result in results
    ]

    p3_outcomes = [
        result.composed_contract.outcome
        for result in results
    ]

    p4_outcomes = [
        result.dara_dt.outcome
        for result in results
    ]

    assert p3_authority == p4_authority
    assert p3_outcomes == p4_outcomes
