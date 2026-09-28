# Experiment 007 — Cross-Dependency Generalisation

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-007  
**Status:** Complete  
**Research Stage:** Cross-Dependency Generalisation and Runtime-Contract Comparison

---

## 1. Objective

The objective of EXP-007 is to test whether the relationship between
physical–digital divergence, decision relevance, decision impact, and runtime
intervention generalises beyond vehicle-capacity decisions.

Earlier experiments established that:

- global Digital Twin divergence can cause unnecessary intervention;
- decision relevance can distinguish relevant from irrelevant divergence;
- relevance alone does not determine whether a decision remains physically valid;
- decision impact can distinguish relevant-but-valid changes from changes that
  invalidate an AI-generated decision.

EXP-007 extends this reasoning across multiple logistics decision dependencies
and compares the decision-impact mechanism against a strong runtime-contract
baseline.

---

## 2. Research Question

> **Does the relationship between physical–digital divergence, decision
> relevance, decision impact, and runtime intervention generalise across
> different logistics decision dependencies?**

A secondary comparison asks:

> **Does decision-conditioned physical–digital divergence provide different
> intervention behaviour from direct runtime-contract checking when reliable
> runtime evidence is available?**

---

## 3. Dependency Families

Three dependency families were evaluated:

1. **Capacity**
2. **Operational Status**
3. **Location / Availability**

Each family contains four controlled conditions.

---

## 4. Experimental Structure

The experiment uses the following conceptual condition structure:

| Condition | Description |
|---|---|
| C0 | No relevant physical–digital divergence |
| C1 | Divergence exists but is irrelevant to the selected decision |
| C2 | Divergence is decision-relevant but the decision remains physically valid |
| C3 | Divergence is decision-relevant and physically invalidates the decision |

This produces a total of:

\[
3 \text{ dependency families} \times 4 \text{ conditions} = 12 \text{ conditions}
\]

The experiment uses controlled deterministic proposed decisions so that the
assurance mechanisms evaluate the same decision across all conditions.

This separates **decision generation** from **runtime assurance evaluation**.

---

## 5. Policies Compared

Five assurance configurations were evaluated.

### P0 — No Assurance

The proposed decision is allowed regardless of detected divergence.

### P1 — Global Divergence

Any detected physical–digital divergence triggers intervention.

### P2 — Decision Relevance

Intervention occurs when divergence affects a dependency of the proposed
decision.

### P3 — Decision Impact

Relevant divergence is evaluated relative to the physical validity of the
specific decision.

The mechanism distinguishes:

- no impact;
- reduced decision margin;
- decision-invalidating impact.

### P4 — Runtime Contract

A direct runtime contract evaluates whether the observed physical state
satisfies the operational requirement of the proposed decision.

Examples include:

- capacity must satisfy demand;
- vehicle status must satisfy the required operational state;
- vehicle location must be permitted;
- vehicle availability must satisfy dispatch requirements.

This provides a strong comparator because it can determine decision validity
without explicitly executing the complete divergence → relevance → impact
reasoning chain.

---

## 6. Ground Truth

Ground truth is derived independently from the physical system state.

A decision is classified as:

- **DO_NOT_INTERVENE** when the proposed action remains physically valid;
- **INTERVENE** when the proposed action is physically invalid.

Ground truth is not derived from:

- Digital Twin state;
- detected divergence;
- decision relevance;
- decision impact;
- assurance-policy output.

This separation prevents the assurance mechanism from defining its own
evaluation target.

---

## 7. Experimental Results

### 7.1 Condition-Level Results

| Condition | Ground Truth | Divergence | Relevant Divergence | Impact | No Assurance | Global Divergence | Decision Relevance | Decision Impact | Runtime Contract |
|---|---|---:|---:|---|---|---|---|---|---|
| CAP-0 | Do Not Intervene | 0 | 0 | No Impact | CNI | CNI | CNI | CNI | CNI |
| CAP-1 | Do Not Intervene | 1 | 0 | No Impact | CNI | FI | CNI | CNI | CNI |
| CAP-2 | Do Not Intervene | 1 | 1 | Margin Reduced | CNI | FI | FI | CNI | CNI |
| CAP-3 | Intervene | 1 | 1 | Invalidating | MI | TI | TI | TI | TI |
| STATUS-0 | Do Not Intervene | 0 | 0 | No Impact | CNI | CNI | CNI | CNI | CNI |
| STATUS-1 | Do Not Intervene | 1 | 0 | No Impact | CNI | FI | CNI | CNI | CNI |
| STATUS-2 | Do Not Intervene | 1 | 1 | Margin Reduced | CNI | FI | FI | CNI | CNI |
| STATUS-3 | Intervene | 1 | 1 | Invalidating | MI | TI | TI | TI | TI |
| LOC-0 | Do Not Intervene | 0 | 0 | No Impact | CNI | CNI | CNI | CNI | CNI |
| LOC-1 | Do Not Intervene | 2 | 0 | No Impact | CNI | FI | CNI | CNI | CNI |
| LOC-2 | Do Not Intervene | 1 | 1 | Margin Reduced | CNI | FI | FI | CNI | CNI |
| LOC-3 | Intervene | 2 | 2 | Invalidating | MI | TI | TI | TI | TI |

Where:

- **TI** = True Intervention
- **FI** = False Intervention
- **MI** = Missed Intervention
- **CNI** = Correct Non-Intervention

---

## 8. Aggregate Results

| Policy | Correct | TI | FI | MI | CNI | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| No Assurance | 9/12 | 0 | 0 | 3 | 9 | 75% |
| Global Divergence | 6/12 | 3 | 6 | 0 | 3 | 50% |
| Decision Relevance | 9/12 | 3 | 3 | 0 | 6 | 75% |
| Decision Impact | 12/12 | 3 | 0 | 0 | 9 | 100% |
| Runtime Contract | 12/12 | 3 | 0 | 0 | 9 | 100% |

These results apply only to the controlled EXP-007 matrix and should not be
interpreted as general real-world performance estimates.

---

## 9. Findings

### 9.1 Global Divergence Is Too Coarse

The global-divergence policy produced six false interventions.

It intervened whenever physical and Digital Twin state differed, regardless of
whether the mismatch affected the proposed decision or changed its physical
validity.

This demonstrates that divergence magnitude or existence alone is insufficient
for selective runtime intervention in this controlled matrix.

---

### 9.2 Decision Relevance Removes Irrelevant Divergence

Decision relevance correctly ignored the irrelevant divergence conditions:

- CAP-1
- STATUS-1
- LOC-1

This demonstrates that conditioning divergence on the dependencies of the
specific decision can reduce unnecessary intervention relative to global
divergence monitoring.

However, relevance alone remained insufficient.

---

### 9.3 Relevant Divergence Does Not Necessarily Invalidate a Decision

The following conditions contained decision-relevant divergence while the
proposed decision remained physically valid:

- CAP-2
- STATUS-2
- LOC-2

The relevance-only policy falsely intervened in all three.

Decision Impact instead classified these conditions as reduced-margin rather
than invalidating and preserved autonomous execution.

This supports the distinction between:

\[
\text{Decision Relevance} \neq \text{Decision Invalidity}
\]

---

### 9.4 Decision-Impact Reasoning Generalised Across the Tested Dependencies

Decision Impact correctly classified all 12 controlled conditions.

The same conceptual progression was observed across:

- capacity;
- operational status;
- location / availability.

Within this bounded experiment, the results therefore support cross-dependency
generalisation of the conceptual chain:

\[
\text{Physical–Digital Divergence}
\rightarrow
\text{Decision Relevance}
\rightarrow
\text{Decision Impact}
\rightarrow
\text{Runtime Intervention}
\]

This is evidence of bounded experimental generalisation, not evidence of
universal generalisation.

---

## 10. Critical Runtime-Contract Result

The Runtime Contract baseline also correctly classified all 12 conditions.

Its intervention outcomes were identical to those of Decision Impact under the
reliable-evidence assumptions of EXP-007.

Therefore:

> **EXP-007 does not demonstrate that decision-impact-aware DARA-DT
> outperforms direct runtime-contract checking.**

This is an important falsification result.

When reliable runtime observations are available and the validity requirement
can be expressed directly as a contract, a simpler runtime-contract mechanism
may be sufficient to determine whether intervention is required.

The experiment therefore does not establish an advantage for the additional
divergence → relevance → impact reasoning chain under these conditions.

---

## 11. Interpretation

EXP-007 provides evidence for two different conclusions.

First, the experiment supports the generalisation of decision-conditioned
divergence reasoning across the three tested dependency families.

Second, it exposes a limitation in the current novelty hypothesis.

The experiment cannot establish that decision-conditioned divergence provides
additional assurance information beyond a strong runtime-contract comparator
when reliable physical evidence is directly available.

This changes the research question from:

> Can DARA-DT determine when divergence invalidates a decision?

to the stronger question:

> **Under what runtime conditions does decision-conditioned physical–digital
> divergence provide assurance information beyond direct runtime-contract
> checking?**

---

## 12. Relationship to EXP-006

EXP-006 demonstrated that runtime evidence may be:

- inaccurate;
- stale;
- missing;
- conflicting;
- misleading.

Under those conditions, direct physical validity is no longer necessarily
observable with certainty.

EXP-007 intentionally removed this complication by using reliable evidence so
that dependency generalisation could be tested independently.

Together, EXP-006 and EXP-007 motivate the next experimental stage:

\[
\text{Imperfect Evidence}
+
\text{Runtime Contracts}
+
\text{Decision-Conditioned Divergence}
\]

The next experiment should therefore investigate whether the two assurance
approaches behave differently when runtime evidence cannot be assumed to be
complete and reliable.

---

## 13. Threats to Validity

EXP-007 remains a controlled experiment.

Important limitations include:

- only three dependency families were evaluated;
- only twelve deterministic conditions were tested;
- proposed decisions were experimentally controlled;
- runtime evidence was assumed reliable;
- the logistics environment remains simplified;
- the experiment does not represent production-scale logistics operations;
- perfect performance in this matrix must not be interpreted as general
  real-world effectiveness.

The results therefore establish bounded experimental behaviour only.

---

## 14. Falsification Outcome

The pre-registered falsification criteria included the possibility that a
simpler runtime contract could perform equivalently to the proposed mechanism.

That condition occurred.

Runtime Contract and Decision Impact both achieved:

- 3 true interventions;
- 0 false interventions;
- 0 missed interventions;
- 9 correct non-interventions;
- 100% accuracy.

Accordingly, the hypothesis that DARA-DT provides superior intervention
decisions to direct runtime contracts under reliable evidence is **not
supported by EXP-007**.

The appropriate response is not to remove or redesign this result, but to test
whether the equivalence persists under more realistic evidence limitations.

---

## 15. Conclusion

EXP-007 extends the decision-relevance and decision-impact framework across
capacity, operational-status, and location/availability dependencies.

The experiment shows that decision relevance is more selective than global
divergence monitoring, while decision impact further distinguishes
relevant-but-valid divergence from decision-invalidating divergence.

However, a strong runtime-contract baseline produced identical intervention
outcomes to Decision Impact under reliable runtime evidence.

The experiment therefore provides bounded evidence for cross-dependency
generalisation while simultaneously narrowing the candidate research
contribution.

The next stage must determine whether decision-conditioned physical–digital
divergence contributes useful assurance information when runtime evidence is
imperfect, incomplete, stale, conflicting, or otherwise uncertain.
