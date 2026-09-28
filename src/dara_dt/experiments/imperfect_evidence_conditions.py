"""Controlled imperfect-evidence conditions for EXP-008.

EXP-008 compares runtime-contract assurance with evidence-aware DARA-DT
when runtime observations cannot be assumed to perfectly represent
physical reality.

The experiment explicitly separates:

    Physical ground truth
    Digital Twin state
    Runtime evidence

The conditions in this module are deterministic experimental inputs.
Ground-truth intervention labels must be derived independently from the
physical state and must never be supplied directly to an assurance policy.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.cross_dependency_conditions import DependencyFamily


class EvidenceScenario(str, Enum):
    """Evidence-quality scenarios evaluated in EXP-008."""

    RELIABLE = "reliable"
    STALE = "stale"
    MISSING = "missing"
    CONFLICTING = "conflicting"


@dataclass(frozen=True)
class ImperfectEvidenceCondition:
    """One controlled EXP-008 condition."""

    condition_id: str
    family: DependencyFamily
    evidence_scenario: EvidenceScenario
    description: str

    twin_value: Any
    physical_value: Any

    primary_evidence_value: Any = None
    secondary_evidence_value: Any = None

    order_demand: float = 5.0
    required_status: str = "operational"
    required_available: bool = True
    permitted_locations: tuple[str, ...] = (
        "depot",
        "near_depot",
    )

    observation_timestamp: float = 10.0
    evaluation_timestamp: float = 10.0

    @property
    def evidence_status(self) -> EvidenceStatus:
        """Map the experimental scenario to the runtime evidence status."""

        if self.evidence_scenario == EvidenceScenario.RELIABLE:
            return EvidenceStatus.AVAILABLE

        if self.evidence_scenario == EvidenceScenario.STALE:
            return EvidenceStatus.STALE

        if self.evidence_scenario == EvidenceScenario.MISSING:
            return EvidenceStatus.MISSING

        if self.evidence_scenario == EvidenceScenario.CONFLICTING:
            return EvidenceStatus.CONFLICTING

        raise ValueError(
            f"Unsupported evidence scenario: {self.evidence_scenario}"
        )

    @property
    def has_twin_divergence(self) -> bool:
        """Return whether physical state differs from Digital Twin state."""

        return self.twin_value != self.physical_value

    @property
    def evidence_age(self) -> float:
        """Return evidence age at evaluation time."""

        return self.evaluation_timestamp - self.observation_timestamp

    @property
    def has_primary_evidence(self) -> bool:
        """Return whether a primary runtime observation exists."""

        return self.primary_evidence_value is not None

    @property
    def has_secondary_evidence(self) -> bool:
        """Return whether a secondary runtime observation exists."""

        return self.secondary_evidence_value is not None

    @property
    def has_conflicting_evidence(self) -> bool:
        """Return whether two incompatible observations are supplied."""

        return (
            self.evidence_scenario == EvidenceScenario.CONFLICTING
            and self.has_primary_evidence
            and self.has_secondary_evidence
            and self.primary_evidence_value != self.secondary_evidence_value
        )


def build_imperfect_evidence_conditions(
) -> tuple[ImperfectEvidenceCondition, ...]:
    """Build the pre-registered 24-condition EXP-008 matrix.

    Each dependency family contains eight conditions:

    R0:
        Physically valid decision with reliable evidence.

    R1:
        Physically invalid decision with reliable evidence.

    S0:
        Physically valid decision with stale evidence suggesting invalidity.

    S1:
        Physically invalid decision with stale evidence suggesting validity.

    M0:
        Physically valid decision with missing evidence.

    M1:
        Physically invalid decision with missing evidence.

    C0:
        Physically valid decision with conflicting evidence.

    C1:
        Physically invalid decision with conflicting evidence.
    """

    return (
        # ===============================================================
        # Capacity
        # ===============================================================
        ImperfectEvidenceCondition(
            condition_id="CAP-R0",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.RELIABLE,
            description=(
                "Valid capacity decision with reliable runtime evidence."
            ),
            twin_value=10.0,
            physical_value=8.0,
            primary_evidence_value=8.0,
            order_demand=5.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="CAP-R1",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.RELIABLE,
            description=(
                "Invalid capacity decision with reliable runtime evidence."
            ),
            twin_value=10.0,
            physical_value=4.0,
            primary_evidence_value=4.0,
            order_demand=5.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="CAP-S0",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.STALE,
            description=(
                "Capacity is physically sufficient, but stale evidence "
                "suggests insufficient capacity."
            ),
            twin_value=10.0,
            physical_value=8.0,
            primary_evidence_value=4.0,
            order_demand=5.0,
            observation_timestamp=2.0,
            evaluation_timestamp=10.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="CAP-S1",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.STALE,
            description=(
                "Capacity is physically insufficient, but stale evidence "
                "suggests sufficient capacity."
            ),
            twin_value=10.0,
            physical_value=4.0,
            primary_evidence_value=8.0,
            order_demand=5.0,
            observation_timestamp=2.0,
            evaluation_timestamp=10.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="CAP-M0",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.MISSING,
            description=(
                "Capacity decision is physically valid, but current "
                "capacity evidence is missing."
            ),
            twin_value=10.0,
            physical_value=8.0,
            primary_evidence_value=None,
            order_demand=5.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="CAP-M1",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.MISSING,
            description=(
                "Capacity decision is physically invalid, but current "
                "capacity evidence is missing."
            ),
            twin_value=10.0,
            physical_value=4.0,
            primary_evidence_value=None,
            order_demand=5.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="CAP-C0",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.CONFLICTING,
            description=(
                "Capacity decision is physically valid while runtime "
                "sources disagree about available capacity."
            ),
            twin_value=10.0,
            physical_value=8.0,
            primary_evidence_value=8.0,
            secondary_evidence_value=4.0,
            order_demand=5.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="CAP-C1",
            family=DependencyFamily.CAPACITY,
            evidence_scenario=EvidenceScenario.CONFLICTING,
            description=(
                "Capacity decision is physically invalid while runtime "
                "sources disagree about available capacity."
            ),
            twin_value=10.0,
            physical_value=4.0,
            primary_evidence_value=8.0,
            secondary_evidence_value=4.0,
            order_demand=5.0,
        ),

        # ===============================================================
        # Operational status
        # ===============================================================
        ImperfectEvidenceCondition(
            condition_id="STATUS-R0",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.RELIABLE,
            description=(
                "Operational vehicle with reliable operational-status "
                "evidence."
            ),
            twin_value="operational",
            physical_value="operational",
            primary_evidence_value="operational",
        ),
        ImperfectEvidenceCondition(
            condition_id="STATUS-R1",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.RELIABLE,
            description=(
                "Broken-down vehicle with reliable failure evidence."
            ),
            twin_value="operational",
            physical_value="broken_down",
            primary_evidence_value="broken_down",
        ),
        ImperfectEvidenceCondition(
            condition_id="STATUS-S0",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.STALE,
            description=(
                "Vehicle is physically operational, but stale evidence "
                "reports an earlier breakdown."
            ),
            twin_value="operational",
            physical_value="operational",
            primary_evidence_value="broken_down",
            observation_timestamp=2.0,
            evaluation_timestamp=10.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="STATUS-S1",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.STALE,
            description=(
                "Vehicle is physically broken down, but stale evidence "
                "still reports it as operational."
            ),
            twin_value="operational",
            physical_value="broken_down",
            primary_evidence_value="operational",
            observation_timestamp=2.0,
            evaluation_timestamp=10.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="STATUS-M0",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.MISSING,
            description=(
                "Vehicle is physically operational, but current status "
                "evidence is missing."
            ),
            twin_value="operational",
            physical_value="operational",
            primary_evidence_value=None,
        ),
        ImperfectEvidenceCondition(
            condition_id="STATUS-M1",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.MISSING,
            description=(
                "Vehicle is physically broken down, but current status "
                "evidence is missing."
            ),
            twin_value="operational",
            physical_value="broken_down",
            primary_evidence_value=None,
        ),
        ImperfectEvidenceCondition(
            condition_id="STATUS-C0",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.CONFLICTING,
            description=(
                "Vehicle is physically operational while runtime sources "
                "disagree about operational status."
            ),
            twin_value="operational",
            physical_value="operational",
            primary_evidence_value="operational",
            secondary_evidence_value="broken_down",
        ),
        ImperfectEvidenceCondition(
            condition_id="STATUS-C1",
            family=DependencyFamily.STATUS,
            evidence_scenario=EvidenceScenario.CONFLICTING,
            description=(
                "Vehicle is physically broken down while runtime sources "
                "disagree about operational status."
            ),
            twin_value="operational",
            physical_value="broken_down",
            primary_evidence_value="operational",
            secondary_evidence_value="broken_down",
        ),

        # ===============================================================
        # Location / availability
        # ===============================================================
        ImperfectEvidenceCondition(
            condition_id="LOC-R0",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.RELIABLE,
            description=(
                "Vehicle is physically available at a permitted location "
                "with reliable evidence."
            ),
            twin_value=("depot", True),
            physical_value=("near_depot", True),
            primary_evidence_value=("near_depot", True),
        ),
        ImperfectEvidenceCondition(
            condition_id="LOC-R1",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.RELIABLE,
            description=(
                "Vehicle is physically unavailable at an incompatible "
                "location with reliable evidence."
            ),
            twin_value=("depot", True),
            physical_value=("remote_site", False),
            primary_evidence_value=("remote_site", False),
        ),
        ImperfectEvidenceCondition(
            condition_id="LOC-S0",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.STALE,
            description=(
                "Vehicle is physically dispatchable, but stale evidence "
                "reports an incompatible location and unavailable state."
            ),
            twin_value=("depot", True),
            physical_value=("near_depot", True),
            primary_evidence_value=("remote_site", False),
            observation_timestamp=2.0,
            evaluation_timestamp=10.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="LOC-S1",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.STALE,
            description=(
                "Vehicle is physically non-dispatchable, but stale evidence "
                "reports a permitted location and available state."
            ),
            twin_value=("depot", True),
            physical_value=("remote_site", False),
            primary_evidence_value=("depot", True),
            observation_timestamp=2.0,
            evaluation_timestamp=10.0,
        ),
        ImperfectEvidenceCondition(
            condition_id="LOC-M0",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.MISSING,
            description=(
                "Vehicle is physically dispatchable, but current "
                "location/availability evidence is missing."
            ),
            twin_value=("depot", True),
            physical_value=("near_depot", True),
            primary_evidence_value=None,
        ),
        ImperfectEvidenceCondition(
            condition_id="LOC-M1",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.MISSING,
            description=(
                "Vehicle is physically non-dispatchable, but current "
                "location/availability evidence is missing."
            ),
            twin_value=("depot", True),
            physical_value=("remote_site", False),
            primary_evidence_value=None,
        ),
        ImperfectEvidenceCondition(
            condition_id="LOC-C0",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.CONFLICTING,
            description=(
                "Vehicle is physically dispatchable while runtime sources "
                "disagree about location and availability."
            ),
            twin_value=("depot", True),
            physical_value=("near_depot", True),
            primary_evidence_value=("near_depot", True),
            secondary_evidence_value=("remote_site", False),
        ),
        ImperfectEvidenceCondition(
            condition_id="LOC-C1",
            family=DependencyFamily.LOCATION_AVAILABILITY,
            evidence_scenario=EvidenceScenario.CONFLICTING,
            description=(
                "Vehicle is physically non-dispatchable while runtime "
                "sources disagree about location and availability."
            ),
            twin_value=("depot", True),
            physical_value=("remote_site", False),
            primary_evidence_value=("depot", True),
            secondary_evidence_value=("remote_site", False),
        ),
    )
