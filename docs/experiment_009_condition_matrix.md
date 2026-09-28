# EXP-009 — Frozen Experimental Condition Matrix

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-009  
**Status:** Pre-Registered Matrix — Frozen Before Implementation  
**Purpose:** Decision-Relevant vs Decision-Irrelevant Evidence Uncertainty

---

## 1. Purpose

This document freezes the experimental condition matrix for EXP-009 before
implementation and execution.

EXP-009 tests whether decision-conditioned runtime assurance can distinguish
uncertain evidence that affects the pending AI decision from uncertain evidence
that is unrelated to that decision.

The primary question is:

> Can decision-conditioned runtime assurance preserve autonomous authority under
> decision-irrelevant evidence uncertainty without increasing missed unsafe
> interventions?

The matrix defined here must not be changed after experimental execution begins
in response to observed results.

---

## 2. Experimental Factors

EXP-009 varies four controlled factors:

1. decision-dependency family;
2. runtime evidence quality;
3. evidence relevance;
4. physical decision validity.

Three dependency families are retained:

- Capacity
- Operational Status
- Location / Availability

Three imperfect evidence states are tested:

- Stale
- Missing
- Conflicting

Two relevance states are tested:

- Relevant
- Irrelevant

Two physical-validity states are tested:

- Valid
- Invalid

---

## 3. Primary Matrix Size

The primary imperfect-evidence matrix contains:

\[
3 \times 3 \times 2 \times 2 = 36
\]

conditions.

Therefore:

**Total primary conditions = 36**

with:

- 18 physically valid decisions;
- 18 physically invalid decisions;
- 18 relevant-uncertainty conditions;
- 18 irrelevant-uncertainty conditions.

---

## 4. Reliable Control Conditions

Reliable evidence is included separately as a control.

Each dependency family contains:

- one physically valid reliable condition;
- one physically invalid reliable condition.

Therefore:

\[
3 \times 2 = 6
\]

reliable control conditions are added.

The complete EXP-009 matrix therefore contains:

\[
36 + 6 = 42
\]

conditions.

---

# 5. Condition Naming Convention

Condition identifiers use:

`<DEPENDENCY>-<EVIDENCE>-<RELEVANCE>-<VALIDITY>`

Dependency:

- `CAP` — Capacity
- `STATUS` — Operational Status
- `LOC` — Location / Availability

Evidence:

- `R` — Reliable
- `S` — Stale
- `M` — Missing
- `C` — Conflicting

Relevance:

- `REL` — Decision Relevant
- `IRR` — Decision Irrelevant

Validity:

- `V` — Physically Valid
- `I` — Physically Invalid

Examples:

`CAP-S-REL-V`

means:

- capacity dependency;
- stale evidence;
- evidence relevant to the pending decision;
- physically valid decision.

`STATUS-M-IRR-I`

means:

- status dependency;
- missing evidence;
- missing evidence is irrelevant to the pending decision;
- pending decision is physically invalid.

---

# 6. Capacity Conditions

## Reliable Controls

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| CAP-R-V | Reliable | Relevant | Valid |
| CAP-R-I | Reliable | Relevant | Invalid |

## Stale Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| CAP-S-REL-V | Stale | Relevant | Valid |
| CAP-S-REL-I | Stale | Relevant | Invalid |
| CAP-S-IRR-V | Stale | Irrelevant | Valid |
| CAP-S-IRR-I | Stale | Irrelevant | Invalid |

## Missing Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| CAP-M-REL-V | Missing | Relevant | Valid |
| CAP-M-REL-I | Missing | Relevant | Invalid |
| CAP-M-IRR-V | Missing | Irrelevant | Valid |
| CAP-M-IRR-I | Missing | Irrelevant | Invalid |

## Conflicting Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| CAP-C-REL-V | Conflicting | Relevant | Valid |
| CAP-C-REL-I | Conflicting | Relevant | Invalid |
| CAP-C-IRR-V | Conflicting | Irrelevant | Valid |
| CAP-C-IRR-I | Conflicting | Irrelevant | Invalid |

Capacity total:

\[
14
\]

conditions.

---

# 7. Operational-Status Conditions

## Reliable Controls

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| STATUS-R-V | Reliable | Relevant | Valid |
| STATUS-R-I | Reliable | Relevant | Invalid |

## Stale Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| STATUS-S-REL-V | Stale | Relevant | Valid |
| STATUS-S-REL-I | Stale | Relevant | Invalid |
| STATUS-S-IRR-V | Stale | Irrelevant | Valid |
| STATUS-S-IRR-I | Stale | Irrelevant | Invalid |

## Missing Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| STATUS-M-REL-V | Missing | Relevant | Valid |
| STATUS-M-REL-I | Missing | Relevant | Invalid |
| STATUS-M-IRR-V | Missing | Irrelevant | Valid |
| STATUS-M-IRR-I | Missing | Irrelevant | Invalid |

## Conflicting Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| STATUS-C-REL-V | Conflicting | Relevant | Valid |
| STATUS-C-REL-I | Conflicting | Relevant | Invalid |
| STATUS-C-IRR-V | Conflicting | Irrelevant | Valid |
| STATUS-C-IRR-I | Conflicting | Irrelevant | Invalid |

Operational-status total:

\[
14
\]

conditions.

---

# 8. Location / Availability Conditions

## Reliable Controls

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| LOC-R-V | Reliable | Relevant | Valid |
| LOC-R-I | Reliable | Relevant | Invalid |

## Stale Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| LOC-S-REL-V | Stale | Relevant | Valid |
| LOC-S-REL-I | Stale | Relevant | Invalid |
| LOC-S-IRR-V | Stale | Irrelevant | Valid |
| LOC-S-IRR-I | Stale | Irrelevant | Invalid |

## Missing Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| LOC-M-REL-V | Missing | Relevant | Valid |
| LOC-M-REL-I | Missing | Relevant | Invalid |
| LOC-M-IRR-V | Missing | Irrelevant | Valid |
| LOC-M-IRR-I | Missing | Irrelevant | Invalid |

## Conflicting Evidence

| ID | Evidence | Relevance | Physical Decision |
|---|---|---|---|
| LOC-C-REL-V | Conflicting | Relevant | Valid |
| LOC-C-REL-I | Conflicting | Relevant | Invalid |
| LOC-C-IRR-V | Conflicting | Irrelevant | Valid |
| LOC-C-IRR-I | Conflicting | Irrelevant | Invalid |

Location / availability total:

\[
14
\]

conditions.

---

# 9. Complete Matrix Summary

| Dependency | Reliable | Stale | Missing | Conflicting | Total |
|---|---:|---:|---:|---:|---:|
| Capacity | 2 | 4 | 4 | 4 | 14 |
| Status | 2 | 4 | 4 | 4 | 14 |
| Location / Availability | 2 | 4 | 4 | 4 | 14 |
| **Total** | **6** | **12** | **12** | **12** | **42** |

---

# 10. Validity Balance

The 36 imperfect-evidence conditions contain:

| Physical validity | Conditions |
|---|---:|
| Valid | 18 |
| Invalid | 18 |

The six reliable controls contain:

| Physical validity | Conditions |
|---|---:|
| Valid | 3 |
| Invalid | 3 |

Complete EXP-009:

| Physical validity | Conditions |
|---|---:|
| Valid | 21 |
| Invalid | 21 |
| **Total** | **42** |

The experiment is therefore balanced by physical validity.

---

# 11. Relevance Balance

Within the primary imperfect-evidence matrix:

| Evidence relevance | Conditions |
|---|---:|
| Relevant | 18 |
| Irrelevant | 18 |

This balance is essential because evidence relevance is the primary experimental
variable introduced by EXP-009.

Reliable controls are not included in the relevance comparison because their
primary purpose is to establish normal assurance behaviour when usable evidence
is available.

---

# 12. Meaning of Relevant Evidence

Evidence is classified as decision relevant only when it concerns a state
dependency required by the specific pending decision.

For example:

> Assign Vehicle 2 to Order 7.

Capacity evidence concerning:

`Vehicle 2 capacity`

is relevant when capacity is a dependency of that assignment.

Evidence concerning:

`Vehicle 8 capacity`

is not automatically relevant simply because it exists within the same
Digital Twin.

---

# 13. Meaning of Irrelevant Evidence

Decision-irrelevant evidence concerns system state that does not participate in
the dependency set of the pending AI decision.

For example:

Pending decision:

> Assign Vehicle 2 to Order 7.

Uncertain evidence:

> Vehicle 8 status observation is stale.

If Vehicle 8 is not involved in the pending decision and its state does not
affect a dependency of the decision, the uncertainty is classified as
irrelevant.

The pending decision must still have sufficient reliable information about its
own required dependencies for the irrelevant-evidence comparison to be valid.

This prevents irrelevant uncertainty from being confused with missing
information about the selected decision.

---

# 14. Critical Irrelevant-Evidence Constraint

For every `IRR` condition:

1. the uncertain evidence must belong to a dependency or entity that is not
   required by the pending decision;

2. the pending decision's actual required dependency must have usable runtime
   evidence;

3. physical validity must be determined independently;

4. the uncertain irrelevant evidence must still be visible to policies that
   monitor system-wide evidence quality;

5. DARA-DT must not receive privileged physical-state information.

This constraint is essential to the validity of EXP-009.

---

# 15. Relevant-Evidence Constraint

For every `REL` condition:

1. the uncertain evidence must correspond directly to a dependency required by
   the pending decision;

2. the evidence quality must match the frozen condition label;

3. no reliable duplicate of the same dependency may silently resolve the
   uncertainty;

4. physical ground truth remains evaluator-only information.

---

# 16. Physically Valid Conditions

For a condition labelled `V`:

\[
GroundTruth = DO\ NOT\ INTERVENE
\]

A policy intervention is therefore classified as:

\[
False\ Intervention
\]

while an `ALLOW` result is:

\[
Correct\ Non\text{-}Intervention
\]

---

# 17. Physically Invalid Conditions

For a condition labelled `I`:

\[
GroundTruth = INTERVENE
\]

A policy intervention is:

\[
True\ Intervention
\]

while `ALLOW` is:

\[
Missed\ Intervention
\]

---

# 18. Frozen Comparator Set

EXP-009 will compare:

### P0 — No Assurance

Always allows execution.

### P1 — Global Evidence-Uncertainty Policy

Responds to uncertain evidence at system level without decision relevance
filtering.

### P2 — Entity-Filtered Uncertainty Policy

Filters evidence according to the selected decision entity.

This baseline tests whether any observed benefit can be explained by simple
entity filtering.

### P3 — Uncertainty-Aware Runtime Contract

Evaluates the pending decision's runtime contract while accounting for evidence
quality.

This remains the strongest simpler comparator carried forward from EXP-008.

### P4 — DARA-DT Decision-Conditioned Assurance

Conditions evidence uncertainty on the dependency set of the specific
AI-generated decision.

---

# 19. Entity-Filtered Baseline

The entity-filtered baseline is required for Kill Test F.

For a decision involving:

> Vehicle 2

the policy considers evidence associated with Vehicle 2 and ignores evidence
associated solely with unrelated vehicles.

However, it does not perform full dependency reasoning.

This distinction creates the comparison:

\[
Global
\rightarrow
Entity\ Filter
\rightarrow
Decision\ Dependency
\]

If entity filtering matches DARA-DT, the experimental evidence does not justify
attributing the benefit to richer decision-dependency reasoning.

---

# 20. Evidence Parity

All assurance mechanisms receive the same observable evidence collection.

Differences arise only from how policies select and interpret that evidence.

No comparator may be deliberately deprived of information available to
DARA-DT.

No policy may receive physical ground truth.

---

# 21. Authority States

Policies may return:

- `ALLOW`
- `RESTRICT`
- `DEFER`
- `FALLBACK`

For binary outcome evaluation:

\[
ALLOW = No\ Intervention
\]

while:

\[
RESTRICT,\ DEFER,\ FALLBACK = Intervention
\]

Authority-state distributions will also be reported separately.

---

# 22. Primary Metrics

For each policy, EXP-009 will calculate:

- True Interventions
- False Interventions
- Missed Interventions
- Correct Non-Interventions
- Accuracy
- Precision
- Recall
- False-Intervention Rate
- Missed-Intervention Rate
- Autonomy Availability

Authority-state counts will also be reported.

---

# 23. Required Grouped Metrics

Results must additionally be grouped by:

### Evidence Quality

- Reliable
- Stale
- Missing
- Conflicting

### Evidence Relevance

- Relevant
- Irrelevant

### Dependency Family

- Capacity
- Status
- Location / Availability

### Physical Validity

- Valid
- Invalid

The relevance-grouped analysis is the central EXP-009 comparison.

---

# 24. Primary Safety–Autonomy Test

The central test is:

> Does DARA-DT reduce false interventions under irrelevant evidence uncertainty
> without increasing missed interventions?

Formally, a potentially supportive pattern would require:

\[
FI_{DARA} < FI_{Comparator}
\]

while:

\[
MI_{DARA} \le MI_{Comparator}
\]

for the strongest justified comparator.

Autonomy improvement alone is not sufficient.

---

# 25. Paired Comparison Requirement

For each dependency family and evidence-quality state, relevant and irrelevant
conditions must be compared directly.

Example:

\[
CAP\text{-}S\text{-}REL\text{-}V
\]

versus:

\[
CAP\text{-}S\text{-}IRR\text{-}V
\]

The physical-validity label and evidence-quality label are held constant.

Only evidence relevance changes.

This paired design isolates the effect of decision relevance.

---

# 26. Frozen Kill Tests

The following falsification criteria are inherited from the EXP-009
pre-registration.

## Kill Test A — No Autonomy Advantage

If DARA-DT and the strongest comparator have equivalent autonomy while
maintaining equivalent safety, the autonomy-preservation claim is unsupported.

## Kill Test B — Safety Degradation

If DARA-DT gains autonomy by increasing missed interventions, the result is not
an assurance improvement.

## Kill Test C — Runtime Contract Equivalence

If the uncertainty-aware runtime contract matches DARA-DT with less mechanism
complexity, the stronger DARA-DT contribution claim is weakened.

## Kill Test D — Capacity-Only Effect

If the result does not generalise beyond capacity, broad framework claims must
be narrowed.

## Kill Test E — Evidence Privilege

If DARA-DT receives privileged evidence unavailable to comparators, the
comparison is invalid.

## Kill Test F — Trivial Entity Filtering

If entity filtering matches DARA-DT, the benefit cannot be attributed to richer
decision-dependency reasoning.

---

# 27. Additional Matrix Integrity Tests

Before execution, automated tests must verify:

1. exactly 42 conditions exist;
2. exactly 14 conditions exist per dependency family;
3. exactly 21 conditions are physically valid;
4. exactly 21 conditions are physically invalid;
5. exactly 18 imperfect-evidence conditions are relevant;
6. exactly 18 imperfect-evidence conditions are irrelevant;
7. stale, missing and conflicting each contain 12 conditions;
8. every imperfect evidence/relevance/dependency combination has both a valid
   and invalid condition;
9. every `IRR` condition contains usable evidence for the actual pending
   decision dependency;
10. every `REL` condition applies uncertainty to the actual pending decision
    dependency;
11. physical ground truth is not exposed to runtime policies;
12. all five policies execute for every condition.

---

# 28. Interpretation Rule

EXP-009 must not be interpreted only from aggregate accuracy.

The primary interpretation order is:

1. missed interventions;
2. false interventions;
3. autonomy availability;
4. relevance-specific behaviour;
5. dependency-family consistency;
6. authority-state distribution;
7. aggregate accuracy.

This prevents a policy from appearing favourable simply because it allows more
decisions.

---

# 29. Contribution Decision Rule

A stronger decision-conditioning claim requires DARA-DT to survive both:

\[
UncertaintyAwareContract
\]

and:

\[
EntityFilteredUncertainty
\]

comparisons.

If it does not, the contribution claim must be narrowed accordingly.

No experimental result will be discarded because it fails to support DARA-DT.

---

# 30. Freeze Statement

This condition matrix is frozen before EXP-009 implementation.

The experiment contains:

\[
42
\]

conditions:

- 14 capacity;
- 14 status;
- 14 location / availability.

The primary imperfect-evidence matrix contains:

\[
36
\]

conditions balanced across:

- stale;
- missing;
- conflicting;
- relevant;
- irrelevant;
- physically valid;
- physically invalid.

Six reliable controls are included separately.

The comparator set is frozen as:

1. No Assurance;
2. Global Evidence-Uncertainty;
3. Entity-Filtered Uncertainty;
4. Uncertainty-Aware Runtime Contract;
5. DARA-DT Decision-Conditioned Assurance.

Any new hypothesis or condition introduced after experimental execution begins
must be evaluated in a separate experiment.

---

## Final Frozen Matrix

\[
\boxed{
3\ Dependencies
\times
3\ ImperfectEvidenceStates
\times
2\ RelevanceStates
\times
2\ ValidityStates
=
36
}
\]

plus:

\[
\boxed{
6\ ReliableControls
}
\]

giving:

\[
\boxed{
EXP009 = 42\ Conditions
}
\]

**Status: FROZEN BEFORE IMPLEMENTATION**
