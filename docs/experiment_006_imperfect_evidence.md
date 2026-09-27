# Experiment 006 — Runtime Assurance Under Imperfect Evidence

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-006  
**Status:** COMPLETE  
**Research Stage:** Imperfect Runtime Evidence  
**Domain:** Autonomous Logistics Digital Twins

---

## 1. Objective

EXP-006 evaluates whether decision-impact-aware runtime assurance remains
effective when the runtime evidence used to assess physical–digital
divergence is imperfect.

Earlier experiments progressively established that:

- physical–digital divergence can affect AI-generated logistics decisions;
- global divergence alone is too coarse for deciding when autonomous
  intervention is necessary;
- decision relevance provides a more targeted assurance signal;
- decision relevance alone is still insufficient because a relevant
  divergence may not invalidate the current decision;
- decision-specific impact and validity margins can improve intervention
  decisions under controlled conditions.

EXP-005 demonstrated the value of decision-impact reasoning under an
idealised assumption: the assurance mechanism received accurate runtime
evidence about physical capacity.

EXP-006 deliberately removes that assumption.

The experiment separates three concepts:

> **Physical Ground Truth ≠ Runtime Evidence ≠ Digital Twin State**

This distinction is critical because a runtime assurance mechanism cannot
normally assume direct access to perfect physical ground truth.

---

## 2. Research Question

EXP-006 investigates:

> **How robust is decision-impact-aware runtime assurance when the evidence
> used to estimate physical–digital divergence and decision impact is
> imperfect?**

The experiment specifically examines whether evidence errors can cause an
assurance mechanism to:

1. permit an invalid autonomous decision;
2. unnecessarily intervene on a valid decision;
3. preserve correct intervention behaviour;
4. preserve autonomous execution when intervention is unnecessary.

---

## 3. Experimental Motivation

A Digital Twin may contain an inaccurate representation of the physical
system.

However, runtime assurance introduces an additional problem.

Even if the assurance mechanism attempts to verify the Digital Twin against
the physical system, the evidence used for verification may itself be:

- noisy;
- stale;
- missing;
- conflicting;
- incomplete; or
- misleading near a decision-validity boundary.

Therefore, detecting divergence is not sufficient.

The reliability and decision consequence of runtime evidence must also be
considered.

---

## 4. Experimental Separation

EXP-006 maintains a strict separation between three information layers.

### 4.1 Physical Ground Truth

The physical logistics environment defines the actual state of the vehicle
and determines whether the AI-generated decision is physically valid.

Physical ground truth is used only for independent experimental evaluation.

It is not supplied directly to the evidence-aware assurance policy.

### 4.2 Digital Twin State

The Digital Twin represents the state available to the AI decision
controller.

The AI therefore generates its decision from the Twin representation rather
than directly from the physical environment.

### 4.3 Runtime Evidence

Runtime evidence represents information available to the assurance
mechanism when checking the decision.

This evidence can intentionally differ from both physical ground truth and
Digital Twin state.

This enables controlled evaluation of assurance behaviour when evidence
quality degrades.

---

## 5. Experimental Variable

EXP-006 initially isolates one decision dependency:

> **vehicle capacity**

This restriction is deliberate.

Introducing multiple dependency types while simultaneously introducing
evidence uncertainty would make it difficult to determine whether observed
effects resulted from:

- evidence quality;
- dependency type;
- decision logic; or
- interactions between these factors.

Capacity therefore provides a controlled environment for studying the
evidence problem before expanding the framework.

---

## 6. Evidence Conditions

Twelve controlled conditions were evaluated.

The conditions include:

| Condition | Evidence Behaviour | Purpose |
|---|---|---|
| E0 | Accurate evidence | Baseline invalid decision with correct observation |
| E1 | Small observation error | Error does not change invalid classification |
| E2 | Boundary-shifting evidence | Observation moves decision to validity boundary |
| E3 | Validity-flipping evidence | Invalid physical decision appears valid |
| E4 | Stale evidence | Old observation hides current physical invalidity |
| E5 | Missing evidence | Required runtime evidence unavailable |
| E6 | Conflicting evidence | Runtime sources disagree |
| E7 | Accurate valid evidence | Valid decision with reliable evidence |
| E8 | Misleading evidence | Valid physical decision appears invalid |
| E9 | Error with larger margin | Tests tolerance when decision has greater margin |
| E10 | Boundary-sensitive error | Similar error produces different consequence near boundary |
| E11 | Stale Twin-matching evidence | Old evidence agrees with Twin but not current physical state |

These conditions were designed to distinguish evidence error magnitude from
decision consequence.

---

## 7. Critical Comparisons

EXP-006 includes several controlled comparisons.

### 7.1 Same Physical State, Different Evidence

Different evidence representations are supplied for comparable physical
conditions.

This tests whether assurance behaviour changes because of evidence quality
rather than because the physical system changed.

### 7.2 Same Evidence Error, Different Decision Margin

Comparable observation errors are applied to decisions with different
validity margins.

This tests whether the consequence of evidence error depends on the
decision-specific boundary.

### 7.3 Stale Evidence That Appears Plausible

Some stale evidence remains consistent with the Digital Twin while being
inconsistent with current physical state.

This tests whether apparent agreement between evidence and the Twin is
sufficient for safe autonomous authority.

---

## 8. Compared Assurance Strategies

Three assurance strategies were evaluated.

### B1 — Decision Relevance

The policy intervenes when detected physical–digital divergence affects a
dependency used by the current decision.

This represents the earlier DARA-DT relevance-based stage.

### B2 — Deterministic Decision Impact

The policy evaluates whether divergence crosses the decision-specific
validity boundary.

For EXP-006 this baseline deliberately receives perfect physical-capacity
evidence.

It therefore represents the idealised evidence assumption used in EXP-005.

It is not intended to represent realistic imperfect sensing.

### P1 — Evidence-Aware Decision Impact

The evidence-aware policy operates only on the runtime evidence available
under each experimental condition.

It explicitly handles:

- available evidence;
- missing evidence;
- stale evidence;
- conflicting evidence; and
- observed capacity relative to decision demand.

Physical ground truth remains hidden from this policy.

---

## 9. Evaluation Outcomes

Each assurance decision is compared against independent physical ground
truth.

Four outcome classes are used:

### True Intervention — TI

The physical decision is invalid and the assurance policy intervenes.

### False Intervention — FI

The physical decision is valid but the assurance policy intervenes.

### Missed Intervention — MI

The physical decision is invalid but autonomous execution remains permitted.

### Correct Non-Intervention — CNI

The physical decision is valid and autonomous execution remains permitted.

---

## 10. Metrics

The experiment reports:

- assurance accuracy;
- intervention precision;
- intervention recall;
- false intervention count;
- missed intervention count;
- false intervention rate;
- missed intervention rate; and
- autonomy availability.

Autonomy availability measures the proportion of conditions in which
unrestricted autonomous execution remains available.

This is important because an assurance mechanism that intervenes on every
decision may achieve high recall while making useful autonomy unavailable.

---

## 11. Verified Results

The completed experiment produced the following aggregate results across
the twelve controlled conditions.

| Policy | Conditions | TI | FI | MI | CNI | Accuracy | Precision | Recall | FI Rate | MI Rate | Autonomy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Decision Relevance | 12 | 9 | 3 | 0 | 0 | 0.750 | 0.750 | 1.000 | 1.000 | 0.000 | 0.000 |
| Deterministic Impact | 12 | 9 | 0 | 0 | 3 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.250 |
| Evidence-Aware Impact | 12 | 8 | 1 | 1 | 2 | 0.833 | 0.889 | 0.889 | 0.333 | 0.111 | 0.250 |

These values are the observed outputs of the implemented EXP-006 controlled
experimental matrix.

---

## 12. Result Interpretation

### 12.1 Decision Relevance Is Conservative

The decision-relevance policy detected all conditions requiring
intervention:

- recall = **1.000**;
- missed interventions = **0**.

However, it also intervened in all physically valid conditions:

- false interventions = **3**;
- false intervention rate = **1.000**;
- autonomy availability = **0.000**.

This reinforces the result from EXP-004 and EXP-005:

> Decision relevance identifies whether a divergence concerns the current
> decision, but relevance alone does not establish whether the divergence
> actually invalidates that decision.

---

### 12.2 Perfect-Evidence Decision Impact Provides an Upper Baseline

The deterministic decision-impact baseline produced:

- accuracy = **1.000**;
- precision = **1.000**;
- recall = **1.000**;
- false interventions = **0**;
- missed interventions = **0**;
- autonomy availability = **0.250**.

This confirms the controlled EXP-005 finding under the EXP-006 conditions:
when accurate physical evidence is available, decision-specific validity
reasoning can distinguish valid from invalid decisions in this capacity
experiment.

However, this result must not be interpreted as evidence that real runtime
assurance can achieve perfect performance.

The baseline is intentionally supplied with perfect physical evidence and
therefore acts as an experimental upper reference.

---

### 12.3 Imperfect Evidence Degrades Decision-Impact Assurance

The evidence-aware policy produced:

- accuracy = **0.833**;
- precision = **0.889**;
- recall = **0.889**;
- false interventions = **1**;
- missed interventions = **1**;
- autonomy availability = **0.250**.

Compared with the deterministic perfect-evidence baseline, imperfect runtime
evidence therefore introduced both:

- an unnecessary intervention; and
- an unsafe missed intervention.

This is a significant experimental finding.

The decision-impact concept remains useful, but its reliability depends on
the evidence from which impact is estimated.

---

## 13. Central Finding

EXP-006 exposes a limitation that was intentionally hidden by the
perfect-evidence assumption in EXP-005.

The experimental progression is now:

```text
Physical–Digital Divergence
            ↓
Decision Relevance
            ↓
Decision Impact / Validity Margin
            ↓
Evidence Reliability
            ↓
Decision Risk
            ↓
Runtime Assurance
            ↓
Autonomous Authority
