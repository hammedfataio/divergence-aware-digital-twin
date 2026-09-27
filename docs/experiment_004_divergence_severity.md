# Experiment 004 — Divergence Severity and Decision Validity

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-004  
**Status:** Completed — Controlled Proof-of-Concept  
**Research Stage:** Decision Relevance → Decision Impact / Validity  
**Domain:** Autonomous Logistics Digital Twin

---

## 1. Purpose

Previous DARA-DT experiments established that the amount of physical–digital
divergence alone is insufficient for determining whether an autonomous
AI-generated decision should be interrupted.

EXP-001 to EXP-003 introduced the distinction between:

- global physical–digital divergence; and
- divergence relevant to the dependencies of the current decision.

However, an unresolved question remained:

> If a divergence affects something the decision depends on, does that
> necessarily mean the decision should be interrupted?

EXP-004 tests this assumption by progressively increasing divergence in a
decision-relevant vehicle-capacity variable while independently evaluating
whether the resulting vehicle-assignment decision remains physically valid.

The experiment therefore marks the transition from **decision relevance** to
**decision impact and validity**.

---

## 2. Research Question

> **How does the severity of decision-relevant physical–digital divergence
> affect the physical validity of an autonomous logistics decision?**

The experiment examines whether:

1. all decision-relevant divergence requires intervention;
2. divergence magnitude alone is sufficient for intervention;
3. a decision-validity boundary can be observed; and
4. decision relevance must be extended with decision-impact reasoning.

---

## 3. Experimental Hypothesis

The working hypothesis is:

> **Decision relevance is useful for identifying which divergence matters to
> a decision, but relevance alone is insufficient to determine whether
> autonomous execution should be restricted.**

A divergence may affect a variable used by a decision while remaining too
small to invalidate that decision.

The assurance problem therefore becomes:

```text
Is the divergence relevant?
        ↓
If yes:
Does it cross the physical validity boundary of this decision?
```

This distinction is central to EXP-004.

---

## 4. Controlled Scenario

A single vehicle and a single order are used to isolate the effect of
capacity divergence.

The Digital Twin initially represents:

| Variable | Twin State |
|---|---:|
| Vehicle capacity | 10 |
| Order demand | 5 |
| Vehicle status | Operational |
| Vehicle availability | Available |

The Digital Twin is first synchronised with the physical logistics
environment.

The physical vehicle capacity is then modified while the Digital Twin retains
the original capacity of `10`.

The controller therefore generates its assignment from a stale but internally
consistent Digital Twin.

All other relevant variables are held constant.

This creates a controlled experiment in which **capacity divergence severity**
is the principal manipulated variable.

---

## 5. Severity Conditions

Seven controlled conditions are evaluated.

| Condition | Twin Capacity | Physical Capacity | Order Demand | Divergence Magnitude | Physical Decision Validity |
|---|---:|---:|---:|---:|---|
| S0 | 10 | 10 | 5 | 0 | Valid |
| S1 | 10 | 9 | 5 | 1 | Valid |
| S2 | 10 | 7 | 5 | 3 | Valid |
| S3 | 10 | 6 | 5 | 4 | Valid |
| S4 | 10 | 5 | 5 | 5 | Valid |
| S5 | 10 | 4 | 5 | 6 | Invalid |
| S6 | 10 | 2 | 5 | 8 | Invalid |

The critical transition occurs between **S4** and **S5**.

At S4:

```text
physical capacity = order demand
5 = 5
```

The assignment remains physically feasible.

At S5:

```text
physical capacity < order demand
4 < 5
```

The assignment becomes physically invalid.

This creates an explicit decision-validity boundary.

---

## 6. Independent Ground Truth

Ground truth is determined from the physical logistics state rather than from
the assurance policy.

For the controlled capacity decision:

```text
physical capacity >= order demand
        ↓
decision physically valid
```

and:

```text
physical capacity < order demand
        ↓
decision physically invalid
```

This separation is important.

The runtime-assurance mechanism must be evaluated against an independent
physical criterion rather than defining the criterion used to judge itself.

Therefore:

| Conditions | Ground-Truth Requirement |
|---|---|
| S0–S4 | No intervention required |
| S5–S6 | Intervention required |

---

## 7. Assurance Strategies

Four assurance behaviours are examined.

### B0 — No Assurance

The autonomous decision is allowed regardless of detected divergence.

This represents unrestricted autonomous execution.

---

### B1 — Global Divergence Assurance

Any detected physical–digital divergence triggers intervention.

This strategy does not consider whether the divergence changes the physical
validity of the decision.

---

### B2 — Fixed-Magnitude Assurance

Intervention is determined using a fixed divergence-magnitude threshold.

For this controlled experiment, the implemented threshold is:

```text
threshold = 5
```

This baseline tests whether divergence severity alone can provide an adequate
intervention rule.

The threshold is experimental and scenario-specific.

It is not proposed as a universal DARA-DT threshold.

---

### P1 — Decision-Relevance Assurance

The relevance-based DARA-DT policy determines whether the capacity divergence
affects a dependency of the current vehicle-assignment decision.

Because capacity is a dependency of the assignment, capacity divergence in
S1–S6 is classified as decision-relevant.

This experiment deliberately tests the limitation of that mechanism.

---

## 8. Expected Behaviour from Physical Ground Truth

The physically appropriate assurance behaviour is:

| Condition | Physical Validity | Correct Assurance Behaviour |
|---|---|---|
| S0 | Valid | Allow |
| S1 | Valid | Allow |
| S2 | Valid | Allow |
| S3 | Valid | Allow |
| S4 | Valid | Allow |
| S5 | Invalid | Intervene |
| S6 | Invalid | Intervene |

The critical requirement is therefore not simply to detect capacity
divergence.

The assurance mechanism must distinguish **relevant but non-invalidating
divergence** from **relevant and invalidating divergence**.

---

## 9. Experimental Results

### 9.1 No Assurance

No Assurance permits execution across all seven conditions.

This is correct for:

```text
S0–S4
```

but incorrect for:

```text
S5–S6
```

Therefore, the unrestricted policy produces missed interventions when
physical capacity falls below order demand.

---

### 9.2 Global Divergence Assurance

The global-divergence policy allows S0 because no divergence exists.

It intervenes whenever physical capacity differs from the Digital Twin.

Therefore it intervenes across:

```text
S1–S6
```

This correctly identifies the invalid S5 and S6 conditions but unnecessarily
intervenes in S1–S4.

The result illustrates the cost of treating any physical–digital mismatch as
sufficient reason to remove autonomous authority.

---

### 9.3 Decision-Relevance Assurance

Capacity is an explicit dependency of the vehicle-assignment decision.

Therefore the relevance mechanism correctly identifies the capacity
divergence in S1–S6 as decision-relevant.

However, relevance alone does not distinguish:

```text
S1–S4
relevant divergence + physically valid decision
```

from:

```text
S5–S6
relevant divergence + physically invalid decision
```

As a result, the relevance-only policy also over-intervenes in S1–S4.

This is the central result of EXP-004.

---

### 9.4 Fixed-Magnitude Assurance

The fixed-magnitude policy provides a more selective response in this
particular synthetic experiment.

The threshold happens to align closely with the constructed validity
transition between S4 and S5.

This is useful as a baseline comparison but must be interpreted cautiously.

The alignment exists because:

- Twin capacity is fixed at `10`;
- demand is fixed at `5`; and
- physical validity changes immediately below capacity `5`.

If order demand changed, the validity boundary would also change.

A fixed global divergence threshold would not necessarily move with that
decision-specific requirement.

Therefore the result does not establish that a threshold of `5`, or any
single fixed threshold, is generally appropriate.

---

## 10. Central Finding

EXP-004 demonstrates a critical distinction:

> **Decision relevance is not equivalent to decision invalidity.**

For example:

```text
Twin capacity     = 10
Physical capacity = 9
Order demand      = 5
```

The capacity mismatch is clearly relevant because the decision depends on
vehicle capacity.

However:

```text
9 >= 5
```

so the assignment remains physically feasible.

Intervention based solely on relevance would therefore unnecessarily remove
autonomous authority.

By contrast:

```text
Twin capacity     = 10
Physical capacity = 4
Order demand      = 5
```

is both decision-relevant and decision-invalidating because:

```text
4 < 5
```

This distinction motivates a move from binary relevance reasoning toward
decision-specific impact and validity reasoning.

---

## 11. Relevance vs Severity vs Impact

EXP-004 separates three concepts.

### Decision Relevance

```text
Does the divergence affect a variable required by the decision?
```

### Divergence Severity

```text
How large is the physical–digital difference?
```

### Decision Impact

```text
Does that difference change whether the decision remains physically valid?
```

These concepts are related but not interchangeable.

The experiment therefore motivates:

```text
Physical–Digital Divergence
        ↓
Decision Relevance
        ↓
Divergence Severity
        ↓
Decision Impact / Validity
        ↓
Runtime Assurance
```

Later experiments refine this further.

---

## 12. Why Magnitude Alone Is Also Insufficient

EXP-004 might appear to suggest that a fixed magnitude threshold solves the
problem.

However, magnitude has meaning only relative to the decision context.

Consider:

```text
Twin capacity     = 10
Physical capacity = 7
Divergence        = 3
```

For an order requiring `5` units:

```text
7 >= 5
```

the assignment remains valid.

For an order requiring `8` units:

```text
7 < 8
```

the same divergence magnitude makes the assignment invalid.

Therefore:

> **Equal divergence magnitude can produce different decision consequences.**

This becomes a central controlled comparison in EXP-005.

---

## 13. Contribution of EXP-004 to the Research Progression

Before EXP-004, the working experimental model was approximately:

```text
Physical–Digital Divergence
        ↓
Decision Relevance
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

EXP-004 demonstrates that an additional reasoning stage is required:

```text
Physical–Digital Divergence
        ↓
Decision Relevance
        ↓
Decision Impact / Validity
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

This represents refinement of the original hypothesis rather than a change
of research scope.

The central research problem remains the runtime regulation of autonomous
decisions under physical–digital divergence.

---

## 14. Connection to EXP-005

EXP-004 identifies the limitation.

EXP-005 tests a potential response to that limitation.

The next experimental question becomes:

> **Can decision-specific impact or validity reasoning distinguish relevant
> divergence that actually invalidates a decision from relevant divergence
> that leaves the decision physically feasible?**

EXP-005 therefore expands the controlled capacity conditions and introduces a
decision-impact-aware assurance baseline.

The progression is:

```text
EXP-003
Decision relevance
        ↓
EXP-004
Relevance is not enough
        ↓
EXP-005
Decision impact / validity
```

---

## 15. What EXP-004 Supports

Within the controlled capacity experiment, EXP-004 supports the following
observations:

- capacity divergence can be decision-relevant without invalidating the
  assignment;
- relevance-only intervention can produce false interventions;
- unrestricted autonomy can produce missed interventions after the physical
  validity boundary is crossed;
- physical decision validity depends on the relationship between physical
  capacity and order demand;
- a validity boundary can be experimentally isolated; and
- divergence severity should be interpreted relative to the decision context.

---

## 16. What EXP-004 Does Not Establish

EXP-004 does **not** establish:

- a universal divergence threshold;
- that capacity is the only important logistics dependency;
- that decision-impact reasoning is generally superior;
- that the observed validity relationship generalises to categorical
  dependencies;
- statistical generalisation;
- robustness to imperfect evidence;
- real-world logistics effectiveness;
- formal safety guarantees; or
- confirmed novelty of DARA-DT.

These questions require subsequent experiments.

---

## 17. Threats to Validity

### 17.1 Single Dependency Type

The experiment manipulates vehicle capacity only.

Capacity provides a clear numeric validity boundary, but this does not
demonstrate equivalent behaviour for:

- operational status;
- availability;
- location; or
- other logistics state variables.

---

### 17.2 Deterministic Conditions

The severity values are deliberately selected rather than sampled from a
stochastic operational process.

This provides experimental control but limits external validity.

---

### 17.3 Simplified Decision Rule

The physical feasibility criterion is intentionally transparent:

```text
physical capacity >= demand
```

Real logistics decisions may depend on multiple interacting constraints.

---

### 17.4 Fixed Threshold Baseline

The fixed magnitude threshold is deliberately simple.

Its apparent effectiveness around the constructed boundary should not be
generalised beyond this experiment.

---

### 17.5 Perfect State Knowledge for Evaluation

Independent ground truth uses the physical state directly.

This is appropriate for controlled evaluation but does not imply that a
deployed assurance system would have perfect knowledge of physical reality.

EXP-006 later investigates the consequences of imperfect runtime evidence.

---

## 18. Falsification Perspective

The emerging decision-impact hypothesis would be weakened if:

- decision validity showed no meaningful relationship to decision-specific
  physical constraints;
- simple global thresholds consistently matched or exceeded decision-specific
  reasoning across varied demands and dependencies;
- relevance alone remained sufficient across broader controlled conditions;
  or
- explicit impact reasoning introduced complexity without improving
  intervention selectivity.

EXP-005 is therefore designed to challenge, rather than assume, the value of
decision-impact reasoning.

---

## 19. Reproducibility

The controlled severity experiment is implemented in:

```text
src/dara_dt/experiments/severity_experiment.py
```

The implementation:

1. creates the logistics environment;
2. synchronises the Digital Twin;
3. modifies physical vehicle capacity;
4. retains stale Twin capacity;
5. generates the vehicle-assignment decision;
6. detects physical–digital divergence;
7. evaluates decision relevance;
8. establishes independent physical ground truth;
9. evaluates assurance strategies; and
10. records the resulting assurance outcomes.

Dedicated automated tests validate the experimental conditions and expected
behaviour.

The experiment should remain reproducible through the repository's automated
test and experiment workflow.

---

## 20. Research Integrity

The purpose of EXP-004 is not to produce a favourable result for DARA-DT.

In fact, the experiment exposes a weakness in the relevance-only version of
the framework.

That negative result is retained because it improves the research model.

The evidence shows:

```text
Decision relevance
        ↓
useful for identifying which divergence matters

but

Decision relevance alone
        ↓
insufficient for deciding whether intervention is required
```

This limitation directly motivates the next experimental stage.

---

## 21. Conclusion

EXP-004 demonstrates that detecting decision-relevant physical–digital
divergence is not sufficient to determine whether an autonomous logistics
decision should be interrupted.

Across the controlled capacity conditions, S1–S4 contain divergence affecting
a decision dependency while the assignment remains physically valid.

Only when physical capacity falls below order demand at S5 and S6 does the
decision become physically invalid.

The experiment therefore establishes the distinction:

> **Relevant divergence tells us that a mismatch matters to the decision.
> Decision impact tells us whether that mismatch changes the decision's
> physical validity.**

This result motivates EXP-005 and advances the DARA-DT research model from
decision relevance toward decision-specific impact and validity reasoning.
