"""Tests for the DARA-DT runtime assurance policy."""

from dara_dt.assurance.model import AuthorityState
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.relevance import DecisionRelevanceAnalyzer
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


def create_system():
    """Create a synchronised physical system and Digital Twin."""
    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_14",
            capacity=40,
        )
    )

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_03",
            location="node_09",
            capacity=30,
        )
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    return environment, twin


def create_decision() -> Decision:
    """Create a decision involving vehicle_07."""
    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=125.0,
    )


def evaluate(environment, twin, decision):
    """Run the divergence-to-assurance pipeline."""
    detector = DivergenceDetector()
    mapper = DependencyMapper()
    analyzer = DecisionRelevanceAnalyzer(mapper)
    policy = DivergenceAwarePolicy()

    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    relevance = analyzer.analyse(
        decision,
        divergences,
    )

    return policy.evaluate(
        decision,
        relevance,
    )


def test_synchronised_system_allows_autonomous_decision():
    environment, twin = create_system()
    decision = create_decision()

    result = evaluate(environment, twin, decision)

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True
    assert result.relevant_divergence_count == 0


def test_irrelevant_divergence_still_allows_decision():
    environment, twin = create_system()
    decision = create_decision()

    environment.get_vehicle("vehicle_03").mark_broken_down()

    result = evaluate(environment, twin, decision)

    assert result.authority == AuthorityState.ALLOW
    assert result.autonomous_execution_allowed is True
    assert result.relevant_divergence_count == 0


def test_relevant_divergence_defers_decision():
    environment, twin = create_system()
    decision = create_decision()

    environment.get_vehicle("vehicle_07").mark_broken_down()

    result = evaluate(environment, twin, decision)

    assert result.authority == AuthorityState.DEFER
    assert result.autonomous_execution_allowed is False
    assert result.relevant_divergence_count == 2
