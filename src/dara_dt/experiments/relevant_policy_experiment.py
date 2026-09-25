"""Policy comparison under decision-relevant divergence."""

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
class RelevantPolicyResult:
    """Policy outcomes under decision-relevant divergence."""

    divergence_count: int
    relevant_count: int
    selected_vehicle_id: str
    no_assurance: AssuranceOutcome
    global_divergence: AssuranceOutcome
    dara_dt: AssuranceOutcome


def run_relevant_policy_experiment() -> RelevantPolicyResult:
    """Compare policies when stale Twin state invalidates a decision."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_00",
            location="node_00",
            capacity=10.0,
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

    # Physical reality changes after Twin synchronisation.
    # The Twin therefore remains stale.
    environment.get_vehicle(
        "vehicle_00"
    ).mark_broken_down()

    controller = LogisticsDecisionController()

    # The controller still sees the stale Digital Twin and
    # therefore selects the broken vehicle.
    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_01",
        timestamp=environment.time,
        decision_id="relevant_policy_decision",
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

    # Ground truth is determined independently from physical reality.
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

    return RelevantPolicyResult(
        divergence_count=len(divergences),
        relevant_count=len(relevance.relevant),
        selected_vehicle_id=decision.vehicle_id,
        no_assurance=no_assurance_outcome.outcome,
        global_divergence=global_outcome.outcome,
        dara_dt=dara_outcome.outcome,
    )
