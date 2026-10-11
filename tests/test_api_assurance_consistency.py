"""API-level assurance consistency checks for frozen EXP-010 scenarios."""

import pytest
from fastapi.testclient import TestClient

from dara_dt.api.app import app


client = TestClient(app)


@pytest.mark.parametrize(
    "scenario_id,expected_authority,expected_intervention",
    [
        ("F0-A", "allow", False),
        ("F1-A", "restrict", True),
        ("F2-A", "allow", False),
        ("F3-A", "restrict", True),
        ("F4-A", "restrict", True),
    ],
)
def test_exp010_api_assurance_consistency(
    scenario_id: str,
    expected_authority: str,
    expected_intervention: bool,
) -> None:
    """Verify real API results against frozen scenario expectations."""

    response = client.post(f"/api/scenarios/{scenario_id}/run")

    assert response.status_code == 200, response.text

    payload = response.json()

    assert payload["scenario_id"] == scenario_id

    dara_results = [
        result
        for result in payload["assurance_results"]
        if "dara" in result["policy"].lower()
    ]

    assert len(dara_results) == 1, (
        f"Expected exactly one DARA-DT result for {scenario_id}"
    )

    assurance = dara_results[0]

    assert assurance["authority"] == expected_authority
    assert assurance["intervene"] is expected_intervention

    assert (
        payload["ground_truth"]["intervention_required"]
        is expected_intervention
    )
