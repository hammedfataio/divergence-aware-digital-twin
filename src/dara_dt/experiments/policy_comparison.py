"""Comparative assurance-policy experiment for DARA-DT."""

from dataclasses import dataclass

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.model import AssuranceDecision
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence
from dara_dt.divergence.relevance import DecisionRelevanceAnalyzer
from dara_dt.evaluation.outcomes import (
    OutcomeEvaluator,
    OutcomeResult,
)
from dara_dt.experiments.ground_truth import GroundTruth


@dataclass(frozen=True)
class PolicyComparisonResult:
    """Outcomes produced by the three assurance strategies."""

    no_assurance: OutcomeResult
    global_divergence: OutcomeResult
    dara_dt: OutcomeResult


def compare_policies(
    decision: Decision,
    divergences: list[Divergence],
    ground_truth: GroundTruth,
) -> PolicyComparisonResult:
    """Compare B0, B1 and DARA-DT on the same decision."""

    relevance = DecisionRelevanceAnalyzer(
        DependencyMapper()
    ).analyse(
        decision,
        divergences,
    )

    no_assurance: AssuranceDecision = (
        NoAssurancePolicy().evaluate(
            decision,
            divergences,
        )
    )

    global_divergence: AssuranceDecision = (
        AnyDivergencePolicy().evaluate(
            decision,
            divergences,
        )
    )

    dara_dt: AssuranceDecision = (
        DivergenceAwarePolicy().evaluate(
            decision,
            relevance,
        )
    )

    evaluator = OutcomeEvaluator()

    return PolicyComparisonResult(
        no_assurance=evaluator.evaluate(
            ground_truth,
            no_assurance,
        ),
        global_divergence=evaluator.evaluate(
            ground_truth,
            global_divergence,
        ),
        dara_dt=evaluator.evaluate(
            ground_truth,
            dara_dt,
        ),
    )
