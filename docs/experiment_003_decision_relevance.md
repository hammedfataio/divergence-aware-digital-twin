# Experiment 003 — Decision-Relevance Analysis

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Experiment:** EXP-003  
**Status:** Completed mechanism validation  
**Research Stage:** Decision-specific divergence analysis  
**Domain:** Autonomous logistics Digital Twin

---

## 1. Objective

Experiment 003 validates the decision-relevance mechanism used by DARA-DT.

Earlier experiments established that the presence or quantity of
physical–digital divergence does not necessarily determine whether an
autonomous decision should be interrupted.

EXP-003 therefore focuses on a more specific question:

> Which detected physical–digital divergences are actually relevant to the
> autonomous decision currently being evaluated?

The purpose of the experiment is not to establish that relevance alone is a
complete runtime-assurance criterion.

Instead, it verifies that DARA-DT can explicitly separate:

- divergence affecting variables required by the current decision; and
- divergence affecting variables unrelated to that decision.

This distinction becomes the foundation for the later decision-impact and
evidence-reliability experiments.

---

## 2. Research Question

EXP-003 addresses:

> Can detected physical–digital divergence be classified according to the
> dependencies of a specific autonomous logistics decision?

The experiment tests whether decision dependency information can distinguish
decision-relevant divergence from background divergence elsewhere in the
Digital Twin.

---

## 3. Motivation

A Digital Twin can contain multiple mismatches simultaneously.

However, not every mismatch necessarily affects every decision.

For example, consider a decision assigning `vehicle_07` to an order.

A mismatch involving the location or operational status of another vehicle
may indicate that the Digital Twin is imperfect, but that mismatch does not
necessarily invalidate the decision involving `vehicle_07`.

Conversely, a stale operational-status value for `vehicle_07` directly
affects information on which the assignment depends.

This motivates the distinction:

```text
Detected Divergence
        ↓
Decision Dependencies
        ↓
Dependency Matching
       ↙ ↘
 Relevant   Irrelevant
