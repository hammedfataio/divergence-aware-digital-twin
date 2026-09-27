"""EXP-006: imperfect runtime evidence experiment.

This experiment evaluates runtime assurance when the evidence available
to the assurance mechanism differs from physical ground truth.

Physical state is used only for independent evaluation. Assurance
policies operate on Digital Twin state, detected divergence, decision
dependencies, or runtime evidence according to their design.
"""

from dataclasses import dataclass

from dara_dt.assurance.evidence_policy import EvidenceAwareDecisionPolicy
from dara_dt.assurance.impact_policy import DecisionImpactPolicy
from dara_dt.assurance.model import AssuranceDecision
from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.evidence.generator import EvidenceGenerator
from dara_dt.evidence.model import RuntimeEvidence
from dara_dt.evaluation.outcomes import OutcomeEvaluator, OutcomeResult
from dara_dt.evaluation.validity import PhysicalDecisionValidator
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


@dataclass(frozen=True)
class EvidenceExperimentResult:
    """Result of one EXP-006 condition."""

    condition: EvidenceCondition
    decision_id: str
    runtime_evidence: tuple[RuntimeEvidence, ...]
    deterministic_impact_assurance: AssuranceDecision
    evidence_aware_assurance: AssuranceDecision
    deterministic_impact_outcome: OutcomeResult
    evidence_aware_outcome: OutcomeResult


def _build_runtime_evidence(
    condition: EvidenceCondition,
    generator: EvidenceGenerator,
) -> tuple[RuntimeEvidence, ...]:
    """Generate the runtime evidence specified by a condition."""

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
            raise ValueError("Noisy condition requires an observed capacity.")

        return (
            generator.noisy(
                **common,
                physical_value=condition.physical_capacity,
                error=(
                    condition.observed_capacity
                    - condition.physical_capacity
                ),
                timestamp=condition.observation_timestamp,
                confidence=condition.confidence,
            ),
        )

    if condition.evidence_type == EvidenceConditionType.STALE:
        if condition.observed_capacity is None:
            raise ValueError("Stale condition requires an observed capacity.")

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
        if (
            condition.observed_capacity is None
            or condition.secondary_observed_capacity is None
        ):
            raise ValueError(
                "Conflicting condition requires two observations."
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
    )
    environment.add_order(order)

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    # Physical reality changes after the Twin has been synchronised.
    vehicle.capacity = condition.physical_capacity

    controller = LogisticsDecisionController()
    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_001",
        timestamp=condition.evaluation_timestamp,
        decision_id=f"decision_{condition.condition_id}",
    )

    validator = PhysicalDecisionValidator()
    ground_truth = validator.ground_truth(
        decision=decision,
        physical_state=environment.physical_state(),
    )

    generator = EvidenceGenerator()
    runtime_evidence = _build_runtime_evidence(
        condition,
        generator,
    )

    # EXP-005-style deterministic impact policy:
    # it trusts the primary observed value when one exists.
    impact_analyser = DecisionImpactAnalyser()

    if (
        condition.observed_capacity is None
        or condition.evidence_type
        in {
            EvidenceConditionType.MISSING,
            EvidenceConditionType.CONFLICTING,
        }
    ):
        impact = impact_analyser.uncertain(
            decision_id=decision.decision_id,
            dependency="vehicle.capacity",
            reason="Runtime capacity evidence is unavailable or ambiguous.",
        )
    else:
        impact = impact_analyser.analyse_capacity(
            decision_id=decision.decision_id,
            twin_capacity=condition.twin_capacity,
            observed_capacity=condition.observed_capacity,
            demand=condition.demand,
            evidence=ImpactEvidence(
                source="runtime_capacity_monitor",
                observed_value=condition.observed_capacity,
            ),
        )

    deterministic_assurance = DecisionImpactPolicy().evaluate(
        decision=decision,
        impact=impact,
    )

    evidence_assurance = EvidenceAwareDecisionPolicy().evaluate(
        decision=decision,
        evidence=runtime_evidence,
        demand=condition.demand,
        current_time=condition.evaluation_timestamp,
    )

    evaluator = OutcomeEvaluator()

    deterministic_outcome = evaluator.evaluate(
        ground_truth=ground_truth,
        assurance=deterministic_assurance,
    )

    evidence_outcome = evaluator.evaluate(
        ground_truth=ground_truth,
        assurance=evidence_assurance,
    )

    return EvidenceExperimentResult(
        condition=condition,
        decision_id=decision.decision_id,
        runtime_evidence=runtime_evidence,
        deterministic_impact_assurance=deterministic_assurance,
        evidence_aware_assurance=evidence_assurance,
        deterministic_impact_outcome=deterministic_outcome,
        evidence_aware_outcome=evidence_outcome,
    )


def run_evidence_experiment() -> tuple[EvidenceExperimentResult, ...]:
    """Run the complete deterministic EXP-006 matrix."""

    return tuple(
        run_evidence_condition(condition)
        for condition in build_evidence_conditions()
    )


def main() -> None:
    """Run EXP-006 and print condition-level outcomes."""

    results = run_evidence_experiment()

    for result in results:
        print(
            result.condition.condition_id,
            result.condition.evidence_type.value,
            f"physical_valid={result.condition.physical_valid}",
            (
                "deterministic="
                f"{result.deterministic_impact_outcome.outcome.value}"
            ),
            (
                "evidence_aware="
                f"{result.evidence_aware_outcome.outcome.value}"
            ),
        )


if __name__ == "__main__":
    main()
