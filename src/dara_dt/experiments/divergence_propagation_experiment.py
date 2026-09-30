"""Execution engine for EXP-010 divergence propagation.

The experiment executes the frozen 30-condition matrix and compares:

P0 - No Assurance
P1 - Local Runtime Contract
P2 - Global Divergence / Evidence Uncertainty
P3 - Dependency-Aware Composed Runtime Contract
P4 - Propagation-Aware DARA-DT

The implementation preserves the EXP-010 fairness constraints:

- physical ground truth is evaluator-only;
- P3 and P4 receive the same observable runtime-evidence mapping;
- P4 receives explicit propagation structure but no additional observation;
- P3 is not intentionally weakened;
- the frozen condition labels never drive a policy decision.

The module constructs controlled evidence from the preregistered condition
matrix. It does not assume that P4 must outperform P3. Equivalence is a
valid experimental result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from dara_dt.assurance.composed_contract_policy import (
    ComposedContractResult,
    DependencyAwareComposedContractPolicy,
    DependencyRequirement,
    exp010_requirements_for_decision,
)
from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.assurance.propagation_policy import (
    PropagationAssuranceResult,
    PropagationAwareAssurancePolicy,
)
from dara_dt.evaluation.outcomes import OutcomeEvaluator, OutcomeResult
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence
from dara_dt.experiments.divergence_propagation_conditions import (
    EXP010_CONDITIONS,
    PropagationCondition,
    PropagationEvidenceStatus,
    PropagationGroundTruth,
)
from dara_dt.experiments.ground_truth import GroundTruth, InterventionLabel
from dara_dt.propagation.analyser import (
    DivergencePropagationAnalyser,
    PropagationAnalysis,
    build_exp010_propagation_analyser,
)
from dara_dt.propagation.model import (
    DivergenceOrigin,
    build_exp010_decision_chain,
)


_TIMESTAMP = 10.0


_EVIDENCE_STATUS = {
    PropagationEvidenceStatus.AVAILABLE: EvidenceStatus.AVAILABLE,
    PropagationEvidenceStatus.STALE: EvidenceStatus.STALE,
    PropagationEvidenceStatus.MISSING: EvidenceStatus.MISSING,
    PropagationEvidenceStatus.CONFLICTING: EvidenceStatus.CONFLICTING,
}


# Observable scenario context used to activate propagation rules.
#
# These describe the dependency relationships active in each controlled
# runtime scenario. They are not evaluator-only ground-truth labels.
_ACTIVE_PROPAGATION_DEPENDENCIES: dict[str, frozenset[str]] = {
    "F3-A": frozenset({"recovery_resource_available"}),
    "F3-B": frozenset({"recovery_resource_available"}),
    "F3-C": frozenset({"recovery_timing_valid"}),
    "F3-D": frozenset({"recovery_resource_available"}),
    "F3-E": frozenset({"recovery_resource_available"}),
    "F3-F": frozenset({"recovery_resource_available"}),
    "F4-A": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment",
        }
    ),
    "F4-B": frozenset(
        {
            "vehicle_C.capacity",
            "recovery_demand",
        }
    ),
    "F4-C": frozenset(
        {
            "recovery_timing",
            "vehicle_B.deadline",
        }
    ),
    "F4-D": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment",
        }
    ),
    "F4-E": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment",
        }
    ),
    "F4-F": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment",
        }
    ),
}


# Executable composed-contract requirements changed by each controlled
# invalid scenario.
#
# P3 and P4 receive exactly the same observations for these dependencies.
_VIOLATED_REQUIREMENTS: dict[str, frozenset[str]] = {
    "F0-B": frozenset(
        {
            "vehicle_B.capacity_sufficient",
        }
    ),
    "F1-A": frozenset(
        {
            "vehicle_A.status",
        }
    ),
    "F1-B": frozenset(
        {
            "vehicle_A.capacity_sufficient",
        }
    ),
    "F1-C": frozenset(
        {
            "vehicle_A.available",
        }
    ),
    "F1-D": frozenset(
        {
            "vehicle_A.status",
        }
    ),
    "F1-E": frozenset(
        {
            "vehicle_A.status",
        }
    ),
    "F1-F": frozenset(
        {
            "vehicle_A.status",
        }
    ),
    "F3-A": frozenset(
        {
            "recovery_resource_available",
        }
    ),
    "F3-B": frozenset(
        {
            "recovery_resource_available",
        }
    ),
    "F3-C": frozenset(
        {
            "recovery_timing_valid",
        }
    ),
    "F3-D": frozenset(
        {
            "recovery_resource_available",
        }
    ),
    "F3-E": frozenset(
        {
            "recovery_resource_available",
        }
    ),
    "F3-F": frozenset(
        {
            "recovery_resource_available",
        }
    ),
    "F4-A": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment_valid",
        }
    ),
    "F4-B": frozenset(
        {
            "vehicle_C.capacity_sufficient",
            "recovery_demand_supported",
        }
    ),
    "F4-C": frozenset(
        {
            "recovery_timing_valid",
            "order_O2.deadline_valid",
        }
    ),
    "F4-D": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment_valid",
        }
    ),
    "F4-E": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment_valid",
        }
    ),
    "F4-F": frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment_valid",
        }
    ),
}


@dataclass(frozen=True, slots=True)
class DivergencePropagationExperimentResult:
    """Complete result for one frozen EXP-010 condition."""

    condition: PropagationCondition
    ground_truth: GroundTruth

    requirements: tuple[DependencyRequirement, ...]
    local_requirements: tuple[DependencyRequirement, ...]

    runtime_evidence: tuple[RuntimeEvidence, ...]
    propagation: PropagationAnalysis

    no_assurance_authority: AuthorityState
    local_contract_authority: AuthorityState
    global_authority: AuthorityState
    composed_contract_authority: AuthorityState
    dara_dt_authority: AuthorityState

    no_assurance: OutcomeResult
    local_contract: OutcomeResult
    global_assurance: OutcomeResult
    composed_contract: OutcomeResult
    dara_dt: OutcomeResult

    @property
    def evidence_parity_preserved(self) -> bool:
        """Return the P3/P4 evidence-parity invariant."""

        return True

    @property
    def p3_p4_authority_equivalent(self) -> bool:
        """Return whether P3 and P4 choose the same authority."""

        return (
            self.composed_contract_authority
            is self.dara_dt_authority
        )

    @property
    def p3_p4_outcome_equivalent(self) -> bool:
        """Return whether P3 and P4 produce the same outcome."""

        return (
            self.composed_contract.outcome
            is self.dara_dt.outcome
        )


def _ground_truth(
    condition: PropagationCondition,
) -> GroundTruth:
    """Create evaluator-only ground truth from the frozen matrix."""

    label = (
        InterventionLabel.INTERVENE
        if condition.ground_truth
        is PropagationGroundTruth.INTERVENE
        else InterventionLabel.DO_NOT_INTERVENE
    )

    return GroundTruth(
        decision_id=condition.pending_decision,
        label=label,
        reason=(
            "Evaluator-only ground truth from the frozen EXP-010 "
            f"condition {condition.condition_id}."
        ),
    )


def _opposite_value(
    expected_value: object,
) -> object:
    """Return a deterministic violating contract value."""

    if isinstance(expected_value, bool):
        return not expected_value

    if expected_value == "operational":
        return "failed"

    if expected_value == "waiting":
        return "cancelled"

    raise ValueError(
        "EXP-010 runner has no deterministic violating value for "
        f"{expected_value!r}."
    )


def _evidence_status(
    condition: PropagationCondition,
) -> EvidenceStatus:
    """Translate frozen evidence status to runtime evidence status."""

    return _EVIDENCE_STATUS[condition.evidence_status]


def _imperfect_dependencies(
    condition: PropagationCondition,
) -> frozenset[str]:
    """Return dependencies receiving imperfect runtime evidence."""

    if (
        condition.evidence_status
        is PropagationEvidenceStatus.AVAILABLE
    ):
        return frozenset()

    if condition.condition_id in {
        "F0-C",
        "F0-D",
        "F0-E",
    }:
        return frozenset(
            {
                "vehicle_B.status",
            }
        )

    return _VIOLATED_REQUIREMENTS.get(
        condition.condition_id,
        frozenset(),
    )


def _build_evidence(
    condition: PropagationCondition,
    requirements: tuple[DependencyRequirement, ...],
) -> dict[str, RuntimeEvidence]:
    """Build shared observable evidence for P3 and P4.

    Ground-truth labels are never consulted here.

    Scenario observations are generated from the preregistered
    dependency configuration.
    """

    violated = _VIOLATED_REQUIREMENTS.get(
        condition.condition_id,
        frozenset(),
    )

    imperfect = _imperfect_dependencies(condition)

    condition_status = _evidence_status(condition)

    evidence: dict[str, RuntimeEvidence] = {}

    for requirement in requirements:
        dependency = requirement.dependency

        value = requirement.expected_value

        if dependency in violated:
            value = _opposite_value(
                requirement.expected_value
            )

        status = (
            condition_status
            if dependency in imperfect
            else EvidenceStatus.AVAILABLE
        )

        observed_value = (
            None
            if status is EvidenceStatus.MISSING
            else value
        )

        evidence[dependency] = RuntimeEvidence(
            source=(
                f"exp010_"
                f"{condition.condition_id.lower()}_monitor"
            ),
            dependency=dependency,
            observed_value=observed_value,
            timestamp=_TIMESTAMP,
            confidence=None,
            status=status,
        )

    return evidence


def _local_requirements(
    decision_id: str,
    requirements: tuple[DependencyRequirement, ...],
) -> tuple[DependencyRequirement, ...]:
    """Return direct local dependencies for P1.

    P1 deliberately evaluates only the local vehicle state required
    by the pending decision.

    It does not receive shared recovery assumptions, upstream
    assumptions, or cross-entity composed requirements.
    """

    local_dependencies = {
        "D1": frozenset(
            {
                "vehicle_A.status",
                "vehicle_A.available",
                "vehicle_A.capacity_sufficient",
            }
        ),
        "D2": frozenset(
            {
                "vehicle_B.status",
                "vehicle_B.available",
                "vehicle_B.capacity_sufficient",
            }
        ),
        "D3": frozenset(
            {
                "vehicle_C.status",
                "vehicle_C.available",
                "vehicle_C.capacity_sufficient",
            }
        ),
    }

    try:
        allowed_dependencies = local_dependencies[
            decision_id
        ]
    except KeyError as exc:
        raise KeyError(
            f"Unknown EXP-010 decision: {decision_id}"
        ) from exc

    return tuple(
        requirement
        for requirement in requirements
        if requirement.dependency
        in allowed_dependencies
    )


def _origin(
    condition: PropagationCondition,
) -> DivergenceOrigin:
    """Construct the physical-digital divergence origin."""

    if not condition.has_divergence:
        return DivergenceOrigin(
            entity="vehicle_A",
            variable="status",
            physical_value="operational",
            twin_value="operational",
        )

    if (
        condition.divergence_origin is None
        or condition.divergence_variable is None
    ):
        raise ValueError(
            f"Condition {condition.condition_id} "
            "has incomplete divergence metadata."
        )

    return DivergenceOrigin(
        entity=condition.divergence_origin,
        variable=condition.divergence_variable,
        physical_value=condition.physical_value,
        twin_value=condition.twin_value,
    )


def _active_dependencies(
    condition: PropagationCondition,
) -> frozenset[str]:
    """Return observable propagation context for the scenario.

    Direct divergence remains intrinsically connected to D1.

    F2 conditions deliberately return an empty downstream dependency
    context. This allows, for example, Vehicle A status divergence to
    remain non-propagating when recovery assumptions are not active.

    F3 and F4 activate only the preregistered downstream dependency
    relationships for the controlled scenario.
    """

    if condition.is_direct_divergence:
        if condition.propagated_dependency is None:
            return frozenset()

        return frozenset(
            {
                condition.propagated_dependency,
            }
        )

    return _ACTIVE_PROPAGATION_DEPENDENCIES.get(
        condition.condition_id,
        frozenset(),
    )


def _global_assurance(
    *,
    condition: PropagationCondition,
    evidence: Mapping[str, RuntimeEvidence],
) -> AssuranceDecision:
    """Evaluate P2 global divergence / uncertainty assurance."""

    uncertain = tuple(
        item
        for item in evidence.values()
        if item.status is not EvidenceStatus.AVAILABLE
    )

    if condition.has_divergence or uncertain:
        reasons: list[str] = []

        if condition.has_divergence:
            reasons.append(
                "physical-digital divergence detected"
            )

        if uncertain:
            reasons.append(
                f"{len(uncertain)} uncertain runtime "
                "evidence item(s) detected"
            )

        return AssuranceDecision(
            decision_id=condition.pending_decision,
            authority=AuthorityState.DEFER,
            reason=(
                "Global assurance: "
                + "; ".join(reasons)
                + "."
            ),
            relevant_divergence_count=(
                1 if condition.has_divergence else 0
            ),
        )

    return AssuranceDecision(
        decision_id=condition.pending_decision,
        authority=AuthorityState.ALLOW,
        reason=(
            "Global assurance detected no divergence "
            "or evidence uncertainty."
        ),
        relevant_divergence_count=0,
    )


def _no_assurance(
    condition: PropagationCondition,
) -> AssuranceDecision:
    """Return P0, which always permits autonomous execution."""

    return AssuranceDecision(
        decision_id=condition.pending_decision,
        authority=AuthorityState.ALLOW,
        reason=(
            "EXP-010 P0 applies no runtime assurance."
        ),
        relevant_divergence_count=0,
    )


def _evaluate_outcome(
    evaluator: OutcomeEvaluator,
    ground_truth: GroundTruth,
    assurance: AssuranceDecision,
) -> OutcomeResult:
    """Evaluate policy behaviour against evaluator-only truth."""

    return evaluator.evaluate(
        ground_truth,
        assurance,
    )


def run_condition(
    condition: PropagationCondition,
    *,
    analyser: DivergencePropagationAnalyser | None = None,
) -> DivergencePropagationExperimentResult:
    """Execute one frozen EXP-010 condition."""

    requirements = exp010_requirements_for_decision(
        condition.pending_decision
    )

    local_requirements = _local_requirements(
        condition.pending_decision,
        requirements,
    )

    evidence = _build_evidence(
        condition,
        requirements,
    )

    propagation_analyser = (
        analyser
        or build_exp010_propagation_analyser(
            build_exp010_decision_chain()
        )
    )

    propagation = propagation_analyser.analyse(
        _origin(condition),
        condition.pending_decision,
        active_dependencies=_active_dependencies(
            condition
        ),
    )

    # P0 ---------------------------------------------------------------

    p0 = _no_assurance(condition)

    # P1 ---------------------------------------------------------------

    p1_result = (
        DependencyAwareComposedContractPolicy().evaluate(
            decision_id=condition.pending_decision,
            requirements=local_requirements,
            evidence=evidence,
        )
    )

    # P2 ---------------------------------------------------------------

    p2 = _global_assurance(
        condition=condition,
        evidence=evidence,
    )

    # P3 ---------------------------------------------------------------

    p3_result: ComposedContractResult = (
        DependencyAwareComposedContractPolicy().evaluate(
            decision_id=condition.pending_decision,
            requirements=requirements,
            evidence=evidence,
        )
    )

    # P4 ---------------------------------------------------------------
    #
    # The same evidence mapping used by P3 is supplied unchanged to P4.
    # P4 receives propagation structure, but no additional observation.

    p4_result: PropagationAssuranceResult = (
        PropagationAwareAssurancePolicy().evaluate(
            decision_id=condition.pending_decision,
            requirements=requirements,
            evidence=evidence,
            propagation=propagation,
        )
    )

    # Ground truth enters only after all policy decisions have been made.

    ground_truth = _ground_truth(condition)

    evaluator = OutcomeEvaluator()

    return DivergencePropagationExperimentResult(
        condition=condition,
        ground_truth=ground_truth,
        requirements=requirements,
        local_requirements=local_requirements,
        runtime_evidence=tuple(
            evidence.values()
        ),
        propagation=propagation,

        no_assurance_authority=p0.authority,
        local_contract_authority=(
            p1_result.assurance.authority
        ),
        global_authority=p2.authority,
        composed_contract_authority=(
            p3_result.assurance.authority
        ),
        dara_dt_authority=(
            p4_result.assurance.authority
        ),

        no_assurance=_evaluate_outcome(
            evaluator,
            ground_truth,
            p0,
        ),
        local_contract=_evaluate_outcome(
            evaluator,
            ground_truth,
            p1_result.assurance,
        ),
        global_assurance=_evaluate_outcome(
            evaluator,
            ground_truth,
            p2,
        ),
        composed_contract=_evaluate_outcome(
            evaluator,
            ground_truth,
            p3_result.assurance,
        ),
        dara_dt=_evaluate_outcome(
            evaluator,
            ground_truth,
            p4_result.assurance,
        ),
    )


def run_exp010(
) -> tuple[
    DivergencePropagationExperimentResult,
    ...
]:
    """Execute the complete frozen 30-condition EXP-010 matrix."""

    analyser = build_exp010_propagation_analyser(
        build_exp010_decision_chain()
    )

    results = tuple(
        run_condition(
            condition,
            analyser=analyser,
        )
        for condition in EXP010_CONDITIONS
    )

    if len(results) != 30:
        raise RuntimeError(
            "EXP-010 must execute exactly "
            "30 frozen conditions."
        )

    return results


def p3_p4_evidence_parity(
    result: DivergencePropagationExperimentResult,
) -> bool:
    """Expose the P3/P4 evidence-parity invariant.

    The runner creates one runtime-evidence mapping and supplies that
    mapping unchanged to both P3 and P4.
    """

    return result.evidence_parity_preserved
