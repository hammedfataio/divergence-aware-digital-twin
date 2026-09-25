"""Controlled decision-relevant divergence scenarios."""

from dataclasses import dataclass

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.relevance import RelevanceAnalyzer
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
class RelevantScenarioResult:
    """Result from one decision-relevant divergence scenario."""

    scenario: str
    divergence_count: int
    relevant_count: int
    no_assurance: AssuranceOutcome
    global_divergence: AssuranceOutcome
    dara_dt: AssuranceOutcome


def _evaluate(
    scenario: str,
    environment: LogisticsEnvironment,
    twin: DigitalTwin,
) -> RelevantScenarioResult:
    """Evaluate one prepared physical/Twin state."""

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_00",
        timestamp=environment.time,
        decision_id=f"{scenario}_decision",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        physical_state=environment.physical_state(),
        twin_state=twin.state,
    )

    relevance = RelevanceAnalyzer().analyse(
        decision=decision,
        divergences=divergences,
    )

    ground_truth = PhysicalDecisionValidator().evaluate(
        decision=decision,
        physical_state=environment.physical_state(),
    )

    no_assurance = NoAssurancePolicy().evaluate(
        decision=decision,
        divergences=divergences,
    )

    global_assurance = AnyDivergencePolicy().evaluate(
        decision=decision,
        divergences=divergences,
    )

    dara_assurance = DivergenceAwarePolicy().evaluate(
        decision=decision,
        relevance=relevance,
    )

    evaluator = OutcomeEvaluator()

    return RelevantScenarioResult(
        scenario=scenario,
        divergence_count=len(divergences),
        relevant_count=len(relevance.relevant),
        no_assurance=evaluator.evaluate(
            ground_truth,
            no_assurance,
        ).outcome,
        global_divergence=evaluator.evaluate(
            ground_truth,
            global_assurance,
        ).outcome,
        dara_dt=evaluator.evaluate(
            ground_truth,
            dara_assurance,
        ).outcome,
    )


def _base_environment() -> tuple[
    LogisticsEnvironment,
    DigitalTwin,
]:
    """Create a synchronized baseline logistics state."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_00",
            location="depot",
            capacity=10,
        )
    )

    environment.add_order(
        Order(
            order_id="order_00",
            location="customer",
            demand=5,
            deadline=100,
        )
    )

    twin = DigitalTwin()

    twin.synchronise(
        environment.physical_state()
    )

    return environment, twin


def run_status_divergence() -> RelevantScenarioResult:
    """Physical vehicle breaks down after Twin synchronization."""

    environment, twin = _base_environment()

    environment.get_vehicle(
        "vehicle_00"
    ).mark_broken_down()

    return _evaluate(
        "relevant_vehicle_status",
        environment,
        twin,
    )


def run_capacity_divergence() -> RelevantScenarioResult:
    """Physical capacity becomes insufficient while Twin stays stale."""

    environment, twin = _base_environment()

    environment.get_vehicle(
        "vehicle_00"
    ).capacity = 2

    return _evaluate(
        "relevant_vehicle_capacity",
        environment,
        twin,
    )


def run_availability_divergence() -> RelevantScenarioResult:
    """Physical vehicle becomes unavailable while Twin stays stale."""

    environment, twin = _base_environment()

    environment.get_vehicle(
        "vehicle_00"
    ).available = False

    return _evaluate(
        "relevant_vehicle_availability",
        environment,
        twin,
    )


def run_all_relevant_scenarios() -> tuple[
    RelevantScenarioResult,
    ...,
]:
    """Execute all current decision-relevant scenarios."""

    return (
        run_status_divergence(),
        run_capacity_divergence(),
        run_availability_divergence(),
    )
