"""Tests for the controlled DARA-DT experimental matrix."""

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.experimental_matrix import (
    run_experimental_matrix,
)


IRRELEVANT_CONDITIONS = {
    "irrelevant_1",
    "irrelevant_5",
    "irrelevant_10",
    "irrelevant_25",
}

RELEVANT_CONDITIONS = {
    "relevant_vehicle_status",
    "relevant_vehicle_capacity",
    "relevant_vehicle_availability",
}


def test_matrix_contains_seven_controlled_conditions():
    """The matrix should contain all seven controlled conditions."""

    matrix = run_experimental_matrix()

    conditions = {
        row.condition
        for row in matrix.rows
    }

    assert conditions == (
        IRRELEVANT_CONDITIONS
        | RELEVANT_CONDITIONS
    )

    assert len(matrix.rows) == 7


def test_irrelevant_conditions_have_zero_relevance():
    """Injected unrelated divergence must remain decision-irrelevant."""

    matrix = run_experimental_matrix()

    irrelevant_rows = [
        row
        for row in matrix.rows
        if row.condition in IRRELEVANT_CONDITIONS
    ]

    assert len(irrelevant_rows) == 4

    for row in irrelevant_rows:
        assert row.relevant_count == 0


def test_irrelevant_conditions_distinguish_global_policy():
    """Global divergence should over-intervene on irrelevant mismatch."""

    matrix = run_experimental_matrix()

    irrelevant_rows = [
        row
        for row in matrix.rows
        if row.condition in IRRELEVANT_CONDITIONS
    ]

    for row in irrelevant_rows:
        assert (
            row.no_assurance
            == AssuranceOutcome.CORRECT_NON_INTERVENTION
        )

        assert (
            row.global_divergence
            == AssuranceOutcome.FALSE_INTERVENTION
        )

        assert (
            row.dara_dt
            == AssuranceOutcome.CORRECT_NON_INTERVENTION
        )


def test_relevant_conditions_are_decision_relevant():
    """Every relevant scenario must affect decision dependencies."""

    matrix = run_experimental_matrix()

    relevant_rows = [
        row
        for row in matrix.rows
        if row.condition in RELEVANT_CONDITIONS
    ]

    assert len(relevant_rows) == 3

    for row in relevant_rows:
        assert row.divergence_count >= 1
        assert row.relevant_count >= 1


def test_relevant_conditions_require_intervention():
    """Relevant stale-Twin states should require intervention."""

    matrix = run_experimental_matrix()

    relevant_rows = [
        row
        for row in matrix.rows
        if row.condition in RELEVANT_CONDITIONS
    ]

    for row in relevant_rows:
        assert (
            row.no_assurance
            == AssuranceOutcome.MISSED_INTERVENTION
        )

        assert (
            row.global_divergence
            == AssuranceOutcome.TRUE_INTERVENTION
        )

        assert (
            row.dara_dt
            == AssuranceOutcome.TRUE_INTERVENTION
        )


def test_matrix_preserves_irrelevant_divergence_count_levels():
    """Irrelevant scenarios should preserve controlled count levels."""

    matrix = run_experimental_matrix()

    observed = {
        row.divergence_count
        for row in matrix.rows
        if row.condition in IRRELEVANT_CONDITIONS
    }

    assert observed == {1, 5, 10, 25}
