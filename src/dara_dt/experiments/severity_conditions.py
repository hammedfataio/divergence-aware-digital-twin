"""Severity conditions for EXP-004.

This module defines controlled vehicle-capacity divergence conditions used to
study how divergence magnitude relates to physical decision validity.

The conditions are experimental inputs only. They do not determine assurance
actions or ground-truth outcomes.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SeverityCondition:
    """A controlled physical-digital capacity divergence condition."""

    name: str
    twin_capacity: int
    physical_capacity: int
    order_demand: int

    @property
    def divergence_magnitude(self) -> int:
        """Return the absolute capacity difference between Twin and reality."""
        return abs(self.twin_capacity - self.physical_capacity)

    @property
    def physically_valid(self) -> bool:
        """Return whether the physical vehicle can satisfy the order."""
        return self.physical_capacity >= self.order_demand


def build_severity_conditions() -> tuple[SeverityCondition, ...]:
    """Return the predefined EXP-004 severity conditions.

    The Digital Twin reports capacity 10 for every condition.
    The physical capacity is progressively reduced around an order-demand
    boundary of 5 units.
    """

    return (
        SeverityCondition(
            name="S0",
            twin_capacity=10,
            physical_capacity=10,
            order_demand=5,
        ),
        SeverityCondition(
            name="S1",
            twin_capacity=10,
            physical_capacity=9,
            order_demand=5,
        ),
        SeverityCondition(
            name="S2",
            twin_capacity=10,
            physical_capacity=7,
            order_demand=5,
        ),
        SeverityCondition(
            name="S3",
            twin_capacity=10,
            physical_capacity=6,
            order_demand=5,
        ),
        SeverityCondition(
            name="S4",
            twin_capacity=10,
            physical_capacity=5,
            order_demand=5,
        ),
        SeverityCondition(
            name="S5",
            twin_capacity=10,
            physical_capacity=4,
            order_demand=5,
        ),
        SeverityCondition(
            name="S6",
            twin_capacity=10,
            physical_capacity=2,
            order_demand=5,
        ),
    )
