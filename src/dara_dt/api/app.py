"""FastAPI application for the DARA-DT research demonstrator.

The API exposes the completed DARA-DT research programme and provides
application access to individual frozen EXP-010 scenarios.

Historical experimental results and live scenario execution are deliberately
kept separate:

- experiment endpoints expose frozen verified research results;
- scenario endpoints execute existing frozen conditions through the research
  engine for interactive demonstration.

The API layer does not redefine experimental logic or modify the frozen
research programme.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from dara_dt.api.scenario_service import (
    ScenarioNotFoundError,
    scenario_service,
)
from dara_dt.api.schemas import (
    ExperimentSummary,
    HealthResponse,
    ProjectStatusResponse,
    ScenarioResponse,
)
from dara_dt.api.service import research_service


app = FastAPI(
    title="DARA-DT Research API",
    description=(
        "Research API for Divergence-Aware Runtime Assurance for "
        "AI-Driven Digital Twins."
    ),
    version="0.1.0",
)


@app.get(
    "/",
    tags=["General"],
)
def root() -> dict[str, str]:
    """Return basic information about the research API."""

    return {
        "project": "DARA-DT",
        "service": "Research API",
        "status": "running",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["General"],
)
def health() -> HealthResponse:
    """Return service health information."""

    return HealthResponse()


@app.get(
    "/api/project/status",
    response_model=ProjectStatusResponse,
    tags=["Research"],
)
def project_status() -> ProjectStatusResponse:
    """Return the current DARA-DT research status."""

    return research_service.project_status()


@app.get(
    "/api/experiments",
    response_model=list[str],
    tags=["Experiments"],
)
def experiments() -> list[str]:
    """Return the completed DARA-DT experimental programme."""

    return research_service.completed_experiments()


@app.get(
    "/api/experiments/EXP-010/results",
    response_model=ExperimentSummary,
    tags=["Experiments"],
)
def experiment_010_results() -> ExperimentSummary:
    """Return the frozen verified EXP-010 aggregate results."""

    return research_service.experiment_010_summary()


@app.get(
    "/api/experiments/{experiment_id}/results",
    response_model=ExperimentSummary,
    tags=["Experiments"],
)
def experiment_results(
    experiment_id: str,
) -> ExperimentSummary:
    """Return results for a supported experiment."""

    normalised_id = experiment_id.upper()

    if normalised_id == "EXP-010":
        return research_service.experiment_010_summary()

    if normalised_id not in research_service.completed_experiments():
        raise HTTPException(
            status_code=404,
            detail=f"Unknown experiment: {experiment_id}",
        )

    raise HTTPException(
        status_code=501,
        detail=(
            f"{normalised_id} is complete, but its API result adapter "
            "has not yet been implemented."
        ),
    )


@app.get(
    "/api/scenarios",
    response_model=list[str],
    tags=["Scenarios"],
)
def scenarios() -> list[str]:
    """Return the frozen EXP-010 scenarios available for demonstration."""

    return scenario_service.available_scenarios()


@app.post(
    "/api/scenarios/{scenario_id}/run",
    response_model=ScenarioResponse,
    tags=["Scenarios"],
)
def run_scenario(
    scenario_id: str,
) -> ScenarioResponse:
    """Execute one frozen scenario through the DARA-DT research engine."""

    try:
        return scenario_service.run_scenario(scenario_id)

    except ScenarioNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
