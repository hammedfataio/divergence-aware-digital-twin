"""Tests for the EXP-006 controlled runtime evidence generator."""

import pytest

from dara_dt.evidence.generator import EvidenceGenerator
from dara_dt.evidence.model import EvidenceStatus


def test_accurate_evidence_matches_physical_value() -> None:
    """Accurate evidence should reproduce the physical observation."""

    generator = EvidenceGenerator()

    evidence = generator.accurate(
        dependency="vehicle.capacity",
        physical_value=6,
        timestamp=5.0,
    )

    assert evidence.observed_value == 6
    assert evidence.status == EvidenceStatus.AVAILABLE
    assert evidence.confidence == pytest.approx(1.0)


def test_noisy_evidence_applies_positive_error() -> None:
    """Positive observation error should increase the reported value."""

    generator = EvidenceGenerator()

    evidence = generator.noisy(
        dependency="vehicle.capacity",
        physical_value=6,
        error=2,
        timestamp=5.0,
    )

    assert evidence.observed_value == 8
    assert evidence.status == EvidenceStatus.AVAILABLE


def test_noisy_evidence_applies_negative_error() -> None:
    """Negative observation error should reduce the reported value."""

    generator = EvidenceGenerator()

    evidence = generator.noisy(
        dependency="vehicle.capacity",
        physical_value=8,
        error=-2,
        timestamp=5.0,
    )

    assert evidence.observed_value == 6


def test_noisy_evidence_does_not_modify_physical_input() -> None:
    """Evidence corruption must not alter the physical ground-truth value."""

    generator = EvidenceGenerator()
    physical_value = 6

    evidence = generator.noisy(
        dependency="vehicle.capacity",
        physical_value=physical_value,
        error=3,
        timestamp=5.0,
    )

    assert physical_value == 6
    assert evidence.observed_value == 9


def test_noisy_evidence_preserves_confidence() -> None:
    """Explicit evidence confidence should be preserved."""

    generator = EvidenceGenerator()

    evidence = generator.noisy(
        dependency="vehicle.capacity",
        physical_value=6,
        error=1,
        timestamp=5.0,
        confidence=0.8,
    )

    assert evidence.confidence == pytest.approx(0.8)


def test_stale_evidence_preserves_old_observation() -> None:
    """Stale evidence should preserve its earlier observed value."""

    generator = EvidenceGenerator()

    evidence = generator.stale(
        dependency="vehicle.capacity",
        stale_value=10,
        observation_timestamp=2.0,
    )

    assert evidence.observed_value == 10
    assert evidence.timestamp == pytest.approx(2.0)
    assert evidence.status == EvidenceStatus.STALE


def test_stale_evidence_age_can_be_calculated() -> None:
    """The evidence model should expose the age of stale observations."""

    generator = EvidenceGenerator()

    evidence = generator.stale(
        dependency="vehicle.capacity",
        stale_value=10,
        observation_timestamp=2.0,
    )

    assert evidence.age_at(8.0) == pytest.approx(6.0)


def test_missing_evidence_contains_no_value() -> None:
    """Missing evidence should contain no fabricated observation."""

    generator = EvidenceGenerator()

    evidence = generator.missing(
        dependency="vehicle.capacity",
        timestamp=5.0,
    )

    assert evidence.observed_value is None
    assert evidence.status == EvidenceStatus.MISSING
    assert evidence.is_available is False


def test_conflicting_evidence_contains_two_sources() -> None:
    """Conflicting evidence should preserve both observations."""

    generator = EvidenceGenerator()

    first, second = generator.conflicting(
        dependency="vehicle.capacity",
        first_value=6,
        second_value=9,
        timestamp=5.0,
    )

    assert first.observed_value == 6
    assert second.observed_value == 9
    assert first.source != second.source


def test_conflicting_evidence_has_explicit_status() -> None:
    """Both conflicting observations should be marked as conflicting."""

    generator = EvidenceGenerator()

    first, second = generator.conflicting(
        dependency="vehicle.capacity",
        first_value=6,
        second_value=9,
        timestamp=5.0,
    )

    assert first.status == EvidenceStatus.CONFLICTING
    assert second.status == EvidenceStatus.CONFLICTING


def test_conflicting_evidence_uses_same_dependency() -> None:
    """Conflicting observations must refer to the same dependency."""

    generator = EvidenceGenerator()

    first, second = generator.conflicting(
        dependency="vehicle.capacity",
        first_value=6,
        second_value=9,
        timestamp=5.0,
    )

    assert first.dependency == "vehicle.capacity"
    assert second.dependency == "vehicle.capacity"


def test_equal_values_cannot_be_marked_conflicting() -> None:
    """Identical observations do not constitute a conflict."""

    generator = EvidenceGenerator()

    with pytest.raises(
        ValueError,
        match="requires different observed values",
    ):
        generator.conflicting(
            dependency="vehicle.capacity",
            first_value=6,
            second_value=6,
            timestamp=5.0,
        )


def test_non_numeric_physical_value_is_rejected_for_noise() -> None:
    """Controlled numeric noise requires a numeric physical value."""

    generator = EvidenceGenerator()

    with pytest.raises(
        TypeError,
        match="Physical value must be numeric",
    ):
        generator.noisy(
            dependency="vehicle.capacity",
            physical_value="six",
            error=1,
            timestamp=5.0,
        )


def test_non_numeric_noise_error_is_rejected() -> None:
    """Controlled observation error must be numeric."""

    generator = EvidenceGenerator()

    with pytest.raises(
        TypeError,
        match="Evidence error must be numeric",
    ):
        generator.noisy(
            dependency="vehicle.capacity",
            physical_value=6,
            error="one",
            timestamp=5.0,
        )
