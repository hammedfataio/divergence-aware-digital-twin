def test_non_propagating_divergence_preserves_direct_interventions(
    results,
) -> None:
    """Direct divergence can require intervention without downstream propagation.

    EXP-010 contains twelve divergent conditions that do not propagate
    downstream. Six are F1 direct-divergence cases that invalidate the
    directly affected decision and therefore require intervention, while
    the six F2 upstream non-propagating controls remain valid.
    """

    summary = calculate_propagation_summary(
        results
    )

    assert (
        summary.non_propagating_divergence_conditions
        == 12
    )

    assert (
        summary.non_propagating_interventions_required
        == 6
    )
