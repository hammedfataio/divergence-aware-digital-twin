# EXP-010 — Propagation-Aware Physical–Digital Divergence

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-010  
**Stage:** Pre-Registration  
**Status:** DESIGN FROZEN BEFORE IMPLEMENTATION  
**Domain:** Multi-Stage Autonomous Logistics  
**Primary Threat:** Dependency-Aware Composed Runtime Contract  
**Previous Evidence:** EXP-001 to EXP-009  
**Novelty Status:** Not Established

---

# 1. Purpose

EXP-010 is designed to test the strongest unresolved differentiation question
remaining after EXP-007, EXP-008 and EXP-009.

Those experiments repeatedly demonstrated that a strong runtime-contract
mechanism can reproduce the primary binary assurance behaviour of DARA-DT for
the decision structures tested so far.

Therefore EXP-010 does not ask whether DARA-DT can outperform:

- no assurance;
- global divergence monitoring;
- global uncertainty monitoring;
- a simple local threshold;
- a single-variable runtime contract.

Those comparisons are no longer sufficient.

EXP-010 instead asks whether explicit reasoning about the **origin and
propagation of physical–digital divergence through a multi-stage autonomous
decision chain** provides assurance information beyond a strong
dependency-aware composed runtime contract.

The experiment is explicitly falsification-oriented.

Possible outcomes are:

```text
DARA-DT advantage
DARA-DT equivalence
DARA-DT disadvantage
```

All three outcomes are scientifically acceptable.

---

# 2. Background

The experimental progression leading to EXP-010 is:

```text
EXP-001
Decision relevance appears useful
        ↓
EXP-002
Controlled policy comparison
        ↓
EXP-003
Decision relevance formalised
        ↓
EXP-004
Relevance ≠ decision invalidity
        ↓
EXP-005
Decision impact improves selectivity
        ↓
EXP-006
Runtime evidence can be imperfect
        ↓
EXP-007
Runtime contract matches impact reasoning
        ↓
EXP-008
Contract equivalence survives imperfect evidence
        ↓
EXP-009
Contract equivalence survives
decision-relevant uncertainty
        ↓
EXP-010
Does equivalence survive divergence propagation
through a multi-stage decision chain?
```

EXP-010 must therefore introduce a genuinely different research challenge.

It must not simply increase the number of EXP-009 conditions.

---

# 3. Primary Research Question

> **Does propagation-aware physical–digital divergence provide additional
> runtime-assurance information beyond a dependency-aware composed runtime
> contract when an upstream physical–digital mismatch propagates through a
> multi-stage autonomous logistics decision chain?**

---

# 4. Supporting Research Questions

## RQ10.1 — Propagation

Can an upstream physical–digital divergence change the validity of a
downstream autonomous decision even when the downstream entity itself has no
direct physical–digital mismatch?

---

## RQ10.2 — Local Contracts

Can independently evaluated local runtime contracts fail to detect downstream
decision invalidation caused by an upstream divergence?

---

## RQ10.3 — Composed Contracts

Can a dependency-aware composed runtime contract recover the downstream
assurance information obtained by propagation-aware DARA-DT?

---

## RQ10.4 — Divergence-Specific Information

Does explicitly representing:

```text
physical state
        vs
Digital Twin state
```

and tracing the origin of mismatch provide assurance information that cannot
be reproduced from ordinary dependency/constraint evaluation?

---

## RQ10.5 — Authority

Do propagated divergence conditions justify different runtime authority
responses such as:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
```

rather than a single binary intervention?

Authority-state interpretation is secondary to the primary binary
differentiation test.

---

# 5. Primary Hypothesis

The experimental hypothesis is:

> **H1:** Under at least some multi-stage logistics conditions, an upstream
> physical–digital divergence will propagate through decision dependencies and
> alter the validity of a downstream decision in a way that is not detected by
> an independently evaluated local runtime contract.

This hypothesis does **not** establish superiority over a dependency-aware
composed runtime contract.

---

# 6. Strong Differentiation Hypothesis

The stronger hypothesis is:

> **H2:** Propagation-aware DARA-DT will identify at least one
> decision-relevant downstream invalidation that cannot be represented
> equivalently by the pre-registered dependency-aware composed runtime
> contract operating on the same observable evidence.

This is the principal novelty hypothesis.

If H2 fails, the contribution must narrow.

---

# 7. Null Hypothesis

> **H0:** Once the relevant cross-decision and cross-entity dependencies are
> represented explicitly, a dependency-aware composed runtime contract
> reproduces the assurance behaviour of propagation-aware DARA-DT.

This is a scientifically acceptable result.

EXP-007 through EXP-009 make H0 particularly important.

---

# 8. Experimental Principle

EXP-010 separates:

```text
Physical Reality
        ↓
Observable Runtime Evidence
        ↓
Digital Twin Representation
        ↓
Decision Dependencies
        ↓
Decision Chain
        ↓
Runtime Assurance
        ↓
Authority
```

Physical ground truth is available only to the evaluator.

No assurance policy may receive privileged access to evaluator-only physical
truth.

---

# 9. Core Scenario

The experiment uses a multi-stage logistics scenario involving three vehicles:

```text
Vehicle A
Vehicle B
Vehicle C
```

and two or more linked autonomous decisions.

The initial Twin state is consistent with the expected operational state.

Example:

```text
Vehicle A:
operational
available
assigned to primary delivery

Vehicle B:
operational
available
assigned to secondary delivery

Vehicle C:
operational
available
reserved as recovery resource
```

The physical system then experiences an event involving Vehicle A.

Example:

```text
Vehicle A physically breaks down.
```

The corresponding Digital Twin update is delayed, stale, missing or
conflicting.

Therefore:

```text
Physical Vehicle A
        =
failed

Digital Twin Vehicle A
        =
operational
```

This creates the upstream physical–digital divergence.

---

# 10. Decision Chain

The minimum decision chain is:

```text
D1
Primary assignment involving Vehicle A
        ↓
Expected fleet state changes
        ↓
D2
Secondary assignment involving Vehicle B
        ↓
Recovery/resource assumptions
        ↓
D3
Recovery or downstream allocation involving Vehicle C
```

Not every experimental condition must require all three decisions.

However, at least one downstream decision must depend on a state relationship
affected by an earlier decision or upstream divergence.

---

# 11. Key Experimental Requirement

A downstream decision must not be labelled invalid merely because an upstream
divergence exists.

The experiment must establish an explicit dependency path:

```text
Upstream Divergence
        ↓
Affected State / Assumption
        ↓
Decision Dependency
        ↓
Downstream Consequence
```

Without this path, the divergence is irrelevant to the downstream decision.

---

# 12. Example Propagation Chain

Example:

```text
Vehicle A physically fails
        ↓
Twin still reports A operational
        ↓
D1 assigns Order 1 to A
        ↓
Twin planning state assumes
Order 1 is covered
        ↓
Vehicle C remains reserved
for recovery capacity
        ↓
D2 assigns Order 2 to B
        ↓
D2 depends on C remaining
available as recovery support
        ↓
Physical recovery demand from A
consumes C
        ↓
D2's recovery assumption
becomes false
```

The important feature is that:

```text
Vehicle B itself may remain:

operational
available
sufficient capacity
```

Therefore a purely local contract for B may continue to pass.

---

# 13. Local Decision Contract

The local runtime contract evaluates only immediate properties of the selected
entity.

Example for D2:

```text
vehicle_B.status == operational

vehicle_B.available == true

vehicle_B.capacity >= order_2.demand
```

If all are true:

```text
LOCAL CONTRACT = PASS
```

This policy deliberately represents the limited local-contract baseline.

It is not the strongest comparator.

---

# 14. Dependency-Aware Composed Runtime Contract

The strong comparator must represent dependencies extending beyond the
selected entity.

For D2, the contract may include:

```text
vehicle_B.status == operational

vehicle_B.available == true

vehicle_B.capacity >= order_2.demand

recovery_resource_available == true

required_handover_resource_available == true

upstream_assignment_assumptions_valid == true
```

The exact conditions must be frozen before implementation.

The composed contract may use:

- cross-entity dependencies;
- shared state;
- upstream decision assumptions;
- resource dependencies;
- preconditions inherited from earlier decisions.

The comparator must be implemented strongly enough that it represents a
credible alternative to DARA-DT.

---

# 15. DARA-DT Propagation-Aware Mechanism

The EXP-010 DARA-DT mechanism will represent:

```text
Detected Physical–Digital Divergence
        ↓
Divergence Origin
        ↓
Affected State Dependency
        ↓
Affected Decision
        ↓
Derived / Downstream Dependency
        ↓
Downstream Decision Impact
        ↓
Runtime Authority
```

Conceptually:

\[
\delta_t = P_t - T_t
\]

where:

- \(P_t\) represents relevant physical state;
- \(T_t\) represents Digital Twin state.

For decision \(d_i\):

\[
Dep(d_i)
\]

represents its direct dependencies.

For a linked decision chain:

\[
d_1 \rightarrow d_2 \rightarrow ... \rightarrow d_n
\]

the experiment introduces a propagation relation:

\[
Prop(\delta_t,d_i,d_j)
\]

representing whether divergence affecting decision \(d_i\) changes a state,
assumption or dependency required by downstream decision \(d_j\).

The downstream divergence-relevance set is provisionally:

\[
D^{prop}_{t}(d_j)
=
\{
\delta :
\exists d_i,\;
Prop(\delta,d_i,d_j)
\}
\]

This notation is experimental.

It is not claimed as a novel formalism.

---

# 16. Divergence Origin

Every propagation condition must record the origin of divergence.

Candidate origins include:

```text
vehicle operational status

vehicle availability

vehicle location

resource consumption

handover completion

recovery-resource availability
```

EXP-010 should begin with a bounded subset.

The experiment should not attempt to model every logistics failure type.

---

# 17. Propagation Types

The frozen condition matrix should include at least the following conceptual
classes.

## P0 — No Divergence

```text
Physical State = Twin State
```

Control condition.

---

## P1 — Direct Relevant Divergence

The downstream decision directly depends on the diverged state.

This provides continuity with previous experiments.

---

## P2 — Upstream Divergence, No Downstream Effect

An upstream mismatch exists but does not alter any dependency required by the
downstream decision.

This tests unnecessary propagation.

---

## P3 — Upstream Divergence, Downstream Effect

An upstream mismatch changes a state or assumption required by the downstream
decision.

This is the primary propagation condition.

---

## P4 — Cross-Entity Propagation

The divergence originates on one entity but affects a decision involving
another entity.

Example:

```text
Divergence origin:
Vehicle A

Pending decision:
Vehicle B

Affected dependency:
Recovery Vehicle C availability
```

---

## P5 — Compound Propagation

Two or more dependencies jointly determine downstream validity.

Example:

```text
Recovery resource unavailable
AND
handover resource unavailable
```

The downstream decision becomes invalid only under the compound condition.

---

# 18. Evidence Conditions

The first EXP-010 matrix should avoid unnecessary combinatorial explosion.

Evidence conditions should initially be limited to:

```text
AVAILABLE
STALE
MISSING
CONFLICTING
```

However, the matrix does not need to cross every propagation condition with
every evidence state.

Conditions must be selected because they test a research distinction.

They must not be selected simply to increase sample size.

---

# 19. Ground Truth

Ground truth answers:

```text
Should autonomous execution of the downstream decision be allowed?
```

Ground truth must be computed from the physical state and frozen operational
constraints.

Possible labels remain:

```text
INTERVENE
DO_NOT_INTERVENE
```

Physical ground truth must not be supplied to the assurance policies.

---

# 20. Assurance Policies

EXP-010 should include at least:

```text
P0 — No Assurance

P1 — Local Runtime Contract

P2 — Global Divergence / Uncertainty

P3 — Dependency-Aware Composed Runtime Contract

P4 — Propagation-Aware DARA-DT
```

Optional additional comparators should be added only if they test a specific
alternative explanation.

---

# 21. P0 — No Assurance

Behaviour:

```text
ALLOW
```

for every proposed decision.

Purpose:

Establish the unsafe-autonomy baseline.

---

# 22. P1 — Local Runtime Contract

Evaluates only direct local dependencies of the pending decision.

Example:

```text
vehicle_B.status
vehicle_B.available
vehicle_B.capacity
```

Purpose:

Test whether upstream divergence can create downstream invalidity invisible to
local checking.

This is a necessary baseline but not the principal novelty comparator.

---

# 23. P2 — Global Divergence / Uncertainty

Intervenes when relevant global Twin/evidence problems are detected without
decision-specific dependency reasoning.

Purpose:

Measure unnecessary conservatism.

This continues the global-baseline logic from earlier experiments.

---

# 24. P3 — Dependency-Aware Composed Runtime Contract

This is the strongest comparator.

It receives the same observable evidence available to DARA-DT.

It can evaluate:

```text
direct dependencies

cross-entity dependencies

shared resources

upstream assumptions

composed preconditions
```

It must not receive physical ground truth.

If this mechanism reproduces DARA-DT's relevant behaviour:

```text
the EXP-010 differentiation claim fails.
```

---

# 25. P4 — Propagation-Aware DARA-DT

DARA-DT evaluates:

```text
divergence origin

physical–digital mismatch evidence

decision dependency

propagation path

downstream decision impact

evidence quality

authority response
```

DARA-DT must not be given additional observations unavailable to P3.

Its difference must arise from reasoning structure, not evidence privilege.

---

# 26. Evidence-Parity Requirement

For every condition:

```text
Observable evidence(P3)
        =
Observable evidence(P4)
```

Physical ground truth:

```text
Evaluator only
```

This is mandatory.

Any condition violating evidence parity must be excluded from comparative
claims.

---

# 27. Primary Outcome Categories

The established categories remain:

```text
TRUE_INTERVENTION

FALSE_INTERVENTION

MISSED_INTERVENTION

CORRECT_NON_INTERVENTION
```

These support comparison with EXP-001 through EXP-009.

---

# 28. Primary Metrics

For every policy:

```text
N

True Interventions

False Interventions

Missed Interventions

Correct Non-Interventions

Accuracy

Precision

Recall

False-Intervention Rate

Missed-Intervention Rate

Autonomy Availability
```

---

# 29. Propagation-Specific Metrics

EXP-010 should additionally measure:

```text
Propagation Detection Rate

Downstream Invalidity Detection Rate

Irrelevant Propagation Rejection Rate

Propagation False-Alarm Rate

Propagation Miss Rate
```

Definitions must be frozen before implementation.

---

# 30. Decision-Chain Metrics

Where appropriate:

```text
Upstream decision outcome

Downstream decision outcome

Number of affected downstream decisions

Propagation depth

Intervention stage

Time / step to intervention
```

The first implementation may use discrete decision stages rather than
continuous time.

---

# 31. Authority Metrics

Record:

```text
ALLOW count

RESTRICT count

DEFER count

FALLBACK count
```

Do not automatically infer superiority from different authority distributions.

Operational consequences must be evaluated separately.

---

# 32. Logistics Metrics

If EXP-010 executes the decisions within the simulator, record:

```text
orders served

orders delayed

failed assignments

recovery-resource utilisation

service rate

decision latency

operational cost
```

These metrics are secondary to the assurance differentiation question.

---

# 33. Primary Success Criterion

EXP-010 does **not** succeed merely because DARA-DT outperforms:

```text
No Assurance

Local Contract

Global Divergence
```

The primary differentiation test is:

```text
DARA-DT
        vs
Dependency-Aware Composed Runtime Contract
```

A meaningful DARA-DT differentiation requires at least one pre-registered
condition where:

1. the policies receive equivalent observable evidence;
2. the composed contract represents all pre-registered known dependencies;
3. DARA-DT correctly identifies downstream invalidation or non-invalidation;
4. the composed contract produces a different incorrect assurance result;
5. the difference can be attributed specifically to divergence-origin or
   propagation reasoning.

Without all five:

```text
strong DARA-DT differentiation is not established.
```

---

# 34. Equivalence Criterion

If:

```text
P3 and P4
```

produce the same:

```text
TI
FI
MI
CNI
Autonomy Availability
```

across the frozen matrix:

```text
Runtime-Contract Equivalence Persists
```

This is a valid experimental result.

---

# 35. DARA-DT Disadvantage Criterion

If P3 produces:

```text
fewer missed interventions
```

or:

```text
fewer false interventions
```

than P4 under evidence parity:

```text
DARA-DT is inferior in that experimental dimension.
```

This result must be retained.

---

# Part IXX — Kill Tests

## 36. Kill Test A — Composed Contract Equivalence

### Trigger

P3 reproduces P4's primary assurance outcomes across the frozen matrix.

### Interpretation

```text
DARA-DT differentiation not established.
```

This is the principal kill test.

---

# 37. Kill Test B — Local Contract Strawman

### Trigger

DARA-DT outperforms P1 but does not outperform or differentiate from P3.

### Interpretation

The apparent advantage results from comparing against an under-specified
local contract.

No strong novelty claim is permitted.

---

# 38. Kill Test C — No Divergence-Specific Value

### Trigger

Removing explicit physical–digital divergence origin from P4 does not change
its relevant assurance outcomes.

### Interpretation

The divergence component has not demonstrated additional value.

---

# 39. Kill Test D — No Propagation Requirement

### Trigger

All downstream invalidations can be detected using only the downstream
decision's current observable state and direct dependencies.

### Interpretation

Propagation reasoning is unnecessary for the frozen matrix.

---

# 40. Kill Test E — Evidence Privilege

### Trigger

P4 receives information unavailable to P3.

### Interpretation

Comparative results are invalid.

The affected conditions cannot support differentiation claims.

---

# 41. Kill Test F — Hard-Coded Scenario Advantage

### Trigger

DARA-DT succeeds only because propagation relationships are manually encoded
specifically for the expected experimental failures while P3 is denied
equivalent dependency knowledge.

### Interpretation

Framework-level claims are rejected.

---

# 42. Kill Test G — Safety Degradation

### Trigger

P4 obtains greater autonomy than P3 only by increasing missed required
interventions.

### Interpretation

The autonomy advantage is not an assurance improvement.

---

# 43. Kill Test H — Global Conservatism Only

### Trigger

P4's only demonstrated advantage is over P2 global divergence/uncertainty,
while P3 matches P4.

### Interpretation

The experiment supports decision-sensitive assurance but not a DARA-DT-specific
contribution.

---

# 44. Kill Test I — Propagation Overreach

### Trigger

P4 unnecessarily intervenes when an upstream divergence exists but the
downstream decision is physically unaffected.

### Interpretation

The propagation mechanism is insufficiently selective.

---

# 45. Kill Test J — Compound-Dependency Collapse

### Trigger

Compound conditions add no assurance distinction beyond independently checking
their constituent contracts.

### Interpretation

Compound dependency reasoning does not support differentiation in the tested
matrix.

---

# 46. Required Ablations

At minimum, compare:

```text
Local Dependency Only

Composed Dependency

Composed Dependency + Evidence Quality

Divergence Origin + Local Dependency

Full Propagation-Aware DARA-DT
```

The purpose is to determine which mechanism actually produces any observed
difference.

---

# 47. No Retrospective Redesign Rule

After the condition matrix is frozen:

```text
Do not add a condition because DARA-DT lost.

Do not remove a condition because DARA-DT failed.

Do not change a threshold because the comparator won.

Do not redefine ground truth after observing outcomes.

Do not change comparator knowledge asymmetrically.

Do not reinterpret a tie as superiority.
```

Any post-hoc exploratory experiment must be labelled:

```text
EXPLORATORY
```

and separated from EXP-010 confirmatory results.

---

# 48. Implementation Boundary

EXP-010 should initially remain deliberately bounded.

Do not add:

```text
LLMs

blockchain

multi-agent orchestration

complex cybersecurity

distributed infrastructure

production streaming systems
```

unless the research question requires them.

The experiment concerns assurance reasoning, not infrastructure complexity.

---

# 49. Simulator Requirement

The experiment should extend the existing logistics simulator rather than
replace it.

Required capabilities include:

```text
multiple vehicles

linked decisions

shared resources

physical state

Digital Twin state

divergence injection

decision dependency representation

decision-chain representation

runtime evidence

assurance policies

physical ground-truth evaluation
```

---

# 50. Reproducibility Requirement

Every condition must have:

```text
Condition ID

Initial physical state

Initial Twin state

Injected event

Evidence state

Divergence origin

Affected dependencies

Decision chain

Expected physical consequence

Ground-truth intervention label
```

The matrix must be machine-readable.

---

# 51. Proposed Condition Naming

Use:

```text
<PROPAGATION>-<EVIDENCE>-<VALIDITY>
```

Examples:

```text
DIRECT-AVAILABLE-INVALID

UPSTREAM-NONE-VALID

UPSTREAM-PROP-AVAILABLE-INVALID

CROSS-ENTITY-STALE-INVALID

COMPOUND-CONFLICTING-INVALID
```

The exact naming scheme will be frozen in the separate condition-matrix
document.

---

# 52. Planned Repository Artifacts

EXP-010 should eventually create:

```text
docs/
    experiment_010_divergence_propagation.md
    experiment_010_condition_matrix.md

src/dara_dt/
    propagation/
        model.py
        analyser.py

    assurance/
        composed_contract_policy.py
        propagation_policy.py

    experiments/
        divergence_propagation_conditions.py
        divergence_propagation_experiment.py
        divergence_propagation_metrics.py

tests/
    test_divergence_propagation_conditions.py
    test_propagation_analyser.py
    test_composed_contract_policy.py
    test_divergence_propagation_experiment.py
    test_divergence_propagation_metrics.py
```

These paths are provisional until implementation begins.

No source file should be created merely because it appears in this design.

---

# 53. Pre-Implementation Gates

Before coding, the following must be completed:

```text
[x] EXP-007 results incorporated into novelty assessment

[x] EXP-008 results incorporated into novelty assessment

[x] EXP-009 results incorporated into novelty assessment

[x] Runtime-contract equivalence acknowledged

[x] Closest-prior-work audit updated

[x] Dependency-aware assurance threat acknowledged

[x] Propagation hypothesis defined

[x] Strong comparator identified

[x] Evidence-parity rule defined

[x] Kill tests defined

[ ] Exact decision chain frozen

[ ] Exact physical states frozen

[ ] Exact Twin states frozen

[ ] Exact propagation semantics frozen

[ ] Exact composed-contract semantics frozen

[ ] Exact condition matrix frozen

[ ] Exact ground-truth rules frozen

[ ] Exact metrics frozen

[ ] Implementation begins
```

---

# 54. Interpretation Rules

## If DARA-DT Beats Local Contract Only

Conclusion:

> Multi-stage dependency reasoning is useful, but DARA-DT-specific
> differentiation is not established.

---

## If DARA-DT Equals Composed Contract

Conclusion:

> Runtime-contract equivalence persists under the tested multi-stage
> propagation conditions.

The contribution must narrow again.

---

## If DARA-DT Beats Composed Contract

Do not immediately claim novelty.

First determine:

```text
What exact information caused the difference?
```

Then test whether that information can be added fairly to the composed
contract.

If it can:

```text
rerun the comparison.
```

Only a difference that survives the strongest justified comparator is
interesting for the contribution.

---

## If DARA-DT Loses

Report the result.

Investigate whether:

```text
propagation reasoning over-intervenes

evidence handling is weak

dependency propagation is incorrect

authority semantics are poorly calibrated
```

Do not redesign the experiment retrospectively.

---

# 55. Current Contribution Boundary

Before EXP-010 results, the safe contribution remains:

> **DARA-DT provides an experimental framework for studying how
> physical–digital divergence, decision dependencies, decision validity and
> runtime evidence quality interact in runtime assurance for AI-driven
> logistics Digital Twins. Existing experiments demonstrate the value of
> decision-sensitive assurance relative to global monitoring while also
> showing repeated equivalence with strong runtime-contract mechanisms in the
> decision structures evaluated so far.**

EXP-010 is intended to test whether this boundary can legitimately be moved.

---

# 56. Contribution Claim Prohibited Before Results

Do not state:

> DARA-DT solves divergence propagation.

Do not state:

> DARA-DT outperforms dependency-aware runtime contracts.

Do not state:

> DARA-DT is the first propagation-aware Digital Twin assurance framework.

Do not state:

> EXP-010 proves DARA-DT novelty.

The experiment has not yet been implemented.

---

# 57. Expected Scientific Value

EXP-010 is valuable even if H0 survives.

If:

```text
Composed Runtime Contract
        =
Propagation-Aware DARA-DT
```

the project will have established a meaningful negative result:

> Explicit divergence propagation may not provide additional binary assurance
> value once all relevant dependencies and runtime evidence are represented
> adequately by a composed contract for the tested logistics decision chain.

That would materially refine the PhD research direction.

---

# 58. Stronger Positive Result

A potentially important result would require:

```text
same observable evidence
        +
same known dependencies
        +
same decision chain
        ↓
Composed Contract misses downstream consequence
        ↓
DARA-DT detects it
        ↓
difference specifically attributable
to divergence-origin / propagation information
```

Only then would EXP-010 provide evidence for a stronger DARA-DT
differentiation hypothesis.

Even then:

```text
experimental differentiation
        ≠
confirmed novelty
```

Literature comparison would still be required.

---

# 59. Final Pre-Registered Position

EXP-010 is not designed to demonstrate that DARA-DT works.

It is designed to determine whether a central proposed distinction survives a
stronger falsification test.

The experiment asks:

> **Does tracing physical–digital divergence through an autonomous logistics
> decision chain provide assurance information that cannot be reproduced by a
> strong dependency-aware composed runtime contract operating on the same
> evidence?**

The acceptable answers are:

```text
YES

NO

CONDITIONALLY
```

All three outcomes must be reported faithfully.

Until the experiment is complete:

```text
DARA-DT NOVELTY
        =
NOT ESTABLISHED
```

---

# 60. Next Step

After this pre-registration is committed:

```text
EXP-010 Pre-Registration
        ↓
Freeze Exact Condition Matrix
        ↓
Audit Matrix for Comparator Fairness
        ↓
Freeze Ground Truth
        ↓
Freeze Metrics
        ↓
Only Then Implement
```

The immediate next artifact is:

```text
docs/experiment_010_condition_matrix.md
```

No EXP-010 implementation should begin before that matrix has been reviewed
and frozen.
