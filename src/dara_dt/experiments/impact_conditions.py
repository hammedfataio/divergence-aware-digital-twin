"""Controlled conditions for EXP-005 decision-impact evaluation.

The conditions vary physical-digital capacity divergence and order
demand so that decision-impact-aware assurance can be evaluated against
policies based only on divergence magnitude.

Ground-truth properties defined here are for experimental evaluation.
They must not be supplied directly to runtime assurance policies.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImpactCondition:
    """Controlled capacity condition for EXP-005."""

    name: str
    twin_capacity: int
    physical_capacity: int
    order_demand: int

    @property
    def divergence_magnitude(self) -> int:
        """Return absolute physical-digital capacity divergence."""

        return abs(
            self.twin_capacity - self.physical_capacity
        )

    @property
    def physical_margin(self) -> int:
        """Return the ground-truth physical decision margin."""

        return self.physical_capacity - self.order_demand

    @property
    def physically_valid(self) -> bool:
        """Return whether physical capacity satisfies demand."""

        return self.physical_margin >= 0


def build_impact_conditions() -> tuple[ImpactCondition, ...]:
    """Build controlled EXP-005 decision-impact conditions.

    I0-I6 reproduce the EXP-004 capacity progression.

    I7-I14 introduce changing decision requirements so that equal or
    similar divergence magnitudes can have different decision impacts.
    """

    return (
        ImpactCondition(
            name="I0_synchronised",
            twin_capacity=10,
            physical_capacity=10,
            order_demand=5,
        ),
        ImpactCondition(
            name="I1_reduced_margin",
            twin_capacity=10,
            physical_capacity=9,
            order_demand=5,
        ),
        ImpactCondition(
            name="I2_reduced_margin",
            twin_capacity=10,
            physical_capacity=7,
            order_demand=5,
        ),
        ImpactCondition(
            name="I3_positive_margin",
            twin_capacity=10,
            physical_capacity=6,
            order_demand=5,
        ),
        ImpactCondition(
            name="I4_boundary",
            twin_capacity=10,
            physical_capacity=5,
            order_demand=5,
        ),
        ImpactCondition(
            name="I5_invalid",
            twin_capacity=10,
            physical_capacity=4,
            order_demand=5,
        ),
        ImpactCondition(
            name="I6_invalid",
            twin_capacity=10,
            physical_capacity=2,
            order_demand=5,
        ),
        ImpactCondition(
            name="I7_same_divergence_valid",
            twin_capacity=10,
            physical_capacity=7,
            order_demand=5,
        ),
        ImpactCondition(
            name="I8_same_divergence_invalid",
            twin_capacity=10,
            physical_capacity=7,
            order_demand=8,
        ),
        ImpactCondition(
            name="I9_high_capacity_valid",
            twin_capacity=15,
            physical_capacity=12,
            order_demand=10,
        ),
        ImpactCondition(
            name="I10_high_capacity_invalid",
            twin_capacity=15,
            physical_capacity=9,
            order_demand=10,
        ),
        ImpactCondition(
            name="I11_tight_boundary",
            twin_capacity=8,
            physical_capacity=7,
            order_demand=7,
        ),
        ImpactCondition(
            name="I12_tight_invalid",
            twin_capacity=8,
            physical_capacity=6,
            order_demand=7,
        ),
        ImpactCondition(
            name="I13_large_system_valid",
            twin_capacity=20,
            physical_capacity=18,
            order_demand=17,
        ),
        ImpactCondition(
            name="I14_large_system_invalid",
            twin_capacity=20,
            physical_capacity=16,
            order_demand=17,
        ),
    )
