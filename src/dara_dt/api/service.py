"""Application service layer for the DARA-DT research API.

This module provides read-only application services over the frozen
experimental programme. It does not modify the research engine or reproduce
experimental logic inside the API layer.

The service currently exposes project metadata and the verified aggregate
results from EXP-010. Scenario execution will be connected separately to the
existing DARA-DT engine.
"""

from __future__ import annotations

from dara_dt.api.schemas import (
    ExperimentMetric,
    ExperimentSummary,
    ProjectStatusResponse,
)


class ResearchService:
    """Read-only service for DARA-DT research information."""

    def project_status(self) -> ProjectStatusResponse:
        """Return the current DARA-DT research status."""
        return ProjectStatusResponse()

    def experiment_010_summary(self) -> ExperimentSummary:
        """Return the verified aggregate results from EXP-010."""

        return ExperimentSummary(
            experiment_id="EXP-010",
            title="Propagation-Aware Physical–Digital Divergence",
            status="complete",
            conditions=30,
            metrics=[
                ExperimentMetric(
                    policy="No Assurance",
                    conditions=30,
                    true_interventions=0,
                    false_interventions=0,
                    missed_interventions=19,
                    correct_non_interventions=11,
                    accuracy=0.367,
                    precision=0.000,
                    recall=0.000,
                    false_intervention_rate=0.000,
                    missed_intervention_rate=1.000,
                    autonomy_availability=1.000,
                ),
                ExperimentMetric(
                    policy="Local Contract",
                    conditions=30,
                    true_interventions=8,
                    false_interventions=3,
                    missed_interventions=11,
                    correct_non_interventions=8,
                    accuracy=0.533,
                    precision=0.727,
                    recall=0.421,
                    false_intervention_rate=0.273,
                    missed_intervention_rate=0.579,
                    autonomy_availability=0.633,
                ),
                ExperimentMetric(
                    policy="Global Assurance",
                    conditions=30,
                    true_interventions=18,
                    false_interventions=9,
                    missed_interventions=1,
                    correct_non_interventions=2,
                    accuracy=0.667,
                    precision=0.667,
                    recall=0.947,
                    false_intervention_rate=0.818,
                    missed_intervention_rate=0.053,
                    autonomy_availability=0.100,
                ),
                ExperimentMetric(
                    policy="Composed Contract",
                    conditions=30,
                    true_interventions=19,
                    false_interventions=3,
                    missed_interventions=0,
                    correct_non_interventions=8,
                    accuracy=0.900,
                    precision=0.864,
                    recall=1.000,
                    false_intervention_rate=0.273,
                    missed_intervention_rate=0.000,
                    autonomy_availability=0.267,
                ),
                ExperimentMetric(
                    policy="DARA-DT",
                    conditions=30,
                    true_interventions=19,
                    false_interventions=3,
                    missed_interventions=0,
                    correct_non_interventions=8,
                    accuracy=0.900,
                    precision=0.864,
                    recall=1.000,
                    false_intervention_rate=0.273,
                    missed_intervention_rate=0.000,
                    autonomy_availability=0.267,
                ),
            ],
            finding=(
                "Within the frozen EXP-010 matrix, propagation-aware "
                "DARA-DT and the dependency-aware composed runtime "
                "contract produced identical binary outcomes and "
                "authority selections across all 30 conditions."
            ),
        )

    def completed_experiments(self) -> list[str]:
        """Return identifiers for the completed experimental programme."""
        return [
            "EXP-001",
            "EXP-002",
            "EXP-003",
            "EXP-004",
            "EXP-005",
            "EXP-006",
            "EXP-007",
            "EXP-008",
            "EXP-009",
            "EXP-010",
        ]


research_service = ResearchService()
