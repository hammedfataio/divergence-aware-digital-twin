# DARA-DT — Preliminary Experimental Results

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Framework:** DARA-DT  
**Research Stage:** Controlled proof-of-concept evaluation  
**Status:** Preliminary results

---

## 1. Purpose

This document records the current experimental results for the proposed
**Divergence-Aware Runtime Assurance for Digital Twins (DARA-DT)** framework.

The current experiments investigate a specific question:

> Does the relevance of physical–digital divergence to a particular decision
> provide a more selective basis for runtime intervention than divergence
> detection alone?

The results reported here are generated from controlled simulation experiments.

They should be interpreted as **proof-of-concept evidence**, not as evidence
of general superiority or statistical generalisation.

---

## 2. Compared Assurance Strategies

Three runtime strategies are evaluated.

### 2.1 No Assurance

The autonomous decision is allowed to proceed without considering detected
physical–digital divergence.

### 2.2 Global Divergence Assurance

The system intervenes whenever physical–digital divergence is detected,
regardless of whether the divergent state affects the current decision.

### 2.3 DARA-DT

The proposed approach evaluates whether detected divergence affects state
variables required by the specific decision under consideration.

Intervention is triggered when divergence is relevant to the decision.

---

## 3. Controlled Experimental Matrix

Seven controlled conditions are currently included.

| Condition | Divergence Count | Decision-Relevant Count | Intervention Required |
|---|---:|---:|---|
| irrelevant_1 | 1 | 0 | No |
| irrelevant_5 | 5 | 0 | No |
| irrelevant_10 | 10 | 0 | No |
| irrelevant_25 | 25 | 0 | No |
| relevant_vehicle_status | 2 | 2 | Yes |
| relevant_vehicle_capacity | 1 | 1 | Yes |
| relevant_vehicle_availability | 1 | 1 | Yes |

The first four conditions test increasing quantities of divergence that do not
affect the selected decision.

The final three conditions introduce divergence in information directly used
to determine whether the selected vehicle can execute the logistics decision.

---

## 4. Experimental Outcomes

The machine-generated outcomes were:

| Condition | No Assurance | Global Divergence | DARA-DT |
|---|---|---|---|
| irrelevant_1 | Correct non-intervention | False intervention | Correct non-intervention |
| irrelevant_5 | Correct non-intervention | False intervention | Correct non-intervention |
| irrelevant_10 | Correct non-intervention | False intervention | Correct non-intervention |
| irrelevant_25 | Correct non-intervention | False intervention | Correct non-intervention |
| relevant_vehicle_status | Missed intervention | True intervention | True intervention |
| relevant_vehicle_capacity | Missed intervention | True intervention | True intervention |
| relevant_vehicle_availability | Missed intervention | True intervention | True intervention |

---

## 5. Aggregate Assurance Metrics

The experimental pipeline produced the following aggregate results:

| Policy | True Interventions | False Interventions | Missed Interventions | Correct Non-Interventions | Precision | Recall | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 3 | 4 | 0.0% | 0.0% | 57.1% |
| Global Divergence | 3 | 4 | 0 | 0 | 42.9% | 100.0% | 42.9% |
| DARA-DT | 3 | 0 | 0 | 4 | 100.0% | 100.0% | 100.0% |

These values describe performance **only across the seven deliberately
constructed proof-of-concept conditions**.

The 100% value observed for DARA-DT must therefore not be interpreted as
general system accuracy.

---

## 6. Primary Observation

The strongest observation from the current experiment is that:

> **The number of detected divergences alone did not determine whether
> intervention was appropriate in these controlled scenarios.**

For example:

- `irrelevant_25` contained **25 divergences**, but none affected the current
  decision and intervention was not required.
- `relevant_vehicle_capacity` contained only **1 divergence**, but that
  divergence affected a state variable required by the decision and
  intervention was required.

This provides a useful contrast between **divergence quantity** and
**decision relevance**.

---

## 7. Controlled Same-Count Comparison

An especially important comparison is:

| Condition | Divergences | Relevant | Required Response |
|---|---:|---:|---|
| irrelevant_1 | 1 | 0 | Allow |
| relevant_vehicle_capacity | 1 | 1 | Intervene |

Both conditions contain exactly one detected divergence.

The difference is whether that divergence affects a dependency of the current
decision.

Under these controlled conditions:

```text
Same divergence count
        |
        v
Different decision relevance
        |
        v
Different appropriate assurance response
```

This comparison isolates decision relevance more clearly than simply comparing
conditions containing different numbers of divergences.

---

## 8. Interpretation of the Three Strategies

### No Assurance

No Assurance avoided unnecessary interventions in all four irrelevant
conditions.

However, it missed all three conditions in which intervention was required.

This illustrates the risk of permitting autonomous execution without
considering physical–digital inconsistency.

### Global Divergence Assurance

Global Divergence Assurance detected all three conditions requiring
intervention.

However, it also intervened in all four conditions where the detected
divergence was irrelevant to the current decision.

This illustrates the potential cost of treating every Digital Twin mismatch
as sufficient reason to restrict autonomous execution.

### DARA-DT

DARA-DT distinguished the relevant and irrelevant divergence conditions
correctly across the current seven-condition matrix.

The result supports continued investigation of the hypothesis that
**decision-relevant divergence can provide a more selective assurance signal
than divergence presence alone**.

---

## 9. What the Results Currently Support

The present evidence supports the following limited statement:

> In the current controlled proof-of-concept experiments, decision-relevant
> divergence distinguished conditions requiring runtime intervention from
> conditions in which detected divergence did not invalidate the selected
> logistics decision.

The experiments also demonstrate that the prototype can operationalise the
research chain:

**Physical–Digital Divergence  
→ Decision Dependency  
→ Decision Relevance  
→ Assurance Response**

---

## 10. What the Results Do Not Yet Establish

The current experiments do **not** establish that:

- DARA-DT is generally superior to existing runtime-assurance methods;
- DARA-DT achieves 100% accuracy in realistic environments;
- decision relevance will remain effective under stochastic logistics
  conditions;
- the approach generalises across logistics domains;
- the current policy is optimal;
- the framework maintains logistics performance under repeated intervention;
- the approach scales to large Digital Twin systems; or
- the proposed research contribution is scientifically novel.

These questions require broader experimental and literature-based evaluation.

---

## 11. Current Experimental Limitations

The present experiment deliberately isolates the core mechanism.

Important limitations include:

1. a small number of deterministic controlled conditions;
2. a simplified logistics environment;
3. a heuristic decision controller rather than a mature AI controller;
4. limited divergence categories;
5. no current statistical generalisation across stochastic repetitions;
6. no realistic road-network dynamics;
7. no current evaluation of logistics cost or delivery performance;
8. no current measurement of autonomy availability;
9. no current runtime-overhead evaluation; and
10. a limited set of runtime-assurance baselines.

These limitations define the next experimental stage rather than being hidden
from the evaluation.

---

## 12. Next Evaluation Stage

The next research stage should extend the controlled proof-of-concept toward:

- stochastic simulation;
- repeated experiments across controlled random seeds;
- temporal divergence;
- stale telemetry;
- operational disturbances;
- distribution shift;
- compound divergence;
- stronger optimisation and AI decision controllers;
- stronger runtime-assurance baselines;
- intervention latency;
- computational overhead;
- autonomy availability;
- logistics-performance measures;
- sensitivity analysis;
- ablation analysis; and
- confidence intervals and effect-size reporting.

The longer-term evaluation should examine the trade-off:

**Assurance ↔ Autonomy Availability ↔ Logistics Performance**

---

## 13. Research Integrity Statement

All results in this document should be reproducible from the research
prototype and experimental pipeline.

The reported metrics correspond only to the current controlled experimental
matrix.

No claim of general superiority, statistical generalisation, or confirmed
scientific novelty is made from these preliminary experiments.

The purpose of the current results is to establish a reproducible
proof-of-concept and provide evidence sufficient to motivate broader doctoral
investigation.
