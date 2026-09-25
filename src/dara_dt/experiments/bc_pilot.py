"""Controlled B-vs-C pilot experiment for DARA-DT."""

from dataclasses import dataclass

from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.divergence.detector import DivergenceDetector
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
    """Create the common physical logistics environment."""

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
    """Run Condition B: divergence exists but is decision-irrelevant."""

    environment = _build_environment()

    # Make vehicle_07 the only vehicle capable of serving the order.
    #
    # This is important because the controller deterministically selects
    # an eligible vehicle. By reducing the capacities of vehicle_03 and
    # vehicle_04 before synchronisation, vehicle_07 becomes the selected
    # vehicle for the decision.
    environment.get_vehicle("vehicle_03").capacity = 1.0
    environment.get_vehicle("vehicle_04").capacity = 1.0

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    controller = LogisticsDecisionController()

    decision = controller.assign_vehicle(
        twin=twin,
        order_id="order_42",
        timestamp=environment.time,
        decision_id="decision_b",
    )

    # Introduce divergence only on vehicles that are NOT used by
    # the current decision.
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

    # Ground truth is derived independently from the physical state.
    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision,
        environment.physical_state(),
    )

    policy_results = compare_policies(
        decision,
        divergences,
        ground_truth,
    )

    return PilotConditionResult(
        condition="B_HIGH_DIVERGENCE_LOW_RELEVANCE",
        divergence_count=len(divergences),
        policy_results=policy_results,
    )


def _run_condition_c() -> PilotConditionResult:
    """Run Condition C: divergence directly affects the decision."""

    environment = _build_environment()

    # Again make vehicle_07 the only vehicle capable of serving
    # the order.
    environment.get_vehicle("vehicle_03").capacity = 1.0
    environment.get_vehicle("vehicle_04").capacity = 1.0

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    # The physical vehicle breaks down AFTER Twin synchronisation.
    #
    # Physical reality:
    #     vehicle_07 = broken_down / unavailable
    #
    # Digital Twin:
    #     vehicle_07 = operational / available
    #
    # The Twin is therefore stale.
    environment.get_vehicle("vehicle_07").mark_broken_down()

    controller = LogisticsDecisionController()

    # The controller reads the stale Digital Twin rather than the
    # physical system, so it still believes vehicle_07 is usable.
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

    # Ground truth comes from physical reality, independently of
    # the assurance mechanism.
    validator = PhysicalDecisionValidator()

    ground_truth = validator.ground_truth(
        decision,
        environment.physical_state(),
    )

    policy_results = compare_policies(
        decision,
        divergences,
        ground_truth,
    )

    return PilotConditionResult(
        condition="C_LOW_DIVERGENCE_HIGH_RELEVANCE",
        divergence_count=len(divergences),
        policy_results=policy_results,
    )


def run_bc_pilot() -> BCPilotResult:
    """Run both controlled B-vs-C pilot conditions."""

    return BCPilotResult(
        condition_b=_run_condition_b(),
        condition_c=_run_condition_c(),
    )
