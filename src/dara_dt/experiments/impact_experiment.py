"""EXP-005 decision-impact-aware runtime assurance experiment.

This experiment compares five assurance strategies across controlled
capacity-divergence conditions with changing decision boundaries:

B0 - No assurance
B1 - Global divergence assurance
B2 - Fixed magnitude assurance
B3 - Decision-relevance assurance
P1 - Decision-impact-aware assurance

Runtime decision-impact evidence is kept conceptually separate from
experimental ground-truth validation.
"""

from dataclasses import dataclass

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.impact_policy import DecisionImpactPolicy
from dara_dt.assurance.magnitude_policy import MagnitudeAssurancePolicy
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.relevance import DecisionRelevanceAnalyzer
from dara_dt.evaluation.outcomes import OutcomeEvaluator, OutcomeResult
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.experiments.impact_conditions import (
    ImpactCondition,
    build_impact_conditions,
)
from dara_dt.impact.analyser import DecisionImpactAnalyser
from dara_dt.impact.model import ImpactEvidence
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class ImpactExperimentResult:
    """Results for one EXP-005 controlled condition."""

    condition: ImpactCondition
    divergence_count: int
    relevant_divergence_count: int
    estimated_margin: float
    impact_state: str
    no_assurance: OutcomeResult
    global_divergence: OutcomeResult
    fixed_magnitude: OutcomeResult
    decision_relevance: OutcomeResult
    decision_impact: OutcomeResult


def _build_environment(
    condition: ImpactCondition,
) -> tuple[LogisticsEnvironment, DigitalTwin]:
    """Create physical and digital states for one condition."""

    environment = LogisticsEnvironment()

    vehicle = Vehicle(
        vehicle_id="vehicle_001",
        capacity=condition.twin_capacity,
        location="depot",
        operational=True,
        available=True,
    )

    order = Order(
        order_id="order_001",
        demand=condition.order_demand,
        location="customer_001",
        deadline=10.0,
    )

    environment.add_vehicle(vehicle)
    environment.add_order(order)

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    # The physical system changes after Digital Twin synchronisation.
    environment.vehicles["vehicle_001"].capacity = (
        condition.physical_capacity
    )

    return environment, twin


def run_impact_condition(
    condition: ImpactCondition,
) -> ImpactExperimentResult:
    """Run one controlled EXP-005 condition."""

    environment, twin = _build_environment(condition)

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_001",
        timestamp=environment.time,
        decision_id=f"decision_{condition.name}",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        physical_state=environment.physical_state(),
        twin_state=twin.state,
    )

    relevance = DecisionRelevanceAnalyzer(
        DependencyMapper()
    ).analyse(
        decision=decision,
        divergences=divergences,
    )

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=decision,
        physical_state=environment.physical_state(),
    )

    # Runtime observation used by the impact analyser.
    #
    # In this controlled experiment the observation is assumed to be
    # perfectly measured. It is intentionally represented separately
    # from the evaluator's ground-truth validity result. Later
    # experiments can introduce noisy, delayed, or incomplete evidence.
    evidence = ImpactEvidence(
        source="runtime_capacity_monitor",
        variable="vehicle.capacity",
        observed_value=condition.physical_capacity,
        twin_value=condition.twin_capacity,
    )

    impact = DecisionImpactAnalyser().analyse_capacity(
        decision_id=decision.decision_id,
        dependency="vehicle.capacity",
        required_demand=condition.order_demand,
        evidence=evidence,
    )

    no_assurance_decision = NoAssurancePolicy().evaluate(
        decision,
        divergences,
    )

    global_decision = AnyDivergencePolicy().evaluate(
        decision,
        divergences,
    )

    magnitude_decision = MagnitudeAssurancePolicy(
        threshold=5.0
    ).decide(
        decision,
        divergences,
    )

    relevance_decision = DivergenceAwarePolicy().evaluate(
        decision,
        relevance,
    )

    impact_decision = DecisionImpactPolicy().evaluate(
        decision,
        impact,
    )

    evaluator = OutcomeEvaluator()

    return ImpactExperimentResult(
        condition=condition,
        divergence_count=len(divergences),
        relevant_divergence_count=len(relevance.relevant),
        estimated_margin=(
            impact.estimated_margin
            if impact.estimated_margin is not None
            else float("nan")
        ),
        impact_state=impact.impact_state.value,
        no_assurance=evaluator.evaluate(
            ground_truth,
            no_assurance_decision,
        ),
        global_divergence=evaluator.evaluate(
            ground_truth,
            global_decision,
        ),
        fixed_magnitude=evaluator.evaluate(
            ground_truth,
            magnitude_decision,
        ),
        decision_relevance=evaluator.evaluate(
            ground_truth,
            relevance_decision,
        ),
        decision_impact=evaluator.evaluate(
            ground_truth,
            impact_decision,
        ),
    )


def run_impact_experiment() -> tuple[ImpactExperimentResult, ...]:
    """Run the complete EXP-005 controlled experiment."""

    return tuple(
        run_impact_condition(condition)
        for condition in build_impact_conditions()
    )


if __name__ == "__main__":
    for result in run_impact_experiment():
        print(
            result.condition.name,
            {
                "divergence": result.condition.divergence_magnitude,
                "physical_margin": result.condition.physical_margin,
                "physically_valid": result.condition.physically_valid,
                "impact_state": result.impact_state,
                "no_assurance": result.no_assurance.outcome.value,
                "global": result.global_divergence.outcome.value,
                "magnitude": result.fixed_magnitude.outcome.value,
                "relevance": result.decision_relevance.outcome.value,
                "impact": result.decision_impact.outcome.value,
            },
        )
