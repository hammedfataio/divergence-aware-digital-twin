"""Live scenario service for the DARA-DT research demonstrator.

This module exposes individual frozen EXP-010 conditions through the
application layer.

It deliberately reuses the existing experimental engine rather than
reimplementing assurance logic inside the API.

Important separation
--------------------
The scenario service executes an existing frozen condition and translates
its result into API-facing models.

It does not:

- modify the frozen EXP-010 matrix;
- change physical ground truth;
- create new experimental evidence;
- give DARA-DT information unavailable to the composed-contract comparator;
- change assurance-policy behaviour.
"""

from __future__ import annotations

from dara_dt.api.schemas import (
    AIDecision,
    AssuranceResult,
    DecisionDependency,
    DivergenceRecord,
    EntityState,
    EvaluationResult,
    GroundTruthResult,
    PropagationRecord,
    RuntimeEvidenceRecord,
    ScenarioResponse,
    SystemState,
)
from dara_dt.assurance.model import AssuranceDecision, AuthorityState
from dara_dt.evaluation.outcomes import OutcomeResult
from dara_dt.experiments.divergence_propagation_conditions import (
    EXP010_CONDITIONS,
    PropagationCondition,
    condition_by_id,
)
from dara_dt.experiments.divergence_propagation_experiment import (
    DivergencePropagationExperimentResult,
    run_condition,
)


class ScenarioNotFoundError(ValueError):
    """Raised when an unknown demonstrator scenario is requested."""


class ScenarioService:
    """Application adapter over the frozen EXP-010 scenario engine."""

    def available_scenarios(self) -> list[str]:
        """Return the frozen scenario identifiers available for execution."""

        return [
            condition.condition_id
            for condition in EXP010_CONDITIONS
        ]

    def run_scenario(
        self,
        scenario_id: str,
    ) -> ScenarioResponse:
        """Execute one frozen scenario through the existing research engine."""

        normalised_id = scenario_id.upper()

        try:
            condition = condition_by_id(normalised_id)
        except KeyError as exc:
            raise ScenarioNotFoundError(
                f"Unknown scenario: {scenario_id}"
            ) from exc

        result = run_condition(condition)

        return self._to_response(result)

    def _to_response(
        self,
        result: DivergencePropagationExperimentResult,
    ) -> ScenarioResponse:
        """Translate a research-engine result into the API schema."""

        condition = result.condition

        return ScenarioResponse(
            scenario_id=condition.condition_id,
            description=condition.description,
            physical_state=self._physical_state(condition),
            twin_state=self._twin_state(condition),
            divergences=self._divergences(condition),
            ai_decision=self._decision(result),
            runtime_evidence=self._runtime_evidence(result),
            propagation=self._propagation(result),
            assurance_results=self._assurance_results(result),
            ground_truth=GroundTruthResult(
                intervention_required=(
                    result.ground_truth.intervention_required
                ),
                reason=result.ground_truth.reason,
            ),
            evaluations=self._evaluations(result),
        )

    def _physical_state(
        self,
        condition: PropagationCondition,
    ) -> SystemState:
        """Build the application view of relevant physical state."""

        if not condition.has_divergence:
            return SystemState(
                timestamp=10.0,
                entities=[],
            )

        assert condition.divergence_origin is not None
        assert condition.divergence_variable is not None

        return SystemState(
            timestamp=10.0,
            entities=[
                EntityState(
                    entity_id=condition.divergence_origin,
                    entity_type=self._entity_type(
                        condition.divergence_origin
                    ),
                    variables={
                        condition.divergence_variable:
                            condition.physical_value
                    },
                )
            ],
        )

    def _twin_state(
        self,
        condition: PropagationCondition,
    ) -> SystemState:
        """Build the application view of relevant Digital Twin state."""

        if not condition.has_divergence:
            return SystemState(
                timestamp=10.0,
                entities=[],
            )

        assert condition.divergence_origin is not None
        assert condition.divergence_variable is not None

        return SystemState(
            timestamp=10.0,
            entities=[
                EntityState(
                    entity_id=condition.divergence_origin,
                    entity_type=self._entity_type(
                        condition.divergence_origin
                    ),
                    variables={
                        condition.divergence_variable:
                            condition.twin_value
                    },
                )
            ],
        )

    def _divergences(
        self,
        condition: PropagationCondition,
    ) -> list[DivergenceRecord]:
        """Translate the controlled physical-digital mismatch."""

        if not condition.has_divergence:
            return []

        assert condition.divergence_origin is not None
        assert condition.divergence_variable is not None

        return [
            DivergenceRecord(
                entity_id=condition.divergence_origin,
                variable=condition.divergence_variable,
                physical_value=condition.physical_value,
                twin_value=condition.twin_value,
                decision_relevant=(
                    condition.is_direct_divergence
                    or condition.is_propagating
                ),
                decision_impacting=(
                    condition.intervention_required
                ),
            )
        ]

    def _decision(
        self,
        result: DivergencePropagationExperimentResult,
    ) -> AIDecision:
        """Expose the pending autonomous decision and its dependencies."""

        condition = result.condition

        vehicle_by_decision = {
            "D1": "vehicle_A",
            "D2": "vehicle_B",
            "D3": "vehicle_C",
        }

        order_by_decision = {
            "D1": "order_O1",
            "D2": "order_O2",
            "D3": None,
        }

        return AIDecision(
            decision_id=condition.pending_decision,
            action="assign_vehicle",
            vehicle_id=vehicle_by_decision.get(
                condition.pending_decision
            ),
            order_id=order_by_decision.get(
                condition.pending_decision
            ),
            dependencies=[
                DecisionDependency(
                    dependency=requirement.dependency,
                    relevant=True,
                )
                for requirement in result.requirements
            ],
        )

    def _runtime_evidence(
        self,
        result: DivergencePropagationExperimentResult,
    ) -> list[RuntimeEvidenceRecord]:
        """Translate runtime evidence used by the assurance policies."""

        return [
            RuntimeEvidenceRecord(
                source=evidence.source,
                dependency=evidence.dependency,
                observed_value=evidence.observed_value,
                timestamp=evidence.timestamp,
                confidence=evidence.confidence,
                status=evidence.status.value,
            )
            for evidence in result.runtime_evidence
        ]

    def _propagation(
        self,
        result: DivergencePropagationExperimentResult,
    ) -> list[PropagationRecord]:
        """Translate explicit divergence-propagation provenance."""

        analysis = result.propagation

        records: list[PropagationRecord] = []

        for path in analysis.paths:
            if path.steps:
                for step in path.steps:
                    records.append(
                        PropagationRecord(
                            origin=analysis.origin.dependency,
                            affected_dependency=(
                                step.affected_dependency
                            ),
                            source_decision=(
                                step.source_decision_id
                            ),
                            target_decision=(
                                step.target_decision_id
                            ),
                            propagating=path.is_propagating,
                            path=[
                                step.source_dependency,
                                step.affected_dependency,
                            ],
                        )
                    )
            else:
                records.append(
                    PropagationRecord(
                        origin=analysis.origin.dependency,
                        propagating=path.is_propagating,
                        path=[],
                    )
                )

        return records

    def _assurance_results(
        self,
        result: DivergencePropagationExperimentResult,
    ) -> list[AssuranceResult]:
        """Expose the five EXP-010 assurance mechanisms."""

        decisions = [
            (
                "No Assurance",
                result.no_assurance_authority,
                (
                    "EXP-010 P0 applies no runtime assurance."
                ),
            ),
            (
                "Local Contract",
                result.local_contract_authority,
                (
                    "Local runtime contract over direct "
                    "decision dependencies."
                ),
            ),
            (
                "Global Assurance",
                result.global_authority,
                (
                    "Global divergence and evidence-uncertainty "
                    "assurance."
                ),
            ),
            (
                "Composed Contract",
                result.composed_contract_authority,
                (
                    "Dependency-aware composed runtime contract."
                ),
            ),
            (
                "DARA-DT",
                result.dara_dt_authority,
                (
                    "Propagation-aware DARA-DT runtime assurance."
                ),
            ),
        ]

        relevant_divergence_count = (
            1
            if result.condition.has_divergence
            else 0
        )

        return [
            self._assurance_result(
                policy=policy,
                authority=authority,
                reason=reason,
                relevant_divergence_count=(
                    relevant_divergence_count
                ),
            )
            for policy, authority, reason in decisions
        ]

    def _assurance_result(
        self,
        *,
        policy: str,
        authority: AuthorityState,
        reason: str,
        relevant_divergence_count: int,
    ) -> AssuranceResult:
        """Create one application-facing assurance result."""

        return AssuranceResult(
            policy=policy,
            authority=authority.value,
            intervene=authority is not AuthorityState.ALLOW,
            reason=reason,
            relevant_divergence_count=(
                relevant_divergence_count
            ),
        )

    def _evaluations(
        self,
        result: DivergencePropagationExperimentResult,
    ) -> dict[str, EvaluationResult]:
        """Translate policy outcomes against evaluator-only ground truth."""

        return {
            "No Assurance": self._evaluation(
                result.no_assurance
            ),
            "Local Contract": self._evaluation(
                result.local_contract
            ),
            "Global Assurance": self._evaluation(
                result.global_assurance
            ),
            "Composed Contract": self._evaluation(
                result.composed_contract
            ),
            "DARA-DT": self._evaluation(
                result.dara_dt
            ),
        }

    def _evaluation(
        self,
        result: OutcomeResult,
    ) -> EvaluationResult:
        """Translate one assurance outcome."""

        outcome = result.outcome.value

        return EvaluationResult(
            outcome=outcome,
            correct=outcome in {
                "true_intervention",
                "correct_non_intervention",
            },
        )

    def _entity_type(
        self,
        entity_id: str,
    ) -> str:
        """Infer the demonstrator entity type from its canonical identifier."""

        if entity_id.startswith("vehicle_"):
            return "vehicle"

        if entity_id.startswith("order_"):
            return "order"

        return "system"


scenario_service = ScenarioService()
