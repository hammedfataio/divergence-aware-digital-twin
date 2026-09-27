# DARA-DT Research Methodology

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Research Area:** Trustworthy Intelligent Systems  
**Application Domain:** Autonomous Logistics Systems  
**Methodology Status:** Active Experimental Prototype  
**Completed Experimental Stages:** EXP-001 to EXP-006  
**Next Validation Stage:** Cross-Dependency Generalisation

---

## 1. Methodological Purpose

DARA-DT investigates how physical–digital divergence should influence the
authority granted to AI-generated decisions in dynamic logistics Digital
Twins.

The central research question is:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

The methodology is designed around controlled experimentation.

Rather than assuming that all physical–digital mismatch requires
intervention, the research progressively evaluates whether intervention
should depend on:

1. divergence presence;
2. decision relevance;
3. decision impact and physical validity;
4. runtime evidence reliability; and
5. ultimately the risk associated with allowing autonomous execution.

The methodology therefore follows a **progressive falsification and
refinement strategy**.

---

## 2. Research Design

The project uses an experimental software-research methodology combining:

- discrete logistics simulation;
- explicit Digital Twin state;
- controlled divergence injection;
- AI-supported decision generation;
- decision dependency modelling;
- runtime assurance policies;
- independent physical ground truth;
- comparative baselines;
- automated testing; and
- reproducible experiment runners.

The purpose is to isolate individual assurance mechanisms before increasing
system complexity.

The experimental structure is:

```text
Physical Logistics Environment
        ↓
Digital Twin Synchronisation
        ↓
Controlled Physical Change
        ↓
Physical–Digital Divergence
        ↓
AI-Generated Decision
        ↓
Decision Dependency Analysis
        ↓
Divergence Relevance
        ↓
Decision Impact / Validity
        ↓
Evidence Reliability
        ↓
Runtime Assurance
        ↓
Autonomous Authority
        ↓
Independent Outcome Evaluation
```

Not every experiment uses every stage.

The pipeline has been expanded progressively as earlier experiments exposed
limitations.

---

## 3. Methodological Principle

The core methodological principle is:

> **An assurance mechanism must not define the ground truth against which its
> own behaviour is evaluated.**

The project therefore separates:

```text
Physical Ground Truth
```

from:

```text
Digital Twin State
```

and, where applicable:

```text
Runtime Evidence
```

This separation allows the experimental evaluator to determine whether an
AI-generated decision is physically valid independently of the assurance
policy.

---

## 4. Physical Logistics Environment

The physical environment represents the current operational logistics state.

The implemented prototype includes entities such as:

- vehicles;
- orders;
- vehicle location;
- vehicle capacity;
- vehicle operational status; and
- vehicle availability.

The physical environment acts as the authoritative state for controlled
experimental evaluation.

For example:

```text
Physical vehicle:
capacity = 4

Digital Twin vehicle:
capacity = 10

Order demand:
5
```

The Twin may consider the vehicle suitable, while the physical environment
shows that the assignment is infeasible.

This creates a measurable physical–digital divergence.

---

## 5. Digital Twin Representation

The Digital Twin maintains a digital representation of the logistics
environment.

At the beginning of a controlled scenario, the Twin can be synchronised with
the physical environment.

A physical change is then introduced without immediately updating the Twin.

This produces controlled divergence:

```text
t0
Physical System = Digital Twin

        ↓

physical change occurs

        ↓

t1
Physical System ≠ Digital Twin
```

This design allows the experiment to know:

- when divergence begins;
- which variable diverges;
- the magnitude or category of divergence;
- which decision depends on that variable; and
- whether the resulting decision remains physically valid.

---

## 6. Controlled Divergence Injection

Divergence is deliberately introduced after synchronisation.

Current and planned divergence categories include:

### Temporal Divergence

Examples:

- delayed telemetry;
- stale state;
- communication delay.

### State Divergence

Examples:

- incorrect vehicle capacity;
- incorrect location;
- incorrect availability.

### Operational Divergence

Examples:

- unreported vehicle breakdown;
- unavailable resource represented as available.

### Distributional Divergence

Examples for later investigation may include:

- unusual demand;
- extreme congestion;
- operational conditions outside previously observed patterns.

### Compound Divergence

Multiple divergence types may occur simultaneously.

Not all categories have received equal experimental validation.

Current claims should therefore remain tied to the specific implemented
conditions.

---

## 7. AI Decision Layer

The prototype contains a decision controller that generates logistics
decisions from the Digital Twin representation.

Current controlled experiments primarily use vehicle-assignment decisions.

Conceptually:

```text
Digital Twin State
        ↓
Decision Controller
        ↓
Vehicle Assignment
```

The research is not primarily evaluating whether the decision controller is
the most advanced logistics optimisation algorithm.

Instead, the controller provides a reproducible decision whose dependencies
can be inspected and whose physical validity can be evaluated after
divergence occurs.

This isolates the runtime-assurance problem.

---

## 8. Decision Dependencies

Each autonomous decision depends on particular state variables.

For decision \(d_t\), define:

\[
Dep(d_t)
\]

as the set of state variables required by the decision.

For example, assigning a vehicle to an order may depend on:

- vehicle identity;
- capacity;
- operational status;
- availability; and
- location.

Explicit dependency modelling enables the assurance system to distinguish
global system mismatch from mismatch affecting the current decision.

---

## 9. Divergence Detection

The divergence detector compares physical and Digital Twin state.

Conceptually:

\[
D_t = \{s_i : s_i^{physical} \neq s_i^{twin}\}
\]

where \(D_t\) is the set of detected physical–digital divergences at time
\(t\).

Each divergence can contain information such as:

- affected entity;
- state variable;
- physical value;
- Digital Twin value; and
- divergence magnitude where applicable.

Divergence detection answers:

> **Where does the Digital Twin differ from the physical system?**

It does not, by itself, determine whether autonomous intervention is
required.

---

## 10. Decision-Relevance Analysis

Decision relevance combines detected divergence with decision dependencies.

For decision \(d_t\):

\[
D_t^{rel}(d_t) = Dep(d_t) \cap D_t
\]

Conceptually:

```text
Detected Divergence
        +
Decision Dependencies
        ↓
Decision-Relevance Analysis
       ↙ ↘
 Relevant   Irrelevant
```

This answers:

> **Does the detected mismatch affect something this particular decision
> depends on?**

EXP-001 to EXP-003 established the controlled relevance mechanism.

EXP-004 subsequently demonstrated that relevance alone is insufficient for
determining physical validity.

---

## 11. Decision Impact and Physical Validity

Decision-impact reasoning evaluates whether relevant divergence changes the
physical feasibility of the current decision.

For a capacity-dependent assignment:

\[
M = C_{physical} - q
\]

where:

- \(C_{physical}\) is physical vehicle capacity;
- \(q\) is order demand; and
- \(M\) is the physical validity margin.

The independent physical rule is:

\[
C_{physical} \geq q
\]

for a valid assignment, and:

\[
C_{physical} < q
\]

for an invalid assignment.

This introduces an important distinction:

```text
Decision Relevance
        ↓
Does the mismatch affect a decision dependency?

Decision Impact
        ↓
Does the mismatch change whether the decision remains valid?
```

EXP-004 and EXP-005 investigate this distinction.

---

## 12. Runtime Evidence

A deployed assurance mechanism may not have direct access to perfect physical
ground truth.

EXP-006 therefore introduces a separate runtime evidence layer.

The methodological separation becomes:

```text
Physical Ground Truth
        ≠
Runtime Evidence
        ≠
Digital Twin State
```

Runtime evidence may be:

- accurate;
- inaccurate;
- stale;
- missing;
- conflicting; or
- misleading.

Ground truth remains available to the experimental evaluator but is not
assumed to be perfectly available to the evidence-aware assurance policy.

This allows robustness under imperfect observation to be tested.

---

## 13. Runtime Assurance Policies

The project uses multiple assurance strategies rather than evaluating the
proposed mechanism in isolation.

### No Assurance

Autonomous execution is permitted without runtime intervention.

Purpose:

> Establish the consequence of unrestricted autonomy.

### Global Divergence

Any detected physical–digital mismatch causes intervention.

Purpose:

> Test whether divergence presence alone is an adequate assurance rule.

### Fixed-Magnitude Assurance

Intervention depends on a predefined divergence threshold.

Purpose:

> Test whether divergence severity alone can provide adequate selectivity.

### Decision-Relevance Assurance

Intervention depends on whether divergence affects a dependency of the
current decision.

Purpose:

> Test the value and limitations of dependency-specific relevance.

### Decision-Impact Assurance

Intervention depends on whether divergence affects the physical validity of
the current decision.

Purpose:

> Test whether consequence-aware reasoning improves intervention
> selectivity.

### Evidence-Aware Decision Impact

Impact reasoning uses imperfect runtime evidence rather than assuming perfect
physical-state knowledge.

Purpose:

> Test robustness when assurance evidence is degraded.

---

## 14. Assurance Actions

Depending on the experimental policy, the assurance layer can produce
actions conceptually including:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
```

Current experiments primarily operationalise:

- unrestricted execution;
- restriction; and
- defer/intervention behaviour.

`FALLBACK` remains part of the broader architecture and should only be
claimed as experimentally evaluated when a fallback controller is explicitly
tested.

---

## 15. Independent Ground Truth

Ground truth is derived from the physical environment.

For each controlled scenario, the evaluator determines whether autonomous
execution should physically remain valid.

The assurance action is then compared against that independent requirement.

This produces four principal outcome classes.

### True Intervention — TI

```text
Invalid physical decision
+
Assurance intervenes
```

### False Intervention — FI

```text
Valid physical decision
+
Assurance intervenes
```

### Missed Intervention — MI

```text
Invalid physical decision
+
Assurance allows execution
```

### Correct Non-Intervention — CNI

```text
Valid physical decision
+
Assurance allows execution
```

---

## 16. Evaluation Metrics

The methodology evaluates more than simple accuracy.

### Assurance Metrics

- true interventions;
- false interventions;
- missed interventions;
- correct non-interventions;
- intervention accuracy;
- precision;
- recall;
- false-intervention rate; and
- missed-intervention rate.

### Autonomy Metrics

- autonomy availability;
- intervention frequency;
- restriction frequency;
- defer frequency; and
- fallback frequency where implemented.

### Logistics Metrics

Broader evaluation should include:

- route distance;
- operational cost;
- lateness;
- service rate;
- utilisation; and
- recovery performance.

### Digital Twin Metrics

Relevant future measures include:

- state-estimation error;
- synchronisation error;
- divergence magnitude;
- divergence duration; and
- detection latency.

### Computational Metrics

Later evaluation should include:

- assurance computation time;
- end-to-end decision latency; and
- scalability.

---

## 17. Assurance–Autonomy–Performance Trade-Off

A runtime-assurance mechanism should not be judged only by whether it
intervenes on invalid decisions.

A policy could obtain high intervention recall simply by preventing every
autonomous action.

The methodology therefore considers the trade-off:

```text
Assurance Effectiveness
        ↕
Autonomy Availability
        ↕
Logistics Performance
```

The current experiments have begun measuring the first two dimensions.

Full system-level logistics-performance evaluation remains a later research
stage.

---

## 18. Experimental Programme

### EXP-001 — Decision-Relevance B-vs-C Pilot

Purpose:

> Test whether equal divergence counts can have different significance to
> the current decision.

Contribution:

- initial feasibility demonstration;
- separation of divergence count from decision significance.

---

### EXP-002 — Controlled Policy Comparison

Purpose:

> Compare No Assurance, Global Divergence and Decision-Relevant DARA-DT
> across a seven-condition matrix.

Contribution:

- controlled comparison;
- demonstrated limitations of global divergence intervention;
- provided initial evidence for decision-specific relevance.

---

### EXP-003 — Decision-Relevance Analysis

Purpose:

> Validate explicit mapping between detected divergence and the dependencies
> of the current decision.

Contribution:

- operational decision-dependency matching;
- relevant/irrelevant divergence separation.

---

### EXP-004 — Divergence Severity

Purpose:

> Test whether every decision-relevant divergence requires intervention.

Contribution:

- demonstrated that relevant divergence can coexist with a physically valid
  decision;
- identified the decision-validity boundary as an important additional
  factor.

---

### EXP-005 — Decision Impact

Purpose:

> Evaluate whether decision-specific validity reasoning improves intervention
> selectivity.

Contribution:

- controlled 15-condition capacity matrix;
- equal-divergence/different-impact comparison;
- explicit validity-margin reasoning;
- exposed exact-boundary policy behaviour.

---

### EXP-006 — Imperfect Evidence

Purpose:

> Test decision-impact-aware assurance when runtime evidence is imperfect.

Contribution:

- separation of ground truth, runtime evidence and Twin state;
- controlled missing, stale, conflicting and incorrect evidence;
- demonstrated both false and missed intervention under imperfect evidence.

---

### EXP-007 — Cross-Dependency Generalisation

**Status:** Planned.

Proposed purpose:

> Test whether the relationship between divergence, decision relevance,
> decision impact and runtime intervention generalises across multiple
> logistics decision dependencies.

Candidate dependencies:

- capacity;
- operational status; and
- location or availability.

No EXP-007 results should be reported until implementation and validation are
complete.

---

## 19. Progressive Experimental Logic

The methodology follows a cumulative sequence:

```text
EXP-001
Can divergence quantity misrepresent decision significance?
        ↓
EXP-002
Do different assurance strategies behave differently?
        ↓
EXP-003
Can divergence be mapped to decision dependencies?
        ↓
EXP-004
Is decision relevance sufficient?
        ↓
EXP-005
Does decision impact improve consequence reasoning?
        ↓
EXP-006
What happens when evidence is imperfect?
        ↓
EXP-007
Does the mechanism generalise across dependency types?
```

Each experiment either supports, challenges or refines the mechanism developed
in the previous stage.

---

## 20. Controlled Benchmark Structure

The broader benchmark methodology organises scenarios into divergence
families such as:

```text
D0 — Synchronized
D1 — Temporal Divergence
D2 — State Divergence
D3 — Operational Divergence
D4 — Distributional Divergence
D5 — Compound Divergence
```

These categories define the intended broader stress-test structure.

However, implementation maturity differs across categories.

Documentation must distinguish between:

```text
Implemented and experimentally evaluated
```

and:

```text
Proposed benchmark coverage
```

until all categories have executable evidence.

---

## 21. Baseline Philosophy

Baselines are retained even when they perform poorly.

The methodology deliberately avoids modifying baseline policies merely to
make the proposed mechanism appear stronger.

Relevant baselines include:

- unrestricted autonomy;
- any-divergence intervention;
- fixed thresholds;
- decision relevance;
- deterministic impact; and
- evidence-aware impact.

Future work may compare against additional established runtime-assurance or
operational-envelope approaches where they can be implemented fairly.

---

## 22. Reproducibility Strategy

The project is structured as an executable research prototype.

Reproducibility is supported through:

- explicit experiment modules;
- deterministic controlled conditions where appropriate;
- automated tests;
- dependency-managed Python environments;
- version-controlled source code;
- experiment-specific documentation;
- aggregate metric runners; and
- continuous integration.

The project uses Python 3.12+ and `uv` for dependency and environment
management.

Example experiment execution includes:

```bash
uv run python -m dara_dt.experiments.run_pilot
uv run python -m dara_dt.experiments.run_matrix
uv run python -m dara_dt.experiments.run_metrics
uv run python -m dara_dt.experiments.impact_metrics
uv run python -m dara_dt.experiments.evidence_metrics
```

The full automated test suite can be executed using:

```bash
uv run pytest -v
```

At the latest verified experimental checkpoint:

```text
275 tests passed
```

Future repository changes should rerun the complete test suite before new
results are treated as verified.

---

## 23. Implementation Structure

The research prototype separates responsibilities across modules.

### Simulation

```text
src/dara_dt/simulation/
```

Represents the physical logistics environment.

### Digital Twin

```text
src/dara_dt/twin/
```

Maintains the digital representation of logistics state.

### Divergence

```text
src/dara_dt/divergence/
```

Detects and analyses physical–digital mismatch.

### Decision

```text
src/dara_dt/decision/
```

Represents autonomous decisions and their dependencies.

### Assurance

```text
src/dara_dt/assurance/
```

Contains baseline and developing runtime-assurance policies.

### Impact

```text
src/dara_dt/impact/
```

Evaluates decision-specific consequence and validity information.

### Evidence

```text
src/dara_dt/evidence/
```

Represents runtime evidence and controlled evidence degradation.

### Evaluation

```text
src/dara_dt/evaluation/
```

Provides physical ground-truth and assurance-outcome evaluation.

### Experiments

```text
src/dara_dt/experiments/
```

Contains controlled experimental conditions, runners and metric aggregation.

This separation supports traceability between the conceptual framework and
the executable prototype.

---

## 24. Validity Strategy

The methodology considers several forms of validity.

### Internal Validity

Controlled divergence injection allows the manipulated condition to be known
precisely.

### Construct Validity

Key concepts are separated explicitly:

```text
divergence
≠
decision relevance
≠
decision impact
≠
evidence reliability
≠
assurance outcome
```

### External Validity

External validity is currently limited.

The experiments use controlled logistics scenarios and should not be treated
as representative of all operational Digital Twins.

### Conclusion Validity

Current deterministic matrices support bounded mechanism-level conclusions.

Broader statistical claims require repeated stochastic evaluation.

---

## 25. Threats to Validity

### Simplified Logistics Environment

The prototype deliberately reduces operational complexity to isolate
assurance mechanisms.

### Capacity Concentration

The strongest later experiments remain heavily focused on vehicle capacity.

This is the primary motivation for cross-dependency evaluation.

### Explicit Decision Dependencies

Current dependencies are directly represented.

Dependencies in learned AI systems may be implicit or difficult to identify.

### Controlled Evidence Model

EXP-006 introduces imperfect evidence but does not yet reproduce the full
complexity of operational telemetry.

### Limited Stochastic Evaluation

More repeated trials and stochastic disruption scenarios are required before
making broader statistical claims.

### Limited Performance Evaluation

The current work emphasises assurance behaviour more strongly than end-to-end
logistics performance.

### Prototype Scale

The current architecture has not yet established scalability to large,
real-time Digital Twin deployments.

---

## 26. Falsification Strategy

DARA-DT is treated as a research hypothesis rather than a predetermined
solution.

The hypothesis should be revised if evidence shows that:

- decision relevance provides no useful information beyond global divergence;
- decision impact provides no useful information beyond simple thresholds;
- the mechanism works only for capacity;
- evidence degradation makes assurance behaviour unreliable;
- simpler policies perform equivalently across broader conditions;
- autonomy loss outweighs assurance benefit;
- computational overhead prevents runtime application; or
- the proposed concepts cannot be operationalised consistently.

Negative experimental results should therefore remain visible in the
research record.

---

## 27. Claim Discipline

Repository claims are divided into three categories.

### Implemented

The mechanism exists in executable source code.

### Experimentally Observed

The behaviour has been demonstrated within a defined controlled experiment.

### Proposed

The concept is planned but has not yet received sufficient experimental
validation.

This distinction prevents architecture plans or future research directions
from being presented as completed findings.

---

## 28. Current Methodological Position

The evidence accumulated through EXP-006 supports the following bounded
progression:

```text
Divergence presence alone
        ↓
too coarse for selective intervention

Decision relevance
        ↓
adds decision-specific context

Decision relevance alone
        ↓
does not determine physical validity

Decision impact
        ↓
improves consequence reasoning in controlled capacity conditions

Decision impact under imperfect evidence
        ↓
can still produce incorrect assurance decisions

Cross-dependency evaluation
        ↓
required before broader generalisation
```

This is the current methodological position.

---

## 29. Next Methodological Stage

The immediate next step should test **cross-dependency generalisation**.

The principal question is:

> **Does the relationship between divergence, decision relevance, decision
> impact and runtime intervention generalise across different logistics
> decision dependencies?**

The experiment should initially keep evidence reliable so that dependency
type remains the primary manipulated variable.

Candidate dependencies are:

```text
Capacity
Operational Status
Location / Availability
```

Only after this relationship is understood should broader evidence
uncertainty be combined with multiple dependency types.

This prevents unnecessary experimental confounding.

---

## 30. Methodological Summary

The DARA-DT methodology is built around a simple but progressively refined
question:

```text
Is the Digital Twin different from physical reality?
        ↓
Does the difference affect this decision?
        ↓
Does it change the decision's physical validity?
        ↓
Can the evidence supporting that conclusion be trusted?
        ↓
Should autonomous authority be retained?
```

The project uses controlled simulation, explicit divergence injection,
decision dependencies, independent physical ground truth, comparative
assurance policies and automated validation to investigate these questions.

The methodology is intentionally incremental.

Each experiment is expected to challenge the assumptions introduced by the
previous stage rather than merely produce favourable results.

This provides the methodological foundation for continued evaluation of
divergence-aware runtime assurance in autonomous logistics Digital Twins.
