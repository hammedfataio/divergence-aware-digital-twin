"""Decision-impact analysis for DARA-DT.

This module estimates how runtime evidence about decision-relevant
physical-digital divergence affects the feasibility of an AI-generated
logistics decision.

The analyser operates on runtime evidence rather than experimental
ground-truth labels. This preserves the separation between runtime
assurance and independent evaluation.

Supported dependency families:
- vehicle capacity;
- vehicle operational status;
- vehicle availability;
- vehicle location compatibility.
"""

from collections.abc import Collection

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
        """Analyse the impact of observed vehicle capacity."""

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

    def analyse_status(
        self,
        decision_id: str,
        dependency: str,
        evidence: ImpactEvidence,
        required_status: str = "operational",
    ) -> DecisionImpact:
        """Analyse operational-status evidence for a selected vehicle."""

        observed_status = evidence.observed_value
        twin_status = evidence.twin_value

        if not isinstance(observed_status, str):
            raise ValueError(
                "Observed operational-status evidence must be a string."
            )

        if not isinstance(twin_status, str):
            raise ValueError(
                "Digital Twin operational status must be a string."
            )

        if not isinstance(required_status, str) or not required_status:
            raise ValueError(
                "Required operational status must be a non-empty string."
            )

        if observed_status != required_status:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.INVALIDATING,
                estimated_margin=None,
                evidence=(evidence,),
                reason=(
                    "Runtime evidence indicates that the selected vehicle "
                    f"is '{observed_status}' rather than the required "
                    f"'{required_status}' state."
                ),
            )

        if twin_status != observed_status:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.MARGIN_REDUCED,
                estimated_margin=None,
                evidence=(evidence,),
                reason=(
                    "Operational-status divergence is decision-relevant, "
                    "but runtime evidence indicates that the selected "
                    "vehicle remains operational."
                ),
            )

        return DecisionImpact(
            decision_id=decision_id,
            dependency=dependency,
            impact_state=ImpactState.NO_IMPACT,
            estimated_margin=None,
            evidence=(evidence,),
            reason=(
                "Runtime evidence indicates no operational-status impact "
                "on the proposed decision."
            ),
        )

    def analyse_availability(
        self,
        decision_id: str,
        dependency: str,
        evidence: ImpactEvidence,
        required_available: bool = True,
    ) -> DecisionImpact:
        """Analyse vehicle-availability evidence."""

        observed_available = evidence.observed_value
        twin_available = evidence.twin_value

        if not isinstance(observed_available, bool):
            raise ValueError(
                "Observed availability evidence must be boolean."
            )

        if not isinstance(twin_available, bool):
            raise ValueError(
                "Digital Twin availability must be boolean."
            )

        if not isinstance(required_available, bool):
            raise ValueError(
                "Required availability must be boolean."
            )

        if observed_available != required_available:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.INVALIDATING,
                estimated_margin=None,
                evidence=(evidence,),
                reason=(
                    "Runtime evidence indicates that the selected vehicle "
                    "does not satisfy the availability condition required "
                    "by the proposed decision."
                ),
            )

        if twin_available != observed_available:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.MARGIN_REDUCED,
                estimated_margin=None,
                evidence=(evidence,),
                reason=(
                    "Availability divergence is decision-relevant, but "
                    "runtime evidence indicates that the selected vehicle "
                    "remains available for the proposed decision."
                ),
            )

        return DecisionImpact(
            decision_id=decision_id,
            dependency=dependency,
            impact_state=ImpactState.NO_IMPACT,
            estimated_margin=None,
            evidence=(evidence,),
            reason=(
                "Runtime evidence indicates no availability impact on "
                "the proposed decision."
            ),
        )

    def analyse_location(
        self,
        decision_id: str,
        dependency: str,
        evidence: ImpactEvidence,
        permitted_locations: Collection[str],
    ) -> DecisionImpact:
        """Analyse location compatibility for the proposed decision.

        Location validity is intentionally expressed through an explicit
        permitted-location set. This prevents EXP-007 from changing the
        compatibility rule after results are observed.
        """

        observed_location = evidence.observed_value
        twin_location = evidence.twin_value

        if not isinstance(observed_location, str):
            raise ValueError(
                "Observed location evidence must be a string."
            )

        if not isinstance(twin_location, str):
            raise ValueError(
                "Digital Twin location must be a string."
            )

        permitted = frozenset(permitted_locations)

        if not permitted:
            raise ValueError(
                "At least one permitted dispatch location is required."
            )

        if any(not isinstance(location, str) for location in permitted):
            raise ValueError(
                "Permitted dispatch locations must be strings."
            )

        if observed_location not in permitted:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.INVALIDATING,
                estimated_margin=None,
                evidence=(evidence,),
                reason=(
                    "Runtime evidence places the selected vehicle outside "
                    "the locations permitted for the proposed dispatch."
                ),
            )

        if twin_location != observed_location:
            return DecisionImpact(
                decision_id=decision_id,
                dependency=dependency,
                impact_state=ImpactState.MARGIN_REDUCED,
                estimated_margin=None,
                evidence=(evidence,),
                reason=(
                    "Location divergence is decision-relevant, but the "
                    "observed vehicle location remains compatible with "
                    "the proposed dispatch."
                ),
            )

        return DecisionImpact(
            decision_id=decision_id,
            dependency=dependency,
            impact_state=ImpactState.NO_IMPACT,
            estimated_margin=None,
            evidence=(evidence,),
            reason=(
                "Runtime evidence indicates no location impact on the "
                "proposed decision."
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
