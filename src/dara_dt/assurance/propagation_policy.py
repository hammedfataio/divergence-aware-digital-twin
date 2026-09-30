"""Propagation-aware DARA-DT assurance policy for EXP-010.

This module implements the EXP-010 P4 policy.

P4 combines:

1. the same observable runtime evidence available to P3;
2. the same dependency requirements available to P3;
3. explicit physical-digital divergence propagation provenance.

The policy never receives physical ground truth.

Scientific fairness rule
------------------------
P3 and P4 must apply the same base runtime-contract semantics:

- known violated requirement -> RESTRICT
- missing, stale, conflicting, or absent required evidence -> DEFER
- all required evidence available and satisfied -> ALLOW

Propagation information may explain which dependencies were reached by a
physical-digital divergence, but propagation alone must not create an
intervention that the observable evidence cannot support.

This design intentionally allows EXP-010 to produce equivalence between
P3 and P4. Such equivalence is scientifically meaningful and must not be
prevented by implementation choices.
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

    P4 deliberately preserves the base assurance semantics of the strong
    P3 dependency-aware composed runtime contract.

    Decision semantics:

    known violated required dependency
        -> RESTRICT

    uncertain required evidence
        -> DEFER

    all required evidence available and satisfied
        -> ALLOW

    Propagation is retained as explicit runtime provenance. It identifies
    which evaluated dependencies are connected to the physical-digital
    divergence and supports propagation-specific analysis.

    Propagation itself is not sufficient grounds for intervention.

    This prevents the implementation from manufacturing an advantage for
    DARA-DT merely because P4 has an explicit propagation graph.
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

        self._validate_propagation_contract_parity(
            requirements=requirements,
            propagation=propagation,
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

        if violated:
            authority = AuthorityState.RESTRICT
            reason = self._violation_reason(violated)

        elif uncertain:
            authority = AuthorityState.DEFER
            reason = self._uncertainty_reason(uncertain)

        else:
            authority = AuthorityState.ALLOW
            reason = self._allow_reason(
                propagation=propagation,
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
        """Evaluate one requirement using P3-equivalent evidence semantics."""

        affected = (
            requirement.dependency
            in propagation.affected_dependencies
        )

        if evidence is None:
            return PropagationDependencyEvaluation(
                requirement=requirement,
                evaluation=PropagationEvaluation.UNCERTAIN,
                evidence=None,
                affected_by_propagation=affected,
                reason=(
                    f"No runtime evidence is available for "
                    f"{requirement.dependency}."
                ),
            )

        if evidence.dependency != requirement.dependency:
            raise ValueError(
                "Evidence dependency does not match requirement: "
                f"{evidence.dependency!r} != "
                f"{requirement.dependency!r}"
            )

        if evidence.status is EvidenceStatus.MISSING:
            return PropagationDependencyEvaluation(
                requirement=requirement,
                evaluation=PropagationEvaluation.UNCERTAIN,
                evidence=evidence,
                affected_by_propagation=affected,
                reason=(
                    f"Evidence for {requirement.dependency} is missing."
                ),
            )

        if evidence.status is EvidenceStatus.STALE:
            return PropagationDependencyEvaluation(
                requirement=requirement,
                evaluation=PropagationEvaluation.UNCERTAIN,
                evidence=evidence,
                affected_by_propagation=affected,
                reason=(
                    f"Evidence for {requirement.dependency} is stale."
                ),
            )

        if evidence.status is EvidenceStatus.CONFLICTING:
            return PropagationDependencyEvaluation(
                requirement=requirement,
                evaluation=PropagationEvaluation.UNCERTAIN,
                evidence=evidence,
                affected_by_propagation=affected,
                reason=(
                    f"Evidence for {requirement.dependency} is "
                    "conflicting."
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
    def _validate_propagation_contract_parity(
        *,
        requirements: tuple[DependencyRequirement, ...],
        propagation: PropagationAnalysis,
    ) -> None:
        """Protect the EXP-010 P3/P4 comparison from hidden P4 advantages.

        The propagation analyser may use descriptive dependency names that
        are more granular than the executable composed contract. Therefore
        propagation-only dependencies are permitted as provenance.

        They must not independently alter authority.

        Any runtime condition used by P4 to RESTRICT or DEFER must be
        represented by an explicit requirement and observable evidence,
        exactly as it is for P3.
        """

        requirement_dependencies = {
            requirement.dependency
            for requirement in requirements
        }

        if len(requirement_dependencies) != len(requirements):
            raise ValueError(
                "Duplicate dependency requirements are not permitted."
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
        """Build deterministic explanation for uncertain required evidence."""

        dependencies = ", ".join(
            sorted(
                evaluation.requirement.dependency
                for evaluation in evaluations
            )
        )

        return (
            "Autonomous authority is deferred because required runtime "
            f"evidence is uncertain for: {dependencies}."
        )

    @staticmethod
    def _allow_reason(
        *,
        propagation: PropagationAnalysis,
    ) -> str:
        """Build deterministic explanation for autonomous execution."""

        if propagation.is_propagating:
            return (
                "A physical-digital divergence propagation path is "
                "observed, but all executable runtime-contract "
                "requirements are satisfied by available evidence."
            )

        return (
            "All executable runtime-contract requirements are satisfied "
            "by available evidence and no actionable propagation-aware "
            "condition requires intervention."
        )


def contract_evaluation_to_propagation(
    evaluation: ContractEvaluation,
) -> PropagationEvaluation:
    """Translate shared P3/P4 contract-evaluation terminology."""

    mapping = {
        ContractEvaluation.SATISFIED:
            PropagationEvaluation.SATISFIED,
        ContractEvaluation.VIOLATED:
            PropagationEvaluation.VIOLATED,
        ContractEvaluation.UNCERTAIN:
            PropagationEvaluation.UNCERTAIN,
    }

    return mapping[evaluation]
