# Experiment 005 — Decision-Impact-Aware Runtime Assurance

**Project:** Divergence-Aware Runtime Assurance for Digital Twins (DARA-DT)  
**Experiment:** EXP-005  
**Status:** Complete — Controlled Proof-of-Concept  
**Research Stage:** Decision-Impact-Aware Runtime Assurance

---

## 1. Objective

EXP-005 investigates whether runtime assurance should respond merely to the
presence or magnitude of physical–digital divergence, or instead consider the
effect of that divergence on the specific AI-generated decision being evaluated.

Earlier experiments established two important observations:

1. global Digital Twin divergence can cause unnecessary intervention when the
   divergent state is unrelated to the current decision; and
2. decision relevance alone is insufficient because a divergence may affect a
   decision-dependent variable without actually invalidating the decision.

EXP-005 therefore introduces an additional reasoning layer:

**Physical–Digital Divergence → Decision Relevance → Decision Impact → Runtime Assurance → Autonomous Authority**

The experiment evaluates whether decision-specific impact information can
reduce unnecessary interventions while still preventing autonomous execution
of invalid decisions.

---

## 2. Research Question

> Can decision-impact-aware runtime assurance reduce unnecessary interventions
> while still preventing autonomous execution when physical–digital divergence
> materially invalidates a logistics decision?

---

## 3. Experimental Hypothesis

The working hypothesis was:

> Decision-impact-aware assurance will reduce false interventions relative to
> relevance-only assurance while preserving intervention when divergence
> invalidates the proposed decision.

This hypothesis is evaluated only within the controlled conditions defined in
EXP-005. The results are not treated as evidence of general superiority across
all Digital Twin or logistics environments.

---

## 4. Experimental Model

The experiment uses vehicle capacity as a controlled decision dependency.

For each condition:

- `C_t` = capacity represented by the Digital Twin
- `C_p` = physical vehicle capacity
- `D` = order demand

The physical decision-validity margin is:

`M_p = C_p - D`

Interpretation:

- `M_p > 0` — positive capacity margin
- `M_p = 0` — exact decision boundary
- `M_p < 0` — physical capacity is insufficient

A key distinction is maintained between **runtime evidence** and
**experimental ground truth**.

The physical validity margin is used by the experimental evaluator to determine
whether intervention was actually required. It is not directly passed to the
assurance policy as an outcome label.

---

## 5. Decision-Impact States

EXP-005 introduces the following impact states:

| Impact State | Interpretation |
|---|---|
| `NO_IMPACT` | Runtime evidence does not reduce the relevant decision margin |
| `MARGIN_REDUCED` | Divergence affects the decision dependency but the estimated margin remains positive |
| `BOUNDARY` | Runtime evidence places the decision exactly at its validity boundary |
| `INVALIDATING` | Runtime evidence indicates that the decision constraint has been violated |
| `UNCERTAIN` | Available runtime evidence is insufficient to establish impact confidently |

The experimental impact-aware policy maps these states to autonomous authority.

`NO_IMPACT` and `MARGIN_REDUCED` permit autonomous execution.

`BOUNDARY` restricts autonomous authority.

`INVALIDATING` and `UNCERTAIN` defer autonomous execution.

---

## 6. Policies Compared

Five assurance strategies were evaluated under the same controlled conditions.

### B0 — No Assurance

The AI-generated decision is allowed to execute without runtime intervention.

### B1 — Global Divergence

Any detected physical–digital divergence triggers intervention.

### B2 — Fixed Magnitude

Intervention is based on a fixed divergence-magnitude threshold.

For EXP-005, the configured threshold is `5`.

### B3 — Decision Relevance

Intervention occurs when detected divergence affects a state variable on which
the current decision depends.

### P1 — Decision-Impact-Aware Assurance

Intervention depends on the estimated effect of the relevant divergence on the
decision-specific validity margin.

---

## 7. Controlled Conditions

EXP-005 evaluates 15 controlled conditions, labelled `I0`–`I14`.

The matrix varies:

- Digital Twin capacity;
- physical capacity;
- order demand;
- divergence magnitude;
- decision-specific validity margin; and
- whether intervention is actually required.

The conditions include:

- synchronised states;
- valid decisions with reduced margins;
- exact decision boundaries;
- invalid decisions;
- different decision boundaries; and
- equal divergence magnitudes producing different decision consequences.

A particularly important pair is:

### I7 — Same Divergence, Valid Decision

- Twin capacity: `10`
- Physical capacity: `7`
- Demand: `5`
- Divergence magnitude: `3`
- Physical margin: `+2`

The divergence is decision-relevant, but the decision remains physically valid.

### I8 — Same Divergence, Invalid Decision

- Twin capacity: `10`
- Physical capacity: `7`
- Demand: `8`
- Divergence magnitude: `3`
- Physical margin: `-1`

The divergence magnitude is identical to I7, but the decision is physically
invalid.

This pair tests whether divergence magnitude alone contains sufficient
information for runtime intervention.

---

## 8. Evaluation Outcomes

Each policy decision is classified into one of four outcome categories.

| Outcome | Meaning |
|---|---|
| True Intervention (TI) | Intervention occurred and was required |
| False Intervention (FI) | Intervention occurred but was unnecessary |
| Missed Intervention (MI) | Intervention was required but did not occur |
| Correct Non-Intervention (CNI) | Autonomous execution was allowed and intervention was unnecessary |

These categories separate unsafe under-intervention from unnecessary
over-intervention.

---

## 9. Evaluation Metrics

The following aggregate metrics are calculated across all 15 conditions.

### Assurance Accuracy

`Accuracy = (TI + CNI) / N`

### Intervention Precision

`Precision = TI / (TI + FI)`

This measures how often an intervention was actually required when the policy
intervened.

### Intervention Recall

`Recall = TI / (TI + MI)`

This measures how many required interventions were successfully identified.

### Autonomy Availability

`Autonomy Availability = (MI + CNI) / N`

This measures the proportion of proposed decisions that remain autonomously
executable.

Autonomy availability is reported alongside assurance metrics because a policy
that intervenes on nearly every decision may achieve high intervention recall
while substantially reducing useful autonomous operation.

---

## 10. Verified Results

The experiment produced the following aggregate results across the 15
controlled conditions.

| Policy | TI | FI | MI | CNI | Accuracy | Precision | Recall | Autonomy Availability |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 6 | 9 | 0.600 | 0.000 | 0.000 | 1.000 |
| Global Divergence | 6 | 8 | 0 | 1 | 0.467 | 0.429 | 1.000 | 0.067 |
| Fixed Magnitude | 3 | 0 | 3 | 9 | 0.800 | 1.000 | 0.500 | 0.800 |
| Decision Relevance | 6 | 8 | 0 | 1 | 0.467 | 0.429 | 1.000 | 0.067 |
| Decision Impact | 6 | 2 | 0 | 7 | 0.867 | 0.750 | 1.000 | 0.467 |

The implementation and metric calculations were validated by the repository
test suite before these results were interpreted.

---

## 11. Result Analysis

### 11.1 No Assurance

The no-assurance baseline retained full autonomy availability:

`1.000`

However, it missed all six conditions requiring intervention:

- TI = `0`
- MI = `6`
- Recall = `0.000`

This demonstrates the unsafe behaviour expected from unrestricted autonomous
execution under the controlled divergence conditions.

---

### 11.2 Global Divergence

Global-divergence assurance identified all six required interventions:

- TI = `6`
- MI = `0`
- Recall = `1.000`

However, it also produced eight false interventions:

- FI = `8`
- Precision = `0.429`

Autonomy availability fell to:

`0.067`

Within this experimental matrix, reacting to any divergence therefore produced
substantial over-intervention.

---

### 11.3 Fixed-Magnitude Assurance

The fixed-magnitude baseline produced:

- TI = `3`
- FI = `0`
- MI = `3`
- CNI = `9`

Its intervention precision was:

`1.000`

but recall was:

`0.500`

The threshold therefore avoided unnecessary interventions in this matrix but
failed to identify half of the required interventions.

The I7/I8 pair illustrates the underlying limitation: equal divergence
magnitude can correspond to different decision consequences.

A fixed magnitude alone cannot represent that distinction without additional
decision context.

---

### 11.4 Decision-Relevance Assurance

Decision-relevance assurance identified all six required interventions:

- TI = `6`
- MI = `0`
- Recall = `1.000`

However, it also produced eight false interventions:

- FI = `8`
- Precision = `0.429`
- Autonomy availability = `0.067`

Within this capacity-focused experiment, all introduced capacity divergences
were relevant to the vehicle-assignment decision.

Relevance therefore established that the changed state mattered to the
decision dependency, but it did not establish whether the change was large
enough to invalidate the decision.

This confirms the limitation exposed by EXP-004:

> Decision relevance is necessary for filtering unrelated divergence, but
> relevance alone is not sufficient for determining whether autonomous
> execution should be interrupted.

---

### 11.5 Decision-Impact-Aware Assurance

The decision-impact policy produced:

- TI = `6`
- FI = `2`
- MI = `0`
- CNI = `7`

This corresponds to:

- Accuracy = `0.867`
- Precision = `0.750`
- Recall = `1.000`
- Autonomy availability = `0.467`

Within the controlled EXP-005 matrix, the policy preserved intervention on all
six invalid decisions while reducing false interventions from eight under the
relevance-only policy to two.

The experiment therefore provides preliminary evidence that decision-specific
impact information can improve the balance between intervention and autonomy
relative to relevance-only reasoning.

This conclusion is restricted to the controlled capacity scenarios evaluated
here.

---

## 12. The Remaining False Interventions

The decision-impact policy still produced two false interventions.

These results are important and are not treated as implementation noise.

The current policy classifies an exact decision boundary as requiring
restricted autonomous authority.

However, the experimental ground-truth definition treats:

`C_p = D`

as physically valid.

Consequently, exact-boundary conditions can produce conservative
interventions even though the physical decision remains technically feasible.

This exposes a distinction between:

- **physical validity**, and
- **operational safety margin**.

A decision may be technically valid at a zero margin while still offering no
buffer against uncertainty, measurement error, or further system change.

The appropriate treatment of such boundary states therefore requires further
investigation rather than simply modifying the policy to eliminate the false
interventions.

---

## 13. Key Finding

The principal finding of EXP-005 is:

> Within the controlled capacity experiment, divergence magnitude and decision
> relevance alone were insufficient to determine whether autonomous
> intervention was appropriate. Incorporating decision-specific impact
> information reduced unnecessary intervention while preserving intervention
> on invalid decisions.

The result supports the evolving DARA-DT reasoning chain:

**Physical–Digital Divergence  
→ Decision Relevance  
→ Decision Impact / Validity Margin  
→ Runtime Assurance  
→ Autonomous Authority**

This is a controlled proof-of-concept result, not evidence that the proposed
approach is universally superior to existing runtime-assurance methods.

---

## 14. Scientific Interpretation

EXP-005 distinguishes three questions that should not be treated as
equivalent:

1. **Has the physical system diverged from its Digital Twin?**
2. **Does that divergence affect a variable used by the current decision?**
3. **Does the divergence materially alter the validity of that decision?**

The experiment demonstrates that the answer to question 2 can be "yes" while
the answer to question 3 remains "no".

Similarly, two conditions can have the same divergence magnitude while
producing different answers to question 3.

This distinction motivates decision-impact reasoning as a separate experimental
component of DARA-DT.

---

## 15. Limitations

EXP-005 remains deliberately narrow.

### 15.1 Capacity-Only Decision Dependency

The current experiment evaluates capacity divergence only.

The findings have not yet been demonstrated for:

- vehicle operational status;
- availability;
- location;
- temporal staleness;
- route feasibility;
- demand uncertainty; or
- compound divergence.

### 15.2 High-Quality Runtime Evidence

The impact analyser receives a runtime capacity observation corresponding to
the physical capacity used in the controlled simulation.

Although the experimental evaluator remains logically separate from the
assurance policy, this represents a strong runtime-information assumption.

Real systems may contain:

- sensor noise;
- delayed observations;
- missing observations;
- contradictory evidence; or
- uncertain state estimates.

The current result therefore does not establish performance under imperfect
runtime evidence.

### 15.3 Small Controlled Matrix

Only 15 deterministic conditions are evaluated.

The matrix is designed for mechanism testing and falsification, not statistical
generalisation.

### 15.4 Boundary Policy

The treatment of zero-margin decisions remains conservative and causes two
false interventions.

This behaviour requires explicit investigation rather than post-hoc adjustment.

### 15.5 Scenario Weighting

Some conditions intentionally reuse similar capacity configurations to test
specific contrasts, including the equal-divergence comparison.

Aggregate metrics should therefore be interpreted as performance over the
designed experimental matrix rather than as estimates of real-world event
frequency.

---

## 16. Threats to Validity

Several competing explanations remain possible.

The observed improvement may depend on:

- direct access to high-quality runtime capacity evidence;
- the simplicity of a single numeric constraint;
- deterministic decision boundaries;
- the selected distribution of experimental conditions; or
- the absence of interacting divergence sources.

Decision-impact reasoning must therefore be challenged under weaker evidence
and more complex dependencies before stronger conclusions are justified.

---

## 17. Falsification Criteria

The decision-impact approach should be weakened or rejected if subsequent
experiments show that it:

- misses materially invalid decisions;
- performs no better than relevance-only reasoning under imperfect evidence;
- collapses into a tuned global magnitude threshold;
- fails when the decision boundary changes;
- fails on non-capacity dependencies;
- cannot handle multiple interacting divergences; or
- introduces unacceptable runtime overhead.

These criteria are retained explicitly to avoid treating favourable EXP-005
results as confirmation of the overall research hypothesis.

---

## 18. Next Experiment

The immediate next experiment should challenge one of EXP-005's strongest
assumptions:

**perfect runtime evidence.**

EXP-006 should therefore investigate decision-impact-aware assurance under:

- noisy observations;
- delayed observations;
- missing evidence; and
- uncertain evidence.

The central question becomes:

> Can decision-impact-aware runtime assurance preserve useful intervention
> behaviour when the evidence used to estimate decision impact is itself
> imperfect?

This provides a stronger test of whether the framework can move beyond a
deterministic proof-of-concept toward realistic runtime assurance.

---

## 19. Reproducibility

The EXP-005 implementation is contained within the repository and includes:

- controlled impact conditions;
- decision-impact models;
- impact analysis;
- assurance policies;
- policy comparison;
- aggregate metric calculation; and
- automated tests.

The complete repository test suite passed after integration of EXP-005 and its
metric evaluation.

No result in this document should be interpreted beyond the experimental scope
described above.

---

## 20. Experiment Status

**EXP-005: COMPLETE — CONTROLLED PROOF-OF-CONCEPT**

Supported within the current experiment:

- decision relevance alone can over-intervene;
- equal divergence magnitude can have different decision consequences;
- decision-specific validity margins provide additional information beyond
  divergence magnitude;
- impact-aware assurance reduced false interventions relative to
  relevance-only assurance in the controlled matrix;
- all required interventions were retained by the impact-aware policy in the
  tested conditions; and
- exact-boundary handling remains an unresolved assurance-design question.

Not yet established:

- robustness to imperfect runtime evidence;
- generalisation beyond capacity;
- performance under compound divergence;
- scalability;
- real-world logistics effectiveness; or
- novelty relative to all existing runtime-assurance approaches.
