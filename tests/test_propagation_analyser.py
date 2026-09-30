"""Tests for the EXP-010 context-sensitive divergence propagation analyser."""

from __future__ import annotations

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


def status_divergence() -> DivergenceOrigin:
    """Vehicle A physical failure hidden from the Digital Twin."""

    return DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )


def location_divergence() -> DivergenceOrigin:
    """Vehicle A physical/Twin location mismatch."""

    return DivergenceOrigin(
        entity="vehicle_A",
        variable="location",
        physical_value="road_segment_7",
        twin_value="road_segment_5",
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

    result = analyser.analyse(
        origin=status_divergence(),
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


def test_direct_dependency_does_not_require_context_activation() -> None:
    """Direct D1 relevance must survive an explicit empty context."""

    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D1",
        active_dependencies=frozenset(),
    )

    assert result.has_matching_rule
    assert not result.is_propagating

    assert result.affected_dependencies == frozenset(
        {"vehicle_A.status"}
    )


def test_synchronised_state_never_propagates() -> None:
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
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert not result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating
    assert result.paths == ()
    assert result.affected_dependencies == frozenset()


def test_structural_analysis_preserves_original_behaviour() -> None:
    """None means structural analysis without runtime context filtering."""

    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
    )

    assert result.has_divergence
    assert result.has_matching_rule
    assert result.is_propagating

    assert "recovery_resource_available" in (
        result.affected_dependencies
    )

    assert "vehicle_C.available" in (
        result.affected_dependencies
    )

    assert "vehicle_B.assignment" in (
        result.affected_dependencies
    )


def test_same_status_divergence_can_be_non_propagating_when_context_inactive() -> None:
    """F2-C style case: status mismatch exists but recovery is irrelevant."""

    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(),
    )

    assert result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating
    assert result.paths == ()
    assert result.affected_dependencies == frozenset()


def test_same_status_divergence_propagates_when_recovery_context_active() -> None:
    """F3-A style case: identical origin, different observable context."""

    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert result.has_divergence
    assert result.has_matching_rule
    assert result.is_propagating

    assert result.affected_dependencies == frozenset(
        {"recovery_resource_available"}
    )


def test_same_origin_changes_only_because_runtime_context_changes() -> None:
    """Critical EXP-010 test: no condition or ground-truth label is needed."""

    analyser = build_analyser()
    origin = status_divergence()

    inactive = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
        active_dependencies=frozenset(),
    )

    active = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert inactive.origin == active.origin
    assert inactive.pending_decision_id == active.pending_decision_id

    assert not inactive.is_propagating
    assert active.is_propagating


def test_only_active_status_propagation_rule_is_selected() -> None:
    """Inactive compound paths must not leak into a simple F3 context."""

    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert result.is_propagating
    assert not result.is_compound

    assert result.affected_dependencies == frozenset(
        {"recovery_resource_available"}
    )

    assert "vehicle_C.available" not in (
        result.affected_dependencies
    )

    assert "vehicle_B.assignment" not in (
        result.affected_dependencies
    )


def test_compound_status_context_activates_compound_path() -> None:
    """F4-style context activates cross-entity propagation."""

    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {
                "vehicle_C.available",
                "vehicle_B.assignment",
            }
        ),
    )

    assert result.is_propagating
    assert result.is_compound

    assert result.affected_dependencies == frozenset(
        {
            "vehicle_C.available",
            "vehicle_B.assignment",
        }
    )


def test_multiple_active_status_paths_can_be_reported() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {
                "recovery_resource_available",
                "vehicle_C.available",
                "vehicle_B.assignment",
            }
        ),
    )

    assert result.is_propagating
    assert result.is_compound

    assert result.affected_dependencies == frozenset(
        {
            "recovery_resource_available",
            "vehicle_C.available",
            "vehicle_B.assignment",
        }
    )


def test_availability_divergence_propagates_when_recovery_active() -> None:
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
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert result.is_propagating

    assert result.affected_dependencies == frozenset(
        {"recovery_resource_available"}
    )


def test_availability_divergence_does_not_propagate_when_recovery_inactive() -> None:
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
        active_dependencies=frozenset(),
    )

    assert result.has_divergence
    assert not result.is_propagating
    assert result.affected_dependencies == frozenset()


def test_location_divergence_can_activate_recovery_timing_only() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=location_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {"recovery_timing_valid"}
        ),
    )

    assert result.is_propagating
    assert not result.is_compound

    assert result.affected_dependencies == frozenset(
        {"recovery_timing_valid"}
    )


def test_location_divergence_can_activate_compound_timing_path() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=location_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {
                "recovery_timing",
                "vehicle_B.deadline",
            }
        ),
    )

    assert result.is_propagating
    assert result.is_compound

    assert result.affected_dependencies == frozenset(
        {
            "recovery_timing",
            "vehicle_B.deadline",
        }
    )


def test_location_context_can_select_both_propagation_paths() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=location_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {
                "recovery_timing_valid",
                "recovery_timing",
                "vehicle_B.deadline",
            }
        ),
    )

    assert result.is_propagating
    assert result.is_compound

    assert result.affected_dependencies == frozenset(
        {
            "recovery_timing_valid",
            "recovery_timing",
            "vehicle_B.deadline",
        }
    )


def test_status_divergence_can_propagate_to_d3() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D3",
        active_dependencies=frozenset(
            {
                "vehicle_C.capacity",
                "recovery_demand",
            }
        ),
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


def test_d3_status_path_is_inactive_without_recovery_dependencies() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D3",
        active_dependencies=frozenset(),
    )

    assert result.has_divergence
    assert not result.is_propagating
    assert result.affected_dependencies == frozenset()


def test_f2_style_capacity_divergence_does_not_propagate_to_d2() -> None:
    """Capacity divergence has no declared D1-to-D2 propagation rule."""

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
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating
    assert result.paths == ()
    assert result.affected_dependencies == frozenset()


def test_unrelated_active_dependency_does_not_activate_status_path() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {"vehicle_B.capacity_sufficient"}
        ),
    )

    assert result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating


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
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert result.has_divergence
    assert not result.has_matching_rule
    assert not result.is_propagating


def test_unknown_pending_decision_is_rejected() -> None:
    analyser = build_analyser()

    with pytest.raises(KeyError, match="Unknown decision"):
        analyser.analyse(
            origin=status_divergence(),
            pending_decision_id="D99",
            active_dependencies=frozenset(),
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
    origin = status_divergence()

    result = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {"recovery_resource_available"}
        ),
    )

    assert result.paths

    assert all(
        path.origin == origin
        for path in result.paths
    )


def test_propagation_paths_target_pending_decision() -> None:
    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {
                "recovery_resource_available",
                "vehicle_C.available",
                "vehicle_B.assignment",
            }
        ),
    )

    assert result.paths

    for path in result.paths:
        assert path.reaches_decision("D2")


def test_active_dependency_matching_is_exact() -> None:
    """Substring or approximate names must not activate propagation."""

    analyser = build_analyser()

    result = analyser.analyse(
        origin=status_divergence(),
        pending_decision_id="D2",
        active_dependencies=frozenset(
            {"recovery_resource"}
        ),
    )

    assert not result.is_propagating


def test_context_analysis_is_deterministic() -> None:
    analyser = build_analyser()
    origin = status_divergence()

    active_dependencies = frozenset(
        {
            "recovery_resource_available",
            "vehicle_C.available",
        }
    )

    first = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
        active_dependencies=active_dependencies,
    )

    second = analyser.analyse(
        origin=origin,
        pending_decision_id="D2",
        active_dependencies=active_dependencies,
    )

    assert first == second


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


def test_duplicate_affected_dependencies_are_rejected() -> None:
    chain = build_exp010_decision_chain()

    bad_rule = PropagationRule(
        origin_dependency="vehicle_A.status",
        source_decision_id="D1",
        target_decision_id="D2",
        affected_dependencies=(
            "recovery_resource_available",
            "recovery_resource_available",
        ),
        propagation_type=PropagationType.COMPOUND,
        description="Invalid duplicate dependencies.",
    )

    with pytest.raises(
        ValueError,
        match="must be unique",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(bad_rule,),
        )


def test_direct_rule_cannot_cross_decision_stage() -> None:
    chain = build_exp010_decision_chain()

    bad_rule = PropagationRule(
        origin_dependency="vehicle_A.status",
        source_decision_id="D1",
        target_decision_id="D2",
        affected_dependencies=(
            "recovery_resource_available",
        ),
        propagation_type=PropagationType.DIRECT,
        description="Invalid cross-decision direct rule.",
    )

    with pytest.raises(
        ValueError,
        match="same decision stage",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(bad_rule,),
        )


def test_duplicate_rules_are_rejected() -> None:
    chain = build_exp010_decision_chain()

    rule = PropagationRule(
        origin_dependency="vehicle_A.status",
        source_decision_id="D1",
        target_decision_id="D2",
        affected_dependencies=(
            "recovery_resource_available",
        ),
        propagation_type=PropagationType.PROPAGATING,
        description="Duplicate rule.",
    )

    with pytest.raises(
        ValueError,
        match="Duplicate propagation rules",
    ):
        DivergencePropagationAnalyser(
            chain=chain,
            rules=(rule, rule),
        )
