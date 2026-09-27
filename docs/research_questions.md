# Research Questions — DARA-DT

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Research Area:** Trustworthy Intelligent Systems  
**Application Domain:** Autonomous Logistics Systems  
**Status:** Active research framework

---

## 1. Research Problem

AI-driven Digital Twins can support increasingly autonomous decisions in
dynamic logistics systems.

However, the Digital Twin used by an AI decision-maker may not always remain
perfectly aligned with physical reality.

Divergence can arise through:

- stale telemetry;
- communication delay;
- incorrect state information;
- resource failure;
- operational disruption;
- state-estimation error;
- unexpected environmental change; or
- combinations of these conditions.

This creates an assurance problem.

An AI-generated decision may be internally valid according to the Digital
Twin while being inappropriate for the physical system.

At the same time, restricting autonomy whenever any mismatch is detected may
cause unnecessary intervention.

The research therefore investigates not only whether physical–digital
divergence exists, but whether that divergence is consequential to the
specific autonomous decision being considered.

---

## 2. Central Research Question

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

This is the central research question of DARA-DT.

Individual experiments may refine the mechanisms used to answer this
question, but they should not silently redefine the overall research problem.

---

## 3. Supporting Research Questions

### RQ1 — Detection and Decision Relevance

> **Which runtime signals and dependency relationships can identify
> decision-relevant physical–digital divergence between a logistics system
> and its Digital Twin?**

RQ1 investigates:

- physical–digital state comparison;
- divergence detection;
- decision dependencies;
- relevant versus irrelevant divergence;
- temporal divergence;
- state divergence;
- operational divergence; and
- combinations of divergence.

The important distinction is between:

```text
Global divergence
