"""Controlled divergence-count experiment for DARA-DT."""

from dataclasses import dataclass

from dara_dt.decision.controller import LogisticsDecisionController
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.relevance import DecisionRelevanceAnalyzer
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class DivergenceCountResult:
    """Observed divergence and relevance counts."""

    injected_count: int
    detected_count: int
    relevant_count: int
    selected_vehicle_id: str


def run_irrelevant_divergence_count(
    divergence_count: int,
) -> DivergenceCountResult:
    """Create N decision-irrelevant divergences."""

    if divergence_count < 1:
        raise ValueError(
            "divergence_count must be at least 1"
        )

    environment = LogisticsEnvironment()

    # vehicle_00 is deliberately the only vehicle capable
    # of serving the order.
    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_00",
            location="node_00",
            capacity=10.0,
        )
    )

    # Add unrelated vehicles that cannot serve the order.
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
        decision_id="divergence_count_decision",
    )

    # Introduce exactly one location mismatch on each
    # unrelated vehicle.
    for index in range(1, divergence_count + 1):
        twin.update_vehicle(
            f"vehicle_{index:02d}",
            location=f"divergent_node_{index:02d}",
        )

    detector = DivergenceDetector()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    relevance = DecisionRelevanceAnalyzer(
        DependencyMapper()
    ).analyse(
        decision,
        divergences,
    )

    return DivergenceCountResult(
        injected_count=divergence_count,
        detected_count=len(divergences),
        relevant_count=len(relevance.relevant),
        selected_vehicle_id=decision.vehicle_id,
    )
