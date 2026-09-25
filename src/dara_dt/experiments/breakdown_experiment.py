"""End-to-end stale Digital Twin breakdown experiment for DARA-DT."""

from dataclasses import dataclass

from dara_dt.assurance.model import AssuranceDecision
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence, DivergenceDetector
from dara_dt.divergence.relevance import (
    DecisionRelevanceAnalyzer,
    RelevanceResult,
)
from dara_dt.evaluation.outcomes import (
    OutcomeEvaluator,
    OutcomeResult,
)
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.experiments.ground_truth import GroundTruth
from dara_dt.experiments.stale_twin import (
    StaleTwinEvent,
    StaleTwinScenario,
)
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class BreakdownExperimentResult:
    """Complete result from the stale-Twin breakdown experiment."""

    decision: Decision
    event: StaleTwinEvent
    divergences: tuple[Divergence, ...]
    relevance: RelevanceResult
    assurance: AssuranceDecision
    ground_truth: GroundTruth
    outcome: OutcomeResult


def run_breakdown_experiment() -> BreakdownExperimentResult:
    """Run an end-to-end stale Digital Twin safety experiment."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_07",
            capacity=10.0,
        )
    )

    environment.add_order(
        Order(
            order_id="order_42",
            location="node_20",
            demand=5.0,
            deadline=200.0,
        )
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    scenario = StaleTwinScenario()

    event = scenario.vehicle_breakdown(
        environment=environment,
        twin=twin,
        vehicle_id="vehicle_07",
    )

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_42",
        timestamp=environment.time,
        decision_id="decision_001",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    relevance_analyzer = DecisionRelevanceAnalyzer(
        DependencyMapper()
    )

    relevance = relevance_analyzer.analyse(
        decision,
        divergences,
    )

    policy = DivergenceAwarePolicy()

    assurance = policy.evaluate(
        decision,
        relevance,
    )

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision,
        environment.physical_state(),
    )

    outcome = OutcomeEvaluator().evaluate(
        assurance,
        ground_truth,
    )

    return BreakdownExperimentResult(
        decision=decision,
        event=event,
        divergences=tuple(divergences),
        relevance=relevance,
        assurance=assurance,
        ground_truth=ground_truth,
        outcome=outcome,
    )
