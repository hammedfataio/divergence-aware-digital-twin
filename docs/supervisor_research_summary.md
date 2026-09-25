# Divergence-Aware Runtime Assurance for AI-Driven Digital Twins in Autonomous Logistics Systems

## Research Summary

### Research Motivation

Digital Twins are increasingly being explored as operational representations
of physical logistics systems, supporting monitoring, optimisation, prediction,
and autonomous decision-making.

Their use for autonomous decision-making introduces an important assurance
problem.

A Digital Twin may become temporarily inconsistent with the physical system
because of delayed telemetry, communication failures, stale state information,
vehicle breakdowns, incorrect resource availability, changing capacity, or
unexpected operational disturbances.

An AI decision generated from such a Digital Twin may therefore be logically
consistent with the digital representation while being inappropriate for the
physical system that actually exists.

This creates a fundamental runtime question:

> **When a Digital Twin diverges from physical reality, does that divergence
> actually invalidate the autonomous decision that is about to be executed?**

Detecting divergence alone does not fully answer this question.

Some physical–digital mismatches may be operationally significant but
irrelevant to the particular decision under consideration. Conversely, a
single mismatch affecting a critical decision dependency may make an
otherwise reasonable autonomous action unsafe or inappropriate.

This research therefore investigates **decision-relevant physical–digital
divergence** as a potential basis for runtime assurance in autonomous
logistics Digital Twins.

---

## Research Gap

Existing Digital Twin research provides mechanisms for synchronisation,
state monitoring, anomaly detection, uncertainty estimation, model fidelity,
and runtime assurance.

However, detecting that a Digital Twin differs from its physical counterpart
does not necessarily establish whether an autonomous decision should be
restricted.

The unresolved research problem investigated here is the relationship between:

**physical–digital divergence → decision dependency → operational consequence
→ assurance response → autonomous authority**

The central hypothesis is that runtime assurance can become more selective
when divergence is evaluated relative to the information dependencies of the
specific decision being considered, rather than treating every detected
mismatch as equally relevant.

This distinction motivates the proposed DARA-DT framework.

---

## Central Research Question

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

Three supporting questions guide the investigation:

1. **Detection:** Which runtime signals most effectively identify
   decision-relevant divergence between a physical logistics system and its
   Digital Twin?

2. **Decision impact:** How do different forms and combinations of
   physical–digital divergence affect the reliability of AI-generated
   logistics decisions?

3. **Runtime assurance:** Can decision-relevant divergence be used to reduce
   inappropriate autonomous actions while preserving useful levels of
   autonomy and logistics performance?

---

## Proposed Framework: DARA-DT

**DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins**

DARA-DT is a proposed runtime assurance framework that relates detected
physical–digital divergence to the dependencies of the specific autonomous
decision under consideration.

The conceptual pipeline is:

**Physical System  
→ Digital Twin  
→ AI Decision  
→ Decision Dependency Mapping  
→ Physical–Digital Divergence Detection  
→ Decision-Relevance Analysis  
→ Runtime Assurance  
→ Autonomous Authority**

For a decision \(d_t\), let:

\[
Dep(d_t)
\]

represent the physical or Digital Twin state variables upon which the decision
depends.

Let:

\[
D_t
\]

represent the set of detected physical–digital divergences at time \(t\).

The decision-relevant divergence set can then be represented conceptually as:

\[
D_t^{rel}(d_t) = Dep(d_t) \cap D_t
\]

The key assurance question is therefore not only:

> **Is the Digital Twin divergent?**

but:

> **Does the detected divergence affect information required by this specific
> decision?**

If the divergence is unrelated to the decision, autonomous execution may
remain appropriate.

If the divergence affects a critical decision dependency, the assurance layer
may defer, restrict, or redirect autonomous execution.

---

## Prototype Implementation

A reproducible research prototype has been developed to evaluate the core
DARA-DT hypothesis under controlled logistics conditions.

The prototype currently includes:

- a physical logistics simulation;
- an independently maintained Digital Twin state;
- controlled physical–digital divergence generation;
- logistics decision generation from Digital Twin state;
- explicit decision-dependency mapping;
- divergence detection;
- decision-relevance analysis;
- independent physical-state ground-truth validation;
- alternative runtime-assurance policies;
- experimental outcome evaluation;
- automated testing; and
- continuous integration for reproducible execution.

A key methodological design choice is that intervention ground truth is
determined independently from the physical system state rather than from the
DARA-DT relevance mechanism itself. This reduces the risk of evaluating the
framework using labels generated by its own decision logic.

---

## Controlled Experimental Evaluation

The current experimental matrix contains seven deliberately controlled
conditions.

### Decision-Irrelevant Divergence

Four conditions introduce:

- 1 irrelevant divergence;
- 5 irrelevant divergences;
- 10 irrelevant divergences; and
- 25 irrelevant divergences.

The mismatches are real physical–digital divergences but do not affect state
variables required by the selected logistics decision.

### Decision-Relevant Divergence

Three conditions introduce stale Digital Twin information affecting:

- vehicle operational status;
- vehicle capacity; and
- vehicle availability.

These variables directly influence whether the selected vehicle can physically
execute the generated logistics decision.

Three runtime strategies are evaluated:

1. **No Assurance** — autonomous execution is not restricted by divergence.
2. **Global Divergence Assurance** — intervention occurs whenever any
   divergence is detected.
3. **DARA-DT** — intervention is determined from divergence affecting the
   dependencies of the current decision.

---

## Preliminary Results

Across the seven controlled proof-of-concept conditions, the machine-generated
experimental results were:

| Policy | Correct Cases | False Interventions | Missed Interventions | Precision | Recall | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| No Assurance | 4/7 | 0 | 3 | 0.0% | 0.0% | 57.1% |
| Global Divergence Assurance | 3/7 | 4 | 0 | 42.9% | 100.0% | 42.9% |
| DARA-DT | 7/7 | 0 | 0 | 100.0% | 100.0% | 100.0% |

The principal observation is not the absolute accuracy value, but the
difference between **divergence presence** and **decision relevance**.

For example:

- a condition containing **25 decision-irrelevant divergences** did not
  require intervention; while
- a condition containing **one decision-relevant capacity divergence**
  required intervention.

An even more controlled comparison is obtained when divergence count is held
constant:

- **one irrelevant divergence** → autonomous execution remained appropriate;
- **one relevant capacity divergence** → intervention was required.

This preliminary result supports further investigation of the hypothesis that
the relevance of divergence to a specific decision may provide a more
selective runtime assurance signal than divergence detection alone.

These results are intentionally interpreted as proof-of-concept evidence and
not as evidence of general superiority.

---

## Proposed PhD Contribution

The proposed doctoral research would investigate whether
**decision-specific dependency matching between physical–digital divergence
and AI-generated logistics decisions can provide a rigorous basis for runtime
assurance and adaptive autonomous authority.**

The intended contribution is therefore not another general Digital Twin
divergence detector.

Instead, the research focuses on establishing and evaluating the relationship:

> **What is different between the physical system and the Digital Twin?  
> Which part of that difference matters to the current decision?  
> What operational consequence could result?  
> Should autonomous authority therefore be maintained, restricted, deferred,
> or transferred to an alternative mechanism?**

The research would seek to determine whether this decision-centred treatment
of divergence improves the balance between assurance and useful autonomous
operation.

---

## Planned Research Development

The current implementation deliberately isolates the core mechanism before
introducing additional system complexity.

The next research stage would extend the evaluation through:

- stochastic and dynamic logistics environments;
- temporal divergence and stale telemetry;
- operational and distributional disturbances;
- compound divergence scenarios;
- optimisation and AI-based decision controllers;
- stronger runtime-assurance baselines;
- repeated experiments across controlled random seeds;
- statistical confidence intervals and effect-size analysis;
- logistics-performance measures;
- autonomy-availability measures;
- intervention latency;
- computational overhead; and
- sensitivity and ablation analysis.

This would enable evaluation of the central trade-off:

\[
\text{Assurance}
\;\longleftrightarrow\;
\text{Autonomy Availability}
\;\longleftrightarrow\;
\text{Logistics Performance}
\]

---

## Research Significance

As Digital Twins become increasingly connected to AI-driven operational
decision-making, maintaining a sufficiently accurate representation of the
physical world becomes an assurance problem rather than only a modelling
problem.

A system that reacts to every mismatch may unnecessarily reduce autonomy.

A system that ignores divergence may execute decisions based on an invalid
representation of reality.

The proposed research investigates the space between these two extremes:
whether autonomous authority can be regulated according to the
**decision-specific consequences of physical–digital divergence**.

If supported through broader empirical evaluation, this could contribute
toward more dependable autonomous Digital Twin systems in logistics and other
dynamic cyber-physical environments.

---

## Current Research Status

**Stage:** Research prototype and preliminary controlled evaluation

The current implementation demonstrates the proposed mechanism across seven
controlled experimental conditions with reproducible automated evaluation.

**DARA-DT** remains a working research framework name.

The current results establish preliminary proof-of-concept behaviour only.
They do not establish general effectiveness, statistical generalisation, or
research novelty. These remain subjects for systematic doctoral investigation.
