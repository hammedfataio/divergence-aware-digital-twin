"""Tests for the combined DARA-DT experimental matrix."""

from dara_dt.evaluation.outcomes import AssuranceOutcome
from dara_dt.experiments.experimental_matrix import (
    run_experimental_matrix,
)


def test_matrix_contains_expected_conditions():
    """Matrix should contain all current controlled conditions."""

    matrix = run_experimental_matrix()

    conditions = {
        row.condition
        for row in matrix.rows
    }

    assert conditions == {
        "irrelevant_1",
        "irrelevant_5",
        "irrelevant_10",
        "irrelevant_25",
        "relevant_breakdown",
    }


def test_irrelevant_conditions_have_zero_relevance():
    """Irrelevant conditions must contain no relevant divergence."""

    matrix = run_experimental_matrix()

    irrelevant_rows = [
        row
        for row in matrix.rows
        if row.condition.startswith("irrelevant_")
    ]

    assert len(irrelevant_rows) == 4

    for row in irrelevant_rows:
        assert row.relevant_count == 0


def test_irrelevant_conditions_distinguish_global_policy():
    """Global policy should falsely intervene on irrelevant divergence."""

    matrix = run_experimental_matrix()

    irrelevant_rows = [
        row
        for row in matrix.rows
        if row.condition.startswith("irrelevant_")
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


def test_relevant_breakdown_requires_intervention():
    """Relevant stale-Twin breakdown should require intervention."""

    matrix = run_experimental_matrix()

    row = next(
        row
        for row in matrix.rows
        if row.condition == "relevant_breakdown"
    )

    assert row.divergence_count == 2
    assert row.relevant_count == 2

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


def test_matrix_preserves_divergence_count_levels():
    """Irrelevant conditions should preserve controlled counts."""

    matrix = run_experimental_matrix()

    counts = {
        row.condition: row.divergence_count
        for row in matrix.rows
    }

    assert counts["irrelevant_1"] == 1
    assert counts["irrelevant_5"] == 5
    assert counts["irrelevant_10"] == 10
    assert counts["irrelevant_25"] == 25
