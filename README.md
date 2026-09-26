# DARA-DT

## Divergence-Aware Runtime Assurance for AI-Driven Digital Twins in Autonomous Logistics

**Research prototype investigating decision-relevant physical–digital divergence as a runtime assurance signal for autonomous logistics Digital Twins.**

[![Tests](https://github.com/hammedfataio/divergence-aware-digital-twin/actions/workflows/tests.yml/badge.svg)](https://github.com/hammedfataio/divergence-aware-digital-twin/actions/workflows/tests.yml)

**Research Stage:** Controlled proof-of-concept evaluation  
**Framework:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Domain:** Digital Twins · AI · Runtime Assurance · Autonomous Logistics

---

## Research Proposition

A Digital Twin can diverge from physical reality without every mismatch
invalidating the autonomous decision currently being considered.

DARA-DT investigates a more selective assurance question:

> **When physical reality and its Digital Twin disagree, does the disagreement
> affect information required by the specific decision about to be executed?**

This leads to the central research chain:

```text
Physical–Digital Divergence
            ↓
     Decision Dependency
            ↓
      Decision Relevance
            ↓
   Operational Consequence
            ↓
      Runtime Assurance
            ↓
    Autonomous Authority
```

The working hypothesis is that **decision-relevant divergence** may provide a
more selective runtime assurance signal than divergence detection alone.

---

## Why This Matters

AI-driven Digital Twins can support increasingly autonomous logistics
decisions.

However, the Digital Twin may become temporarily inconsistent with the
physical system because of:

- stale or delayed telemetry;
- vehicle breakdowns;
- incorrect resource availability;
- capacity changes;
- communication delays; or
- unexpected operational disturbances.

An AI-generated decision may therefore be internally valid according to the
Digital Twin while being inappropriate for the physical system that actually
exists.

At the opposite extreme, restricting autonomy whenever *any* mismatch occurs
may create unnecessary interventions.

DARA-DT investigates the space between these two behaviours.

---

## Central Research Question

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

Supporting questions examine:

1. which runtime signals identify decision-relevant divergence;
2. how different forms and combinations of divergence affect decision
   reliability; and
3. whether divergence-aware runtime assurance can reduce inappropriate
   autonomous actions while preserving useful autonomy and logistics
   performance.

---

## DARA-DT

**DARA-DT** stands for:

> **Divergence-Aware Runtime Assurance for Digital Twins**

The proposed research architecture is:

```text
┌─────────────────────────┐
│ Physical Logistics      │
│ System                  │
└────────────┬────────────┘
             │ telemetry
             ▼
┌─────────────────────────┐
│ Digital Twin            │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ AI / Decision           │
│ Controller              │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Decision Dependencies   │
└────────────┬────────────┘
             │
             ├──────────────────┐
             │                  │
             ▼                  ▼
┌──────────────────┐   ┌──────────────────┐
│ Physical–Digital │   │ Decision         │
│ Divergence       │   │ Dependencies     │
└────────┬─────────┘   └────────┬─────────┘
         │                      │
         └──────────┬───────────┘
                    ▼
          ┌─────────────────────┐
          │ Decision-Relevance  │
          │ Analysis            │
          └──────────┬──────────┘
                     ▼
          ┌─────────────────────┐
          │ DARA-DT Runtime     │
          │ Assurance           │
          └──────────┬──────────┘
                     ▼
          ┌─────────────────────┐
          │ Autonomous          │
          │ Authority           │
          └─────────────────────┘
```

The architecture changes the assurance question from:

> **Is divergence present?**

to:

> **Does the detected divergence affect this decision?**

---

## Decision-Relevant Divergence

For decision \(d_t\), let:

\[
Dep(d_t)
\]

represent the state variables required by the decision.

Let:

\[
D_t
\]

represent detected physical–digital divergences at time \(t\).

The decision-relevant divergence set is represented conceptually as:

\[
D_t^{rel}(d_t)=Dep(d_t)\cap D_t
\]

This distinction allows divergence to be evaluated in the context of the
decision rather than treating every Digital Twin mismatch as equally
consequential.

---

# Preliminary Evidence

The current implementation evaluates the core mechanism using **seven
deliberately controlled conditions**.

Three assurance strategies are compared:

1. **No Assurance** — divergence does not restrict execution.
2. **Global Divergence Assurance** — any detected divergence triggers
   intervention.
3. **DARA-DT** — intervention depends on whether divergence affects the
   current decision.

Ground-truth intervention requirements are determined independently from the
physical system state.

---

## The Key Experiment

The clearest current comparison holds divergence count constant:

| Condition | Total Divergence | Decision-Relevant | Required Response |
|---|---:|---:|---|
| `irrelevant_1` | 1 | 0 | Allow |
| `relevant_vehicle_capacity` | 1 | 1 | Intervene |

Both conditions contain exactly **one physical–digital divergence**.

What changes is its relationship to the decision.

```text
              SAME DIVERGENCE COUNT
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
         IRRELEVANT          RELEVANT
        TO DECISION        TO DECISION
              │                 │
              ▼                 ▼
            ALLOW           INTERVENE
```

This controlled comparison motivates the project's central proposition:

> **Divergence quantity alone may be insufficient for determining whether
> autonomous authority should be restricted.**

---

## Seven-Condition Experimental Matrix

### Decision-Irrelevant Conditions

| Condition | Divergence Count | Relevant Count |
|---|---:|---:|
| `irrelevant_1` | 1 | 0 |
| `irrelevant_5` | 5 | 0 |
| `irrelevant_10` | 10 | 0 |
| `irrelevant_25` | 25 | 0 |

### Decision-Relevant Conditions

| Condition | Divergence Count | Relevant Count |
|---|---:|---:|
| `relevant_vehicle_status` | 2 | 2 |
| `relevant_vehicle_capacity` | 1 | 1 |
| `relevant_vehicle_availability` | 1 | 1 |

---

## Aggregate Preliminary Results

| Policy | Correct | False Interventions | Missed Interventions | Precision | Recall | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| No Assurance | 4/7 | 0 | 3 | 0.0% | 0.0% | 57.1% |
| Global Divergence | 3/7 | 4 | 0 | 42.9% | 100.0% | 42.9% |
| **DARA-DT** | **7/7** | **0** | **0** | **100.0%** | **100.0%** | **100.0%** |

### Interpretation

Within these seven controlled conditions:

- **No Assurance** preserved execution but missed all three cases requiring
  intervention.
- **Global Divergence Assurance** detected all three intervention cases but
  also produced four unnecessary interventions.
- **DARA-DT** distinguished all tested decision-relevant and
  decision-irrelevant conditions.

The important result is **not simply the 100% value**.

The current evidence demonstrates that the prototype can operationalise:

```text
divergence → dependency → relevance → assurance response
```

and motivates broader investigation of whether this relationship remains
useful under more realistic and stochastic conditions.

> **Scope warning:** These results represent seven deliberately constructed
> proof-of-concept conditions. They do not establish general superiority,
> statistical generalisation, or 100% performance in realistic logistics
> systems.

See the full [`Preliminary Results`](docs/results.md).

---

# What Has Been Implemented

The current research prototype contains:

- physical logistics state simulation;
- independently maintained Digital Twin state;
- controlled divergence injection;
- logistics decision generation;
- explicit decision-dependency mapping;
- physical–digital divergence detection;
- decision-relevance analysis;
- independent physical-state ground-truth validation;
- multiple assurance policies;
- experimental outcome evaluation;
- aggregate assurance metrics;
- automated tests; and
- continuous integration.

The current controller is deliberately simple. The present experimental stage
isolates the assurance mechanism before introducing more sophisticated
optimisation and AI decision controllers.

---

# Candidate Research Contribution

The doctoral research will investigate whether:

> **Decision-specific dependency matching between physical–digital divergence
> and AI-generated logistics decisions can provide a rigorous basis for
> runtime assurance and adaptive autonomous authority.**

The candidate contribution is therefore not simply another divergence
detector.

It is the investigation of the relationship:

```text
What differs between reality and the Twin?
                  ↓
Does that difference matter to this decision?
                  ↓
What operational consequence could result?
                  ↓
Should autonomous authority change?
```

This remains a **candidate research contribution** subject to literature-based
novelty testing and broader empirical evaluation.

---

# Evaluation Roadmap

The next experimental stage will introduce:

- stochastic and dynamic logistics simulation;
- temporal divergence and stale telemetry;
- operational and compound disturbances;
- distribution shift;
- stronger optimisation and AI-based controllers;
- stronger runtime-assurance baselines;
- repeated experiments across controlled random seeds;
- statistical confidence intervals and effect sizes;
- logistics-performance metrics;
- autonomy-availability metrics;
- intervention latency;
- computational overhead;
- sensitivity analysis; and
- ablation studies.

The broader research will examine the trade-off:

\[
\text{Assurance}
\longleftrightarrow
\text{Autonomy Availability}
\longleftrightarrow
\text{Logistics Performance}
\]

---

# Research Documentation

For a quick research overview, start with:

**[`Supervisor Research Summary`](docs/supervisor_research_summary.md)**

For the experimental evidence:

**[`Preliminary Results`](docs/results.md)**

For deeper research documentation:

| Area | Document |
|---|---|
| Research problem | [`Research Gap`](docs/research_gap.md) |
| Research questions | [`Research Questions`](docs/research_questions.md) |
| Literature | [`Literature Matrix`](docs/literature_matrix.md) |
| Novelty analysis | [`Novelty Evidence Matrix`](docs/novelty_evidence_matrix.md) |
| Closest research | [`Closest Prior Work`](docs/closest_prior_work.md) |
| Methodology | [`Methodology`](docs/methodology.md) |
| Architecture | [`System Architecture`](docs/system_architecture.md) |
| Benchmark | [`Benchmark Protocol`](docs/benchmark_protocol.md) |
| Pilot experiment | [`Experiment 001`](docs/experiment_001_bc_pilot.md) |
| Decision relevance | [`Experiment 003`](docs/experiment_003_decision_relevance.md) |

---

# Repository Structure

```text
divergence-aware-digital-twin/
│
├── .github/workflows/       # automated validation
├── docs/                    # research documentation
├── src/dara_dt/
│   ├── assurance/           # runtime assurance policies
│   ├── decision/            # decisions and dependencies
│   ├── divergence/          # detection and relevance
│   ├── evaluation/          # outcomes and metrics
│   ├── experiments/         # controlled experiments
│   ├── simulation/          # physical logistics model
│   └── twin/                # Digital Twin representation
│
├── tests/                   # automated test suite
├── README.md
└── pyproject.toml
```

---

# Reproducibility

The project currently uses:

- **Python 3.12+**
- **uv** for dependency management
- **pytest** for automated testing
- **GitHub Actions** for continuous integration

Experimental runners generate machine-readable outputs so that reported
results can be traced back to executable experiments.

---

# Research Status

**Current stage:** Controlled proof-of-concept evaluation

### Established in the current prototype

- executable DARA-DT research pipeline;
- explicit decision-dependency representation;
- physical–digital divergence detection;
- decision-relevance analysis;
- independent physical ground truth;
- comparative assurance policies;
- seven-condition controlled evaluation;
- aggregate machine-generated metrics; and
- automated validation.

### Not yet established

- effectiveness under realistic stochastic logistics;
- statistical generalisation;
- scalability;
- autonomy/performance trade-offs;
- effectiveness with advanced AI controllers;
- superiority over stronger assurance approaches; or
- confirmed scientific novelty.

---

# Research Integrity

**DARA-DT is a working research framework name.**

The repository documents an active research investigation rather than a
completed or validated assurance standard.

Current results are preliminary and deliberately bounded to the implemented
controlled experiments.

Claims of broader effectiveness or novelty will require systematic comparison,
expanded experimentation, and statistical evaluation.
