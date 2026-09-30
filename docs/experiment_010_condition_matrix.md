# EXP-010 — Frozen Condition Matrix

**Experiment:** EXP-010 — Propagation-Aware Physical–Digital Divergence  
**Project:** DARA-DT  
**Status:** PRE-REGISTERED CONDITION MATRIX  
**Implementation Status:** Not Started  
**Primary Comparator:** Dependency-Aware Composed Runtime Contract  
**Conditions:** 30  
**Decision Chain:** D1 → D2 → D3  
**Novelty Status:** Not Established

---

# 1. Purpose

This document freezes the controlled condition matrix for EXP-010 before
implementation.

EXP-010 tests whether physical–digital divergence that originates upstream can
propagate through a multi-stage autonomous logistics decision chain and provide
runtime-assurance information beyond a strong dependency-aware composed
runtime contract.

The primary comparison is:

```text
Dependency-Aware Composed Runtime Contract
                    vs
Propagation-Aware DARA-DT
```

The experiment must permit:

```text
DARA-DT advantage
DARA-DT equivalence
DARA-DT disadvantage
```

No condition may be changed after results are observed merely to favour a
particular policy.

---

# 2. Core Decision Chain

EXP-010 uses three vehicles:

```text
Vehicle A
Vehicle B
Vehicle C
```

and three linked decision stages:

```text
D1
Primary assignment involving Vehicle A
        ↓
D2
Secondary assignment involving Vehicle B
        ↓
D3
Recovery / downstream allocation involving Vehicle C
```

The experiment evaluates whether an upstream physical–digital mismatch can
alter assumptions required by later decisions.

---

# 3. Canonical Initial Physical State

Unless a condition explicitly overrides a value:

```text
Vehicle A
---------
status      = operational
available   = true
capacity    = 10
location    = depot

Vehicle B
---------
status      = operational
available   = true
capacity    = 10
location    = depot

Vehicle C
---------
status      = operational
available   = true
capacity    = 10
location    = depot
role        = recovery_resource
```

---

# 4. Canonical Initial Digital Twin State

At the start of every condition:

```text
Twin Vehicle A = Physical Vehicle A

Twin Vehicle B = Physical Vehicle B

Twin Vehicle C = Physical Vehicle C
```

Divergence is introduced only through the frozen experimental event.

---

# 5. Orders

The controlled decision chain uses:

```text
Order O1
---------
demand = 5

Order O2
---------
demand = 5

Order O3
---------
demand = 5
```

These values remain fixed unless explicitly stated otherwise.

---

# 6. D1 — Primary Assignment

D1 is:

```text
Assign O1 → Vehicle A
```

Direct dependencies:

```text
vehicle_A.status

vehicle_A.available

vehicle_A.capacity

order_O1.demand
```

Local validity requires:

```text
vehicle_A.status == operational

vehicle_A.available == true

vehicle_A.capacity >= order_O1.demand
```

---

# 7. D2 — Secondary Assignment

D2 is:

```text
Assign O2 → Vehicle B
```

Direct local dependencies:

```text
vehicle_B.status

vehicle_B.available

vehicle_B.capacity

order_O2.demand
```

Local validity requires:

```text
vehicle_B.status == operational

vehicle_B.available == true

vehicle_B.capacity >= order_O2.demand
```

D2 additionally participates in the shared recovery dependency:

```text
recovery_resource_available
```

when the frozen condition requires recovery coverage.

---

# 8. D3 — Recovery / Downstream Decision

D3 concerns Vehicle C.

Conceptually:

```text
Reserve / allocate Vehicle C as recovery support
```

Dependencies may include:

```text
vehicle_C.status

vehicle_C.available

vehicle_C.capacity

recovery_demand

upstream_failure_state
```

The exact D3 operation must remain consistent across the implementation.

---

# 9. Shared Recovery Rule

The controlled system contains one designated recovery resource:

```text
Vehicle C
```

If Vehicle A physically fails after D1:

```text
Vehicle C
```

may become required for recovery.

This can change the resource assumptions supporting later decisions.

The experiment therefore distinguishes:

```text
Direct dependency

Shared dependency

Propagated dependency
```

---

# 10. Physical–Digital Divergence

For physical state:

\[
P_t
\]

and Digital Twin state:

\[
T_t
\]

a divergence exists when:

\[
P_t \neq T_t
\]

for a monitored state variable.

Examples include:

```text
Physical A.status = failed

Twin A.status = operational
```

or:

```text
Physical C.available = false

Twin C.available = true
```

---

# 11. Propagation Definition

A divergence is considered propagated when:

1. it originates in an upstream state;
2. it affects an assumption or resource produced or consumed by an earlier
   decision;
3. that changed assumption is required by a later decision.

Conceptually:

```text
Divergence δ
      ↓
D1 dependency
      ↓
Changed system/resource assumption
      ↓
D2 or D3 dependency
      ↓
Downstream validity
```

---

# 12. Non-Propagation Definition

An upstream divergence is non-propagating when:

```text
divergence exists
```

but:

```text
no dependency required by the pending downstream decision changes.
```

These conditions are essential for measuring propagation false alarms.

---

# 13. Evidence States

EXP-010 uses:

```text
AVAILABLE

STALE

MISSING

CONFLICTING
```

Definitions remain consistent with earlier experiments.

---

## AVAILABLE

Runtime evidence is present and usable.

---

## STALE

Runtime evidence exists but no longer satisfies the accepted freshness
requirement.

---

## MISSING

Required runtime evidence is unavailable.

---

## CONFLICTING

Two or more runtime observations disagree about the required state.

---

# 14. Evidence-Parity Rule

The primary comparator and DARA-DT must receive identical observable evidence.

For every condition:

```text
Evidence(P3) = Evidence(P4)
```

where:

```text
P3 = Dependency-Aware Composed Runtime Contract

P4 = Propagation-Aware DARA-DT
```

Physical ground truth is evaluator-only information.

---

# 15. Policy Set

The frozen policy set is:

```text
P0 — No Assurance

P1 — Local Runtime Contract

P2 — Global Divergence / Uncertainty

P3 — Dependency-Aware Composed Runtime Contract

P4 — Propagation-Aware DARA-DT
```

P3 is the principal comparator.

---

# 16. Condition Families

The matrix contains five experimental families:

```text
F0 — Synchronized Control

F1 — Direct Divergence

F2 — Upstream Non-Propagating Divergence

F3 — Upstream Propagating Divergence

F4 — Compound / Cross-Entity Propagation
```

There are:

```text
6 conditions per family
```

for:

```text
5 × 6 = 30 conditions
```

---

# 17. F0 — Synchronized Controls

These conditions establish normal behaviour without physical–digital
divergence.

| ID | Evidence | Physical Validity | Divergence | Expected Ground Truth |
|---|---|---:|---|---|
| F0-A | AVAILABLE | Valid | None | DO_NOT_INTERVENE |
| F0-B | AVAILABLE | Invalid | None | INTERVENE |
| F0-C | STALE | Valid | None | DO_NOT_INTERVENE |
| F0-D | MISSING | Valid | None | DO_NOT_INTERVENE |
| F0-E | CONFLICTING | Valid | None | DO_NOT_INTERVENE |
| F0-F | AVAILABLE | Valid | None | DO_NOT_INTERVENE |

F0-F provides a repeated deterministic control for reproducibility.

The invalid F0-B condition is caused by a genuine physical decision
constraint, not physical–digital divergence.

---

# 18. F1 — Direct Divergence

These conditions reproduce direct decision-relevant divergence.

The divergence directly affects the entity selected by the pending decision.

| ID | Origin | Evidence | Physical Validity | Expected Ground Truth |
|---|---|---|---:|---|
| F1-A | A.status | AVAILABLE | Invalid | INTERVENE |
| F1-B | A.capacity | AVAILABLE | Invalid | INTERVENE |
| F1-C | A.available | AVAILABLE | Invalid | INTERVENE |
| F1-D | A.status | STALE | Invalid | INTERVENE |
| F1-E | A.status | MISSING | Invalid | INTERVENE |
| F1-F | A.status | CONFLICTING | Invalid | INTERVENE |

Purpose:

```text
confirm continuity with earlier direct-divergence experiments
```

These conditions are not expected to establish EXP-010 differentiation.

---

# 19. F2 — Upstream Non-Propagating Divergence

An upstream divergence exists but does not affect the validity of the pending
downstream decision.

| ID | Origin | Pending Decision | Evidence | Downstream Validity | Ground Truth |
|---|---|---|---|---:|---|
| F2-A | A.location | D2/B | AVAILABLE | Valid | DO_NOT_INTERVENE |
| F2-B | A.capacity | D2/B | AVAILABLE | Valid | DO_NOT_INTERVENE |
| F2-C | A.status | D2/B | AVAILABLE | Valid | DO_NOT_INTERVENE |
| F2-D | A.location | D2/B | STALE | Valid | DO_NOT_INTERVENE |
| F2-E | A.location | D2/B | MISSING | Valid | DO_NOT_INTERVENE |
| F2-F | A.location | D2/B | CONFLICTING | Valid | DO_NOT_INTERVENE |

These conditions test whether assurance mechanisms overreact merely because an
upstream divergence exists.

A propagation-aware mechanism should reject propagation where no dependency
path exists.

---

# 20. F3 — Upstream Propagating Divergence

These are the primary EXP-010 conditions.

The divergence originates upstream and affects a dependency required by a
downstream decision.

| ID | Origin | Propagated Dependency | Evidence | Downstream Validity | Ground Truth |
|---|---|---|---|---:|---|
| F3-A | A.status | recovery_resource_available | AVAILABLE | Invalid | INTERVENE |
| F3-B | A.available | recovery_resource_available | AVAILABLE | Invalid | INTERVENE |
| F3-C | A.location | recovery_timing_valid | AVAILABLE | Invalid | INTERVENE |
| F3-D | A.status | recovery_resource_available | STALE | Invalid | INTERVENE |
| F3-E | A.status | recovery_resource_available | MISSING | Invalid | INTERVENE |
| F3-F | A.status | recovery_resource_available | CONFLICTING | Invalid | INTERVENE |

Canonical F3 propagation:

```text
Physical A fails
        ↓
Twin A still operational
        ↓
D1 planning state remains incorrect
        ↓
Vehicle C becomes physically required for recovery
        ↓
Twin/shared planning state still assumes C available
        ↓
D2 is generated under invalid recovery assumption
        ↓
Downstream decision requires intervention
```

---

# 21. F4 — Compound / Cross-Entity Propagation

These conditions test interactions involving more than one dependency.

| ID | Divergence Origin | Compound Dependency | Evidence | Downstream Validity | Ground Truth |
|---|---|---|---|---:|---|
| F4-A | A.status | C.available + B.assignment | AVAILABLE | Invalid | INTERVENE |
| F4-B | A.status | C.capacity + recovery_demand | AVAILABLE | Invalid | INTERVENE |
| F4-C | A.location | recovery_timing + B.deadline | AVAILABLE | Invalid | INTERVENE |
| F4-D | A.status | C.available + B.assignment | STALE | Invalid | INTERVENE |
| F4-E | A.status | C.available + B.assignment | MISSING | Invalid | INTERVENE |
| F4-F | A.status | C.available + B.assignment | CONFLICTING | Invalid | INTERVENE |

The important requirement is:

```text
the downstream decision cannot be classified solely from
Vehicle B's direct local state.
```

---

# 22. Matrix Balance

Total:

```text
30 conditions
```

Family balance:

```text
F0 = 6
F1 = 6
F2 = 6
F3 = 6
F4 = 6
```

---

# 23. Validity Balance

Frozen expected labels:

```text
F0:
5 valid
1 invalid

F1:
0 valid
6 invalid

F2:
6 valid
0 invalid

F3:
0 valid
6 invalid

F4:
0 valid
6 invalid
```

Total:

```text
Valid / DO_NOT_INTERVENE = 11

Invalid / INTERVENE      = 19
```

The matrix is not artificially balanced 50/50.

The distribution follows the research distinctions being tested.

Metrics must therefore not rely on accuracy alone.

---

# 24. Evidence Distribution

AVAILABLE conditions:

```text
F0 = 3
F1 = 3
F2 = 3
F3 = 3
F4 = 3
```

Total:

```text
15 AVAILABLE
```

Imperfect evidence:

```text
STALE       = 5

MISSING     = 5

CONFLICTING = 5
```

Total:

```text
15 imperfect-evidence conditions
```

Overall:

```text
30 conditions
```

---

# 25. Ground-Truth Rule

For every pending decision:

```text
INTERVENE
```

if execution violates at least one frozen physical operational requirement.

Otherwise:

```text
DO_NOT_INTERVENE
```

The ground-truth evaluator may use physical state.

Assurance policies may not.

---

# 26. Local Contract Knowledge

P1 knows only direct dependencies of the pending decision.

For D2:

```text
B.status

B.available

B.capacity

O2.demand
```

P1 does not receive:

```text
upstream decision dependency structure

propagation path

divergence origin
```

This limitation is intentional because P1 represents the local-contract
baseline.

---

# 27. Global Policy Knowledge

P2 can observe that:

```text
a divergence or evidence problem exists
```

but does not determine whether it affects the pending decision.

This policy is expected to demonstrate possible global conservatism.

---

# 28. Composed Contract Knowledge

P3 receives all pre-registered dependencies necessary to evaluate the pending
decision.

For example:

```text
B.status

B.available

B.capacity

O2.demand

C.available

recovery_resource_required

upstream_assignment_assumptions
```

P3 may evaluate composed logical conditions.

Example:

```text
B.status == operational

AND

B.available == true

AND

B.capacity >= O2.demand

AND

(
    recovery_resource_required == false

    OR

    C.available == true
)
```

P3 must not be intentionally weakened.

---

# 29. DARA-DT Knowledge

P4 receives the same observable runtime evidence as P3.

P4 additionally represents the reasoning structure:

```text
divergence origin
        ↓
affected dependency
        ↓
decision relationship
        ↓
propagation relationship
        ↓
downstream impact
```

The research question is whether this explicit representation changes
assurance performance relative to P3.

---

# 30. Critical Fairness Rule

If P4 uses a dependency such as:

```text
recovery_resource_required
```

then P3 must be allowed to represent that dependency too.

If P4 uses:

```text
C.available
```

P3 must receive the same observable evidence about:

```text
C.available
```

If P4 knows:

```text
D2 depends on recovery coverage
```

P3 must be permitted to encode the corresponding composed requirement.

Otherwise the comparison is invalid.

---

# 31. Divergence-Specific Ablation

A required ablation removes divergence-origin information while retaining
dependency knowledge.

Compare:

```text
P3
Dependency-Aware Composed Contract
```

against:

```text
P4
Propagation-Aware DARA-DT
```

The experiment asks whether explicit divergence origin and propagation adds
anything beyond dependency knowledge.

---

# 32. Expected Local-Contract Challenge

F3 and F4 deliberately contain cases where:

```text
B.status      = operational

B.available   = true

B.capacity    >= O2.demand
```

but the downstream decision is physically invalid because a shared or
upstream dependency has changed.

Therefore:

```text
P1 may ALLOW
```

while ground truth requires:

```text
INTERVENE
```

This demonstrates the limitation of local-only checking.

It does not demonstrate DARA-DT superiority over P3.

---

# 33. Expected Global-Policy Challenge

F2 deliberately contains upstream divergence that does not affect the pending
decision.

Therefore a global policy may:

```text
INTERVENE
```

while ground truth requires:

```text
DO_NOT_INTERVENE
```

This demonstrates potential over-conservatism.

It does not establish DARA-DT novelty.

---

# 34. Strongest Test

The strongest conditions are F3 and F4.

The central comparison is:

```text
P3 vs P4
```

If both correctly intervene:

```text
contract equivalence persists.
```

If P4 intervenes correctly and P3 incorrectly allows:

the exact reason must be isolated.

The first question must then be:

> Could the missing information be represented fairly as an additional
> dependency in P3?

If yes:

```text
P3 must be strengthened before making a differentiation claim.
```

---

# 35. Primary Metrics

For every policy calculate:

```text
N

TI

FI

MI

CNI

Accuracy

Precision

Recall

False-Intervention Rate

Missed-Intervention Rate

Autonomy Availability
```

---

# 36. Propagation Metrics

Calculate:

```text
Propagation Detection Rate
```

defined as:

```text
correctly detected propagating invalid conditions
/
all propagating invalid conditions
```

---

Calculate:

```text
Propagation False-Alarm Rate
```

defined as:

```text
non-propagating valid conditions incorrectly treated as propagated
/
all non-propagating valid conditions
```

---

Calculate:

```text
Downstream Invalidity Detection Rate
```

for F3 and F4.

---

# 37. Family-Level Metrics

Report metrics separately for:

```text
F0

F1

F2

F3

F4
```

Do not report only aggregate performance.

This is required because aggregate results can hide the exact mechanism being
tested.

---

# 38. Evidence-Level Metrics

Report separately for:

```text
AVAILABLE

STALE

MISSING

CONFLICTING
```

This tests whether any apparent propagation advantage depends on a particular
evidence state.

---

# 39. Authority Distribution

Record for every policy:

```text
ALLOW

RESTRICT

DEFER

FALLBACK
```

Binary intervention metrics remain primary.

Authority semantics remain secondary unless operational consequences are
explicitly evaluated.

---

# 40. Kill Test A — Composed Contract Equivalence

Triggered if:

```text
P3 and P4
```

produce equivalent primary assurance outcomes across the frozen propagation
matrix.

Interpretation:

```text
DARA-DT differentiation not established.
```

---

# 41. Kill Test B — Local Contract Strawman

Triggered if:

```text
P4 > P1
```

but:

```text
P4 = P3
```

on the relevant assurance trade-off.

Interpretation:

```text
DARA-DT advantage exists only against an under-specified local baseline.
```

---

# 42. Kill Test C — No Divergence-Specific Value

Triggered if removing explicit divergence-origin information does not alter
relevant outcomes.

Interpretation:

```text
dependency reasoning, rather than divergence reasoning,
explains the result.
```

---

# 43. Kill Test D — No Propagation Requirement

Triggered if all F3/F4 invalid decisions can be identified entirely from the
pending decision's direct current state.

Interpretation:

```text
propagation is unnecessary.
```

---

# 44. Kill Test E — Evidence Privilege

Triggered if:

```text
Evidence(P4) != Evidence(P3)
```

in a way that advantages P4.

Interpretation:

```text
comparative result invalid.
```

---

# 45. Kill Test F — Hard-Coded Advantage

Triggered if P4 receives manually encoded relationships that are denied to P3
despite representing known decision dependencies.

Interpretation:

```text
framework-level differentiation invalid.
```

---

# 46. Kill Test G — Safety Degradation

Triggered if P4 gains autonomy relative to P3 only through increased:

```text
Missed Interventions
```

Interpretation:

```text
autonomy advantage is not an assurance improvement.
```

---

# 47. Kill Test H — Global Conservatism Only

Triggered if P4 improves over P2 but remains equivalent to P3.

Interpretation:

```text
decision-sensitive assurance supported

DARA-DT-specific differentiation not supported
```

---

# 48. Kill Test I — Propagation Overreach

Triggered if P4 unnecessarily intervenes in F2 conditions.

Interpretation:

```text
DARA-DT incorrectly propagates irrelevant divergence.
```

---

# 49. Kill Test J — Compound Collapse

Triggered if F4 provides no additional assurance challenge beyond independent
evaluation of its constituent dependencies.

Interpretation:

```text
compound propagation does not establish additional differentiation.
```

---

# 50. Frozen Comparator Hierarchy

The experiment must interpret comparator results in this order:

```text
No Assurance
        ↓
Local Contract
        ↓
Global Divergence
        ↓
Dependency-Aware Composed Contract
        ↓
Propagation-Aware DARA-DT
```

The existence of this hierarchy does not imply expected performance ordering.

---

# 51. Result Interpretation

## Outcome A

```text
P4 > P3
```

Do not immediately claim novelty.

First isolate the mechanism causing the difference.

Then strengthen P3 if the missing information can reasonably be represented as
a contract dependency.

---

## Outcome B

```text
P4 = P3
```

Conclusion:

> Runtime-contract equivalence persists under the frozen multi-stage
> propagation matrix.

This is a valid negative result.

---

## Outcome C

```text
P4 < P3
```

Conclusion:

> Propagation-aware DARA-DT performs worse than the composed contract on the
> affected metric within the frozen matrix.

Retain the result.

---

# 52. Prohibited Changes After Freeze

After this document is committed:

```text
Do not change ground truth because of results.

Do not add a scenario because DARA-DT lost.

Do not remove a scenario because P3 won.

Do not weaken P3.

Do not give P4 additional physical evidence.

Do not change evidence status after observing outcomes.

Do not change a propagation path retrospectively.

Do not redefine a tie as superiority.
```

Any subsequent conditions must be labelled:

```text
EXPLORATORY
```

---

# 53. Implementation Test Requirements

Before running the full experiment, tests must verify:

```text
exactly 30 conditions exist

exactly 6 conditions per family

ground-truth counts are correct

evidence distribution is correct

P3 and P4 receive evidence parity

physical ground truth is evaluator-only

F2 conditions contain no downstream propagation

F3 conditions contain a valid propagation path

F4 conditions contain compound/cross-entity dependencies

local contract contains only direct dependencies

composed contract contains all frozen known dependencies
```

---

# 54. Frozen Counts

The implementation must reproduce:

```text
Total conditions:
30

Families:
5

Conditions per family:
6

DO_NOT_INTERVENE:
11

INTERVENE:
19

AVAILABLE:
15

STALE:
5

MISSING:
5

CONFLICTING:
5
```

Any mismatch must fail the experiment validation before policy results are
accepted.

---

# 55. Expected Scientific Interpretation

EXP-010 is not designed around an expected DARA-DT victory.

The strongest possible scientific outcomes include:

```text
DARA-DT adds information beyond composed contracts
```

or:

```text
composed contracts fully reproduce DARA-DT behaviour
```

or:

```text
DARA-DT introduces unnecessary intervention
```

Each outcome refines the research question.

---

# 56. Contribution Boundary

Even if P4 outperforms P3, EXP-010 alone does not establish novelty.

The result would support:

```text
experimental differentiation
```

which must still survive:

```text
mechanism ablation

strong comparator refinement

prior-work comparison
```

before becoming a contribution claim.

---

# 57. Final Frozen Research Question

> **Does propagation-aware physical–digital divergence provide additional
> runtime-assurance information beyond a dependency-aware composed runtime
> contract when an upstream physical–digital mismatch propagates through a
> multi-stage autonomous logistics decision chain?**

---

# 58. Final Matrix Position

```text
EXP-010 CONDITIONS
        =
30

IMPLEMENTATION
        =
NOT STARTED

RESULTS
        =
UNKNOWN

DARA-DT ADVANTAGE
        =
NOT ASSUMED

RUNTIME-CONTRACT EQUIVALENCE
        =
MUST REMAIN POSSIBLE

DARA-DT NOVELTY
        =
NOT ESTABLISHED
```

---

# 59. Next Gate

After this matrix is committed:

```text
EXP-010 Pre-Registration
        ✓
        ↓
EXP-010 Condition Matrix
        ✓
        ↓
Implementation Design Audit
        ↓
Implement Condition Model
        ↓
Validate 30 Conditions
        ↓
Implement Strong Composed Contract
        ↓
Implement Propagation Mechanism
        ↓
Run Unit Tests
        ↓
Run EXP-010
        ↓
Evaluate Kill Tests
        ↓
Accept Result
```

No EXP-010 result should be generated before the frozen condition model and
comparator-fairness tests pass.
