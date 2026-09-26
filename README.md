# DARA-DT

## Divergence-Aware Runtime Assurance for AI-Driven Digital Twins in Autonomous Logistics

[![Tests](https://github.com/hammedfataio/divergence-aware-digital-twin/actions/workflows/tests.yml/badge.svg)](https://github.com/hammedfataio/divergence-aware-digital-twin/actions/workflows/tests.yml)

> **Research prototype investigating whether physical–digital divergence should influence autonomous decision-making according to its relevance to the specific decision being executed.**

**Research Stage:** Controlled proof-of-concept evaluation  
**Framework:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Research Domain:** Digital Twins · Artificial Intelligence · Runtime Assurance · Autonomous Logistics  
**Implementation Status:** Active research prototype

---

## 1. Research Overview

Digital Twins are increasingly being considered as operational representations
of physical systems that can support monitoring, prediction, optimisation, and
autonomous decision-making.

In dynamic logistics environments, however, the Digital Twin may not always
perfectly represent physical reality.

Vehicle breakdowns, stale telemetry, delayed communication, incorrect
availability information, capacity changes, and unexpected operational events
can create **physical–digital divergence**.

This creates an important assurance problem:

> An autonomous decision may be valid according to the Digital Twin while
> being inappropriate for the physical system that actually exists.

A simple response would be to restrict autonomy whenever *any* divergence is
detected.

However, not every mismatch necessarily affects the decision currently being
made.

DARA-DT investigates a more selective question:

> **Does the detected physical–digital divergence actually matter to the
> specific decision that is about to be executed?**

---

## 2. Core Research Proposition

The project investigates **decision-relevant divergence**.

Instead of treating every Digital Twin mismatch as equally important, DARA-DT
examines whether the divergent state variable is part of the information upon
which the current decision depends.

The conceptual research chain is:

```text
Physical–Digital Divergence
            │
            ▼
     Decision Dependency
            │
            ▼
      Decision Relevance
            │
            ▼
   Operational Consequence
            │
            ▼
      Runtime Assurance
            │
            ▼
    Autonomous Authority
```

The working hypothesis is:

> **Decision-relevant physical–digital divergence may provide a more selective
> basis for runtime intervention than divergence detection alone.**

This hypothesis remains subject to broader experimental evaluation.

---

## 3. Motivating Example

Consider a logistics system containing autonomous delivery vehicles.

A Digital Twin reports:

```text
Vehicle 02
Status: operational
Available: yes
Capacity: sufficient
```

The physical vehicle has actually broken down, but the update has not yet
reached the Digital Twin.

The decision controller assigns an urgent delivery to Vehicle 02.

From the controller's perspective, the decision is reasonable because the
Digital Twin reports that the vehicle is available.

From the physical system's perspective, the decision cannot be executed.

The problem is therefore not necessarily that the decision algorithm itself
has failed.

The information upon which the decision depended was inconsistent with
physical reality.

DARA-DT investigates whether this relationship can be detected before the
decision is executed.

---

## 4. Central Research Question

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

The supporting research questions investigate:

1. **Detection** — Which runtime signals can identify decision-relevant
   divergence between a logistics system and its Digital Twin?

2. **Quantification** — How do different forms and combinations of
   physical–digital divergence affect the reliability of generated logistics
   decisions?

3. **Assurance** — Can divergence-aware runtime assurance reduce inappropriate
   autonomous actions while maintaining acceptable autonomy availability and
   logistics performance?

---

## 5. What Is DARA-DT?

**DARA-DT** stands for:

> **Divergence-Aware Runtime Assurance for Digital Twins**

It is currently a **working research framework**, not a validated assurance
standard.

The framework investigates the following process:

```text
┌──────────────────────────┐
│ Physical Logistics       │
│ System                   │
└─────────────┬────────────┘
              │
              │ telemetry / state
              ▼
┌──────────────────────────┐
│ Digital Twin             │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Decision Controller      │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Decision Dependencies    │
└─────────────┬────────────┘
              │
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
┌───────────────┐  ┌────────────────┐
│ Physical–     │  │ Decision       │
│ Digital       │  │ Dependency     │
│ Divergence    │  │ Information    │
└───────┬───────┘  └───────┬────────┘
        │                  │
        └─────────┬────────┘
                  ▼
       ┌──────────────────────┐
       │ Decision-Relevance   │
       │ Analysis             │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ DARA-DT Runtime      │
       │ Assurance            │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Autonomous Authority │
       └──────────────────────┘
```

The key change is from asking:

> **Is the Digital Twin different from reality?**

to asking:

> **Does the difference affect information required by this particular
> decision?**

---

## 6. Decision-Relevant Divergence

The current prototype explicitly represents the dependencies of a decision.

For example, a vehicle-assignment decision may depend on:

```text
vehicle.status
vehicle.available
vehicle.capacity
order.status
order.demand
```

Suppose divergence is detected in:

```text
vehicle_00.status
warehouse_temperature
traffic_sensor_17
```

If the current decision depends on `vehicle_00.status` but does not depend on
the other two variables, only the first divergence is considered relevant to
that decision.

This distinction enables the assurance mechanism to reason about:

```text
Divergence exists
        ↓
Which state is divergent?
        ↓
What does this decision depend on?
        ↓
Do the two intersect?
        ↓
Should autonomous execution continue?
```

---

# 7. Experimental Strategy

The research begins with deliberately controlled experiments.

This is intentional.

Before adding realistic traffic networks, stochastic demand, complex AI
controllers, and large logistics fleets, the core mechanism must first be
tested under conditions where the source and relevance of divergence are
known.

The current proof-of-concept therefore controls:

- physical system state;
- Digital Twin state;
- injected divergence;
- decision dependencies;
- required intervention;
- assurance policy; and
- experimental outcome.

Ground-truth intervention requirements are determined independently from the
physical system state.

---

## 8. Assurance Strategies

Three strategies are currently compared.

### 8.1 No Assurance

The generated decision is allowed to proceed regardless of detected
physical–digital divergence.

```text
Decision
   ↓
ALLOW
```

This represents the absence of runtime intervention.

---

### 8.2 Global Divergence Assurance

Any detected divergence triggers intervention.

```text
Any divergence?
      │
   YES│
      ▼
    DEFER
```

This represents a conservative approach in which all physical–digital
mismatches are treated as potentially important.

---

### 8.3 DARA-DT

DARA-DT evaluates whether detected divergence affects the dependencies of the
current decision.

```text
Divergence detected
        ↓
Decision dependencies
        ↓
Relevance analysis
        ↓
Relevant?
   │          │
  NO         YES
   │          │
   ▼          ▼
 ALLOW      DEFER
```

The current prototype deliberately uses a simple **ALLOW / DEFER** policy so
that the effect of decision relevance can be isolated.

Richer adaptive-authority states are part of the future research direction.

---

# 9. Controlled Experimental Matrix

The current experimental matrix contains **seven deliberately constructed
conditions**.

Four conditions contain divergence that is irrelevant to the current decision.

Three conditions contain divergence that directly affects decision
dependencies.

### Decision-Irrelevant Conditions

| Condition | Total Divergences | Decision-Relevant Divergences |
|---|---:|---:|
| `irrelevant_1` | 1 | 0 |
| `irrelevant_5` | 5 | 0 |
| `irrelevant_10` | 10 | 0 |
| `irrelevant_25` | 25 | 0 |

### Decision-Relevant Conditions

| Condition | Total Divergences | Decision-Relevant Divergences |
|---|---:|---:|
| `relevant_vehicle_status` | 2 | 2 |
| `relevant_vehicle_capacity` | 1 | 1 |
| `relevant_vehicle_availability` | 1 | 1 |

---

# 10. Critical Same-Count Comparison

One of the most informative comparisons holds **divergence count constant**.

| Condition | Divergence Count | Relevant Count | Required Response |
|---|---:|---:|---|
| `irrelevant_1` | 1 | 0 | Allow |
| `relevant_vehicle_capacity` | 1 | 1 | Intervene |

Both conditions contain exactly:

```text
1 physical–digital divergence
```

However:

```text
                 SAME DIVERGENCE COUNT
                          │
                ┌─────────┴─────────┐
                │                   │
                ▼                   ▼
         IRRELEVANT             RELEVANT
        TO DECISION            TO DECISION
                │                   │
                ▼                   ▼
              ALLOW             INTERVENE
```

The difference is not the **number** of divergences.

The difference is whether the divergent state affects information required by
the current decision.

This controlled comparison motivates the project's central proposition:

> **Divergence quantity alone may be insufficient for deciding whether
> autonomous authority should be restricted.**

---

# 11. Preliminary Results

The current machine-generated aggregate results are:

| Assurance Strategy | True Interventions | False Interventions | Missed Interventions | Correct Non-Interventions | Accuracy |
|---|---:|---:|---:|---:|---:|
| No Assurance | 0 | 0 | 3 | 4 | 57.1% |
| Global Divergence | 3 | 4 | 0 | 0 | 42.9% |
| **DARA-DT** | **3** | **0** | **0** | **4** | **100.0%** |

Additional intervention metrics:

| Assurance Strategy | Precision | Recall | False Intervention Rate | Missed Intervention Rate |
|---|---:|---:|---:|---:|
| No Assurance | 0.0% | 0.0% | 0.0% | 100.0% |
| Global Divergence | 42.9% | 100.0% | 100.0% | 0.0% |
| **DARA-DT** | **100.0%** | **100.0%** | **0.0%** | **0.0%** |

---

## 12. Interpretation of Preliminary Evidence

Within the seven deliberately controlled conditions:

### No Assurance

No Assurance allowed all decisions to proceed.

This preserved autonomy but missed all three cases in which physical state
required intervention.

### Global Divergence Assurance

The global-divergence strategy successfully intervened in all three
intervention-required conditions.

However, it also intervened in all four conditions where divergence existed
but was irrelevant to the current decision.

### DARA-DT

DARA-DT distinguished all seven currently tested decision-relevant and
decision-irrelevant conditions.

The strongest observation is therefore **not simply the 100% accuracy value**.

The more important result is that the prototype operationalised the chain:

```text
Physical–Digital Divergence
            ↓
Decision Dependency
            ↓
Decision Relevance
            ↓
Assurance Response
```

and behaved differently when divergence count was held constant but decision
relevance changed.

This provides preliminary evidence supporting broader investigation of
decision relevance as a runtime assurance signal.

> **Important limitation:** DARA-DT achieved 100% classification accuracy only
> across these seven deliberately controlled proof-of-concept conditions.
> These results do not establish general superiority, statistical
> generalisation, or equivalent performance in realistic logistics systems.

Full experimental evidence is documented in:

**[Preliminary Results](docs/results.md)**

---

# 13. What Has Actually Been Implemented

The current prototype includes:

### Physical System

- logistics vehicle representation;
- order representation;
- physical environment state;
- vehicle availability;
- vehicle operational status; and
- vehicle capacity.

### Digital Twin

- independent Digital Twin state;
- physical-to-digital synchronisation;
- controlled stale state; and
- state updates.

### Divergence

- physical–digital state comparison;
- divergence detection;
- controlled divergence injection; and
- decision-relevance analysis.

### Decision Layer

- logistics decision representation;
- decision controller;
- explicit decision dependencies; and
- dependency mapping.

### Runtime Assurance

- no-assurance baseline;
- global-divergence baseline;
- DARA-DT relevance policy; and
- ALLOW / DEFER authority decisions.

### Evaluation

- independent physical-state validation;
- ground-truth intervention labels;
- outcome classification;
- assurance metrics;
- controlled experimental matrix; and
- machine-readable experiment output.

### Engineering

- modular Python package;
- automated tests;
- reproducible experimental runners; and
- GitHub Actions continuous integration.

---

# 14. Current Controller Scope

The current decision controller is deliberately **heuristic rather than a
trained AI model**.

This is an important methodological choice at the present stage.

The purpose of the proof-of-concept is to isolate and test the runtime
assurance mechanism without confounding the experiment with the behaviour of a
complex learning algorithm.

The wider doctoral research direction concerns **AI-driven Digital Twins**.

Future experimental stages are intended to introduce stronger controllers,
including classical optimisation and AI-based decision-making, once the core
assurance mechanism has been validated under controlled conditions.

---

# 15. Candidate Research Contribution

The proposed doctoral research investigates whether:

> **Decision-specific dependency matching between physical–digital divergence
> and AI-generated logistics decisions can provide a rigorous basis for
> runtime assurance and adaptive autonomous authority.**

The candidate contribution is therefore not simply another Digital Twin
divergence detector.

The research investigates the relationship:

```text
What differs between reality and the Digital Twin?
                      ↓
Does that difference matter to this decision?
                      ↓
What operational consequence could result?
                      ↓
Should autonomous authority change?
```

This remains a **candidate research contribution**.

Its scientific novelty must be established through systematic comparison with
the closest prior research and through broader empirical evaluation.

---

# 16. Research Evaluation Roadmap

The controlled prototype is the starting point rather than the final
evaluation environment.

The next research stages will investigate:

### More Realistic Logistics Dynamics

- vehicle movement;
- road-network representation;
- travel time;
- dynamic orders;
- resource utilisation;
- delivery deadlines;
- congestion;
- vehicle failures; and
- stochastic operational events.

### Expanded Divergence

The broader benchmark is intended to investigate:

```text
D0 — Synchronized operation
D1 — Temporal divergence
D2 — State divergence
D3 — Operational divergence
D4 — Distributional divergence
D5 — Compound divergence
```

Not all of these categories are currently implemented.

### Stronger Decision Controllers

Future evaluation will introduce:

- heuristic baselines;
- classical optimisation;
- OR-Tools-based logistics optimisation; and
- AI-based decision controllers.

### Stronger Assurance Baselines

Future comparisons are intended to include:

- no assurance;
- global divergence;
- fixed thresholds;
- operational envelopes;
- model-confidence approaches;
- runtime assumption monitoring;
- combined fidelity/uncertainty approaches; and
- DARA-DT.

### Statistical Evaluation

Later experiments will include:

- multiple controlled random seeds;
- repeated trials;
- confidence intervals;
- effect sizes;
- paired comparisons;
- sensitivity analysis; and
- ablation studies.

---

# 17. Evaluation Dimensions

The wider research will move beyond intervention classification.

### Logistics Performance

Potential measures include:

- delivery cost;
- route distance;
- lateness;
- service rate;
- resource utilisation; and
- disruption recovery.

### Digital Twin Quality

Potential measures include:

- state estimation error;
- synchronisation error;
- divergence magnitude; and
- divergence detection latency.

### Runtime Assurance

Measures include:

- true interventions;
- false interventions;
- missed interventions;
- correct non-interventions;
- intervention precision;
- intervention recall; and
- time to intervention.

### Autonomous Authority

Future experiments will evaluate:

- autonomy availability;
- defer frequency;
- restriction frequency;
- fallback frequency; and
- unnecessary autonomy loss.

### Computational Performance

The system will also be evaluated for:

- assurance overhead;
- decision latency; and
- runtime scalability.

The broader research therefore examines the trade-off:

```text
               ASSURANCE
                   ▲
                  / \
                 /   \
                /     \
               /       \
              ▼         ▼
AUTONOMY AVAILABILITY ↔ LOGISTICS PERFORMANCE
```

---

# 18. Falsification Principle

The project is designed so that the central proposition can fail.

The research would be weakened if broader experiments demonstrate that
decision relevance:

- does not improve intervention selectivity;
- introduces unacceptable missed interventions;
- substantially reduces logistics performance;
- creates excessive runtime overhead;
- provides no meaningful improvement over simpler assurance mechanisms; or
- duplicates an already established assurance method without a substantive
  distinction.

Negative results will therefore be treated as research evidence rather than
hidden or reinterpreted as success.

---

# 19. Research Documentation

For a concise overview of the research direction:

### [Supervisor Research Summary](docs/supervisor_research_summary.md)

For the current experimental evidence:

### [Preliminary Results](docs/results.md)

Additional technical documentation:

| Document | Purpose |
|---|---|
| [Methodology](docs/methodology.md) | Experimental design and evaluation methodology |
| [System Architecture](docs/system_architecture.md) | DARA-DT components and system interfaces |
| [Benchmark Protocol](docs/benchmark_protocol.md) | Controlled evaluation and falsification protocol |
| [Experiment 001](docs/experiment_001_bc_pilot.md) | Initial controlled B-vs-C pilot |
| [Experiment 003](docs/experiment_003_decision_relevance.md) | Decision-relevance experiment |

---

# 20. Repository Structure

```text
divergence-aware-digital-twin/
│
├── .github/
│   └── workflows/          # automated validation
│
├── docs/                   # research documentation and results
│
├── src/
│   └── dara_dt/
│       ├── assurance/      # runtime assurance policies
│       ├── decision/       # decisions and dependencies
│       ├── divergence/     # divergence detection and relevance
│       ├── evaluation/     # outcomes and metrics
│       ├── experiments/    # controlled experiments
│       ├── simulation/     # physical logistics representation
│       └── twin/           # Digital Twin representation
│
├── tests/                  # automated validation
├── README.md               # research overview
└── pyproject.toml          # project configuration
```

---

# 21. Reproducibility

The project currently uses:

- **Python 3.12+**
- **uv** for Python dependency management
- **pytest** for automated testing
- **GitHub Actions** for continuous integration

The experimental pipeline produces machine-readable outputs so that reported
results can be traced back to executable experiments.

Typical development workflow:

```bash
uv sync --dev
uv run pytest -v
```

Run the controlled experimental matrix:

```bash
uv run python -m dara_dt.experiments.run_matrix
```

Generate aggregate assurance metrics:

```bash
uv run python -m dara_dt.experiments.run_metrics
```

---

# 22. Current Research Status

## Completed in the Current Prototype

- [x] research problem formulation
- [x] initial literature and gap investigation
- [x] central research question
- [x] experimental methodology
- [x] system architecture
- [x] benchmark protocol
- [x] physical logistics representation
- [x] independent Digital Twin state
- [x] controlled divergence injection
- [x] divergence detection
- [x] decision-dependency mapping
- [x] decision-relevance analysis
- [x] independent physical-state ground truth
- [x] baseline assurance strategies
- [x] DARA-DT assurance policy
- [x] controlled experimental matrix
- [x] aggregate assurance metrics
- [x] automated testing
- [x] continuous integration
- [x] preliminary proof-of-concept results

## Next Research Stage

- [ ] dynamic logistics simulation
- [ ] temporal divergence
- [ ] distributional divergence
- [ ] compound divergence
- [ ] divergence severity modelling
- [ ] stronger assurance baselines
- [ ] optimisation controller
- [ ] AI-based decision controller
- [ ] repeated stochastic experiments
- [ ] statistical analysis
- [ ] autonomy-availability measurement
- [ ] logistics-performance evaluation
- [ ] runtime-overhead evaluation
- [ ] sensitivity analysis
- [ ] ablation studies
- [ ] high-fidelity Digital Twin visual demonstrator

---

# 23. Current Limitations

The current prototype deliberately has a narrow scope.

Key limitations include:

1. The current logistics environment is simplified and does not yet represent
   a realistic road network.

2. The current decision controller is heuristic rather than a trained AI
   controller.

3. The seven experimental conditions are deliberately constructed rather than
   sampled from a stochastic logistics environment.

4. The current DARA-DT policy primarily evaluates **ALLOW / DEFER** behaviour.

5. The current results are deterministic proof-of-concept evidence rather than
   statistically generalisable findings.

6. Broader temporal, distributional, and compound divergence scenarios remain
   to be implemented.

7. Logistics performance, autonomy availability, intervention latency, and
   computational overhead require broader evaluation.

These limitations define the next experimental stages rather than being
presented as resolved problems.

---

# 24. Research Integrity

DARA-DT is currently a **working research framework name**.

The repository documents an active research investigation and should not be
interpreted as a completed or validated runtime assurance standard.

The current experimental results establish preliminary proof-of-concept
behaviour only.

No claim is currently made that:

- DARA-DT is the first framework of its kind;
- scientific novelty has been conclusively established;
- DARA-DT is generally superior to existing assurance approaches;
- the current results generalise to realistic logistics environments; or
- the current 100% controlled-condition result represents expected real-world
  performance.

Those questions require systematic literature comparison, stronger baselines,
broader experimentation, and statistical evaluation.

---

# 25. Research Direction

The long-term objective is to investigate whether an AI-driven Digital Twin
can reason not only about:

> **how different its representation is from physical reality**

but also:

> **whether that difference is consequential to the autonomous decision being
> considered.**

If supported by broader evidence, this could provide a foundation for
runtime mechanisms that dynamically regulate autonomous authority according to
the relationship between:

**physical reality, Digital Twin fidelity, decision dependencies, operational
risk, and autonomous action.**

---

## Author

**Fatai Hammed**

MSc Computer Science & Artificial Intelligence

Research interests:

**Trustworthy AI · Digital Twins · Runtime Assurance · Autonomous Systems ·
Intelligent Logistics**

---

## Project Status

**Active Research Prototype — Preliminary Controlled Evaluation Completed**

The repository will continue to evolve as additional divergence scenarios,
decision controllers, assurance baselines, and realistic logistics experiments
are implemented.
