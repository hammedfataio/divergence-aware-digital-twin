"""Tests for the EXP-010 divergence propagation domain model."""

import pytest

from dara_dt.propagation.model import (
    DecisionChain,
    DecisionEdge,
    DecisionNode,
    DivergenceOrigin,
    PropagationPath,
    PropagationStep,
    PropagationType,
    build_exp010_decision_chain,
)


def test_exp010_chain_contains_three_decisions() -> None:
    chain = build_exp010_decision_chain()

    assert len(chain.nodes) == 3
    assert [node.decision_id for node in chain.ordered_nodes] == [
        "D1",
        "D2",
        "D3",
    ]


def test_exp010_chain_stages_are_ordered() -> None:
    chain = build_exp010_decision_chain()

    assert [node.stage for node in chain.ordered_nodes] == [1, 2, 3]


def test_d1_contains_direct_vehicle_a_dependencies() -> None:
    chain = build_exp010_decision_chain()
    d1 = chain.node("D1")

    assert d1.depends_on("vehicle_A.status")
    assert d1.depends_on("vehicle_A.available")
    assert d1.depends_on("vehicle_A.capacity")
    assert d1.depends_on("order_O1.demand")


def test_d2_contains_direct_and_shared_dependencies() -> None:
    chain = build_exp010_decision_chain()
    d2 = chain.node("D2")

    assert d2.depends_on("vehicle_B.status")
    assert d2.depends_on("vehicle_B.available")
    assert d2.depends_on("vehicle_B.capacity")
    assert d2.depends_on("order_O2.demand")
    assert d2.depends_on("order_O2.deadline")

    assert d2.depends_on("recovery_resource_available")
    assert d2.depends_on("recovery_timing_valid")
    assert d2.depends_on("upstream_assignment_assumptions_valid")


def test_d3_contains_recovery_dependencies() -> None:
    chain = build_exp010_decision_chain()
    d3 = chain.node("D3")

    assert d3.depends_on("vehicle_C.status")
    assert d3.depends_on("vehicle_C.available")
    assert d3.depends_on("vehicle_C.capacity")
    assert d3.depends_on("recovery_demand")
    assert d3.depends_on("upstream_failure_state")


def test_unknown_decision_raises_key_error() -> None:
    chain = build_exp010_decision_chain()

    with pytest.raises(KeyError, match="Unknown decision"):
        chain.node("D99")


def test_chain_has_expected_cross_decision_edges() -> None:
    chain = build_exp010_decision_chain()

    edges = {
        (edge.source_decision_id, edge.target_decision_id)
        for edge in chain.edges
    }

    assert edges == {
        ("D1", "D2"),
        ("D1", "D3"),
        ("D2", "D3"),
    }


def test_d1_to_d2_edge_carries_recovery_dependencies() -> None:
    chain = build_exp010_decision_chain()

    edges = [
        edge
        for edge in chain.outgoing_edges("D1")
        if edge.target_decision_id == "D2"
    ]

    assert len(edges) == 1

    edge = edges[0]

    assert edge.carries("recovery_resource_available")
    assert edge.carries("recovery_timing_valid")
    assert edge.carries("upstream_assignment_assumptions_valid")


def test_d1_has_two_outgoing_edges() -> None:
    chain = build_exp010_decision_chain()

    edges = chain.outgoing_edges("D1")

    assert len(edges) == 2
    assert {edge.target_decision_id for edge in edges} == {
        "D2",
        "D3",
    }


def test_d3_has_two_incoming_edges() -> None:
    chain = build_exp010_decision_chain()

    edges = chain.incoming_edges("D3")

    assert len(edges) == 2
    assert {edge.source_decision_id for edge in edges} == {
        "D1",
        "D2",
    }


def test_downstream_decisions_from_d1_are_d2_and_d3() -> None:
    chain = build_exp010_decision_chain()

    downstream = chain.downstream_decisions("D1")

    assert [node.decision_id for node in downstream] == [
        "D2",
        "D3",
    ]


def test_downstream_decisions_from_d2_contains_only_d3() -> None:
    chain = build_exp010_decision_chain()

    downstream = chain.downstream_decisions("D2")

    assert [node.decision_id for node in downstream] == ["D3"]


def test_d3_has_no_downstream_decisions() -> None:
    chain = build_exp010_decision_chain()

    assert chain.downstream_decisions("D3") == ()


def test_divergence_origin_builds_canonical_dependency() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    assert origin.dependency == "vehicle_A.status"
    assert origin.is_divergent is True


def test_synchronised_origin_is_not_divergent() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="operational",
        twin_value="operational",
    )

    assert origin.is_divergent is False


def test_propagation_step_detects_cross_decision_relationship() -> None:
    step = PropagationStep(
        source_decision_id="D1",
        target_decision_id="D2",
        source_dependency="vehicle_A.status",
        affected_dependency="recovery_resource_available",
        description=(
            "Vehicle A failure changes recovery-resource availability."
        ),
    )

    assert step.is_cross_decision is True


def test_same_decision_step_is_not_cross_decision() -> None:
    step = PropagationStep(
        source_decision_id="D1",
        target_decision_id="D1",
        source_dependency="vehicle_A.status",
        affected_dependency="vehicle_A.available",
        description="Direct within-decision relationship.",
    )

    assert step.is_cross_decision is False


def test_propagation_path_reports_depth() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    path = PropagationPath(
        origin=origin,
        propagation_type=PropagationType.PROPAGATING,
        steps=(
            PropagationStep(
                source_decision_id="D1",
                target_decision_id="D2",
                source_dependency="vehicle_A.status",
                affected_dependency="recovery_resource_available",
                description="Recovery capacity becomes constrained.",
            ),
        ),
    )

    assert path.depth == 1
    assert path.is_propagating is True
    assert path.is_compound is False


def test_propagation_path_exposes_affected_dependencies() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    path = PropagationPath(
        origin=origin,
        propagation_type=PropagationType.PROPAGATING,
        steps=(
            PropagationStep(
                source_decision_id="D1",
                target_decision_id="D2",
                source_dependency="vehicle_A.status",
                affected_dependency="recovery_resource_available",
                description="Recovery resource becomes required.",
            ),
            PropagationStep(
                source_decision_id="D2",
                target_decision_id="D3",
                source_dependency="recovery_resource_available",
                affected_dependency="recovery_demand",
                description="Recovery demand propagates to D3.",
            ),
        ),
    )

    assert path.affected_dependencies == frozenset(
        {
            "recovery_resource_available",
            "recovery_demand",
        }
    )


def test_propagation_path_exposes_affected_decisions() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    path = PropagationPath(
        origin=origin,
        propagation_type=PropagationType.PROPAGATING,
        steps=(
            PropagationStep(
                source_decision_id="D1",
                target_decision_id="D2",
                source_dependency="vehicle_A.status",
                affected_dependency="recovery_resource_available",
                description="Affects D2.",
            ),
            PropagationStep(
                source_decision_id="D2",
                target_decision_id="D3",
                source_dependency="recovery_resource_available",
                affected_dependency="recovery_demand",
                description="Affects D3.",
            ),
        ),
    )

    assert path.affected_decisions == frozenset({"D2", "D3"})
    assert path.reaches_decision("D2")
    assert path.reaches_decision("D3")
    assert not path.reaches_decision("D1")


def test_propagation_path_can_query_affected_dependency() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    path = PropagationPath(
        origin=origin,
        propagation_type=PropagationType.PROPAGATING,
        steps=(
            PropagationStep(
                source_decision_id="D1",
                target_decision_id="D2",
                source_dependency="vehicle_A.status",
                affected_dependency="recovery_resource_available",
                description="Recovery resource affected.",
            ),
        ),
    )

    assert path.affects_dependency("recovery_resource_available")
    assert not path.affects_dependency("vehicle_B.capacity")


def test_compound_path_is_identified() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="status",
        physical_value="failed",
        twin_value="operational",
    )

    path = PropagationPath(
        origin=origin,
        propagation_type=PropagationType.COMPOUND,
        steps=(
            PropagationStep(
                source_decision_id="D1",
                target_decision_id="D2",
                source_dependency="vehicle_A.status",
                affected_dependency="vehicle_C.available",
                description="Recovery vehicle availability affected.",
            ),
            PropagationStep(
                source_decision_id="D1",
                target_decision_id="D2",
                source_dependency="vehicle_A.status",
                affected_dependency="vehicle_B.assignment",
                description="Vehicle B assignment affected.",
            ),
        ),
    )

    assert path.is_propagating
    assert path.is_compound
    assert path.depth == 2


def test_non_propagating_path_is_not_marked_as_propagating() -> None:
    origin = DivergenceOrigin(
        entity="vehicle_A",
        variable="location",
        physical_value="road_segment_7",
        twin_value="road_segment_5",
    )

    path = PropagationPath(
        origin=origin,
        propagation_type=PropagationType.NON_PROPAGATING,
        steps=(),
    )

    assert path.is_propagating is False
    assert path.is_compound is False
    assert path.depth == 0
    assert path.affected_dependencies == frozenset()
    assert path.affected_decisions == frozenset()


def test_duplicate_decision_ids_are_rejected() -> None:
    d1 = DecisionNode(
        decision_id="D1",
        stage=1,
        description="First decision.",
        dependencies=frozenset(),
    )

    duplicate = DecisionNode(
        decision_id="D1",
        stage=2,
        description="Duplicate identifier.",
        dependencies=frozenset(),
    )

    with pytest.raises(
        ValueError,
        match="decision identifiers must be unique",
    ):
        DecisionChain(
            nodes=(d1, duplicate),
            edges=(),
        )


def test_duplicate_stages_are_rejected() -> None:
    d1 = DecisionNode(
        decision_id="D1",
        stage=1,
        description="First decision.",
        dependencies=frozenset(),
    )

    d2 = DecisionNode(
        decision_id="D2",
        stage=1,
        description="Same stage.",
        dependencies=frozenset(),
    )

    with pytest.raises(
        ValueError,
        match="stages must be unique",
    ):
        DecisionChain(
            nodes=(d1, d2),
            edges=(),
        )


def test_edge_with_unknown_source_is_rejected() -> None:
    d1 = DecisionNode(
        decision_id="D1",
        stage=1,
        description="Known decision.",
        dependencies=frozenset(),
    )

    edge = DecisionEdge(
        source_decision_id="D99",
        target_decision_id="D1",
        shared_dependencies=frozenset(),
    )

    with pytest.raises(
        ValueError,
        match="unknown source decision",
    ):
        DecisionChain(
            nodes=(d1,),
            edges=(edge,),
        )


def test_edge_with_unknown_target_is_rejected() -> None:
    d1 = DecisionNode(
        decision_id="D1",
        stage=1,
        description="Known decision.",
        dependencies=frozenset(),
    )

    edge = DecisionEdge(
        source_decision_id="D1",
        target_decision_id="D99",
        shared_dependencies=frozenset(),
    )

    with pytest.raises(
        ValueError,
        match="unknown target decision",
    ):
        DecisionChain(
            nodes=(d1,),
            edges=(edge,),
        )


def test_backward_edge_is_rejected() -> None:
    d1 = DecisionNode(
        decision_id="D1",
        stage=1,
        description="First decision.",
        dependencies=frozenset(),
    )

    d2 = DecisionNode(
        decision_id="D2",
        stage=2,
        description="Second decision.",
        dependencies=frozenset(),
    )

    edge = DecisionEdge(
        source_decision_id="D2",
        target_decision_id="D1",
        shared_dependencies=frozenset(),
    )

    with pytest.raises(
        ValueError,
        match="earlier decision",
    ):
        DecisionChain(
            nodes=(d1, d2),
            edges=(edge,),
        )


def test_self_edge_is_rejected() -> None:
    d1 = DecisionNode(
        decision_id="D1",
        stage=1,
        description="Decision.",
        dependencies=frozenset(),
    )

    edge = DecisionEdge(
        source_decision_id="D1",
        target_decision_id="D1",
        shared_dependencies=frozenset(),
    )

    with pytest.raises(
        ValueError,
        match="earlier decision",
    ):
        DecisionChain(
            nodes=(d1,),
            edges=(edge,),
        )


def test_exp010_chain_structure_is_deterministic() -> None:
    first = build_exp010_decision_chain()
    second = build_exp010_decision_chain()

    assert first == second
