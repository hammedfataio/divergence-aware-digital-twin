"""Propagation-aware DARA-DT assurance policy for EXP-010.

This module implements the EXP-010 P4 policy.

The policy combines:

1. observable runtime evidence;
2. explicit divergence-propagation analysis;
3. dependency requirements for the pending decision.

It does not receive physical ground truth.

EXP-010 compares this policy against the strong dependency-aware composed
runtime contract. Both policies must receive equivalent observable runtime
evidence.

The scientific question is therefore not whether DARA-DT has access to
more sensor information. It is whether explicit knowledge of divergence
origin and propagation contributes useful runtime-assurance information
beyond a strong composed contract operating on the same evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from dara_dt.assurance.composed_contract_policy import (
    ContractEvaluation,
    DependencyRequirement,
)
from dara_dt.assurance.model import (
    AssuranceDecision,
    AuthorityState,
)
from dara_dt.evidence.model import (
    EvidenceStatus,
    RuntimeEvidence,
)
from dara_dt.propagation.analyser import PropagationAnalysis


class PropagationEvaluation(str, Enum):
    """Classification of one propagation-aware dependency evaluation."""

    SATISFIED = "satisfied"
    VIOLATED = "violated"
    UNCERTAIN = "uncertain"
    NOT_AFFECTED = "not_affected"


@dataclass(frozen=True, slots=True)
class PropagationDependencyEvaluation:
    """Evaluation of one dependency in propagation context."""

    requirement: DependencyRequirement
    evaluation: PropagationEvaluation
    evidence: RuntimeEvidence | None
    affected_by_propagation: bool
    reason: str


@dataclass(frozen=True, slots=True)
class PropagationAssuranceResult:
    """Detailed result returned by the propagation-aware policy."""

    decision_id: str
    propagation: PropagationAnalysis
    evaluations: tuple[PropagationDependencyEvaluation, ...]
    assurance: AssuranceDecision

    @property
    def violated_dependencies(self) -> frozenset[str]:
        """Return violated runtime dependencies."""

        return frozenset(
            evaluation.requirement.dependency
            for evaluation in self.evaluations
            if evaluation.evaluation is PropagationEvaluation.VIOLATED
        )

    @property
    def uncertain_dependencies(self) -> frozenset[str]:
        """Return dependencies whose runtime evidence is uncertain."""

        return frozenset(
            evaluation.requirement.dependency
            for evaluation in self.evaluations
            if evaluation.evaluation is PropagationEvaluation.UNCERTAIN
        )

    @property
    def propagation_affected_dependencies(self) -> frozenset[str]:
        """Return evaluated dependencies reached by propagation."""

        return frozenset(
            evaluation.requirement.dependency
            for evaluation in self.evaluations
            if evaluation.affected_by_propagation
        )

    @property
    def intervene(self) -> bool:
        """Return whether autonomous execution is not fully allowed."""

        return self.assurance.authority is not AuthorityState.ALLOW


class PropagationAwareAssurancePolicy:
    """EXP-010 propagation-aware DARA-DT policy.

    Decision semantics:

    known violated required dependency
        -> RESTRICT

    uncertain evidence for a propagation-affected dependency
        -> DEFER

    propagation reaches the pending decision but cannot be evaluated
    through an observable required dependency
        -> DEFER

    otherwise
        -> ALLOW

    A propagation path alone is not automatically treated as evidence of
    invalidity. This prevents the policy from collapsing into:

        divergence exists -> propagation exists -> intervene

    Instead, the policy must connect propagation to the pending decision
    and its runtime evidence.
    """

    def evaluate(
        self,
        *,
        decision_id: str,
        requirements: tuple[DependencyRequirement, ...],
        evidence: Mapping[str, RuntimeEvidence],
        propagation: PropagationAnalysis,
    ) -> PropagationAssuranceResult:
        """Evaluate a pending decision using evidence and propagation."""

        if propagation.pending_decision_id != decision_id:
            raise ValueError(
                "Propagation analysis does not correspond to the "
                f"pending decision: {propagation.pending_decision_id!r} "
                f"!= {decision_id!r}"
            )

        evaluations = tuple(
            self._evaluate_requirement(
                requirement=requirement,
                evidence=evidence.get(requirement.dependency),
                propagation=propagation,
            )
            for requirement in requirements
        )

        violated = tuple(
            evaluation
            for evaluation in evaluations
            if evaluation.evaluation is PropagationEvaluation.VIOLATED
        )

        uncertain = tuple(
            evaluation
            for evaluation in evaluations
            if evaluation.evaluation is PropagationEvaluation.UNCERTAIN
        )

        requirement_dependencies = {
            requirement.dependency
            for requirement in requirements
        }

        propagated_dependencies = propagation.affected_dependencies

        unresolved_propagation = (
            propagation.is_propagating
            and bool(
                propagated_dependencies
                - requirement_dependencies
            )
        )

        if violated:
            authority = AuthorityState.RESTRICT
            reason = self._violation_reason(violated)

        elif uncertain:
            authority = AuthorityState.DEFER
            reason = self._uncertainty_reason(uncertain)

        elif unresolved_propagation:
            authority = AuthorityState.DEFER
            reason = (
                "Physical-digital divergence propagates to the pending "
                "decision through dependencies not established by the "
                "current observable runtime contract."
            )

        else:
            authority = AuthorityState.ALLOW
            reason = (
                "No observable propagation-aware runtime condition "
                "requires restriction of autonomous authority."
            )

        assurance = AssuranceDecision(
            decision_id=decision_id,
            authority=authority,
            reason=reason,
            relevant_divergence_count=len(
                propagation.affected_dependencies
            ),
        )

        return PropagationAssuranceResult(
            decision_id=decision_id,
            propagation=propagation,
            evaluations=evaluations,
            assurance=assurance,
        )

    def _evaluate_requirement(
        self,
        *,
        requirement: DependencyRequirement,
        evidence: RuntimeEvidence | None,
        propagation: PropagationAnalysis,
    ) -> PropagationDependencyEvaluation:
        """Evaluate one requirement in propagation context."""

        affected = (
            requirement.dependency
            in propagation.affected_dependencies
        )

        if evidence is None:
            if affected:
                return PropagationDependencyEvaluation(
                    requirement=requirement,
                    evaluation=PropagationEvaluation.UNCERTAIN,
                    evidence=None,
                    affected_by_propagation=True,
                    reason=(
                        "Propagation reaches "
                        f"{requirement.dependency}, but no runtime "
                        "evidence is available."
                    ),
                )

            return PropagationDependencyEvaluation(
                requirement=requirement,
                evaluation=PropagationEvaluation.NOT_AFFECTED,
                evidence=None,
                affected_by_propagation=False,
                reason=(
                    f"No propagation reaches {requirement.dependency}."
                ),
            )

        if evidence.dependency != requirement.dependency:
            raise ValueError(
                "Evidence dependency does not match requirement: "
                f"{evidence.dependency!r} != "
                f"{requirement.dependency!r}"
            )

        if evidence.status in {
            EvidenceStatus.MISSING,
            EvidenceStatus.STALE,
            EvidenceStatus.CONFLICTING,
        }:
            if affected:
                return PropagationDependencyEvaluation(
                    requirement=requirement,
                    evaluation=PropagationEvaluation.UNCERTAIN,
                    evidence=evidence,
                    affected_by_propagation=True,
                    reason=(
                        f"Propagation reaches {requirement.dependency}, "
                        "but its runtime evidence is "
                        f"{evidence.status.value}."
                    ),
                )

            return PropagationDependencyEvaluation(
                requirement=requirement,
                evaluation=PropagationEvaluation.NOT_AFFECTED,
                evidence=evidence,
                affected_by_propagation=False,
                reason=(
                    f"Evidence for {requirement.dependency} is "
                    f"{evidence.status.value}, but the dependency is "
                    "not reached by the observed propagation path."
                ),
            )

        if evidence.observed_value != requirement.expected_value:
            return PropagationDependencyEvaluation(
                requirement=requirement,
                evaluation=PropagationEvaluation.VIOLATED,
                evidence=evidence,
                affected_by_propagation=affected,
                reason=(
                    f"{requirement.dependency} violates its runtime "
                    "requirement: "
                    f"observed={evidence.observed_value!r}, "
                    f"expected={requirement.expected_value!r}."
                ),
            )

        return PropagationDependencyEvaluation(
            requirement=requirement,
            evaluation=PropagationEvaluation.SATISFIED,
            evidence=evidence,
            affected_by_propagation=affected,
            reason=(
                f"{requirement.dependency} satisfies its runtime "
                "requirement."
            ),
        )

    @staticmethod
    def _violation_reason(
        evaluations: tuple[
            PropagationDependencyEvaluation,
            ...
        ],
    ) -> str:
        """Build deterministic explanation for known violations."""

        dependencies = ", ".join(
            sorted(
                evaluation.requirement.dependency
                for evaluation in evaluations
            )
        )

        return (
            "Propagation-aware runtime requirements are violated for: "
            f"{dependencies}."
        )

    @staticmethod
    def _uncertainty_reason(
        evaluations: tuple[
            PropagationDependencyEvaluation,
            ...
        ],
    ) -> str:
        """Build deterministic explanation for relevant uncertainty."""

        dependencies = ", ".join(
            sorted(
                evaluation.requirement.dependency
                for evaluation in evaluations
            )
        )

        return (
            "Autonomous authority is deferred because "
            "propagation-relevant runtime evidence is uncertain for: "
            f"{dependencies}."
        )


def contract_evaluation_to_propagation(
    evaluation: ContractEvaluation,
) -> PropagationEvaluation:
    """Translate shared contract semantics when required by experiments.

    This helper makes the relationship between P3 and P4 evaluation
    terminology explicit without coupling either policy implementation
    to the other's decision procedure.
    """

    mapping = {
        ContractEvaluation.SATISFIED:
            PropagationEvaluation.SATISFIED,
        ContractEvaluation.VIOLATED:
            PropagationEvaluation.VIOLATED,
        ContractEvaluation.UNCERTAIN:
            PropagationEvaluation.UNCERTAIN,
    }

    return mapping[evaluation]
