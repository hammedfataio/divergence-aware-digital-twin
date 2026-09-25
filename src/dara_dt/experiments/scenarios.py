"""Experimental divergence scenarios for DARA-DT."""

from dataclasses import dataclass
from enum import Enum


class ScenarioType(str, Enum):
    """Controlled divergence scenarios used in DARA-DT experiments."""

    D0_SYNCHRONISED = "D0"
    D1_TEMPORAL = "D1"
    D2_STATE = "D2"
    D3_OPERATIONAL = "D3"
    D4_DISTRIBUTIONAL = "D4"
    D5_COMPOUND = "D5"


@dataclass(frozen=True)
class Scenario:
    """Definition of a controlled experimental scenario."""

    scenario_type: ScenarioType
    name: str
    description: str


SCENARIOS = {
    ScenarioType.D0_SYNCHRONISED: Scenario(
        scenario_type=ScenarioType.D0_SYNCHRONISED,
        name="Synchronised baseline",
        description=(
            "Physical and Digital Twin states remain synchronised."
        ),
    ),
    ScenarioType.D1_TEMPORAL: Scenario(
        scenario_type=ScenarioType.D1_TEMPORAL,
        name="Temporal divergence",
        description=(
            "The Digital Twin contains stale or delayed state information."
        ),
    ),
    ScenarioType.D2_STATE: Scenario(
        scenario_type=ScenarioType.D2_STATE,
        name="State divergence",
        description=(
            "A Digital Twin state variable differs from physical reality."
        ),
    ),
    ScenarioType.D3_OPERATIONAL: Scenario(
        scenario_type=ScenarioType.D3_OPERATIONAL,
        name="Operational divergence",
        description=(
            "An operational event is not correctly represented "
            "in the Digital Twin."
        ),
    ),
    ScenarioType.D4_DISTRIBUTIONAL: Scenario(
        scenario_type=ScenarioType.D4_DISTRIBUTIONAL,
        name="Distributional divergence",
        description=(
            "Operating conditions differ from the conditions represented "
            "by the Digital Twin or decision model."
        ),
    ),
    ScenarioType.D5_COMPOUND: Scenario(
        scenario_type=ScenarioType.D5_COMPOUND,
        name="Compound divergence",
        description=(
            "Multiple divergence mechanisms occur simultaneously."
        ),
    ),
}
