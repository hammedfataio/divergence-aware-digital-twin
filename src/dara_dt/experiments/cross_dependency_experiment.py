"""EXP-007 cross-dependency generalisation experiment.

This experiment tests whether the DARA-DT reasoning chain generalises
across multiple logistics decision dependencies rather than working only
for vehicle capacity.

The experiment evaluates three dependency families:

- vehicle capacity;
- vehicle operational status;
- vehicle location / availability.

Five assurance strategies are compared:

P0 - No assurance
P1 - Global divergence
P2 - Decision relevance
P3 - Decision impact (DARA-DT)
P4 - Runtime contract / assumption checking

All assurance strategies are evaluated against independent physical
ground truth.

The proposed decision is deliberately controlled across the experimental
matrix. EXP-007 evaluates the assurance response to a fixed proposed
decision rather than allowing controller behaviour to change the decision
under test.
"""

from dataclasses import dataclass
from typing import Any

from dara_dt.assurance.baselines import (
    AnyDivergencePolicy,
    NoAssurancePolicy,
)
from dara_dt.assurance.contract_policy import (
    ContractResult,
    RuntimeContractPolicy,
)
from dara_dt.assurance.impact_policy import DecisionImpactPolicy
from dara_dt.assurance.model import (
    AssuranceDecision,
    AuthorityState,
)
from dara_dt.assurance.policy import DivergenceAwarePolicy
from dara_dt.decision.dependency import DependencyMapper
from dara_dt.decision.model import Decision
from dara_dt.divergence.detector import (
    Divergence,
    DivergenceDetector,
)
from dara_dt.divergence.relevance import (
    DecisionRelevanceAnalyzer,
    RelevanceResult,
)
from dara_dt.evaluation.outcomes import (
    OutcomeEvaluator,
    OutcomeResult,
)
from dara_dt.evaluation.validity import PhysicalDecisionValidator
from dara_dt.experiments.cross_dependency_conditions import (
    CrossDependencyCondition,
    DependencyFamily,
    build_cross_dependency_conditions,
)
from dara_dt.experiments.ground_truth import GroundTruth
from dara_dt.impact.analyser import DecisionImpactAnalyser
from dara_dt.impact.model import (
    DecisionImpact,
    ImpactEvidence,
)


@dataclass(frozen=True)
class CrossDependencyExperimentResult:
    """Result for one EXP-007 controlled condition."""

    condition: CrossDependencyCondition
    decision: Decision
    ground_truth: GroundTruth

    divergence_count: int
    relevant_divergence_count: int

    impact_dependency: str
    impact_state: str

    contract_dependency: str
    contract_satisfied: bool

    no_assurance: OutcomeResult
    global_divergence: OutcomeResult
    decision_relevance: OutcomeResult
    decision_impact: OutcomeResult
    runtime_contract: OutcomeResult


def _build_decision(
    condition: CrossDependencyCondition,
) -> Decision:
    """Create the controlled proposed decision for one condition.

    EXP-007 studies runtime assurance behaviour for a fixed proposed
    assignment. The experiment therefore does not ask the logistics
    controller to regenerate or replace the decision after divergence
    has been introduced.
    """

    return Decision(
        decision_id=f"decision_{condition.condition_id}",
        action="assign_vehicle",
        vehicle_id=condition.selected_vehicle_id,
        order_id="order_01",
        timestamp=0.0,
    )


def _base_vehicle_state(
    vehicle_id: str,
) -> dict[str, Any]:
    """Return a valid default vehicle state."""

    return {
        "vehicle_id": vehicle_id,
        "capacity": 10.0,
        "location": "depot",
        "available": True,
        "status": "operational",
    }


def _base_order_state(
    condition: CrossDependencyCondition,
) -> dict[str, Any]:
    """Return the controlled order state."""

    return {
        "order_id": "order_01",
        "demand": condition.order_demand,
        "location": "customer_01",
        "deadline": 10.0,
        "status": "waiting",
    }


def _build_states(
    condition: CrossDependencyCondition,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build Digital Twin and physical states for one condition."""

    twin_selected = _base_vehicle_state(
        condition.selected_vehicle_id
    )
    physical_selected = _base_vehicle_state(
        condition.selected_vehicle_id
    )

    twin_unrelated = _base_vehicle_state(
        condition.unrelated_vehicle_id
    )
    physical_unrelated = _base_vehicle_state(
        condition.unrelated_vehicle_id
    )

    if condition.family == DependencyFamily.CAPACITY:
        twin_selected["capacity"] = (
            condition.twin_selected_value
        )
        physical_selected["capacity"] = (
            condition.physical_selected_value
        )

        twin_unrelated["capacity"] = (
            condition.twin_unrelated_value
        )
        physical_unrelated["capacity"] = (
            condition.physical_unrelated_value
        )

    elif condition.family == DependencyFamily.STATUS:
        twin_selected["status"] = (
            condition.twin_selected_value
        )
        physical_selected["status"] = (
            condition.physical_selected_value
        )

        twin_unrelated["status"] = (
            condition.twin_unrelated_value
        )
        physical_unrelated["status"] = (
            condition.physical_unrelated_value
        )

    elif (
        condition.family
        == DependencyFamily.LOCATION_AVAILABILITY
    ):
        (
            twin_selected["location"],
            twin_selected["available"],
        ) = condition.twin_selected_value

        (
            physical_selected["location"],
            physical_selected["available"],
        ) = condition.physical_selected_value

        (
            twin_unrelated["location"],
            twin_unrelated["available"],
        ) = condition.twin_unrelated_value

        (
            physical_unrelated["location"],
            physical_unrelated["available"],
        ) = condition.physical_unrelated_value

    else:
        raise ValueError(
            f"Unsupported dependency family: {condition.family!r}"
        )

    twin_state = {
        "vehicles": {
            condition.selected_vehicle_id: twin_selected,
            condition.unrelated_vehicle_id: twin_unrelated,
        },
        "orders": {
            "order_01": _base_order_state(condition),
        },
    }

    physical_state = {
        "vehicles": {
            condition.selected_vehicle_id: physical_selected,
            condition.unrelated_vehicle_id: physical_unrelated,
        },
        "orders": {
            "order_01": _base_order_state(condition),
        },
    }

    return twin_state, physical_state


def _analyse_impact(
    condition: CrossDependencyCondition,
    decision: Decision,
) -> DecisionImpact:
    """Estimate decision impact from reliable runtime evidence.

    EXP-007 intentionally uses reliable evidence so that dependency
    generalisation can be studied independently from the imperfect
    evidence problem investigated in EXP-006.
    """

    analyser = DecisionImpactAnalyser()

    if condition.family == DependencyFamily.CAPACITY:
        evidence = ImpactEvidence(
            source="runtime_capacity_monitor",
            variable="vehicle.capacity",
            observed_value=condition.physical_selected_value,
            twin_value=condition.twin_selected_value,
        )

        return analyser.analyse_capacity(
            decision_id=decision.decision_id,
            dependency="vehicle.capacity",
            required_demand=condition.order_demand,
            evidence=evidence,
        )

    if condition.family == DependencyFamily.STATUS:
        evidence = ImpactEvidence(
            source="runtime_status_monitor",
            variable="vehicle.status",
            observed_value=condition.physical_selected_value,
            twin_value=condition.twin_selected_value,
        )

        return analyser.analyse_status(
            decision_id=decision.decision_id,
            dependency="vehicle.status",
            evidence=evidence,
            required_status=condition.required_status,
        )

    if (
        condition.family
        == DependencyFamily.LOCATION_AVAILABILITY
    ):
        twin_location, twin_available = (
            condition.twin_selected_value
        )
        physical_location, physical_available = (
            condition.physical_selected_value
        )

        availability_evidence = ImpactEvidence(
            source="runtime_availability_monitor",
            variable="vehicle.available",
            observed_value=physical_available,
            twin_value=twin_available,
        )

        availability_impact = analyser.analyse_availability(
            decision_id=decision.decision_id,
            dependency="vehicle.available",
            evidence=availability_evidence,
            required_available=condition.required_available,
        )

        # Availability failure is sufficient to invalidate dispatch.
        # When availability remains valid, location compatibility is
        # evaluated as the remaining dependency.
        if availability_impact.invalidating:
            return availability_impact

        location_evidence = ImpactEvidence(
            source="runtime_location_monitor",
            variable="vehicle.location",
            observed_value=physical_location,
            twin_value=twin_location,
        )

        return analyser.analyse_location(
            decision_id=decision.decision_id,
            dependency="vehicle.location",
            evidence=location_evidence,
            permitted_locations=condition.permitted_locations,
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.family!r}"
    )


def _evaluate_contract(
    condition: CrossDependencyCondition,
    decision: Decision,
) -> ContractResult:
    """Evaluate the strong runtime-contract comparator."""

    policy = RuntimeContractPolicy()

    if condition.family == DependencyFamily.CAPACITY:
        return policy.evaluate_capacity(
            decision_id=decision.decision_id,
            observed_capacity=condition.physical_selected_value,
            required_demand=condition.order_demand,
        )

    if condition.family == DependencyFamily.STATUS:
        return policy.evaluate_status(
            decision_id=decision.decision_id,
            observed_status=condition.physical_selected_value,
            required_status=condition.required_status,
        )

    if (
        condition.family
        == DependencyFamily.LOCATION_AVAILABILITY
    ):
        physical_location, physical_available = (
            condition.physical_selected_value
        )

        return policy.evaluate_location_availability(
            decision_id=decision.decision_id,
            observed_location=physical_location,
            observed_available=physical_available,
            permitted_locations=condition.permitted_locations,
            required_available=condition.required_available,
        )

    raise ValueError(
        f"Unsupported dependency family: {condition.family!r}"
    )


def _contract_to_assurance(
    contract: ContractResult,
) -> AssuranceDecision:
    """Adapt a runtime-contract result for common outcome evaluation."""

    authority = (
        AuthorityState.DEFER
        if contract.intervene
        else AuthorityState.ALLOW
    )

    return AssuranceDecision(
        decision_id=contract.decision_id,
        authority=authority,
        reason=contract.reason,
        relevant_divergence_count=0,
    )


def _ground_truth(
    condition: CrossDependencyCondition,
    decision: Decision,
    physical_state: dict[str, Any],
) -> GroundTruth:
    """Derive independent physical ground truth."""

    validator = PhysicalDecisionValidator()

    permitted_locations = None

    if (
        condition.family
        == DependencyFamily.LOCATION_AVAILABILITY
    ):
        permitted_locations = condition.permitted_locations

    return validator.ground_truth(
        decision=decision,
        physical_state=physical_state,
        permitted_vehicle_locations=permitted_locations,
    )


def _detect_and_analyse_relevance(
    decision: Decision,
    physical_state: dict[str, Any],
    twin_state: dict[str, Any],
) -> tuple[list[Divergence], RelevanceResult]:
    """Detect divergence and match it to decision dependencies."""

    divergences = DivergenceDetector().detect(
        physical_state=physical_state,
        twin_state=twin_state,
    )

    relevance = DecisionRelevanceAnalyzer(
        DependencyMapper()
    ).analyse(
        decision=decision,
        divergences=divergences,
    )

    return divergences, relevance


def run_cross_dependency_condition(
    condition: CrossDependencyCondition,
) -> CrossDependencyExperimentResult:
    """Run one pre-registered EXP-007 condition."""

    decision = _build_decision(condition)

    twin_state, physical_state = _build_states(condition)

    divergences, relevance = (
        _detect_and_analyse_relevance(
            decision=decision,
            physical_state=physical_state,
            twin_state=twin_state,
        )
    )

    ground_truth = _ground_truth(
        condition=condition,
        decision=decision,
        physical_state=physical_state,
    )

    impact = _analyse_impact(
        condition=condition,
        decision=decision,
    )

    contract = _evaluate_contract(
        condition=condition,
        decision=decision,
    )

    no_assurance_decision = NoAssurancePolicy().evaluate(
        decision,
        divergences,
    )

    global_divergence_decision = (
        AnyDivergencePolicy().evaluate(
            decision,
            divergences,
        )
    )

    relevance_decision = DivergenceAwarePolicy().evaluate(
        decision,
        relevance,
    )

    impact_decision = DecisionImpactPolicy().evaluate(
        decision,
        impact,
    )

    contract_decision = _contract_to_assurance(contract)

    evaluator = OutcomeEvaluator()

    return CrossDependencyExperimentResult(
        condition=condition,
        decision=decision,
        ground_truth=ground_truth,
        divergence_count=len(divergences),
        relevant_divergence_count=len(relevance.relevant),
        impact_dependency=impact.dependency,
        impact_state=impact.impact_state.value,
        contract_dependency=contract.dependency,
        contract_satisfied=contract.satisfied,
        no_assurance=evaluator.evaluate(
            ground_truth,
            no_assurance_decision,
        ),
        global_divergence=evaluator.evaluate(
            ground_truth,
            global_divergence_decision,
        ),
        decision_relevance=evaluator.evaluate(
            ground_truth,
            relevance_decision,
        ),
        decision_impact=evaluator.evaluate(
            ground_truth,
            impact_decision,
        ),
        runtime_contract=evaluator.evaluate(
            ground_truth,
            contract_decision,
        ),
    )


def run_cross_dependency_experiment(
) -> tuple[CrossDependencyExperimentResult, ...]:
    """Run all 12 pre-registered EXP-007 conditions."""

    return tuple(
        run_cross_dependency_condition(condition)
        for condition in build_cross_dependency_conditions()
    )


if __name__ == "__main__":
    for result in run_cross_dependency_experiment():
        print(
            result.condition.condition_id,
            {
                "family": result.condition.family.value,
                "ground_truth": (
                    result.ground_truth.label.value
                ),
                "divergence_count": (
                    result.divergence_count
                ),
                "relevant_divergence_count": (
                    result.relevant_divergence_count
                ),
                "impact_state": result.impact_state,
                "no_assurance": (
                    result.no_assurance.outcome.value
                ),
                "global_divergence": (
                    result.global_divergence.outcome.value
                ),
                "decision_relevance": (
                    result.decision_relevance.outcome.value
                ),
                "decision_impact": (
                    result.decision_impact.outcome.value
                ),
                "runtime_contract": (
                    result.runtime_contract.outcome.value
                ),
            },
        )
