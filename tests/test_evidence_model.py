"""Tests for the EXP-006 runtime evidence model."""

import pytest

from dara_dt.evidence.model import (
    EvidenceStatus,
    RuntimeEvidence,
)


def test_available_evidence_preserves_observation() -> None:
    """Available evidence should preserve its runtime observation."""

    evidence = RuntimeEvidence(
        source="capacity_sensor",
        dependency="vehicle.capacity",
        observed_value=8,
        timestamp=2.0,
    )

    assert evidence.source == "capacity_sensor"
    assert evidence.dependency == "vehicle.capacity"
    assert evidence.observed_value == 8
    assert evidence.timestamp == 2.0
    assert evidence.status == EvidenceStatus.AVAILABLE
    assert evidence.is_available is True


def test_missing_evidence_has_no_observed_value() -> None:
    """Missing evidence should explicitly contain no observation."""

    evidence = RuntimeEvidence(
        source="capacity_sensor",
        dependency="vehicle.capacity",
        observed_value=None,
        timestamp=2.0,
        status=EvidenceStatus.MISSING,
    )

    assert evidence.observed_value is None
    assert evidence.status == EvidenceStatus.MISSING
    assert evidence.is_available is False


def test_stale_evidence_remains_observable() -> None:
    """Stale evidence may contain a value even though it is outdated."""

    evidence = RuntimeEvidence(
        source="capacity_sensor",
        dependency="vehicle.capacity",
        observed_value=10,
        timestamp=1.0,
        status=EvidenceStatus.STALE,
    )

    assert evidence.observed_value == 10
    assert evidence.status == EvidenceStatus.STALE
    assert evidence.is_available is True


def test_conflicting_evidence_remains_observable() -> None:
    """Conflicting evidence should preserve the reported value."""

    evidence = RuntimeEvidence(
        source="sensor_a",
        dependency="vehicle.capacity",
        observed_value=7,
        timestamp=3.0,
        status=EvidenceStatus.CONFLICTING,
    )

    assert evidence.status == EvidenceStatus.CONFLICTING
    assert evidence.is_available is True


def test_evidence_age_is_calculated() -> None:
    """Evidence age should be calculated from simulation time."""

    evidence = RuntimeEvidence(
        source="capacity_sensor",
        dependency="vehicle.capacity",
        observed_value=8,
        timestamp=4.0,
    )

    assert evidence.age_at(10.0) == pytest.approx(6.0)


def test_future_evidence_timestamp_is_rejected() -> None:
    """Evidence cannot be evaluated before it was produced."""

    evidence = RuntimeEvidence(
        source="capacity_sensor",
        dependency="vehicle.capacity",
        observed_value=8,
        timestamp=10.0,
    )

    with pytest.raises(
        ValueError,
        match="Current time must not precede",
    ):
        evidence.age_at(5.0)


def test_negative_timestamp_is_rejected() -> None:
    """Evidence timestamps must not be negative."""

    with pytest.raises(
        ValueError,
        match="timestamp must not be negative",
    ):
        RuntimeEvidence(
            source="capacity_sensor",
            dependency="vehicle.capacity",
            observed_value=8,
            timestamp=-1.0,
        )


def test_confidence_must_not_exceed_one() -> None:
    """Confidence values above one should be rejected."""

    with pytest.raises(
        ValueError,
        match="confidence must be between 0 and 1",
    ):
        RuntimeEvidence(
            source="capacity_sensor",
            dependency="vehicle.capacity",
            observed_value=8,
            timestamp=1.0,
            confidence=1.1,
        )


def test_confidence_must_not_be_negative() -> None:
    """Negative confidence values should be rejected."""

    with pytest.raises(
        ValueError,
        match="confidence must be between 0 and 1",
    ):
        RuntimeEvidence(
            source="capacity_sensor",
            dependency="vehicle.capacity",
            observed_value=8,
            timestamp=1.0,
            confidence=-0.1,
        )


def test_valid_confidence_is_preserved() -> None:
    """A valid confidence value should be preserved."""

    evidence = RuntimeEvidence(
        source="capacity_sensor",
        dependency="vehicle.capacity",
        observed_value=8,
        timestamp=1.0,
        confidence=0.85,
    )

    assert evidence.confidence == pytest.approx(0.85)


def test_missing_evidence_cannot_contain_value() -> None:
    """Missing evidence must not silently contain an observation."""

    with pytest.raises(
        ValueError,
        match="Missing evidence must not contain",
    ):
        RuntimeEvidence(
            source="capacity_sensor",
            dependency="vehicle.capacity",
            observed_value=8,
            timestamp=1.0,
            status=EvidenceStatus.MISSING,
        )


def test_non_missing_evidence_requires_value() -> None:
    """Non-missing evidence must contain an observation."""

    with pytest.raises(
        ValueError,
        match="Available evidence must contain",
    ):
        RuntimeEvidence(
            source="capacity_sensor",
            dependency="vehicle.capacity",
            observed_value=None,
            timestamp=1.0,
            status=EvidenceStatus.AVAILABLE,
        )


def test_empty_source_is_rejected() -> None:
    """Evidence source identifiers must not be empty."""

    with pytest.raises(
        ValueError,
        match="source must not be empty",
    ):
        RuntimeEvidence(
            source="",
            dependency="vehicle.capacity",
            observed_value=8,
            timestamp=1.0,
        )


def test_empty_dependency_is_rejected() -> None:
    """Evidence dependency identifiers must not be empty."""

    with pytest.raises(
        ValueError,
        match="dependency must not be empty",
    ):
        RuntimeEvidence(
            source="capacity_sensor",
            dependency="",
            observed_value=8,
            timestamp=1.0,
        )
