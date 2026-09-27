# DARA-DT System Architecture

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Framework:** DARA-DT  
**Domain:** Autonomous Logistics Systems  
**Architecture Status:** Implemented Research Prototype  
**Validated Experimental Stages:** EXP-001 to EXP-006  
**Next Planned Stage:** Cross-Dependency Generalisation

---

## 1. Architecture Purpose

DARA-DT is a research architecture for investigating how
physical–digital divergence should influence autonomous AI decision-making
in logistics Digital Twins.

The architecture separates:

- physical logistics state;
- Digital Twin state;
- autonomous decision generation;
- physical–digital divergence detection;
- decision dependencies;
- decision relevance;
- decision impact and validity;
- runtime evidence;
- assurance policy;
- autonomous authority; and
- independent evaluation.

The architecture is deliberately modular so that each research hypothesis
can be tested independently.

---

## 2. Current Architectural Model

The developing DARA-DT architecture is:

```text
┌──────────────────────────────┐
│ Physical Logistics System    │
└──────────────┬───────────────┘
               │
               │ state / observations
               ↓
┌──────────────────────────────┐
│ Digital Twin                 │
└──────────────┬───────────────┘
               │
               │ represented state
               ↓
┌──────────────────────────────┐
│ AI Decision Controller       │
└──────────────┬───────────────┘
               │
               │ proposed decision
               ↓
┌──────────────────────────────┐
│ Decision Dependency Model    │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ Divergence Detection         │
│ Physical State ↔ Twin State  │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ Decision-Relevance Analysis  │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ Decision Impact / Validity   │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ Evidence Reliability Layer   │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ Runtime Assurance Policy     │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ Autonomous Authority         │
│ ALLOW / RESTRICT / DEFER     │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ Outcome Evaluation           │
└──────────────────────────────┘
```

This diagram represents the conceptual architecture.

Individual experiments activate only the components required by their
research question.

---

## 3. Critical State Separation

The architecture distinguishes three forms of state.

```text
Physical Ground Truth
        ≠
Runtime Evidence
        ≠
Digital Twin State
```

### Physical Ground Truth

Represents the actual physical logistics environment in the controlled
simulation.

It is used for independent experimental validation.

### Digital Twin State

Represents the system state available to the autonomous decision controller.

The Twin may become stale or inconsistent with physical reality.

### Runtime Evidence

Represents observations available to the assurance mechanism.

Evidence may be:

- accurate;
- inaccurate;
- stale;
- missing; or
- conflicting.

This separation became especially important in EXP-006.

---

# Part I — Core System Layers

## 4. Physical Simulation Layer

Implementation:

```text
src/dara_dt/simulation/
```

Key components include:

```text
vehicle.py
order.py
environment.py
```

The simulation layer represents the physical logistics system.

Its responsibilities include:

- maintaining vehicle state;
- maintaining order state;
- exposing physical system state;
- representing capacity;
- representing location;
- representing operational status;
- representing availability; and
- supporting controlled state modification.

The physical simulation provides the authoritative ground truth used by the
experimental evaluator.

---

## 5. Digital Twin Layer

Implementation:

```text
src/dara_dt/twin/
```

Key component:

```text
digital_twin.py
```

The Digital Twin stores a digital representation of the physical logistics
system.

The Twin can be synchronised with physical state:

```text
Physical State
        ↓
Digital Twin
```

A physical change can subsequently occur without immediate Twin
synchronisation:

```text
Physical State
        ↓
changes

Digital Twin
        ↓
remains stale
```

This produces controlled physical–digital divergence.

---

## 6. Decision Layer

Implementation:

```text
src/dara_dt/decision/
```

Key components include:

```text
model.py
dependency.py
controller.py
```

The decision layer generates autonomous logistics decisions from the Digital
Twin representation.

The current experimental prototype primarily evaluates vehicle-assignment
decisions.

Conceptually:

```text
Digital Twin
        ↓
Decision Controller
        ↓
Vehicle Assignment Decision
```

The decision object provides the context required by downstream dependency,
relevance and assurance mechanisms.

---

## 7. Decision Dependency Layer

Implementation includes:

```text
src/dara_dt/decision/dependency.py
```

The dependency layer identifies state variables required by a specific
decision.

For decision \(d_t\):

\[
Dep(d_t)
\]

represents its dependency set.

Example dependencies may include:

```text
vehicle.capacity
vehicle.operational_status
vehicle.availability
vehicle.location
```

The exact dependency set depends on the decision.

This allows DARA-DT to reason about:

> Which parts of system state actually matter to the current decision?

---

## 8. Divergence Detection Layer

Implementation:

```text
src/dara_dt/divergence/
```

Key components include:

```text
detector.py
injector.py
relevance.py
```

The divergence detector compares physical and Digital Twin state.

Conceptually:

\[
D_t = \{s_i : s_i^{physical} \neq s_i^{twin}\}
\]

The detector identifies mismatch but does not independently determine whether
that mismatch requires intervention.

Example:

```text
Physical vehicle capacity = 4
Twin vehicle capacity     = 10

Detected divergence:
capacity 10 → 4
```

---

## 9. Decision-Relevance Layer

Implementation includes:

```text
src/dara_dt/divergence/relevance.py
src/dara_dt/decision/dependency.py
```

Decision relevance combines:

```text
Detected Divergence
        +
Decision Dependencies
```

to produce:

```text
Relevant Divergence
        +
Irrelevant Divergence
```

Conceptually:

\[
D_t^{rel}(d_t) = Dep(d_t) \cap D_t
\]

This mechanism was developed and evaluated through EXP-001 to EXP-003.

---

## 10. Why Relevance Is a Separate Layer

Consider a decision involving:

```text
vehicle_07
```

while divergence exists on:

```text
vehicle_02
vehicle_04
vehicle_11
```

The Digital Twin may contain several mismatches.

However, if none affect a dependency of the selected decision, global
divergence alone provides limited evidence that the decision should be
interrupted.

The relevance layer therefore transforms:

```text
System-level mismatch
```

into:

```text
Decision-specific mismatch
```

EXP-004 subsequently demonstrated that relevance itself is not sufficient.

---

## 11. Decision Impact Layer

Implementation:

```text
src/dara_dt/impact/
```

Key components include:

```text
model.py
analyser.py
```

The decision-impact layer evaluates whether relevant divergence changes the
physical validity of the decision.

For a capacity-dependent decision:

\[
M = C - q
\]

where:

- \(C\) is the observed physical capacity; and
- \(q\) is required demand.

Conceptually:

```text
Relevant Divergence
        ↓
Decision Requirement
        ↓
Validity Margin
        ↓
Decision Impact
```

This mechanism was introduced after EXP-004 demonstrated:

> **Relevant divergence does not necessarily imply an invalid decision.**

---

## 12. Evidence Layer

Implementation:

```text
src/dara_dt/evidence/
```

Key components include:

```text
model.py
generator.py
```

The evidence layer represents runtime observations used by the assurance
mechanism.

Evidence can differ from both:

- physical ground truth; and
- Digital Twin state.

Conceptually:

```text
Physical Reality
        ↓
observation process
        ↓
Runtime Evidence
```

The evidence model supports controlled conditions including:

- accurate evidence;
- inaccurate evidence;
- stale evidence;
- missing evidence; and
- conflicting evidence.

This layer is central to EXP-006.

---

# Part II — Runtime Assurance

## 13. Assurance Layer

Implementation:

```text
src/dara_dt/assurance/
```

Current components include:

```text
model.py
policy.py
baselines.py
magnitude_policy.py
impact_policy.py
evidence_policy.py
```

The assurance layer determines whether the proposed autonomous action should
retain authority.

Different policies deliberately use different amounts of information.

This allows controlled comparison of alternative assurance strategies.

---

## 14. No-Assurance Baseline

Conceptually:

```text
AI Decision
        ↓
ALLOW
```

No runtime assurance is applied.

Purpose:

- establish unrestricted autonomy;
- measure missed interventions; and
- provide a baseline against which intervention strategies can be compared.

---

## 15. Global-Divergence Baseline

Conceptually:

```text
Any divergence?
   ↓
 YES → INTERVENE
 NO  → ALLOW
```

This policy treats every detected mismatch as potentially sufficient for
intervention.

It does not evaluate:

- decision dependency;
- decision consequence; or
- evidence quality.

---

## 16. Magnitude-Based Baseline

Conceptually:

```text
Divergence magnitude
        ↓
Fixed threshold
        ↓
ALLOW / INTERVENE
```

This tests whether divergence severity alone can provide an adequate
assurance rule.

EXP-004 and EXP-005 show why a fixed magnitude should not automatically be
interpreted as decision consequence.

---

## 17. Decision-Relevance Policy

Conceptually:

```text
Detected Divergence
        ↓
Decision Dependency Match
        ↓
Relevant?
   ↙          ↘
 NO           YES
 ↓             ↓
ALLOW      INTERVENE
```

This mechanism improves selectivity relative to global divergence in the
early controlled experiments.

However, EXP-004 shows that it can over-intervene when a relevant mismatch
does not invalidate the decision.

---

## 18. Decision-Impact Policy

Conceptually:

```text
Relevant Divergence
        ↓
Decision Requirement
        ↓
Observed Physical Value
        ↓
Validity / Impact
        ↓
Assurance Action
```

This mechanism asks:

> Does the mismatch actually change whether the current decision remains
> feasible?

EXP-005 evaluates this architecture under controlled capacity conditions.

---

## 19. Evidence-Aware Policy

Conceptually:

```text
Runtime Evidence
        ↓
Evidence Status
        ↓
Decision Impact
        ↓
ALLOW / RESTRICT / DEFER
```

The implemented controlled behaviour includes:

```text
MISSING     → DEFER
STALE       → DEFER
CONFLICTING → DEFER
```

For usable capacity evidence:

```text
observed capacity < demand → DEFER

observed capacity = demand → RESTRICT

observed capacity > demand → ALLOW
```

EXP-006 demonstrates that even this architecture can fail when apparently
usable evidence is incorrect.

---

## 20. Autonomous Authority

The assurance layer regulates whether the AI-generated decision retains
authority.

The broader architecture supports the conceptual actions:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
```

### ALLOW

The AI decision retains autonomous authority.

### RESTRICT

The decision is prevented from unrestricted autonomous execution.

### DEFER

The decision is withheld pending additional evidence or another
decision-making mechanism.

### FALLBACK

Control would transfer to an alternative mechanism.

`FALLBACK` is part of the broader architecture but should not be described as
experimentally validated until a fallback controller is explicitly
implemented and evaluated.

---

# Part III — Independent Evaluation

## 21. Evaluation Layer

Implementation:

```text
src/dara_dt/evaluation/
```

Key components include:

```text
outcomes.py
metrics.py
validity.py
```

The evaluation layer is intentionally separate from the assurance policy.

Its role is to determine:

1. whether the decision is physically valid;
2. whether intervention was required;
3. what action the assurance policy produced; and
4. whether that action was correct relative to physical ground truth.

---

## 22. Assurance Outcome Model

Four primary outcomes are used.

```text
                    Ground Truth
               Valid          Invalid

Intervene       FI              TI

Allow           CNI             MI
```

where:

- **TI** = True Intervention;
- **FI** = False Intervention;
- **MI** = Missed Intervention;
- **CNI** = Correct Non-Intervention.

This structure allows the project to measure both:

- protection from invalid autonomous execution; and
- unnecessary loss of autonomy.

---

## 23. Architectural Trade-Off

The system is not designed to optimise intervention recall in isolation.

A policy that intervenes on every decision may obtain high recall while
eliminating autonomous operation.

The architecture therefore exposes the trade-off:

```text
Assurance Effectiveness
        ↕
Autonomy Availability
        ↕
Logistics Performance
```

Current experiments measure assurance effectiveness and autonomy
availability.

Broader logistics-performance evaluation remains an important later stage.

---

# Part IV — Experimental Architecture Evolution

## 24. EXP-001 Architecture

```text
Physical System
        ↓
Digital Twin
        ↓
Decision
        ↓
Divergence Detection
        ↓
Decision Relevance
        ↓
Assurance
```

Purpose:

> Initial B-vs-C relevance pilot.

---

## 25. EXP-002 Architecture

Added controlled policy comparison:

```text
No Assurance
Global Divergence
Decision-Relevant DARA-DT
```

Purpose:

> Compare intervention behaviour across seven controlled conditions.

---

## 26. EXP-003 Architecture

Formalised:

```text
Decision
        ↓
Dependency Mapping

Detected Divergence
        ↓
Decision-Relevance Analysis
        ↓
Relevant / Irrelevant
```

Purpose:

> Make decision relevance an explicit architectural component.

---

## 27. EXP-004 Architecture

EXP-004 exposed the limitation:

```text
Relevant Divergence
        ↓
does not necessarily mean
        ↓
Invalid Decision
```

This required an additional architectural stage.

---

## 28. EXP-005 Architecture

Decision impact was introduced:

```text
Relevant Divergence
        ↓
Decision Requirement
        ↓
Validity Margin
        ↓
Decision Impact
        ↓
Assurance
```

Purpose:

> Determine whether relevant divergence actually changes decision validity.

---

## 29. EXP-006 Architecture

EXP-006 introduced imperfect evidence:

```text
Physical Ground Truth
        │
        │ observation
        ↓
Runtime Evidence
        ↓
Decision Impact
        ↓
Evidence-Aware Assurance
```

while independent evaluation continues to use:

```text
Physical Ground Truth
```

This separation prevents the runtime evidence used by the policy from also
defining the experimental truth.

---

## 30. Current Integrated Architecture

The current research architecture can therefore be represented as:

```text
┌─────────────────────────────┐
│ Physical Logistics System   │
└─────────────┬───────────────┘
              │
       ┌──────┴───────┐
       │              │
       ↓              ↓
Digital Twin     Runtime Evidence
       │              │
       ↓              │
AI Decision           │
       │              │
       ↓              │
Decision Dependencies │
       │              │
       └──────┬───────┘
              ↓
      Divergence Detection
              ↓
     Decision Relevance
              ↓
      Decision Impact
              ↓
      Evidence Reliability
              ↓
      Runtime Assurance
              ↓
     Autonomous Authority
              ↓
     Executed / Withheld
              │
              ↓
     Independent Evaluation
```

This is the current conceptual integration of the implemented research
components.

---

# Part V — Implementation Map

## 31. Repository Architecture

```text
src/
└── dara_dt/
    ├── simulation/
    │   ├── vehicle.py
    │   ├── order.py
    │   └── environment.py
    │
    ├── twin/
    │   └── digital_twin.py
    │
    ├── divergence/
    │   ├── detector.py
    │   ├── injector.py
    │   └── relevance.py
    │
    ├── decision/
    │   ├── model.py
    │   ├── dependency.py
    │   └── controller.py
    │
    ├── impact/
    │   ├── model.py
    │   └── analyser.py
    │
    ├── evidence/
    │   ├── model.py
    │   └── generator.py
    │
    ├── assurance/
    │   ├── model.py
    │   ├── policy.py
    │   ├── baselines.py
    │   ├── magnitude_policy.py
    │   ├── impact_policy.py
    │   └── evidence_policy.py
    │
    ├── evaluation/
    │   ├── outcomes.py
    │   ├── metrics.py
    │   └── validity.py
    │
    └── experiments/
        └── controlled experiment modules
```

This modular structure separates:

```text
world representation
decision generation
assurance reasoning
experimental evaluation
```

so that individual mechanisms can be changed without silently redefining the
entire system.

---

## 32. Experimental Modules

The experiment package currently contains modules supporting:

- B-vs-C pilot evaluation;
- controlled relevance conditions;
- divergence-count experiments;
- seven-condition policy comparison;
- severity experiments;
- decision-impact experiments;
- imperfect-evidence experiments; and
- aggregate metrics.

Representative modules include:

```text
bc_pilot.py
divergence_count.py
experimental_matrix.py
matrix_metrics.py
relevance_conditions.py
relevance_generator.py
severity_conditions.py
severity_experiment.py
impact_conditions.py
impact_experiment.py
impact_metrics.py
evidence_conditions.py
evidence_experiment.py
evidence_metrics.py
```

The exact experiment documentation should remain the authoritative source for
the interpretation of each experiment.

---

## 33. Testing Architecture

Automated tests cover major architectural components including:

- simulation state;
- Digital Twin behaviour;
- divergence detection;
- dependency mapping;
- decision relevance;
- assurance policies;
- controlled experiment generation;
- physical validity;
- decision impact;
- runtime evidence; and
- aggregate experimental metrics.

At the latest verified checkpoint:

```text
275 tests passed
```

This supports implementation correctness for the tested behaviours.

It does not by itself establish scientific validity or real-world
effectiveness.

---

## 34. Continuous Integration

The repository's automated workflow performs:

```text
Repository checkout
        ↓
Python 3.12 setup
        ↓
uv dependency installation
        ↓
pytest
        ↓
B-vs-C pilot
        ↓
Controlled matrix
        ↓
Aggregate matrix metrics
        ↓
EXP-005 impact metrics
        ↓
EXP-006 evidence metrics
```

This provides a reproducible verification path for the implemented
experimental stages.

---

# Part VI — Architecture Boundaries

## 35. Implemented

The current prototype contains implemented components for:

- logistics simulation;
- Digital Twin state;
- vehicle-assignment decisions;
- divergence detection;
- decision dependency mapping;
- decision relevance;
- divergence magnitude;
- decision impact;
- physical validity;
- runtime evidence;
- baseline assurance policies;
- evidence-aware assurance;
- outcome classification;
- metrics;
- controlled experiments; and
- automated testing.

---

## 36. Experimentally Evaluated

Controlled experimental evidence currently exists for:

- decision relevance;
- irrelevant versus relevant divergence;
- divergence-count variation;
- operational-status divergence;
- availability divergence;
- capacity divergence;
- divergence severity;
- decision validity boundaries;
- decision-impact reasoning;
- exact-boundary behaviour; and
- imperfect capacity evidence.

The depth of evidence is not equal across all categories.

Later experiments are substantially more capacity-focused.

---

## 37. Planned or Not Yet Fully Validated

The following should remain clearly identified as future or incomplete work:

- cross-dependency impact generalisation;
- compound divergence evaluation;
- broad stochastic testing;
- learned AI decision controllers;
- full routing optimisation evaluation;
- adaptive fallback controllers;
- large-scale logistics simulation;
- extensive logistics-performance analysis;
- computational scalability;
- real sensor integration;
- probabilistic evidence fusion;
- deployment-level runtime assurance; and
- real-world validation.

These should not be represented as completed capabilities.

---

# Part VII — Next Architectural Stage

## 38. EXP-007 Requirement

The current architecture has developed strongly around capacity-based
decision impact.

The next experiment should therefore test whether the architecture can apply
the same reasoning across different decision dependencies.

Proposed dependency families are:

```text
Capacity
Operational Status
Location / Availability
```

The intended question is:

> **Does the relationship between divergence, decision relevance, decision
> impact and runtime intervention generalise across different logistics
> decision dependencies?**

EXP-007 should initially use reliable evidence.

This prevents evidence uncertainty from becoming a confounding variable while
dependency generalisation is being tested.

---

## 39. Architecture Extension Principle

New components should only be added when required by a research question.

The project should avoid introducing technologies merely to increase apparent
complexity.

Examples that should not become independent architecture streams without
experimental justification include:

- blockchain;
- large language models;
- multi-agent systems;
- complex cybersecurity infrastructure;
- event-streaming platforms;
- large cloud deployments; and
- dashboards.

Architectural complexity must remain subordinate to the research question.

---

## 40. Research Integrity

The architecture should distinguish:

```text
IMPLEMENTED
```

from:

```text
EXPERIMENTALLY VALIDATED
```

from:

```text
PLANNED
```

An implemented component is not automatically scientifically validated.

Likewise, a conceptual architecture diagram does not establish operational
effectiveness.

All architectural claims should therefore remain traceable to:

- source code;
- tests;
- experiment results; or
- clearly identified future work.

---

## 41. Current Architecture Position

The current DARA-DT architecture embodies the following progression:

```text
Physical–Digital Divergence
        ↓
Decision Relevance
        ↓
Decision Impact / Validity
        ↓
Evidence Reliability
        ↓
Decision Risk
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

The strongest current implementation and controlled evidence exists through:

```text
Divergence
        ↓
Relevance
        ↓
Impact / Validity
        ↓
Evidence-Aware Assurance
```

`Decision Risk` remains a developing integration concept rather than a fully
validated independent subsystem.

This distinction should remain explicit.

---

## 42. Conclusion

DARA-DT is implemented as a modular research architecture for investigating
runtime assurance under physical–digital divergence.

The architecture separates:

```text
What is physically true?
        ↓
What does the Digital Twin represent?
        ↓
What evidence does assurance receive?
        ↓
What decision is the AI proposing?
        ↓
Which divergent state matters to that decision?
        ↓
Does the divergence change physical validity?
        ↓
How reliable is the evidence?
        ↓
What autonomous authority should be retained?
```

The architecture has evolved through EXP-001 to EXP-006 rather than being
fixed in advance.

Each experimental stage has either supported or exposed a limitation in the
previous architecture.

The next architectural challenge is not to add more components.

It is to determine whether the existing divergence → relevance → impact
mechanism generalises beyond capacity to multiple logistics decision
dependencies.

That question forms the basis of EXP-007.
