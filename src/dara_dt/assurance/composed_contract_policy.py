"""Dependency-aware composed runtime contract for EXP-010.

This module implements the strongest runtime-contract comparator used in
the EXP-010 divergence-propagation study.

The comparator is deliberately allowed to reason over:

- direct decision dependencies;
- shared recovery dependencies;
- cross-entity dependencies;
- upstream assumptions;
- evidence quality.

It does not receive physical ground truth or divergence-propagation paths.

This creates the central EXP-010 comparison:

    strong dependency-aware composed contract
        versus
    propagation-aware DARA-DT

Both approaches must operate on equivalent observable runtime evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from dara_dt.assurance.model import (
    AssuranceDecision,
    AuthorityState,
)
from dara_dt.evidence.model import (
    EvidenceStatus,
    RuntimeEvidence,
)


class ContractEvaluation(str, Enum):
    """Result of evaluating one composed contract dependency."""

    SATISFIED = "satisfied"
    VIOLATED = "violated"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True, slots=True)
class DependencyRequirement:
    """Expected runtime condition for one dependency.

    Attributes:
        dependency:
            Canonical dependency identifier.

        expected_value:
            Value required by the contract.

        description:
            Human-readable explanation of the requirement.
    """

    dependency: str
    expected_value: object
    description: str


@dataclass(frozen=True, slots=True)
class DependencyEvaluation:
    """Evaluation result for one dependency requirement."""

    requirement: DependencyRequirement
    evaluation: ContractEvaluation
    evidence: RuntimeEvidence | None
    reason: str


@dataclass(frozen=True, slots=True)
class ComposedContractResult:
    """Detailed result of a composed runtime-contract evaluation."""

    decision_id: str
    evaluations: tuple[DependencyEvaluation, ...]
    assurance: AssuranceDecision

    @property
    def violated_dependencies(self) -> frozenset[str]:
        """Return dependencies whose runtime requirements are violated."""

        return frozenset(
            evaluation.requirement.dependency
            for evaluation in self.evaluations
            if evaluation.evaluation is ContractEvaluation.VIOLATED
        )

    @property
    def uncertain_dependencies(self) -> frozenset[str]:
        """Return dependencies whose runtime evidence is uncertain."""

        return frozenset(
            evaluation.requirement.dependency
            for evaluation in self.evaluations
            if evaluation.evaluation is ContractEvaluation.UNCERTAIN
        )

    @property
    def satisfied_dependencies(self) -> frozenset[str]:
        """Return dependencies whose requirements are satisfied."""

        return frozenset(
            evaluation.requirement.dependency
            for evaluation in self.evaluations
            if evaluation.evaluation is ContractEvaluation.SATISFIED
        )

    @property
    def intervene(self) -> bool:
        """Return whether autonomous execution is not fully allowed."""

        return self.assurance.authority is not AuthorityState.ALLOW


class DependencyAwareComposedContractPolicy:
    """Strong dependency-aware composed runtime-contract comparator.

    The policy evaluates all declared requirements for the pending decision.

    Decision semantics:

    - violated requirement -> RESTRICT
    - uncertain required evidence -> DEFER
    - all requirements satisfied -> ALLOW

    Violation takes precedence over uncertainty because a known contract
    violation already provides sufficient evidence that autonomous execution
    should not proceed.

    The policy intentionally knows about cross-decision and cross-entity
    dependencies when they have been explicitly declared in its contract.
    It does not know the physical ground-truth label and does not receive
    DARA-DT propagation paths.
    """

    def evaluate(
        self,
        *,
        decision_id: str,
        requirements: tuple[DependencyRequirement, ...],
        evidence: Mapping[str, RuntimeEvidence],
    ) -> ComposedContractResult:
        """Evaluate a composed contract for one pending decision."""

        evaluations = tuple(
            self._evaluate_requirement(
                requirement=requirement,
                evidence=evidence.get(requirement.dependency),
            )
            for requirement in requirements
        )

        violated = tuple(
            evaluation
            for evaluation in evaluations
            if evaluation.evaluation is ContractEvaluation.VIOLATED
        )

        uncertain = tuple(
            evaluation
            for evaluation in evaluations
            if evaluation.evaluation is ContractEvaluation.UNCERTAIN
        )

        if violated:
            authority = AuthorityState.RESTRICT
            reason = self._violation_reason(violated)

        elif uncertain:
            authority = AuthorityState.DEFER
            reason = self._uncertainty_reason(uncertain)

        else:
            authority = AuthorityState.ALLOW
            reason = (
                "All composed runtime-contract requirements are "
                "satisfied by available evidence."
            )

        assurance = AssuranceDecision(
            decision_id=decision_id,
            authority=authority,
            reason=reason,
            relevant_divergence_count=0,
        )

        return ComposedContractResult(
            decision_id=decision_id,
            evaluations=evaluations,
            assurance=assurance,
        )

    def _evaluate_requirement(
        self,
        *,
        requirement: DependencyRequirement,
        evidence: RuntimeEvidence | None,
    ) -> DependencyEvaluation:
        """Evaluate one dependency requirement."""

        if evidence is None:
            return DependencyEvaluation(
                requirement=requirement,
                evaluation=ContractEvaluation.UNCERTAIN,
                evidence=None,
                reason=(
                    f"No runtime evidence is available for "
                    f"{requirement.dependency}."
                ),
            )

        if evidence.dependency != requirement.dependency:
            raise ValueError(
                "Evidence dependency does not match contract requirement: "
                f"{evidence.dependency!r} != "
                f"{requirement.dependency!r}"
            )

        if evidence.status is EvidenceStatus.MISSING:
            return DependencyEvaluation(
                requirement=requirement,
                evaluation=ContractEvaluation.UNCERTAIN,
                evidence=evidence,
                reason=(
                    f"Evidence for {requirement.dependency} is missing."
                ),
            )

        if evidence.status is EvidenceStatus.STALE:
            return DependencyEvaluation(
                requirement=requirement,
                evaluation=ContractEvaluation.UNCERTAIN,
                evidence=evidence,
                reason=(
                    f"Evidence for {requirement.dependency} is stale."
                ),
            )

        if evidence.status is EvidenceStatus.CONFLICTING:
            return DependencyEvaluation(
                requirement=requirement,
                evaluation=ContractEvaluation.UNCERTAIN,
                evidence=evidence,
                reason=(
                    f"Evidence for {requirement.dependency} is conflicting."
                ),
            )

        if evidence.observed_value != requirement.expected_value:
            return DependencyEvaluation(
                requirement=requirement,
                evaluation=ContractEvaluation.VIOLATED,
                evidence=evidence,
                reason=(
                    f"{requirement.dependency} violates its contract: "
                    f"observed={evidence.observed_value!r}, "
                    f"expected={requirement.expected_value!r}."
                ),
            )

        return DependencyEvaluation(
            requirement=requirement,
            evaluation=ContractEvaluation.SATISFIED,
            evidence=evidence,
            reason=(
                f"{requirement.dependency} satisfies its "
                "runtime requirement."
            ),
        )

    @staticmethod
    def _violation_reason(
        evaluations: tuple[DependencyEvaluation, ...],
    ) -> str:
        """Build deterministic explanation for violated requirements."""

        dependencies = ", ".join(
            sorted(
                evaluation.requirement.dependency
                for evaluation in evaluations
            )
        )

        return (
            "Composed runtime contract violated for required "
            f"dependencies: {dependencies}."
        )

    @staticmethod
    def _uncertainty_reason(
        evaluations: tuple[DependencyEvaluation, ...],
    ) -> str:
        """Build deterministic explanation for uncertain requirements."""

        dependencies = ", ".join(
            sorted(
                evaluation.requirement.dependency
                for evaluation in evaluations
            )
        )

        return (
            "Composed runtime contract cannot be established because "
            f"required evidence is uncertain: {dependencies}."
        )


def exp010_d1_requirements() -> tuple[DependencyRequirement, ...]:
    """Return the preregistered composed requirements for D1."""

    return (
        DependencyRequirement(
            dependency="vehicle_A.status",
            expected_value="operational",
            description="Vehicle A must remain operational.",
        ),
        DependencyRequirement(
            dependency="vehicle_A.available",
            expected_value=True,
            description="Vehicle A must remain available.",
        ),
        DependencyRequirement(
            dependency="vehicle_A.capacity_sufficient",
            expected_value=True,
            description=(
                "Vehicle A must retain sufficient capacity for Order O1."
            ),
        ),
        DependencyRequirement(
            dependency="order_O1.waiting",
            expected_value=True,
            description="Order O1 must remain eligible for assignment.",
        ),
    )


def exp010_d2_requirements() -> tuple[DependencyRequirement, ...]:
    """Return the strong preregistered composed requirements for D2.

    D2 deliberately includes both direct Vehicle B requirements and the
    shared upstream/recovery assumptions declared in the EXP-010 design.
    """

    return (
        DependencyRequirement(
            dependency="vehicle_B.status",
            expected_value="operational",
            description="Vehicle B must remain operational.",
        ),
        DependencyRequirement(
            dependency="vehicle_B.available",
            expected_value=True,
            description="Vehicle B must remain available.",
        ),
        DependencyRequirement(
            dependency="vehicle_B.capacity_sufficient",
            expected_value=True,
            description=(
                "Vehicle B must retain sufficient capacity for Order O2."
            ),
        ),
        DependencyRequirement(
            dependency="order_O2.waiting",
            expected_value=True,
            description="Order O2 must remain eligible for assignment.",
        ),
        DependencyRequirement(
            dependency="order_O2.deadline_valid",
            expected_value=True,
            description=(
                "Order O2 must remain feasible within its deadline."
            ),
        ),
        DependencyRequirement(
            dependency="recovery_resource_available",
            expected_value=True,
            description=(
                "Required recovery resources must remain available."
            ),
        ),
        DependencyRequirement(
            dependency="recovery_timing_valid",
            expected_value=True,
            description=(
                "Recovery timing must remain valid for D2."
            ),
        ),
        DependencyRequirement(
            dependency="upstream_assignment_assumptions_valid",
            expected_value=True,
            description=(
                "Assumptions inherited from upstream assignments "
                "must remain valid."
            ),
        ),
        DependencyRequirement(
            dependency="vehicle_C.available",
            expected_value=True,
            description=(
                "Recovery Vehicle C must be available when the composed "
                "decision contract requires it."
            ),
        ),
        DependencyRequirement(
            dependency="vehicle_B.assignment_valid",
            expected_value=True,
            description=(
                "Vehicle B's downstream assignment must remain valid."
            ),
        ),
    )


def exp010_d3_requirements() -> tuple[DependencyRequirement, ...]:
    """Return the preregistered composed requirements for D3."""

    return (
        DependencyRequirement(
            dependency="vehicle_C.status",
            expected_value="operational",
            description="Recovery Vehicle C must remain operational.",
        ),
        DependencyRequirement(
            dependency="vehicle_C.available",
            expected_value=True,
            description="Recovery Vehicle C must remain available.",
        ),
        DependencyRequirement(
            dependency="vehicle_C.capacity_sufficient",
            expected_value=True,
            description=(
                "Vehicle C must have sufficient recovery capacity."
            ),
        ),
        DependencyRequirement(
            dependency="recovery_demand_supported",
            expected_value=True,
            description=(
                "The current recovery demand must be supportable."
            ),
        ),
        DependencyRequirement(
            dependency="upstream_failure_state_known",
            expected_value=True,
            description=(
                "The upstream failure state required by D3 must "
                "be established."
            ),
        ),
    )


def exp010_requirements_for_decision(
    decision_id: str,
) -> tuple[DependencyRequirement, ...]:
    """Return the frozen composed contract for an EXP-010 decision."""

    requirements = {
        "D1": exp010_d1_requirements,
        "D2": exp010_d2_requirements,
        "D3": exp010_d3_requirements,
    }

    try:
        factory = requirements[decision_id]
    except KeyError as exc:
        raise KeyError(
            f"Unknown EXP-010 decision: {decision_id}"
        ) from exc

    return factory()
