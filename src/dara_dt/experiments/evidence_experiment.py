"""EXP-006: imperfect runtime evidence experiment.

This experiment evaluates runtime assurance when the evidence available
to the assurance mechanism differs from physical ground truth.

The experiment deliberately separates:

    Physical ground truth
    Digital Twin state
    Runtime evidence

Physical state is used for independent evaluation. The evidence-aware
assurance policy receives only the runtime evidence defined by each
experimental condition.

The deterministic decision-impact baseline represents the EXP-005
perfect-observation assumption and is retained as a comparison point.
"""

from dataclasses import dataclass

from dara_dt.assurance.evidence_policy import EvidenceAwareDecisionPolicy
from dara_dt.assurance.impact_policy import DecisionImpactPolicy
from dara_dt.assurance.model import AssuranceDecision
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.decision.dependency import DependencyMapper
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
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class EvidenceExperimentResult:
    """Result of one controlled EXP-006 condition."""

    condition: EvidenceCondition
    decision_id: str
    runtime_evidence: tuple[RuntimeEvidence, ...]
    relevance_assurance: AssuranceDecision
    deterministic_impact_assurance: AssuranceDecision
    evidence_aware_assurance: AssuranceDecision
    relevance_outcome: OutcomeResult
    deterministic_impact_outcome: OutcomeResult
    evidence_aware_outcome: OutcomeResult


def _build_runtime_evidence(
    condition: EvidenceCondition,
    generator: EvidenceGenerator,
) -> tuple[RuntimeEvidence, ...]:
    """Generate runtime evidence specified by an EXP-006 condition."""

    common = {
        "dependency": "vehicle.capacity",
    }

    if condition.evidence_type == EvidenceConditionType.ACCURATE:
        return (
            generator.accurate(
                **common,
                physical_value=condition.physical_capacity,
                timestamp=condition.observation_timestamp,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.NOISY:
        if condition.observed_capacity is None:
            raise ValueError(
                "Noisy evidence condition requires an observed capacity."
            )

        error = (
            condition.observed_capacity
            - condition.physical_capacity
        )

        return (
            generator.noisy(
                **common,
                physical_value=condition.physical_capacity,
                error=error,
                timestamp=condition.observation_timestamp,
                confidence=condition.confidence,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.STALE:
        if condition.observed_capacity is None:
            raise ValueError(
                "Stale evidence condition requires an observed capacity."
            )

        return (
            generator.stale(
                **common,
                stale_value=condition.observed_capacity,
                observation_timestamp=condition.observation_timestamp,
                confidence=condition.confidence,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.MISSING:
        return (
            generator.missing(
                **common,
                timestamp=condition.observation_timestamp,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.CONFLICTING:
        if condition.observed_capacity is None:
            raise ValueError(
                "Conflicting evidence requires a primary observation."
            )

        if condition.secondary_observed_capacity is None:
            raise ValueError(
                "Conflicting evidence requires a secondary observation."
            )

        return generator.conflicting(
            **common,
            first_value=condition.observed_capacity,
            second_value=condition.secondary_observed_capacity,
            timestamp=condition.observation_timestamp,
            confidence=condition.confidence,
        )

    raise ValueError(
        f"Unsupported evidence condition: {condition.evidence_type}"
    )


def _deterministic_impact_assurance(
    *,
    decision,
    condition: EvidenceCondition,
) -> AssuranceDecision:
    """Reproduce the EXP-005 perfect-observation impact baseline.

    EXP-005 assumed that the runtime observation of physical capacity
    was correct. EXP-006 challenges that assumption.

    This helper therefore supplies the physical capacity directly to
    the existing DecisionImpactAnalyser as the observed value.

    Physical ground truth is used here only because this policy is an
    explicit perfect-evidence experimental baseline. It is not the
    proposed EXP-006 evidence-aware policy.
    """

    analyser = DecisionImpactAnalyser()

    impact = analyser.analyse_capacity(
        decision_id=decision.decision_id,
        twin_capacity=condition.twin_capacity,
        observed_capacity=condition.physical_capacity,
        demand=condition.demand,
        evidence=None,
    )

    return DecisionImpactPolicy().evaluate(
        decision=decision,
        impact=impact,
    )


def run_evidence_condition(
    condition: EvidenceCondition,
) -> EvidenceExperimentResult:
    """Run one controlled EXP-006 condition."""

    # ---------------------------------------------------------
    # 1. Create physical logistics environment
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # 2. Synchronise the Digital Twin
    # ---------------------------------------------------------

    twin = DigitalTwin()
    twin.synchronise(
        environment.physical_state()
    )

    # ---------------------------------------------------------
    # 3. Change physical reality after Twin synchronisation
    # ---------------------------------------------------------

    environment.vehicles["vehicle_001"].capacity = (
        condition.physical_capacity
    )

    # ---------------------------------------------------------
    # 4. AI controller makes its decision from the stale Twin
    # ---------------------------------------------------------

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_001",
        timestamp=condition.evaluation_timestamp,
        decision_id=f"decision_{condition.condition_id}",
    )

    # ---------------------------------------------------------
    # 5. Detect physical-digital divergence
    # ---------------------------------------------------------

    detector = DivergenceDetector()

    divergences = detector.detect(
        physical_state=environment.physical_state(),
        twin_state=twin.state,
    )

    # ---------------------------------------------------------
    # 6. Determine decision relevance
    # ---------------------------------------------------------

    relevance_analyser = DecisionRelevanceAnalyzer(
        DependencyMapper()
    )

    relevance = relevance_analyser.analyse(
        decision=decision,
        divergences=divergences,
    )

    # ---------------------------------------------------------
    # 7. Independent physical ground truth
    # ---------------------------------------------------------

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=decision,
        physical_state=environment.physical_state(),
    )

    evaluator = OutcomeEvaluator()

    # ---------------------------------------------------------
    # 8. Baseline B1:
    #    decision-relevance assurance
    # ---------------------------------------------------------

    relevance_policy = DivergenceAwarePolicy()

    relevance_assurance = relevance_policy.evaluate(
        decision=decision,
        relevance=relevance,
    )

    relevance_outcome = evaluator.evaluate(
        ground_truth,
        relevance_assurance,
    )

    # ---------------------------------------------------------
    # 9. Baseline B2:
    #    deterministic decision-impact assurance
    #
    # This deliberately retains the perfect-observation
    # assumption from EXP-005.
    # ---------------------------------------------------------

    deterministic_impact_assurance = (
        _deterministic_impact_assurance(
            decision=decision,
            condition=condition,
        )
    )

    deterministic_impact_outcome = evaluator.evaluate(
        ground_truth,
        deterministic_impact_assurance,
    )

    # ---------------------------------------------------------
    # 10. Generate imperfect runtime evidence
    # ---------------------------------------------------------

    generator = EvidenceGenerator()

    runtime_evidence = _build_runtime_evidence(
        condition,
        generator,
    )

    # ---------------------------------------------------------
    # 11. Proposed EXP-006 evidence-aware policy
    #
    # IMPORTANT:
    # This policy receives runtime evidence, not physical truth.
    # ---------------------------------------------------------

    evidence_policy = EvidenceAwareDecisionPolicy()

    evidence_aware_assurance = evidence_policy.evaluate(
        decision=decision,
        evidence=runtime_evidence,
        demand=condition.demand,
        current_time=condition.evaluation_timestamp,
    )

    # ---------------------------------------------------------
    # 12. Independent outcome evaluation
    # ---------------------------------------------------------

    evidence_aware_outcome = evaluator.evaluate(
        ground_truth,
        evidence_aware_assurance,
    )

    # ---------------------------------------------------------
    # 13. Return complete experimental record
    # ---------------------------------------------------------

    return EvidenceExperimentResult(
        condition=condition,
        decision_id=decision.decision_id,
        runtime_evidence=runtime_evidence,
        relevance_assurance=relevance_assurance,
        deterministic_impact_assurance=deterministic_impact_assurance,
        evidence_aware_assurance=evidence_aware_assurance,
        relevance_outcome=relevance_outcome,
        deterministic_impact_outcome=deterministic_impact_outcome,
        evidence_aware_outcome=evidence_aware_outcome,
    )


def run_evidence_experiment(
) -> tuple[EvidenceExperimentResult, ...]:
    """Run the complete deterministic EXP-006 matrix."""

    return tuple(
        run_evidence_condition(condition)
        for condition in build_evidence_conditions()
    )


def main() -> None:
    """Run EXP-006 and print condition-level results."""

    results = run_evidence_experiment()

    print(
        "condition",
        "evidence_type",
        "physical_valid",
        "relevance",
        "deterministic_impact",
        "evidence_aware",
    )

    for result in results:
        print(
            result.condition.condition_id,
            result.condition.evidence_type.value,
            result.condition.physical_valid,
            result.relevance_outcome.outcome.value,
            result.deterministic_impact_outcome.outcome.value,
            result.evidence_aware_outcome.outcome.value,
        )


if __name__ == "__main__":
    main()
