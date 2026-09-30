"""Tests for the EXP-010 divergence propagation analyser."""

import pytest

from dara_dt.propagation.analyser import (
    DivergencePropagationAnalyser,
    PropagationRule,
    build_exp010_propagation_analyser,
    build_exp010_propagation_rules,
)
from dara_dt.propagation.model import (
    DivergenceOrigin,
    PropagationType,
    build_exp010_decision_chain,
)


def build_analyser() -> DivergencePropagationAnalyser:
    """Return the frozen EXP-010 propagation analyser."""

    return build_exp010_propagation_analyser(
        build_exp010_decision_chain()
    )


def test_exp010_rules_are_defined() -> None:
    rules = build_exp010_propagation_rules()

    assert len(rules) == 9


def test_analyser_uses_exp010_chain() -> None:
    analyser = build_analyser()

    assert [
        node.decision_id
        for node in analyser.chain.ordered_nodes
    ] == ["D1", "D2", "D3"]


def test_direct_status_divergence_matches_d1() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D1",
    )

    assert result.has_divergence
    assert result.has_matching_rule
    assert not result.is_propagating

    assert result.affected_dependencies == frozenset(
        {"vehicle_A.status"}
    )

    assert result.affected_decisions == frozenset({"D1"})


def test_direct_capacity_divergence_matches_d1() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="capacity",
        physical_value=3,
        twin_value=10,
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D1",
    )

    assert result.has_matching_rule
    assert not result.is_propagating
    assert result.affected_dependencies == frozenset(
        {"vehicle_A.capacity"}
    )


def test_direct_availability_divergence_matches_d1() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="available",
        physical_value=False,
        twin_value=True,
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D1",
    )

    assert result.has_matching_rule
    assert not result.is_propagating
    assert result.affected_dependencies == frozenset(
        {"vehicle_A.available"}
    )


def test_synchronised_state_does_not_match_even_when_rule_exists() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="operational",
        twin_value="operational",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert not result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating
    assert result.paths == ()
    assert result.affected_dependencies == frozenset()


def test_status_divergence_can_propagate_to_d2() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.has_divergence
    assert result.has_matching_rule
    assert result.is_propagating

    assert "recovery_resource_available" in (
        result.affected_dependencies
    )

    assert "D2" in result.affected_decisions


def test_availability_divergence_can_propagate_to_d2() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="available",
        physical_value=False,
        twin_value=True,
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.is_propagating

    assert result.affected_dependencies == frozenset(
        {"recovery_resource_available"}
    )


def test_location_divergence_can_propagate_to_recovery_timing() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="location",
        physical_value="road_segment_7",
        twin_value="road_segment_5",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.is_propagating
    assert "recovery_timing_valid" in (
        result.affected_dependencies
    )


def test_status_divergence_can_have_compound_d2_path() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.is_compound

    assert "vehicle_C.available" in (
        result.affected_dependencies
    )

    assert "vehicle_B.assignment" in (
        result.affected_dependencies
    )


def test_status_divergence_can_propagate_to_d3() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D3",
    )

    assert result.is_propagating
    assert result.is_compound

    assert result.affected_dependencies == frozenset(
        {
            "vehicle_C.capacity",
            "recovery_demand",
        }
    )

    assert result.affected_decisions == frozenset({"D3"})


def test_location_divergence_exposes_compound_d2_dependencies() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="location",
        physical_value="road_segment_7",
        twin_value="road_segment_5",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.is_compound

    assert "recovery_timing" in (
        result.affected_dependencies
    )

    assert "vehicle_B.deadline" in (
        result.affected_dependencies
    )


def test_f2_style_capacity_divergence_does_not_propagate_to_d2() -> None:
    """Capacity divergence may exist upstream without reaching D2."""

    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="capacity",
        physical_value=7,
        twin_value=10,
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating
    assert result.paths == ()
    assert result.affected_dependencies == frozenset()


def test_unrelated_origin_does_not_propagate() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_X",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating


def test_unknown_pending_decision_is_rejected() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    with pytest.raises(KeyError, match="Unknown decision"):
        analyser.analyse(
            origin=origin,
            pending_decision_id="D99",
        )


def test_rules_for_origin_returns_matching_rules() -> None:
    analyser = build_analyser()

    rules = analyser.rules_for_origin(
        "vehicle_A.status"
    )

    assert rules
    assert all(
        rule.origin_dependency == "vehicle_A.status"
        for rule in rules
    )


def test_rules_for_unknown_origin_returns_empty_tuple() -> None:
    analyser = build_analyser()

    assert analyser.rules_for_origin(
        "vehicle_X.status"
    ) == ()


def test_rules_for_d3_target_d3_only() -> None:
    analyser = build_analyser()

    rules = analyser.rules_for_decision("D3")

    assert rules
    assert all(
        rule.target_decision_id == "D3"
        for rule in rules
    )


def test_rules_for_unknown_decision_are_rejected() -> None:
    analyser = build_analyser()

    with pytest.raises(KeyError, match="Unknown decision"):
        analyser.rules_for_decision("D99")


def test_propagation_path_preserves_origin() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="available",
        physical_value=False,
        twin_value=True,
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.paths
    assert all(
        path.origin == origin
        for path in result.paths
    )


def test_propagation_paths_target_pending_decision() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert result.paths

    for path in result.paths:
        assert path.reaches_decision("D2")


def test_compound_rule_requires_multiple_dependencies() -> None:
    chain = build_exp010_decision_chain()

    bad_rule = PropagationRule(
        origin_dependency="vehicle_A.status",
        source_decision_id="D1",
        target_decision_id="D2",
        affected_dependencies=(
            "recovery_resource_available",
        ),
        propagation_type=PropagationType.COMPOUND,
        description="Invalid compound rule.",
    )

    with pytest.raises(
        ValueError,
        match="at least two dependencies",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(bad_rule,),
        )


def test_propagating_rule_cannot_target_same_stage() -> None:
    chain = build_exp010_decision_chain()

    bad_rule = PropagationRule(
        origin_dependency="vehicle_A.status",
        source_decision_id="D1",
        target_decision_id="D1",
        affected_dependencies=("vehicle_A.status",),
        propagation_type=PropagationType.PROPAGATING,
        description="Invalid same-decision propagation.",
    )

    with pytest.raises(
        ValueError,
        match="earlier decision",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(bad_rule,),
        )


def test_backward_propagation_rule_is_rejected() -> None:
    chain = build_exp010_decision_chain()

    bad_rule = PropagationRule(
        origin_dependency="vehicle_C.status",
        source_decision_id="D3",
        target_decision_id="D1",
        affected_dependencies=("vehicle_A.status",),
        propagation_type=PropagationType.PROPAGATING,
        description="Invalid backward propagation.",
    )

    with pytest.raises(
        ValueError,
        match="backwards",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(bad_rule,),
        )


def test_empty_origin_dependency_is_rejected() -> None:
    chain = build_exp010_decision_chain()

    bad_rule = PropagationRule(
        origin_dependency="",
        source_decision_id="D1",
        target_decision_id="D2",
        affected_dependencies=(
            "recovery_resource_available",
        ),
        propagation_type=PropagationType.PROPAGATING,
        description="Invalid empty origin.",
    )

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(bad_rule,),
        )


def test_rule_without_affected_dependencies_is_rejected() -> None:
    chain = build_exp010_decision_chain()

    bad_rule = PropagationRule(
        origin_dependency="vehicle_A.status",
        source_decision_id="D1",
        target_decision_id="D2",
        affected_dependencies=(),
        propagation_type=PropagationType.PROPAGATING,
        description="Invalid empty affected dependencies.",
    )

    with pytest.raises(
        ValueError,
        match="at least one",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(bad_rule,),
        )


def test_analysis_is_deterministic() -> None:
    analyser = build_analyser()

    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    first = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    second = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
    )

    assert first == second
