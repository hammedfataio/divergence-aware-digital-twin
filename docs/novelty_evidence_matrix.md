# DARA-DT Novelty Evidence and Falsification Matrix

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Framework:** DARA-DT  
**Research Identity:** Trustworthy Intelligent Systems  
**Application Domain:** Autonomous Logistics Systems  
**Document Status:** Living Novelty, Differentiation and Falsification Record  
**Evidence Base:** EXP-001 to EXP-009  
**Current Novelty Gate:** Added value beyond strong runtime contracts under richer decision structures  
**Novelty Status:** Not Yet Established

---

# 1. Purpose

This document evaluates whether DARA-DT contains a defensible research
contribution after comparison with adjacent and potentially equivalent
assurance mechanisms.

It is deliberately designed to challenge the project rather than defend it.

The objective is not to prove that DARA-DT is novel.

The objective is to determine:

1. which concepts are already established;
2. which DARA-DT mechanisms overlap with prior work;
3. which behaviours are experimentally supported;
4. which candidate differentiators have survived experimental challenge;
5. which candidate differentiators have been weakened or falsified;
6. what additional evidence would be required before making a contribution
   claim.

The governing principle is:

> **Implementation is not novelty, experimental success is not novelty, and
> integration of existing components is not automatically novelty.**

A second principle now follows from EXP-007 through EXP-009:

> **A proposed mechanism should not be claimed as a contribution when a
> simpler, strong comparator reproduces its relevant behaviour.**

---

# Part I — Research Position

## 2. Central Research Question

The canonical research question is:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

The DARA-DT reasoning chain is:

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

A strong-baseline challenge is now explicitly added:

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
        ↓
Does a simpler strong mechanism provide the same assurance result?
```

Not every element of this chain is expected to be novel.

Most individual elements have substantial prior work.

The unresolved research question is whether explicit decision-conditioned
physical–digital divergence provides additional assurance information under
conditions where simpler mechanisms are insufficient.

---

## 3. Current Candidate Contribution

Before EXP-007 to EXP-009, the candidate contribution was broadly:

> A decision-conditioned runtime-assurance mechanism that evaluates
> physical–digital divergence relative to the state dependencies and physical
> validity of an AI-generated logistics decision.

The experimental evidence now requires this formulation to be narrowed.

The current candidate contribution is:

> **An experimental and computational framework for investigating whether
> physical–digital divergence provides additional runtime-assurance evidence
> when conditioned on the dependencies, validity and evidence quality of a
> specific AI-generated logistics decision, particularly under decision
> structures where simpler runtime contracts may be insufficient.**

Status:

```text
CANDIDATE CONTRIBUTION
NARROWED BY EXP-007 TO EXP-009
NOT CONFIRMED NOVELTY
```

DARA-DT superiority over runtime contracts is **not** part of the current
contribution statement.

---

# Part II — Novelty Assessment Rules

## 4. Evidence Dimensions

Every candidate contribution is assessed across:

```text
Prior-Work Overlap
Implementation Evidence
Experimental Evidence
Cross-Dependency Evidence
Strong-Baseline Evidence
Falsification Evidence
Differentiation Evidence
```

Strong implementation evidence cannot compensate for weak differentiation
evidence.

---

## 5. Status Scale

### ESTABLISHED

Substantial prior work exists.

Do not claim novelty.

### HIGH OVERLAP

The DARA-DT mechanism strongly resembles existing research.

A narrower differentiator is required.

### CANDIDATE DIFFERENTIATOR

A potentially meaningful distinction exists but has not survived sufficient
literature and experimental challenge.

### EXPERIMENTALLY SUPPORTED

Controlled repository evidence supports the stated behaviour.

This does not imply novelty.

### FALSIFIED IN CURRENT MATRIX

A pre-registered or explicit claim failed under the tested conditions.

This does not imply that the concept is useless.

It means that the corresponding claim cannot be made from the current
evidence.

### REQUIRES GENERALISATION

The result remains tied to limited scenarios or dependency structures.

### NOVELTY THREAT

Existing work or a simpler comparator may already contain an equivalent
mechanism.

### FALSIFICATION REQUIRED

A direct experiment is required to determine whether the distinction survives.

### NOT ESTABLISHED

Available evidence is insufficient for a novelty claim.

---

# Part III — Prior-Work Threat Map

## 6. Threat A — Digital Twin Assurance

Digital Twin assurance is already an established area.

Relevant concerns include:

- fidelity;
- trustworthiness;
- data quality;
- validation;
- synchronisation;
- model performance;
- uncertainty;
- lifecycle assurance;
- operational assurance.

Therefore DARA-DT does not contribute the general idea that:

```text
Digital Twins require assurance.
```

### Status

```text
ESTABLISHED
```

---

## 7. Threat B — Continuous Digital Twin Assurance

Contemporary research explicitly investigates continuous runtime assurance for
Digital Twins.

Relevant mechanisms include:

- runtime data verification;
- model-performance monitoring;
- validated thresholds;
- operational-domain monitoring;
- distribution drift detection;
- automated evidence generation;
- continuously maintained assurance evidence.

Therefore DARA-DT must not claim:

```text
first runtime assurance for Digital Twins

first continuous assurance for Digital Twins

first use of runtime evidence for Twin assurance
```

### Threat Level

```text
VERY HIGH
```

---

## 8. Threat C — Contract-Based Runtime Monitoring

Runtime contracts can express operational conditions required before a
decision is permitted.

For example:

```text
vehicle.capacity >= order.demand

vehicle.status == operational

vehicle.available == true
```

Such mechanisms can produce runtime intervention when these conditions are
violated or cannot be established reliably.

This threat is no longer theoretical.

EXP-007, EXP-008 and EXP-009 directly compare DARA-DT-related mechanisms with
runtime-contract baselines.

### Experimental Evidence

EXP-007:

```text
Decision Impact  = 12/12 correct
Runtime Contract = 12/12 correct
```

EXP-008:

```text
Uncertainty-Aware Contract
TI = 12
FI = 9
MI = 0
CNI = 3

DARA-DT
TI = 12
FI = 9
MI = 0
CNI = 3
```

EXP-009:

```text
Uncertainty-Aware Contract
TI = 21
FI = 9
MI = 0
CNI = 12

DARA-DT
TI = 21
FI = 9
MI = 0
CNI = 12
```

### Current Conclusion

> **Runtime-contract equivalence is currently one of the strongest threats to
> the DARA-DT contribution.**

### Threat Level

```text
VERY HIGH — EXPERIMENTALLY CONFIRMED THREAT
```

---

## 9. Threat D — Runtime Assumption Monitoring

Runtime assumption monitoring evaluates whether assumptions relied upon by a
system remain valid during operation.

For example:

```text
Decision:
assign vehicle V1 to order O1

Required condition:
capacity(V1) >= demand(O1)
```

may be represented as either:

```text
decision dependency
```

or:

```text
runtime assumption / contract
```

The conceptual overlap is substantial.

### Critical Question

> Does explicit physical–digital divergence provide information that cannot
> be obtained by monitoring the operational assumptions of the decision?

EXP-007 through EXP-009 have not yet demonstrated that it does for the tested
single-decision structures.

### Threat Level

```text
VERY HIGH
```

---

## 10. Threat E — Decision Assurance

Decision assurance focuses assurance evidence on operational decisions rather
than only on model outputs.

Relevant concepts include:

- decision-centred test design;
- operational confidence thresholds;
- escalation conditions;
- governance boundaries;
- authority constraints;
- evidence-to-decision traceability;
- operational context.

Therefore:

```text
decision-specific assurance
```

cannot itself constitute DARA-DT novelty.

### Threat Level

```text
VERY HIGH
```

---

## 11. Threat F — Decision Feasibility

Decision feasibility and constraint validation are established.

For example:

```text
capacity >= demand
```

is a conventional feasibility constraint.

Therefore the following is not a contribution:

```text
check whether capacity satisfies demand.
```

EXP-004 and EXP-005 demonstrate useful behaviour around the relationship
between divergence and feasibility, but this does not make feasibility checking
novel.

### Threat Level

```text
HIGH
```

---

## 12. Threat G — Adaptive Authority

Runtime systems already regulate authority through mechanisms such as:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
HUMAN ESCALATION
```

Therefore adaptive authority itself is not a DARA-DT contribution.

EXP-009 additionally demonstrates that two policies can produce identical
binary intervention outcomes while using different authority states.

This means authority semantics require operational evaluation before they can
form part of a contribution claim.

### Threat Level

```text
HIGH
```

---

## 13. Threat H — Entity Filtering

A simple mechanism can ignore uncertainty associated with entities unrelated
to the pending decision.

EXP-009 explicitly tested this explanation.

The entity-filtered baseline produced:

```text
TI = 9
FI = 9
MI = 12
CNI = 12
Autonomy = 0.571
```

DARA-DT produced:

```text
TI = 21
FI = 9
MI = 0
CNI = 12
Autonomy = 0.286
```

Therefore simple entity filtering did not reproduce the complete DARA-DT
safety/autonomy behaviour.

### Status

```text
TESTED
TRIVIAL ENTITY-FILTER EXPLANATION NOT SUFFICIENT IN EXP-009
```

This result does not resolve the stronger runtime-contract threat.

---

# Part IV — Component-Level Novelty Matrix

## 14. Updated Evidence Matrix

| DARA-DT Element | Closest Threat | Evidence Through | Generalisation | Novelty Position |
|---|---|---|---|---|
| Physical–digital divergence | DT fidelity / synchronisation | EXP-001–009 | Multiple conditions | Established concept |
| Divergence magnitude | Error / fidelity metrics | EXP-004/005 | Limited | Established concept |
| Runtime assurance | Runtime assurance literature | EXP-001–009 | Controlled | Established concept |
| Authority regulation | Adaptive autonomy | EXP-001–009 | Multiple conditions | High overlap |
| Decision dependencies | Contracts / assumptions | EXP-001–009 | Three dependency families | Very high threat |
| Decision relevance | Contract / assumption monitoring | EXP-001–009 | Three dependency families | Experimentally useful, high overlap |
| Decision impact | Feasibility / constraint checking | EXP-004–009 | Capacity, status, location/availability | Experimentally supported, high overlap |
| Evidence reliability | Data / sensor assurance | EXP-006–009 | Three evidence failure modes | Established concept |
| Decision-sensitive uncertainty | Runtime contracts / scoped monitoring | EXP-009 | Three dependency families | Supported behaviour, not unique |
| Entity filtering | Entity-scoped monitoring | EXP-009 | Controlled | Insufficient explanation |
| Physical–digital divergence conditioned on decision dependency | Combined threat | EXP-001–009 | Cross-dependency evidence exists | Candidate differentiator weakened by contract equivalence |
| Divergence-caused validity change | Constraint + discrepancy reasoning | EXP-004–009 | Cross-dependency | Candidate / high threat |
| Integrated DARA-DT mechanism | All above | EXP-001–009 | Controlled cross-dependency | Candidate contribution, not differentiated from strong contract baseline |
| Decision risk | Risk-aware assurance | Conceptual | Not independently tested | Not established |
| Multi-decision divergence propagation | Contracts / temporal assurance | Not yet tested | None | Open candidate direction |

---

# Part V — Experimental Evidence

## 15. Finding 1 — Divergence Count Is Insufficient

EXP-001 and EXP-002 demonstrate that equal or larger quantities of divergence
do not necessarily imply greater significance to the current decision.

### Supported Statement

> In the controlled DARA-DT experiments, divergence count alone does not
> reliably indicate whether intervention is required for the current
> decision.

### Status

```text
EXPERIMENTALLY SUPPORTED
NOT A NOVELTY CLAIM
```

---

## 16. Finding 2 — Decision Relevance Improves Selectivity

EXP-002 demonstrated that decision-relevant assurance could distinguish
unrelated divergence from divergence affecting the pending decision.

### Status

```text
EXPERIMENTALLY SUPPORTED
NOT UNIQUE TO DARA-DT
```

Subsequent experiments show that dependency-aware contracts can reproduce
important parts of this behaviour.

---

## 17. Finding 3 — Relevance Is Not Validity

EXP-004 demonstrated that divergence can affect a required decision variable
without invalidating the decision.

Example:

```text
Twin capacity     = 10
Physical capacity = 9
Demand            = 5
```

The capacity mismatch is decision relevant.

However:

```text
9 >= 5
```

and the decision remains physically feasible.

Therefore:

```text
Decision Relevance
        ≠
Decision Invalidity
```

### Status

```text
STRONG EXPERIMENTAL FINDING
```

---

## 18. Finding 4 — Divergence Magnitude Is Not Decision Impact

EXP-005 includes conditions with equal divergence magnitude but different
decision consequences.

Therefore:

```text
Same divergence magnitude
        ↓
Different decision validity
```

### Supported Statement

> Divergence magnitude alone is insufficient to determine decision impact in
> the controlled EXP-005 matrix.

### Status

```text
EXPERIMENTALLY SUPPORTED
```

---

## 19. Finding 5 — Impact Reasoning Improves Selectivity

EXP-005 produced:

```text
Decision Relevance
TI  = 6
FI  = 8
MI  = 0
CNI = 1
Accuracy = 0.467
Autonomy = 0.067
```

compared with:

```text
Decision Impact
TI  = 6
FI  = 2
MI  = 0
CNI = 7
Accuracy = 0.867
Autonomy = 0.467
```

### Supported Statement

> Within EXP-005, decision-impact reasoning reduced unnecessary intervention
> relative to relevance-only assurance while retaining all required
> interventions.

### Status

```text
EXPERIMENTALLY SUPPORTED
```

This behaviour does not establish novelty because ordinary feasibility and
runtime-contract mechanisms remain strong competing explanations.

---

## 20. Finding 6 — Evidence Reliability Matters

EXP-006 separated:

```text
Physical Ground Truth
        ≠
Runtime Evidence
        ≠
Digital Twin State
```

The evidence-aware mechanism produced both a false intervention and a missed
intervention under imperfect evidence.

### Supported Statement

> Assurance quality depends on the reliability of the runtime evidence used
> to evaluate the decision.

### Status

```text
EXPERIMENTALLY SUPPORTED
ESTABLISHED CONCEPT
```

---

## 21. Finding 7 — Cross-Dependency Generalisation

EXP-007 evaluated:

```text
Capacity
Status
Location / Availability
```

The Decision Impact and Runtime Contract mechanisms both produced:

```text
12/12 correct
```

### Supported Statement

> The controlled impact reasoning used by the prototype is not confined to
> capacity and can be represented across the three tested dependency
> families.

### Status

```text
CROSS-DEPENDENCY BEHAVIOUR SUPPORTED
```

However:

```text
Decision Impact = Runtime Contract
```

at the EXP-007 binary outcome level.

Therefore EXP-007 supports generalisation of behaviour but simultaneously
weakens the claim that DARA-DT provides unique assurance information.

---

## 22. Finding 8 — Runtime-Contract Equivalence Under Imperfect Evidence

EXP-008 evaluated 24 conditions involving:

```text
Reliable
Stale
Missing
Conflicting
```

runtime evidence.

The uncertainty-aware runtime contract and DARA-DT both produced:

```text
TI  = 12
FI  = 9
MI  = 0
CNI = 3
Accuracy = 0.625
Recall = 1.000
Autonomy = 0.125
```

### Supported Statement

> Under the EXP-008 imperfect-evidence matrix, DARA-DT does not improve the
> primary binary safety–autonomy outcomes beyond an uncertainty-aware runtime
> contract.

### Status

```text
STRONG FALSIFICATION EVIDENCE
RUNTIME-CONTRACT THREAT SURVIVES
```

---

## 23. Finding 9 — Decision-Relevant Evidence Uncertainty

EXP-009 separated:

```text
Decision-Relevant Uncertainty
```

from:

```text
Decision-Irrelevant Uncertainty
```

Across the 18 irrelevant imperfect-evidence conditions:

```text
Global Uncertainty
TI  = 9
FI  = 9
MI  = 0
CNI = 0
Autonomy = 0.000
```

while:

```text
DARA-DT
TI  = 9
FI  = 0
MI  = 0
CNI = 9
Accuracy = 1.000
Autonomy = 0.500
```

This demonstrates that decision-sensitive assurance can avoid unnecessary
global conservatism.

However, the uncertainty-aware runtime contract produced exactly the same
result:

```text
TI  = 9
FI  = 0
MI  = 0
CNI = 9
Accuracy = 1.000
Autonomy = 0.500
```

### Status

```text
DECISION-SENSITIVE BEHAVIOUR SUPPORTED
DARA-DT-SPECIFIC ADVANTAGE NOT SUPPORTED
```

---

# Part VI — EXP-009 Falsification Record

## 24. Kill Test A — No Autonomy Advantage

### Result

```text
TRIGGERED
```

DARA-DT and the uncertainty-aware runtime contract both achieved:

```text
Autonomy Availability = 0.286
MI = 0
```

### Consequence

The claim that DARA-DT provides greater aggregate autonomy than the strongest
current runtime-contract comparator is:

```text
NOT SUPPORTED
```

---

## 25. Kill Test B — Safety Degradation

### Result

```text
NOT TRIGGERED
```

DARA-DT did not obtain increased autonomy by accepting additional missed
interventions.

### Consequence

No evidence of safety sacrifice explains the observed DARA-DT result.

---

## 26. Kill Test C — Runtime Contract Equivalence

### Result

```text
TRIGGERED
```

Both policies produced:

```text
TI  = 21
FI  = 9
MI  = 0
CNI = 12
Accuracy = 0.786
Precision = 0.700
Recall = 1.000
Autonomy = 0.286
```

### Consequence

The stronger claim that DARA-DT provides improved binary assurance performance
beyond an uncertainty-aware runtime contract is:

```text
FALSIFIED IN EXP-009
```

This is currently the most important novelty result.

---

## 27. Kill Test D — Capacity-Only Effect

### Result

```text
NOT TRIGGERED
```

The behaviour reproduces across:

```text
Capacity
Status
Location / Availability
```

### Consequence

The framework cannot be dismissed simply as a capacity-only mechanism.

However, the runtime contract also reproduces the same binary behaviour across
all three families.

---

## 28. Kill Test E — Evidence Privilege

### Result

```text
NOT TRIGGERED
```

DARA-DT receives no physical ground truth or separate privileged runtime
evidence.

### Consequence

The EXP-009 comparison satisfies the implemented evidence-parity requirement.

---

## 29. Kill Test F — Trivial Entity Filtering

### Result

```text
NOT TRIGGERED
```

Entity filtering produced:

```text
MI = 12
```

while DARA-DT produced:

```text
MI = 0
```

### Consequence

The complete DARA-DT behaviour cannot be explained by simple entity filtering
alone.

This removes a weak competing explanation but does not remove the stronger
runtime-contract explanation.

---

# Part VII — Strongest Candidate Differentiator

## 30. What DARA-DT Must Not Claim

The contribution must not be framed simply as:

```text
Digital Twin assurance
```

or:

```text
runtime assurance
```

or:

```text
decision assurance
```

or:

```text
runtime assumption monitoring
```

or:

```text
constraint checking
```

or:

```text
adaptive autonomy
```

or:

```text
evidence-aware assurance
```

or:

```text
decision relevance.
```

All have significant conceptual overlap with established work.

The evidence also currently prohibits the claim:

```text
DARA-DT outperforms uncertainty-aware runtime contracts.
```

---

## 31. Previous Candidate Differentiator

The earlier candidate was:

> **Decision-conditioned physical–digital divergence: determining whether a
> mismatch between physical and Twin state affects a state dependency of the
> specific AI-generated decision and whether that mismatch changes the
> decision's physical validity.**

Formally:

\[
D_t^{rel}(d_t)=Dep(d_t)\cap D_t
\]

followed by:

\[
I_t=f(d_t,D_t^{rel},E_t)
\]

and:

\[
A_t=\pi(d_t,D_t^{rel},I_t,E_t)
\]

EXP-007 through EXP-009 show that this mechanism remains conceptually useful.

However, its current binary assurance behaviour can be reproduced by a strong
runtime-contract mechanism in the tested structures.

Therefore this formulation alone is no longer sufficient for a strong novelty
claim.

---

## 32. Current Candidate Differentiator

The sharper unresolved candidate is:

> **Whether explicit physical–digital divergence provides additional
> assurance information when autonomous decisions depend on interacting,
> cross-entity, compound or temporally propagating state relationships that
> cannot be represented adequately by the local runtime contracts evaluated
> so far.**

Status:

```text
OPEN RESEARCH HYPOTHESIS
NOT EXPERIMENTALLY ESTABLISHED
```

This formulation is deliberately conditional.

The project must allow the possibility that the answer is:

```text
No.
```

---

# Part VIII — Differentiation Tests

## 33. Test A — Global Fidelity vs Decision-Conditioned Divergence

### Competing Explanation

A global Twin-fidelity or trust measure may provide sufficient assurance
information.

### Existing Evidence

EXP-001, EXP-002 and EXP-009 show that global divergence or uncertainty can
over-intervene when the mismatch is unrelated to the pending decision.

### Status

```text
PARTIALLY DIFFERENTIATED
```

Decision-sensitive assurance is better targeted in the controlled matrices.

This does not establish DARA-DT novelty.

---

## 34. Test B — Runtime Contract vs DARA-DT

### Competing Explanation

A runtime contract can represent the same operational dependencies and produce
equivalent intervention decisions.

### Evidence

EXP-007:

```text
EQUIVALENCE OBSERVED
```

EXP-008:

```text
EQUIVALENCE OBSERVED
```

EXP-009:

```text
EQUIVALENCE OBSERVED
```

### Status

```text
MAJOR NOVELTY THREAT
EXPERIMENTALLY CONFIRMED IN CURRENT MATRICES
```

### Required Next Question

> Does this equivalence persist under interacting, compound, cross-entity or
> temporally propagating decision dependencies?

---

## 35. Test C — Ordinary Feasibility vs DARA-DT

### Competing Explanation

The decision-impact mechanism may reproduce conventional feasibility checking.

### Existing Evidence

EXP-004 and EXP-005 show that explicit divergence, relevance and validity can
be separated experimentally.

However, EXP-007 demonstrates that a runtime contract can reproduce the
resulting intervention decisions.

### Status

```text
UNRESOLVED AS A NOVELTY DIFFERENTIATOR
```

---

## 36. Test D — Global Twin Trust vs Decision-Level Trust

### Competing Explanation

A sufficiently strong global Twin assurance mechanism may determine whether
the Twin is trustworthy enough for autonomous use.

### Existing Evidence

Controlled experiments show:

```text
High unrelated divergence
        ≠
Current decision invalidity
```

and:

```text
Small local divergence
        →
Potential decision invalidity
```

### Status

```text
DECISION-LEVEL SELECTIVITY SUPPORTED
STRONGER REALISTIC GLOBAL-FIDELITY BASELINE STILL REQUIRED
```

---

## 37. Test E — Entity Filtering vs Dependency Reasoning

### Competing Explanation

Simple filtering by selected entity may explain the apparent benefit.

### Existing Evidence

EXP-009 Kill Test F:

```text
NOT TRIGGERED
```

Entity filtering missed 12 required interventions.

### Status

```text
SIMPLE ENTITY FILTERING INSUFFICIENT IN EXP-009
```

---

## 38. Test F — Authority Semantics

EXP-009 revealed:

```text
Uncertainty Contract:
ALLOW    = 12
RESTRICT = 12
DEFER    = 18

DARA-DT:
ALLOW    = 12
RESTRICT = 0
DEFER    = 30
```

The binary evaluator nevertheless gives both policies identical intervention
outcomes.

### Open Question

> Do RESTRICT, DEFER and FALLBACK produce meaningfully different operational
> consequences?

### Status

```text
UNRESOLVED
```

Authority-state difference alone is not evidence of superiority.

---

# Part IX — Current Novelty Kill Conditions

## 39. Literature Kill Condition

The novelty case is substantially weakened if prior work already integrates:

1. physical system state;
2. Digital Twin state;
3. explicit physical–digital discrepancy;
4. specific autonomous decisions;
5. decision dependencies;
6. runtime discrepancy-to-dependency mapping;
7. evidence-quality reasoning;
8. evaluation of decision consequence;
9. adaptive authority regulation;
10. interacting or temporally propagating decision dependencies.

If such work exists, DARA-DT must identify a narrower contribution.

---

## 40. Runtime-Contract Kill Condition

The broad DARA-DT differentiation claim should be rejected if:

```text
strong runtime contracts
```

continue to reproduce DARA-DT's relevant behaviour across richer decision
structures while requiring less mechanism complexity.

### Current Status

```text
PARTIALLY TRIGGERED
```

More precisely:

- triggered for the tested EXP-007 structures;
- triggered under EXP-008 imperfect evidence;
- triggered under EXP-009 decision-relevant uncertainty;
- not yet tested for richer interacting or temporally propagating decisions.

---

## 41. Generalisation Kill Condition

The earlier concern that DARA-DT might only work for capacity has been tested.

EXP-007 and EXP-009 include:

```text
Capacity
Status
Location / Availability
```

### Current Status

```text
NOT TRIGGERED
```

The behaviour generalises across these three controlled dependency families.

This is bounded generalisation, not universal generalisation.

---

## 42. Entity-Filtering Kill Condition

If entity filtering reproduced the complete DARA-DT trade-off, dependency
reasoning would be difficult to defend as necessary.

EXP-009 directly tested this.

### Current Status

```text
NOT TRIGGERED
```

Entity filtering preserves more autonomy but misses required interventions.

---

# Part X — Contribution Ladder

## 43. Level 1 — Engineering Contribution

```text
Implemented modular DARA-DT research prototype.
```

Status:

```text
ACHIEVED
```

---

## 44. Level 2 — Controlled Experimental Contribution

```text
Controlled evidence distinguishes divergence quantity, decision relevance,
decision impact, evidence quality and decision-conditioned uncertainty.
```

Status:

```text
ACHIEVED WITH BOUNDED SCOPE
```

---

## 45. Level 3 — Cross-Dependency Mechanism

```text
Relevant mechanisms operate across capacity, status and
location / availability dependencies.
```

Status:

```text
ACHIEVED WITHIN CONTROLLED MATRICES
```

This level was previously dependent on EXP-007.

EXP-007 has now completed that test.

---

## 46. Level 4 — Strong Comparative Contribution

```text
DARA-DT provides assurance information or performance not captured by strong
alternative mechanisms.
```

Status:

```text
NOT ESTABLISHED
```

Evidence against the claim currently includes:

```text
EXP-007 → Runtime-contract equivalence
EXP-008 → Runtime-contract equivalence
EXP-009 → Runtime-contract equivalence
```

This is now the principal contribution bottleneck.

---

## 47. Level 5 — Distinct Research Contribution

```text
Systematic prior-work review plus comparative experiments demonstrate a
defensible mechanism that adds knowledge beyond established alternatives.
```

Status:

```text
NOT ESTABLISHED
```

A new experiment alone cannot establish this level.

Both literature differentiation and experimental differentiation are required.

---

# Part XI — Claim Permission Matrix

## 48. Currently Permitted Claims

| Claim | Status |
|---|---|
| DARA-DT investigates physical–digital divergence | Supported |
| The prototype implements decision dependency mapping | Supported |
| The prototype distinguishes relevant and irrelevant divergence | Supported |
| Global divergence can over-intervene in controlled experiments | Supported |
| Decision relevance alone can over-intervene | Supported |
| Equal divergence magnitude can produce different decision outcomes | Supported |
| Decision-impact reasoning reduced FI in EXP-005 | Supported |
| Imperfect evidence affects assurance reliability | Supported |
| The mechanism has been tested across capacity, status and location/availability | Supported within controlled matrices |
| Global uncertainty can over-intervene under decision-irrelevant uncertainty | Supported |
| Entity filtering alone is insufficient in EXP-009 | Supported |
| DARA-DT and uncertainty-aware runtime contracts are equivalent on primary binary outcomes in EXP-008 and EXP-009 | Supported |
| Runtime-contract equivalence is a current threat to the contribution | Supported |
| DARA-DT has demonstrated superior performance to strong runtime contracts | **Not supported** |
| DARA-DT preserves more autonomy than the uncertainty-aware contract | **Not supported** |
| Decision-specific assurance is novel | **Not supported** |
| Runtime DT assurance is novel | **Not supported** |
| DARA-DT is the first framework of its type | **Not supported** |
| DARA-DT is safer than established assurance systems | **Not supported** |
| DARA-DT novelty is confirmed | **Not supported** |

---

# Part XII — Evidence Strength

## 49. Physical–Digital Divergence

```text
Implementation:             STRONG
Controlled evidence:        STRONG
Cross-dependency evidence:  MODERATE
Novelty:                    LOW
```

---

## 50. Decision Relevance

```text
Implementation:             STRONG
Controlled evidence:        STRONG
Cross-dependency evidence:  STRONG WITHIN CURRENT MATRICES
Differentiation:            LIMITED
Novelty:                    HIGH OVERLAP
```

---

## 51. Decision Impact

```text
Implementation:             STRONG
Controlled evidence:        STRONG
Cross-dependency evidence:  SUPPORTED
Differentiation:            WEAKENED BY CONTRACT EQUIVALENCE
Novelty:                    CANDIDATE / HIGH THREAT
```

---

## 52. Evidence-Aware Assurance

```text
Implementation:             STRONG
Controlled evidence:        STRONG
Evidence-quality coverage:  STALE / MISSING / CONFLICTING
Cross-dependency evidence:  SUPPORTED
Novelty as isolated idea:   LOW
```

---

## 53. Decision-Sensitive Evidence Uncertainty

```text
Implementation:             STRONG
Controlled evidence:        STRONG
Cross-dependency evidence:  SUPPORTED
Advantage over global:      SUPPORTED
Advantage over entity filter:
                            SUPPORTED ON SAFETY/TRADE-OFF
Advantage over strong runtime contract:
                            NOT SUPPORTED
Novelty:                    UNRESOLVED
```

---

## 54. Integrated DARA-DT Mechanism

```text
Implementation:             SUBSTANTIAL
Controlled evidence:        STRONG
Cross-dependency evidence:  SUPPORTED
Imperfect-evidence evidence:
                            SUPPORTED
Strong-baseline evidence:   UNFAVOURABLE / EQUIVALENT
Novelty:                    NOT ESTABLISHED
```

---

# Part XIII — Research Integrity Gate

## 55. Completed Requirements

```text
[x] EXP-007 cross-dependency evaluation completed

[x] Runtime-contract baseline implemented

[x] Runtime-contract comparison completed under reliable evidence

[x] Runtime-contract comparison completed under imperfect evidence

[x] Decision-relevant vs irrelevant uncertainty tested

[x] Entity-filter baseline tested

[x] Framework failure / falsification conditions documented

[x] EXP-009 pre-registered kill tests evaluated

[x] Negative results retained

[x] Generalisation boundaries documented
```

---

## 56. Requirements Still Outstanding

```text
[ ] Systematic closest-prior-work review completed to publication standard

[ ] Strong global Twin-fidelity baseline evaluated

[ ] Operational-envelope comparator evaluated if justified

[ ] AI-uncertainty comparator evaluated when a learned controller requires it

[ ] Compound / interacting decision dependencies evaluated

[ ] Temporal or cascading decision dependencies evaluated

[ ] Authority-state consequences evaluated beyond binary intervention

[ ] Operational logistics consequences integrated into assurance evaluation

[ ] Runtime-contract equivalence challenged under richer decision structures

[ ] Candidate contribution remains meaningful after all strong comparators

[ ] Final novelty claim independently re-audited
```

---

# Part XIV — Supervisor-Facing Formulation

## 57. Current Safe Formulation

> **DARA-DT investigates how physical–digital divergence, decision
> dependencies, physical validity and runtime evidence quality interact in
> runtime assurance for AI-driven logistics Digital Twins. Controlled
> experiments show that decision-sensitive assurance can reduce unnecessary
> intervention caused by globally irrelevant uncertainty, while also showing
> that strong uncertainty-aware runtime contracts reproduce the same primary
> binary safety–autonomy trade-off in the decision structures evaluated so
> far.**

This is currently the preferred supervisor-facing formulation.

---

## 58. Current Research Challenge

The next question is:

> **Does explicit decision-conditioned physical–digital divergence provide
> additional assurance value when autonomous decisions involve interacting,
> compound, cross-entity or temporally propagating dependencies that cannot be
> represented adequately by the local runtime contracts evaluated so far?**

This is a research question.

It is not yet a contribution claim.

---

## 59. Formulation That Must Not Yet Be Used

Do not currently state:

> DARA-DT is a novel runtime-assurance framework that outperforms existing
> runtime contracts.

The repository evidence does not support that statement.

Do not state:

> DARA-DT improves autonomy over uncertainty-aware runtime contracts.

EXP-009 directly contradicts that statement in the frozen matrix.

---

# Part XV — Next Novelty Gate

## 60. Why Another Similar Matrix Is Insufficient

The project should not create EXP-010 simply by adding:

```text
more vehicles
more capacity values
more stale evidence
more missing evidence
more conflicting evidence
```

to the same decision structure.

That would increase sample count without addressing the central novelty threat.

The next experiment must challenge the reason runtime-contract equivalence may
currently occur.

---

## 61. Current Explanation for Equivalence

The decisions evaluated so far are relatively local and explicit.

For example:

```text
Vehicle capacity >= Order demand
```

or:

```text
Vehicle status == operational
```

or:

```text
Vehicle available AND location permitted
```

These requirements map naturally to runtime contracts.

Therefore a plausible explanation for EXP-007 through EXP-009 is:

> **The tested decision structures are sufficiently local and explicit that a
> strong runtime contract captures the same information required for the
> binary intervention decision.**

This explanation must now be challenged directly.

---

## 62. Candidate EXP-010 Direction

A scientifically justified next experiment should test richer dependency
structures.

Candidate mechanisms include:

```text
Cross-Entity Dependency
```

Example:

```text
Vehicle A assignment depends on
Vehicle B availability because B is the recovery vehicle.
```

---

```text
Compound Dependency
```

Example:

```text
Assignment valid only if:

capacity sufficient
AND
vehicle operational
AND
handover resource available.
```

---

```text
Temporal Dependency
```

Example:

```text
Decision valid now only if a state dependency remains valid
through the expected execution interval.
```

---

```text
Cascading Decision Dependency
```

Example:

```text
Decision D1 changes the state required by Decision D2.
```

---

```text
Divergence Propagation
```

Example:

```text
A physical–digital mismatch in one resource changes the validity
of downstream decisions involving other resources.
```

The experiment should determine whether runtime-contract equivalence survives.

---

## 63. Candidate EXP-010 Research Question

A defensible candidate question is:

> **Does runtime-contract equivalence persist when autonomous logistics
> decisions depend on interacting physical–digital state dependencies across
> multiple entities or decision stages?**

The wording deliberately allows either answer.

---

## 64. Candidate EXP-010 Falsification Principle

The experiment must be designed so that:

```text
DARA-DT may win
DARA-DT may tie
DARA-DT may lose
```

All three outcomes must remain possible.

If the strong runtime contract continues to reproduce DARA-DT behaviour:

```text
the contribution must narrow further.
```

If DARA-DT performs differently:

```text
the mechanism responsible for the difference must be isolated.
```

The result must not automatically be attributed to the complete framework.

---

# Part XVI — Research Decisions

## 65. Decision 1 — Do Not Broaden Technologically

Do not add unrelated complexity simply to make the project appear advanced.

Avoid introducing:

```text
LLMs
blockchain
multi-agent systems
complex cybersecurity architecture
distributed streaming infrastructure
```

unless required by a specific research question.

---

## 66. Decision 2 — Protect the Research Question, Not DARA-DT

DARA-DT is a hypothesis and experimental framework.

It is not a conclusion that must be defended.

If evidence demonstrates that runtime contracts are sufficient, that result
must remain visible.

---

## 67. Decision 3 — Do Not Engineer a DARA-DT Win

Future conditions must be motivated independently of expected policy
performance.

Do not create scenarios specifically because DARA-DT is known to outperform a
baseline in them.

Pre-register:

- experimental factors;
- conditions;
- comparators;
- metrics;
- success criteria;
- kill tests;

before interpreting the result.

---

## 68. Decision 4 — Keep Decision Risk Provisional

The conceptual chain has previously included:

```text
Evidence Reliability
        ↓
Decision Risk
        ↓
Runtime Assurance
```

However, Decision Risk should not become a major subsystem merely to
differentiate DARA-DT.

It should be introduced only if a specific research question and experimental
need require explicit risk aggregation.

Current status:

```text
PROVISIONAL
```

---

# Part XVII — Final Novelty Position

## 69. What Is Established

```text
Digital Twin assurance              ESTABLISHED
Runtime assurance                   ESTABLISHED
Continuous DT assurance             ESTABLISHED
Runtime assumption monitoring       ESTABLISHED
Contract-based runtime monitoring   ESTABLISHED
Decision assurance                  ESTABLISHED / ACTIVE
Decision feasibility                ESTABLISHED
Adaptive authority                  ESTABLISHED
Physical–digital fidelity           ESTABLISHED
Evidence reliability                ESTABLISHED
```

DARA-DT must not claim these concepts individually as novel.

---

## 70. What Has Been Experimentally Established in This Repository

```text
Divergence count alone is insufficient
        → SUPPORTED

Decision relevance can improve selectivity
        → SUPPORTED

Decision relevance is not equivalent to decision invalidity
        → SUPPORTED

Equal divergence magnitude can have different decision consequences
        → SUPPORTED

Decision-impact reasoning can reduce false intervention
        → SUPPORTED IN CONTROLLED CONDITIONS

Evidence reliability affects assurance behaviour
        → SUPPORTED

Impact reasoning extends across three dependency families
        → SUPPORTED

Global uncertainty can be unnecessarily conservative
        → SUPPORTED

Entity filtering alone is insufficient
        → SUPPORTED IN EXP-009

Runtime-contract equivalence
        → OBSERVED REPEATEDLY
```

---

## 71. What Has Been Falsified or Weakened

```text
DARA-DT aggregate autonomy advantage over uncertainty-aware contract
        → FALSIFIED IN EXP-009

DARA-DT binary assurance superiority over uncertainty-aware contract
        → FALSIFIED IN EXP-009

Runtime-contract equivalence as merely a one-off EXP-007 result
        → REJECTED; EQUIVALENCE REPEATS IN EXP-008 AND EXP-009

Capacity-only explanation
        → WEAKENED / NOT SUPPORTED BY CROSS-DEPENDENCY RESULTS

Trivial entity-filter explanation
        → NOT SUPPORTED BY EXP-009
```

---

## 72. What Remains Open

```text
Decision-conditioned physical–digital divergence
        → CANDIDATE, HIGH THREAT

Divergence-caused validity reasoning
        → CANDIDATE, HIGH OVERLAP

Added value beyond strong runtime contracts
        → NOT ESTABLISHED

Added value under compound dependencies
        → UNTESTED

Added value under cross-entity dependencies
        → UNTESTED

Added value under temporal dependencies
        → UNTESTED

Added value under cascading decisions
        → UNTESTED

Operational value of RESTRICT vs DEFER vs FALLBACK
        → UNTESTED

Added value over strong global Twin-fidelity assurance
        → PARTIALLY TESTED

Confirmed novelty
        → NOT ESTABLISHED
```

---

## 73. Current Research Decision

```text
CONTINUE
        ↓
Preserve EXP-007–009 falsification evidence
        ↓
Do not claim superiority
        ↓
Challenge runtime-contract equivalence
        ↓
Use richer decision structures
        ↓
Pre-register EXP-010
        ↓
Run strong comparator experiment
        ↓
Accept win, tie or loss
        ↓
Refine contribution from evidence
        ↓
Complete systematic closest-prior-work review
```

---

# 74. Final Position

The strongest current DARA-DT research proposition is not that Digital Twins
require runtime assurance.

It is not that autonomous decisions should be checked before execution.

It is not that uncertainty should affect autonomous authority.

It is not even that decision dependencies are useful for assurance.

All of these ideas have substantial overlap with existing concepts and
mechanisms.

The sharper unresolved proposition is:

> **Whether explicit physical–digital divergence contains additional
> runtime-assurance information when conditioned on the dependencies and
> validity of AI-generated decisions whose state relationships are richer
> than the local runtime contracts evaluated so far.**

This proposition remains scientifically useful because it is falsifiable.

The current evidence already demonstrates that it can fail.

Across EXP-007, EXP-008 and EXP-009, strong runtime contracts reproduce the
primary binary outcomes of the DARA-DT mechanism in the tested decision
structures.

Therefore the present novelty position is:

> **DARA-DT is a technically implemented and experimentally developed
> research framework with evidence for decision-sensitive treatment of
> physical–digital divergence and runtime uncertainty. However, repeated
> runtime-contract equivalence prevents a claim of distinct comparative
> advantage or confirmed novelty. The next research gate is to determine
> whether this equivalence persists under richer interacting, cross-entity or
> temporally propagating decision dependencies.**

That conclusion should remain unchanged unless subsequent literature or
experimental evidence justifies changing it.
