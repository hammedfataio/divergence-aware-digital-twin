"""Controlled B-vs-C pilot experiment for DARA-DT."""

from dataclasses import dataclass

from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.evaluation.outcomes import OutcomeResult
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.experiments.policy_comparison import (
    PolicyComparisonResult,
    compare_policies,
)
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class PilotConditionResult:
    """Result from one controlled B-vs-C condition."""

    condition: str
    divergence_count: int
    policy_results: PolicyComparisonResult


@dataclass(frozen=True)
class BCPilotResult:
    """Complete result from the B-vs-C pilot."""

    condition_b: PilotConditionResult
    condition_c: PilotConditionResult


def _build_environment() -> LogisticsEnvironment:
    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_07",
            capacity=10.0,
        )
    )

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_03",
            location="node_03",
            capacity=10.0,
        )
    )

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_04",
            location="node_04",
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

    return environment


def _run_condition_b() -> PilotConditionResult:
    """High divergence, low decision relevance."""

    environment = _build_environment()

    # Ensure vehicle_07 is the only vehicle capable of serving
    # the order. Divergence can then be introduced on unrelated
    # vehicles without affecting the selected decision.
    environment.get_vehicle("vehicle_03").capacity = 1.0
    environment.get_vehicle("vehicle_04").capacity = 1.0

    twin = DigitalTwin()

    # Create multiple mismatches on vehicles unrelated to the decision.
    twin.update_vehicle(
        "vehicle_03",
        location="node_99",
    )

    twin.update_vehicle(
        "vehicle_04",
        status="broken_down",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision,
        environment.physical_state(),
    )

    results = compare_policies(
        decision,
        divergences,
        ground_truth,
    )

    return PilotConditionResult(
        condition="B_HIGH_DIVERGENCE_LOW_RELEVANCE",
        divergence_count=len(divergences),
        policy_results=results,
    )


def _run_condition_c() -> PilotConditionResult:
    """Low divergence, high decision relevance."""

    environment = _build_environment()

    # Force the controller to select vehicle_07.
    environment.get_vehicle("vehicle_03").capacity = 1.0
    environment.get_vehicle("vehicle_04").capacity = 1.0

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    # Physical breakdown occurs after synchronisation.
    # The Digital Twin therefore becomes stale.
    environment.get_vehicle("vehicle_07").mark_broken_down()

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_42",
        timestamp=environment.time,
        decision_id="decision_c",
    )

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision,
        environment.physical_state(),
    )

    results = compare_policies(
        decision,
        divergences,
        ground_truth,
    )

    return PilotConditionResult(
        condition="C_LOW_DIVERGENCE_HIGH_RELEVANCE",
        divergence_count=len(divergences),
        policy_results=results,
    )


def run_bc_pilot() -> BCPilotResult:
    """Run the controlled B-vs-C pilot experiment."""

    return BCPilotResult(
        condition_b=_run_condition_b(),
        condition_c=_run_condition_c(),
    )
