# Experiment 009 — Decision-Relevant vs Decision-Irrelevant Evidence Uncertainty

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-009  
**Status:** Completed  
**Research Stage:** Decision-conditioned evidence uncertainty and autonomy preservation

---

## 1. Motivation

EXP-008 evaluated runtime assurance when evidence associated with the pending
AI decision was reliable, stale, missing, or conflicting.

The strongest evidence-quality-aware policies were:

- Uncertainty-Aware Runtime Contract;
- DARA-DT Evidence-Aware Assurance.

Across the 24 EXP-008 conditions, both policies produced identical binary
assurance outcomes:

- 12 true interventions;
- 9 false interventions;
- 0 missed interventions;
- 3 correct non-interventions;
- 100% intervention recall;
- 12.5% autonomy availability.

The result demonstrated that conservative handling of uncertain evidence can
prevent unsafe autonomous execution.

However, it also demonstrated a substantial autonomy cost.

EXP-008 did not isolate an important part of the DARA-DT hypothesis:

> Whether evidence uncertainty should affect autonomous authority when the
> uncertain evidence is unrelated to the dependencies of the specific
> AI-generated decision being evaluated.

EXP-009 was designed specifically to test this question.

---

## 2. Primary Research Question

> **Can decision-conditioned runtime assurance distinguish
> decision-relevant evidence uncertainty from decision-irrelevant evidence
> uncertainty and thereby preserve autonomous authority without increasing
> missed unsafe interventions?**

---

## 3. Secondary Research Questions

EXP-009 investigates:

1. whether generic evidence-quality monitoring over-intervenes when uncertainty
   exists outside the dependencies of the pending decision;

2. whether decision-conditioned assurance can ignore irrelevant uncertainty
   while remaining conservative about relevant uncertainty;

3. whether this behaviour generalises across capacity, operational status, and
   location / availability dependencies;

4. whether improved autonomy can be achieved without increasing missed
   interventions;

5. whether the additional dependency information used by DARA-DT provides
   measurable assurance value beyond simpler uncertainty-aware mechanisms.

---

## 4. Central Hypothesis

The experiment tests the following hypothesis:

> Evidence uncertainty should influence autonomous authority only when the
> uncertain evidence affects a dependency required by the specific
> AI-generated decision.

For a decision \(d_t\), let:

\[
Dep(d_t)
\]

represent the state dependencies required by the decision.

Let:

\[
U_t
\]

represent runtime evidence whose quality is uncertain.

Decision-relevant uncertain evidence is:

\[
U_t^{rel}(d_t) = U_t \cap Dep(d_t)
\]

Decision-irrelevant uncertain evidence is:

\[
U_t^{irr}(d_t) = U_t \setminus Dep(d_t)
\]

The experimental question is whether distinguishing these sets improves the
runtime assurance trade-off.

---

## 5. Core Experimental Principle

EXP-009 separates:

\[
Physical\ Ground\ Truth
\]

from:

\[
Digital\ Twin\ State
\]

from:

\[
Runtime\ Evidence
\]

and additionally separates runtime evidence into:

\[
Decision\text{-}Relevant\ Evidence
\]

and:

\[
Decision\text{-}Irrelevant\ Evidence
\]

Physical ground truth remains evaluator-only information.

No runtime policy may use physical ground truth to determine its authority
decision.

---

## 6. Illustrative Example

Consider an AI decision:

> Assign Vehicle 2 to Order 7.

Suppose this decision depends on:

- Vehicle 2 capacity;
- Vehicle 2 operational status;
- Vehicle 2 availability;
- Vehicle 2 dispatch location;
- Order 7 demand and state.

Now suppose evidence about Vehicle 8 becomes stale.

The system contains uncertain evidence, but the uncertain evidence does not
affect a dependency of the Vehicle 2 assignment.

A global evidence-quality mechanism may react to the uncertainty simply because
uncertain evidence exists.

A decision-conditioned mechanism should be capable of determining that the
Vehicle 8 evidence is irrelevant to the Vehicle 2 decision.

EXP-009 tests this distinction directly.

---

## 7. Dependency Families

The experiment retains the three dependency families used in EXP-007 and
EXP-008.

### 7.1 Capacity

The selected vehicle must have sufficient capacity for the assigned order.

### 7.2 Operational Status

The selected vehicle must remain operational.

### 7.3 Location / Availability

The selected vehicle must remain available and within the permitted dispatch
location.

This preserves continuity with the preceding experiments.

---

## 8. Evidence Quality Conditions

EXP-009 evaluates the imperfect-evidence states established by EXP-008:

- stale;
- missing;
- conflicting.

Reliable evidence is retained as a control.

The critical additional experimental variable is:

\[
Evidence\ Relevance
\]

with two principal states:

- decision-relevant;
- decision-irrelevant.

---

## 9. Frozen Experimental Matrix

The final matrix was frozen before execution.

The experiment contains:

- 3 dependency families;
- 3 imperfect evidence states;
- 2 evidence-relevance states;
- 2 physical-validity states;
- 6 reliable controls.

This produces:

\[
36\ imperfect\ conditions + 6\ controls = 42\ conditions
\]

The matrix contains:

- 14 capacity conditions;
- 14 status conditions;
- 14 location / availability conditions;
- 21 physically valid conditions;
- 21 physically invalid conditions;
- 18 relevant imperfect-evidence conditions;
- 18 irrelevant imperfect-evidence conditions;
- 12 stale conditions;
- 12 missing conditions;
- 12 conflicting conditions;
- 6 reliable controls.

The complete frozen condition definitions are recorded separately in:

`docs/experiment_009_condition_matrix.md`

---

## 10. Paired Conditions

The matrix contains paired conditions where evidence quality is held constant
while decision relevance changes.

The principal imperfect-evidence comparisons are:

### Irrelevant Uncertainty

The uncertain evidence does not belong to a dependency required by the pending
decision.

The pending decision retains usable evidence for its required dependency.

### Relevant Uncertainty

The uncertain evidence directly affects a dependency required by the pending
decision.

No reliable duplicate observation is introduced to silently resolve that
uncertainty.

This pairing is repeated for:

- stale evidence;
- missing evidence;
- conflicting evidence;

and across:

- capacity;
- status;
- location / availability.

---

## 11. Unsafe-Decision Controls

Autonomy preservation alone is insufficient evidence of improved assurance.

The matrix therefore contains physically invalid decisions as well as valid
decisions.

For each condition:

\[
Physical\ Decision \in \{VALID, INVALID\}
\]

This allows the experiment to distinguish genuine autonomy preservation from
unsafe permissiveness.

A policy cannot be interpreted as improved merely because it allows more
decisions.

---

## 12. Comparator Policies

The frozen experiment evaluates five primary policies.

### P0 — No Assurance

Always permits autonomous execution.

Purpose:

- maximum-autonomy reference;
- unsafe baseline.

---

### P1 — Global Evidence-Uncertainty Policy

Reduces autonomous authority whenever uncertain runtime evidence exists,
regardless of whether the evidence affects the current decision.

Purpose:

- measure the cost of treating all system uncertainty as decision relevant.

---

### P2 — Entity-Filtered Uncertainty

Filters uncertain evidence according to the entity selected by the pending
decision.

Purpose:

- test whether any apparent benefit can be explained by simple entity
  filtering rather than dependency reasoning;
- operationalise Kill Test F.

This baseline does not perform full decision-dependency reasoning.

---

### P3 — Uncertainty-Aware Runtime Contract

Evaluates the requirements of the pending decision and explicitly handles
evidence quality.

Purpose:

- strongest simpler assurance comparator;
- continuation of the runtime-contract challenge exposed in EXP-007 and
  EXP-008.

The comparator is not artificially weakened to favour DARA-DT.

---

### P4 — DARA-DT Decision-Conditioned Assurance

Evaluates runtime evidence relative to the dependencies of the specific
AI-generated decision and combines this with decision-validity reasoning.

Conceptually:

\[
U_t^{rel}(d_t)=U_t\cap Dep(d_t)
\]

Decision-irrelevant uncertain evidence does not automatically remove autonomous
authority.

Decision-relevant uncertain evidence may reduce autonomous authority.

---

## 13. Diagnostic Dependency-Conditioned Ablation

In addition to the five primary policies, the implementation includes a raw
dependency-conditioned uncertainty diagnostic.

Its purpose is to isolate the effect of exact dependency matching from the
complete DARA-DT assurance mechanism.

This diagnostic is not treated as a sixth primary comparator.

The conceptual ablation is:

\[
Global\ Uncertainty
\rightarrow
Entity\text{-}Filtered\ Uncertainty
\rightarrow
Decision\text{-}Dependency\text{-}Conditioned\ Uncertainty
\]

This is important because:

\[
SelectedEntity \neq CompleteDecisionDependency
\]

A logistics decision can depend on multiple variables and entities rather than
only a selected vehicle identifier.

---

## 14. Fairness Constraint

All runtime policies receive equivalent observable runtime information.

No policy receives:

- physical ground truth;
- evaluator labels;
- future state;
- hidden scenario identifiers;
- information derived from the expected experimental outcome.

Differences between policies arise from assurance logic rather than unequal
access to evidence.

---

## 15. Independent Ground Truth

Physical decision validity is determined independently.

For every condition:

\[
GroundTruth(d_t,P_t)
\]

determines whether intervention was actually required.

Runtime policies do not call this evaluator during authority selection.

Ground truth is used only after the assurance decision to classify the
experimental outcome.

---

## 16. Primary Outcome Categories

Each assurance decision is classified as:

- True Intervention (TI)
- False Intervention (FI)
- Missed Intervention (MI)
- Correct Non-Intervention (CNI)

These remain consistent with EXP-005 through EXP-008.

---

## 17. Metrics

The experiment reports:

### Safety Metrics

- True Interventions
- Missed Interventions
- Intervention Recall
- Missed-Intervention Rate

### Over-Intervention Metrics

- False Interventions
- False-Intervention Rate
- Precision

### Autonomy Metrics

- Autonomy Availability
- ALLOW frequency
- RESTRICT frequency
- DEFER frequency
- FALLBACK frequency

### Overall Metric

- Accuracy

The central evaluation remains the trade-off:

\[
Safety
\leftrightarrow
Autonomy\ Availability
\]

---

## 18. Pre-Registered Falsification Criteria

EXP-009 was explicitly falsification-oriented.

### Kill Test A — No Autonomy Advantage

If DARA-DT and the strongest uncertainty-aware comparator have equivalent
autonomy availability while maintaining equivalent safety, the claim that
decision conditioning improves autonomy preservation is not supported.

### Kill Test B — Safety Degradation

If DARA-DT preserves additional autonomy but increases missed interventions,
the additional autonomy cannot be interpreted as an assurance improvement.

### Kill Test C — Runtime Contract Equivalence

If an ordinary uncertainty-aware runtime contract can achieve the same
safety/autonomy trade-off using less mechanism complexity, the stronger
DARA-DT contribution claim is weakened.

### Kill Test D — Capacity-Only Effect

If the proposed benefit occurs only for capacity and does not reproduce for
status or location / availability, the framework-level generalisation claim
must be narrowed.

### Kill Test E — Evidence Privilege

If DARA-DT requires evidence unavailable to the comparator in order to achieve
better results, the comparison is invalid.

### Kill Test F — Trivial Entity Filtering

If the apparent benefit can be reproduced simply by filtering evidence by
selected entity identifier, the contribution must be described as simple
filtering rather than general decision-conditioned assurance.

These criteria were fixed before the final results were interpreted.

---

# 19. Experimental Results

EXP-009 executed all:

\[
N=42
\]

frozen conditions.

The complete automated test suite passed following implementation and metric
integration.

---

## 19.1 Aggregate Assurance Results

| Policy | N | TI | FI | MI | CNI | Accuracy | Precision | Recall | FI Rate | MI Rate | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 42 | 0 | 0 | 21 | 21 | 0.500 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| Global Uncertainty | 42 | 18 | 18 | 3 | 3 | 0.500 | 0.500 | 0.857 | 0.857 | 0.143 | 0.143 |
| Entity Filtered | 42 | 9 | 9 | 12 | 12 | 0.500 | 0.500 | 0.429 | 0.429 | 0.571 | 0.571 |
| Uncertainty Contract | 42 | 21 | 9 | 0 | 12 | 0.786 | 0.700 | 1.000 | 0.429 | 0.000 | 0.286 |
| DARA-DT | 42 | 21 | 9 | 0 | 12 | 0.786 | 0.700 | 1.000 | 0.429 | 0.000 | 0.286 |

The principal aggregate result is:

\[
DARA\text{-}DT =
UncertaintyAwareRuntimeContract
\]

at the binary assurance-outcome level.

Both produced:

\[
TI=21,\quad FI=9,\quad MI=0,\quad CNI=12
\]

with:

\[
Accuracy=0.786
\]

\[
Recall=1.000
\]

and:

\[
AutonomyAvailability=0.286
\]

Therefore EXP-009 does **not** establish superior binary assurance performance
for DARA-DT over the uncertainty-aware runtime contract.

---

## 19.2 Authority-State Distribution

| Policy | ALLOW | RESTRICT | DEFER | FALLBACK |
|---|---:|---:|---:|---:|
| No Assurance | 42 | 0 | 0 | 0 |
| Global Uncertainty | 6 | 0 | 36 | 0 |
| Entity Filtered | 24 | 0 | 18 | 0 |
| Uncertainty Contract | 12 | 12 | 18 | 0 |
| DARA-DT | 12 | 0 | 30 | 0 |

Although DARA-DT and the uncertainty-aware contract have identical binary
intervention outcomes, their authority semantics are not identical.

The runtime contract uses:

\[
RESTRICT=12,\quad DEFER=18
\]

whereas DARA-DT uses:

\[
RESTRICT=0,\quad DEFER=30
\]

Both permit autonomous execution in 12 conditions.

This distinction is descriptive rather than evidence of superiority.

The present experiment does not establish that one authority decomposition is
preferable to the other.

---

# 20. Results by Evidence Quality

## 20.1 Reliable Evidence

For the six reliable controls:

| Policy | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 3 | 3 | 0.500 | 0.000 | 1.000 |
| Global Uncertainty | 0 | 0 | 3 | 3 | 0.500 | 0.000 | 1.000 |
| Entity Filtered | 0 | 0 | 3 | 3 | 0.500 | 0.000 | 1.000 |
| Uncertainty Contract | 3 | 0 | 0 | 3 | 1.000 | 1.000 | 0.500 |
| DARA-DT | 3 | 0 | 0 | 3 | 1.000 | 1.000 | 0.500 |

The runtime contract and DARA-DT both perfectly classify the six reliable
control conditions.

---

## 20.2 Stale Evidence

For the 12 stale-evidence conditions:

| Policy | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 6 | 6 | 0.500 | 0.000 | 1.000 |
| Global Uncertainty | 6 | 6 | 0 | 0 | 0.500 | 1.000 | 0.000 |
| Entity Filtered | 3 | 3 | 3 | 3 | 0.500 | 0.500 | 0.500 |
| Uncertainty Contract | 6 | 3 | 0 | 3 | 0.750 | 1.000 | 0.250 |
| DARA-DT | 6 | 3 | 0 | 3 | 0.750 | 1.000 | 0.250 |

---

## 20.3 Missing Evidence

For the 12 missing-evidence conditions:

| Policy | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 6 | 6 | 0.500 | 0.000 | 1.000 |
| Global Uncertainty | 6 | 6 | 0 | 0 | 0.500 | 1.000 | 0.000 |
| Entity Filtered | 3 | 3 | 3 | 3 | 0.500 | 0.500 | 0.500 |
| Uncertainty Contract | 6 | 3 | 0 | 3 | 0.750 | 1.000 | 0.250 |
| DARA-DT | 6 | 3 | 0 | 3 | 0.750 | 1.000 | 0.250 |

---

## 20.4 Conflicting Evidence

For the 12 conflicting-evidence conditions:

| Policy | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 6 | 6 | 0.500 | 0.000 | 1.000 |
| Global Uncertainty | 6 | 6 | 0 | 0 | 0.500 | 1.000 | 0.000 |
| Entity Filtered | 3 | 3 | 3 | 3 | 0.500 | 0.500 | 0.500 |
| Uncertainty Contract | 6 | 3 | 0 | 3 | 0.750 | 1.000 | 0.250 |
| DARA-DT | 6 | 3 | 0 | 3 | 0.750 | 1.000 | 0.250 |

The same pattern is observed for stale, missing, and conflicting evidence.

This controlled symmetry indicates that the result is not attributable to one
specific imperfect-evidence category within the frozen matrix.

---

# 21. Results by Dependency Family

Each dependency family contains 14 conditions.

The DARA-DT results are identical across all three families:

| Dependency | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|
| Capacity | 7 | 3 | 0 | 4 | 0.786 | 1.000 | 0.286 |
| Status | 7 | 3 | 0 | 4 | 0.786 | 1.000 | 0.286 |
| Location / Availability | 7 | 3 | 0 | 4 | 0.786 | 1.000 | 0.286 |

The uncertainty-aware runtime contract produces the same binary results for
each dependency family.

Therefore:

1. the observed behaviour is not capacity-specific;
2. the result reproduces across the three controlled dependency families;
3. this cross-family consistency does not resolve runtime-contract
   equivalence.

---

# 22. Decision-Relevant vs Decision-Irrelevant Uncertainty

This is the central EXP-009 comparison.

## 22.1 Decision-Relevant Imperfect Evidence

Across the 18 relevant imperfect-evidence conditions:

| Policy | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 9 | 9 | 0.500 | 0.000 | 1.000 |
| Global Uncertainty | 9 | 9 | 0 | 0 | 0.500 | 1.000 | 0.000 |
| Entity Filtered | 9 | 9 | 0 | 0 | 0.500 | 1.000 | 0.000 |
| Uncertainty Contract | 9 | 9 | 0 | 0 | 0.500 | 1.000 | 0.000 |
| DARA-DT | 9 | 9 | 0 | 0 | 0.500 | 1.000 | 0.000 |

All conservative assurance mechanisms intervene on all 18 relevant uncertain
conditions.

Because half of these decisions are physically valid, this produces nine false
interventions as the cost of conservative uncertainty handling.

---

## 22.2 Decision-Irrelevant Imperfect Evidence

Across the 18 irrelevant imperfect-evidence conditions:

| Policy | TI | FI | MI | CNI | Accuracy | Recall | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 9 | 9 | 0.500 | 0.000 | 1.000 |
| Global Uncertainty | 9 | 9 | 0 | 0 | 0.500 | 1.000 | 0.000 |
| Entity Filtered | 0 | 0 | 9 | 9 | 0.500 | 0.000 | 1.000 |
| Uncertainty Contract | 9 | 0 | 0 | 9 | 1.000 | 1.000 | 0.500 |
| DARA-DT | 9 | 0 | 0 | 9 | 1.000 | 1.000 | 0.500 |

This is the strongest positive finding from EXP-009.

Under decision-irrelevant uncertainty:

\[
DARA\text{-}DT:
TI=9,\ FI=0,\ MI=0,\ CNI=9
\]

and:

\[
Accuracy=1.000
\]

\[
Recall=1.000
\]

\[
AutonomyAvailability=0.500
\]

Global uncertainty removes autonomy from every condition.

Entity filtering preserves autonomy but misses all nine invalid decisions.

DARA-DT therefore demonstrates that selective treatment of irrelevant
uncertainty can preserve autonomous execution for valid decisions without
missing the invalid decisions in this controlled subset.

However, the uncertainty-aware runtime contract achieves the **same result**.

Therefore the result supports the usefulness of decision-sensitive assurance
logic but does not establish DARA-DT-specific superiority.

---

# 23. Falsification Results

The six pre-registered kill tests produced the following outcomes.

| Kill Test | Result |
|---|---|
| A — No Autonomy Advantage | **TRIGGERED** |
| B — Safety Degradation | **NOT TRIGGERED** |
| C — Runtime Contract Equivalence | **TRIGGERED** |
| D — Capacity-Only Effect | **NOT TRIGGERED** |
| E — Evidence Privilege | **NOT TRIGGERED** |
| F — Trivial Entity Filtering | **NOT TRIGGERED** |

---

## 23.1 Kill Test A — No Autonomy Advantage

**Result: TRIGGERED**

DARA-DT does not provide greater aggregate autonomy availability than the
uncertainty-aware runtime contract while maintaining equivalent
missed-intervention safety.

Both produce:

\[
AutonomyAvailability=0.286
\]

and:

\[
MI=0
\]

Therefore the pre-registered claim that DARA-DT improves autonomy preservation
relative to the strongest uncertainty-aware comparator is not supported by
EXP-009.

---

## 23.2 Kill Test B — Safety Degradation

**Result: NOT TRIGGERED**

DARA-DT does not obtain an autonomy advantage by accepting additional missed
unsafe interventions.

The policy records:

\[
MI=0
\]

Therefore the observed behaviour is not explained by sacrificing the
missed-intervention safety criterion.

---

## 23.3 Kill Test C — Runtime Contract Equivalence

**Result: TRIGGERED**

This is the most important falsification result.

The uncertainty-aware runtime contract and DARA-DT have identical aggregate
binary assurance outcomes:

\[
TI=21,\ FI=9,\ MI=0,\ CNI=12
\]

They also have identical:

- accuracy;
- precision;
- recall;
- false-intervention rate;
- missed-intervention rate;
- autonomy availability.

The equivalence also reproduces:

- across stale, missing, and conflicting evidence;
- across capacity, status, and location / availability;
- across relevant and irrelevant uncertainty subsets.

Therefore EXP-009 does not demonstrate that the additional DARA-DT mechanism
improves binary intervention performance beyond the uncertainty-aware runtime
contract for the tested decision structure.

The stronger superiority claim must be rejected for this experiment.

---

## 23.4 Kill Test D — Capacity-Only Effect

**Result: NOT TRIGGERED**

The result is not confined to capacity.

The same DARA-DT binary metrics occur for:

- capacity;
- status;
- location / availability.

However, DARA-DT also fails to outperform the runtime contract in each of those
families.

The appropriate interpretation is therefore cross-family consistency, not
cross-family superiority.

---

## 23.5 Kill Test E — Evidence Privilege

**Result: NOT TRIGGERED**

All 42 conditions expose a shared runtime-evidence collection.

DARA-DT does not receive:

- physical ground truth;
- evaluator validity labels;
- future information;
- a separate privileged evidence source.

Physical validity is used only after authority selection by the evaluator.

The comparison therefore satisfies the evidence-parity constraint implemented
for EXP-009.

---

## 23.6 Kill Test F — Trivial Entity Filtering

**Result: NOT TRIGGERED**

Entity filtering does not reproduce the complete DARA-DT safety/autonomy
trade-off.

The entity-filtered policy obtains:

\[
TI=9,\ FI=9,\ MI=12,\ CNI=12
\]

whereas DARA-DT obtains:

\[
TI=21,\ FI=9,\ MI=0,\ CNI=12
\]

Entity filtering therefore preserves more autonomous execution:

\[
0.571
\]

versus:

\[
0.286
\]

but does so while missing 12 required interventions.

Consequently, the complete DARA-DT behaviour cannot be reduced to entity
filtering alone in this matrix.

This does not establish DARA-DT superiority over the stronger runtime-contract
baseline.

---

# 24. Interpretation

EXP-009 produces a mixed but informative result.

## 24.1 What the Experiment Supports

The experiment supports the controlled observation that treating all uncertain
system evidence as equally relevant can be unnecessarily conservative.

Global uncertainty obtains only:

\[
AutonomyAvailability=0.143
\]

across the complete matrix.

Decision-sensitive mechanisms can distinguish uncertainty that affects the
pending decision from uncertainty that does not.

Within the decision-irrelevant imperfect-evidence subset, both DARA-DT and the
uncertainty-aware runtime contract achieve:

\[
Accuracy=1.000
\]

\[
Recall=1.000
\]

\[
FI=0
\]

\[
MI=0
\]

while retaining:

\[
AutonomyAvailability=0.500
\]

This demonstrates the value of conditioning assurance on information relevant
to the pending decision rather than treating all system uncertainty globally.

---

## 24.2 What the Experiment Does Not Support

EXP-009 does **not** support the claim that DARA-DT provides a superior
safety-autonomy trade-off to a properly designed uncertainty-aware runtime
contract.

The two mechanisms are equivalent on all primary binary outcome metrics in the
frozen matrix.

Therefore the following claim is not justified:

> DARA-DT outperforms uncertainty-aware runtime contracts.

The experimental evidence instead supports the narrower conclusion:

> Decision-sensitive runtime assurance can reduce unnecessary conservatism
> relative to global uncertainty monitoring, but the tested DARA-DT mechanism
> does not provide additional binary assurance performance beyond an
> uncertainty-aware runtime contract for the decision structures evaluated in
> EXP-009.

---

# 25. Authority Semantics

EXP-009 reveals one unresolved difference that is not visible in the binary
outcome metrics.

The uncertainty-aware contract uses:

- ALLOW;
- RESTRICT;
- DEFER.

DARA-DT uses:

- ALLOW;
- DEFER.

This results in:

\[
Contract:
ALLOW=12,\ RESTRICT=12,\ DEFER=18
\]

versus:

\[
DARA:
ALLOW=12,\ RESTRICT=0,\ DEFER=30
\]

The binary evaluator treats every non-ALLOW authority state as an intervention.

Consequently, EXP-009 cannot determine whether the semantic distinction between
RESTRICT and DEFER has operational value.

This is an identified limitation of the current evaluation framework rather
than evidence that either mechanism is better.

A future experiment should evaluate authority states through their downstream
operational consequences rather than collapsing them into a single binary
intervention category.

---

# 26. Relationship to Previous Experiments

The experimental progression is now:

### EXP-004

Established that decision relevance alone is insufficient.

### EXP-005

Introduced decision-specific impact and physical-validity boundaries.

### EXP-006

Introduced imperfect runtime evidence.

### EXP-007

Generalised impact reasoning across capacity, status, and
location / availability and exposed equivalence with a simpler runtime contract
under reliable evidence.

### EXP-008

Tested stale, missing, and conflicting evidence.

DARA-DT and the uncertainty-aware runtime contract achieved identical binary
performance.

### EXP-009

Separated decision-relevant from decision-irrelevant evidence uncertainty.

The experiment demonstrated that decision-sensitive assurance avoids some
unnecessary conservatism associated with global uncertainty monitoring.

However, runtime-contract equivalence persisted.

This repeated equivalence is now an important empirical result rather than an
isolated observation.

---

# 27. Contribution Reassessment

EXP-009 requires the candidate DARA-DT contribution to be narrowed.

The current evidence supports:

1. explicit modelling of physical–digital divergence;
2. decision-specific dependency reasoning;
3. decision-validity reasoning;
4. explicit runtime evidence quality;
5. selective handling of decision-irrelevant uncertainty;
6. cross-dependency evaluation across capacity, status, and
   location / availability.

The current evidence does **not** establish:

1. general superiority of DARA-DT over runtime contracts;
2. improved aggregate autonomy relative to the strongest comparator;
3. a unique binary intervention capability unavailable to simpler
   uncertainty-aware contracts.

The safe contribution statement after EXP-009 is therefore:

> **DARA-DT provides an experimental framework for studying how
> physical–digital divergence, runtime evidence quality, and decision
> dependencies interact in runtime assurance for AI-driven logistics Digital
> Twins. Controlled experiments show that decision-sensitive assurance can
> avoid unnecessary intervention caused by globally irrelevant uncertainty,
> while also revealing that a strong uncertainty-aware runtime contract can
> reproduce the same binary safety–autonomy trade-off in the tested decision
> structures.**

This statement is deliberately narrower than a superiority claim.

---

# 28. Novelty Implication

The remaining novelty question becomes sharper:

> **Under what runtime decision structures, if any, does explicit
> decision-conditioned physical–digital divergence provide assurance
> information that cannot be represented adequately by ordinary runtime
> contracts?**

EXP-009 does not answer this question positively.

Instead, it provides evidence that simple single-decision dependency structures
may be representable adequately through strong runtime contracts.

This result should constrain the design of any subsequent experiment.

A further experiment is justified only if it tests a genuinely different
mechanism or decision structure rather than expanding the matrix until DARA-DT
appears superior.

---

# 29. Candidate Next Research Test

A scientifically justified next stage would investigate whether the equivalence
persists when assurance must reason over dependencies that cannot be represented
as a single local state check.

Candidate structures include:

- compound dependencies across multiple entities;
- cascading decisions where one autonomous decision changes the validity of a
  later decision;
- divergence propagation across a decision chain;
- interacting physical–digital mismatches;
- authority-state consequences where RESTRICT, DEFER, and FALLBACK produce
  different operational outcomes.

The purpose of such an experiment would not be to force a DARA-DT advantage.

The question would be:

> Does runtime-contract equivalence continue under richer, interacting
> decision dependencies?

If equivalence persists, the contribution claim must be narrowed further.

If equivalence breaks under a pre-registered design, the specific mechanism
responsible must be isolated and tested independently.

---

# 30. Threats to Validity

EXP-009 remains a controlled research prototype.

Important limitations include:

### Controlled Matrix

The 42 conditions are deliberately structured rather than sampled from
real-world fleet operations.

### Symmetric Factor Design

The balanced matrix creates intentionally symmetric results across several
evidence-quality and dependency groups.

### Simplified Decisions

The current assignment decisions use relatively local and explicit
dependencies.

### Binary Outcome Evaluation

TI, FI, MI, and CNI collapse RESTRICT, DEFER, and FALLBACK into intervention.

This prevents the experiment from evaluating the operational value of different
authority states.

### Limited Operational Consequences

The experiment evaluates immediate decision validity rather than downstream
effects such as:

- lateness;
- service failure;
- recovery cost;
- route disruption;
- cascading assignment effects.

### No Claim of External Generalisation

The results demonstrate behaviour within the implemented controlled matrix.

They do not establish general superiority across logistics systems or Digital
Twin architectures.

---

# 31. Reproducibility

The experiment is implemented through:

- frozen condition definitions;
- explicit policy implementations;
- independent physical ground truth;
- automated outcome classification;
- aggregate metrics;
- evidence-status breakdowns;
- dependency-family breakdowns;
- relevance breakdowns;
- authority-state distributions;
- pre-registered kill-test evaluation;
- automated regression tests;
- continuous integration execution.

The experiment can be reproduced using the repository's automated research
workflow.

---

# 32. Final EXP-009 Conclusion

EXP-009 successfully tests the pre-registered decision-relevance hypothesis
without assuming a favourable DARA-DT outcome.

Three conclusions are supported by the controlled experiment.

First:

> Global treatment of runtime evidence uncertainty is unnecessarily
> conservative when uncertainty is unrelated to the pending decision.

Second:

> Simple entity filtering preserves autonomy but is insufficient to maintain
> safety across the frozen valid/invalid conditions.

Third, and most importantly:

> DARA-DT and the uncertainty-aware runtime contract achieve the same binary
> safety–autonomy trade-off across all 42 EXP-009 conditions.

Accordingly:

\[
KillTestA = TRIGGERED
\]

and:

\[
KillTestC = TRIGGERED
\]

while:

\[
KillTestsB,D,E,F = NOT\ TRIGGERED
\]

The candidate DARA-DT contribution therefore survives neither as a demonstrated
aggregate autonomy improvement nor as a demonstrated binary-performance
advantage over the strongest runtime-contract comparator.

The experiment instead sharpens the research problem.

The next scientifically defensible question is no longer:

> Does DARA-DT outperform a runtime contract in this matrix?

It is:

> **Does explicit decision-conditioned physical–digital divergence provide
> additional assurance value when autonomous decisions involve interacting,
> compound, or temporally propagating dependencies that cannot be reduced to
> the local runtime contracts evaluated so far?**

That question should be addressed only through a separately pre-registered
experiment.

---

## 33. Final Research Question Record

The pre-registered EXP-009 question was:

> **Can decision-conditioned runtime assurance distinguish
> decision-relevant from decision-irrelevant evidence uncertainty in dynamic
> logistics Digital Twins, preserving autonomous authority without increasing
> missed unsafe interventions relative to simpler uncertainty-aware assurance
> mechanisms?**

### Answer from EXP-009

**Partially.**

Decision-sensitive assurance successfully distinguishes relevant from
irrelevant uncertainty relative to global uncertainty monitoring.

However, DARA-DT does not preserve more autonomy than the strongest
uncertainty-aware runtime-contract comparator and does not improve its binary
assurance performance.

The strongest pre-registered comparator therefore remains sufficient for the
decision structures represented in EXP-009.
