# Experiment 008 — Imperfect-Evidence Contract Comparison

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-008  
**Status:** Complete  
**Research Stage:** Comparative runtime assurance under imperfect evidence

---

## 1. Objective

EXP-008 evaluates whether decision-conditioned physical–digital divergence
provides useful runtime-assurance information beyond direct runtime contracts
when runtime evidence is incomplete, stale, inaccurate, or conflicting.

The experiment was motivated directly by EXP-007.

EXP-007 showed that decision-impact-aware assurance generalised across three
decision-dependency families:

- vehicle capacity,
- operational status,
- location / availability.

However, under reliable runtime evidence, the Decision Impact policy and a
simpler Runtime Contract baseline produced identical binary assurance outcomes.

EXP-008 therefore introduces imperfect runtime evidence and a stronger
uncertainty-aware contract comparator.

The experiment is deliberately falsification-oriented.

The purpose is not to demonstrate that DARA-DT must outperform the baselines.
The purpose is to determine whether its decision-conditioned divergence
mechanism contributes assurance information beyond simpler runtime validity
mechanisms.

---

## 2. Research Question

The primary research question is:

> **Does decision-conditioned physical–digital divergence provide useful
> runtime-assurance information beyond direct runtime contracts when
> physical-state evidence is incomplete, stale, inaccurate, or conflicting?**

EXP-008 additionally investigates:

1. how imperfect evidence affects unsafe-action detection;
2. how evidence uncertainty affects unnecessary intervention;
3. whether the observed behaviour generalises across different decision
   dependencies;
4. whether explicitly modelling evidence quality provides an advantage over
   evidence-quality-unaware contracts;
5. whether DARA-DT provides additional assurance discrimination beyond a
   simpler uncertainty-aware runtime contract.

---

## 3. Experimental Principle

EXP-008 maintains a strict separation between three system states:

\[
P_t = \text{Physical Ground Truth}
\]

\[
T_t = \text{Digital Twin State}
\]

\[
E_t = \text{Runtime Evidence}
\]

These quantities are intentionally not treated as interchangeable.

### Physical Ground Truth

Physical ground truth represents the actual simulated logistics system.

It is used only by the independent evaluator to determine whether the proposed
AI decision is physically valid.

Runtime assurance policies do not receive privileged access to physical ground
truth.

### Digital Twin State

The Digital Twin represents the state available to the AI decision process.

It may differ from the physical system.

### Runtime Evidence

Runtime evidence represents observations available to the assurance layer.

Evidence may be:

- available and reliable,
- stale,
- missing,
- conflicting.

This separation allows the experiment to evaluate assurance behaviour without
silently giving runtime policies access to evaluator-only information.

---

## 4. Dependency Families

EXP-008 evaluates three decision-dependency families.

### 4.1 Capacity

The selected vehicle must have sufficient physical capacity for the order.

### 4.2 Operational Status

The selected vehicle must remain operational.

### 4.3 Location / Availability

The selected vehicle must remain available and within the permitted dispatch
location.

These dependency families were retained from EXP-007 to test whether findings
under imperfect evidence generalise beyond a single capacity example.

---

## 5. Evidence Conditions

Four evidence-quality conditions are evaluated.

| Evidence condition | Meaning |
|---|---|
| Reliable / Available | Runtime evidence is current and usable |
| Stale | Evidence represents an older system state |
| Missing | No usable runtime observation is available |
| Conflicting | Runtime sources provide incompatible observations |

Each evidence condition contains one physically valid and one physically
invalid decision for each dependency family.

This produces:

\[
3 \text{ dependency families}
\times
4 \text{ evidence conditions}
\times
2 \text{ physical validity states}
=
24 \text{ scenarios}
\]

The complete matrix therefore contains:

- 12 physically valid decisions;
- 12 physically invalid decisions.

---

## 6. Experimental Conditions

Each dependency family contains the following eight conditions:

| Condition | Evidence | Physical decision |
|---|---|---|
| R0 | Reliable | Valid |
| R1 | Reliable | Invalid |
| S0 | Stale | Valid |
| S1 | Stale | Invalid |
| M0 | Missing | Valid |
| M1 | Missing | Invalid |
| C0 | Conflicting | Valid |
| C1 | Conflicting | Invalid |

The complete experiment contains 24 conditions.

Examples include:

- `CAP-R0`
- `CAP-R1`
- `CAP-S0`
- `CAP-S1`
- `STATUS-M0`
- `STATUS-M1`
- `LOC-C0`
- `LOC-C1`

---

## 7. Compared Assurance Policies

Five policies are evaluated.

### P0 — No Assurance

The AI-generated decision is allowed regardless of divergence or evidence
quality.

This represents the unprotected autonomy baseline.

---

### P1 — Global Divergence

The policy reacts to observed mismatch between runtime evidence and the Digital
Twin without conditioning the mismatch on the specific decision dependency.

This represents global Twin mismatch monitoring.

---

### P2 — Direct Runtime Contract

The runtime observation is evaluated directly against the decision requirement.

This baseline does not explicitly reason about evidence-quality metadata.

Where no runtime value is available, the direct contract cannot evaluate the
requirement and allows execution by default in the EXP-008 implementation.

---

### P3 — Uncertainty-Aware Runtime Contract

This is the stronger contract baseline introduced specifically for EXP-008.

When evidence is available, the relevant runtime contract is evaluated.

When evidence is:

- stale,
- missing, or
- conflicting,

the policy defers autonomous execution.

This comparator is important because it tests whether DARA-DT contributes
something beyond simply adding evidence-quality awareness to an ordinary
runtime contract.

---

### P4 — DARA-DT Evidence-Aware Assurance

DARA-DT evaluates runtime evidence relative to the dependency and validity
requirements of the specific AI-generated decision.

The policy distinguishes authority states including:

- `ALLOW`
- `RESTRICT`
- `DEFER`
- `FALLBACK`

In EXP-008, uncertain evidence associated with the selected decision dependency
causes DARA-DT to defer execution.

---

## 8. Ground-Truth Evaluation

Ground truth is determined independently from physical system state.

A physically valid decision requires no intervention.

A physically invalid decision requires intervention.

Each policy result is classified as one of:

- **True Intervention (TI)** — intervention was required and occurred;
- **False Intervention (FI)** — intervention occurred although the decision was
  physically valid;
- **Missed Intervention (MI)** — intervention was required but did not occur;
- **Correct Non-Intervention (CNI)** — the valid decision was correctly allowed.

This ensures policy evaluation remains independent from the runtime evidence
used by the assurance mechanism.

---

## 9. Aggregate Results

The complete 24-condition matrix produced the following results.

| Policy | N | TI | FI | MI | CNI | Accuracy | Precision | Recall | FI Rate | MI Rate | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 24 | 0 | 0 | 12 | 12 | 0.500 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| Global Divergence | 24 | 5 | 7 | 7 | 5 | 0.417 | 0.417 | 0.417 | 0.583 | 0.583 | 0.500 |
| Direct Runtime Contract | 24 | 3 | 3 | 9 | 9 | 0.500 | 0.500 | 0.250 | 0.250 | 0.750 | 0.750 |
| Uncertainty-Aware Contract | 24 | 12 | 9 | 0 | 3 | 0.625 | 0.571 | 1.000 | 0.750 | 0.000 | 0.125 |
| DARA-DT | 24 | 12 | 9 | 0 | 3 | 0.625 | 0.571 | 1.000 | 0.750 | 0.000 | 0.125 |

---

## 10. Aggregate Interpretation

### 10.1 No Assurance

No Assurance preserves maximum autonomy:

\[
Autonomy = 1.000
\]

However, it misses all 12 physically invalid decisions:

\[
MI = 12
\]

\[
Recall = 0
\]

The result demonstrates the expected safety cost of unrestricted autonomy.

---

### 10.2 Global Divergence

Global divergence monitoring produces:

- 5 true interventions;
- 7 false interventions;
- 7 missed interventions;
- 5 correct non-interventions.

Its accuracy is:

\[
0.417
\]

The result demonstrates that global mismatch alone is not sufficient to
reliably determine whether an individual AI-generated decision should execute.

A mismatch may exist without invalidating the current decision, while imperfect
evidence may also fail to expose the true physical condition.

---

### 10.3 Direct Runtime Contract

The direct contract achieves:

- 3 true interventions;
- 3 false interventions;
- 9 missed interventions;
- 9 correct non-interventions.

Its intervention recall is:

\[
0.250
\]

Its autonomy availability is:

\[
0.750
\]

The direct contract performs correctly when reliable runtime observations are
available, but its lack of explicit evidence-quality handling makes it
vulnerable when observations are stale, missing, or conflicting.

---

### 10.4 Uncertainty-Aware Runtime Contract

The uncertainty-aware contract eliminates missed interventions:

\[
MI = 0
\]

\[
Recall = 1.000
\]

However, this is achieved through conservative intervention.

Nine of the twelve physically valid decisions are unnecessarily prevented:

\[
FI = 9
\]

\[
FI\ Rate = 0.750
\]

Autonomy availability falls to:

\[
0.125
\]

The policy therefore exchanges autonomy availability for protection against
unsafe execution under uncertain evidence.

---

### 10.5 DARA-DT

DARA-DT produces exactly the same binary outcome counts as the
uncertainty-aware contract:

- 12 true interventions;
- 9 false interventions;
- 0 missed interventions;
- 3 correct non-interventions.

Therefore:

\[
Accuracy = 0.625
\]

\[
Precision = 0.571
\]

\[
Recall = 1.000
\]

\[
Autonomy = 0.125
\]

This is a central result of EXP-008.

DARA-DT does **not** outperform the uncertainty-aware runtime contract at the
binary intervention level in the frozen EXP-008 matrix.

---

## 11. Authority-State Results

Although binary intervention outcomes are identical for the two strongest
policies, their authority-state distributions differ.

| Policy | ALLOW | RESTRICT | DEFER | FALLBACK |
|---|---:|---:|---:|---:|
| No Assurance | 24 | 0 | 0 | 0 |
| Global Divergence | 12 | 0 | 12 | 0 |
| Direct Runtime Contract | 18 | 6 | 0 | 0 |
| Uncertainty-Aware Contract | 3 | 3 | 18 | 0 |
| DARA-DT | 3 | 0 | 21 | 0 |

The difference occurs in the three reliable but physically invalid cases:

- `CAP-R1`
- `STATUS-R1`
- `LOC-R1`

For these cases:

\[
UncertaintyAwareContract = RESTRICT
\]

while:

\[
DARA\text{-}DT = DEFER
\]

Both authority states count as interventions in the binary outcome evaluator.

Therefore this difference demonstrates distinct authority semantics, but it
does **not** establish superior assurance performance for DARA-DT.

---

## 12. Condition-Level Results

| Condition | Evidence | Truth | No Assurance | Global | Direct | Uncertainty Contract | DARA-DT |
|---|---|---|---|---|---|---|---|
| CAP-R0 | available | ALLOW | allow | defer | allow | allow | allow |
| CAP-R1 | available | INTERVENE | allow | defer | restrict | restrict | defer |
| CAP-S0 | stale | ALLOW | allow | defer | restrict | defer | defer |
| CAP-S1 | stale | INTERVENE | allow | defer | allow | defer | defer |
| CAP-M0 | missing | ALLOW | allow | allow | allow | defer | defer |
| CAP-M1 | missing | INTERVENE | allow | allow | allow | defer | defer |
| CAP-C0 | conflicting | ALLOW | allow | defer | allow | defer | defer |
| CAP-C1 | conflicting | INTERVENE | allow | defer | allow | defer | defer |
| STATUS-R0 | available | ALLOW | allow | allow | allow | allow | allow |
| STATUS-R1 | available | INTERVENE | allow | defer | restrict | restrict | defer |
| STATUS-S0 | stale | ALLOW | allow | defer | restrict | defer | defer |
| STATUS-S1 | stale | INTERVENE | allow | allow | allow | defer | defer |
| STATUS-M0 | missing | ALLOW | allow | allow | allow | defer | defer |
| STATUS-M1 | missing | INTERVENE | allow | allow | allow | defer | defer |
| STATUS-C0 | conflicting | ALLOW | allow | allow | allow | defer | defer |
| STATUS-C1 | conflicting | INTERVENE | allow | allow | allow | defer | defer |
| LOC-R0 | available | ALLOW | allow | defer | allow | allow | allow |
| LOC-R1 | available | INTERVENE | allow | defer | restrict | restrict | defer |
| LOC-S0 | stale | ALLOW | allow | defer | restrict | defer | defer |
| LOC-S1 | stale | INTERVENE | allow | allow | allow | defer | defer |
| LOC-M0 | missing | ALLOW | allow | allow | allow | defer | defer |
| LOC-M1 | missing | INTERVENE | allow | allow | allow | defer | defer |
| LOC-C0 | conflicting | ALLOW | allow | defer | allow | defer | defer |
| LOC-C1 | conflicting | INTERVENE | allow | allow | allow | defer | defer |

---

## 13. Evidence-Quality Analysis

### 13.1 Reliable Evidence

For the six available-evidence conditions:

| Policy | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|
| No Assurance | 0.500 | 0.000 | 1.000 |
| Global Divergence | 0.667 | 1.000 | 0.167 |
| Direct Contract | 1.000 | 1.000 | 0.500 |
| Uncertainty-Aware Contract | 1.000 | 1.000 | 0.500 |
| DARA-DT | 1.000 | 1.000 | 0.500 |

With reliable evidence, the direct contract, uncertainty-aware contract and
DARA-DT all perfectly classify the six controlled decisions.

This reinforces the EXP-007 finding that a simpler runtime contract can be
sufficient when reliable decision-relevant state is directly observable.

---

### 13.2 Stale Evidence

For stale evidence, DARA-DT and the uncertainty-aware contract both produce:

- 3 true interventions;
- 3 false interventions;
- 0 missed interventions;
- 0 correct non-interventions.

Therefore:

\[
Recall = 1.000
\]

but:

\[
Autonomy = 0
\]

Both mechanisms conservatively defer all stale-evidence decisions.

The policy cannot distinguish a physically valid stale-evidence condition from
a physically invalid stale-evidence condition using the current experimental
mechanism.

---

### 13.3 Missing Evidence

For missing evidence, DARA-DT and the uncertainty-aware contract again produce:

- 3 true interventions;
- 3 false interventions;
- 0 missed interventions;
- 0 correct non-interventions.

Missing evidence therefore prevents unsafe autonomous execution but removes
autonomy for all six conditions.

Importantly, missing evidence is not treated as physical truth.

---

### 13.4 Conflicting Evidence

The same pattern appears under conflicting evidence:

- 3 true interventions;
- 3 false interventions;
- 0 missed interventions;
- 0 correct non-interventions.

Again:

\[
Recall = 1.000
\]

and:

\[
Autonomy = 0
\]

This confirms that the current DARA-DT implementation treats uncertain
decision-relevant evidence conservatively.

---

## 14. Cross-Dependency Results

The DARA-DT results are identical across all three dependency families.

| Dependency | N | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Capacity | 8 | 4 | 3 | 0 | 1 | 0.625 | 1.000 | 0.125 |
| Status | 8 | 4 | 3 | 0 | 1 | 0.625 | 1.000 | 0.125 |
| Location / Availability | 8 | 4 | 3 | 0 | 1 | 0.625 | 1.000 | 0.125 |

The uncertainty-aware contract produces the same binary metrics for all three
dependency families.

Therefore the EXP-008 result is not confined to the capacity dependency.

Within this controlled matrix, the safety–autonomy trade-off generalises across
capacity, operational status, and location / availability.

---

## 15. Safety–Autonomy Trade-Off

EXP-008 exposes an important trade-off.

No Assurance maximises autonomy:

\[
Autonomy = 1.000
\]

but misses every required intervention:

\[
Recall = 0
\]

DARA-DT and the uncertainty-aware contract achieve:

\[
Recall = 1.000
\]

but autonomy falls to:

\[
0.125
\]

The result demonstrates that simply responding conservatively to uncertain
evidence can protect against unsafe execution while severely reducing useful
autonomous operation.

A useful runtime-assurance mechanism therefore needs to consider both:

\[
Safety
\]

and:

\[
Autonomy\ Availability
\]

rather than optimising intervention recall alone.

---

## 16. Kill Test E — Strong Comparator Result

EXP-008 explicitly included the following falsification condition:

> If a simpler uncertainty-aware runtime contract produces equivalent
> intervention outcomes to DARA-DT using the same runtime evidence, the claim
> that DARA-DT provides superior binary runtime assurance is weakened.

This condition was met.

Across all 24 scenarios:

\[
BinaryOutcome(DARA\text{-}DT)
=
BinaryOutcome(UncertaintyAwareContract)
\]

The two policies have identical:

- true interventions;
- false interventions;
- missed interventions;
- correct non-interventions;
- accuracy;
- precision;
- recall;
- false-intervention rate;
- missed-intervention rate;
- autonomy availability.

Therefore EXP-008 does **not** support a claim that DARA-DT outperforms the
simpler uncertainty-aware contract at binary intervention classification.

This falsification result is retained rather than removed or reframed as a
performance advantage.

---

## 17. What EXP-008 Supports

EXP-008 provides controlled evidence for the following bounded conclusions.

### Finding 1

Explicit evidence-quality handling can prevent unsafe autonomous execution
under stale, missing and conflicting evidence in the tested matrix.

### Finding 2

That protection can impose a substantial autonomy cost.

### Finding 3

Global physical–digital mismatch alone is not sufficient for reliable
decision-level assurance under imperfect evidence.

### Finding 4

Direct contracts that ignore evidence quality can miss physically invalid
decisions when observations are stale, missing, or conflicting.

### Finding 5

Under reliable evidence, a simple runtime contract can match the tested
decision-conditioned mechanisms.

### Finding 6

Under the imperfect-evidence conditions tested here, DARA-DT and an
uncertainty-aware runtime contract are equivalent at the binary intervention
level.

### Finding 7

DARA-DT and the uncertainty-aware contract retain different authority semantics
for the three reliable-invalid conditions, but EXP-008 does not establish that
this distinction improves assurance performance.

---

## 18. What EXP-008 Does Not Establish

EXP-008 does not establish that:

- DARA-DT is superior to uncertainty-aware runtime contracts;
- decision-conditioned divergence is a novel mechanism;
- DARA-DT improves logistics performance;
- the observed results generalise to real logistics systems;
- the framework handles arbitrary sensor uncertainty;
- all forms of physical–digital divergence are covered;
- conservative deferral is an optimal assurance strategy;
- authority-state differences necessarily produce operational benefit.

These questions require additional experimental and literature evidence.

---

## 19. Limitation Exposed by EXP-008

The strongest limitation exposed by EXP-008 is that both DARA-DT and the
uncertainty-aware contract respond conservatively whenever evidence associated
with the selected decision dependency is stale, missing, or conflicting.

Consequently, both mechanisms achieve zero missed interventions by sacrificing
autonomy on physically valid imperfect-evidence cases.

This means EXP-008 does not yet test an important aspect of the central
decision-conditioning hypothesis:

> What happens when imperfect evidence exists in the Digital Twin system but
> does **not** affect a dependency of the specific AI-generated decision being
> evaluated?

For example, stale evidence concerning an unrelated vehicle should not
necessarily remove authority from a decision involving a different vehicle.

This distinction is not isolated by the frozen EXP-008 matrix.

---

## 20. Resulting Research Question

EXP-008 therefore motivates a sharper subsequent question:

> **Can decision-conditioned runtime assurance distinguish
> decision-relevant evidence uncertainty from decision-irrelevant evidence
> uncertainty, preserving autonomous authority without increasing missed
> unsafe interventions?**

This question directly tests whether decision conditioning contributes useful
assurance information beyond generic evidence-quality awareness.

---

## 21. Proposed Next Experiment

A subsequent experiment should introduce controlled imperfect evidence that is:

1. relevant to the pending AI decision; or
2. irrelevant to the pending AI decision.

The experiment should compare at least:

- global evidence-quality monitoring;
- uncertainty-aware runtime contracts;
- decision-conditioned DARA-DT assurance.

The critical outcome would not simply be whether DARA-DT intervenes.

The experiment should test whether decision conditioning can improve the
trade-off:

\[
Safety
\leftrightarrow
Autonomy\ Availability
\]

without receiving privileged physical-ground-truth information.

This experiment must be pre-registered before its results are observed.

---

## 22. Research Progression

The experimental progression is now:

### EXP-004

Decision relevance alone was shown to be insufficient because relevant
divergence can exist without invalidating a decision.

### EXP-005

Decision impact introduced decision-specific validity boundaries.

### EXP-006

Imperfect evidence demonstrated that decision-impact reasoning depends on the
quality of runtime observations.

### EXP-007

The relevance → impact → intervention relationship generalised across
capacity, status, and location / availability, but a simpler runtime contract
matched decision-impact assurance under reliable evidence.

### EXP-008

Evidence-quality-aware assurance prevented missed unsafe decisions under
imperfect evidence, but DARA-DT matched a simpler uncertainty-aware contract at
the binary level and incurred the same autonomy cost.

The remaining experimental question is therefore whether decision conditioning
adds value when evidence uncertainty exists outside the dependencies of the
specific AI-generated decision.

---

## 23. Conclusion

EXP-008 provides a controlled comparison of runtime assurance under reliable,
stale, missing, and conflicting evidence.

The experiment shows that evidence-quality-aware mechanisms can eliminate
missed interventions in the tested scenarios, but conservative handling of
uncertain evidence substantially reduces autonomy availability.

Most importantly, DARA-DT does not outperform the uncertainty-aware runtime
contract at the binary intervention level:

\[
DARA\text{-}DT:
TI=12,\ FI=9,\ MI=0,\ CNI=3
\]

\[
UncertaintyAwareContract:
TI=12,\ FI=9,\ MI=0,\ CNI=3
\]

This result activates the pre-defined falsification concern and narrows the
candidate contribution.

The next experiment should therefore test the aspect of decision conditioning
that EXP-008 does not isolate: whether imperfect evidence should affect
autonomous authority only when that evidence is relevant to the dependencies of
the specific AI-generated decision.

EXP-008 is now treated as a frozen experimental result.
