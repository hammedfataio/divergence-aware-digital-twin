# Experiment 004 — Divergence Severity and Decision Relevance

**Project:** DARA-DT  
**Experiment:** EXP-004  
**Status:** Design Stage  
**Research Theme:** Decision-Relevant Physical–Digital Divergence  
**Primary Domain:** Dynamic Logistics Digital Twin  

---

## 1. Purpose

Earlier DARA-DT experiments established a controlled proof of concept in which
the number of detected physical–digital divergences was not sufficient to
determine whether runtime intervention was appropriate.

In particular, the existing experimental matrix contains cases in which:

- multiple divergences are irrelevant to the current decision; and
- a single divergence is sufficient to invalidate the decision when it affects
  a decision dependency.

EXP-004 extends this investigation by introducing **divergence severity**.

The experiment asks whether the magnitude of a physical–digital mismatch is
itself sufficient to determine intervention, or whether its effect must be
interpreted relative to the decision being made.

---

## 2. Research Question

> **How does the severity of physical–digital divergence interact with
> decision relevance in determining whether an autonomous action remains
> valid?**

A secondary question is:

> **Can a relatively small but decision-critical divergence require
> intervention while a larger but decision-irrelevant divergence does not?**

---

## 3. Motivation

A Digital Twin does not need to be perfectly synchronised with the physical
system for every autonomous decision to remain valid.

For example, consider an order requiring a vehicle capacity of 5 units.

The Digital Twin may report:

```text
vehicle capacity = 10
