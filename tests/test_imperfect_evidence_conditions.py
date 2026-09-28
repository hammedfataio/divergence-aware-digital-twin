"""Tests for the controlled EXP-008 imperfect-evidence matrix."""

import pytest

from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.cross_dependency_conditions import DependencyFamily
from dara_dt.experiments.imperfect_evidence_conditions import (
    EvidenceScenario,
    ImperfectEvidenceCondition,
    build_imperfect_evidence_conditions,
)


@pytest.fixture
def conditions() -> tuple[ImperfectEvidenceCondition, ...]:
    """Return the complete EXP-008 condition matrix."""

    return build_imperfect_evidence_conditions()


def condition_by_id(
    conditions: tuple[ImperfectEvidenceCondition, ...],
    condition_id: str,
) -> ImperfectEvidenceCondition:
    """Return one condition by its stable experimental identifier."""

    matches = [
        condition
        for condition in conditions
        if condition.condition_id == condition_id
    ]

    assert len(matches) == 1
    return matches[0]


def test_matrix_contains_exactly_24_conditions(conditions):
    """EXP-008 must contain the pre-registered 24-condition matrix."""

    assert len(conditions) == 24


def test_condition_ids_are_unique(conditions):
    """Every experimental condition must have a unique identifier."""

    condition_ids = [condition.condition_id for condition in conditions]

    assert len(condition_ids) == len(set(condition_ids))


@pytest.mark.parametrize(
    ("family", "expected_count"),
    [
        (DependencyFamily.CAPACITY, 8),
        (DependencyFamily.STATUS, 8),
        (DependencyFamily.LOCATION_AVAILABILITY, 8),
    ],
)
def test_each_dependency_family_contains_eight_conditions(
    conditions,
    family,
    expected_count,
):
    """Each dependency family must contain eight evidence conditions."""

    family_conditions = [
        condition
        for condition in conditions
        if condition.family == family
    ]

    assert len(family_conditions) == expected_count


@pytest.mark.parametrize(
    ("scenario", "expected_count"),
    [
        (EvidenceScenario.RELIABLE, 6),
        (EvidenceScenario.STALE, 6),
        (EvidenceScenario.MISSING, 6),
        (EvidenceScenario.CONFLICTING, 6),
    ],
)
def test_each_evidence_scenario_contains_six_conditions(
    conditions,
    scenario,
    expected_count,
):
    """Each evidence scenario must occur twice per dependency family."""

    scenario_conditions = [
        condition
        for condition in conditions
        if condition.evidence_scenario == scenario
    ]

    assert len(scenario_conditions) == expected_count


@pytest.mark.parametrize(
    ("scenario", "expected_status"),
    [
        (EvidenceScenario.RELIABLE, EvidenceStatus.AVAILABLE),
        (EvidenceScenario.STALE, EvidenceStatus.STALE),
        (EvidenceScenario.MISSING, EvidenceStatus.MISSING),
        (EvidenceScenario.CONFLICTING, EvidenceStatus.CONFLICTING),
    ],
)
def test_evidence_scenario_maps_to_expected_status(
    scenario,
    expected_status,
):
    """Experimental evidence scenarios must map to runtime evidence status."""

    condition = ImperfectEvidenceCondition(
        condition_id="TEST",
        family=DependencyFamily.CAPACITY,
        evidence_scenario=scenario,
        description="test condition",
        twin_value=10.0,
        physical_value=8.0,
        primary_evidence_value=8.0,
    )

    assert condition.evidence_status == expected_status


def test_reliable_conditions_have_primary_evidence(conditions):
    """Reliable conditions must contain a runtime observation."""

    reliable_conditions = [
        condition
        for condition in conditions
        if condition.evidence_scenario == EvidenceScenario.RELIABLE
    ]

    assert reliable_conditions

    for condition in reliable_conditions:
        assert condition.has_primary_evidence
        assert condition.primary_evidence_value is not None


def test_missing_conditions_have_no_primary_or_secondary_evidence(
    conditions,
):
    """Missing-evidence conditions must not accidentally contain evidence."""

    missing_conditions = [
        condition
        for condition in conditions
        if condition.evidence_scenario == EvidenceScenario.MISSING
    ]

    assert missing_conditions

    for condition in missing_conditions:
        assert condition.primary_evidence_value is None
        assert condition.secondary_evidence_value is None
        assert not condition.has_primary_evidence
        assert not condition.has_secondary_evidence


def test_conflicting_conditions_have_two_distinct_observations(
    conditions,
):
    """Conflicting conditions must contain incompatible evidence sources."""

    conflicting_conditions = [
        condition
        for condition in conditions
        if condition.evidence_scenario == EvidenceScenario.CONFLICTING
    ]

    assert conflicting_conditions

    for condition in conflicting_conditions:
        assert condition.has_primary_evidence
        assert condition.has_secondary_evidence
        assert condition.has_conflicting_evidence
        assert (
            condition.primary_evidence_value
            != condition.secondary_evidence_value
        )


def test_non_conflicting_conditions_are_not_marked_conflicting(
    conditions,
):
    """Only pre-registered conflicting scenarios may report conflict."""

    non_conflicting_conditions = [
        condition
        for condition in conditions
        if condition.evidence_scenario != EvidenceScenario.CONFLICTING
    ]

    for condition in non_conflicting_conditions:
        assert not condition.has_conflicting_evidence


def test_stale_conditions_have_positive_evidence_age(conditions):
    """Stale observations must pre-date the assurance evaluation."""

    stale_conditions = [
        condition
        for condition in conditions
        if condition.evidence_scenario == EvidenceScenario.STALE
    ]

    assert stale_conditions

    for condition in stale_conditions:
        assert condition.evidence_age > 0
        assert condition.observation_timestamp < condition.evaluation_timestamp


def test_reliable_conditions_have_zero_evidence_age(conditions):
    """Reliable control observations are current at evaluation time."""

    reliable_conditions = [
        condition
        for condition in conditions
        if condition.evidence_scenario == EvidenceScenario.RELIABLE
    ]

    for condition in reliable_conditions:
        assert condition.evidence_age == 0


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-R0",
        "CAP-R1",
        "CAP-S0",
        "CAP-S1",
        "CAP-M0",
        "CAP-M1",
        "CAP-C0",
        "CAP-C1",
    ],
)
def test_capacity_condition_ids_exist(conditions, condition_id):
    """All eight capacity conditions must exist."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.family == DependencyFamily.CAPACITY


@pytest.mark.parametrize(
    "condition_id",
    [
        "STATUS-R0",
        "STATUS-R1",
        "STATUS-S0",
        "STATUS-S1",
        "STATUS-M0",
        "STATUS-M1",
        "STATUS-C0",
        "STATUS-C1",
    ],
)
def test_status_condition_ids_exist(conditions, condition_id):
    """All eight operational-status conditions must exist."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.family == DependencyFamily.STATUS


@pytest.mark.parametrize(
    "condition_id",
    [
        "LOC-R0",
        "LOC-R1",
        "LOC-S0",
        "LOC-S1",
        "LOC-M0",
        "LOC-M1",
        "LOC-C0",
        "LOC-C1",
    ],
)
def test_location_availability_condition_ids_exist(
    conditions,
    condition_id,
):
    """All eight location/availability conditions must exist."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.family == DependencyFamily.LOCATION_AVAILABILITY


@pytest.mark.parametrize(
    ("condition_id", "expected_physical", "expected_evidence"),
    [
        ("CAP-R0", 8.0, 8.0),
        ("CAP-R1", 4.0, 4.0),
        ("CAP-S0", 8.0, 4.0),
        ("CAP-S1", 4.0, 8.0),
    ],
)
def test_capacity_reliable_and_stale_semantics(
    conditions,
    condition_id,
    expected_physical,
    expected_evidence,
):
    """Capacity controls must preserve the intended physical/evidence split."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.physical_value == expected_physical
    assert condition.primary_evidence_value == expected_evidence
    assert condition.order_demand == 5.0


@pytest.mark.parametrize(
    ("condition_id", "expected_physical", "expected_evidence"),
    [
        ("STATUS-R0", "operational", "operational"),
        ("STATUS-R1", "broken_down", "broken_down"),
        ("STATUS-S0", "operational", "broken_down"),
        ("STATUS-S1", "broken_down", "operational"),
    ],
)
def test_status_reliable_and_stale_semantics(
    conditions,
    condition_id,
    expected_physical,
    expected_evidence,
):
    """Status controls must preserve the intended physical/evidence split."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.physical_value == expected_physical
    assert condition.primary_evidence_value == expected_evidence
    assert condition.required_status == "operational"


@pytest.mark.parametrize(
    ("condition_id", "expected_physical", "expected_evidence"),
    [
        (
            "LOC-R0",
            ("near_depot", True),
            ("near_depot", True),
        ),
        (
            "LOC-R1",
            ("remote_site", False),
            ("remote_site", False),
        ),
        (
            "LOC-S0",
            ("near_depot", True),
            ("remote_site", False),
        ),
        (
            "LOC-S1",
            ("remote_site", False),
            ("depot", True),
        ),
    ],
)
def test_location_reliable_and_stale_semantics(
    conditions,
    condition_id,
    expected_physical,
    expected_evidence,
):
    """Location controls must preserve the physical/evidence split."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.physical_value == expected_physical
    assert condition.primary_evidence_value == expected_evidence


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-S0",
        "STATUS-S0",
        "LOC-S0",
    ],
)
def test_stale_zero_conditions_are_physically_valid_but_evidence_is_adverse(
    conditions,
    condition_id,
):
    """S0 conditions intentionally contain misleading adverse stale evidence."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.evidence_scenario == EvidenceScenario.STALE
    assert condition.primary_evidence_value != condition.physical_value


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-S1",
        "STATUS-S1",
        "LOC-S1",
    ],
)
def test_stale_one_conditions_hide_physical_invalidity(
    conditions,
    condition_id,
):
    """S1 conditions intentionally contain stale evidence hiding invalidity."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.evidence_scenario == EvidenceScenario.STALE
    assert condition.primary_evidence_value != condition.physical_value


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-M0",
        "CAP-M1",
        "STATUS-M0",
        "STATUS-M1",
        "LOC-M0",
        "LOC-M1",
    ],
)
def test_missing_conditions_expose_no_runtime_value(
    conditions,
    condition_id,
):
    """Missing conditions must not expose physical truth through evidence."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.evidence_status == EvidenceStatus.MISSING
    assert condition.primary_evidence_value is None
    assert condition.secondary_evidence_value is None


@pytest.mark.parametrize(
    "condition_id",
    [
        "CAP-C0",
        "CAP-C1",
        "STATUS-C0",
        "STATUS-C1",
        "LOC-C0",
        "LOC-C1",
    ],
)
def test_conflicting_conditions_expose_two_incompatible_values(
    conditions,
    condition_id,
):
    """Conflicting conditions must preserve genuine observation disagreement."""

    condition = condition_by_id(conditions, condition_id)

    assert condition.evidence_status == EvidenceStatus.CONFLICTING
    assert condition.primary_evidence_value is not None
    assert condition.secondary_evidence_value is not None
    assert (
        condition.primary_evidence_value
        != condition.secondary_evidence_value
    )


def test_capacity_valid_invalid_pairs_share_same_requirement(conditions):
    """Capacity validity pairs must use the same demand requirement."""

    pairs = (
        ("CAP-R0", "CAP-R1"),
        ("CAP-S0", "CAP-S1"),
        ("CAP-M0", "CAP-M1"),
        ("CAP-C0", "CAP-C1"),
    )

    for valid_id, invalid_id in pairs:
        valid = condition_by_id(conditions, valid_id)
        invalid = condition_by_id(conditions, invalid_id)

        assert valid.order_demand == invalid.order_demand == 5.0
        assert valid.physical_value >= valid.order_demand
        assert invalid.physical_value < invalid.order_demand


def test_status_valid_invalid_pairs_share_same_requirement(conditions):
    """Status pairs must use the same operational requirement."""

    pairs = (
        ("STATUS-R0", "STATUS-R1"),
        ("STATUS-S0", "STATUS-S1"),
        ("STATUS-M0", "STATUS-M1"),
        ("STATUS-C0", "STATUS-C1"),
    )

    for valid_id, invalid_id in pairs:
        valid = condition_by_id(conditions, valid_id)
        invalid = condition_by_id(conditions, invalid_id)

        assert valid.required_status == invalid.required_status == "operational"
        assert valid.physical_value == "operational"
        assert invalid.physical_value != "operational"


def test_location_valid_invalid_pairs_share_same_requirement(conditions):
    """Location/availability pairs must use identical dispatch requirements."""

    pairs = (
        ("LOC-R0", "LOC-R1"),
        ("LOC-S0", "LOC-S1"),
        ("LOC-M0", "LOC-M1"),
        ("LOC-C0", "LOC-C1"),
    )

    for valid_id, invalid_id in pairs:
        valid = condition_by_id(conditions, valid_id)
        invalid = condition_by_id(conditions, invalid_id)

        assert valid.permitted_locations == invalid.permitted_locations
        assert valid.required_available == invalid.required_available is True

        valid_location, valid_available = valid.physical_value
        invalid_location, invalid_available = invalid.physical_value

        assert valid_location in valid.permitted_locations
        assert valid_available is True

        assert (
            invalid_location not in invalid.permitted_locations
            or invalid_available is False
        )


def test_matrix_contains_expected_complete_id_set(conditions):
    """Lock the exact pre-registered EXP-008 condition identifiers."""

    expected_ids = {
        "CAP-R0",
        "CAP-R1",
        "CAP-S0",
        "CAP-S1",
        "CAP-M0",
        "CAP-M1",
        "CAP-C0",
        "CAP-C1",
        "STATUS-R0",
        "STATUS-R1",
        "STATUS-S0",
        "STATUS-S1",
        "STATUS-M0",
        "STATUS-M1",
        "STATUS-C0",
        "STATUS-C1",
        "LOC-R0",
        "LOC-R1",
        "LOC-S0",
        "LOC-S1",
        "LOC-M0",
        "LOC-M1",
        "LOC-C0",
        "LOC-C1",
    }

    actual_ids = {
        condition.condition_id
        for condition in conditions
    }

    assert actual_ids == expected_ids
