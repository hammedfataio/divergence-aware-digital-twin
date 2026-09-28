# Experiment 008 — Imperfect Evidence and Runtime-Contract Comparison

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-008  
**Status:** Experimental Design — Pre-Implementation  
**Research Stage:** Imperfect Evidence and Comparative Runtime Assurance

---

## 1. Objective

EXP-008 investigates whether decision-conditioned physical–digital divergence
provides useful runtime-assurance information beyond direct runtime-contract
checking when runtime evidence about the physical system is imperfect.

EXP-007 established that Decision Impact and Runtime Contract produced identical
intervention outcomes across the tested capacity, operational-status, and
location/availability dependencies when reliable runtime evidence was available.

Therefore, EXP-008 deliberately removes the reliable-evidence assumption.

The experiment introduces controlled imperfections into runtime evidence while
preserving independent knowledge of the physical ground truth.

The purpose is not to demonstrate that DARA-DT is superior.

The purpose is to test whether the additional reasoning performed by DARA-DT
produces measurably different and useful assurance behaviour when direct
physical-state observations cannot be assumed to be complete and trustworthy.

---

## 2. Primary Research Question

> **Does decision-conditioned physical–digital divergence provide useful
> runtime-assurance information beyond direct runtime contracts when
> physical-state evidence is incomplete, stale, inaccurate, or conflicting?**

---

## 3. Supporting Research Questions

### RQ8.1 — Evidence Reliability

How does degradation in runtime evidence affect the intervention decisions of
direct runtime contracts and divergence-aware assurance?

### RQ8.2 — Safety

Which assurance mechanism better avoids missed interventions when unreliable
evidence hides a physically invalid decision?

### RQ8.3 — Autonomy Preservation

Which mechanism better avoids unnecessary intervention when imperfect evidence
creates apparent risk while the proposed decision remains physically valid?

### RQ8.4 — Uncertainty Handling

Can explicit treatment of evidence quality support more appropriate
ALLOW, RESTRICT, or DEFER behaviour than treating an observation as a
definitive physical fact?

### RQ8.5 — Comparative Contribution

Does the divergence → relevance → impact → evidence reasoning chain provide
assurance information that cannot be reproduced by a simpler runtime-contract
mechanism under the same evidence constraints?

---

## 4. Experimental Principle

EXP-008 separates three representations of system state:

\[
P_t = \text{Physical Ground Truth}
\]

\[
T_t = \text{Digital Twin State}
\]

\[
E_t = \text{Runtime Evidence}
\]

These states must not be treated as equivalent.

The physical state determines whether the proposed decision is actually valid.

The Digital Twin represents the state available to the AI decision process.

Runtime evidence represents observations available to the assurance mechanism.

Therefore:

\[
P_t \neq T_t \neq E_t
\]

may occur during the experiment.

This separation is essential because imperfect runtime evidence is the variable
being tested.

---

## 5. Decision-Level Assurance Model

The conceptual DARA-DT chain remains:

\[
D_t = \text{Detected Physical–Digital Divergence}
\]

\[
D_t^{rel}(d_t) = Dep(d_t) \cap D_t
\]

where:

- \(d_t\) is the proposed AI decision;
- \(Dep(d_t)\) is the set of state dependencies required by that decision;
- \(D_t\) is detected divergence;
- \(D_t^{rel}(d_t)\) is decision-relevant divergence.

Decision impact is then conditioned on runtime evidence:

\[
I_t = f(d_t, D_t^{rel}, E_t)
\]

and authority is determined by:

\[
A_t = \pi(d_t, D_t^{rel}, I_t, E_t)
\]

EXP-008 tests whether this richer reasoning provides useful assurance behaviour
when \(E_t\) cannot be assumed to perfectly represent \(P_t\).

---

## 6. Dependency Families

The experiment retains the three dependency families established in EXP-007:

1. **Capacity**
2. **Operational Status**
3. **Location / Availability**

This prevents the experiment from becoming another capacity-only evaluation.

---

## 7. Evidence Conditions

Four primary evidence conditions are evaluated.

### E0 — Reliable Evidence

Runtime evidence accurately represents the relevant physical state.

Example:

- physical capacity = 6;
- runtime evidence = 6.

This provides the control condition.

---

### E1 — Stale Evidence

Runtime evidence was previously correct but no longer represents the current
physical state.

Example:

- Digital Twin status = operational;
- vehicle physically breaks down;
- evidence still reports operational.

This tests whether an assurance mechanism can recognise that apparently valid
evidence may no longer be sufficiently trustworthy.

---

### E2 — Missing Evidence

Evidence required to validate a decision dependency is unavailable.

Example:

- current vehicle availability cannot be observed.

A mechanism must determine whether to:

- allow the decision;
- restrict authority;
- defer the decision;
- use fallback behaviour.

---

### E3 — Conflicting Evidence

Two or more evidence sources provide incompatible observations.

Example:

- one location source reports `depot`;
- another reports `remote_site`.

The assurance mechanism must not silently treat one observation as unquestioned
physical truth unless an explicit resolution rule justifies doing so.

---

## 8. Optional Secondary Evidence Conditions

If the primary experiment is successful and remains manageable, later extensions
may examine:

### E4 — Noisy Evidence

Observed values contain bounded measurement error.

### E5 — Incorrect but High-Confidence Evidence

An evidence source reports an incorrect state while appearing trustworthy.

### E6 — Compound Evidence Failure

Multiple evidence limitations occur simultaneously.

These are not required for the minimum EXP-008 matrix and should not be added
until the primary experiment is complete.

---

## 9. Core Experimental Matrix

Each dependency family should contain at least the following evidence scenarios:

| Scenario | Physical Decision State | Evidence State | Purpose |
|---|---|---|---|
| R0 | Valid | Reliable | Control — valid |
| R1 | Invalid | Reliable | Control — invalid |
| S0 | Valid | Stale | Test unnecessary intervention |
| S1 | Invalid | Stale | Test hidden invalidity |
| M0 | Valid | Missing | Test conservative uncertainty handling |
| M1 | Invalid | Missing | Test safety under unavailable evidence |
| C0 | Valid | Conflicting | Test false-intervention risk |
| C1 | Invalid | Conflicting | Test missed-intervention risk |

With three dependency families:

\[
3 \times 8 = 24
\]

minimum controlled experimental conditions.

The minimum EXP-008 matrix therefore contains **24 conditions**.

---

## 10. Example Capacity Conditions

Examples include:

### CAP-R0

Physical capacity satisfies demand and reliable evidence reports the correct
capacity.

Expected ground truth:

**DO_NOT_INTERVENE**

---

### CAP-R1

Physical capacity is below required demand and reliable evidence reports the
correct capacity.

Expected ground truth:

**INTERVENE**

---

### CAP-S0

Physical capacity satisfies demand, but stale evidence reports an older value
that suggests insufficient capacity.

Expected ground truth:

**DO_NOT_INTERVENE**

This condition measures unnecessary intervention caused by stale evidence.

---

### CAP-S1

Physical capacity has fallen below demand, but stale evidence reports an older
higher capacity.

Expected ground truth:

**INTERVENE**

This condition measures whether stale evidence can hide decision invalidity.

---

### CAP-M0 / CAP-M1

Current capacity evidence is unavailable while the physical decision is,
respectively, valid or invalid.

The assurance mechanism cannot know physical validity directly from the missing
observation.

---

### CAP-C0 / CAP-C1

Multiple evidence sources disagree about current capacity.

The physical ground truth remains independently known by the experiment.

---

## 11. Status Conditions

The same experimental structure is applied to operational status.

Examples include:

- operational physical vehicle with reliable operational evidence;
- broken-down vehicle with reliable failure evidence;
- stale operational evidence after physical breakdown;
- stale failure evidence after physical recovery;
- missing status evidence;
- conflicting operational and failure reports.

The physical state determines ground truth.

Evidence determines what the assurance mechanism can observe.

---

## 12. Location / Availability Conditions

Location and availability are evaluated as a combined dispatch dependency.

Examples include:

- vehicle physically at an allowed location and available;
- vehicle physically outside the permitted operational region;
- stale location observation;
- stale availability observation;
- missing location or availability evidence;
- conflicting location observations.

A decision is physically valid only when the required location and availability
constraints are satisfied.

---

## 13. Assurance Policies

The primary comparison includes four policy families.

### P0 — No Assurance

Always permits the proposed AI decision.

Purpose:

Provide a lower-bound safety comparator.

---

### P1 — Global Divergence

Intervenes whenever divergence is detected.

Purpose:

Test whether coarse divergence detection remains overly conservative.

---

### P2 — Direct Runtime Contract

Evaluates the decision requirement using the runtime evidence available to it.

Examples:

\[
capacity_{observed} \ge demand
\]

\[
status_{observed} = operational
\]

\[
location_{observed} \in permitted\_locations
\]

The runtime contract must receive the same evidence available to DARA-DT.

It must not receive privileged access to physical ground truth.

---

### P3 — DARA-DT Evidence-Aware Assurance

Uses:

- detected divergence;
- decision dependencies;
- decision relevance;
- estimated decision impact;
- runtime evidence;
- evidence quality or reliability state.

The mechanism may return:

- **ALLOW**
- **RESTRICT**
- **DEFER**
- **FALLBACK**

depending on the available evidence and estimated decision risk.

---

## 14. Fair-Comparison Requirement

Runtime Contract and DARA-DT must operate under the **same information
constraints**.

Neither mechanism may receive physical ground truth during runtime evaluation.

Physical ground truth is reserved exclusively for experimental evaluation.

This prevents unfair comparison such as:

\[
RuntimeContract(E_t)
\]

versus:

\[
DARA(P_t, T_t, E_t)
\]

Instead, both policies must operate using information legitimately available at
runtime.

Ground truth \(P_t\) is revealed only to the evaluator after the assurance
decision has been produced.

---

## 15. Ground Truth

Ground truth is determined independently using the physical system state.

The validator determines whether the proposed decision is physically valid.

Ground-truth classes remain:

- **INTERVENE**
- **DO_NOT_INTERVENE**

This remains independent from policy output.

---

## 16. Handling DEFER and RESTRICT

EXP-008 introduces an important distinction between intervention correctness and
authority state.

A policy may produce:

- ALLOW
- RESTRICT
- DEFER
- FALLBACK

For safety evaluation, non-ALLOW states may count as intervention.

However, they should also be recorded separately.

For example:

- DEFER caused by missing evidence is not semantically identical to RESTRICT
  caused by confirmed invalidity.

Therefore EXP-008 must report both:

1. binary intervention outcome;
2. authority-state distribution.

---

## 17. Primary Metrics

For each policy:

- True Interventions (TI)
- False Interventions (FI)
- Missed Interventions (MI)
- Correct Non-Interventions (CNI)
- Accuracy
- Intervention Precision
- Intervention Recall
- False-Intervention Rate
- Missed-Intervention Rate
- Autonomy Availability

Where:

\[
AutonomyAvailability =
\frac{ALLOW}{TotalDecisions}
\]

---

## 18. Evidence-Specific Metrics

Results must also be grouped by evidence condition:

- reliable;
- stale;
- missing;
- conflicting.

This prevents strong performance under reliable evidence from hiding poor
performance under degraded evidence.

---

## 19. Dependency-Specific Metrics

Results must also be grouped by:

- capacity;
- operational status;
- location / availability.

This tests whether any observed advantage is dependency-specific.

---

## 20. Authority Metrics

Record:

- ALLOW count;
- RESTRICT count;
- DEFER count;
- FALLBACK count.

This allows the experiment to distinguish:

> avoiding unsafe actions

from:

> simply refusing to make autonomous decisions.

A mechanism that defers every uncertain case may achieve high intervention
recall while providing very little useful autonomy.

---

## 21. Safety–Autonomy Trade-Off

EXP-008 explicitly evaluates:

\[
\text{Safety}
\leftrightarrow
\text{Autonomy Availability}
\]

A useful assurance mechanism should not be evaluated only by its ability to
prevent invalid actions.

It should also preserve autonomous operation when sufficient evidence supports
the decision.

---

## 22. Hypotheses

### H8.1

Global divergence monitoring will remain vulnerable to unnecessary intervention
because it does not condition mismatch on the proposed decision.

### H8.2

Direct runtime contracts will perform strongly when evidence is reliable.

### H8.3

Runtime-contract performance may degrade when required evidence is stale,
missing, or conflicting.

### H8.4

Evidence-aware DARA-DT may provide different authority behaviour under imperfect
evidence by explicitly representing uncertainty rather than treating every
observation as definitive physical truth.

### H8.5

Any improvement must be evaluated against the additional information and
complexity required by DARA-DT.

These are hypotheses, not expected results.

---

## 23. Falsification Criteria

EXP-008 is explicitly designed to challenge the proposed contribution.

### Kill Test A — Runtime-Contract Equivalence

If Runtime Contract performs equivalently to DARA-DT across imperfect-evidence
conditions while requiring less information or complexity, the evidence does
not support DARA-DT as a superior runtime-assurance mechanism.

The contribution must be narrowed or reframed.

---

### Kill Test B — Conservative Deferral

If DARA-DT appears safer only because it defers or restricts nearly every
uncertain decision, the result does not establish useful assurance superiority.

Autonomy availability must be considered.

---

### Kill Test C — Dependency Specificity

If any advantage appears only for capacity and does not generalise to status or
location/availability, the broad cross-dependency claim must be narrowed.

---

### Kill Test D — Evidence Privilege

If DARA-DT requires access to evidence unavailable to Runtime Contract, any
performance difference cannot be attributed fairly to the assurance mechanism.

Both mechanisms must receive equivalent runtime information.

---

### Kill Test E — Equivalent Simpler Mechanism

If a small extension to Runtime Contract, such as explicit UNKNOWN or evidence
freshness checking, reproduces DARA-DT behaviour with substantially less
complexity, the stronger DARA-DT contribution is weakened.

This comparator should be considered before making novelty claims.

---

## 24. Interpretation Rules

The experiment must not conclude that DARA-DT is novel merely because it
outperforms one baseline.

Possible outcomes include:

### Outcome A — DARA-DT and Runtime Contract remain equivalent

The additional divergence-aware reasoning may not provide sufficient practical
value under the tested conditions.

### Outcome B — DARA-DT improves safety but sharply reduces autonomy

The mechanism may be more conservative rather than more informative.

### Outcome C — DARA-DT improves the safety–autonomy trade-off

This would provide evidence supporting further investigation, but would not by
itself establish novelty.

### Outcome D — A simple uncertainty-aware contract matches DARA-DT

The contribution may lie in system integration, evidence modelling, or
decision-conditioned assurance rather than superior intervention performance.

### Outcome E — Results vary substantially across dependencies

The proposed general framework may need to become a family of
dependency-specific assurance mechanisms.

---

## 25. Relationship to Previous Experiments

The experimental progression is:

### EXP-001

Demonstrated that equal divergence counts can have different decision
consequences.

### EXP-002

Compared assurance policies across a controlled divergence matrix.

### EXP-003

Formalised decision relevance.

### EXP-004

Demonstrated that relevance alone does not determine invalidity.

### EXP-005

Introduced decision-impact reasoning.

### EXP-006

Demonstrated the importance of imperfect runtime evidence.

### EXP-007

Demonstrated bounded cross-dependency generalisation and found equivalence
between Decision Impact and Runtime Contract under reliable evidence.

### EXP-008

Directly tests whether that equivalence persists when runtime evidence becomes
imperfect.

---

## 26. Expected Contribution of EXP-008

EXP-008 is not intended to prove the final research contribution.

Its purpose is to determine whether the candidate contribution survives a
stronger comparative test.

The key question is no longer simply:

> Can DARA-DT identify invalid decisions?

Instead:

> **Does decision-conditioned physical–digital divergence provide useful
> assurance information beyond simpler runtime validity mechanisms when the
> evidence describing physical reality is imperfect?**

This is a substantially stronger test of the research hypothesis.

---

## 27. Threats to Validity

Important limitations include:

- controlled synthetic evidence failures;
- simplified logistics dependencies;
- limited number of dependency families;
- deterministic proposed decisions;
- simplified evidence reliability representation;
- limited operational complexity;
- absence of production-scale sensor infrastructure;
- limited temporal dynamics in the initial matrix.

Results must therefore be interpreted as controlled experimental evidence, not
as production deployment evidence.

---

## 28. Implementation Plan

Implementation should proceed only after this design is frozen.

Required components are expected to include:

1. EXP-008 condition definitions;
2. evidence-quality representation;
3. equal-information runtime-contract comparator;
4. DARA-DT evidence-aware policy;
5. independent physical ground-truth evaluation;
6. experiment runner;
7. aggregate metrics;
8. dependency-specific metrics;
9. evidence-condition-specific metrics;
10. automated tests;
11. GitHub Actions execution;
12. results documentation.

No result should be entered into this document until generated by the
implemented experiment.

---

## 29. Pre-Implementation Status

At this stage:

- the research question is defined;
- the experimental matrix is specified;
- comparator policies are defined;
- information-access constraints are defined;
- evaluation metrics are defined;
- falsification criteria are pre-registered;
- no EXP-008 results have been generated.

**EXP-008 remains a pre-implementation experimental design.**
