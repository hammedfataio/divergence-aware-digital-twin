"""Propagation analysis for EXP-010.

The analyser determines whether an observed physical-digital divergence
has a declared relationship to a pending decision in the EXP-010
multi-stage decision chain.

It does NOT:

- decide whether assurance should intervene;
- inspect experimental ground-truth labels;
- infer safety from physical validity;
- modify the existing DependencyMapper;
- give DARA-DT access to evidence unavailable to comparator policies.

Its responsibility is limited to representing and tracing declared
divergence-propagation relationships.
"""

from __future__ import annotations

from dataclasses import dataclass

from dara_dt.propagation.model import (
    DecisionChain,
    DivergenceOrigin,
    PropagationPath,
    PropagationStep,
    PropagationType,
)


@dataclass(frozen=True, slots=True)
class PropagationRule:
    """A declared relationship between divergence and a later dependency.

    Attributes:
        origin_dependency:
            Dependency at which physical-digital divergence originates.

        source_decision_id:
            Decision associated with the divergence origin.

        target_decision_id:
            Decision whose dependency or assumption may be affected.

        affected_dependencies:
            Downstream dependencies affected by the relationship.

        propagation_type:
            Direct, non-propagating, propagating, or compound.

        description:
            Human-readable explanation of the relationship.
    """

    origin_dependency: str
    source_decision_id: str
    target_decision_id: str
    affected_dependencies: tuple[str, ...]
    propagation_type: PropagationType
    description: str

    @property
    def is_propagating(self) -> bool:
        """Return whether this rule represents downstream propagation."""

        return self.propagation_type in {
            PropagationType.PROPAGATING,
            PropagationType.COMPOUND,
        }

    @property
    def is_compound(self) -> bool:
        """Return whether this rule affects multiple dependencies."""

        return self.propagation_type is PropagationType.COMPOUND


@dataclass(frozen=True, slots=True)
class PropagationAnalysis:
    """Result of analysing one divergence against one pending decision."""

    origin: DivergenceOrigin
    pending_decision_id: str
    matched_rules: tuple[PropagationRule, ...]
    paths: tuple[PropagationPath, ...]

    @property
    def has_divergence(self) -> bool:
        """Return whether the supplied origin is physically divergent."""

        return self.origin.is_divergent

    @property
    def has_matching_rule(self) -> bool:
        """Return whether any declared relationship matched."""

        return bool(self.matched_rules)

    @property
    def is_propagating(self) -> bool:
        """Return whether any matched path represents propagation."""

        return any(path.is_propagating for path in self.paths)

    @property
    def is_compound(self) -> bool:
        """Return whether any matched path is compound."""

        return any(path.is_compound for path in self.paths)

    @property
    def affected_dependencies(self) -> frozenset[str]:
        """Return all dependencies affected by matched paths."""

        return frozenset(
            dependency
            for path in self.paths
            for dependency in path.affected_dependencies
        )

    @property
    def affected_decisions(self) -> frozenset[str]:
        """Return all decisions reached by matched paths."""

        return frozenset(
            decision_id
            for path in self.paths
            for decision_id in path.affected_decisions
        )


class DivergencePropagationAnalyser:
    """Trace declared divergence relationships through a decision chain.

    The analyser is intentionally deterministic. Relationships are supplied
    explicitly as rules rather than learned from EXP-010 ground-truth
    outcomes.

    This separation is important because EXP-010 is testing whether explicit
    propagation information contributes assurance information beyond strong
    runtime contracts. The analyser must therefore describe propagation,
    not encode the desired assurance result.
    """

    def __init__(
        self,
        chain: DecisionChain,
        rules: tuple[PropagationRule, ...],
    ) -> None:
        self._chain = chain
        self._rules = rules
        self._validate_rules()

    @property
    def chain(self) -> DecisionChain:
        """Return the decision chain used by the analyser."""

        return self._chain

    @property
    def rules(self) -> tuple[PropagationRule, ...]:
        """Return immutable propagation rules."""

        return self._rules

    def analyse(
        self,
        origin: DivergenceOrigin,
        pending_decision_id: str,
    ) -> PropagationAnalysis:
        """Analyse an origin against a pending decision.

        A rule can match only when:

        1. the physical and Digital Twin values actually diverge;
        2. the rule's origin dependency equals the observed origin;
        3. the rule targets the pending decision.

        No ground-truth intervention label is consulted.
        """

        self._chain.node(pending_decision_id)

        if not origin.is_divergent:
            return PropagationAnalysis(
                origin=origin,
                pending_decision_id=pending_decision_id,
                matched_rules=(),
                paths=(),
            )

        matched_rules = tuple(
            rule
            for rule in self._rules
            if rule.origin_dependency == origin.dependency
            and rule.target_decision_id == pending_decision_id
        )

        paths = tuple(
            self._path_from_rule(
                origin=origin,
                rule=rule,
            )
            for rule in matched_rules
        )

        return PropagationAnalysis(
            origin=origin,
            pending_decision_id=pending_decision_id,
            matched_rules=matched_rules,
            paths=paths,
        )

    def rules_for_origin(
        self,
        origin_dependency: str,
    ) -> tuple[PropagationRule, ...]:
        """Return rules associated with one divergence origin."""

        return tuple(
            rule
            for rule in self._rules
            if rule.origin_dependency == origin_dependency
        )

    def rules_for_decision(
        self,
        decision_id: str,
    ) -> tuple[PropagationRule, ...]:
        """Return rules targeting one decision."""

        self._chain.node(decision_id)

        return tuple(
            rule
            for rule in self._rules
            if rule.target_decision_id == decision_id
        )

    def _path_from_rule(
        self,
        origin: DivergenceOrigin,
        rule: PropagationRule,
    ) -> PropagationPath:
        """Convert a declared rule into a propagation path."""

        steps = tuple(
            PropagationStep(
                source_decision_id=rule.source_decision_id,
                target_decision_id=rule.target_decision_id,
                source_dependency=rule.origin_dependency,
                affected_dependency=dependency,
                description=rule.description,
            )
            for dependency in rule.affected_dependencies
        )

        return PropagationPath(
            origin=origin,
            propagation_type=rule.propagation_type,
            steps=steps,
        )

    def _validate_rules(self) -> None:
        """Validate rule structure against the supplied decision chain."""

        for rule in self._rules:
            source = self._chain.node(rule.source_decision_id)
            target = self._chain.node(rule.target_decision_id)

            if not rule.origin_dependency:
                raise ValueError(
                    "PropagationRule origin_dependency cannot be empty."
                )

            if not rule.affected_dependencies:
                raise ValueError(
                    "PropagationRule must contain at least one "
                    "affected dependency."
                )

            if source.stage > target.stage:
                raise ValueError(
                    "PropagationRule cannot point backwards in the "
                    "decision chain."
                )

            if (
                rule.propagation_type
                in {
                    PropagationType.PROPAGATING,
                    PropagationType.COMPOUND,
                }
                and source.stage >= target.stage
            ):
                raise ValueError(
                    "Propagating rules must cross from an earlier "
                    "decision to a later decision."
                )

            if (
                rule.propagation_type is PropagationType.COMPOUND
                and len(rule.affected_dependencies) < 2
            ):
                raise ValueError(
                    "Compound propagation must affect at least two "
                    "dependencies."
                )


def build_exp010_propagation_rules() -> tuple[PropagationRule, ...]:
    """Build the pre-declared propagation relationships for EXP-010.

    These rules encode the causal/dependency structure being tested.
    They do not contain experimental ground-truth labels.

    F2 non-propagating cases intentionally have no propagation rule.
    Their divergence can therefore exist without automatically reaching D2.

    Direct F1 relationships are represented separately from cross-decision
    propagation so direct divergence remains distinguishable from F3/F4.
    """

    return (
        # ---------------------------------------------------------------
        # F1-style direct decision dependencies
        # ---------------------------------------------------------------
        PropagationRule(
            origin_dependency="vehicle_A.status",
            source_decision_id="D1",
            target_decision_id="D1",
            affected_dependencies=("vehicle_A.status",),
            propagation_type=PropagationType.DIRECT,
            description=(
                "Vehicle A status is a direct dependency of D1."
            ),
        ),
        PropagationRule(
            origin_dependency="vehicle_A.capacity",
            source_decision_id="D1",
            target_decision_id="D1",
            affected_dependencies=("vehicle_A.capacity",),
            propagation_type=PropagationType.DIRECT,
            description=(
                "Vehicle A capacity is a direct dependency of D1."
            ),
        ),
        PropagationRule(
            origin_dependency="vehicle_A.available",
            source_decision_id="D1",
            target_decision_id="D1",
            affected_dependencies=("vehicle_A.available",),
            propagation_type=PropagationType.DIRECT,
            description=(
                "Vehicle A availability is a direct dependency of D1."
            ),
        ),

        # ---------------------------------------------------------------
        # F3-style upstream propagation into D2
        # ---------------------------------------------------------------
        PropagationRule(
            origin_dependency="vehicle_A.status",
            source_decision_id="D1",
            target_decision_id="D2",
            affected_dependencies=("recovery_resource_available",),
            propagation_type=PropagationType.PROPAGATING,
            description=(
                "Vehicle A failure can change the recovery-resource "
                "assumption required by D2."
            ),
        ),
        PropagationRule(
            origin_dependency="vehicle_A.available",
            source_decision_id="D1",
            target_decision_id="D2",
            affected_dependencies=("recovery_resource_available",),
            propagation_type=PropagationType.PROPAGATING,
            description=(
                "Vehicle A unavailability can change the recovery-resource "
                "assumption required by D2."
            ),
        ),
        PropagationRule(
            origin_dependency="vehicle_A.location",
            source_decision_id="D1",
            target_decision_id="D2",
            affected_dependencies=("recovery_timing_valid",),
            propagation_type=PropagationType.PROPAGATING,
            description=(
                "Vehicle A location divergence can change downstream "
                "recovery timing for D2."
            ),
        ),

        # ---------------------------------------------------------------
        # F4-style compound propagation
        # ---------------------------------------------------------------
        PropagationRule(
            origin_dependency="vehicle_A.status",
            source_decision_id="D1",
            target_decision_id="D2",
            affected_dependencies=(
                "vehicle_C.available",
                "vehicle_B.assignment",
            ),
            propagation_type=PropagationType.COMPOUND,
            description=(
                "Vehicle A failure can propagate through recovery Vehicle C "
                "availability and Vehicle B assignment assumptions."
            ),
        ),
        PropagationRule(
            origin_dependency="vehicle_A.status",
            source_decision_id="D1",
            target_decision_id="D3",
            affected_dependencies=(
                "vehicle_C.capacity",
                "recovery_demand",
            ),
            propagation_type=PropagationType.COMPOUND,
            description=(
                "Vehicle A failure can propagate into Vehicle C capacity "
                "requirements and recovery demand."
            ),
        ),
        PropagationRule(
            origin_dependency="vehicle_A.location",
            source_decision_id="D1",
            target_decision_id="D2",
            affected_dependencies=(
                "recovery_timing",
                "vehicle_B.deadline",
            ),
            propagation_type=PropagationType.COMPOUND,
            description=(
                "Vehicle A location divergence can propagate through "
                "recovery timing and the downstream deadline assumption."
            ),
        ),
    )


def build_exp010_propagation_analyser(
    chain: DecisionChain,
) -> DivergencePropagationAnalyser:
    """Build the EXP-010 analyser using the frozen rule structure."""

    return DivergencePropagationAnalyser(
        chain=chain,
        rules=build_exp010_propagation_rules(),
    )
