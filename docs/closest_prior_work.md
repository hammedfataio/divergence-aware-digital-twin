# Closest Prior Work and Research Differentiation

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Research Area:** Trustworthy Intelligent Systems  
**Application Domain:** Autonomous Logistics Systems  
**Document Status:** Living Prior-Work and Novelty-Control Document  
**Evidence Base:** Literature audit + EXP-001 to EXP-009  
**Last Research Position:** September 2026  
**Novelty Status:** Not Yet Established

---

# 1. Purpose

This document identifies the research areas, systems and mechanisms currently
closest to DARA-DT.

Its purpose is not to defend novelty.

Its purpose is to determine whether the proposed research contribution is:

- already established;
- directly represented by existing research;
- an incremental adaptation;
- an integration of known mechanisms;
- experimentally distinguishable from strong alternatives; or
- sufficiently unresolved to justify further investigation.

DARA-DT must not claim:

```text
"first"
"unique"
"no previous research"
"novel"
"superior to existing runtime assurance"
```

unless systematic literature and experimental evidence justify such claims.

The current position is:

> **DARA-DT is a research hypothesis and experimental framework whose
> differentiation remains under active falsification.**

---

# 2. Central Research Question

The canonical research question is:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

The current conceptual chain is:

```text
Physical–Digital Divergence
        ↓
Decision Dependency
        ↓
Decision Relevance
        ↓
Decision Impact / Validity
        ↓
Evidence Reliability
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

Following EXP-007 through EXP-009, a further question must now be attached:

```text
Autonomous Authority
        ↓
Can a simpler strong runtime-assurance mechanism
produce the same result?
```

This strong-baseline comparison is now central to the research.

---

# Part I — Digital Twin Assurance

## 3. Digital Twin Assurance Is Established

Digital Twin assurance already addresses concerns including:

- fidelity;
- synchronisation;
- data quality;
- model validation;
- uncertainty;
- trustworthiness;
- operational monitoring;
- lifecycle assurance;
- model-performance monitoring;
- assurance evidence.

Therefore DARA-DT does not treat the following as novel:

```text
Digital Twins require assurance.
```

Nor does it treat:

```text
Digital Twins can become inconsistent with physical reality.
```

as a novel observation.

The relevant question must be narrower.

---

# 4. DNV-RP-A204

DNV-RP-A204 provides structured guidance for assurance of Digital Twins.

Its relevance includes:

- Twin quality;
- trustworthiness;
- risk associated with relying on Twin information;
- deployment;
- operation;
- maintenance;
- lifecycle assurance.

This creates an important prior-work boundary.

DARA-DT should not be positioned as a replacement for Digital Twin assurance
standards.

The DARA-DT research question operates at a different experimental level:

```text
Digital Twin assurance:
Can information from this Twin be trusted for its intended use?

DARA-DT investigation:
Given a particular autonomous decision,
does a physical–digital mismatch affect information required by that
decision and alter whether autonomous execution remains justified?
```

The distinction is useful.

It is not yet evidence of novelty.

---

# 5. Continuous Digital Twin Assurance

A broad claim that Digital Twin assurance is primarily static is no longer
defensible.

Contemporary research explicitly investigates continuous runtime assurance.

The strongest example currently identified for this project is DARTER.

---

# 6. DARTER

The Alan Turing Institute's:

**DARTER — Digital Twin Assurance via Runtime Trust and Evidence Reporting**

is among the closest current projects to the general DARA-DT research area.

DARTER investigates continuous assurance for safety-critical Digital Twins.

Its runtime assurance pipeline includes:

- incoming-data verification;
- model-performance evaluation;
- validated thresholds;
- structured evidence generation;
- operational-design-domain monitoring;
- distribution-drift monitoring;
- continuously maintained assurance evidence.

Its primary testbed is air traffic management.

Its methodology is intended to transfer across other safety-critical domains,
including transportation and logistics.

---

# 7. DARTER Novelty Threat

DARTER creates a very strong threat to claims such as:

```text
DARA-DT introduces runtime Digital Twin assurance.

DARA-DT introduces continuous Digital Twin assurance.

DARA-DT introduces runtime evidence for Twin assurance.

DARA-DT introduces monitoring of Twin trustworthiness.

DARA-DT is the first system to adapt assurance as a Twin changes.
```

These formulations must not be used.

### Threat Level

```text
VERY HIGH
```

---

# 8. DARA-DT vs DARTER

The current candidate distinction is not:

```text
Static Assurance
        vs
Runtime Assurance
```

because DARTER already operates continuously.

A more precise comparison is:

```text
DARTER-type question:

Can the Digital Twin, its data and its predictions continue to be trusted
within the conditions for which they have been validated?
```

versus:

```text
DARA-DT question:

Given an AI-generated operational decision,
what physical–digital divergences affect the state relationships on which
that decision depends, and what should those divergences imply for the
authority of that decision?
```

This is a narrower distinction.

However, later prior work introduces significant overlap even with this
formulation.

---

# Part II — Runtime Assurance

## 9. Runtime Assurance Is Established

Runtime assurance predates DARA-DT.

Existing approaches include:

- Simplex architectures;
- safety monitors;
- runtime verification;
- operational envelopes;
- safety filters;
- fallback controllers;
- runtime assumption monitoring;
- safety cages;
- runtime controller switching;
- reachability-based protection;
- adaptive assurance;
- runtime certification evidence.

Therefore:

```text
monitor system
        ↓
detect unsafe condition
        ↓
restrict autonomous behaviour
```

is not itself a research contribution.

---

# 10. Runtime Assumption Monitoring

Runtime assumption monitoring presents a particularly serious overlap.

Such mechanisms evaluate whether assumptions relied upon by a system remain
valid during operation.

Conceptually:

```text
Decision / System Assumption
        ↓
Runtime Observation
        ↓
Assumption Still Valid?
        ↓
Continue / Restrict / Intervene
```

A DARA-DT decision dependency can potentially be represented as such an
assumption.

For example:

```text
Decision:
Assign vehicle_01 to order_01

Required dependency:
vehicle_01.capacity

Operational assumption:
vehicle_01.capacity >= order_01.demand
```

A runtime contract or assumption monitor may therefore capture much of the
same intervention logic.

This concern is no longer merely conceptual.

It is supported by the DARA-DT experimental results.

---

# 11. Experimental Runtime-Contract Threat

EXP-007 first exposed runtime-contract equivalence.

Across 12 cross-dependency conditions:

```text
Decision Impact:
12 / 12 correct

Runtime Contract:
12 / 12 correct
```

EXP-008 reproduced the threat under imperfect evidence.

```text
Uncertainty-Aware Contract:
TI  = 12
FI  = 9
MI  = 0
CNI = 3

DARA-DT:
TI  = 12
FI  = 9
MI  = 0
CNI = 3
```

EXP-009 challenged the equivalence again using decision-relevant and
decision-irrelevant evidence uncertainty.

The result remained:

```text
Uncertainty-Aware Contract:
TI  = 21
FI  = 9
MI  = 0
CNI = 12
Autonomy = 0.286

DARA-DT:
TI  = 21
FI  = 9
MI  = 0
CNI = 12
Autonomy = 0.286
```

Therefore:

> **Runtime-contract equivalence is currently an experimentally demonstrated
> threat to the DARA-DT contribution.**

---

# Part III — Dependency-Aware Runtime Assurance

## 12. Dependency-Aware Assurance Is a Major 2026 Threat

Recent research on assured AI-native control loops introduces an especially
important challenge to the next stage of DARA-DT.

The work considers autonomous control loops whose decisions:

- depend on shared system state;
- operate concurrently;
- rely on assumptions that can later become invalid;
- interact through shared resources;
- may require runtime conflict resolution.

The proposed research direction associates decisions with:

```text
Assumptions
+
Dependencies
```

and monitors changes capable of invalidating previously accepted decisions.

This significantly overlaps with a broad formulation of:

```text
Decision
        ↓
Dependencies
        ↓
Runtime State Change
        ↓
Decision Invalidated
        ↓
Runtime Intervention
```

---

# 13. Consequence for DARA-DT

The following can no longer be treated as a sufficiently distinctive
contribution by themselves:

```text
decision dependencies

dependency-aware assurance

cross-entity dependencies

monitoring state changes that invalidate decisions

interaction between autonomous decisions

runtime dependency validation
```

These concepts remain useful to DARA-DT.

They cannot alone support the novelty argument.

### Threat Level

```text
VERY HIGH
```

---

# Part IV — Mission-Level Runtime Assurance

## 14. Mission-Level Assurance

Recent runtime-assurance work also extends evaluation beyond immediate local
safety.

Mission-level runtime assurance investigates whether an autonomous command is
not merely locally executable, but whether it preserves the feasibility of the
larger mission.

This is important because it demonstrates that:

```text
Locally acceptable action
        ≠
Globally acceptable autonomous behaviour
```

A command can satisfy immediate safety constraints while still making the
overall mission infeasible.

---

# 15. Consequence for DARA-DT

DARA-DT must therefore not claim as novel the general idea that:

```text
a locally valid decision may still create a downstream system problem.
```

That problem is already represented in contemporary runtime-assurance
research.

A DARA-DT contribution would require a more specific connection to:

```text
physical–digital divergence
        ↓
dependency / decision chain
        ↓
downstream operational consequence
```

and experimental differentiation from strong mission-level or
dependency-aware assurance mechanisms.

---

# Part V — Cooperative and Composed Runtime Assurance

## 16. Synergistic and Composed Assurance

Recent autonomous-system research also investigates cooperative runtime
assurance across components rather than treating every monitor independently.

This matters because a future DARA-DT experiment involving multiple
interacting entities cannot assume that:

```text
multi-component assurance
```

or:

```text
interacting safety monitors
```

is automatically novel.

The relevant question remains whether physical–digital divergence contributes
specific information not captured by the composed assurance mechanism.

---

# Part VI — Temporal Assurance

## 17. Temporal Reasoning Is Not Sufficient Novelty

Runtime verification and temporal-logic research already considers system
behaviour over time rather than evaluating only an instantaneous state.

Consequently:

```text
temporal dependency
```

or:

```text
future-state reasoning
```

alone is not a sufficient DARA-DT novelty claim.

The project may still investigate temporal divergence.

However, the contribution must concern something more specific than merely
adding time to the assurance mechanism.

---

# Part VII — Physical–Digital Divergence

## 18. Divergence Detection Is Established

Digital Twin research already studies:

- state mismatch;
- synchronisation error;
- model discrepancy;
- fidelity;
- data quality;
- distribution shift;
- drift;
- state-estimation error;
- physical–digital consistency.

Therefore:

```text
Physical State != Digital Twin State
```

is not a contribution.

Nor is:

```text
abs(physical_value - twin_value)
```

sufficient novelty.

---

# 19. Decision-Relevant Divergence

The DARA-DT prototype maps divergence to a particular decision.

For decision \(d_t\):

\[
Dep(d_t)
\]

represents its state dependencies.

Detected divergence is:

\[
D_t
\]

and decision-relevant divergence is:

\[
D_t^{rel}(d_t)=Dep(d_t)\cap D_t
\]

This asks:

```text
Global Twin question:

What is wrong in the Twin?
```

versus:

```text
Decision-conditioned question:

What is wrong in the Twin that matters to this particular decision?
```

EXP-001 through EXP-003 demonstrate this mechanism.

EXP-009 further demonstrates the value of distinguishing decision-relevant
from decision-irrelevant evidence uncertainty relative to global uncertainty
monitoring.

However, dependency-aware runtime contracts reproduce the strongest binary
assurance behaviour in the current matrices.

Therefore:

```text
Decision-Relevant Divergence
```

remains experimentally useful but is not established as a unique assurance
mechanism.

---

# Part VIII — Decision Impact and Physical Validity

## 20. Relevance Is Not Validity

EXP-004 demonstrated:

```text
Relevant divergence
        !=
Invalid decision
```

For example:

```text
Twin capacity     = 10
Physical capacity = 9
Demand            = 5
```

The capacity mismatch affects a required dependency.

However:

```text
9 >= 5
```

so the assignment remains physically feasible.

This is an important DARA-DT experimental result.

It does not establish novelty.

---

# 21. Decision Impact

EXP-005 demonstrated that equal divergence magnitude can produce different
decision consequences.

For example:

```text
Twin capacity     = 10
Physical capacity = 7
Divergence        = 3
```

If:

```text
Demand = 5
```

the decision remains valid.

If:

```text
Demand = 8
```

the decision becomes invalid.

Therefore:

```text
Divergence Magnitude
        !=
Decision Consequence
```

This motivates decision-specific impact reasoning.

However, conventional feasibility checking and runtime contracts remain strong
alternative explanations.

---

# Part IX — Evidence Reliability

## 22. Runtime Evidence Reliability

Sensor reliability, data quality and runtime evidence uncertainty are
established research areas.

DARA-DT therefore does not claim novelty from recognising that runtime
evidence can be:

```text
AVAILABLE
STALE
MISSING
CONFLICTING
```

EXP-006 through EXP-009 instead use evidence quality to make the evaluation
more realistic.

The key methodological separation is:

```text
Physical Ground Truth
        !=
Runtime Evidence
        !=
Digital Twin State
```

Physical ground truth is evaluator-only information.

Runtime policies operate on observable evidence rather than privileged truth.

---

# Part X — Adaptive Autonomous Authority

## 23. Adaptive Authority Is Established

Autonomous-system assurance already considers:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
```

and related forms of:

- degraded autonomy;
- controller switching;
- fallback behaviour;
- human escalation;
- operational envelopes.

DARA-DT therefore cannot claim novelty from adaptive authority itself.

The research question concerns:

> What evidence justifies changing authority for a particular decision?

---

# 24. Authority Semantics Remain Open

EXP-009 revealed:

```text
Uncertainty-Aware Runtime Contract

ALLOW    = 12
RESTRICT = 12
DEFER    = 18
```

while:

```text
DARA-DT

ALLOW    = 12
RESTRICT = 0
DEFER    = 30
```

Both mechanisms nevertheless produce identical binary TI/FI/MI/CNI outcomes.

This exposes an unresolved question:

> Do different authority states produce meaningfully different downstream
> operational consequences?

The current experiments cannot answer this because every non-ALLOW state is
treated as an intervention by the binary evaluator.

Authority semantics are therefore a potential future research dimension.

They are not currently a contribution.

---

# Part XI — Logistics Digital Twins

## 25. Logistics Is an Established Digital Twin Domain

Digital Twins are already investigated for:

- supply-chain management;
- production scheduling;
- routing;
- dispatching;
- warehouses;
- resource allocation;
- inventory;
- disruption management;
- fleet management;
- transportation systems.

Recent systematic-review evidence shows increasing use of Digital Twins as
real-time decision environments in logistics and supply-chain systems.

Therefore:

```text
Digital Twin + AI + Logistics
```

is not itself novel.

---

# 26. Why Logistics Remains a Strong Testbed

Logistics remains useful because autonomous decisions depend on physical state
that changes dynamically.

Examples include:

```text
vehicle location
vehicle capacity
vehicle availability
vehicle operational status
inventory
order demand
traffic
resource availability
handover state
recovery resources
```

Digital representations of these states can become stale or incorrect.

Consequently logistics provides a useful domain for studying:

```text
Physical change
        ↓
Digital Twin mismatch
        ↓
Decision dependency
        ↓
Decision consequence
        ↓
Runtime authority
```

The application is experimentally meaningful even though the domain itself is
not novel.

---

# Part XII — Closest-Work Comparison Matrix

## 27. Updated Comparison

| Research Area | Existing Capability | DARA-DT Question | Threat |
|---|---|---|---|
| Digital Twin assurance | Fidelity, quality, validation, trust | How should mismatch affect a specific autonomous decision? | High |
| Continuous DT assurance | Runtime data/model/domain monitoring | Is decision-conditioned divergence additional assurance evidence? | Very High |
| Runtime assurance | Monitor, intervene, fallback | What physical–digital evidence should regulate decision authority? | High |
| Runtime assumptions/contracts | Validate required operational conditions | Does divergence add information beyond the contract? | Very High |
| Dependency-aware assurance | Decisions linked to assumptions/shared state | Does divergence propagation add something beyond dependency monitoring? | Very High |
| Mission-level assurance | Detect globally infeasible commands | Can Twin divergence reveal downstream invalidation not captured otherwise? | High |
| Cooperative/composed RTA | Interacting components and monitors | Does divergence provide cross-component assurance information? | High |
| Temporal runtime verification | History/future-dependent properties | Does physical–digital divergence alter temporal decision validity? | High |
| DT fidelity/divergence | Detect mismatch and synchronisation loss | Does the mismatch matter to this decision chain? | High |
| Decision feasibility | Constraint checking | Is divergence-to-validity reasoning more informative than feasibility alone? | High |
| Adaptive autonomy | Restrict/defer/fallback | Which divergence evidence should cause which authority response? | High |
| Logistics Digital Twins | Real-time operational decision support | How does divergence affect autonomous decision chains? | High |
| Entity filtering | Ignore unrelated entities | Is dependency reasoning necessary beyond entity scope? | Tested |
| Decision-conditioned divergence | Map mismatch to decision dependency | Does it add assurance information beyond contracts? | Unresolved |
| Divergence propagation | Track effects across decisions/dependencies | Does origin/propagation provide additional runtime evidence? | Candidate / Unresolved |

The final two rows now represent the most important unresolved area.

---

# Part XIII — EXP-007 to EXP-009 Prior-Work Implications

## 28. EXP-007

EXP-007 tested:

```text
Capacity
Status
Location / Availability
```

Decision Impact and Runtime Contract both achieved:

```text
12 / 12 correct
```

### Implication

Cross-dependency generalisation was supported.

DARA-DT differentiation was not.

---

# 29. EXP-008

EXP-008 introduced:

```text
Reliable
Stale
Missing
Conflicting
```

runtime evidence.

DARA-DT and the uncertainty-aware runtime contract both produced:

```text
TI  = 12
FI  = 9
MI  = 0
CNI = 3
```

### Implication

Imperfect evidence did not break runtime-contract equivalence.

---

# 30. EXP-009

EXP-009 introduced:

```text
Decision-Relevant Evidence Uncertainty
```

versus:

```text
Decision-Irrelevant Evidence Uncertainty
```

DARA-DT demonstrated improved selectivity relative to global uncertainty.

However:

```text
DARA-DT
        =
Uncertainty-Aware Runtime Contract
```

on the primary binary assurance outcomes.

EXP-009 therefore triggered:

```text
Kill Test A — No Autonomy Advantage
Kill Test C — Runtime Contract Equivalence
```

### Implication

Decision relevance to uncertainty is useful.

It is not currently a DARA-DT-specific advantage.

---

# Part XIV — Previous Candidate Contribution

## 31. Earlier Formulation

The previous candidate contribution was:

> A decision-specific runtime-assurance mechanism that maps
> physical–digital divergence to the dependencies and physical validity of an
> AI-generated logistics decision and experimentally evaluates whether that
> information improves runtime intervention decisions.

This remains a valid description of the prototype.

However, it is no longer sufficient as a strong novelty formulation.

The reason is:

```text
EXP-007
        ↓
Runtime-contract equivalence

EXP-008
        ↓
Runtime-contract equivalence persists

EXP-009
        ↓
Runtime-contract equivalence persists again
```

The candidate contribution must therefore become narrower.

---

# Part XV — New Candidate Research Gap

## 32. What Is No Longer Sufficient

The project should not use any of the following alone as its claimed
differentiator:

```text
runtime Digital Twin assurance

decision-specific assurance

decision dependencies

cross-entity dependencies

runtime assumption monitoring

temporal dependencies

mission-level reasoning

adaptive authority

physical–digital divergence detection

evidence-quality monitoring
```

All have substantial prior-work overlap.

---

# 33. Emerging Candidate Gap

The current candidate gap is more specific:

> **Whether the origin and propagation of physical–digital divergence through
> an autonomous decision chain provides runtime-assurance information beyond
> that available from independently evaluated local contracts or other
> dependency-aware assurance mechanisms.**

This can be represented as:

```text
Physical Event
        ↓
Physical–Digital Divergence
        ↓
Affected Dependency
        ↓
Decision D1
        ↓
Changed Expected System State
        ↓
Decision D2
        ↓
Downstream Validity / Authority
```

The important question is not merely:

```text
Is D2's local contract satisfied?
```

It is:

```text
Has an upstream physical–digital divergence propagated through the
decision/state dependency structure in a way that changes whether D2 can
still be trusted?
```

This is a **candidate research gap**.

It is not confirmed novelty.

---

# Part XVI — Illustrative Research Scenario

## 34. Multi-Stage Logistics Example

Consider three vehicles:

```text
Vehicle A
Vehicle B
Vehicle C
```

and a sequence of autonomous decisions.

The Digital Twin initially represents:

```text
Vehicle A = operational
Vehicle B = operational
Vehicle C = recovery resource available
```

Physically, Vehicle A breaks down.

The Twin update is delayed.

Therefore:

```text
Physical A = failed
Twin A     = operational
```

Decision D1 assigns an order to Vehicle A based on the stale Twin.

D1 changes the expected future fleet state used by later planning.

Decision D2 assigns another order to Vehicle B.

Vehicle B may satisfy its immediate local checks:

```text
Vehicle B operational = true
Vehicle B capacity sufficient = true
```

However, the feasibility or risk of D2 may depend on assumptions about:

```text
fleet capacity
recovery availability
handover resources
timing
backup allocation
```

that were affected by the unresolved divergence involving Vehicle A.

A local contract for Vehicle B may therefore remain satisfied while a
decision-chain assumption has become invalid.

The research question is whether explicit divergence-origin and propagation
information provides useful additional assurance evidence.

---

# Part XVII — Critical Comparator Design

## 35. Local Runtime Contract Is No Longer Enough

A future experiment must not compare DARA-DT only with a weak local contract
such as:

```text
vehicle.capacity >= demand
```

That comparator would no longer provide a convincing novelty test.

---

# 36. Required Strong Comparator

The future strong comparator should be capable of representing:

```text
decision dependencies

cross-entity dependencies

shared state

upstream assumptions

dependency invalidation

composed constraints
```

Conceptually:

```text
Dependency-Aware / Composed Runtime Contract
```

This comparator should receive the same observable runtime evidence as
DARA-DT.

No policy should receive privileged physical ground truth.

---

# 37. Core Differentiation Test

The decisive question becomes:

```text
Can a dependency-aware composed runtime contract detect
the same downstream invalidations as propagation-aware DARA-DT?
```

If:

```text
YES
```

then the DARA-DT differentiation claim must narrow again.

If:

```text
NO
```

the specific information responsible for the difference must be isolated.

A DARA-DT advantage must not automatically be attributed to the whole
framework.

---

# Part XVIII — Candidate EXP-010

## 38. Candidate Research Question

The literature audit supports the following provisional EXP-010 question:

> **Can propagation-aware physical–digital divergence identify downstream
> decision invalidation that remains undetected by independently evaluated
> local runtime contracts in a multi-stage autonomous logistics decision
> chain?**

However, because dependency-aware assurance already exists as a research
direction, a stronger version should also be tested:

> **Does propagation-aware physical–digital divergence provide additional
> runtime-assurance information beyond a dependency-aware composed runtime
> contract when physical–digital mismatch propagates through a multi-stage
> autonomous logistics decision chain?**

The second question represents the stronger novelty test.

---

# 39. EXP-010 Must Be Pre-Registered

Before implementation, EXP-010 should freeze:

```text
Research question

Decision-chain structure

Physical state

Digital Twin state

Divergence origin

Propagation mechanism

Decision dependencies

Local contracts

Composed/dependency-aware contract

DARA-DT propagation mechanism

Ground truth

Comparator policies

Authority semantics

Metrics

Success criteria

Kill tests
```

No experimental condition should be added after observing results merely to
make DARA-DT perform better.

---

# Part XIX — Candidate EXP-010 Kill Tests

## 40. Kill Test A — Composed Contract Equivalence

If a dependency-aware composed runtime contract reproduces DARA-DT's relevant
downstream intervention behaviour:

```text
DARA-DT differentiation fails for the tested decision chain.
```

This should be the strongest kill test.

---

## 41. Kill Test B — Local-Contract Strawman

If DARA-DT appears superior only because the comparator checks each decision
independently while ignoring known cross-decision dependencies:

```text
the comparison is too weak.
```

The result must not support a strong contribution claim.

---

## 42. Kill Test C — No Divergence-Specific Information

If the same result can be achieved without representing:

```text
Physical State
vs
Digital Twin State
```

and without tracing the origin of mismatch:

```text
the physical–digital divergence component has not demonstrated additional
assurance value.
```

---

## 43. Kill Test D — No Propagation Requirement

If every downstream invalidation can be detected from the downstream
decision's current local state alone:

```text
divergence propagation is unnecessary in that matrix.
```

---

## 44. Kill Test E — Privileged Evidence

If DARA-DT receives physical-state information unavailable to the comparator:

```text
the comparison is invalid.
```

Both mechanisms must operate on equivalent observable runtime evidence.

---

## 45. Kill Test F — Domain-Specific Hard Coding

If the propagation mechanism only works because the experimental decision
chain has been manually encoded for one scenario:

```text
general framework-level claims must be rejected.
```

---

# Part XX — Literature Search Priorities

## 46. Updated Search Areas

The next systematic search should prioritise combinations such as:

```text
"digital twin" AND "runtime assurance"

"digital twin" AND "decision dependency"

"digital twin" AND "dependency-aware assurance"

"digital twin" AND "physical digital divergence"

"digital twin" AND "divergence propagation"

"digital twin" AND "decision chain"

"digital twin" AND "runtime contract"

"runtime assurance" AND "dependency-aware"

"runtime assurance" AND "shared state"

"runtime assurance" AND "decision interaction"

"runtime assurance" AND "mission feasibility"

"runtime assumption monitoring" AND "dependency"

"autonomous systems" AND "composed runtime assurance"

"logistics digital twin" AND "runtime assurance"

"logistics digital twin" AND "decision validity"

"logistics digital twin" AND "state synchronisation"

"logistics digital twin" AND "decision propagation"
```

---

# 47. Paper Review Template

For every close work, record:

```text
Citation

Domain

System type

Digital Twin present?

Physical state represented?

Twin state represented?

Physical–digital mismatch explicit?

Decision dependencies represented?

Cross-entity dependencies represented?

Temporal dependencies represented?

Multiple decisions represented?

Assumption invalidation represented?

Divergence origin represented?

Divergence propagation represented?

Decision consequence evaluated?

Runtime authority changed?

Evidence quality represented?

Comparator used?

Ground truth available?

Primary contribution

Overlap with DARA-DT

Remaining distinction

Novelty threat
```

This information should feed into:

```text
docs/literature_matrix.md
docs/novelty_evidence_matrix.md
```

---

# Part XXI — Current Prior-Work Threat Ranking

## 48. Threat Matrix

| Area | Threat |
|---|---|
| Digital Twin assurance | HIGH |
| Continuous Digital Twin assurance | VERY HIGH |
| DARTER-style runtime assurance | VERY HIGH |
| Runtime contracts | VERY HIGH |
| Runtime assumption monitoring | VERY HIGH |
| Dependency-aware runtime assurance | VERY HIGH |
| Decision assurance | VERY HIGH |
| Mission-level runtime assurance | HIGH |
| Composed/cooperative runtime assurance | HIGH |
| Temporal runtime verification | HIGH |
| Physical–digital divergence detection | HIGH |
| Decision feasibility | HIGH |
| Adaptive authority | HIGH |
| Logistics Digital Twins | HIGH |
| Entity filtering | TESTED / INSUFFICIENT EXPLANATION |
| Decision-conditioned divergence | UNRESOLVED |
| Divergence-origin reasoning | UNRESOLVED |
| Divergence propagation through decision chains | UNRESOLVED |
| Added value beyond composed dependency-aware contracts | UNRESOLVED |

---

# Part XXII — Current Claim Permissions

## 49. Claims Supported by the Repository

The repository may state that DARA-DT:

- investigates physical–digital divergence;
- explicitly models decision dependencies;
- distinguishes global from decision-relevant divergence;
- distinguishes relevance from physical decision validity;
- separates physical ground truth, runtime evidence and Digital Twin state;
- evaluates stale, missing and conflicting evidence;
- has been evaluated across capacity, status and location / availability;
- compares multiple assurance mechanisms;
- has tested runtime-contract baselines;
- has tested entity filtering;
- has tested decision-relevant versus irrelevant uncertainty;
- preserves negative and equivalence results;
- has repeatedly observed runtime-contract equivalence in its current
  decision structures.

---

# 50. Claims Not Currently Supported

The repository must not state that DARA-DT:

- is the first runtime-assurance framework for Digital Twins;
- is the first divergence-aware assurance system;
- introduces dependency-aware runtime assurance;
- introduces temporal runtime assurance;
- introduces cross-entity runtime assurance;
- introduces mission-level assurance;
- introduces adaptive autonomous authority;
- generally outperforms runtime contracts;
- provides higher autonomy than uncertainty-aware runtime contracts;
- provides formal safety guarantees;
- has demonstrated real-world logistics generalisation;
- has confirmed research novelty.

---

# Part XXIII — Current Research Gap Statement

## 51. Updated Working Gap

A cautious current formulation is:

> **Digital Twin assurance, runtime assurance, runtime contracts,
> assumption monitoring and dependency-aware assurance already provide
> substantial mechanisms for monitoring operational trust and regulating
> autonomous behaviour. DARA-DT therefore investigates the narrower unresolved
> question of whether the origin and propagation of physical–digital
> divergence through the state dependencies of autonomous logistics decisions
> provides additional runtime-assurance information beyond strong
> dependency-aware contract mechanisms, particularly when an upstream
> physical–digital mismatch changes the validity of downstream decisions.**

This is a:

```text
WORKING RESEARCH GAP
```

not a confirmed literature gap.

---

# Part XXIV — Research Integrity Position

## 52. Evidence Before Contribution

The project currently has a stronger research position because it has already
produced results that weaken its own initial contribution hypothesis.

The evidence progression is:

```text
EXP-001–003
Decision relevance appears useful
        ↓
EXP-004
Relevance alone is insufficient
        ↓
EXP-005
Decision impact improves selectivity
        ↓
EXP-006
Imperfect evidence creates failures
        ↓
EXP-007
Runtime contract matches impact reasoning
        ↓
EXP-008
Contract equivalence survives imperfect evidence
        ↓
EXP-009
Contract equivalence survives decision-relevance challenge
        ↓
Literature audit
Dependency-aware assurance creates an even stronger comparator
```

The next experiment must respect this evidence.

---

# 53. Protect the Question, Not the Framework

DARA-DT should remain falsifiable.

The project should not assume:

```text
DARA-DT must outperform the comparator.
```

Instead:

```text
Research Question
        ↓
Strongest Reasonable Comparator
        ↓
Pre-Registered Conditions
        ↓
Experiment
        ↓
Result
        ↓
Contribution Narrowed or Strengthened
```

If a composed dependency-aware runtime contract continues to match DARA-DT,
that result should be retained.

---

# Part XXV — Current Decision

## 54. EXP-010 Decision

EXP-010 remains justified only if it directly addresses the stronger
differentiation question.

Do not build:

```text
EXP-009 + more conditions
```

Do not merely add:

```text
more vehicles
more stale values
more missing values
more divergence magnitude
```

Instead, EXP-010 should investigate:

```text
upstream physical–digital divergence
        ↓
decision/state dependency
        ↓
multi-stage autonomous decision
        ↓
downstream consequence
        ↓
local contract comparison
        ↓
dependency-aware composed contract comparison
        ↓
DARA-DT propagation-aware assurance
```

---

# 55. Current Candidate EXP-010 Question

The strongest provisional formulation is:

> **Does propagation-aware physical–digital divergence provide additional
> runtime-assurance information beyond a dependency-aware composed runtime
> contract when an upstream physical–digital mismatch propagates through a
> multi-stage autonomous logistics decision chain?**

This question is intentionally capable of producing:

```text
DARA-DT advantage
DARA-DT equivalence
DARA-DT disadvantage
```

All three outcomes are scientifically acceptable.

---

# 56. Current Candidate Contribution

The candidate contribution has therefore narrowed to:

> **An experimental investigation of whether tracing the origin and
> propagation of physical–digital divergence through autonomous decision
> dependencies provides assurance information beyond strong
> dependency-aware runtime contracts in dynamic logistics Digital Twins.**

Status:

```text
CANDIDATE
NOT ESTABLISHED
HIGH NOVELTY THREAT
REQUIRES EXP-010 + FURTHER LITERATURE REVIEW
```

---

# Part XXVI — Final Verdict

## 57. Prior-Work Verdict

The literature audit shows that DARA-DT operates in a highly active research
space.

The following are already well represented:

```text
Digital Twin assurance
continuous runtime assurance
runtime evidence
runtime contracts
runtime assumption monitoring
decision assurance
dependency-aware assurance
mission-level assurance
adaptive authority
Digital Twin logistics decision support
```

The project's earlier broad differentiators are therefore insufficient.

At the same time, the current audit does not justify terminating the research.

The question has instead become more precise.

The strongest unresolved proposition is:

> **Whether physical–digital divergence has assurance value not merely as a
> detected mismatch, but as a traceable causal/runtime signal whose effects
> propagate through the dependencies of subsequent autonomous decisions.**

Even this proposition remains under threat from dependency-aware and composed
runtime assurance.

The decisive experimental question is therefore:

> **Does explicit divergence-origin and propagation reasoning add information
> beyond a strong dependency-aware composed runtime contract?**

Until that question is tested, the correct novelty status remains:

```text
NOT ESTABLISHED
```

---

# 58. Next Research Gate

The next sequence is:

```text
Closest-Prior-Work Audit
        ✓
        ↓
Update Novelty Boundary
        ✓
        ↓
Define EXP-010 Decision Chain
        ↓
Define Strong Dependency-Aware Comparator
        ↓
Pre-Register EXP-010
        ↓
Freeze Kill Tests
        ↓
Implement
        ↓
Run
        ↓
Accept Advantage / Tie / Loss
        ↓
Reassess Contribution
```

The immediate next task is therefore **not implementation**.

It is the formal pre-registration of EXP-010 around the stronger
dependency-aware comparator and divergence-propagation hypothesis.
