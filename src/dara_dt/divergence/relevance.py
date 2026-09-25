"""Decision-relevant divergence analysis for DARA-DT."""

from dataclasses import dataclass

from dara_dt.decision.dependency import DependencyMapper
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import Divergence


@dataclass(frozen=True)
class RelevanceResult:
    """Result of matching divergences to a decision's dependencies."""

    decision_id: str
    relevant: tuple[Divergence, ...]
    irrelevant: tuple[Divergence, ...]

    @property
    def has_relevant_divergence(self) -> bool:
        """Return True when at least one divergence affects the decision."""
        return bool(self.relevant)


class DecisionRelevanceAnalyzer:
    """Determine which divergences are relevant to a specific decision."""

    def __init__(self, dependency_mapper: DependencyMapper) -> None:
        self.dependency_mapper = dependency_mapper

    def analyse(
        self,
        decision: Decision,
        divergences: list[Divergence],
    ) -> RelevanceResult:
        """Match detected divergences against decision dependencies."""

        dependencies = self.dependency_mapper.dependencies(decision)

        relevant = tuple(
            divergence
            for divergence in divergences
            if divergence.path in dependencies
        )

        irrelevant = tuple(
            divergence
            for divergence in divergences
            if divergence.path not in dependencies
        )

        return RelevanceResult(
            decision_id=decision.decision_id,
            relevant=relevant,
            irrelevant=irrelevant,
        )
