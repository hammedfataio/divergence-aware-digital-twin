"""Frozen condition matrix for EXP-010.

EXP-010 investigates whether physical-digital divergence that originates
upstream can propagate through a multi-stage autonomous logistics decision
chain and provide runtime-assurance information beyond a strong
dependency-aware composed runtime contract.

This module contains experimental definitions only.  It deliberately does
not implement assurance-policy behaviour.

The condition matrix is frozen at:

    30 conditions
    5 families
    6 conditions per family
    11 DO_NOT_INTERVENE
    19 INTERVENE
    15 AVAILABLE
    5 STALE
    5 MISSING
    5 CONFLICTING
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PropagationFamily(str, Enum):
    """Frozen EXP-010 experimental families."""

    SYNCHRONISED_CONTROL = "F0"
    DIRECT_DIVERGENCE = "F1"
    UPSTREAM_NON_PROPAGATING = "F2"
    UPSTREAM_PROPAGATING = "F3"
    COMPOUND_PROPAGATING = "F4"


class PropagationEvidenceStatus(str, Enum):
    """Evidence-quality states used by the EXP-010 matrix."""

    AVAILABLE = "available"
    STALE = "stale"
    MISSING = "missing"
    CONFLICTING = "conflicting"


class PropagationGroundTruth(str, Enum):
    """Frozen physical ground-truth labels."""

    INTERVENE = "intervene"
    DO_NOT_INTERVENE = "do_not_intervene"


@dataclass(frozen=True, slots=True)
class PropagationCondition:
    """One frozen EXP-010 experimental condition.

    The object records the experimental facts needed to construct the
    physical state, Digital Twin state, decision chain, evidence state and
    evaluator-only ground truth.

    Policy outputs are intentionally absent.  No assurance mechanism is
    allowed to define the condition's ground truth.
    """

    condition_id: str
    family: PropagationFamily
    description: str

    evidence_status: PropagationEvidenceStatus
    ground_truth: PropagationGroundTruth

    pending_decision: str

    divergence_origin: str | None
    divergence_variable: str | None

    physical_value: object | None
    twin_value: object | None

    propagated_dependency: str | None

    is_direct_divergence: bool
    is_propagating: bool
    is_compound: bool

    physical_validity: bool

    @property
    def intervention_required(self) -> bool:
        """Return the evaluator-only intervention requirement."""

        return self.ground_truth is PropagationGroundTruth.INTERVENE

    @property
    def has_divergence(self) -> bool:
        """Return whether the condition contains physical-digital divergence."""

        return self.divergence_origin is not None

    @property
    def has_imperfect_evidence(self) -> bool:
        """Return whether runtime evidence is not fully available."""

        return self.evidence_status is not PropagationEvidenceStatus.AVAILABLE


def _condition(
    *,
    condition_id: str,
    family: PropagationFamily,
    description: str,
    evidence_status: PropagationEvidenceStatus,
    ground_truth: PropagationGroundTruth,
    pending_decision: str,
    divergence_origin: str | None = None,
    divergence_variable: str | None = None,
    physical_value: object | None = None,
    twin_value: object | None = None,
    propagated_dependency: str | None = None,
    is_direct_divergence: bool = False,
    is_propagating: bool = False,
    is_compound: bool = False,
) -> PropagationCondition:
    """Construct a frozen EXP-010 condition."""

    return PropagationCondition(
        condition_id=condition_id,
        family=family,
        description=description,
        evidence_status=evidence_status,
        ground_truth=ground_truth,
        pending_decision=pending_decision,
        divergence_origin=divergence_origin,
        divergence_variable=divergence_variable,
        physical_value=physical_value,
        twin_value=twin_value,
        propagated_dependency=propagated_dependency,
        is_direct_divergence=is_direct_divergence,
        is_propagating=is_propagating,
        is_compound=is_compound,
        physical_validity=(
            ground_truth is PropagationGroundTruth.DO_NOT_INTERVENE
        ),
    )


# ---------------------------------------------------------------------------
# F0 — Synchronised controls
# ---------------------------------------------------------------------------

_F0 = (
    _condition(
        condition_id="F0-A",
        family=PropagationFamily.SYNCHRONISED_CONTROL,
        description="Synchronised valid control with available evidence.",
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
    ),
    _condition(
        condition_id="F0-B",
        family=PropagationFamily.SYNCHRONISED_CONTROL,
        description=(
            "Synchronised but physically invalid control caused by a genuine "
            "decision constraint rather than physical-digital divergence."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
    ),
    _condition(
        condition_id="F0-C",
        family=PropagationFamily.SYNCHRONISED_CONTROL,
        description="Synchronised valid control with stale runtime evidence.",
        evidence_status=PropagationEvidenceStatus.STALE,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
    ),
    _condition(
        condition_id="F0-D",
        family=PropagationFamily.SYNCHRONISED_CONTROL,
        description="Synchronised valid control with missing runtime evidence.",
        evidence_status=PropagationEvidenceStatus.MISSING,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
    ),
    _condition(
        condition_id="F0-E",
        family=PropagationFamily.SYNCHRONISED_CONTROL,
        description=(
            "Synchronised valid control with conflicting runtime evidence."
        ),
        evidence_status=PropagationEvidenceStatus.CONFLICTING,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
    ),
    _condition(
        condition_id="F0-F",
        family=PropagationFamily.SYNCHRONISED_CONTROL,
        description="Repeated deterministic synchronised valid control.",
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
    ),
)


# ---------------------------------------------------------------------------
# F1 — Direct decision-relevant divergence
# ---------------------------------------------------------------------------

_F1 = (
    _condition(
        condition_id="F1-A",
        family=PropagationFamily.DIRECT_DIVERGENCE,
        description="Direct Vehicle A status divergence.",
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D1",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_A.status",
        is_direct_divergence=True,
    ),
    _condition(
        condition_id="F1-B",
        family=PropagationFamily.DIRECT_DIVERGENCE,
        description="Direct Vehicle A capacity divergence.",
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D1",
        divergence_origin="vehicle_A",
        divergence_variable="capacity",
        physical_value=4.0,
        twin_value=10.0,
        propagated_dependency="vehicle_A.capacity",
        is_direct_divergence=True,
    ),
    _condition(
        condition_id="F1-C",
        family=PropagationFamily.DIRECT_DIVERGENCE,
        description="Direct Vehicle A availability divergence.",
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D1",
        divergence_origin="vehicle_A",
        divergence_variable="available",
        physical_value=False,
        twin_value=True,
        propagated_dependency="vehicle_A.available",
        is_direct_divergence=True,
    ),
    _condition(
        condition_id="F1-D",
        family=PropagationFamily.DIRECT_DIVERGENCE,
        description="Direct Vehicle A status divergence with stale evidence.",
        evidence_status=PropagationEvidenceStatus.STALE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D1",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_A.status",
        is_direct_divergence=True,
    ),
    _condition(
        condition_id="F1-E",
        family=PropagationFamily.DIRECT_DIVERGENCE,
        description="Direct Vehicle A status divergence with missing evidence.",
        evidence_status=PropagationEvidenceStatus.MISSING,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D1",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_A.status",
        is_direct_divergence=True,
    ),
    _condition(
        condition_id="F1-F",
        family=PropagationFamily.DIRECT_DIVERGENCE,
        description=(
            "Direct Vehicle A status divergence with conflicting evidence."
        ),
        evidence_status=PropagationEvidenceStatus.CONFLICTING,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D1",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_A.status",
        is_direct_divergence=True,
    ),
)


# ---------------------------------------------------------------------------
# F2 — Upstream divergence without downstream propagation
# ---------------------------------------------------------------------------

_F2 = (
    _condition(
        condition_id="F2-A",
        family=PropagationFamily.UPSTREAM_NON_PROPAGATING,
        description=(
            "Vehicle A location diverges without affecting pending D2."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="location",
        physical_value="customer_1",
        twin_value="depot",
    ),
    _condition(
        condition_id="F2-B",
        family=PropagationFamily.UPSTREAM_NON_PROPAGATING,
        description=(
            "Vehicle A capacity diverges without affecting pending D2."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="capacity",
        physical_value=8.0,
        twin_value=10.0,
    ),
    _condition(
        condition_id="F2-C",
        family=PropagationFamily.UPSTREAM_NON_PROPAGATING,
        description=(
            "Vehicle A status divergence is isolated from pending D2."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
    ),
    _condition(
        condition_id="F2-D",
        family=PropagationFamily.UPSTREAM_NON_PROPAGATING,
        description=(
            "Non-propagating Vehicle A location divergence with stale evidence."
        ),
        evidence_status=PropagationEvidenceStatus.STALE,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="location",
        physical_value="customer_1",
        twin_value="depot",
    ),
    _condition(
        condition_id="F2-E",
        family=PropagationFamily.UPSTREAM_NON_PROPAGATING,
        description=(
            "Non-propagating Vehicle A location divergence with missing "
            "evidence."
        ),
        evidence_status=PropagationEvidenceStatus.MISSING,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="location",
        physical_value="customer_1",
        twin_value="depot",
    ),
    _condition(
        condition_id="F2-F",
        family=PropagationFamily.UPSTREAM_NON_PROPAGATING,
        description=(
            "Non-propagating Vehicle A location divergence with conflicting "
            "evidence."
        ),
        evidence_status=PropagationEvidenceStatus.CONFLICTING,
        ground_truth=PropagationGroundTruth.DO_NOT_INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="location",
        physical_value="customer_1",
        twin_value="depot",
    ),
)


# ---------------------------------------------------------------------------
# F3 — Upstream divergence that propagates downstream
# ---------------------------------------------------------------------------

_F3 = (
    _condition(
        condition_id="F3-A",
        family=PropagationFamily.UPSTREAM_PROPAGATING,
        description=(
            "Vehicle A status divergence propagates into the recovery-resource "
            "assumption required by D2."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="recovery_resource_available",
        is_propagating=True,
    ),
    _condition(
        condition_id="F3-B",
        family=PropagationFamily.UPSTREAM_PROPAGATING,
        description=(
            "Vehicle A availability divergence propagates into the recovery "
            "resource assumption required by D2."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="available",
        physical_value=False,
        twin_value=True,
        propagated_dependency="recovery_resource_available",
        is_propagating=True,
    ),
    _condition(
        condition_id="F3-C",
        family=PropagationFamily.UPSTREAM_PROPAGATING,
        description=(
            "Vehicle A location divergence invalidates downstream recovery "
            "timing."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="location",
        physical_value="remote_zone",
        twin_value="depot",
        propagated_dependency="recovery_timing_valid",
        is_propagating=True,
    ),
    _condition(
        condition_id="F3-D",
        family=PropagationFamily.UPSTREAM_PROPAGATING,
        description=(
            "Propagating Vehicle A status divergence with stale evidence."
        ),
        evidence_status=PropagationEvidenceStatus.STALE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="recovery_resource_available",
        is_propagating=True,
    ),
    _condition(
        condition_id="F3-E",
        family=PropagationFamily.UPSTREAM_PROPAGATING,
        description=(
            "Propagating Vehicle A status divergence with missing evidence."
        ),
        evidence_status=PropagationEvidenceStatus.MISSING,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="recovery_resource_available",
        is_propagating=True,
    ),
    _condition(
        condition_id="F3-F",
        family=PropagationFamily.UPSTREAM_PROPAGATING,
        description=(
            "Propagating Vehicle A status divergence with conflicting evidence."
        ),
        evidence_status=PropagationEvidenceStatus.CONFLICTING,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="recovery_resource_available",
        is_propagating=True,
    ),
)


# ---------------------------------------------------------------------------
# F4 — Compound / cross-entity propagation
# ---------------------------------------------------------------------------

_F4 = (
    _condition(
        condition_id="F4-A",
        family=PropagationFamily.COMPOUND_PROPAGATING,
        description=(
            "Vehicle A status divergence propagates through Vehicle C "
            "availability and Vehicle B assignment assumptions."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_C.available+vehicle_B.assignment",
        is_propagating=True,
        is_compound=True,
    ),
    _condition(
        condition_id="F4-B",
        family=PropagationFamily.COMPOUND_PROPAGATING,
        description=(
            "Vehicle A status divergence propagates through Vehicle C "
            "capacity and recovery demand."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D3",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_C.capacity+recovery_demand",
        is_propagating=True,
        is_compound=True,
    ),
    _condition(
        condition_id="F4-C",
        family=PropagationFamily.COMPOUND_PROPAGATING,
        description=(
            "Vehicle A location divergence propagates through recovery timing "
            "and the downstream order deadline."
        ),
        evidence_status=PropagationEvidenceStatus.AVAILABLE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="location",
        physical_value="remote_zone",
        twin_value="depot",
        propagated_dependency="recovery_timing+vehicle_B.deadline",
        is_propagating=True,
        is_compound=True,
    ),
    _condition(
        condition_id="F4-D",
        family=PropagationFamily.COMPOUND_PROPAGATING,
        description=(
            "Compound Vehicle A status propagation with stale evidence."
        ),
        evidence_status=PropagationEvidenceStatus.STALE,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_C.available+vehicle_B.assignment",
        is_propagating=True,
        is_compound=True,
    ),
    _condition(
        condition_id="F4-E",
        family=PropagationFamily.COMPOUND_PROPAGATING,
        description=(
            "Compound Vehicle A status propagation with missing evidence."
        ),
        evidence_status=PropagationEvidenceStatus.MISSING,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_C.available+vehicle_B.assignment",
        is_propagating=True,
        is_compound=True,
    ),
    _condition(
        condition_id="F4-F",
        family=PropagationFamily.COMPOUND_PROPAGATING,
        description=(
            "Compound Vehicle A status propagation with conflicting evidence."
        ),
        evidence_status=PropagationEvidenceStatus.CONFLICTING,
        ground_truth=PropagationGroundTruth.INTERVENE,
        pending_decision="D2",
        divergence_origin="vehicle_A",
        divergence_variable="status",
        physical_value="failed",
        twin_value="operational",
        propagated_dependency="vehicle_C.available+vehicle_B.assignment",
        is_propagating=True,
        is_compound=True,
    ),
)


EXP010_CONDITIONS: tuple[PropagationCondition, ...] = (
    *_F0,
    *_F1,
    *_F2,
    *_F3,
    *_F4,
)


def conditions() -> tuple[PropagationCondition, ...]:
    """Return the immutable frozen EXP-010 condition matrix."""

    return EXP010_CONDITIONS


def condition_by_id(condition_id: str) -> PropagationCondition:
    """Return one EXP-010 condition by its frozen identifier.

    Raises:
        KeyError: if the condition identifier does not exist.
    """

    for item in EXP010_CONDITIONS:
        if item.condition_id == condition_id:
            return item

    raise KeyError(f"Unknown EXP-010 condition: {condition_id}")


def conditions_for_family(
    family: PropagationFamily,
) -> tuple[PropagationCondition, ...]:
    """Return all frozen conditions belonging to one family."""

    return tuple(
        item for item in EXP010_CONDITIONS if item.family is family
    )


def validate_condition_matrix() -> None:
    """Validate the frozen structural invariants of EXP-010.

    This function intentionally validates the pre-registered matrix before
    any assurance policy is executed.
    """

    if len(EXP010_CONDITIONS) != 30:
        raise ValueError(
            "EXP-010 must contain exactly 30 frozen conditions."
        )

    identifiers = [item.condition_id for item in EXP010_CONDITIONS]

    if len(identifiers) != len(set(identifiers)):
        raise ValueError(
            "EXP-010 condition identifiers must be unique."
        )

    for family in PropagationFamily:
        family_conditions = conditions_for_family(family)

        if len(family_conditions) != 6:
            raise ValueError(
                f"{family.value} must contain exactly 6 conditions."
            )

    intervene = sum(
        item.ground_truth is PropagationGroundTruth.INTERVENE
        for item in EXP010_CONDITIONS
    )

    do_not_intervene = sum(
        item.ground_truth is PropagationGroundTruth.DO_NOT_INTERVENE
        for item in EXP010_CONDITIONS
    )

    if intervene != 19:
        raise ValueError(
            "EXP-010 must contain exactly 19 INTERVENE conditions."
        )

    if do_not_intervene != 11:
        raise ValueError(
            "EXP-010 must contain exactly 11 DO_NOT_INTERVENE conditions."
        )

    expected_evidence_counts = {
        PropagationEvidenceStatus.AVAILABLE: 15,
        PropagationEvidenceStatus.STALE: 5,
        PropagationEvidenceStatus.MISSING: 5,
        PropagationEvidenceStatus.CONFLICTING: 5,
    }

    for evidence_status, expected_count in expected_evidence_counts.items():
        actual_count = sum(
            item.evidence_status is evidence_status
            for item in EXP010_CONDITIONS
        )

        if actual_count != expected_count:
            raise ValueError(
                "Unexpected EXP-010 evidence distribution for "
                f"{evidence_status.value}: expected {expected_count}, "
                f"found {actual_count}."
            )

    f0 = conditions_for_family(
        PropagationFamily.SYNCHRONISED_CONTROL
    )
    if any(item.has_divergence for item in f0):
        raise ValueError(
            "F0 synchronised controls must not contain divergence."
        )

    f1 = conditions_for_family(
        PropagationFamily.DIRECT_DIVERGENCE
    )
    if not all(
        item.has_divergence
        and item.is_direct_divergence
        and not item.is_propagating
        for item in f1
    ):
        raise ValueError(
            "Every F1 condition must contain direct, non-propagating "
            "divergence."
        )

    f2 = conditions_for_family(
        PropagationFamily.UPSTREAM_NON_PROPAGATING
    )
    if not all(
        item.has_divergence and not item.is_propagating
        for item in f2
    ):
        raise ValueError(
            "Every F2 condition must contain upstream non-propagating "
            "divergence."
        )

    f3 = conditions_for_family(
        PropagationFamily.UPSTREAM_PROPAGATING
    )
    if not all(
        item.has_divergence
        and item.is_propagating
        and not item.is_compound
        and item.propagated_dependency is not None
        for item in f3
    ):
        raise ValueError(
            "Every F3 condition must contain a single frozen propagation "
            "relationship."
        )

    f4 = conditions_for_family(
        PropagationFamily.COMPOUND_PROPAGATING
    )
    if not all(
        item.has_divergence
        and item.is_propagating
        and item.is_compound
        and item.propagated_dependency is not None
        for item in f4
    ):
        raise ValueError(
            "Every F4 condition must contain compound propagation."
        )

    for item in EXP010_CONDITIONS:
        expected_validity = (
            item.ground_truth
            is PropagationGroundTruth.DO_NOT_INTERVENE
        )

        if item.physical_validity is not expected_validity:
            raise ValueError(
                f"{item.condition_id} has inconsistent physical validity."
            )


# Fail fast if the committed matrix itself is internally inconsistent.
validate_condition_matrix()
