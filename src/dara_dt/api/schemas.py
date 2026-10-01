"""Pydantic schemas for the DARA-DT research API.

These schemas define the application-facing representation of a DARA-DT
scenario. They intentionally remain separate from the experimental domain
models so the API layer does not modify the frozen research engine.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


EvidenceStatusValue = Literal[
    "available",
    "stale",
    "missing",
    "conflicting",
]

AuthorityValue = Literal[
    "allow",
    "restrict",
    "defer",
    "fallback",
]


class StateVariable(BaseModel):
    """A single named state variable."""

    name: str
    value: Any


class EntityState(BaseModel):
    """State representation for a physical or Digital Twin entity."""

    entity_id: str
    entity_type: str
    variables: dict[str, Any] = Field(default_factory=dict)


class SystemState(BaseModel):
    """Collection of entities representing a system state."""

    timestamp: float | None = None
    entities: list[EntityState] = Field(default_factory=list)


class DivergenceRecord(BaseModel):
    """Application-facing representation of physical–digital divergence."""

    entity_id: str
    variable: str
    physical_value: Any
    twin_value: Any

    decision_relevant: bool | None = None
    decision_impacting: bool | None = None


class DecisionDependency(BaseModel):
    """Dependency required by an autonomous decision."""

    dependency: str
    relevant: bool = True


class AIDecision(BaseModel):
    """Autonomous decision exposed through the research API."""

    decision_id: str
    action: str

    vehicle_id: str | None = None
    order_id: str | None = None

    dependencies: list[DecisionDependency] = Field(default_factory=list)


class RuntimeEvidenceRecord(BaseModel):
    """Runtime evidence associated with a decision dependency."""

    source: str
    dependency: str

    observed_value: Any | None = None

    timestamp: float | None = None

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    status: EvidenceStatusValue = "available"


class PropagationRecord(BaseModel):
    """A physical–digital divergence propagation relationship."""

    origin: str

    affected_dependency: str | None = None

    source_decision: str | None = None
    target_decision: str | None = None

    propagating: bool = False

    path: list[str] = Field(default_factory=list)


class AssuranceResult(BaseModel):
    """Runtime assurance decision returned by an assurance policy."""

    policy: str

    authority: AuthorityValue

    intervene: bool

    reason: str

    relevant_divergence_count: int = Field(
        default=0,
        ge=0,
    )


class GroundTruthResult(BaseModel):
    """Evaluator-only physical ground-truth result."""

    intervention_required: bool

    reason: str | None = None


class EvaluationResult(BaseModel):
    """Evaluation of an assurance decision against physical ground truth."""

    outcome: Literal[
        "true_intervention",
        "false_intervention",
        "missed_intervention",
        "correct_non_intervention",
    ]

    correct: bool


class ScenarioResponse(BaseModel):
    """Complete application-facing DARA-DT scenario."""

    scenario_id: str

    description: str

    physical_state: SystemState

    twin_state: SystemState

    divergences: list[DivergenceRecord] = Field(default_factory=list)

    ai_decision: AIDecision

    runtime_evidence: list[RuntimeEvidenceRecord] = Field(
        default_factory=list,
    )

    propagation: list[PropagationRecord] = Field(
        default_factory=list,
    )

    assurance_results: list[AssuranceResult] = Field(
        default_factory=list,
    )

    ground_truth: GroundTruthResult | None = None

    evaluations: dict[str, EvaluationResult] = Field(
        default_factory=dict,
    )


class ExperimentMetric(BaseModel):
    """Aggregate metric for an assurance policy."""

    policy: str

    conditions: int = Field(ge=0)

    true_interventions: int = Field(ge=0)
    false_interventions: int = Field(ge=0)
    missed_interventions: int = Field(ge=0)
    correct_non_interventions: int = Field(ge=0)

    accuracy: float = Field(ge=0.0, le=1.0)
    precision: float = Field(ge=0.0, le=1.0)
    recall: float = Field(ge=0.0, le=1.0)

    false_intervention_rate: float = Field(
        ge=0.0,
        le=1.0,
    )

    missed_intervention_rate: float = Field(
        ge=0.0,
        le=1.0,
    )

    autonomy_availability: float = Field(
        ge=0.0,
        le=1.0,
    )


class ExperimentSummary(BaseModel):
    """Summary of a completed DARA-DT experiment."""

    experiment_id: str

    title: str

    status: Literal["complete"]

    conditions: int | None = Field(
        default=None,
        ge=0,
    )

    metrics: list[ExperimentMetric] = Field(
        default_factory=list,
    )

    finding: str | None = None


class ProjectStatusResponse(BaseModel):
    """High-level status returned by the research API."""

    project: str = "DARA-DT"

    full_name: str = (
        "Divergence-Aware Runtime Assurance for Digital Twins"
    )

    research_domain: str = "Trustworthy Intelligent Systems"

    experimental_domain: str = (
        "Autonomous Logistics Digital Twins"
    )

    experiments_completed: int = 10

    experiments_total: int = 10

    experimental_programme_complete: bool = True

    contribution_status: str = "frozen"

    current_stage: str = "research demonstrator engineering"


class HealthResponse(BaseModel):
    """Basic service health response."""

    status: Literal["ok"] = "ok"

    service: str = "DARA-DT Research API"

    version: str = "0.1.0"
