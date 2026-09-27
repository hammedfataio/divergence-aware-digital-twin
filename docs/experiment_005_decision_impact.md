# Experiment 005 — Decision-Impact-Aware Runtime Assurance

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-005  
**Status:** Completed — Controlled Proof-of-Concept  
**Research Stage:** Decision Relevance → Decision Impact / Validity  
**Domain:** Autonomous Logistics Digital Twin

---

## 1. Purpose

EXP-004 demonstrated an important limitation of relevance-only runtime
assurance:

> A physical–digital divergence can affect a variable required by an
> autonomous decision without making that decision physically invalid.

EXP-005 therefore investigates whether runtime assurance can become more
selective by evaluating the **impact of divergence on the validity of the
specific decision**, rather than intervening whenever relevant divergence is
detected.

The experiment focuses on vehicle-capacity decisions because capacity
provides a transparent physical-validity boundary that can be independently
evaluated.

---

## 2. Research Question

> **Can decision-specific impact and validity reasoning distinguish
> consequential physical–digital divergence from relevant but
> non-invalidating divergence?**

The experiment tests whether decision-impact information provides additional
assurance value beyond:

- no assurance;
- global divergence detection;
- fixed divergence magnitude; and
- decision relevance alone.

---

## 3. Working Hypothesis

The working hypothesis is:

> **Runtime intervention can become more selective when relevant divergence
> is evaluated relative to the physical validity requirements of the
> specific decision.**

For a capacity-dependent vehicle assignment, the important question is not
simply:

```text
Is physical capacity different from Twin capacity?
```

or:

```text
Is capacity relevant to this decision?
```

but:

```text
Does the observed physical capacity still satisfy the demand required by
this particular assignment?
```

---

## 4. Experimental Principle

For a vehicle-assignment decision with demand \(q\), physical validity is
defined independently as:

\[
C_{physical} \geq q
\]

where:

- \(C_{physical}\) is physical vehicle capacity; and
- \(q\) is the demand required by the order.

The decision is physically invalid when:

\[
C_{physical} < q
\]

A useful validity margin can therefore be represented as:

\[
M = C_{physical} - q
\]

where:

- \(M > 0\): positive feasibility margin;
- \(M = 0\): exact physical boundary;
- \(M < 0\): physically invalid assignment.

This formulation makes impact decision-specific.

---

## 5. Why Divergence Magnitude Is Not Enough

Consider two decisions with identical physical–digital divergence:

```text
Twin capacity     = 10
Physical capacity = 7
Divergence        = 3
```

### Decision A

```text
Demand = 5

7 >= 5
```

The decision remains physically valid.

### Decision B

```text
Demand = 8

7 < 8
```

The decision is physically invalid.

Therefore:

> **Equal divergence magnitude can produce different decision consequences.**

This comparison directly motivates decision-impact reasoning.

---

## 6. Controlled Experimental Matrix

EXP-005 evaluates **15 controlled capacity conditions**.

The conditions vary:

- Twin capacity;
- physical capacity;
- order demand;
- divergence magnitude; and
- resulting physical validity.

The matrix deliberately includes:

- synchronized conditions;
- divergent but valid decisions;
- divergent and invalid decisions;
- different validity margins;
- equal-divergence/different-impact comparisons; and
- exact-boundary conditions.

The purpose is not to simulate the entire logistics domain.

It is to isolate whether decision-specific validity information improves
runtime intervention decisions.

---

## 7. Important Equal-Divergence Pair

A particularly important comparison is I7 versus I8.

Both conditions use:

```text
Twin capacity     = 10
Physical capacity = 7
Divergence        = 3
```

### I7

```text
Demand = 5

Physical capacity = 7
Demand            = 5

7 >= 5
```

The assignment is physically valid.

### I8

```text
Demand = 8

Physical capacity = 7
Demand            = 8

7 < 8
```

The assignment is physically invalid.

The physical–digital divergence is identical.

The decision consequence is not.

This pair isolates the distinction between:

```text
Divergence magnitude
```

and:

```text
Decision impact
```

---

## 8. Assurance Strategies

Five strategies are evaluated.

### B0 — No Assurance

The decision is allowed without runtime intervention.

This maximises autonomy but does not respond to invalid decisions caused by
physical–digital divergence.

---

### B1 — Global Divergence

Any detected physical–digital divergence triggers intervention.

This provides high sensitivity to mismatch but does not distinguish
decision consequence.

---

### B2 — Fixed-Magnitude Assurance

Intervention is determined using a fixed divergence-magnitude threshold.

This tests whether a simple severity rule can approximate the physical
validity boundary.

---

### B3 — Decision-Relevance Assurance

Intervention occurs when detected divergence affects a dependency of the
current decision.

This represents the relevance mechanism developed in EXP-001 to EXP-003.

EXP-004 demonstrated that relevance alone may over-intervene.

---

### P1 — Decision-Impact Assurance

The decision-impact mechanism evaluates the relationship between:

- the decision dependency;
- required demand; and
- evidence about physical capacity.

The purpose is to determine whether divergence crosses the decision's
validity boundary rather than merely whether divergence exists.

For EXP-005, the impact mechanism uses deterministic physical-capacity
evidence.

This represents an intentionally controlled setting.

The assumption of reliable evidence is challenged later in EXP-006.

---

## 9. Evaluation Outcomes

Each policy outcome is evaluated against independent physical ground truth.

Four outcome classes are used.

### True Intervention — TI

```text
Decision physically invalid
+
Policy intervenes
```

### False Intervention — FI

```text
Decision physically valid
+
Policy intervenes
```

### Missed Intervention — MI

```text
Decision physically invalid
+
Policy allows execution
```

### Correct Non-Intervention — CNI

```text
Decision physically valid
+
Policy allows execution
```

This separation prevents an assurance policy from defining its own
evaluation labels.

---

## 10. Verified Aggregate Results

The implemented 15-condition experiment produces the following results:

| Policy | Conditions | TI | FI | MI | CNI | Accuracy | Precision | Recall | Autonomy Availability |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 15 | 0 | 0 | 6 | 9 | 0.600 | 0.000 | 0.000 | 1.000 |
| Global Divergence | 15 | 6 | 8 | 0 | 1 | 0.467 | 0.429 | 1.000 | 0.067 |
| Fixed Magnitude | 15 | 3 | 0 | 3 | 9 | 0.800 | 1.000 | 0.500 | 0.800 |
| Decision Relevance | 15 | 6 | 8 | 0 | 1 | 0.467 | 0.429 | 1.000 | 0.067 |
| Decision Impact | 15 | 6 | 2 | 0 | 7 | 0.867 | 0.750 | 1.000 | 0.467 |

These values describe only the controlled EXP-005 matrix.

They should not be interpreted as general system-performance estimates.

---

## 11. No-Assurance Result

No Assurance allows every decision.

This produces:

```text
TI  = 0
FI  = 0
MI  = 6
CNI = 9
```

with:

```text
Accuracy = 0.600
Recall   = 0.000
Autonomy = 1.000
```

The policy preserves complete autonomy but misses all six physically invalid
decisions.

This illustrates why autonomy availability cannot be interpreted as an
assurance-quality metric by itself.

---

## 12. Global-Divergence Result

Global Divergence produces:

```text
TI  = 6
FI  = 8
MI  = 0
CNI = 1
```

with:

```text
Accuracy  = 0.467
Precision = 0.429
Recall    = 1.000
Autonomy  = 0.067
```

The policy catches all physically invalid decisions but unnecessarily
intervenes in eight valid conditions.

This demonstrates the opposite extreme from No Assurance.

High intervention recall is achieved at substantial cost to autonomous
availability.

---

## 13. Fixed-Magnitude Result

Fixed Magnitude produces:

```text
TI  = 3
FI  = 0
MI  = 3
CNI = 9
```

with:

```text
Accuracy  = 0.800
Precision = 1.000
Recall    = 0.500
Autonomy  = 0.800
```

The threshold is selective and avoids false intervention in this matrix.

However, it misses half of the physically invalid conditions.

The result demonstrates that a simple threshold can preserve autonomy but
may fail when the same divergence magnitude has different consequences under
different decision requirements.

---

## 14. Decision-Relevance Result

Decision Relevance produces:

```text
TI  = 6
FI  = 8
MI  = 0
CNI = 1
```

with:

```text
Accuracy  = 0.467
Precision = 0.429
Recall    = 1.000
Autonomy  = 0.067
```

Within this capacity-focused matrix, nearly every divergence concerns the
capacity dependency of the current decision.

The relevance mechanism therefore correctly identifies the divergence as
decision-relevant but cannot determine whether the remaining physical
capacity is still sufficient for the order.

This confirms the limitation exposed by EXP-004:

> **Decision relevance identifies what matters to the decision, but does not
> necessarily determine whether the decision remains valid.**

---

## 15. Decision-Impact Result

Decision Impact produces:

```text
TI  = 6
FI  = 2
MI  = 0
CNI = 7
```

with:

```text
Accuracy  = 0.867
Precision = 0.750
Recall    = 1.000
Autonomy  = 0.467
```

Within the controlled matrix, decision-impact reasoning:

- intervenes in all six physically invalid conditions;
- avoids six of the eight false interventions produced by relevance-only
  assurance;
- preserves substantially more autonomous execution than global or
  relevance-only intervention; and
- still produces two false interventions.

The result therefore supports the usefulness of decision-specific validity
reasoning without suggesting that the implemented policy is perfect.

---

## 16. Boundary Behaviour

The two false interventions produced by the decision-impact policy are
important.

They occur at exact-boundary conditions where:

```text
physical capacity = demand
```

The independent physical validator treats equality as physically valid:

\[
C_{physical} \geq q
\]

However, the impact policy treats the zero-margin boundary conservatively.

Therefore:

```text
Ground truth:
margin = 0 → valid

Impact policy:
margin = 0 → restrict
```

This produces a false intervention.

This should not be hidden or manually corrected merely to improve the
reported metric.

Instead, it identifies a genuine policy-design question:

> Should an autonomous system retain full authority when a decision is
> exactly feasible but has no remaining physical margin?

The answer may depend on the operational risk model and cannot be resolved by
this experiment alone.

---

## 17. Scientific Interpretation

EXP-005 provides controlled evidence that the following concepts should be
distinguished:

```text
Physical–Digital Divergence
        ↓
How different are physical and digital state?

Decision Relevance
        ↓
Does the mismatch affect something this decision depends on?

Decision Impact
        ↓
Does the mismatch change whether this decision remains physically valid?
```

This is more informative than treating all three questions as equivalent.

---

## 18. Assurance–Autonomy Trade-Off

The experiment also illustrates the trade-off between intervention
sensitivity and autonomy preservation.

### No Assurance

```text
Autonomy = 1.000
Recall   = 0.000
```

Maximum autonomy, but all required interventions are missed.

### Global / Relevance

```text
Autonomy = 0.067
Recall   = 1.000
```

All invalid conditions are caught, but autonomy is almost completely
removed.

### Fixed Magnitude

```text
Autonomy = 0.800
Recall   = 0.500
```

Greater autonomy, but half of the required interventions are missed.

### Decision Impact

```text
Autonomy = 0.467
Recall   = 1.000
```

Within this controlled matrix, decision-impact reasoning preserves more
autonomy than global/relevance-only intervention while retaining all required
interventions.

This does not establish an optimal trade-off.

It demonstrates why both assurance effectiveness and autonomy preservation
must be measured.

---

## 19. Relationship to EXP-004

EXP-004 established:

```text
Relevant divergence ≠ Invalid decision
```

EXP-005 operationalises the next question:

```text
If divergence is relevant,
does it cross the validity boundary of this specific decision?
```

The resulting progression is:

```text
Decision Relevance
        ↓
Divergence Severity
        ↓
Decision Impact / Validity
```

---

## 20. Limitation Exposed by EXP-005

The decision-impact mechanism in EXP-005 uses reliable evidence about
physical capacity.

That creates another important assumption:

```text
Impact reasoning
        ↓
requires evidence about physical reality
```

But deployed Digital Twins may receive:

- delayed evidence;
- missing observations;
- noisy measurements;
- conflicting observations; or
- incorrect but apparently valid telemetry.

Therefore a decision-impact mechanism may reason correctly from incorrect
evidence.

This motivates EXP-006.

---

## 21. Connection to EXP-006

EXP-006 asks:

> **How robust is decision-impact-aware runtime assurance when the evidence
> used to estimate physical–digital divergence and decision impact is
> imperfect?**

The progression becomes:

```text
EXP-003
Decision relevance
        ↓
EXP-004
Relevance is insufficient
        ↓
EXP-005
Decision impact / validity
        ↓
EXP-006
Reliability of the evidence supporting impact
```

This advances the DARA-DT research model to:

```text
Physical–Digital Divergence
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

---

## 22. What EXP-005 Supports

Within the controlled 15-condition capacity matrix, EXP-005 supports the
following observations:

- equal divergence magnitude can produce different decision consequences;
- decision relevance alone does not distinguish valid from invalid
  capacity-dependent assignments;
- fixed magnitude can preserve autonomy while missing invalid decisions;
- decision-specific validity reasoning can reduce unnecessary intervention
  relative to global and relevance-only policies;
- decision-impact reasoning retained intervention across all six physically
  invalid conditions in this matrix; and
- exact validity boundaries create an explicit policy-design problem.

---

## 23. What EXP-005 Does Not Establish

EXP-005 does **not** establish:

- general superiority of decision-impact assurance;
- general superiority of DARA-DT;
- effectiveness outside capacity-dependent decisions;
- effectiveness under imperfect evidence;
- an optimal treatment of exact validity boundaries;
- statistical generalisation;
- real-world logistics effectiveness;
- robustness under compound divergence;
- acceptable computational overhead;
- formal safety guarantees; or
- confirmed novelty.

These remain subjects for further investigation.

---

## 24. Threats to Validity

### 24.1 Capacity-Centric Evaluation

The experiment focuses on a numeric capacity dependency.

The observed behaviour may not transfer directly to categorical or spatial
dependencies such as:

- operational status;
- availability; or
- location.

---

### 24.2 Deterministic Evidence

The impact mechanism receives controlled evidence about physical capacity.

This simplifies causal interpretation but does not represent all real
runtime evidence conditions.

---

### 24.3 Simplified Validity Function

Physical validity is based on the transparent constraint:

```text
capacity >= demand
```

Real logistics decisions may involve multiple interacting constraints and
objectives.

---

### 24.4 Controlled Experimental Matrix

The 15 conditions are deliberately constructed.

The resulting metrics describe this matrix and should not be interpreted as
population-level performance estimates.

---

### 24.5 Boundary Policy

The treatment of zero validity margin is conservative in the impact policy
but valid under the independent physical ground-truth rule.

This policy mismatch accounts for two false interventions and requires
further investigation rather than silent removal.

---

## 25. Falsification Perspective

The decision-impact hypothesis would be weakened if broader experiments show
that:

- impact reasoning provides no advantage over simpler thresholds;
- the observed benefit exists only for capacity;
- impact estimates become unreliable under realistic evidence conditions;
- missed interventions increase substantially;
- autonomy gains disappear under broader scenarios; or
- the computational cost of impact reasoning outweighs its assurance value.

The purpose of subsequent experiments is therefore to challenge the mechanism
under increasingly difficult conditions.

---

## 26. Reproducibility

The decision-impact experiment is implemented through the repository's
impact experiment and evaluation modules.

Key experimental components include:

```text
src/dara_dt/experiments/impact_experiment.py
src/dara_dt/experiments/impact_metrics.py
src/dara_dt/impact/model.py
src/dara_dt/impact/analyser.py
src/dara_dt/assurance/impact_policy.py
```

The aggregate metrics can be reproduced through the repository experiment
runner:

```bash
uv run python -m dara_dt.experiments.impact_metrics
```

Automated tests verify the controlled conditions, impact calculations,
assurance outcomes and aggregate metrics.

---

## 27. Research Integrity

The experiment does not modify the baseline policies to make DARA-DT appear
superior.

In particular:

- relevance-only assurance is preserved as an intentionally incomplete
  baseline;
- the fixed-magnitude policy is retained even where it performs well;
- the two decision-impact false interventions are retained;
- exact-boundary behaviour is explicitly documented; and
- conclusions are limited to the controlled capacity matrix.

This allows later experiments to test whether the observed mechanism
generalises.

---

## 28. Conclusion

EXP-005 demonstrates that physical–digital divergence should not be
interpreted independently of the decision it affects.

Within the controlled capacity matrix, the same divergence magnitude can
leave one vehicle-assignment decision valid while invalidating another.

Decision-impact reasoning therefore provides information that is absent from
divergence magnitude and decision relevance alone.

The experiment supports the transition:

```text
Physical–Digital Divergence
        ↓
Decision Relevance
        ↓
Decision Impact / Validity
```

However, EXP-005 relies on reliable evidence about physical state.

The next experiment therefore asks whether the same reasoning remains
dependable when runtime evidence is incomplete, stale, conflicting or
incorrect.

That question is investigated in EXP-006.
