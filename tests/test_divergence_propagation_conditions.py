"""Tests for the frozen EXP-010 divergence-propagation condition matrix."""

from collections import Counter

import pytest

from dara_dt.experiments.divergence_propagation_conditions import (
    EXP010_CONDITIONS,
    PropagationEvidenceStatus,
    PropagationFamily,
    PropagationGroundTruth,
    condition_by_id,
    conditions,
    conditions_for_family,
    validate_condition_matrix,
)


def test_exp010_contains_exactly_30_conditions() -> None:
    """The pre-registered EXP-010 matrix must contain exactly 30 cases."""

    assert len(EXP010_CONDITIONS) == 30
    assert len(conditions()) == 30


def test_condition_identifiers_are_unique() -> None:
    """Every EXP-010 condition must have a unique identifier."""

    identifiers = [
        condition.condition_id
        for condition in EXP010_CONDITIONS
    ]

    assert len(identifiers) == len(set(identifiers))


@pytest.mark.parametrize(
    "family",
    list(PropagationFamily),
)
def test_each_family_contains_exactly_six_conditions(
    family: PropagationFamily,
) -> None:
    """Each frozen family must contain exactly six conditions."""

    family_conditions = conditions_for_family(family)

    assert len(family_conditions) == 6


def test_family_distribution_is_frozen() -> None:
    """The matrix must preserve the 6/6/6/6/6 family distribution."""

    counts = Counter(
        condition.family
        for condition in EXP010_CONDITIONS
    )

    assert counts == {
        PropagationFamily.SYNCHRONISED_CONTROL: 6,
        PropagationFamily.DIRECT_DIVERGENCE: 6,
        PropagationFamily.UPSTREAM_NON_PROPAGATING: 6,
        PropagationFamily.UPSTREAM_PROPAGATING: 6,
        PropagationFamily.COMPOUND_PROPAGATING: 6,
    }


def test_ground_truth_distribution_is_frozen() -> None:
    """EXP-010 must contain 19 intervention and 11 autonomy cases."""

    counts = Counter(
        condition.ground_truth
        for condition in EXP010_CONDITIONS
    )

    assert counts[PropagationGroundTruth.INTERVENE] == 19
    assert (
        counts[PropagationGroundTruth.DO_NOT_INTERVENE]
        == 11
    )


def test_evidence_distribution_is_frozen() -> None:
    """Evidence quality must follow the pre-registered 15/5/5/5 split."""

    counts = Counter(
        condition.evidence_status
        for condition in EXP010_CONDITIONS
    )

    assert counts[PropagationEvidenceStatus.AVAILABLE] == 15
    assert counts[PropagationEvidenceStatus.STALE] == 5
    assert counts[PropagationEvidenceStatus.MISSING] == 5
    assert counts[PropagationEvidenceStatus.CONFLICTING] == 5


def test_f0_contains_no_physical_digital_divergence() -> None:
    """Synchronised controls must not contain physical-digital divergence."""

    family = conditions_for_family(
        PropagationFamily.SYNCHRONISED_CONTROL
    )

    assert all(
        not condition.has_divergence
        for condition in family
    )

    assert all(
        not condition.is_propagating
        for condition in family
    )


def test_f0_contains_exactly_one_invalid_control() -> None:
    """F0 must contain the single pre-registered invalid control."""

    family = conditions_for_family(
        PropagationFamily.SYNCHRONISED_CONTROL
    )

    invalid = [
        condition
        for condition in family
        if condition.intervention_required
    ]

    assert len(invalid) == 1
    assert invalid[0].condition_id == "F0-B"


def test_f1_contains_direct_non_propagating_divergence() -> None:
    """F1 represents direct decision-relevant divergence."""

    family = conditions_for_family(
        PropagationFamily.DIRECT_DIVERGENCE
    )

    assert all(
        condition.has_divergence
        for condition in family
    )

    assert all(
        condition.is_direct_divergence
        for condition in family
    )

    assert all(
        not condition.is_propagating
        for condition in family
    )

    assert all(
        condition.intervention_required
        for condition in family
    )


def test_f2_contains_only_non_propagating_divergence() -> None:
    """F2 must isolate upstream divergence with no downstream effect."""

    family = conditions_for_family(
        PropagationFamily.UPSTREAM_NON_PROPAGATING
    )

    assert all(
        condition.has_divergence
        for condition in family
    )

    assert all(
        not condition.is_propagating
        for condition in family
    )

    assert all(
        not condition.intervention_required
        for condition in family
    )

    assert all(
        condition.physical_validity
        for condition in family
    )


def test_f3_contains_propagating_divergence() -> None:
    """F3 must contain genuine single-path propagation conditions."""

    family = conditions_for_family(
        PropagationFamily.UPSTREAM_PROPAGATING
    )

    assert all(
        condition.has_divergence
        for condition in family
    )

    assert all(
        condition.is_propagating
        for condition in family
    )

    assert all(
        not condition.is_compound
        for condition in family
    )

    assert all(
        condition.propagated_dependency is not None
        for condition in family
    )

    assert all(
        condition.intervention_required
        for condition in family
    )


def test_f4_contains_compound_propagation() -> None:
    """F4 must contain compound or cross-entity propagation."""

    family = conditions_for_family(
        PropagationFamily.COMPOUND_PROPAGATING
    )

    assert all(
        condition.has_divergence
        for condition in family
    )

    assert all(
        condition.is_propagating
        for condition in family
    )

    assert all(
        condition.is_compound
        for condition in family
    )

    assert all(
        condition.propagated_dependency is not None
        for condition in family
    )

    assert all(
        condition.intervention_required
        for condition in family
    )


def test_physical_validity_matches_ground_truth() -> None:
    """Physical validity must remain independent of policy behaviour."""

    for condition in EXP010_CONDITIONS:
        if condition.intervention_required:
            assert condition.physical_validity is False
        else:
            assert condition.physical_validity is True


def test_available_evidence_count_per_family() -> None:
    """Each family must contain exactly three AVAILABLE conditions."""

    for family in PropagationFamily:
        family_conditions = conditions_for_family(family)

        available = sum(
            condition.evidence_status
            is PropagationEvidenceStatus.AVAILABLE
            for condition in family_conditions
        )

        assert available == 3


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (PropagationEvidenceStatus.STALE, 1),
        (PropagationEvidenceStatus.MISSING, 1),
        (PropagationEvidenceStatus.CONFLICTING, 1),
    ],
)
def test_each_family_contains_one_of_each_imperfect_evidence_state(
    status: PropagationEvidenceStatus,
    expected: int,
) -> None:
    """Every family must preserve the frozen imperfect-evidence balance."""

    for family in PropagationFamily:
        family_conditions = conditions_for_family(family)

        count = sum(
            condition.evidence_status is status
            for condition in family_conditions
        )

        assert count == expected


def test_f1_direct_variables_are_frozen() -> None:
    """F1 must test status, capacity and availability as registered."""

    assert condition_by_id("F1-A").divergence_variable == "status"
    assert condition_by_id("F1-B").divergence_variable == "capacity"
    assert condition_by_id("F1-C").divergence_variable == "available"

    assert condition_by_id("F1-A").physical_value == "failed"
    assert condition_by_id("F1-A").twin_value == "operational"

    assert condition_by_id("F1-B").physical_value == 4.0
    assert condition_by_id("F1-B").twin_value == 10.0

    assert condition_by_id("F1-C").physical_value is False
    assert condition_by_id("F1-C").twin_value is True


def test_f3_recovery_dependencies_are_frozen() -> None:
    """Primary propagation dependencies must match the pre-registration."""

    assert (
        condition_by_id("F3-A").propagated_dependency
        == "recovery_resource_available"
    )

    assert (
        condition_by_id("F3-B").propagated_dependency
        == "recovery_resource_available"
    )

    assert (
        condition_by_id("F3-C").propagated_dependency
        == "recovery_timing_valid"
    )


def test_f4_compound_dependencies_are_frozen() -> None:
    """Compound dependency definitions must not drift during implementation."""

    assert (
        condition_by_id("F4-A").propagated_dependency
        == "vehicle_C.available+vehicle_B.assignment"
    )

    assert (
        condition_by_id("F4-B").propagated_dependency
        == "vehicle_C.capacity+recovery_demand"
    )

    assert (
        condition_by_id("F4-C").propagated_dependency
        == "recovery_timing+vehicle_B.deadline"
    )


def test_f2_has_no_propagated_dependency() -> None:
    """Non-propagating controls must not secretly encode propagation."""

    family = conditions_for_family(
        PropagationFamily.UPSTREAM_NON_PROPAGATING
    )

    assert all(
        condition.propagated_dependency is None
        for condition in family
    )


def test_condition_lookup_returns_requested_condition() -> None:
    """Frozen conditions should be retrievable by identifier."""

    condition = condition_by_id("F3-A")

    assert condition.condition_id == "F3-A"
    assert (
        condition.family
        is PropagationFamily.UPSTREAM_PROPAGATING
    )


def test_unknown_condition_identifier_raises_key_error() -> None:
    """Invalid identifiers must fail explicitly."""

    with pytest.raises(
        KeyError,
        match="Unknown EXP-010 condition",
    ):
        condition_by_id("F9-Z")


def test_matrix_validation_passes() -> None:
    """The committed frozen matrix must satisfy all structural invariants."""

    validate_condition_matrix()
