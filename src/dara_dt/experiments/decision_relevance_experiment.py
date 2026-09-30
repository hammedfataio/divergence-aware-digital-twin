"""EXP-009 decision-relevant evidence-uncertainty experiment.

This experiment evaluates whether conditioning runtime assurance on the
dependencies of an individual AI-generated logistics decision can distinguish
decision-relevant from decision-irrelevant evidence uncertainty.

The frozen design contains 42 conditions spanning:

- capacity;
- operational status;
- location and availability;
- reliable, stale, missing, and conflicting evidence;
- relevant and irrelevant imperfect evidence; and
- physically valid and physically invalid decisions.

Physical ground truth is evaluator-only information. Runtime assurance
policies receive runtime evidence and decision information, but never hidden
physical truth.

The experiment compares:

P0 - No Assurance
P1 - Global Evidence Uncertainty
P2 - Entity-Filtered Evidence Uncertainty
P3 - Uncertainty-Aware Runtime Contract
P4 - DARA-DT Decision-Conditioned Assurance

A dependency-conditioned uncertainty result is also retained explicitly as
an ablation so that dependency filtering can be separated from richer
decision-conditioned assurance.

The implementation does not assume that DARA-DT must outperform any
comparator. Equivalence or worse performance is a valid experimental result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dara_dt.assurance.baselines import NoAssurancePolicy
from dara_dt.assurance.dependency_conditioned_evidence_policy import (
    DependencyConditionedEvidencePolicy,
)
from dara_dt.assurance.divergence_evidence_policy import (
    DivergenceEvidencePolicy,
)
from dara_dt.assurance.entity_filtered_evidence_policy import (
    EntityFilteredEvidencePolicy,
)
from dara_dt.assurance.evidence_contract_policy import (
    EvidenceAwareRuntimeContractPolicy,
)
from dara_dt.assurance.global_evidence_policy import (
    GlobalEvidenceUncertaintyPolicy,
)
from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.evaluation.outcomes import OutcomeEvaluator, OutcomeResult
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence
from dara_dt.experiments.decision_relevance_conditions import (
    DecisionRelevanceCondition,
    DependencyFamily,
    EvidenceRelevance,
    EXP009_CONDITIONS,
)
from dara_dt.experiments.ground_truth import GroundTruth, InterventionLabel


_SELECTED_ENTITY = "vehicle_01"
_OTHER_ENTITY = "vehicle_08"

_ORDER_DEMAND = 5.0
_REQUIRED_STATUS = "operational"
_REQUIRED_AVAILABLE = True
_PERMITTED_LOCATIONS = {"depot"}

_UNCERTAIN_STATUSES = {
    EvidenceStatus.STALE,
    EvidenceStatus.MISSING,
    EvidenceStatus.CONFLICTING,
}


@dataclass(frozen=True)
class DecisionRelevanceExperimentResult:
    """Result for one frozen EXP-009 condition."""

    condition: DecisionRelevanceCondition
    decision: Decision
    ground_truth: GroundTruth

    evidence_status: EvidenceStatus
    evidence_relevance: EvidenceRelevance
    required_dependencies: tuple[str, ...]
    runtime_evidence: tuple[RuntimeEvidence, ...]

    no_assurance_authority: AuthorityState
    global_uncertainty_authority: AuthorityState
    entity_filtered_authority: AuthorityState
    dependency_conditioned_authority: AuthorityState
    uncertainty_contract_authority: AuthorityState
    dara_dt_authority: AuthorityState

    no_assurance: OutcomeResult
    global_uncertainty: OutcomeResult
    entity_filtered: OutcomeResult
    dependency_conditioned: OutcomeResult
    uncertainty_contract: OutcomeResult
    dara_dt: OutcomeResult


def _build_decision(
    condition: DecisionRelevanceCondition,
) -> Decision:
    """Create the controlled proposed logistics decision."""

    return Decision(
        decision_id=f"decision_{condition.condition_id}",
        action="assign_vehicle",
        vehicle_id=_SELECTED_ENTITY,
        order_id="order_01",
        timestamp=10.0,
    )


def _required_dependencies(
    condition: DecisionRelevanceCondition,
) -> tuple[str, ...]:
    """Return exact dependencies required by the pending decision."""

    if condition.dependency_family == DependencyFamily.CAPACITY:
        return (f"{_SELECTED_ENTITY}.capacity",)

    if condition.dependency_family == DependencyFamily.STATUS:
        return (f"{_SELECTED_ENTITY}.status",)

    if condition.dependency_family == DependencyFamily.LOCATION_AVAILABILITY:
        return (
            f"{_SELECTED_ENTITY}.location",
            f"{_SELECTED_ENTITY}.available",
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.dependency_family!r}"
    )


def _ground_truth(
    condition: DecisionRelevanceCondition,
    decision: Decision,
) -> GroundTruth:
    """Create evaluator-only ground truth from the frozen validity label."""

    if condition.physically_valid:
        return GroundTruth(
            decision_id=decision.decision_id,
            label=InterventionLabel.DO_NOT_INTERVENE,
            reason=(
                "Frozen EXP-009 condition defines the proposed decision "
                "as physically valid."
            ),
        )

    return GroundTruth(
        decision_id=decision.decision_id,
        label=InterventionLabel.INTERVENE,
        reason=(
            "Frozen EXP-009 condition defines the proposed decision "
            "as physically invalid."
        ),
    )


def _make_evidence(
    *,
    dependency: str,
    observed_value: Any,
    status: EvidenceStatus,
    source: str,
) -> RuntimeEvidence:
    """Create one runtime-evidence item."""

    return RuntimeEvidence(
        source=source,
        dependency=dependency,
        observed_value=observed_value,
        timestamp=10.0,
        confidence=None,
        status=status,
    )


def _available_required_evidence(
    condition: DecisionRelevanceCondition,
) -> tuple[RuntimeEvidence, ...]:
    """Create usable evidence for all required dependencies.

    Values are deliberately based on the controlled runtime observation
    available to assurance, not hidden physical ground truth.
    """

    if condition.dependency_family == DependencyFamily.CAPACITY:
        observed_capacity = (
            8.0 if condition.physically_valid else 4.0
        )

        return (
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.capacity",
                observed_value=observed_capacity,
                status=EvidenceStatus.AVAILABLE,
                source="selected_vehicle_capacity_monitor",
            ),
        )

    if condition.dependency_family == DependencyFamily.STATUS:
        observed_status = (
            "operational"
            if condition.physically_valid
            else "broken_down"
        )

        return (
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.status",
                observed_value=observed_status,
                status=EvidenceStatus.AVAILABLE,
                source="selected_vehicle_status_monitor",
            ),
        )

    if condition.dependency_family == DependencyFamily.LOCATION_AVAILABILITY:
        if condition.physically_valid:
            location = "depot"
            available = True
        else:
            location = "remote"
            available = False

        return (
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.location",
                observed_value=location,
                status=EvidenceStatus.AVAILABLE,
                source="selected_vehicle_location_monitor",
            ),
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.available",
                observed_value=available,
                status=EvidenceStatus.AVAILABLE,
                source="selected_vehicle_availability_monitor",
            ),
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.dependency_family!r}"
    )


def _uncertain_value(
    status: EvidenceStatus,
    available_value: Any,
) -> Any:
    """Return an observation compatible with an evidence-quality state."""

    if status == EvidenceStatus.MISSING:
        return None

    return available_value


def _relevant_imperfect_evidence(
    condition: DecisionRelevanceCondition,
) -> tuple[RuntimeEvidence, ...]:
    """Place imperfect evidence on a required decision dependency."""

    status = condition.evidence_status

    if status not in _UNCERTAIN_STATUSES:
        raise ValueError(
            "Relevant imperfect evidence requires an uncertain status."
        )

    if condition.dependency_family == DependencyFamily.CAPACITY:
        value = 8.0 if condition.physically_valid else 4.0

        return (
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.capacity",
                observed_value=_uncertain_value(status, value),
                status=status,
                source="selected_vehicle_capacity_monitor",
            ),
        )

    if condition.dependency_family == DependencyFamily.STATUS:
        value = (
            "operational"
            if condition.physically_valid
            else "broken_down"
        )

        return (
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.status",
                observed_value=_uncertain_value(status, value),
                status=status,
                source="selected_vehicle_status_monitor",
            ),
        )

    if condition.dependency_family == DependencyFamily.LOCATION_AVAILABILITY:
        if condition.physically_valid:
            location = "depot"
            available = True
        else:
            location = "remote"
            available = False

        return (
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.location",
                observed_value=_uncertain_value(status, location),
                status=status,
                source="selected_vehicle_location_monitor",
            ),
            _make_evidence(
                dependency=f"{_SELECTED_ENTITY}.available",
                observed_value=_uncertain_value(status, available),
                status=status,
                source="selected_vehicle_availability_monitor",
            ),
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.dependency_family!r}"
    )


def _irrelevant_imperfect_evidence(
    condition: DecisionRelevanceCondition,
) -> tuple[RuntimeEvidence, ...]:
    """Create uncertainty outside the pending decision dependencies.

    The uncertain observation belongs to another vehicle. Required evidence
    for the selected vehicle remains available, satisfying the frozen IRR
    protocol.

    This deliberately gives the entity-filtered comparator a fair chance.
    If entity filtering reproduces the dependency-conditioned behaviour,
    EXP-009 must report that equivalence rather than manufacturing an
    advantage for DARA-DT.
    """

    required = _available_required_evidence(condition)
    status = condition.evidence_status

    if status not in _UNCERTAIN_STATUSES:
        raise ValueError(
            "Irrelevant imperfect evidence requires an uncertain status."
        )

    irrelevant = _make_evidence(
        dependency=f"{_OTHER_ENTITY}.status",
        observed_value=_uncertain_value(status, "operational"),
        status=status,
        source="unrelated_vehicle_status_monitor",
    )

    return (*required, irrelevant)


def _build_runtime_evidence(
    condition: DecisionRelevanceCondition,
) -> tuple[RuntimeEvidence, ...]:
    """Build the runtime evidence visible to assurance mechanisms."""

    if condition.is_reliable_control:
        return _available_required_evidence(condition)

    if condition.evidence_relevance == EvidenceRelevance.RELEVANT:
        return _relevant_imperfect_evidence(condition)

    if condition.evidence_relevance == EvidenceRelevance.IRRELEVANT:
        return _irrelevant_imperfect_evidence(condition)

    raise ValueError(
        f"Unsupported evidence relevance: {condition.evidence_relevance!r}"
    )


def _no_assurance_decision(
    decision: Decision,
) -> AssuranceDecision:
    """Evaluate the no-assurance baseline."""

    return NoAssurancePolicy().evaluate(
        decision=decision,
        divergences=[],
    )


def _uncertainty_contract_decision(
    condition: DecisionRelevanceCondition,
    decision: Decision,
    evidence: tuple[RuntimeEvidence, ...],
) -> AssuranceDecision:
    """Evaluate the uncertainty-aware runtime-contract comparator.

    Only evidence belonging to the dependency being contracted is supplied
    to the contract. Unrelated system evidence is not silently converted into
    a decision requirement.
    """

    policy = EvidenceAwareRuntimeContractPolicy()

    evidence_by_dependency = {
        item.dependency: item
        for item in evidence
    }

    if condition.dependency_family == DependencyFamily.CAPACITY:
        item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.capacity"
        ]

        contract_evidence = RuntimeEvidence(
            source=item.source,
            dependency="vehicle.capacity",
            observed_value=item.observed_value,
            timestamp=item.timestamp,
            confidence=item.confidence,
            status=item.status,
        )

        result = policy.evaluate_capacity(
            decision_id=decision.decision_id,
            evidence=contract_evidence,
            required_demand=_ORDER_DEMAND,
        )

    elif condition.dependency_family == DependencyFamily.STATUS:
        item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.status"
        ]

        contract_evidence = RuntimeEvidence(
            source=item.source,
            dependency="vehicle.status",
            observed_value=item.observed_value,
            timestamp=item.timestamp,
            confidence=item.confidence,
            status=item.status,
        )

        result = policy.evaluate_status(
            decision_id=decision.decision_id,
            evidence=contract_evidence,
            required_status=_REQUIRED_STATUS,
        )

    elif condition.dependency_family == DependencyFamily.LOCATION_AVAILABILITY:
        location_item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.location"
        ]
        availability_item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.available"
        ]

        location_evidence = RuntimeEvidence(
            source=location_item.source,
            dependency="vehicle.location",
            observed_value=location_item.observed_value,
            timestamp=location_item.timestamp,
            confidence=location_item.confidence,
            status=location_item.status,
        )

        availability_evidence = RuntimeEvidence(
            source=availability_item.source,
            dependency="vehicle.available",
            observed_value=availability_item.observed_value,
            timestamp=availability_item.timestamp,
            confidence=availability_item.confidence,
            status=availability_item.status,
        )

        result = policy.evaluate_location_availability(
            decision_id=decision.decision_id,
            location_evidence=location_evidence,
            availability_evidence=availability_evidence,
            permitted_locations=_PERMITTED_LOCATIONS,
            required_available=_REQUIRED_AVAILABLE,
        )

    else:
        raise ValueError(
            f"Unsupported dependency family: "
            f"{condition.dependency_family!r}"
        )

    return AssuranceDecision(
        decision_id=decision.decision_id,
        authority=result.authority,
        reason=result.reason,
        relevant_divergence_count=0,
    )


def _dara_dt_decision(
    condition: DecisionRelevanceCondition,
    decision: Decision,
    evidence: tuple[RuntimeEvidence, ...],
) -> AssuranceDecision:
    """Evaluate decision-conditioned DARA-DT assurance.

    The DARA policy receives only the exact evidence required by the
    pending decision. Physical ground truth remains unavailable.
    """

    policy = DivergenceEvidencePolicy()

    evidence_by_dependency = {
        item.dependency: item
        for item in evidence
    }

    if condition.dependency_family == DependencyFamily.CAPACITY:
        item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.capacity"
        ]

        dara_evidence = RuntimeEvidence(
            source=item.source,
            dependency="vehicle.capacity",
            observed_value=item.observed_value,
            timestamp=item.timestamp,
            confidence=item.confidence,
            status=item.status,
        )

        return policy.evaluate_capacity(
            decision_id=decision.decision_id,
            evidence=dara_evidence,
            twin_capacity=10.0,
            required_demand=_ORDER_DEMAND,
        )

    if condition.dependency_family == DependencyFamily.STATUS:
        item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.status"
        ]

        dara_evidence = RuntimeEvidence(
            source=item.source,
            dependency="vehicle.status",
            observed_value=item.observed_value,
            timestamp=item.timestamp,
            confidence=item.confidence,
            status=item.status,
        )

        return policy.evaluate_status(
            decision_id=decision.decision_id,
            evidence=dara_evidence,
            twin_status="operational",
            required_status=_REQUIRED_STATUS,
        )

    if condition.dependency_family == DependencyFamily.LOCATION_AVAILABILITY:
        location_item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.location"
        ]
        availability_item = evidence_by_dependency[
            f"{_SELECTED_ENTITY}.available"
        ]

        location_evidence = RuntimeEvidence(
            source=location_item.source,
            dependency="vehicle.location",
            observed_value=location_item.observed_value,
            timestamp=location_item.timestamp,
            confidence=location_item.confidence,
            status=location_item.status,
        )

        availability_evidence = RuntimeEvidence(
            source=availability_item.source,
            dependency="vehicle.available",
            observed_value=availability_item.observed_value,
            timestamp=availability_item.timestamp,
            confidence=availability_item.confidence,
            status=availability_item.status,
        )

        return policy.evaluate_location_availability(
            decision_id=decision.decision_id,
            location_evidence=location_evidence,
            availability_evidence=availability_evidence,
            twin_location="depot",
            twin_available=True,
            permitted_locations=_PERMITTED_LOCATIONS,
            required_available=_REQUIRED_AVAILABLE,
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.dependency_family!r}"
    )


def _evaluate_outcome(
    ground_truth: GroundTruth,
    assurance: AssuranceDecision,
) -> OutcomeResult:
    """Evaluate one assurance decision against evaluator-only truth."""

    return OutcomeEvaluator().evaluate(
        ground_truth=ground_truth,
        assurance=assurance,
    )


def run_condition(
    condition: DecisionRelevanceCondition,
) -> DecisionRelevanceExperimentResult:
    """Execute one frozen EXP-009 condition."""

    decision = _build_decision(condition)

    ground_truth = _ground_truth(
        condition=condition,
        decision=decision,
    )

    required_dependencies = _required_dependencies(condition)

    runtime_evidence = _build_runtime_evidence(condition)

    no_assurance_decision = _no_assurance_decision(decision)

    global_uncertainty_decision = (
        GlobalEvidenceUncertaintyPolicy().evaluate(
            evidence=runtime_evidence,
            decision_id=decision.decision_id,
        )
    )

    entity_filtered_decision = EntityFilteredEvidencePolicy().evaluate(
        evidence=runtime_evidence,
        selected_entity=_SELECTED_ENTITY,
        decision_id=decision.decision_id,
    )

    dependency_conditioned_decision = (
        DependencyConditionedEvidencePolicy().evaluate(
            evidence=runtime_evidence,
            required_dependencies=set(required_dependencies),
            decision_id=decision.decision_id,
        )
    )

    uncertainty_contract_decision = _uncertainty_contract_decision(
        condition=condition,
        decision=decision,
        evidence=runtime_evidence,
    )

    dara_dt_decision = _dara_dt_decision(
        condition=condition,
        decision=decision,
        evidence=runtime_evidence,
    )

    return DecisionRelevanceExperimentResult(
        condition=condition,
        decision=decision,
        ground_truth=ground_truth,
        evidence_status=condition.evidence_status,
        evidence_relevance=condition.evidence_relevance,
        required_dependencies=required_dependencies,
        runtime_evidence=runtime_evidence,
        no_assurance_authority=no_assurance_decision.authority,
        global_uncertainty_authority=global_uncertainty_decision.authority,
        entity_filtered_authority=entity_filtered_decision.authority,
        dependency_conditioned_authority=(
            dependency_conditioned_decision.authority
        ),
        uncertainty_contract_authority=(
            uncertainty_contract_decision.authority
        ),
        dara_dt_authority=dara_dt_decision.authority,
        no_assurance=_evaluate_outcome(
            ground_truth,
            no_assurance_decision,
        ),
        global_uncertainty=_evaluate_outcome(
            ground_truth,
            global_uncertainty_decision,
        ),
        entity_filtered=_evaluate_outcome(
            ground_truth,
            entity_filtered_decision,
        ),
        dependency_conditioned=_evaluate_outcome(
            ground_truth,
            dependency_conditioned_decision,
        ),
        uncertainty_contract=_evaluate_outcome(
            ground_truth,
            uncertainty_contract_decision,
        ),
        dara_dt=_evaluate_outcome(
            ground_truth,
            dara_dt_decision,
        ),
    )


def run_decision_relevance_experiment(
) -> tuple[DecisionRelevanceExperimentResult, ...]:
    """Execute all 42 frozen EXP-009 conditions in registered order."""

    return tuple(
        run_condition(condition)
        for condition in EXP009_CONDITIONS
    )
