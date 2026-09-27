"""Tests for the DARA-DT decision-impact data model."""

from dara_dt.impact.model import (
    DecisionImpact,
    ImpactEvidence,
    ImpactState,
)


def test_impact_evidence_preserves_runtime_observation() -> None:
    """Runtime evidence should preserve its source and observed values."""

    evidence = ImpactEvidence(
        source="vehicle_sensor",
        variable="capacity",
        observed_value=7,
        twin_value=10,
    )

    assert evidence.source == "vehicle_sensor"
    assert evidence.variable == "capacity"
    assert evidence.observed_value == 7
    assert evidence.twin_value == 10


def test_margin_reduced_impact_is_not_invalidating() -> None:
    """A reduced margin should not automatically invalidate a decision."""

    impact = DecisionImpact(
        decision_id="decision_001",
        dependency="vehicle.capacity",
        impact_state=ImpactState.MARGIN_REDUCED,
        estimated_margin=2.0,
        evidence=(),
        reason="Capacity margin remains positive.",
    )

    assert impact.invalidating is False
    assert impact.uncertain is False
    assert impact.requires_attention is False


def test_boundary_impact_requires_attention() -> None:
    """A decision at its validity boundary should require attention."""

    impact = DecisionImpact(
        decision_id="decision_002",
        dependency="vehicle.capacity",
        impact_state=ImpactState.BOUNDARY,
        estimated_margin=0.0,
        evidence=(),
        reason="Capacity equals required demand.",
    )

    assert impact.invalidating is False
    assert impact.uncertain is False
    assert impact.requires_attention is True


def test_invalidating_impact_is_identified() -> None:
    """Negative decision margin should be representable as invalidating."""

    impact = DecisionImpact(
        decision_id="decision_003",
        dependency="vehicle.capacity",
        impact_state=ImpactState.INVALIDATING,
        estimated_margin=-1.0,
        evidence=(),
        reason="Observed capacity is below required demand.",
    )

    assert impact.invalidating is True
    assert impact.uncertain is False
    assert impact.requires_attention is True


def test_uncertain_impact_requires_attention() -> None:
    """Insufficient runtime evidence should remain explicitly uncertain."""

    impact = DecisionImpact(
        decision_id="decision_004",
        dependency="vehicle.status",
        impact_state=ImpactState.UNCERTAIN,
        estimated_margin=None,
        evidence=(),
        reason="Runtime evidence is insufficient.",
    )

    assert impact.invalidating is False
    assert impact.uncertain is True
    assert impact.requires_attention is True


def test_non_numeric_dependency_can_omit_margin() -> None:
    """Impact representation should support non-numeric dependencies."""

    evidence = ImpactEvidence(
        source="operations_monitor",
        variable="status",
        observed_value="broken_down",
        twin_value="operational",
    )

    impact = DecisionImpact(
        decision_id="decision_005",
        dependency="vehicle.status",
        impact_state=ImpactState.INVALIDATING,
        estimated_margin=None,
        evidence=(evidence,),
        reason="Selected vehicle is no longer operational.",
    )

    assert impact.estimated_margin is None
    assert impact.evidence == (evidence,)
    assert impact.invalidating is True
