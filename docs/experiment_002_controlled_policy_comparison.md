# Experiment 002 — Controlled Assurance Policy Comparison

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Experiment:** EXP-002  
**Status:** Completed controlled proof-of-concept  
**Scope:** Decision-irrelevant and decision-relevant physical–digital divergence  
**Domain:** Autonomous logistics Digital Twin

---

## 1. Objective

Experiment 002 extends the initial B-vs-C pilot by evaluating the assurance
strategies across a broader controlled matrix.

The experiment investigates whether an assurance mechanism should react to:

1. the presence or quantity of physical–digital divergence; or
2. the relevance of that divergence to the specific autonomous decision
   currently being evaluated.

The experiment therefore compares three assurance strategies across both
decision-irrelevant and decision-relevant divergence conditions.

This remains a controlled proof-of-concept. It is not intended to establish
general superiority or real-world effectiveness.

---

## 2. Research Question

The experiment addresses the following question:

> Does decision-specific divergence relevance provide more selective runtime
> intervention than either no assurance or intervention based on the presence
> of any physical–digital divergence?

The experiment specifically tests whether increasing amounts of irrelevant
divergence should alter the authority of an otherwise physically valid
decision.

---

## 3. Relationship to EXP-001

EXP-001 established a minimal B-vs-C comparison.

It demonstrated that two conditions containing the same number of detected
divergences could require different assurance responses depending on whether
those divergences affected the current decision.

EXP-002 extends that observation into a controlled experimental matrix.

Rather than considering only two cases, EXP-002 evaluates:

- four levels of decision-irrelevant divergence; and
- three forms of decision-relevant divergence.

The purpose is to test whether the preliminary distinction observed in
EXP-001 remains consistent across a wider set of deliberately constructed
conditions.

---

## 4. Assurance Strategies

Three policies are evaluated.

### B0 — No Assurance

The autonomous decision is permitted without using detected
physical–digital divergence to regulate execution.

This provides a baseline representing unrestricted autonomous execution.

---

### B1 — Global Divergence Assurance

The system intervenes whenever any physical–digital divergence is detected.

This strategy treats divergence presence as sufficient evidence for
intervention, regardless of whether the divergent variable affects the
current decision.

---

### P1 — Decision-Relevant Divergence Assurance

The DARA-DT relevance mechanism evaluates detected divergence against the
dependencies of the current decision.

Intervention occurs when divergence affects a state variable required by the
decision.

Divergence unrelated to the decision does not independently trigger
intervention.

At this experimental stage, this mechanism represents **decision relevance
only**. Later experiments test whether relevance alone is sufficient.

---

## 5. Controlled Experimental Matrix

The matrix contains seven conditions.

### 5.1 Decision-Irrelevant Divergence

Four conditions vary the number of detected divergences while keeping all
divergences unrelated to the selected vehicle-assignment decision.

| Condition | Divergence Count | Relevant Count | Ground-Truth Requirement |
|---|---:|---:|---|
| irrelevant_1 | 1 | 0 | No intervention |
| irrelevant_5 | 5 | 0 | No intervention |
| irrelevant_10 | 10 | 0 | No intervention |
| irrelevant_25 | 25 | 0 | No intervention |

In these conditions, the selected vehicle remains physically capable of
serving the order.

The injected mismatches concern other vehicles that are not required by the
selected decision.

The experiment therefore isolates whether an assurance policy reacts merely
to the amount of divergence.

---

### 5.2 Decision-Relevant Divergence

Three additional conditions introduce stale Digital Twin information
affecting the selected vehicle.

| Condition | Divergent Dependency | Ground-Truth Requirement |
|---|---|---|
| relevant_vehicle_status | Operational status | Intervention required |
| relevant_vehicle_capacity | Vehicle capacity | Intervention required |
| relevant_vehicle_availability | Vehicle availability | Intervention required |

In each case:

1. the Digital Twin is initially synchronised with the physical environment;
2. physical reality subsequently changes;
3. the Digital Twin remains stale;
4. the controller generates a vehicle-assignment decision using the stale
   Twin state; and
5. physical-state validation independently determines whether intervention
   is required.

This separation prevents the assurance policy from defining its own
ground-truth label.

---

## 6. Experimental Pipeline

The controlled evaluation follows the same conceptual sequence for each
condition:

```text
Physical Logistics State
        ↓
Digital Twin Synchronisation
        ↓
Controlled Physical–Digital Divergence
        ↓
AI/Autonomous Vehicle-Assignment Decision
        ↓
Divergence Detection
        ↓
Decision Dependency Mapping
        ↓
Decision-Relevance Analysis
        ↓
Runtime Assurance Policy
        ↓
Independent Physical-State Evaluation
        ↓
Assurance Outcome
