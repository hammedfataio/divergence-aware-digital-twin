"""EXP-006 imperfect-runtime-evidence experiment.

This experiment evaluates runtime assurance when the evidence available
to the assurance mechanism is imperfect.

Physical ground truth, Digital Twin state, and runtime evidence remain
separate throughout the experiment. This prevents the assurance policy
from accessing evaluator-only physical truth.
"""

from dataclasses import dataclass

from dara_dt.assurance.evidence_policy import EvidenceAwareDecisionPolicy
from dara_dt.assurance.impact_policy import DecisionImpactPolicy
from dara_dt.assurance.model import AssuranceDecision
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.relevance import DecisionRelevanceAnalyzer
from dara_dt.evaluation.outcomes import OutcomeEvaluator, OutcomeResult
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.evidence.generator import EvidenceGenerator
from dara_dt.evidence.model import RuntimeEvidence
from dara_dt.experiments.evidence_conditions import (
    EvidenceCondition,
    EvidenceConditionType,
    build_evidence_conditions,
)
from dara_dt.impact.analyser import DecisionImpactAnalyser
from dara_dt.impact.model import ImpactEvidence
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin
from dara_dt.decision.dependency import DependencyMapper


@dataclass(frozen=True)
class EvidenceExperimentResult:
    """Outputs from one controlled EXP-006 condition."""

    condition: EvidenceCondition
    runtime_evidence: tuple[RuntimeEvidence, ...]
    evidence_aware_assurance: AssuranceDecision
    evidence_aware_outcome: OutcomeResult
    relevance_assurance: AssuranceDecision
    relevance_outcome: OutcomeResult
    deterministic_impact_assurance: AssuranceDecision
    deterministic_impact_outcome: OutcomeResult


def _build_runtime_evidence(
    condition: EvidenceCondition,
) -> tuple[RuntimeEvidence, ...]:
    """Create runtime evidence for one controlled condition."""

    generator = EvidenceGenerator()

    if condition.evidence_type == EvidenceConditionType.ACCURATE:
        return (
            generator.accurate(
                dependency="vehicle.capacity",
                physical_value=condition.observed_capacity,
                timestamp=condition.observation_timestamp,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.NOISY:
        error = (
            condition.observed_capacity
            - condition.physical_capacity
        )

        return (
            generator.noisy(
                dependency="vehicle.capacity",
                physical_value=condition.physical_capacity,
                error=error,
                timestamp=condition.observation_timestamp,
                confidence=condition.confidence,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.STALE:
        return (
            generator.stale(
                dependency="vehicle.capacity",
                stale_value=condition.observed_capacity,
                observation_timestamp=condition.observation_timestamp,
                confidence=condition.confidence,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.MISSING:
        return (
            generator.missing(
                dependency="vehicle.capacity",
                timestamp=condition.observation_timestamp,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.CONFLICTING:
        return generator.conflicting(
            dependency="vehicle.capacity",
            first_value=condition.observed_capacity,
            second_value=condition.secondary_observed_capacity,
            timestamp=condition.observation_timestamp,
            confidence=condition.confidence,
        )

    raise ValueError(
        f"Unsupported evidence condition: {condition.evidence_type}"
    )


def run_evidence_condition(
    condition: EvidenceCondition,
) -> EvidenceExperimentResult:
    """Run one controlled EXP-006 condition."""

    environment = LogisticsEnvironment()

    vehicle = Vehicle(
        vehicle_id="vehicle_001",
        capacity=condition.twin_capacity,
        location="depot",
    )
    environment.add_vehicle(vehicle)

    order = Order(
        order_id="order_001",
        demand=condition.demand,
        location="customer",
        deadline=100.0,
    )
    environment.add_order(order)

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    # Physical reality changes after the Twin snapshot.
    environment.vehicles["vehicle_001"].capacity = (
        condition.physical_capacity
    )

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_001",
        timestamp=condition.evaluation_timestamp,
        decision_id=f"decision_{condition.condition_id}",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        physical_state=environment.physical_state(),
        twin_state=twin.state,
    )

    relevance_analyser = DecisionRelevanceAnalyzer(
        DependencyMapper()
    )

    relevance = relevance_analyser.analyse(
        decision=decision,
        divergences=divergences,
    )

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=decision,
        physical_state=environment.physical_state(),
    )

    outcome_evaluator = OutcomeEvaluator()

    # ---------------------------------------------------------
    # Baseline: decision relevance only
    # ---------------------------------------------------------

    relevance_policy = DivergenceAwarePolicy()

    relevance_assurance = relevance_policy.evaluate(
        decision=decision,
        relevance=relevance,
    )

    relevance_outcome = outcome_evaluator.evaluate(
        ground_truth,
        relevance_assurance,
    )

    # ---------------------------------------------------------
    # Baseline: deterministic decision impact
    #
    # This deliberately reproduces the EXP-005 assumption that
    # runtime capacity evidence is perfectly observed.
    # ---------------------------------------------------------

    impact_analyser = DecisionImpactAnalyser()

    perfect_impact_evidence = ImpactEvidence(
        source="perfect_runtime_capacity",
        dependency="vehicle.capacity",
        observed_value=condition.physical_capacity,
        twin_value=condition.twin_capacity,
    )

    impact = impact_analyser.analyse_capacity(
        decision=decision,
        evidence=perfect_impact_evidence,
        demand=condition.demand,
    )

    impact_policy = DecisionImpactPolicy()

    deterministic_impact_assurance = impact_policy.evaluate(
        decision=decision,
        impact=impact,
    )

    deterministic_impact_outcome = outcome_evaluator.evaluate(
        ground_truth,
        deterministic_impact_assurance,
    )

    # ---------------------------------------------------------
    # Proposed EXP-006 policy: evidence-aware decision assurance
    # ---------------------------------------------------------

    runtime_evidence = _build_runtime_evidence(condition)

    evidence_policy = EvidenceAwareDecisionPolicy()

    evidence_aware_assurance = evidence_policy.evaluate(
        decision=decision,
        evidence=runtime_evidence,
        demand=condition.demand,
        current_time=condition.evaluation_timestamp,
    )

    evidence_aware_outcome = outcome_evaluator.evaluate(
        ground_truth,
        evidence_aware_assurance,
    )

    return EvidenceExperimentResult(
        condition=condition,
        runtime_evidence=runtime_evidence,
        evidence_aware_assurance=evidence_aware_assurance,
        evidence_aware_outcome=evidence_aware_outcome,
        relevance_assurance=relevance_assurance,
        relevance_outcome=relevance_outcome,
        deterministic_impact_assurance=deterministic_impact_assurance,
        deterministic_impact_outcome=deterministic_impact_outcome,
    )


def run_evidence_experiment() -> tuple[EvidenceExperimentResult, ...]:
    """Run the complete deterministic EXP-006 evidence matrix."""

    return tuple(
        run_evidence_condition(condition)
        for condition in build_evidence_conditions()
    )


if __name__ == "__main__":
    results = run_evidence_experiment()

    for result in results:
        print(
            result.condition.condition_id,
            result.condition.evidence_type.value,
            result.condition.physical_valid,
            result.evidence_aware_assurance.authority.value,
            result.evidence_aware_outcome.outcome.value,
        )
