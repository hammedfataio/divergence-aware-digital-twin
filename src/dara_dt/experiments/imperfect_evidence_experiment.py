"""EXP-008 imperfect-evidence contract comparison.

This experiment evaluates runtime assurance when the observations available
to assurance mechanisms cannot be assumed to represent current physical
reality perfectly.

EXP-008 deliberately separates three information layers:

    Physical ground truth
    Digital Twin state
    Runtime evidence

Physical ground truth is used only by the independent evaluator. Runtime
assurance policies receive Digital Twin state and/or runtime evidence, but
never the physical ground-truth value.

The experiment compares:

P0 - No Assurance
P1 - Global Evidence-Divergence
P2 - Direct Runtime Contract
P3 - Uncertainty-Aware Runtime Contract
P4 - DARA-DT Evidence-Aware Assurance

The central comparison is P3 versus P4. Both policies receive the same
runtime evidence. If the simpler uncertainty-aware contract reproduces the
behaviour of DARA-DT, that is a valid falsification outcome rather than a
result to be hidden.
"""

from dataclasses import dataclass
from typing import Any

from dara_dt.assurance.baselines import NoAssurancePolicy
from dara_dt.assurance.contract_policy import RuntimeContractPolicy
from dara_dt.assurance.divergence_evidence_policy import (
    DivergenceEvidencePolicy,
)
from dara_dt.assurance.evidence_contract_policy import (
    EvidenceAwareRuntimeContractPolicy,
)
from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence
from dara_dt.evaluation.outcomes import OutcomeEvaluator, OutcomeResult
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.evidence.model import EvidenceStatus, RuntimeEvidence
from dara_dt.experiments.cross_dependency_conditions import DependencyFamily
from dara_dt.experiments.ground_truth import GroundTruth
from dara_dt.experiments.imperfect_evidence_conditions import (
    ImperfectEvidenceCondition,
    build_imperfect_evidence_conditions,
)


@dataclass(frozen=True)
class ImperfectEvidenceExperimentResult:
    """Result for one controlled EXP-008 condition."""

    condition: ImperfectEvidenceCondition
    decision: Decision
    ground_truth: GroundTruth

    evidence_status: EvidenceStatus
    runtime_divergence_count: int

    no_assurance_authority: AuthorityState
    global_divergence_authority: AuthorityState
    direct_contract_authority: AuthorityState
    uncertainty_contract_authority: AuthorityState
    dara_dt_authority: AuthorityState

    no_assurance: OutcomeResult
    global_divergence: OutcomeResult
    direct_contract: OutcomeResult
    uncertainty_contract: OutcomeResult
    dara_dt: OutcomeResult


def _build_decision(
    condition: ImperfectEvidenceCondition,
) -> Decision:
    """Create the fixed proposed logistics decision."""

    return Decision(
        decision_id=f"decision_{condition.condition_id}",
        action="assign_vehicle",
        vehicle_id="vehicle_01",
        order_id="order_01",
        timestamp=condition.evaluation_timestamp,
    )


def _base_vehicle_state() -> dict[str, Any]:
    """Return a valid default vehicle state."""

    return {
        "vehicle_id": "vehicle_01",
        "capacity": 10.0,
        "location": "depot",
        "available": True,
        "status": "operational",
    }


def _base_order_state(
    condition: ImperfectEvidenceCondition,
) -> dict[str, Any]:
    """Return the controlled order state."""

    return {
        "order_id": "order_01",
        "demand": condition.order_demand,
        "location": "customer_01",
        "deadline": 20.0,
        "status": "waiting",
    }


def _build_physical_state(
    condition: ImperfectEvidenceCondition,
) -> dict[str, Any]:
    """Build physical ground truth for independent evaluation.

    This state must never be passed to a runtime assurance policy.
    """

    vehicle = _base_vehicle_state()

    if condition.family == DependencyFamily.CAPACITY:
        vehicle["capacity"] = condition.physical_value

    elif condition.family == DependencyFamily.STATUS:
        vehicle["status"] = condition.physical_value

    elif condition.family == DependencyFamily.LOCATION_AVAILABILITY:
        location, available = condition.physical_value
        vehicle["location"] = location
        vehicle["available"] = available

    else:
        raise ValueError(
            f"Unsupported dependency family: {condition.family!r}"
        )

    return {
        "vehicles": {
            "vehicle_01": vehicle,
        },
        "orders": {
            "order_01": _base_order_state(condition),
        },
    }


def _build_ground_truth(
    condition: ImperfectEvidenceCondition,
    decision: Decision,
) -> GroundTruth:
    """Derive intervention ground truth from physical state only."""

    physical_state = _build_physical_state(condition)
    validator = PhysicalDecisionValidator()

    permitted_locations = None

    if condition.family == DependencyFamily.LOCATION_AVAILABILITY:
        permitted_locations = condition.permitted_locations

    return validator.ground_truth(
        decision=decision,
        physical_state=physical_state,
        permitted_vehicle_locations=permitted_locations,
    )


def _make_evidence(
    *,
    source: str,
    dependency: str,
    observed_value: Any,
    condition: ImperfectEvidenceCondition,
) -> RuntimeEvidence:
    """Create runtime evidence without exposing physical ground truth."""

    return RuntimeEvidence(
        source=source,
        dependency=dependency,
        observed_value=observed_value,
        timestamp=condition.observation_timestamp,
        confidence=None,
        status=condition.evidence_status,
    )


def _build_runtime_evidence(
    condition: ImperfectEvidenceCondition,
) -> tuple[RuntimeEvidence, ...]:
    """Build the runtime observations visible to assurance policies."""

    status = condition.evidence_status

    if condition.family == DependencyFamily.CAPACITY:
        observed = (
            None
            if status == EvidenceStatus.MISSING
            else condition.primary_evidence_value
        )

        return (
            _make_evidence(
                source="runtime_capacity_monitor",
                dependency="vehicle.capacity",
                observed_value=observed,
                condition=condition,
            ),
        )

    if condition.family == DependencyFamily.STATUS:
        observed = (
            None
            if status == EvidenceStatus.MISSING
            else condition.primary_evidence_value
        )

        return (
            _make_evidence(
                source="runtime_status_monitor",
                dependency="vehicle.status",
                observed_value=observed,
                condition=condition,
            ),
        )

    if condition.family == DependencyFamily.LOCATION_AVAILABILITY:
        if status == EvidenceStatus.MISSING:
            location_value = None
            availability_value = None
        else:
            (
                location_value,
                availability_value,
            ) = condition.primary_evidence_value

        return (
            _make_evidence(
                source="runtime_location_monitor",
                dependency="vehicle.location",
                observed_value=location_value,
                condition=condition,
            ),
            _make_evidence(
                source="runtime_availability_monitor",
                dependency="vehicle.available",
                observed_value=availability_value,
                condition=condition,
            ),
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.family!r}"
    )


def _runtime_divergences(
    condition: ImperfectEvidenceCondition,
    evidence: tuple[RuntimeEvidence, ...],
) -> list[Divergence]:
    """Infer observable Twin mismatch from runtime evidence.

    This baseline deliberately does not use physical ground truth.

    Missing evidence cannot establish an observed mismatch.

    Stale or conflicting evidence can still contain an observed value, but
    this global baseline does not reason about evidence quality. It simply
    compares the visible observation with the Digital Twin value.

    This makes the baseline intentionally simple and distinguishes it from
    the evidence-aware policies.
    """

    divergences: list[Divergence] = []

    if condition.family == DependencyFamily.CAPACITY:
        item = evidence[0]

        if (
            item.observed_value is not None
            and item.observed_value != condition.twin_value
        ):
            divergences.append(
                Divergence(
                    entity_type="vehicles",
                    entity_id="vehicle_01",
                    variable="capacity",
                    physical_value=item.observed_value,
                    twin_value=condition.twin_value,
                )
            )

        return divergences

    if condition.family == DependencyFamily.STATUS:
        item = evidence[0]

        if (
            item.observed_value is not None
            and item.observed_value != condition.twin_value
        ):
            divergences.append(
                Divergence(
                    entity_type="vehicles",
                    entity_id="vehicle_01",
                    variable="status",
                    physical_value=item.observed_value,
                    twin_value=condition.twin_value,
                )
            )

        return divergences

    if condition.family == DependencyFamily.LOCATION_AVAILABILITY:
        location_evidence, availability_evidence = evidence
        twin_location, twin_available = condition.twin_value

        if (
            location_evidence.observed_value is not None
            and location_evidence.observed_value != twin_location
        ):
            divergences.append(
                Divergence(
                    entity_type="vehicles",
                    entity_id="vehicle_01",
                    variable="location",
                    physical_value=location_evidence.observed_value,
                    twin_value=twin_location,
                )
            )

        if (
            availability_evidence.observed_value is not None
            and availability_evidence.observed_value != twin_available
        ):
            divergences.append(
                Divergence(
                    entity_type="vehicles",
                    entity_id="vehicle_01",
                    variable="available",
                    physical_value=availability_evidence.observed_value,
                    twin_value=twin_available,
                )
            )

        return divergences

    raise ValueError(
        f"Unsupported dependency family: {condition.family!r}"
    )


def _global_divergence_decision(
    decision: Decision,
    divergences: list[Divergence],
) -> AssuranceDecision:
    """Apply a simple any-observed-divergence baseline."""

    if not divergences:
        return AssuranceDecision(
            decision_id=decision.decision_id,
            authority=AuthorityState.ALLOW,
            reason=(
                "No runtime-observable Digital Twin divergence detected."
            ),
            relevant_divergence_count=0,
        )

    return AssuranceDecision(
        decision_id=decision.decision_id,
        authority=AuthorityState.DEFER,
        reason=(
            "At least one runtime-observable Digital Twin divergence "
            "was detected."
        ),
        relevant_divergence_count=len(divergences),
    )


def _direct_contract_decision(
    condition: ImperfectEvidenceCondition,
    decision: Decision,
    evidence: tuple[RuntimeEvidence, ...],
) -> AssuranceDecision:
    """Evaluate the ordinary direct runtime-contract baseline.

    This comparator does not understand evidence-quality metadata.

    When no observation exists, the direct contract cannot evaluate the
    requirement and therefore allows by default. This behaviour is kept
    explicit so EXP-008 can distinguish ordinary contracts from the stronger
    uncertainty-aware contract comparator.

    Stale and conflicting observations are treated only as observed values;
    their quality labels are ignored by this baseline.
    """

    policy = RuntimeContractPolicy()

    if condition.family == DependencyFamily.CAPACITY:
        item = evidence[0]

        if item.observed_value is None:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.ALLOW,
                reason=(
                    "Direct contract received no observable capacity value."
                ),
                relevant_divergence_count=0,
            )

        result = policy.evaluate_capacity(
            decision_id=decision.decision_id,
            observed_capacity=item.observed_value,
            required_demand=condition.order_demand,
        )

    elif condition.family == DependencyFamily.STATUS:
        item = evidence[0]

        if item.observed_value is None:
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.ALLOW,
                reason=(
                    "Direct contract received no observable status value."
                ),
                relevant_divergence_count=0,
            )

        result = policy.evaluate_status(
            decision_id=decision.decision_id,
            observed_status=item.observed_value,
            required_status=condition.required_status,
        )

    elif condition.family == DependencyFamily.LOCATION_AVAILABILITY:
        location_evidence, availability_evidence = evidence

        if (
            location_evidence.observed_value is None
            or availability_evidence.observed_value is None
        ):
            return AssuranceDecision(
                decision_id=decision.decision_id,
                authority=AuthorityState.ALLOW,
                reason=(
                    "Direct contract received incomplete dispatch evidence."
                ),
                relevant_divergence_count=0,
            )

        result = policy.evaluate_location_availability(
            decision_id=decision.decision_id,
            observed_location=location_evidence.observed_value,
            observed_available=availability_evidence.observed_value,
            permitted_locations=condition.permitted_locations,
            required_available=condition.required_available,
        )

    else:
        raise ValueError(
            f"Unsupported dependency family: {condition.family!r}"
        )

    authority = (
        AuthorityState.ALLOW
        if not result.intervene
        else AuthorityState.RESTRICT
    )

    return AssuranceDecision(
        decision_id=decision.decision_id,
        authority=authority,
        reason=result.reason,
        relevant_divergence_count=0,
    )


def _uncertainty_contract_decision(
    condition: ImperfectEvidenceCondition,
    decision: Decision,
    evidence: tuple[RuntimeEvidence, ...],
) -> AssuranceDecision:
    """Evaluate the fair uncertainty-aware contract comparator."""

    policy = EvidenceAwareRuntimeContractPolicy()

    if condition.family == DependencyFamily.CAPACITY:
        result = policy.evaluate_capacity(
            decision_id=decision.decision_id,
            evidence=evidence[0],
            required_demand=condition.order_demand,
        )

    elif condition.family == DependencyFamily.STATUS:
        result = policy.evaluate_status(
            decision_id=decision.decision_id,
            evidence=evidence[0],
            required_status=condition.required_status,
        )

    elif condition.family == DependencyFamily.LOCATION_AVAILABILITY:
        result = policy.evaluate_location_availability(
            decision_id=decision.decision_id,
            location_evidence=evidence[0],
            availability_evidence=evidence[1],
            permitted_locations=condition.permitted_locations,
            required_available=condition.required_available,
        )

    else:
        raise ValueError(
            f"Unsupported dependency family: {condition.family!r}"
        )

    return AssuranceDecision(
        decision_id=decision.decision_id,
        authority=result.authority,
        reason=result.reason,
        relevant_divergence_count=0,
    )


def _dara_dt_decision(
    condition: ImperfectEvidenceCondition,
    decision: Decision,
    evidence: tuple[RuntimeEvidence, ...],
) -> AssuranceDecision:
    """Evaluate evidence-aware DARA-DT using the same runtime evidence."""

    policy = DivergenceEvidencePolicy()

    if condition.family == DependencyFamily.CAPACITY:
        return policy.evaluate_capacity(
            decision_id=decision.decision_id,
            evidence=evidence[0],
            twin_capacity=condition.twin_value,
            required_demand=condition.order_demand,
        )

    if condition.family == DependencyFamily.STATUS:
        return policy.evaluate_status(
            decision_id=decision.decision_id,
            evidence=evidence[0],
            twin_status=condition.twin_value,
            required_status=condition.required_status,
        )

    if condition.family == DependencyFamily.LOCATION_AVAILABILITY:
        twin_location, twin_available = condition.twin_value

        return policy.evaluate_location_availability(
            decision_id=decision.decision_id,
            location_evidence=evidence[0],
            availability_evidence=evidence[1],
            twin_location=twin_location,
            twin_available=twin_available,
            permitted_locations=condition.permitted_locations,
            required_available=condition.required_available,
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.family!r}"
    )


def run_condition(
    condition: ImperfectEvidenceCondition,
) -> ImperfectEvidenceExperimentResult:
    """Run one EXP-008 controlled condition."""

    decision = _build_decision(condition)

    # Physical ground truth is derived independently and is never passed
    # into any runtime assurance policy.
    ground_truth = _build_ground_truth(
        condition=condition,
        decision=decision,
    )

    evidence = _build_runtime_evidence(condition)

    runtime_divergences = _runtime_divergences(
        condition=condition,
        evidence=evidence,
    )

    no_assurance_decision = NoAssurancePolicy().evaluate(
        decision=decision,
        divergences=runtime_divergences,
    )

    global_divergence_decision = _global_divergence_decision(
        decision=decision,
        divergences=runtime_divergences,
    )

    direct_contract_decision = _direct_contract_decision(
        condition=condition,
        decision=decision,
        evidence=evidence,
    )

    uncertainty_contract_decision = _uncertainty_contract_decision(
        condition=condition,
        decision=decision,
        evidence=evidence,
    )

    dara_dt_decision = _dara_dt_decision(
        condition=condition,
        decision=decision,
        evidence=evidence,
    )

    evaluator = OutcomeEvaluator()

    return ImperfectEvidenceExperimentResult(
        condition=condition,
        decision=decision,
        ground_truth=ground_truth,
        evidence_status=condition.evidence_status,
        runtime_divergence_count=len(runtime_divergences),
        no_assurance_authority=no_assurance_decision.authority,
        global_divergence_authority=global_divergence_decision.authority,
        direct_contract_authority=direct_contract_decision.authority,
        uncertainty_contract_authority=(
            uncertainty_contract_decision.authority
        ),
        dara_dt_authority=dara_dt_decision.authority,
        no_assurance=evaluator.evaluate(
            ground_truth,
            no_assurance_decision,
        ),
        global_divergence=evaluator.evaluate(
            ground_truth,
            global_divergence_decision,
        ),
        direct_contract=evaluator.evaluate(
            ground_truth,
            direct_contract_decision,
        ),
        uncertainty_contract=evaluator.evaluate(
            ground_truth,
            uncertainty_contract_decision,
        ),
        dara_dt=evaluator.evaluate(
            ground_truth,
            dara_dt_decision,
        ),
    )


def run_imperfect_evidence_experiment(
) -> tuple[ImperfectEvidenceExperimentResult, ...]:
    """Run the complete pre-registered 24-condition EXP-008 matrix."""

    return tuple(
        run_condition(condition)
        for condition in build_imperfect_evidence_conditions()
    )


def _print_results(
    results: tuple[ImperfectEvidenceExperimentResult, ...],
) -> None:
    """Print a compact human-readable EXP-008 result table."""

    print("\nEXP-008 — Imperfect Evidence Contract Comparison")
    print("=" * 96)

    header = (
        f"{'Condition':<12}"
        f"{'Evidence':<13}"
        f"{'Truth':<12}"
        f"{'NoAssur':<11}"
        f"{'Global':<11}"
        f"{'Direct':<11}"
        f"{'Uncert':<11}"
        f"{'DARA':<11}"
    )

    print(header)
    print("-" * 96)

    for result in results:
        truth = (
            "INTERVENE"
            if result.ground_truth.intervention_required
            else "ALLOW"
        )

        print(
            f"{result.condition.condition_id:<12}"
            f"{result.evidence_status.value:<13}"
            f"{truth:<12}"
            f"{result.no_assurance_authority.value:<11}"
            f"{result.global_divergence_authority.value:<11}"
            f"{result.direct_contract_authority.value:<11}"
            f"{result.uncertainty_contract_authority.value:<11}"
            f"{result.dara_dt_authority.value:<11}"
        )


def main() -> None:
    """Run EXP-008 from the command line."""

    results = run_imperfect_evidence_experiment()
    _print_results(results)


if __name__ == "__main__":
    main()
