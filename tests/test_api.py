"""Tests for the DARA-DT FastAPI research application.

These tests verify the public API boundary without modifying or rerunning
the frozen EXP-001 to EXP-010 experimental programme.
"""

from fastapi.testclient import TestClient

from dara_dt.api.app import app


client = TestClient(app)


def test_root() -> None:
    """The API root should identify the DARA-DT research service."""

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "DARA-DT"
    assert data["service"] == "Research API"
    assert data["status"] == "running"


def test_health() -> None:
    """The health endpoint should report a healthy API service."""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "status": "ok",
        "service": "DARA-DT Research API",
        "version": "0.1.0",
    }


def test_project_status() -> None:
    """Project status should expose the frozen research programme state."""

    response = client.get("/api/project/status")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "DARA-DT"

    assert (
        data["full_name"]
        == "Divergence-Aware Runtime Assurance for Digital Twins"
    )

    assert data["research_domain"] == "Trustworthy Intelligent Systems"

    assert (
        data["experimental_domain"]
        == "Autonomous Logistics Digital Twins"
    )

    assert data["experiments_completed"] == 10
    assert data["experiments_total"] == 10
    assert data["experimental_programme_complete"] is True
    assert data["contribution_status"] == "frozen"

    assert (
        data["current_stage"]
        == "research demonstrator engineering"
    )


def test_completed_experiments() -> None:
    """The API should expose exactly EXP-001 through EXP-010."""

    response = client.get("/api/experiments")

    assert response.status_code == 200

    data = response.json()

    assert data == [
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


def test_exp010_results() -> None:
    """EXP-010 should expose the verified frozen aggregate results."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    data = response.json()

    assert data["experiment_id"] == "EXP-010"

    assert (
        data["title"]
        == "Propagation-Aware Physical–Digital Divergence"
    )

    assert data["status"] == "complete"
    assert data["conditions"] == 30

    metrics = {
        item["policy"]: item
        for item in data["metrics"]
    }

    assert set(metrics) == {
        "No Assurance",
        "Local Contract",
        "Global Assurance",
        "Composed Contract",
        "DARA-DT",
    }


def test_exp010_no_assurance_metrics() -> None:
    """No Assurance should preserve the verified EXP-010 results."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    metrics = {
        item["policy"]: item
        for item in response.json()["metrics"]
    }

    result = metrics["No Assurance"]

    assert result["conditions"] == 30
    assert result["true_interventions"] == 0
    assert result["false_interventions"] == 0
    assert result["missed_interventions"] == 19
    assert result["correct_non_interventions"] == 11

    assert result["accuracy"] == 0.367
    assert result["precision"] == 0.000
    assert result["recall"] == 0.000

    assert result["false_intervention_rate"] == 0.000
    assert result["missed_intervention_rate"] == 1.000
    assert result["autonomy_availability"] == 1.000


def test_exp010_local_contract_metrics() -> None:
    """Local Contract should preserve the verified EXP-010 results."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    metrics = {
        item["policy"]: item
        for item in response.json()["metrics"]
    }

    result = metrics["Local Contract"]

    assert result["conditions"] == 30
    assert result["true_interventions"] == 8
    assert result["false_interventions"] == 3
    assert result["missed_interventions"] == 11
    assert result["correct_non_interventions"] == 8

    assert result["accuracy"] == 0.533
    assert result["precision"] == 0.727
    assert result["recall"] == 0.421

    assert result["false_intervention_rate"] == 0.273
    assert result["missed_intervention_rate"] == 0.579
    assert result["autonomy_availability"] == 0.633


def test_exp010_global_assurance_metrics() -> None:
    """Global Assurance should preserve the verified EXP-010 results."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    metrics = {
        item["policy"]: item
        for item in response.json()["metrics"]
    }

    result = metrics["Global Assurance"]

    assert result["conditions"] == 30
    assert result["true_interventions"] == 18
    assert result["false_interventions"] == 9
    assert result["missed_interventions"] == 1
    assert result["correct_non_interventions"] == 2

    assert result["accuracy"] == 0.667
    assert result["precision"] == 0.667
    assert result["recall"] == 0.947

    assert result["false_intervention_rate"] == 0.818
    assert result["missed_intervention_rate"] == 0.053
    assert result["autonomy_availability"] == 0.100


def test_exp010_composed_contract_metrics() -> None:
    """Composed Contract should preserve the verified EXP-010 results."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    metrics = {
        item["policy"]: item
        for item in response.json()["metrics"]
    }

    result = metrics["Composed Contract"]

    assert result["conditions"] == 30
    assert result["true_interventions"] == 19
    assert result["false_interventions"] == 3
    assert result["missed_interventions"] == 0
    assert result["correct_non_interventions"] == 8

    assert result["accuracy"] == 0.900
    assert result["precision"] == 0.864
    assert result["recall"] == 1.000

    assert result["false_intervention_rate"] == 0.273
    assert result["missed_intervention_rate"] == 0.000
    assert result["autonomy_availability"] == 0.267


def test_exp010_dara_metrics() -> None:
    """DARA-DT should preserve the verified EXP-010 results."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    metrics = {
        item["policy"]: item
        for item in response.json()["metrics"]
    }

    result = metrics["DARA-DT"]

    assert result["conditions"] == 30
    assert result["true_interventions"] == 19
    assert result["false_interventions"] == 3
    assert result["missed_interventions"] == 0
    assert result["correct_non_interventions"] == 8

    assert result["accuracy"] == 0.900
    assert result["precision"] == 0.864
    assert result["recall"] == 1.000

    assert result["false_intervention_rate"] == 0.273
    assert result["missed_intervention_rate"] == 0.000
    assert result["autonomy_availability"] == 0.267


def test_exp010_composed_contract_and_dara_are_equivalent() -> None:
    """The API must preserve the central EXP-010 equivalence result."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    metrics = {
        item["policy"]: item
        for item in response.json()["metrics"]
    }

    composed = metrics["Composed Contract"]
    dara = metrics["DARA-DT"]

    comparable_fields = [
        "conditions",
        "true_interventions",
        "false_interventions",
        "missed_interventions",
        "correct_non_interventions",
        "accuracy",
        "precision",
        "recall",
        "false_intervention_rate",
        "missed_intervention_rate",
        "autonomy_availability",
    ]

    for field in comparable_fields:
        assert composed[field] == dara[field]


def test_exp010_finding_preserves_negative_result() -> None:
    """The API should not hide the central EXP-010 equivalence finding."""

    response = client.get("/api/experiments/EXP-010/results")

    assert response.status_code == 200

    finding = response.json()["finding"]

    assert finding is not None

    assert "identical" in finding.lower()
    assert "30 conditions" in finding.lower()


def test_lowercase_exp010_route() -> None:
    """The generic experiment route should normalise experiment IDs."""

    response = client.get("/api/experiments/exp-010/results")

    assert response.status_code == 200
    assert response.json()["experiment_id"] == "EXP-010"


def test_unknown_experiment_returns_404() -> None:
    """Unknown experiment identifiers should return HTTP 404."""

    response = client.get("/api/experiments/EXP-999/results")

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Unknown experiment: EXP-999"
    )


def test_unimplemented_completed_experiment_returns_501() -> None:
    """Completed experiments without adapters should return HTTP 501."""

    response = client.get("/api/experiments/EXP-001/results")

    assert response.status_code == 501

    detail = response.json()["detail"]

    assert "EXP-001 is complete" in detail
    assert "adapter" in detail.lower()
