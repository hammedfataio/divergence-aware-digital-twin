"""EXP-004: Divergence severity experiment.

This experiment investigates how the magnitude of a decision-relevant
physical-digital divergence affects the validity of an AI-generated
logistics decision and the behaviour of different runtime assurance
policies.

The experiment compares:

1. No assurance
2. Global-divergence assurance
3. Magnitude-threshold assurance
4. DARA-DT decision-relevance assurance

Ground truth is determined independently from the assurance policies
using the physical logistics state.
"""

from dataclasses import dataclass

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.magnitude_policy import MagnitudeAssurancePolicy
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
from dara_dt.experiments.severity_conditions import (
    SeverityCondition,
    build_severity_conditions,
)
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class SeverityExperimentResult:
    """Result produced by one EXP-004 severity condition."""

    condition: str
    divergence_magnitude: int
    physically_valid: bool
    divergence_count: int
    relevant_count: int
    no_assurance: AssuranceOutcome
    global_divergence: AssuranceOutcome
    magnitude_threshold: AssuranceOutcome
    dara_dt: AssuranceOutcome


def _build_environment() -> LogisticsEnvironment:
    """Create the baseline physical logistics environment."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_00",
            location="depot",
            capacity=10,
            available=True,
            status="operational",
        )
    )

    environment.add_order(
        Order(
            order_id="order_00",
            location="customer",
            demand=5,
            deadline=100,
            status="waiting",
        )
    )

    return environment


def run_severity_condition(
    condition: SeverityCondition,
    magnitude_threshold: float = 5.0,
) -> SeverityExperimentResult:
    """Run one controlled divergence-severity condition."""

    # ---------------------------------------------------------
    # 1. Create synchronized physical system and Digital Twin
    # ---------------------------------------------------------

    environment = _build_environment()

    twin = DigitalTwin()

    twin.synchronise(
        environment.physical_state()
    )

    # ---------------------------------------------------------
    # 2. Introduce controlled physical-digital divergence
    # ---------------------------------------------------------
    #
    # The Digital Twin remains at capacity 10.
    # Only the physical vehicle capacity changes.
    #
    # This preserves the stale-Twin condition required by
    # the experiment.

    environment.vehicles["vehicle_00"].capacity = (
        condition.physical_capacity
    )

    physical_state = environment.physical_state()

    # ---------------------------------------------------------
    # 3. Generate AI decision from the stale Digital Twin
    # ---------------------------------------------------------

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_00",
        timestamp=environment.time,
        decision_id=f"{condition.name}_decision",
    )

    # ---------------------------------------------------------
    # 4. Detect physical-digital divergence
    # ---------------------------------------------------------

    detector = DivergenceDetector()

    divergences = detector.detect(
        physical_state=physical_state,
        twin_state=twin.state,
    )

    # ---------------------------------------------------------
    # 5. Determine decision relevance
    # ---------------------------------------------------------

    relevance_analyzer = DecisionRelevanceAnalyzer(
        DependencyMapper()
    )

    relevance = relevance_analyzer.analyse(
        decision=decision,
        divergences=divergences,
    )

    # ---------------------------------------------------------
    # 6. Establish independent physical ground truth
    # ---------------------------------------------------------

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision=decision,
        physical_state=physical_state,
    )

    # ---------------------------------------------------------
    # 7. Evaluate assurance strategies
    # ---------------------------------------------------------

    no_assurance_decision = NoAssurancePolicy().decide(
        decision=decision,
        divergences=divergences,
    )

    global_divergence_decision = AnyDivergencePolicy().decide(
        decision=decision,
        divergences=divergences,
    )

    magnitude_decision = MagnitudeAssurancePolicy(
        threshold=magnitude_threshold
    ).decide(
        decision=decision,
        divergences=divergences,
    )

    dara_decision = DivergenceAwarePolicy().evaluate(
        decision=decision,
        relevance=relevance,
    )

    # ---------------------------------------------------------
    # 8. Compare assurance behaviour with ground truth
    # ---------------------------------------------------------

    evaluator = OutcomeEvaluator()

    no_assurance_outcome = evaluator.evaluate(
        ground_truth,
        no_assurance_decision,
    )

    global_divergence_outcome = evaluator.evaluate(
        ground_truth,
        global_divergence_decision,
    )

    magnitude_outcome = evaluator.evaluate(
        ground_truth,
        magnitude_decision,
    )

    dara_outcome = evaluator.evaluate(
        ground_truth,
        dara_decision,
    )

    # ---------------------------------------------------------
    # 9. Return experimental result
    # ---------------------------------------------------------

    return SeverityExperimentResult(
        condition=condition.name,
        divergence_magnitude=condition.divergence_magnitude,
        physically_valid=condition.physically_valid,
        divergence_count=len(divergences),
        relevant_count=len(relevance.relevant),
        no_assurance=no_assurance_outcome,
        global_divergence=global_divergence_outcome,
        magnitude_threshold=magnitude_outcome,
        dara_dt=dara_outcome,
    )


def run_severity_experiment(
    magnitude_threshold: float = 5.0,
) -> tuple[SeverityExperimentResult, ...]:
    """Run the complete S0-S6 EXP-004 severity experiment."""

    conditions = build_severity_conditions()

    return tuple(
        run_severity_condition(
            condition=condition,
            magnitude_threshold=magnitude_threshold,
        )
        for condition in conditions
    )
