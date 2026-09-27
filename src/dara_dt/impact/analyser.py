"""Decision-impact analysis for DARA-DT.

This module estimates how runtime evidence about a decision-relevant
physical-digital divergence affects the feasibility of an AI-generated
logistics decision.

The analyser operates on runtime evidence. It does not use experimental
ground-truth validity labels, preserving the separation between runtime
assurance and evaluation.
"""

from dara_dt.impact.model import (
    DecisionImpact,
    ImpactEvidence,
    ImpactState,
)


class DecisionImpactAnalyser:
    """Estimate decision impact from runtime evidence."""

    def analyse_capacity(
        self,
        decision_id: str,
        dependency: str,
        required_demand: float,
        evidence: ImpactEvidence,
    ) -> DecisionImpact:
        """Analyse the impact of observed vehicle capacity.

        Args:
            decision_id:
                Identifier of the AI-generated decision.

            dependency:
                Decision dependency being evaluated.

            required_demand:
                Capacity required by the proposed decision.

            evidence:
                Runtime evidence containing the observed and Digital
                Twin capacity values.

        Returns:
            A DecisionImpact describing the estimated effect of the
            observed capacity on the proposed decision.

        Raises:
            ValueError:
                If demand or capacity evidence is not numeric.
        """

        if isinstance(required_demand, bool) or not isinstance(
            required_demand,
            (int, float),
        ):
            raise ValueError("Required demand must be numeric.")

        observed_capacity = evidence.observed_value
        twin_capacity = evidence.twin_value

        if isinstance(observed_capacity, bool) or not isinstance(
            observed_capacity,
            (int, float),
        ):
            raise ValueError(
                "Observed capacity evidence must be numeric."
            )

        if isinstance(twin_capacity, bool) or not isinstance(
            twin_capacity,
            (int, float),
        ):
            raise ValueError(
                "Digital Twin capacity must be numeric."
            )

        observed_margin = float(observed_capacity) - float(
            required_demand
        )

        twin_margin = float(twin_capacity) - float(required_demand)

        if observed_margin < 0:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.INVALIDATING,
                estimated_margin=observed_margin,
                evidence=(evidence,),
                reason=(
                    "Runtime evidence indicates that observed capacity "
                    "is below the capacity required by the decision."
                ),
            )

        if observed_margin == 0:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.BOUNDARY,
                estimated_margin=observed_margin,
                evidence=(evidence,),
                reason=(
                    "Runtime evidence places the decision exactly at "
                    "the capacity-validity boundary."
                ),
            )

        if observed_margin < twin_margin:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.MARGIN_REDUCED,
                estimated_margin=observed_margin,
                evidence=(evidence,),
                reason=(
                    "Runtime evidence reduces the available capacity "
                    "margin but the decision remains feasible."
                ),
            )

        return DecisionImpact(
            decision_id=decision_id,
            dependency=dependency,
            impact_state=ImpactState.NO_IMPACT,
            estimated_margin=observed_margin,
            evidence=(evidence,),
            reason=(
                "Runtime evidence does not reduce the capacity margin "
                "available to the decision."
            ),
        )

    def uncertain(
        self,
        decision_id: str,
        dependency: str,
        reason: str,
        evidence: tuple[ImpactEvidence, ...] = (),
    ) -> DecisionImpact:
        """Represent impact that cannot be determined from available evidence."""

        return DecisionImpact(
            decision_id=decision_id,
            dependency=dependency,
            impact_state=ImpactState.UNCERTAIN,
            estimated_margin=None,
            evidence=evidence,
            reason=reason,
        )
