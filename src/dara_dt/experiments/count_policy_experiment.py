"""Policy comparison across irrelevant divergence counts."""

from dataclasses import dataclass

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.relevance import DecisionRelevanceAnalyzer
from dara_dt.evaluation.outcomes import (
    AssuranceOutcome,
    OutcomeEvaluator,
)
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class CountPolicyResult:
    """Policy outcomes for one irrelevant-divergence count."""

    divergence_count: int
    relevant_count: int
    no_assurance: AssuranceOutcome
    global_divergence: AssuranceOutcome
    dara_dt: AssuranceOutcome


def run_count_policy_experiment(
    divergence_count: int,
) -> CountPolicyResult:
    """Compare assurance policies under irrelevant divergence."""

    if divergence_count < 1:
        raise ValueError(
            "divergence_count must be at least 1"
        )

    environment = LogisticsEnvironment()

    # Selected vehicle.
    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_00",
            location="node_00",
            capacity=10.0,
        )
    )

    # Vehicles that cannot serve the order and are therefore
    # unrelated to the selected decision.
    for index in range(1, divergence_count + 1):
        environment.add_vehicle(
            Vehicle(
                vehicle_id=f"vehicle_{index:02d}",
                location=f"node_{index:02d}",
                capacity=1.0,
            )
        )

    environment.add_order(
        Order(
            order_id="order_01",
            location="customer_01",
            demand=5.0,
            deadline=200.0,
        )
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_01",
        timestamp=environment.time,
        decision_id="count_policy_decision",
    )

    # Inject one irrelevant location mismatch per unrelated vehicle.
    for index in range(1, divergence_count + 1):
        twin.update_vehicle(
            f"vehicle_{index:02d}",
            location=f"divergent_node_{index:02d}",
        )

    divergences = DivergenceDetector().detect(
        environment.physical_state(),
        twin.state,
    )

    relevance = DecisionRelevanceAnalyzer(
        DependencyMapper()
    ).analyse(
        decision,
        divergences,
    )

    # Independent physical-state ground truth.
    ground_truth = PhysicalDecisionValidator().ground_truth(
        decision,
        environment.physical_state(),
    )

    no_assurance_decision = NoAssurancePolicy().evaluate(
        decision,
        divergences,
    )

    global_decision = AnyDivergencePolicy().evaluate(
        decision,
        divergences,
    )

    dara_decision = DivergenceAwarePolicy().evaluate(
        decision,
        relevance,
    )

    evaluator = OutcomeEvaluator()

    no_assurance_outcome = evaluator.evaluate(
        ground_truth,
        no_assurance_decision,
    )

    global_outcome = evaluator.evaluate(
        ground_truth,
        global_decision,
    )

    dara_outcome = evaluator.evaluate(
        ground_truth,
        dara_decision,
    )

    return CountPolicyResult(
        divergence_count=len(divergences),
        relevant_count=len(relevance.relevant),
        no_assurance=no_assurance_outcome.outcome,
        global_divergence=global_outcome.outcome,
        dara_dt=dara_outcome.outcome,
    )
