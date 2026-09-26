"""EXP-004 divergence-severity experiment.

This module evaluates how increasing physical-digital capacity divergence
affects decision validity and runtime assurance behaviour.

The experiment preserves independent physical ground truth and compares:

1. No assurance
2. Global-divergence assurance
3. Magnitude-threshold assurance
4. DARA-DT decision-relevance assurance

The experiment is deliberately diagnostic. It does not assume that DARA-DT
will outperform the baselines.
"""

from dataclasses import dataclass

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.magnitude_policy import MagnitudeAssurancePolicy
from dara_dt.assurance.policy import DARADTPolicy
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
    """Result for one EXP-004 severity condition."""

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
    """Create the synchronized baseline logistics environment."""

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
            status="waiting",
        )
    )

    return environment


def run_severity_condition(
    condition: SeverityCondition,
    magnitude_threshold: float = 5.0,
) -> SeverityExperimentResult:
    """Execute one controlled EXP-004 severity condition."""

    environment = _build_environment()

    twin = DigitalTwin()
    twin.synchronize(environment.snapshot())

    # Divergence is introduced after synchronization so that the Twin
    # retains the original capacity while the physical system changes.
    environment.vehicles["vehicle_00"].capacity = condition.physical_capacity

    physical_state = environment.snapshot()

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_00",
        timestamp=1.0,
        decision_id=f"decision_{condition.name.lower()}",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        physical_state=physical_state,
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
        physical_state=physical_state,
    )

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

    dara_decision = DARADTPolicy().decide(
        decision=decision,
        relevance=relevance,
    )

    evaluator = OutcomeEvaluator()

    return SeverityExperimentResult(
        condition=condition.name,
        divergence_magnitude=condition.divergence_magnitude,
        physically_valid=condition.physically_valid,
        divergence_count=len(divergences),
        relevant_count=len(relevance.relevant),
        no_assurance=evaluator.evaluate(
            ground_truth,
            no_assurance_decision,
        ),
        global_divergence=evaluator.evaluate(
            ground_truth,
            global_divergence_decision,
        ),
        magnitude_threshold=evaluator.evaluate(
            ground_truth,
            magnitude_decision,
        ),
        dara_dt=evaluator.evaluate(
            ground_truth,
            dara_decision,
        ),
    )


def run_severity_experiment(
    magnitude_threshold: float = 5.0,
) -> tuple[SeverityExperimentResult, ...]:
    """Execute all predefined EXP-004 severity conditions."""

    return tuple(
        run_severity_condition(
            condition=condition,
            magnitude_threshold=magnitude_threshold,
        )
        for condition in build_severity_conditions()
    )
