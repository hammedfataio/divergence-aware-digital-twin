"""Integrity tests for the frozen EXP-009 condition matrix."""

from collections import Counter

from dara_dt.evidence.model import EvidenceStatus
from dara_dt.experiments.decision_relevance_conditions import (
    EXP009_CONDITIONS,
    DependencyFamily,
    EvidenceRelevance,
)


def test_exp009_contains_exactly_42_conditions() -> None:
    assert len(EXP009_CONDITIONS) == 42


def test_exp009_condition_ids_are_unique() -> None:
    condition_ids = [condition.condition_id for condition in EXP009_CONDITIONS]

    assert len(condition_ids) == len(set(condition_ids))


def test_exp009_contains_14_conditions_per_dependency_family() -> None:
    counts = Counter(
        condition.dependency_family for condition in EXP009_CONDITIONS
    )

    assert counts == {
        DependencyFamily.CAPACITY: 14,
        DependencyFamily.STATUS: 14,
        DependencyFamily.LOCATION_AVAILABILITY: 14,
    }


def test_exp009_is_balanced_by_physical_validity() -> None:
    valid = [
        condition
        for condition in EXP009_CONDITIONS
        if condition.physically_valid
    ]
    invalid = [
        condition
        for condition in EXP009_CONDITIONS
        if not condition.physically_valid
    ]

    assert len(valid) == 21
    assert len(invalid) == 21


def test_exp009_contains_six_reliable_controls() -> None:
    reliable = [
        condition
        for condition in EXP009_CONDITIONS
        if condition.evidence_status == EvidenceStatus.AVAILABLE
    ]

    assert len(reliable) == 6

    assert sum(condition.physically_valid for condition in reliable) == 3
    assert sum(not condition.physically_valid for condition in reliable) == 3

    assert all(
        condition.evidence_relevance == EvidenceRelevance.RELEVANT
        for condition in reliable
    )


def test_exp009_contains_36_imperfect_evidence_conditions() -> None:
    imperfect = [
        condition
        for condition in EXP009_CONDITIONS
        if condition.is_imperfect_evidence
    ]

    assert len(imperfect) == 36


def test_exp009_imperfect_conditions_are_balanced_by_relevance() -> None:
    imperfect = [
        condition
        for condition in EXP009_CONDITIONS
        if condition.is_imperfect_evidence
    ]

    relevant = [
        condition
        for condition in imperfect
        if condition.evidence_relevance == EvidenceRelevance.RELEVANT
    ]
    irrelevant = [
        condition
        for condition in imperfect
        if condition.evidence_relevance == EvidenceRelevance.IRRELEVANT
    ]

    assert len(relevant) == 18
    assert len(irrelevant) == 18


def test_exp009_imperfect_conditions_are_balanced_by_validity() -> None:
    imperfect = [
        condition
        for condition in EXP009_CONDITIONS
        if condition.is_imperfect_evidence
    ]

    assert sum(condition.physically_valid for condition in imperfect) == 18
    assert sum(not condition.physically_valid for condition in imperfect) == 18


def test_exp009_has_12_conditions_per_imperfect_evidence_status() -> None:
    counts = Counter(
        condition.evidence_status
        for condition in EXP009_CONDITIONS
        if condition.is_imperfect_evidence
    )

    assert counts == {
        EvidenceStatus.STALE: 12,
        EvidenceStatus.MISSING: 12,
        EvidenceStatus.CONFLICTING: 12,
    }


def test_exp009_every_imperfect_combination_has_valid_and_invalid_pair() -> None:
    for dependency_family in DependencyFamily:
        for evidence_status in (
            EvidenceStatus.STALE,
            EvidenceStatus.MISSING,
            EvidenceStatus.CONFLICTING,
        ):
            for relevance in EvidenceRelevance:
                matching = [
                    condition
                    for condition in EXP009_CONDITIONS
                    if condition.dependency_family == dependency_family
                    and condition.evidence_status == evidence_status
                    and condition.evidence_relevance == relevance
                ]

                assert len(matching) == 2

                validity = {
                    condition.physically_valid for condition in matching
                }

                assert validity == {True, False}


def test_exp009_intervention_requirement_matches_physical_validity() -> None:
    for condition in EXP009_CONDITIONS:
        assert condition.intervention_required is (
            not condition.physically_valid
        )


def test_exp009_reliable_control_property_is_correct() -> None:
    for condition in EXP009_CONDITIONS:
        expected = condition.evidence_status == EvidenceStatus.AVAILABLE

        assert condition.is_reliable_control is expected


def test_exp009_imperfect_evidence_property_is_correct() -> None:
    imperfect_statuses = {
        EvidenceStatus.STALE,
        EvidenceStatus.MISSING,
        EvidenceStatus.CONFLICTING,
    }

    for condition in EXP009_CONDITIONS:
        expected = condition.evidence_status in imperfect_statuses

        assert condition.is_imperfect_evidence is expected


def test_exp009_expected_condition_ids_exist() -> None:
    condition_ids = {
        condition.condition_id for condition in EXP009_CONDITIONS
    }

    expected_examples = {
        "CAP-R-V",
        "CAP-R-I",
        "CAP-S-REL-V",
        "CAP-S-REL-I",
        "CAP-S-IRR-V",
        "CAP-S-IRR-I",
        "STATUS-M-REL-V",
        "STATUS-M-IRR-I",
        "LOC-C-REL-I",
        "LOC-C-IRR-V",
    }

    assert expected_examples.issubset(condition_ids)


def test_exp009_matrix_matches_frozen_factor_counts() -> None:
    imperfect = [
        condition
        for condition in EXP009_CONDITIONS
        if condition.is_imperfect_evidence
    ]

    combinations = Counter(
        (
            condition.dependency_family,
            condition.evidence_status,
            condition.evidence_relevance,
            condition.physically_valid,
        )
        for condition in imperfect
    )

    # 3 dependencies × 3 imperfect evidence states
    # × 2 relevance states × 2 validity states = 36.
    assert len(combinations) == 36

    # Every frozen factor combination must occur exactly once.
    assert all(count == 1 for count in combinations.values())
