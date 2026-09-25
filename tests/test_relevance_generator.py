"""Tests for controlled decision-relevance condition generation."""

import pytest

from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import DivergenceDetector
from dara_dt.divergence.injector import DivergenceInjector
from dara_dt.divergence.relevance import DecisionRelevanceAnalyzer
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.experiments.relevance_conditions import RelevanceCondition
from dara_dt.experiments.relevance_generator import (
    RelevanceConditionGenerator,
)
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle
from dara_dt.twin.digital_twin import DigitalTwin


def create_experiment():
    """Create a reproducible environment for B/C testing."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle("vehicle_01", "node_01", 10.0)
    )
    environment.add_vehicle(
        Vehicle("vehicle_02", "node_02", 10.0)
    )
    environment.add_vehicle(
        Vehicle("vehicle_07", "node_07", 10.0)
    )

    environment.add_order(
        Order("order_42", "node_20", 5.0, 200.0)
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    decision = Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=125.0,
    )

    return environment, twin, decision


def analyse_condition(environment, twin, decision):
    """Detect divergence and analyse decision relevance."""

    detector = DivergenceDetector()
    divergences = detector.detect(
        environment.physical_state(),
        twin.state,
    )

    analyzer = DecisionRelevanceAnalyzer(
        DependencyMapper()
    )

    relevance = analyzer.analyse(
        decision,
        divergences,
    )

    return divergences, relevance


def test_condition_b_has_high_but_irrelevant_divergence():
    environment, twin, decision = create_experiment()

    generator = RelevanceConditionGenerator(
        DivergenceInjector()
    )

    generator.apply(
        RelevanceCondition.B_HIGH_DIVERGENCE_LOW_RELEVANCE,
        twin,
        decision,
    )

    divergences, relevance = analyse_condition(
        environment,
        twin,
        decision,
    )

    assert len(divergences) == 2
    assert len(relevance.relevant) == 0
    assert len(relevance.irrelevant) == 2
    assert relevance.has_relevant_divergence is False


def test_condition_c_has_low_but_relevant_divergence():
    environment, twin, decision = create_experiment()

    generator = RelevanceConditionGenerator(
        DivergenceInjector()
    )

    generator.apply(
        RelevanceCondition.C_LOW_DIVERGENCE_HIGH_RELEVANCE,
        twin,
        decision,
    )

    divergences, relevance = analyse_condition(
        environment,
        twin,
        decision,
    )

    assert len(divergences) == 1
    assert len(relevance.relevant) == 1
    assert len(relevance.irrelevant) == 0
    assert relevance.has_relevant_divergence is True


def test_condition_b_requires_unrelated_vehicles():
    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle("vehicle_07", "node_07", 10.0)
    )

    environment.add_order(
        Order("order_42", "node_20", 5.0, 200.0)
    )

    twin = DigitalTwin()
    twin.synchronise(environment.physical_state())

    decision = Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=125.0,
    )

    generator = RelevanceConditionGenerator(
        DivergenceInjector()
    )

    with pytest.raises(ValueError):
        generator.apply(
            RelevanceCondition.B_HIGH_DIVERGENCE_LOW_RELEVANCE,
            twin,
            decision,
        )
