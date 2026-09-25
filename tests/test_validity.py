"""Tests for independent physical decision-validity evaluation."""

from dara_dt.decision.model import Decision
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.experiments.ground_truth import InterventionLabel
from dara_dt.simulation.environment import LogisticsEnvironment
from dara_dt.simulation.order import Order
from dara_dt.simulation.vehicle import Vehicle


def create_environment(
    capacity: float = 10.0,
) -> LogisticsEnvironment:
    """Create a physical logistics environment for validation."""

    environment = LogisticsEnvironment()

    environment.add_vehicle(
        Vehicle(
            vehicle_id="vehicle_07",
            location="node_07",
            capacity=capacity,
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


def create_decision() -> Decision:
    """Create the decision evaluated by the physical validator."""

    return Decision(
        decision_id="decision_001",
        action="assign_vehicle",
        vehicle_id="vehicle_07",
        order_id="order_42",
        timestamp=125.0,
    )


def test_valid_physical_decision_requires_no_intervention():
    environment = create_environment()
    validator = PhysicalDecisionValidator()

    validity = validator.validate(
        create_decision(),
        environment.physical_state(),
    )

    ground_truth = validator.ground_truth(
        create_decision(),
        environment.physical_state(),
    )

    assert validity.valid is True
    assert ground_truth.label == InterventionLabel.DO_NOT_INTERVENE
    assert ground_truth.intervention_required is False


def test_broken_vehicle_requires_intervention():
    environment = create_environment()

    environment.get_vehicle(
        "vehicle_07"
    ).mark_broken_down()

    validator = PhysicalDecisionValidator()

    validity = validator.validate(
        create_decision(),
        environment.physical_state(),
    )

    ground_truth = validator.ground_truth(
        create_decision(),
        environment.physical_state(),
    )

    assert validity.valid is False
    assert ground_truth.label == InterventionLabel.INTERVENE
    assert ground_truth.intervention_required is True


def test_insufficient_capacity_requires_intervention():
    environment = create_environment(capacity=4.0)
    validator = PhysicalDecisionValidator()

    validity = validator.validate(
        create_decision(),
        environment.physical_state(),
    )

    assert validity.valid is False

    ground_truth = validator.ground_truth(
        create_decision(),
        environment.physical_state(),
    )

    assert ground_truth.label == InterventionLabel.INTERVENE


def test_non_waiting_order_requires_intervention():
    environment = create_environment()

    environment.get_order(
        "order_42"
    ).assign()

    validator = PhysicalDecisionValidator()

    validity = validator.validate(
        create_decision(),
        environment.physical_state(),
    )

    assert validity.valid is False


def test_missing_vehicle_is_invalid():
    environment = create_environment()

    decision = Decision(
        decision_id="decision_002",
        action="assign_vehicle",
        vehicle_id="vehicle_missing",
        order_id="order_42",
        timestamp=125.0,
    )

    validator = PhysicalDecisionValidator()

    validity = validator.validate(
        decision,
        environment.physical_state(),
    )

    assert validity.valid is False
