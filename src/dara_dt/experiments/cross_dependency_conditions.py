"""Pre-registered conditions for EXP-007 cross-dependency generalisation.

EXP-007 tests whether the DARA-DT relevance-to-impact reasoning chain
generalises beyond vehicle capacity to operational status and
location/availability dependencies.

The conditions defined here are experimental inputs. Ground-truth labels
are derived independently from physical state and decision requirements;
they must not be supplied directly to assurance policies.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class DependencyFamily(str, Enum):
    """Decision-dependency families evaluated in EXP-007."""

    CAPACITY = "capacity"
    STATUS = "status"
    LOCATION_AVAILABILITY = "location_availability"


@dataclass(frozen=True)
class CrossDependencyCondition:
    """Controlled condition for EXP-007."""

    condition_id: str
    family: DependencyFamily
    description: str

    selected_vehicle_id: str = "vehicle_01"
    unrelated_vehicle_id: str = "vehicle_02"

    twin_selected_value: Any = None
    physical_selected_value: Any = None

    twin_unrelated_value: Any = None
    physical_unrelated_value: Any = None

    order_demand: float = 5.0
    required_status: str = "operational"
    required_available: bool = True
    permitted_locations: tuple[str, ...] = (
        "depot",
        "near_depot",
    )

    @property
    def has_selected_vehicle_divergence(self) -> bool:
        """Return whether the selected vehicle differs from its Twin."""

        return self.twin_selected_value != self.physical_selected_value

    @property
    def has_unrelated_vehicle_divergence(self) -> bool:
        """Return whether an unrelated vehicle differs from its Twin."""

        return self.twin_unrelated_value != self.physical_unrelated_value

    @property
    def has_any_divergence(self) -> bool:
        """Return whether the condition contains any divergence."""

        return (
            self.has_selected_vehicle_divergence
            or self.has_unrelated_vehicle_divergence
        )


def build_cross_dependency_conditions(
) -> tuple[CrossDependencyCondition, ...]:
    """Build the pre-registered 12-condition EXP-007 matrix.

    Each dependency family contains four conceptual cases:

    C0:
        No relevant divergence.

    C1:
        Divergence exists on an unrelated vehicle.

    C2:
        Divergence affects the selected decision dependency but the
        physical decision remains valid.

    C3:
        Divergence affects the selected dependency and invalidates the
        physical decision.
    """

    return (
        # ---------------------------------------------------------------
        # Capacity
        # ---------------------------------------------------------------
        CrossDependencyCondition(
            condition_id="CAP-0",
            family=DependencyFamily.CAPACITY,
            description="Synchronized selected-vehicle capacity.",
            twin_selected_value=10.0,
            physical_selected_value=10.0,
            twin_unrelated_value=10.0,
            physical_unrelated_value=10.0,
            order_demand=5.0,
        ),
        CrossDependencyCondition(
            condition_id="CAP-1",
            family=DependencyFamily.CAPACITY,
            description=(
                "Capacity divergence exists only on an unrelated vehicle."
            ),
            twin_selected_value=10.0,
            physical_selected_value=10.0,
            twin_unrelated_value=10.0,
            physical_unrelated_value=3.0,
            order_demand=5.0,
        ),
        CrossDependencyCondition(
            condition_id="CAP-2",
            family=DependencyFamily.CAPACITY,
            description=(
                "Selected-vehicle capacity diverges but remains sufficient "
                "for the order."
            ),
            twin_selected_value=10.0,
            physical_selected_value=7.0,
            twin_unrelated_value=10.0,
            physical_unrelated_value=10.0,
            order_demand=5.0,
        ),
        CrossDependencyCondition(
            condition_id="CAP-3",
            family=DependencyFamily.CAPACITY,
            description=(
                "Selected-vehicle capacity divergence makes the assignment "
                "physically infeasible."
            ),
            twin_selected_value=10.0,
            physical_selected_value=6.0,
            twin_unrelated_value=10.0,
            physical_unrelated_value=10.0,
            order_demand=8.0,
        ),

        # ---------------------------------------------------------------
        # Operational status
        # ---------------------------------------------------------------
        CrossDependencyCondition(
            condition_id="STATUS-0",
            family=DependencyFamily.STATUS,
            description="Selected vehicle remains operational and synchronized.",
            twin_selected_value="operational",
            physical_selected_value="operational",
            twin_unrelated_value="operational",
            physical_unrelated_value="operational",
        ),
        CrossDependencyCondition(
            condition_id="STATUS-1",
            family=DependencyFamily.STATUS,
            description=(
                "Operational-status divergence exists only on an unrelated "
                "vehicle."
            ),
            twin_selected_value="operational",
            physical_selected_value="operational",
            twin_unrelated_value="operational",
            physical_unrelated_value="broken_down",
        ),
        CrossDependencyCondition(
            condition_id="STATUS-2",
            family=DependencyFamily.STATUS,
            description=(
                "Selected-vehicle status differs from the Twin but still "
                "satisfies the required operational state."
            ),
            twin_selected_value="maintenance_due",
            physical_selected_value="operational",
            twin_unrelated_value="operational",
            physical_unrelated_value="operational",
            required_status="operational",
        ),
        CrossDependencyCondition(
            condition_id="STATUS-3",
            family=DependencyFamily.STATUS,
            description=(
                "Selected vehicle is physically broken down while the Twin "
                "still reports it as operational."
            ),
            twin_selected_value="operational",
            physical_selected_value="broken_down",
            twin_unrelated_value="operational",
            physical_unrelated_value="operational",
            required_status="operational",
        ),

        # ---------------------------------------------------------------
        # Location / availability
        # ---------------------------------------------------------------
        CrossDependencyCondition(
            condition_id="LOC-0",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            description=(
                "Selected vehicle is synchronized at a permitted dispatch "
                "location."
            ),
            twin_selected_value=("depot", True),
            physical_selected_value=("depot", True),
            twin_unrelated_value=("depot", True),
            physical_unrelated_value=("depot", True),
        ),
        CrossDependencyCondition(
            condition_id="LOC-1",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            description=(
                "Location/availability divergence exists only on an "
                "unrelated vehicle."
            ),
            twin_selected_value=("depot", True),
            physical_selected_value=("depot", True),
            twin_unrelated_value=("depot", True),
            physical_unrelated_value=("remote_site", False),
        ),
        CrossDependencyCondition(
            condition_id="LOC-2",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            description=(
                "Selected vehicle has moved from the Twin location but "
                "remains available at a permitted dispatch location."
            ),
            twin_selected_value=("depot", True),
            physical_selected_value=("near_depot", True),
            twin_unrelated_value=("depot", True),
            physical_unrelated_value=("depot", True),
            permitted_locations=("depot", "near_depot"),
        ),
        CrossDependencyCondition(
            condition_id="LOC-3",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            description=(
                "Selected vehicle is physically unavailable at an "
                "incompatible location while the Twin reports it ready "
                "at the depot."
            ),
            twin_selected_value=("depot", True),
            physical_selected_value=("remote_site", False),
            twin_unrelated_value=("depot", True),
            physical_unrelated_value=("depot", True),
            permitted_locations=("depot", "near_depot"),
        ),
    )
