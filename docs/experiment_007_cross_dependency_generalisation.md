# EXP-007 — Cross-Dependency Generalisation

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-007  
**Stage:** Cross-Dependency Generalisation  
**Status:** Experimental Design — Pre-Implementation  
**Domain:** Autonomous Logistics Systems  
**Evidence Condition:** Reliable runtime evidence  
**Primary Purpose:** Generalisation and falsification

---

## 1. Motivation

EXP-001 to EXP-006 progressively established and challenged the developing
DARA-DT reasoning chain:

```text
Physical–Digital Divergence
        ↓
Decision Dependency
        ↓
Decision Relevance
        ↓
Decision Impact / Validity
        ↓
Evidence Reliability
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

However, an important limitation remains.

Much of the strongest later experimental evidence is based on:

```text
vehicle capacity
```

This creates a plausible alternative explanation:

> DARA-DT may currently be demonstrating sophisticated capacity-feasibility
> checking rather than a general decision-conditioned divergence mechanism.

EXP-007 is designed to test that explanation directly.

---

# 2. Research Question

The primary experimental question is:

> **Does the relationship between physical–digital divergence, decision
> relevance, decision impact and runtime intervention generalise across
> different logistics decision dependencies?**

The experiment evaluates three dependency families:

```text
Capacity
Operational Status
Location / Availability
```

These represent different decision semantics while remaining inside the
existing autonomous-logistics research scope.

---

# 3. Connection to the Central Research Question

The project's central research question is:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

EXP-007 addresses the generalisation component of this question.

Previous experiments establish controlled behaviour for individual
mechanisms.

EXP-007 asks whether the mechanism remains meaningful when the type of state
dependency changes.

---

# 4. Experimental Objective

The objective is not to make DARA-DT outperform every baseline.

The objective is to determine whether the conceptual relationship:

```text
Physical–Digital Divergence
        ↓
Decision Dependency
        ↓
Decision Relevance
        ↓
Decision Impact
        ↓
Runtime Intervention
```

remains operational across different logistics dependencies.

A failure to generalise is a valid research result.

---

# 5. Primary Hypothesis

## H1

> Decision-conditioned divergence can distinguish intervention-relevant from
> intervention-irrelevant physical–digital mismatches across multiple
> logistics decision dependencies.

The experiment should attempt to falsify this hypothesis.

---

# 6. Secondary Hypotheses

## H2 — Global Divergence

> Global divergence monitoring will produce unnecessary intervention when
> divergence exists but does not invalidate the current decision.

---

## H3 — Relevance

> Decision relevance will improve discrimination over global divergence but
> will remain insufficient when a relevant mismatch does not invalidate the
> decision.

---

## H4 — Impact

> Decision-impact reasoning will distinguish relevant-but-valid divergence
> from relevant-and-invalid divergence across multiple dependency families.

---

## H5 — Dependency Generalisation

> The relevance → impact distinction observed in capacity experiments will
> remain meaningful for operational-status and location/availability
> dependencies.

H5 is the primary generalisation hypothesis.

---

# 7. Null / Competing Explanations

EXP-007 must explicitly consider explanations that could weaken DARA-DT.

## CE1 — Capacity-Specific Explanation

The existing results may arise because capacity has a simple numerical
feasibility condition:

```text
capacity >= demand
```

If the mechanism does not transfer meaningfully to categorical or spatial
dependencies, the broader framework claim should be narrowed.

---

## CE2 — Runtime Contract Explanation

A simple runtime contract may be sufficient.

For example:

```text
capacity >= demand
```

```text
status == operational
```

```text
availability == true
```

or:

```text
vehicle_location compatible with assignment
```

may determine whether the decision remains executable without requiring a
separate divergence-aware reasoning layer.

---

## CE3 — Global Fidelity Explanation

A sufficiently informative global Digital Twin trust or fidelity mechanism
may provide equivalent intervention information.

---

# 8. Experimental Scope

EXP-007 initially uses:

```text
Reliable runtime evidence
Controlled physical state
Controlled Digital Twin state
Deterministic decision generation
Known ground truth
Controlled divergence injection
```

Imperfect evidence is deliberately excluded from the primary experiment.

Reason:

> EXP-007 should isolate dependency type rather than simultaneously changing
> dependency semantics and evidence reliability.

Evidence uncertainty has already been investigated separately in EXP-006.

---

# 9. Dependency Family A — Capacity

Capacity remains the reference dependency.

A vehicle assignment depends on:

```text
physical_capacity >= order_demand
```

Example:

```text
Twin capacity     = 10
Physical capacity = 6
Demand            = 8
```

The Twin supports the assignment.

Physical reality does not.

Therefore:

```text
Decision = INVALID
Intervention Required = YES
```

---

# 10. Capacity Control Condition

Example:

```text
Twin capacity     = 10
Physical capacity = 7
Demand            = 5
```

Divergence exists.

Capacity is decision-relevant.

However:

```text
7 >= 5
```

Therefore:

```text
Decision = VALID
Intervention Required = NO
```

This preserves the relevance-versus-impact distinction established in
EXP-004 and EXP-005.

---

# 11. Dependency Family B — Operational Status

The second dependency family concerns whether the selected vehicle remains
operational.

A decision may depend on:

```text
vehicle_status == operational
```

Example:

```text
Digital Twin:
vehicle_01.status = operational

Physical System:
vehicle_01.status = broken_down
```

The decision:

```text
assign vehicle_01 to order_01
```

was generated from stale or incorrect Twin state.

Therefore:

```text
Divergence = RELEVANT
Decision = INVALID
Intervention Required = YES
```

---

# 12. Operational-Status Irrelevant Condition

The experiment must also include divergence on an unrelated vehicle.

Example:

```text
Selected vehicle:
vehicle_01

Divergent vehicle:
vehicle_05
```

Physical state:

```text
vehicle_05 = broken_down
```

Twin state:

```text
vehicle_05 = operational
```

If the current decision depends only on:

```text
vehicle_01
```

then the divergence is:

```text
Detected = YES
Decision Relevant = NO
Intervention Required = NO
```

This tests whether the framework avoids global over-intervention.

---

# 13. Dependency Family C — Location / Availability

The third dependency family concerns whether the selected vehicle is
available in a location compatible with the assignment.

A decision may depend on:

```text
vehicle_available == true
```

and/or:

```text
vehicle_location compatible with assignment
```

Example:

```text
Digital Twin:
vehicle_01.location = depot
vehicle_01.available = true

Physical System:
vehicle_01.location = remote_site
vehicle_01.available = false
```

If immediate dispatch from the depot is required:

```text
Decision = INVALID
Intervention Required = YES
```

---

# 14. Location / Availability Control

The experiment must distinguish divergence from invalidity.

Example:

```text
Digital Twin location:
depot

Physical location:
near_depot

Decision requirement:
vehicle can still satisfy dispatch constraint
```

A location difference may be relevant without necessarily invalidating the
decision.

The exact compatibility rule must be defined explicitly in implementation.

It must not be changed after observing results merely to improve DARA-DT
performance.

---

# 15. Experimental Condition Structure

Each dependency family should contain at least the following conceptual
conditions:

```text
C0 — No relevant divergence
C1 — Irrelevant divergence
C2 — Relevant but decision-valid divergence
C3 — Relevant and decision-invalid divergence
```

This produces the conceptual matrix:

| Condition | Divergence | Relevant? | Decision Valid? | Intervention Required? |
|---|---|---:|---:|---:|
| C0 | None / irrelevant to selected dependency | No | Yes | No |
| C1 | Present elsewhere | No | Yes | No |
| C2 | Present on dependency | Yes | Yes | No |
| C3 | Present on dependency | Yes | No | Yes |

Not every dependency needs identical internal mechanics.

The semantics must remain appropriate to the dependency being tested.

---

# 16. Minimum Experimental Matrix

The initial target is:

```text
3 dependency families
×
4 conceptual conditions
=
12 controlled conditions
```

Therefore the initial EXP-007 matrix should contain at least:

```text
12 conditions
```

before optional stress cases are added.

---

# 17. Proposed Condition IDs

## Capacity

```text
CAP-0
CAP-1
CAP-2
CAP-3
```

## Operational Status

```text
STATUS-0
STATUS-1
STATUS-2
STATUS-3
```

## Location / Availability

```text
LOC-0
LOC-1
LOC-2
LOC-3
```

These identifiers should remain stable once implementation begins.

---

# 18. Ground Truth

Ground truth must be derived independently from physical state.

The assurance policy must not define the label used to evaluate itself.

Conceptually:

```text
Physical State
        ↓
Independent Decision Validator
        ↓
VALID / INVALID
        ↓
Intervention Ground Truth
```

---

# 19. Capacity Ground Truth

For capacity:

\[
Valid_{capacity}(d)=
C_{physical}\geq Demand(d)
\]

Therefore:

```text
True  → intervention not required
False → intervention required
```

---

# 20. Operational-Status Ground Truth

For operational status:

```text
selected_vehicle.status == operational
```

must hold.

If:

```text
selected_vehicle.status == broken_down
```

the assignment is invalid.

---

# 21. Location / Availability Ground Truth

The location/availability rule must be explicitly encoded before execution.

At minimum:

```text
selected_vehicle.available == true
```

must hold.

Where location is evaluated, the experiment must define a deterministic
compatibility condition.

For example:

```text
physical_location ∈ permitted_dispatch_locations
```

The implementation must avoid subjective post-hoc interpretation.

---

# 22. Assurance Policies

EXP-007 should initially compare:

```text
P0 — No Assurance
P1 — Global Divergence
P2 — Decision Relevance
P3 — Decision Impact
P4 — Runtime Contract / Assumption
```

The experiment should not assume that P3 must outperform P4.

---

# 23. P0 — No Assurance

Rule:

```text
Always allow autonomous execution.
```

Purpose:

- measure missed interventions;
- establish unrestricted-autonomy baseline.

---

# 24. P1 — Global Divergence

Rule:

```text
Any detected divergence
        ↓
Intervene
```

Purpose:

- test whether system-level mismatch alone is sufficiently selective.

---

# 25. P2 — Decision Relevance

Rule:

```text
Detected divergence
        ↓
Does it affect a decision dependency?
        ↓
YES → intervene
NO  → allow
```

Purpose:

- test whether dependency matching improves selectivity;
- expose relevant-but-valid false interventions.

---

# 26. P3 — Decision Impact

Rule:

```text
Relevant divergence
        ↓
Evaluate effect on physical decision validity
        ↓
Invalid → intervene
Valid   → allow
```

Purpose:

- test whether decision consequence adds information beyond relevance.

---

# 27. P4 — Runtime Contract / Assumption Baseline

This is a deliberately strong comparator.

For each dependency, define the operational condition required for execution.

Examples:

```text
Capacity:
physical_capacity >= demand
```

```text
Status:
physical_status == operational
```

```text
Availability:
physical_available == true
```

The baseline asks:

> If runtime evidence already permits direct checking of the execution
> condition, what additional value is provided by explicit
> physical–digital-divergence reasoning?

This baseline is scientifically important.

If it performs equivalently with less complexity, that result must be
reported.

---

# 28. Important Baseline Fairness Rule

P3 and P4 must receive comparable runtime evidence.

DARA-DT must not receive privileged access to physical information that is
withheld from the contract baseline.

Otherwise the comparison would be invalid.

---

# 29. Outcome Classes

Use the established DARA-DT outcome model:

```text
True Intervention (TI)
False Intervention (FI)
Missed Intervention (MI)
Correct Non-Intervention (CNI)
```

---

# 30. Primary Metrics

Calculate:

```text
TI
FI
MI
CNI
Accuracy
Precision
Recall
False Intervention Rate
Missed Intervention Rate
Autonomy Availability
```

Metrics should be calculated:

1. across the complete matrix; and
2. separately for each dependency family.

The second calculation is essential for detecting dependency-specific
failure.

---

# 31. Generalisation Metric

EXP-007 should not declare generalisation from aggregate accuracy alone.

Define a dependency-level success vector:

```text
G = [
    performance_capacity,
    performance_status,
    performance_location
]
```

A high aggregate score cannot hide failure in one dependency family.

---

# 32. Generalisation Criterion

A cautious generalisation criterion is:

> The mechanism demonstrates preliminary cross-dependency generalisation if
> the relevance → impact distinction remains operationally meaningful across
> all tested dependency families without changing the core assurance
> principle after observing results.

This does not establish universal generality.

---

# 33. Falsification Criterion F1

The broad framework hypothesis is weakened if:

```text
Decision Impact works for capacity
```

but:

```text
fails to provide meaningful discrimination
for status or location/availability.
```

---

# 34. Falsification Criterion F2

The candidate contribution is weakened if:

```text
Runtime Contract / Assumption
```

matches DARA-DT across all relevant outcomes while requiring:

```text
less state
less reasoning
less complexity
```

without introducing another meaningful disadvantage.

---

# 35. Falsification Criterion F3

The candidate contribution is weakened if:

```text
Global Divergence
```

performs equivalently across all designed conditions.

That would indicate that decision conditioning adds little experimental
value in the tested setting.

---

# 36. Falsification Criterion F4

The experiment fails to demonstrate generalisation if the same conceptual
assurance mechanism requires substantial post-hoc redesign for each
dependency.

Dependency-specific impact functions are acceptable.

A completely different assurance principle for every dependency would weaken
the framework interpretation.

---

# 37. Success Is Not Defined as Winning

EXP-007 must not use:

```text
DARA-DT has highest accuracy
```

as the sole success criterion.

The experiment is successful scientifically if it determines:

- where the mechanism generalises;
- where it does not;
- what information divergence contributes;
- whether simpler alternatives are sufficient; and
- what the framework's boundary conditions are.

---

# 38. Key Pairwise Comparisons

The most important comparisons are:

```text
Global Divergence
vs
Decision Relevance
```

to test dependency specificity.

Then:

```text
Decision Relevance
vs
Decision Impact
```

to test relevance versus validity.

Most importantly:

```text
Decision Impact
vs
Runtime Contract / Assumption
```

to test whether explicit divergence reasoning adds value beyond direct
runtime condition checking.

---

# 39. 2×2 Divergence-Relevance Test

Conditions should support the conceptual quadrants:

| | Low Decision Relevance | High Decision Relevance |
|---|---|---|
| **Low Global Divergence** | A | C |
| **High Global Divergence** | B | D |

Particularly important are:

```text
B:
High global divergence
Low decision relevance
```

and:

```text
C:
Low global divergence
High decision relevance
```

These conditions help separate global mismatch from decision consequence.

---

# 40. Expected Scientific Interpretations

## Result Pattern A

If global divergence over-intervenes but decision conditioning remains
selective:

```text
Evidence supports decision-conditioned reasoning.
```

---

## Result Pattern B

If relevance over-intervenes but impact does not:

```text
Evidence supports separating relevance from validity.
```

---

## Result Pattern C

If contract monitoring equals decision-impact assurance:

```text
DARA-DT's incremental value remains unresolved or weak.
```

The result must not be hidden.

---

## Result Pattern D

If performance varies substantially by dependency:

```text
DARA-DT requires dependency-specific boundary conditions.
```

---

## Result Pattern E

If the mechanism generalises across all three dependencies:

```text
Evidence supports preliminary cross-dependency generalisation.
```

This still does not establish novelty.

---

# 41. What EXP-007 Will Not Test

EXP-007 will not initially test:

```text
LLM reasoning
multi-agent coordination
cybersecurity attacks
blockchain
complex sensor fusion
large-scale fleet optimisation
real-world deployment
human-in-the-loop behaviour
```

These are outside the immediate experimental question.

---

# 42. Evidence Reliability

EXP-007 initially assumes reliable runtime evidence.

This is deliberate.

EXP-006 already demonstrated that imperfect evidence can alter assurance
outcomes.

Combining:

```text
new dependency types
+
new evidence uncertainty
```

in the same experiment would make causal interpretation more difficult.

A later experiment may combine these factors.

---

# 43. Implementation Requirements

Implementation should reuse the existing architecture where possible.

Likely components include:

```text
simulation/
twin/
divergence/
decision/
impact/
assurance/
evaluation/
experiments/
```

New code should only be introduced where required to represent:

- dependency-specific conditions;
- dependency-specific validity;
- the contract baseline; and
- EXP-007 aggregation.

---

# 44. Proposed Implementation Modules

Exact filenames may be refined after inspecting the current codebase.

Candidate modules are:

```text
src/dara_dt/experiments/cross_dependency_conditions.py
src/dara_dt/experiments/cross_dependency_experiment.py
src/dara_dt/experiments/cross_dependency_metrics.py
```

A contract baseline may require:

```text
src/dara_dt/assurance/contract_policy.py
```

Existing modules should be reused rather than duplicated where their
semantics already fit the experiment.

---

# 45. Test Requirements

Before accepting EXP-007 results, tests should verify:

```text
dependency mapping
divergence relevance
physical validity
ground-truth intervention labels
contract baseline behaviour
decision-impact behaviour
policy outcome classification
dependency-level aggregation
```

Tests should include both positive and negative cases.

---

# 46. Reproducibility Requirements

The experiment should be executable through a stable command such as:

```bash
uv run python -m dara_dt.experiments.cross_dependency_experiment
```

and metrics through:

```bash
uv run python -m dara_dt.experiments.cross_dependency_metrics
```

These commands are proposed until implementation is complete.

They should not be added to CI until the corresponding modules exist and
pass their tests.

---

# 47. Result Reporting Rules

Results must be reported:

```text
by policy
```

and:

```text
by dependency family.
```

Do not report aggregate performance alone.

A policy that performs well overall but fails completely on one dependency
must be described accordingly.

---

# 48. No Post-Hoc Rule Changes

After the experiment begins:

```text
validity rules
dependency definitions
condition labels
baseline rules
```

must not be changed merely because the results are unfavourable.

If a genuine design defect is discovered:

1. document the defect;
2. correct it;
3. rerun all affected conditions; and
4. record the methodological change.

---

# 49. Claim Boundaries

A successful EXP-007 may support:

> The DARA-DT mechanism demonstrated preliminary generalisation across the
> tested capacity, operational-status and location/availability dependency
> families under controlled conditions.

It would **not** support:

```text
DARA-DT works for all logistics decisions.

DARA-DT is universally generalisable.

DARA-DT is safer than existing runtime assurance.

DARA-DT novelty is confirmed.
```

---

# 50. Connection to Novelty Evaluation

EXP-007 addresses one of the major current novelty threats:

```text
Capacity-Specific Explanation
```

However, even successful generalisation will not answer the second major
threat:

```text
Runtime Contract / Assumption Equivalence
```

Including the contract baseline begins that comparison.

Further experiments may still be required.

---

# 51. Expected Research Progression

If EXP-007 supports cross-dependency generalisation:

```text
EXP-001
Pilot
        ↓
EXP-002
Controlled Policy Comparison
        ↓
EXP-003
Decision Relevance
        ↓
EXP-004
Divergence Severity
        ↓
EXP-005
Decision Impact
        ↓
EXP-006
Imperfect Evidence
        ↓
EXP-007
Cross-Dependency Generalisation
        ↓
NEXT
Stronger Comparator / Robust Assurance Study
```

---

# 52. Decision Gate After EXP-007

After results are available:

### If Generalisation Is Supported

Proceed to stronger comparative evaluation.

### If Generalisation Is Partial

Refine DARA-DT around the dependency classes for which the mechanism is
meaningful.

### If Generalisation Fails

Narrow or reject the broad framework interpretation.

Do not add complexity merely to rescue the original hypothesis.

---

# 53. Pre-Registration Summary

Before implementation, EXP-007 fixes the following:

```text
Primary variable:
Decision dependency type

Dependency families:
Capacity
Operational Status
Location / Availability

Evidence:
Reliable

Minimum conditions:
12

Primary policies:
No Assurance
Global Divergence
Decision Relevance
Decision Impact
Runtime Contract / Assumption

Ground truth:
Independent physical-state validation

Primary question:
Does the relevance → impact distinction generalise?

Primary competing explanation:
Simple runtime contracts are sufficient.

Primary falsification risk:
The mechanism works only for capacity.
```

---

# 54. Final Experimental Principle

EXP-007 is deliberately structured so that DARA-DT can fail.

That is essential.

The experiment should not ask:

> **How can we demonstrate that DARA-DT works?**

It should ask:

> **Under a controlled change in decision dependency, does the proposed
> divergence → relevance → impact mechanism continue to provide meaningful
> runtime-assurance information, and does explicit divergence reasoning add
> anything beyond simpler runtime condition checking?**

The answer will determine whether DARA-DT should continue as a general
framework, be narrowed to particular dependency classes, or be reformulated.
