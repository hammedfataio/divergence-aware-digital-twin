# Experiment 006 — Runtime Assurance Under Imperfect Evidence

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-006  
**Status:** Completed — Controlled Proof-of-Concept  
**Research Stage:** Decision Impact → Evidence Reliability  
**Domain:** Autonomous Logistics Digital Twin

---

## 1. Purpose

EXP-005 demonstrated that decision-impact reasoning can provide more selective
runtime intervention than divergence presence or decision relevance alone
within controlled vehicle-capacity conditions.

However, EXP-005 assumes that the assurance mechanism has reliable evidence
about physical reality.

That assumption is potentially unrealistic.

Operational Digital Twins may receive evidence that is:

- inaccurate;
- delayed;
- stale;
- missing;
- conflicting; or
- apparently valid but misleading.

EXP-006 therefore tests what happens when the runtime evidence used to
estimate decision impact is imperfect.

The experiment introduces a critical separation:

> **Physical Ground Truth ≠ Runtime Evidence ≠ Digital Twin State**

---

## 2. Research Question

> **How robust is decision-impact-aware runtime assurance when the evidence
> used to estimate physical–digital divergence and decision impact is
> imperfect?**

The experiment investigates whether an evidence-aware assurance policy can
preserve useful autonomous authority while responding appropriately to
uncertain or degraded runtime evidence.

---

## 3. Motivation

Decision-impact reasoning depends on information about the physical system.

For a capacity-dependent decision, the reasoning may appear straightforward:

```text
Observed physical capacity
        ↓
Compare with required demand
        ↓
Estimate decision validity
        ↓
Choose assurance action
```

However, the observed capacity may itself be wrong.

For example:

```text
Actual physical capacity = 4
Observed capacity        = 6
Demand                   = 5
```

Ground truth says:

```text
4 < 5
Decision invalid
```

but runtime evidence suggests:

```text
6 >= 5
Decision appears valid
```

A logically correct assurance rule can therefore still produce an incorrect
decision when its evidence is misleading.

EXP-006 explicitly investigates this problem.

---

## 4. Three-State Separation

The experiment distinguishes three information layers.

### Physical Ground Truth

The actual physical state of the logistics system.

This is used only for independent experimental evaluation.

### Runtime Evidence

The information available to the assurance mechanism about physical reality.

Runtime evidence may be correct, incorrect, stale, missing or conflicting.

### Digital Twin State

The state currently represented by the Digital Twin and used by the
autonomous decision-maker.

These states must not be treated as interchangeable.

Conceptually:

```text
Physical Ground Truth
        │
        │ may be imperfectly observed
        ↓
Runtime Evidence
        │
        │ used for assurance reasoning
        ↓
Runtime Assurance

Digital Twin State
        │
        ↓
AI Decision
```

The evaluator retains access to physical ground truth so that assurance
behaviour can be judged independently.

---

## 5. Experimental Domain

EXP-006 continues using vehicle capacity as the controlled dependency.

This preserves comparability with EXP-004 and EXP-005 while changing the
principal experimental factor from:

```text
decision impact
```

to:

```text
evidence reliability
```

The experiment therefore does not simultaneously introduce a new dependency
type.

This helps isolate the effect of imperfect evidence.

---

## 6. Evidence Conditions

Twelve controlled evidence conditions are evaluated.

### E0 — Accurate Evidence, Invalid Decision

Runtime evidence accurately represents an invalid physical condition.

This provides a straightforward positive control.

---

### E1 — Small Error, Still Invalid

Runtime evidence contains measurement error, but the estimated state remains
on the invalid side of the decision boundary.

This tests whether small error necessarily changes the assurance outcome.

---

### E2 — Boundary-Shifting Evidence

Evidence error moves the estimated state toward or onto the decision
boundary.

This tests sensitivity near the physical validity threshold.

---

### E3 — Validity-Flipping Evidence

The physical decision is invalid, but runtime evidence makes it appear valid.

This is a critical failure condition.

---

### E4 — Stale Evidence Hides Invalidity

Evidence represents an earlier physical state and no longer reflects the
current invalid condition.

---

### E5 — Missing Evidence

Required runtime evidence is unavailable.

The assurance mechanism must decide whether autonomous execution can still be
justified.

---

### E6 — Conflicting Evidence

Available observations disagree.

The assurance mechanism cannot obtain a single unambiguous estimate from the
available evidence.

---

### E7 — Accurate Evidence, Valid Decision

Runtime evidence accurately represents a physically valid condition.

This provides a negative control.

---

### E8 — Valid Decision Appears Invalid

The physical decision is valid, but pessimistic evidence makes it appear
invalid.

This tests unnecessary loss of autonomous authority.

---

### E9 — Larger Validity Margin Tolerates Error

Evidence contains error, but the physical and estimated states remain
sufficiently far from the validity boundary for the decision outcome to
remain unchanged.

---

### E10 — Same Positive Error Near the Boundary

A similar evidence error occurs closer to the validity boundary where the
physical decision is invalid.

This tests whether the consequence of evidence error depends on decision
margin.

---

### E11 — Stale Twin-Matching Evidence

Runtime evidence agrees with the Digital Twin but no longer reflects current
physical reality.

This demonstrates that agreement between evidence and the Twin does not
necessarily imply agreement with the physical system.

---

## 7. Assurance Strategies

Three strategies are compared.

### B1 — Decision Relevance

The policy intervenes when divergence affects a dependency of the current
decision.

This baseline does not reason about whether the divergence actually
invalidates the decision.

---

### B2 — Deterministic Decision Impact

The deterministic impact policy receives reliable evidence about physical
capacity.

It evaluates whether the physical capacity satisfies the demand required by
the decision.

This policy represents an **idealised evidence baseline**.

It is useful for comparison but should not be interpreted as a realistic
assumption of perfect physical-state knowledge.

---

### P1 — Evidence-Aware Decision Impact

The evidence-aware policy evaluates decision impact using the runtime evidence
available to the assurance mechanism.

Its behaviour is deliberately conservative for explicitly unusable evidence.

Conceptually:

```text
Evidence available?
        ↓
Evidence status usable?
        ↓
Estimate capacity relative to demand
        ↓
ALLOW / RESTRICT / DEFER
```

---

## 8. Evidence-Aware Policy Behaviour

The implemented evidence-aware policy follows the controlled rules below.

### Missing Evidence

```text
MISSING
    ↓
DEFER
```

### Stale Evidence

```text
STALE
    ↓
DEFER
```

### Conflicting Evidence

```text
CONFLICTING
    ↓
DEFER
```

### Usable Evidence Below Demand

```text
observed capacity < demand
        ↓
DEFER
```

### Usable Evidence at the Boundary

```text
observed capacity = demand
        ↓
RESTRICT
```

### Usable Evidence Above Demand

```text
observed capacity > demand
        ↓
ALLOW
```

The implementation does not introduce an arbitrary freshness threshold for
this experiment.

Evidence explicitly represented as stale is handled according to its evidence
status.

---

## 9. Ground Truth

Physical decision validity is determined independently from the assurance
policy.

For the capacity-dependent assignment:

\[
C_{physical} \geq q
\]

means the decision is physically valid.

\[
C_{physical} < q
\]

means the decision is physically invalid.

Runtime evidence does not determine ground truth.

This distinction allows the experiment to identify cases where:

```text
Runtime evidence suggests validity
```

while:

```text
Physical ground truth shows invalidity
```

and vice versa.

---

## 10. Evaluation Outcomes

The experiment uses four primary assurance outcomes.

| Outcome | Meaning |
|---|---|
| True Intervention (TI) | Physically invalid decision and policy intervenes |
| False Intervention (FI) | Physically valid decision but policy intervenes |
| Missed Intervention (MI) | Physically invalid decision but policy allows execution |
| Correct Non-Intervention (CNI) | Physically valid decision and policy allows execution |

For aggregate evaluation, restrictive and defer actions are treated as
interventions when they prevent unrestricted autonomous execution.

Autonomy availability represents the proportion of conditions in which the
policy permits autonomous execution.

---

## 11. Verified Aggregate Results

The implemented 12-condition experiment produces:

| Policy | Conditions | TI | FI | MI | CNI | Accuracy | Precision | Recall | FI Rate | MI Rate | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Decision Relevance | 12 | 9 | 3 | 0 | 0 | 0.750 | 0.750 | 1.000 | 1.000 | 0.000 | 0.000 |
| Deterministic Impact | 12 | 9 | 0 | 0 | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.250 |
| Evidence-Aware Impact | 12 | 8 | 1 | 1 | 2 | 0.833 | 0.889 | 0.889 | 0.333 | 0.111 | 0.250 |

These values describe the controlled EXP-006 matrix only.

They are not estimates of performance in real logistics systems.

---

## 12. Decision-Relevance Result

Decision Relevance produces:

```text
TI  = 9
FI  = 3
MI  = 0
CNI = 0
```

with:

```text
Accuracy  = 0.750
Precision = 0.750
Recall    = 1.000
FI Rate   = 1.000
MI Rate   = 0.000
Autonomy  = 0.000
```

The policy catches all nine conditions requiring intervention.

However, it also intervenes in all three physically valid conditions.

This eliminates autonomous availability across the matrix.

The result reinforces the earlier conclusion:

> **Decision relevance is useful for identifying affected dependencies but is
> insufficient for determining physical decision validity.**

---

## 13. Deterministic-Impact Result

Deterministic Decision Impact produces:

```text
TI  = 9
FI  = 0
MI  = 0
CNI = 3
```

with:

```text
Accuracy  = 1.000
Precision = 1.000
Recall    = 1.000
FI Rate   = 0.000
MI Rate   = 0.000
Autonomy  = 0.250
```

This is the strongest result in the matrix.

However, its interpretation is deliberately limited.

The deterministic policy receives reliable physical-capacity evidence.

It therefore represents an **idealised upper baseline under the controlled
conditions**.

The result does not establish that decision-impact assurance will achieve
perfect performance under realistic runtime observation.

---

## 14. Evidence-Aware Result

Evidence-Aware Impact produces:

```text
TI  = 8
FI  = 1
MI  = 1
CNI = 2
```

with:

```text
Accuracy  = 0.833
Precision = 0.889
Recall    = 0.889
FI Rate   = 0.333
MI Rate   = 0.111
Autonomy  = 0.250
```

Unlike the deterministic baseline, the evidence-aware mechanism must make
assurance decisions from imperfect observations.

The resulting performance is therefore lower.

This is an important research result rather than a defect to hide.

---

## 15. Missed Intervention

The evidence-aware policy produces one missed intervention.

This demonstrates a particularly important limitation.

A conservative policy can respond safely to evidence explicitly marked as:

- missing;
- stale; or
- conflicting.

However, a harder problem occurs when evidence is:

```text
available
+
apparently usable
+
incorrect
```

If incorrect evidence makes a physically invalid condition appear valid, the
assurance mechanism may allow execution.

Therefore:

> **Evidence availability is not equivalent to evidence correctness.**

This becomes an important boundary of the current assurance mechanism.

---

## 16. False Intervention

The evidence-aware policy also produces one false intervention.

In this condition, pessimistic or misleading evidence causes a physically
valid decision to appear unacceptable.

The assurance mechanism therefore removes autonomous authority unnecessarily.

This exposes the opposite failure mode:

```text
Optimistic incorrect evidence
        ↓
risk of missed intervention

Pessimistic incorrect evidence
        ↓
risk of false intervention
```

A trustworthy runtime-assurance mechanism must manage both.

---

## 17. Why Explicit Evidence Status Is Not Enough

EXP-006 distinguishes evidence that is explicitly known to be unreliable from
evidence that is wrong without being labelled unreliable.

For:

```text
MISSING
STALE
CONFLICTING
```

the policy can take a conservative action.

But if incorrect evidence is represented as normal usable evidence, status
checking alone cannot identify the problem.

This means that evidence reliability cannot be reduced solely to:

```text
Is the evidence present?
```

or:

```text
Is the evidence explicitly marked stale?
```

Future work may require richer evidence-quality estimation, redundancy,
cross-validation or uncertainty reasoning.

Such extensions should only be introduced where they directly support the
research questions.

---

## 18. Equal Autonomy Does Not Mean Equal Assurance

Both Deterministic Impact and Evidence-Aware Impact achieve:

```text
Autonomy availability = 0.250
```

This does **not** mean the two policies provide equivalent assurance.

Deterministic Impact produces:

```text
TI = 9
FI = 0
MI = 0
CNI = 3
```

Evidence-Aware Impact produces:

```text
TI = 8
FI = 1
MI = 1
CNI = 2
```

The same autonomy availability can therefore arise from substantially
different assurance behaviour.

This demonstrates why autonomy availability must be interpreted together
with intervention correctness.

---

## 19. Cumulative Experimental Interpretation

EXP-006 extends the research progression:

### EXP-001 / EXP-002

```text
Divergence quantity alone is insufficient.
```

### EXP-003

```text
Decision dependencies can distinguish relevant from irrelevant divergence.
```

### EXP-004

```text
Decision relevance alone is insufficient.
```

### EXP-005

```text
Decision impact / physical validity provides additional consequence
information.
```

### EXP-006

```text
Impact reasoning is itself constrained by the reliability of runtime
evidence.
```

This produces the developing research chain:

```text
Physical–Digital Divergence
        ↓
Decision Relevance
        ↓
Decision Impact / Validity
        ↓
Evidence Reliability
        ↓
Decision Risk
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

---

## 20. What EXP-006 Supports

Within the controlled 12-condition capacity experiment, EXP-006 supports the
following observations:

- decision-impact reasoning depends on the evidence used to estimate physical
  state;
- explicit missing, stale and conflicting evidence can be handled
  conservatively;
- available but incorrect evidence can still produce missed intervention;
- pessimistic evidence can produce unnecessary intervention;
- evidence-aware impact does not reproduce the perfect result of a
  perfect-evidence baseline;
- evidence reliability affects both assurance correctness and autonomous
  authority; and
- autonomy availability alone is insufficient for comparing assurance
  policies.

---

## 21. What EXP-006 Does Not Establish

EXP-006 does **not** establish:

- general robustness to sensor failure;
- general evidence-quality estimation;
- probabilistic sensor fusion;
- optimal handling of conflicting evidence;
- generalisation beyond capacity;
- generalisation to arbitrary Digital Twin architectures;
- statistical real-world reliability;
- formal safety guarantees;
- real-time scalability;
- superiority over established runtime-assurance approaches; or
- confirmed novelty of the overall DARA-DT framework.

---

## 22. Threats to Validity

### 22.1 Controlled Evidence Errors

Evidence conditions are deliberately constructed.

Real telemetry failures may be correlated, time-dependent and more complex.

### 22.2 Capacity-Centric Evaluation

The experiment continues to use vehicle capacity.

Results cannot automatically be generalised to:

- operational status;
- availability;
- location; or
- other decision dependencies.

### 22.3 Simplified Evidence Representation

Evidence quality is represented using controlled values and explicit status
conditions.

Real evidence systems may require probabilistic confidence, provenance,
sensor redundancy or source-specific trust models.

### 22.4 Deterministic Ground Truth

Physical state is known exactly to the experimental evaluator.

This is appropriate for controlled validation but does not represent the
information available to a deployed assurance system.

### 22.5 Limited Experimental Scale

The experiment contains 12 controlled conditions.

The resulting metrics should therefore be interpreted descriptively rather
than as broad statistical estimates.

---

## 23. Falsification Perspective

The evidence-aware assurance hypothesis should be weakened or revised if
future evaluation demonstrates that:

- evidence-aware reasoning does not outperform simpler conservative
  intervention strategies;
- missed interventions remain unacceptably frequent;
- the mechanism depends on unrealistic evidence metadata;
- performance collapses across different dependency types;
- evidence-quality reasoning introduces unacceptable computational overhead;
  or
- autonomy preservation provides little operational benefit.

Negative results should remain part of the research evidence.

---

## 24. Reproducibility

Key EXP-006 implementation components include:

```text
src/dara_dt/evidence/model.py
src/dara_dt/evidence/generator.py
src/dara_dt/assurance/evidence_policy.py
src/dara_dt/experiments/evidence_conditions.py
src/dara_dt/experiments/evidence_experiment.py
src/dara_dt/experiments/evidence_metrics.py
```

The aggregate experiment can be reproduced using:

```bash
uv run python -m dara_dt.experiments.evidence_metrics
```

The repository's automated test workflow validates the supporting
implementation.

At the latest verified experimental checkpoint, the repository test suite
completed:

```text
275 passed
```

The experiment and test workflow should continue to be rerun whenever the
implementation changes.

---

## 25. Research Integrity

EXP-006 deliberately retains its imperfect result.

The evidence-aware policy does **not** achieve 100% accuracy.

It produces:

```text
1 false intervention
1 missed intervention
```

These errors are not removed or hidden because they identify important
limitations of runtime assurance under imperfect information.

The result therefore provides a stronger basis for subsequent research than
artificially constructing conditions in which the proposed policy always
wins.

---

## 26. Next Scientific Question

The strongest decision-impact and evidence-reliability experiments currently
remain concentrated on vehicle capacity.

Before introducing substantially more complex evidence models, the research
should test whether the underlying mechanism generalises across different
decision dependencies.

The next proposed question is:

> **Does the relationship between divergence, decision relevance, decision
> impact and runtime intervention generalise across different logistics
> decision dependencies?**

Candidate dependency families are:

```text
Capacity
Operational Status
Location / Availability
```

This forms the basis of the proposed EXP-007.

---

## 27. Conclusion

EXP-006 demonstrates that decision-impact reasoning cannot be separated from
the reliability of the evidence used to estimate physical reality.

Within the controlled 12-condition experiment, deterministic impact reasoning
with reliable evidence achieves perfect classification, while the
evidence-aware policy operating under imperfect evidence produces:

```text
Accuracy  = 0.833
Precision = 0.889
Recall    = 0.889
FI        = 1
MI        = 1
Autonomy  = 0.250
```

The imperfect result reveals two important assurance risks:

```text
Incorrect optimistic evidence
        ↓
Missed intervention

Incorrect pessimistic evidence
        ↓
False intervention
```

The experiment therefore advances DARA-DT from the question:

> Does this divergence invalidate the decision?

to the more difficult question:

> **How confidently can the assurance mechanism determine whether the
> divergence invalidates the decision when its view of physical reality may
> itself be imperfect?**

This establishes evidence reliability as a necessary part of the developing
DARA-DT runtime-assurance model.
