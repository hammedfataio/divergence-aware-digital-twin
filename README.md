# Divergence-Aware Runtime Assurance for AI-Driven Digital Twins in Autonomous Logistics Systems

> **Research status:** Research design and literature-validation stage.
> **Results:** No experimental results are claimed at this stage.

## Overview

AI-enabled Digital Twins can support increasingly autonomous decisions in dynamic logistics systems, including routing, dispatch, resource allocation, and disruption response.

However, an AI decision may be computationally valid while still being operationally inappropriate if the Digital Twin on which the decision is based no longer represents the physical system with sufficient fidelity.

This project investigates the relationship between:

**Physical–Digital Divergence → AI Decision Reliability → Runtime Assurance → Autonomous Authority**

The central research problem is therefore not only whether an AI model is accurate, but whether the Digital Twin provides a sufficiently valid representation of the current logistics system for an AI-generated decision to be executed autonomously.

---

## Research Problem

Consider a delivery vehicle that has physically broken down.

If this event has not yet propagated to the Digital Twin, the twin may continue to represent the vehicle as available. An AI controller operating on that state could therefore recommend assigning another delivery to the unavailable vehicle.

The AI may have behaved correctly given its input.

The underlying problem is that its digital representation of reality has diverged from the physical system.

This project investigates how such divergence can be detected, quantified, and incorporated into runtime decisions about whether autonomous AI actions should be permitted, restricted, or rejected.

---

## Primary Research Question

> **How can physical–digital divergence be quantified at runtime and used to regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

### RQ1 — Detection

Which runtime signals are most effective for detecting decision-relevant divergence between a logistics system and its Digital Twin?

### RQ2 — Quantification

How can temporal, state, model, and distributional divergence be quantified in relation to AI decision reliability?

### RQ3 — Assurance

Can divergence-aware runtime assurance reduce inappropriate autonomous actions under disruption while maintaining acceptable logistics performance and autonomy availability?

---

## Research Hypothesis

The project will investigate whether monitoring physical–digital divergence provides useful assurance evidence for determining when autonomous AI decisions should be executed, restricted, or subjected to a safe fallback.

No assumption is made that greater raw divergence necessarily produces proportionally worse decisions.

A key research question is whether the **type, context, and decision relevance of divergence** are more informative than raw state difference alone.

---

## Conceptual Architecture

```text
Physical / Simulated Logistics System
                 │
                 │ observations
                 ▼
          ┌───────────────┐
          │ Digital Twin  │
          └───────┬───────┘
                  │
                  ▼
          AI Decision Engine
                  │
                  ▼
          Proposed Decision
                  │
                  ▼
        Divergence Monitoring
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
   Temporal      State      Model
  Divergence   Divergence  Divergence
       │          │          │
       └──────────┼──────────┘
                  │
                  ▼
        Distributional Shift
                  │
                  ▼
       Runtime Assurance Layer
                  │
                  ▼
           Decision Risk
                  │
                  ▼
          Autonomy Manager
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      Execute   Restrict   Fallback
```

This architecture is provisional and will be refined through literature review and experimental evidence.

---

## Candidate Research Framework

The working name for the experimental framework is:

### DARA-DT

**Divergence-Aware Runtime Assurance for Digital Twins**

DARA-DT is currently a research concept rather than a validated method.

The project will investigate whether runtime evidence concerning Digital Twin divergence can be used to determine whether an AI-generated logistics decision remains suitable for autonomous execution.

---

## Experimental Strategy

A simulated dynamic logistics environment will provide a controlled physical-system surrogate.

Its corresponding Digital Twin will receive state updates from the simulation.

Controlled divergence will then be introduced between the simulated system and its Digital Twin.

### D0 — Synchronised Operation

The Digital Twin accurately represents the simulated logistics system.

### D1 — Temporal Divergence

Examples:

* delayed GPS updates;
* communication latency;
* stale vehicle information;
* delayed warehouse updates.

### D2 — State Divergence

Examples:

* incorrect vehicle location;
* incorrect capacity;
* incorrect inventory;
* incorrect traffic state.

### D3 — Operational Divergence

Examples:

* unreported vehicle breakdown;
* unavailable resource represented as available;
* route disruption absent from the twin.

### D4 — Distributional Divergence

Examples:

* unexpected demand surge;
* unfamiliar congestion patterns;
* previously unseen operating conditions.

### D5 — Compound Divergence

Multiple divergence mechanisms will be introduced simultaneously to evaluate system behaviour under more difficult operating conditions.

---

## Decision-Relevant Divergence

A central part of this research is distinguishing **raw divergence** from **decision-relevant divergence**.

Not every mismatch between the physical system and Digital Twin has equal operational significance.

For example:

* a small inventory mismatch may have little effect on a routing decision;
* an unreported vehicle breakdown may completely invalidate a dispatch decision.

The project will therefore investigate whether divergence should be evaluated relative to the decision being considered rather than treated as a single global state-error value.

---

## Benchmarking Strategy

The project will use established logistics benchmark instances where appropriate and augment them with controlled dynamic and divergence scenarios.

Potential benchmark sources include:

* Solomon Vehicle Routing Problem with Time Windows instances;
* Gehring & Homberger benchmark instances;
* CVRPLIB instances.

These provide operational reference problems. The divergence experiments form an additional assurance-oriented evaluation layer.

### Operational Baselines

* simple heuristic policies;
* classical optimisation;
* AI-based decision controller;
* AI controller coupled to a Digital Twin.

### Assurance Baselines

The proposed framework will be compared against progressively stronger assurance strategies, potentially including:

1. no runtime assurance;
2. fixed safety thresholds;
3. model-confidence thresholds;
4. uncertainty-aware decision gating;
5. fixed operational-envelope constraints;
6. divergence-aware runtime assurance.

Exact baselines will be frozen before final experiments following the literature review.

---

## Evaluation

Performance will not be represented by a single metric.

### Logistics Performance

* travel distance;
* operational cost;
* lateness;
* service rate;
* vehicle utilisation;
* disruption recovery time.

### Digital Twin Fidelity

* state estimation error;
* synchronisation error;
* divergence magnitude;
* divergence detection latency.

### AI Decision Performance

* decision quality;
* failure rate;
* uncertainty and calibration where applicable.

### Assurance Performance

* inappropriate-action prevention rate;
* missed intervention rate;
* false intervention rate;
* time to intervention;
* divergence detection performance.

### Autonomy

* autonomy availability;
* fallback frequency;
* restriction frequency;
* autonomy-state transitions.

### Computational Performance

* assurance overhead;
* decision latency;
* operational performance cost introduced by assurance.

A central evaluation objective is to characterise the trade-off between:

**Assurance ↔ Autonomy ↔ Operational Performance**

---

## Planned Ablation Studies

If DARA-DT combines multiple divergence signals, ablation experiments will test their individual contribution.

Candidate experiments include removing:

* temporal-divergence monitoring;
* state-divergence monitoring;
* model-divergence monitoring;
* distribution-shift detection;
* operational-risk information.

This will help determine which evidence sources materially contribute to runtime assurance rather than assuming that every component is necessary.

---

## Research Contributions Under Investigation

This project will investigate the feasibility and value of:

1. characterising different forms of physical–digital divergence in dynamic logistics Digital Twins;
2. measuring the relationship between divergence and AI decision reliability;
3. identifying decision-relevant rather than purely state-level divergence;
4. developing a divergence-aware runtime assurance mechanism;
5. regulating autonomous decision execution using runtime assurance evidence;
6. constructing a reproducible divergence stress-testing protocol for AI-enabled logistics Digital Twins.

These are **candidate contributions** and will not be presented as established novel contributions until supported by literature analysis and experimental evidence.

---

## Research Workflow

```text
Literature & Gap Validation
            ↓
Research Questions
            ↓
Benchmark Protocol
            ↓
Simulation Environment
            ↓
Digital Twin
            ↓
Operational Baselines
            ↓
AI Decision Controller
            ↓
Controlled Divergence
            ↓
Divergence Detection
            ↓
Runtime Assurance
            ↓
Benchmark Experiments
            ↓
Ablation Studies
            ↓
Statistical Analysis
            ↓
Deployment Demonstrator
            ↓
Research Conclusions
```

---

## Planned Technology Stack

The implementation is expected to use a focused Python research stack.

* Python
* `uv` for dependency and environment management
* NumPy / Pandas
* SimPy for discrete-event simulation where appropriate
* PyTorch for learned models where justified
* scikit-learn for statistical and baseline models
* Google OR-Tools for optimisation baselines
* MLflow for experiment tracking
* Hydra for experiment configuration
* FastAPI for the eventual runtime demonstrator
* pytest for automated testing
* Docker for reproducibility
* GitHub Actions for CI

Technologies will be introduced only where they support a defined research or engineering requirement.

---

## Reproducibility Principles

The project will aim to provide:

* fixed random seeds where applicable;
* version-controlled configurations;
* documented benchmark instances;
* reproducible divergence scenarios;
* baseline implementations;
* experiment tracking;
* automated tests;
* recorded environment dependencies;
* clear separation between exploratory and final experiments.

No experimental metric will be reported without corresponding reproducible evidence.

---

## Repository Structure

```text
divergence-aware-digital-twin/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── docs/
│   ├── research_overview.md
│   ├── research_gap.md
│   ├── research_questions.md
│   ├── benchmark_protocol.md
│   ├── methodology.md
│   ├── architecture.md
│   ├── research_log.md
│   └── references.md
│
├── data/
│   └── README.md
│
├── experiments/
│   └── README.md
│
├── notebooks/
│
├── src/
│
└── tests/
```

The implementation structure will be expanded only after the benchmark and methodology are frozen.

---

## Current Status

**Stage 1 — Research Foundation**

## Project Status

**Current Stage: Stage 2 — Research Prototype Implementation**

DARA-DT has progressed from research design into an executable and automatically tested research prototype.

### Completed Research Foundation

- Research problem and gap definition
- Research questions and hypothesis
- Literature and novelty evidence mapping
- Closest-prior-work analysis
- System architecture
- Research methodology
- Benchmark and falsification protocol
- D0–D5 divergence scenario specification

### Implemented Prototype Components

- Physical logistics state models
- Simulation environment
- Independent Digital Twin state representation
- Physical–digital state synchronisation
- Physical–digital divergence detection
- AI decision representation
- Decision dependency mapping
- Decision-relevant divergence analysis
- Runtime assurance authority model
- Initial divergence-aware assurance policy
- Automated unit and integration testing
- GitHub Actions continuous integration

### Current Executable Pipeline

```text
Physical Logistics System
          │
          │ physical state sₜ
          ▼
   Digital Twin Comparison
          │
          ▼
   Divergence Detection
          │
          ▼
    Detected Divergence
          │
          │
AI Decision ──→ Dependency Mapping
          │              │
          └──────────────┘
                 │
                 ▼
      Decision-Relevance Analysis
                 │
                 ▼
        Runtime Assurance
                 │
          ┌──────┴──────┐
          ▼             ▼
        ALLOW          DEFER

Implementation has not yet been treated as evidence of research contribution.

---

## Research Integrity

This repository documents ongoing research.

Proposed frameworks, hypotheses, and candidate contributions should not be interpreted as validated findings.

Results will be reported only after experiments are completed, benchmarked, analysed, and made reproducible.
