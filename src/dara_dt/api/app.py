"""FastAPI application for the DARA-DT research demonstrator.

The API exposes the completed DARA-DT research programme through a small,
read-only application interface.

Interactive scenario execution will be added separately so that frozen
experimental evidence remains distinct from live demonstration runs.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from dara_dt.api.schemas import (
    ExperimentSummary,
    HealthResponse,
    ProjectStatusResponse,
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
