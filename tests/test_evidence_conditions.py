"""Tests for the EXP-006 controlled evidence-condition matrix."""

import pytest

from dara_dt.experiments.evidence_conditions import (
    EvidenceConditionType,
    build_evidence_conditions,
)


def _conditions_by_id():
    """Return EXP-006 conditions indexed by identifier."""

    return {
        condition.condition_id: condition
        for condition in build_evidence_conditions()
    }


def test_builds_twelve_controlled_conditions() -> None:
    """EXP-006 should contain twelve controlled evidence conditions."""

    conditions = build_evidence_conditions()

    assert len(conditions) == 12


def test_condition_ids_are_unique() -> None:
    """Every experimental condition must have a unique identifier."""

    conditions = build_evidence_conditions()

    ids = [condition.condition_id for condition in conditions]

    assert len(ids) == len(set(ids))


def test_e0_contains_accurate_invalid_evidence() -> None:
    """E0 should expose the true invalid physical capacity."""

    condition = _conditions_by_id()["E0"]

    assert condition.evidence_type == EvidenceConditionType.ACCURATE
    assert condition.physical_capacity == 6
    assert condition.observed_capacity == 6
    assert condition.demand == 8
    assert condition.physical_valid is False


def test_e1_error_does_not_change_invalid_classification() -> None:
    """E1 should remain below the decision-validity boundary."""

    condition = _conditions_by_id()["E1"]

    assert condition.physical_valid is False
    assert condition.observed_capacity == 7
    assert condition.observed_capacity < condition.demand
    assert condition.evidence_error == pytest.approx(1.0)


def test_e2_moves_observation_to_boundary() -> None:
    """E2 should move the observed value exactly to the demand boundary."""

    condition = _conditions_by_id()["E2"]

    assert condition.physical_valid is False
    assert condition.observed_capacity == condition.demand
    assert condition.evidence_error == pytest.approx(2.0)


def test_e3_makes_invalid_decision_appear_valid() -> None:
    """E3 should demonstrate a validity-flipping observation error."""

    condition = _conditions_by_id()["E3"]

    assert condition.physical_valid is False
    assert condition.observed_capacity > condition.demand
    assert condition.evidence_error == pytest.approx(3.0)


def test_e4_is_stale_and_hides_physical_invalidity() -> None:
    """E4 should contain old evidence that appears safe."""

    condition = _conditions_by_id()["E4"]

    assert condition.evidence_type == EvidenceConditionType.STALE
    assert condition.physical_valid is False
    assert condition.observed_capacity > condition.demand
    assert condition.evidence_age == pytest.approx(8.0)


def test_e5_contains_missing_evidence() -> None:
    """E5 should contain no runtime capacity observation."""

    condition = _conditions_by_id()["E5"]

    assert condition.evidence_type == EvidenceConditionType.MISSING
    assert condition.observed_capacity is None
    assert condition.evidence_error is None


def test_e6_contains_conflicting_observations() -> None:
    """E6 should contain observations on opposite sides of the boundary."""

    condition = _conditions_by_id()["E6"]

    assert condition.evidence_type == EvidenceConditionType.CONFLICTING
    assert condition.observed_capacity < condition.demand
    assert condition.secondary_observed_capacity > condition.demand


def test_e7_is_physically_valid_with_accurate_evidence() -> None:
    """E7 should provide a valid-decision control condition."""

    condition = _conditions_by_id()["E7"]

    assert condition.evidence_type == EvidenceConditionType.ACCURATE
    assert condition.physical_valid is True
    assert condition.observed_capacity == condition.physical_capacity


def test_e8_makes_valid_decision_appear_invalid() -> None:
    """E8 should expose the false-intervention risk from noisy evidence."""

    condition = _conditions_by_id()["E8"]

    assert condition.physical_valid is True
    assert condition.observed_capacity < condition.demand
    assert condition.evidence_error == pytest.approx(-2.0)


def test_e9_preserves_validity_with_larger_margin() -> None:
    """E9 should remain safe despite observation error."""

    condition = _conditions_by_id()["E9"]

    assert condition.physical_margin == pytest.approx(4.0)
    assert condition.physical_valid is True
    assert condition.observed_capacity > condition.demand


def test_e10_same_positive_error_can_hide_invalidity() -> None:
    """E10 should show that error meaning depends on decision margin."""

    condition = _conditions_by_id()["E10"]

    assert condition.physical_valid is False
    assert condition.evidence_error == pytest.approx(1.0)
    assert condition.observed_capacity == condition.demand


def test_e1_and_e10_have_same_error_but_different_boundary_effect() -> None:
    """Equal evidence error should have decision-specific consequences."""

    conditions = _conditions_by_id()

    e1 = conditions["E1"]
    e10 = conditions["E10"]

    assert e1.evidence_error == pytest.approx(e10.evidence_error)
    assert e1.observed_capacity < e1.demand
    assert e10.observed_capacity == e10.demand


def test_e11_is_old_evidence_matching_twin_not_physical_state() -> None:
    """E11 should model stale evidence that agrees with the Twin."""

    condition = _conditions_by_id()["E11"]

    assert condition.evidence_type == EvidenceConditionType.STALE
    assert condition.physical_valid is False
    assert condition.observed_capacity == condition.twin_capacity
    assert condition.observed_capacity != condition.physical_capacity
    assert condition.evidence_age == pytest.approx(9.0)


def test_physical_validity_is_independent_of_runtime_evidence() -> None:
    """Ground-truth validity must depend on physical state, not evidence."""

    conditions = _conditions_by_id()

    e3 = conditions["E3"]
    e8 = conditions["E8"]

    # E3 looks valid from evidence but is invalid in reality.
    assert e3.observed_capacity >= e3.demand
    assert e3.physical_valid is False

    # E8 looks invalid from evidence but is valid in reality.
    assert e8.observed_capacity < e8.demand
    assert e8.physical_valid is True


def test_all_evidence_ages_are_non_negative() -> None:
    """No observation may originate in the future."""

    for condition in build_evidence_conditions():
        assert condition.evidence_age >= 0
