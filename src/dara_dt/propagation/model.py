"""Core propagation models for EXP-010.

This module represents how a physical-digital divergence can originate at
one point in an autonomous logistics decision chain and affect dependencies
used by later decisions.

The model deliberately separates:

    direct decision dependencies
        from
    cross-decision divergence propagation

Existing DependencyMapper behaviour is therefore not modified.

EXP-010 uses this representation to test whether explicit knowledge of
divergence origin and propagation provides runtime-assurance information
beyond a strong dependency-aware composed runtime contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PropagationType(str, Enum):
    """Classification of a divergence relationship."""

    DIRECT = "direct"
    NON_PROPAGATING = "non_propagating"
    PROPAGATING = "propagating"
    COMPOUND = "compound"


@dataclass(frozen=True, slots=True)
class DecisionNode:
    """A decision participating in an autonomous decision chain.

    Attributes:
        decision_id:
            Unique decision identifier such as ``D1``.

        stage:
            Position in the decision chain.

        description:
            Human-readable description of the decision.

        dependencies:
            Dependencies required for the decision to remain valid.
    """

    decision_id: str
    stage: int
    description: str
    dependencies: frozenset[str]

    def depends_on(self, dependency: str) -> bool:
        """Return whether this decision explicitly depends on a variable."""

        return dependency in self.dependencies


@dataclass(frozen=True, slots=True)
class DecisionEdge:
    """Directed relationship between two decisions.

    An edge means that the validity or assumptions of the downstream
    decision may depend on state produced or assumed by the upstream
    decision.
    """

    source_decision_id: str
    target_decision_id: str
    shared_dependencies: frozenset[str]

    def carries(self, dependency: str) -> bool:
        """Return whether the edge carries the supplied dependency."""

        return dependency in self.shared_dependencies


@dataclass(frozen=True, slots=True)
class DivergenceOrigin:
    """Physical-digital mismatch from which propagation may begin."""

    entity: str
    variable: str
    physical_value: object
    twin_value: object

    @property
    def dependency(self) -> str:
        """Return canonical dependency representation."""

        return f"{self.entity}.{self.variable}"

    @property
    def is_divergent(self) -> bool:
        """Return whether physical and Digital Twin values differ."""

        return self.physical_value != self.twin_value


@dataclass(frozen=True, slots=True)
class PropagationStep:
    """One step in a divergence-propagation path.

    A step records how an upstream mismatch affects another dependency
    or decision assumption.
    """

    source_decision_id: str
    target_decision_id: str
    source_dependency: str
    affected_dependency: str
    description: str

    @property
    def is_cross_decision(self) -> bool:
        """Return whether the propagation crosses decision boundaries."""

        return self.source_decision_id != self.target_decision_id


@dataclass(frozen=True, slots=True)
class PropagationPath:
    """Trace of a divergence through an autonomous decision chain."""

    origin: DivergenceOrigin
    propagation_type: PropagationType
    steps: tuple[PropagationStep, ...]

    @property
    def depth(self) -> int:
        """Return the number of propagation steps."""

        return len(self.steps)

    @property
    def is_propagating(self) -> bool:
        """Return whether the path represents genuine propagation."""

        return self.propagation_type in {
            PropagationType.PROPAGATING,
            PropagationType.COMPOUND,
        }

    @property
    def is_compound(self) -> bool:
        """Return whether multiple propagation relationships are involved."""

        return self.propagation_type is PropagationType.COMPOUND

    @property
    def affected_dependencies(self) -> frozenset[str]:
        """Return all dependencies affected along the propagation path."""

        return frozenset(
            step.affected_dependency
            for step in self.steps
        )

    @property
    def affected_decisions(self) -> frozenset[str]:
        """Return all downstream decisions reached by the path."""

        return frozenset(
            step.target_decision_id
            for step in self.steps
        )

    def reaches_decision(self, decision_id: str) -> bool:
        """Return whether the propagation path reaches a decision."""

        return decision_id in self.affected_decisions

    def affects_dependency(self, dependency: str) -> bool:
        """Return whether the path affects a particular dependency."""

        return dependency in self.affected_dependencies


@dataclass(frozen=True, slots=True)
class DecisionChain:
    """Ordered autonomous decision chain used by EXP-010."""

    nodes: tuple[DecisionNode, ...]
    edges: tuple[DecisionEdge, ...]

    def __post_init__(self) -> None:
        """Validate basic structural invariants."""

        if not self.nodes:
            raise ValueError(
                "DecisionChain must contain at least one decision."
            )

        decision_ids = [
            node.decision_id
            for node in self.nodes
        ]

        if len(decision_ids) != len(set(decision_ids)):
            raise ValueError(
                "DecisionChain decision identifiers must be unique."
            )

        stages = [
            node.stage
            for node in self.nodes
        ]

        if len(stages) != len(set(stages)):
            raise ValueError(
                "DecisionChain stages must be unique."
            )

        known_decisions = set(decision_ids)

        for edge in self.edges:
            if edge.source_decision_id not in known_decisions:
                raise ValueError(
                    "DecisionEdge references unknown source decision: "
                    f"{edge.source_decision_id}"
                )

            if edge.target_decision_id not in known_decisions:
                raise ValueError(
                    "DecisionEdge references unknown target decision: "
                    f"{edge.target_decision_id}"
                )

            source = self.node(edge.source_decision_id)
            target = self.node(edge.target_decision_id)

            if source.stage >= target.stage:
                raise ValueError(
                    "DecisionEdge must point from an earlier decision "
                    "to a later decision."
                )

    @property
    def ordered_nodes(self) -> tuple[DecisionNode, ...]:
        """Return decisions ordered by chain stage."""

        return tuple(
            sorted(
                self.nodes,
                key=lambda node: node.stage,
            )
        )

    def node(self, decision_id: str) -> DecisionNode:
        """Return a decision node by identifier.

        Raises:
            KeyError:
                If the decision is not part of the chain.
        """

        for node in self.nodes:
            if node.decision_id == decision_id:
                return node

        raise KeyError(
            f"Unknown decision in chain: {decision_id}"
        )

    def outgoing_edges(
        self,
        decision_id: str,
    ) -> tuple[DecisionEdge, ...]:
        """Return edges leaving a decision."""

        self.node(decision_id)

        return tuple(
            edge
            for edge in self.edges
            if edge.source_decision_id == decision_id
        )

    def incoming_edges(
        self,
        decision_id: str,
    ) -> tuple[DecisionEdge, ...]:
        """Return edges entering a decision."""

        self.node(decision_id)

        return tuple(
            edge
            for edge in self.edges
            if edge.target_decision_id == decision_id
        )

    def downstream_decisions(
        self,
        decision_id: str,
    ) -> tuple[DecisionNode, ...]:
        """Return decisions occurring after the supplied decision."""

        source = self.node(decision_id)

        return tuple(
            node
            for node in self.ordered_nodes
            if node.stage > source.stage
        )


def build_exp010_decision_chain() -> DecisionChain:
    """Build the frozen D1 -> D2 -> D3 EXP-010 decision chain.

    D1
        Assign Order O1 to Vehicle A.

    D2
        Assign Order O2 to Vehicle B while respecting shared recovery
        assumptions produced by the earlier decision state.

    D3
        Reserve or allocate Vehicle C as recovery support.

    This function defines the experimental dependency structure only.
    It does not determine assurance outcomes or physical ground truth.
    """

    d1 = DecisionNode(
        decision_id="D1",
        stage=1,
        description="Assign Order O1 to Vehicle A.",
        dependencies=frozenset(
            {
                "vehicle_A.status",
                "vehicle_A.available",
                "vehicle_A.capacity",
                "order_O1.demand",
            }
        ),
    )

    d2 = DecisionNode(
        decision_id="D2",
        stage=2,
        description=(
            "Assign Order O2 to Vehicle B under current recovery "
            "and upstream assignment assumptions."
        ),
        dependencies=frozenset(
            {
                "vehicle_B.status",
                "vehicle_B.available",
                "vehicle_B.capacity",
                "order_O2.demand",
                "order_O2.deadline",
                "recovery_resource_available",
                "recovery_timing_valid",
                "upstream_assignment_assumptions_valid",
            }
        ),
    )

    d3 = DecisionNode(
        decision_id="D3",
        stage=3,
        description="Reserve Vehicle C as recovery support.",
        dependencies=frozenset(
            {
                "vehicle_C.status",
                "vehicle_C.available",
                "vehicle_C.capacity",
                "recovery_demand",
                "upstream_failure_state",
            }
        ),
    )

    d1_to_d2 = DecisionEdge(
        source_decision_id="D1",
        target_decision_id="D2",
        shared_dependencies=frozenset(
            {
                "recovery_resource_available",
                "recovery_timing_valid",
                "upstream_assignment_assumptions_valid",
            }
        ),
    )

    d1_to_d3 = DecisionEdge(
        source_decision_id="D1",
        target_decision_id="D3",
        shared_dependencies=frozenset(
            {
                "upstream_failure_state",
                "recovery_demand",
            }
        ),
    )

    d2_to_d3 = DecisionEdge(
        source_decision_id="D2",
        target_decision_id="D3",
        shared_dependencies=frozenset(
            {
                "recovery_demand",
            }
        ),
    )

    return DecisionChain(
        nodes=(d1, d2, d3),
        edges=(
            d1_to_d2,
            d1_to_d3,
            d2_to_d3,
        ),
    )
