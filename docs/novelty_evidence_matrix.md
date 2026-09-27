# DARA-DT Novelty Evidence and Falsification Matrix

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Framework:** DARA-DT  
**Research Identity:** Trustworthy Intelligent Systems  
**Application Domain:** Autonomous Logistics Systems  
**Document Status:** Living Novelty, Differentiation and Falsification Record  
**Evidence Base:** EXP-001 to EXP-006  
**Next Novelty Gate:** EXP-007 — Cross-Dependency Generalisation  
**Novelty Status:** Not Yet Established

---

## 1. Purpose

This document evaluates whether DARA-DT contains a defensible research
contribution after comparison with adjacent and potentially equivalent prior
work.

It is deliberately designed to challenge the project rather than defend it.

The objective is not to prove that DARA-DT is novel.

The objective is to determine:

1. which concepts are already established;
2. which DARA-DT mechanisms overlap with prior work;
3. which experimental findings are currently supported;
4. which candidate differentiators remain unresolved;
5. which experiments could falsify those differentiators; and
6. what evidence would be required before making a contribution claim.

The central rule is:

> **Implementation is not novelty, experimental success is not novelty, and
> integration of existing components is not automatically novelty.**

---

# Part I — Research Position

## 2. Central Research Question

The canonical research question is:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

The developing DARA-DT reasoning chain is:

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
Decision Risk
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

Not every element of this chain is expected to be novel.

Most individual elements have substantial prior work.

The research question is whether a particular relationship between these
elements produces new and useful knowledge.

---

## 3. Current Candidate Contribution

The current candidate contribution is:

> **A decision-conditioned runtime-assurance mechanism that evaluates
> physical–digital divergence relative to the state dependencies and physical
> validity of an AI-generated logistics decision, and experimentally tests
> whether this information improves intervention decisions beyond global
> Digital Twin fidelity, generic divergence monitoring, and simpler runtime
> validity mechanisms.**

Status:

```text
CANDIDATE CONTRIBUTION
NOT CONFIRMED NOVELTY
```

The wording is intentionally narrower than earlier formulations.

---

# Part II — Novelty Assessment Rules

## 4. Evidence Categories

Every candidate contribution is assessed across five dimensions:

```text
Prior-Work Overlap
Implementation Evidence
Experimental Evidence
Generalisation Evidence
Differentiation Evidence
```

A feature should not progress toward a contribution claim simply because it
has strong implementation evidence.

---

## 5. Status Scale

### ESTABLISHED

Substantial prior work clearly exists.

Do not claim novelty.

### HIGH OVERLAP

The DARA-DT mechanism strongly resembles existing research.

A narrower differentiator is required.

### CANDIDATE DIFFERENTIATOR

A potentially meaningful distinction exists but has not survived sufficient
literature and experimental challenge.

### EXPERIMENTALLY SUPPORTED

The repository contains controlled evidence for the stated behaviour.

This does not imply novelty.

### REQUIRES GENERALISATION

The result is currently tied to a narrow dependency, scenario or experimental
construction.

### NOVELTY THREAT

Existing research may already contain an equivalent mechanism.

### FALSIFICATION REQUIRED

A direct experiment is required to determine whether the candidate
distinction survives.

### NOT ESTABLISHED

Available evidence is insufficient for a novelty or contribution claim.

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
- lifecycle assurance; and
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

Contemporary work explicitly investigates continuous runtime assurance for
Digital Twins.

DARTER is a particularly important example.

Its scope includes:

- runtime data verification;
- model-performance monitoring;
- validated thresholds;
- operational-domain monitoring;
- distribution drift;
- automated evidence generation; and
- continuously maintained assurance information.

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

Contemporary Digital Twin research also includes contract-based runtime
monitoring.

Such systems can verify runtime signals and controller behaviour against
explicit conditions and change control behaviour when violations occur.

This is highly relevant because DARA-DT also reasons about whether runtime
conditions required by a decision remain acceptable.

### Critical Question

> Is a DARA-DT decision dependency simply another form of runtime contract?

If yes, the contribution must be narrowed substantially.

### Threat Level

```text
VERY HIGH
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

can be interpreted as:

```text
decision dependency
```

or:

```text
runtime assumption / contract.
```

This creates one of the strongest conceptual threats to DARA-DT.

### Critical Question

> Does explicit physical–digital divergence provide information that cannot
> be obtained from monitoring the decision's operational assumptions alone?

### Threat Level

```text
VERY HIGH
```

---

## 10. Threat E — Decision Assurance

Decision assurance increasingly focuses assurance evidence on operational
decisions rather than model outputs alone.

Relevant concepts include:

- decision-centred test design;
- operational confidence thresholds;
- escalation conditions;
- governance boundaries;
- authority constraints;
- traceability from evidence to decisions; and
- mission or operational context.

Therefore:

```text
decision-specific assurance
```

cannot itself be treated as the DARA-DT novelty.

### Threat Level

```text
VERY HIGH
```

---

## 11. Threat F — Decision Feasibility

Decision feasibility and constraint validation are established concepts.

For example:

```text
capacity >= demand
```

is a conventional feasibility constraint.

Therefore the following alone is not a contribution:

```text
check whether capacity satisfies demand.
```

### Critical Question

The relevant DARA-DT question is instead:

> Does identifying the physical–digital mismatch responsible for changing a
> decision's feasibility provide additional runtime-assurance information?

### Threat Level

```text
HIGH
```

---

## 12. Threat G — Adaptive Autonomy

Runtime systems already regulate authority through mechanisms such as:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
HUMAN ESCALATION
```

Therefore adaptive authority itself is not a DARA-DT contribution.

The candidate distinction must concern the evidence used to change authority.

### Threat Level

```text
HIGH
```

---

# Part IV — Component-Level Novelty Matrix

## 13. Evidence Matrix

| DARA-DT Element | Closest Threat | Experimental Evidence | Generalisation | Novelty Position |
|---|---|---|---|---|
| Physical–digital divergence | DT fidelity / synchronisation | Strong | Multiple controlled cases | Established |
| Divergence magnitude | Error/fidelity metrics | EXP-004/005 | Capacity-heavy | Established |
| Runtime assurance | DARTER / runtime assurance | Strong implementation | Controlled | Established |
| Authority regulation | Adaptive autonomy | EXP-001–006 | Limited | High overlap |
| Decision dependencies | Contracts / assumptions | EXP-001–003 | Limited | Very high threat |
| Decision relevance | Assumption/contract monitoring | EXP-001–004 | Limited | Candidate |
| Decision impact | Feasibility/constraint checking | EXP-004/005 | Capacity only | High overlap |
| Evidence reliability | Data/sensor assurance | EXP-006 | Capacity only | Established concept |
| Decision-specific assurance | Decision assurance literature | EXP-001–006 | Limited | High overlap |
| Physical–digital divergence conditioned on decision dependency | Combined threat | EXP-001–006 | Not yet cross-dependency | Candidate differentiator |
| Divergence-caused validity change | Constraint + discrepancy reasoning | EXP-004/005 | Capacity only | Candidate differentiator |
| Integrated DARA-DT mechanism | All above | Developing | EXP-007 required | Candidate contribution |
| Decision risk | Risk-aware assurance | Conceptual | None | Not established |

---

# Part V — Experimental Claims

## 14. Finding 1 — Divergence Count Is Insufficient

EXP-001 and EXP-002 demonstrate that equal or larger quantities of divergence
do not necessarily imply greater significance to the current decision.

For example, divergence may exist on vehicles unrelated to the selected
vehicle.

### Supported Statement

> In the controlled DARA-DT experiments, divergence count alone does not
> reliably indicate whether intervention is required for the current
> decision.

### Novelty Status

```text
EXPERIMENTALLY SUPPORTED
NOT A NOVELTY CLAIM
```

---

## 15. Finding 2 — Decision Relevance Improves Selectivity

EXP-002 evaluates:

```text
No Assurance
Global Divergence
Decision-Relevant Assurance
```

Across the controlled seven-condition matrix:

```text
Decision-Relevant Assurance

TI  = 3
FI  = 0
MI  = 0
CNI = 4
Accuracy = 1.000
```

### Correct Interpretation

This establishes controlled feasibility.

It does not establish universal superiority.

### Novelty Status

```text
EXPERIMENTALLY SUPPORTED
```

---

## 16. Finding 3 — Relevance Is Not Validity

EXP-004 demonstrates that divergence can affect a decision dependency without
invalidating the decision.

Example:

```text
Twin capacity     = 10
Physical capacity = 9
Demand            = 5
```

The capacity variable is relevant.

However:

```text
9 >= 5
```

and the assignment remains physically feasible.

Therefore:

```text
Decision Relevance
        ≠
Decision Invalidity
```

within the controlled experiment.

### Status

```text
STRONG EXPERIMENTAL FINDING
```

---

## 17. Finding 4 — Divergence Magnitude Is Not Decision Impact

EXP-005 contains the controlled pair:

```text
I7
Twin capacity     = 10
Physical capacity = 7
Demand            = 5
Divergence        = 3
Decision          = Valid
```

and:

```text
I8
Twin capacity     = 10
Physical capacity = 7
Demand            = 8
Divergence        = 3
Decision          = Invalid
```

Therefore:

```text
same divergence magnitude
        ↓
different decision consequence
```

within the controlled conditions.

### Supported Statement

> Divergence magnitude alone is insufficient to determine decision impact in
> the EXP-005 capacity matrix.

### Status

```text
STRONG EXPERIMENTAL FINDING
REQUIRES GENERALISATION
```

---

## 18. Finding 5 — Impact Reasoning Improves Selectivity

EXP-005 produces:

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

> Within the controlled EXP-005 capacity matrix, decision-impact reasoning
> reduced unnecessary intervention relative to relevance-only assurance while
> retaining all required interventions.

### Status

```text
EXPERIMENTALLY SUPPORTED
CAPACITY-SPECIFIC
```

---

## 19. Finding 6 — Perfect Evidence Is an Unrealistic Upper Baseline

EXP-006 separates:

```text
Physical Ground Truth
        ≠
Runtime Evidence
        ≠
Digital Twin State
```

The deterministic impact baseline using reliable evidence achieves:

```text
Accuracy = 1.000
```

while evidence-aware impact under imperfect evidence achieves:

```text
Accuracy  = 0.833
Precision = 0.889
Recall    = 0.889
FI        = 1
MI        = 1
```

### Supported Statement

> Impact-aware assurance performance depends on the reliability of runtime
> evidence.

### Status

```text
EXPERIMENTALLY SUPPORTED
```

---

# Part VI — The Strongest Candidate Differentiator

## 20. What DARA-DT Should NOT Claim

The contribution should not be framed as:

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
adaptive autonomy.
```

All have significant prior work.

---

## 21. Stronger Candidate

The narrower candidate is:

> **Decision-conditioned physical–digital divergence: determining whether a
> mismatch between physical and Twin state affects a state dependency of the
> specific AI-generated decision and whether that mismatch changes the
> decision's physical validity.**

This can be represented as:

\[
D_t^{rel}(d_t)=Dep(d_t)\cap D_t
\]

followed by:

\[
I_t=f(d_t,D_t^{rel},E_t)
\]

where:

- \(d_t\) is the proposed decision;
- \(Dep(d_t)\) represents decision dependencies;
- \(D_t\) represents detected physical–digital divergence;
- \(D_t^{rel}\) represents decision-conditioned divergence;
- \(E_t\) represents runtime evidence; and
- \(I_t\) represents estimated decision impact.

The assurance action is then conceptually:

\[
A_t=\pi(d_t,D_t^{rel},I_t,E_t)
\]

The notation is not itself a contribution.

The contribution would need to arise from the demonstrated behaviour of the
mechanism.

---

# Part VII — Critical Differentiation Tests

## 22. Test A — Global Fidelity vs Decision-Conditioned Divergence

### Competing Explanation

A global Digital Twin fidelity score may already provide sufficient
information.

### Required Experiment

Construct conditions where:

```text
Global divergence is high
Decision relevance is low
```

and:

```text
Global divergence is low
Decision relevance is high
```

Then compare intervention quality.

### Existing Evidence

EXP-001 and EXP-002 provide initial evidence.

### Remaining Requirement

Broader dependency and stochastic evaluation.

---

## 23. Test B — Runtime Contract vs DARA-DT

### Competing Explanation

A runtime contract such as:

```text
capacity >= demand
```

may solve the same problem without explicitly modelling physical–digital
divergence.

### Required Comparison

Compare:

```text
Contract / assumption monitoring
```

against:

```text
Divergence + dependency + impact reasoning.
```

Measure:

- TI;
- FI;
- MI;
- CNI;
- autonomy availability;
- evidence requirements; and
- failure conditions.

### Status

```text
NOT YET COMPLETED
HIGH PRIORITY
```

---

## 24. Test C — Ordinary Feasibility vs DARA-DT

### Competing Explanation

The decision-impact mechanism may simply reproduce conventional feasibility
checking.

### Required Question

> What does explicit knowledge of physical–digital divergence add beyond
> evaluating the physical constraint directly?

Potential answers must be demonstrated experimentally rather than asserted.

### Status

```text
UNRESOLVED
```

---

## 25. Test D — Global Twin Trust vs Decision-Level Trust

### Competing Explanation

A sufficiently strong continuous assurance framework may already determine
whether the Twin is trustworthy enough for use.

### Required Experiment

Construct conditions in which:

```text
Twin globally degraded
but current decision remains valid
```

and:

```text
Twin globally acceptable
but a small local divergence invalidates the current decision.
```

Then compare:

```text
global trust/fidelity
```

with:

```text
decision-conditioned divergence.
```

### Status

```text
PARTIALLY TESTED
REQUIRES STRONGER BASELINE
```

---

# Part VIII — 2×2 Differentiation Model

## 26. Core Experimental Quadrants

A strong DARA-DT evaluation should include:

| | Low Decision Relevance | High Decision Relevance |
|---|---|---|
| **Low Global Divergence** | A | C |
| **High Global Divergence** | B | D |

### A — Low Divergence / Low Relevance

Expected:

```text
ALLOW
```

### B — High Divergence / Low Relevance

Critical test of global assurance.

Expected DARA-DT hypothesis:

```text
Autonomy may remain justified.
```

### C — Low Divergence / High Relevance

Critical test of decision-conditioned assurance.

A small divergence may still invalidate the decision.

### D — High Divergence / High Relevance

Both global and decision-conditioned approaches may intervene.

This quadrant alone provides little differentiation.

The strongest scientific evidence comes from:

```text
B versus C
```

because they separate:

```text
magnitude
```

from:

```text
decision consequence.
```

---

# Part IX — EXP-007 as a Novelty Gate

## 27. EXP-007 Research Question

> **Does the relationship between physical–digital divergence, decision
> relevance, decision impact and runtime intervention generalise across
> different logistics decision dependencies?**

Candidate dependency families:

```text
Capacity
Operational Status
Location / Availability
```

---

## 28. Why EXP-007 Is Critical

Current later evidence is heavily capacity-based.

Without EXP-007, a reviewer could reasonably argue:

> The framework is primarily a capacity-threshold mechanism expressed using
> Digital Twin terminology.

EXP-007 must challenge that explanation.

---

## 29. EXP-007 Success Criterion

The objective should not be:

```text
make DARA-DT win.
```

The objective should be:

```text
determine whether the same conceptual mechanism remains meaningful across
different dependency semantics.
```

---

## 30. EXP-007 Possible Outcomes

### Outcome A — Generalises

The mechanism produces useful discrimination across capacity, operational
status and location/availability.

Implication:

```text
Framework-level interpretation becomes more defensible.
```

Novelty is still not automatically established.

### Outcome B — Partially Generalises

Some dependencies require different impact semantics.

Implication:

```text
DARA-DT may require dependency-specific impact models.
```

This would still be a valuable research result.

### Outcome C — Does Not Generalise

The mechanism provides little value outside capacity.

Implication:

```text
Broad framework claim should be rejected or narrowed.
```

This is scientifically valid.

---

# Part X — Strong Novelty Kill Conditions

## 31. Literature Kill Condition

The novelty case is substantially weakened if prior work is identified that
already integrates:

1. physical system state;
2. Digital Twin state;
3. explicit physical–digital discrepancy;
4. a specific autonomous decision;
5. explicit dependencies or contracts for that decision;
6. runtime mapping of discrepancy to those dependencies;
7. evaluation of decision consequence or validity;
8. intervention based on that consequence;
9. adaptive authority regulation; and
10. evaluation across multiple dependency types.

If such work exists, DARA-DT must identify a narrower contribution.

---

## 32. Experimental Kill Condition

The framework-level hypothesis should be weakened if:

```text
simple contract monitoring
```

or:

```text
ordinary feasibility checking
```

performs equivalently across the relevant experiments while requiring less
information and complexity.

This is a particularly important falsification criterion.

---

## 33. Generalisation Kill Condition

If EXP-007 demonstrates that the mechanism only works for capacity:

```text
general DARA-DT framework claim
        ↓
should be rejected or narrowed.
```

---

# Part XI — Stronger Baseline Roadmap

## 34. Current Baselines

Implemented comparisons include:

```text
No Assurance
Global Divergence
Fixed Magnitude
Decision Relevance
Deterministic Impact
Evidence-Aware Impact
```

These are useful but insufficient for a strong final contribution claim.

---

## 35. Required Stronger Baselines

Future experiments should consider:

### Runtime Contract / Assumption Baseline

Tests whether explicit decision assumptions provide equivalent performance.

### Global Fidelity Baseline

Tests whether overall Twin quality is sufficient.

### Operational-Envelope Baseline

Tests whether predefined valid operating regions provide equivalent
protection.

### AI-Uncertainty Baseline

Where a learned controller is introduced, tests whether model confidence
provides equivalent assurance information.

### Combined Fidelity + Uncertainty Baseline

Tests whether decision-conditioned divergence adds value beyond established
trust signals.

Only baselines that can be implemented fairly should be included.

---

# Part XII — Contribution Ladder

## 36. Level 1 — Engineering Contribution

```text
Implemented modular DARA-DT research prototype
```

Status:

```text
ACHIEVED
```

---

## 37. Level 2 — Experimental Contribution

```text
Controlled evidence showing divergence magnitude, relevance, impact and
evidence quality can produce different assurance outcomes.
```

Status:

```text
ACHIEVED WITH BOUNDED SCOPE
```

---

## 38. Level 3 — General Mechanism Contribution

```text
Decision-conditioned divergence mechanism generalises across different
decision dependencies.
```

Status:

```text
NOT YET ESTABLISHED
EXP-007 REQUIRED
```

---

## 39. Level 4 — Comparative Research Contribution

```text
Mechanism provides information or performance not captured by strong
alternative assurance approaches.
```

Status:

```text
NOT YET ESTABLISHED
STRONGER BASELINES REQUIRED
```

---

## 40. Level 5 — Novel Research Contribution

```text
Systematic prior-work review + generalisation + comparative experiments
demonstrate a defensible new contribution.
```

Status:

```text
NOT YET ESTABLISHED
```

---

# Part XIII — Claim Permission Matrix

## 41. Currently Permitted Claims

| Claim | Status |
|---|---|
| DARA-DT investigates physical–digital divergence | Supported |
| The prototype implements decision dependency mapping | Supported |
| The prototype distinguishes relevant and irrelevant divergence | Supported |
| Global divergence can over-intervene in the controlled experiments | Supported |
| Decision relevance can over-intervene in EXP-004 | Supported |
| Equal divergence magnitude can produce different outcomes in EXP-005 | Supported |
| Decision-impact reasoning reduced FI in EXP-005 | Supported |
| Imperfect evidence produced one FI and one MI in EXP-006 | Supported |
| DARA-DT has been validated across all logistics dependencies | Not supported |
| Decision-specific assurance is novel | Not supported |
| Runtime DT assurance is novel | Not supported |
| DARA-DT is the first framework of its type | Not supported |
| DARA-DT is safer than established assurance systems | Not supported |
| DARA-DT novelty is confirmed | Not supported |

---

# Part XIV — Evidence Strength

## 42. Physical–Digital Divergence

```text
Implementation:          STRONG
Controlled evidence:     STRONG
Generalisation:          MODERATE
Novelty:                 LOW
```

---

## 43. Decision Relevance

```text
Implementation:          STRONG
Controlled evidence:     STRONG
Generalisation:          LIMITED
Differentiation:         UNRESOLVED
Novelty:                 CANDIDATE
```

---

## 44. Decision Impact

```text
Implementation:          STRONG
Controlled evidence:     STRONG
Generalisation:          CAPACITY-LIMITED
Differentiation:         UNRESOLVED
Novelty:                 CANDIDATE / HIGH THREAT
```

---

## 45. Evidence-Aware Assurance

```text
Implementation:          STRONG
Controlled evidence:     STRONG
Generalisation:          LIMITED
Novelty as isolated idea: LOW
```

---

## 46. Integrated DARA-DT Mechanism

```text
Implementation:          SUBSTANTIAL
Controlled evidence:     DEVELOPING
Cross-dependency evidence: NOT YET ESTABLISHED
Strong-baseline evidence:  NOT YET ESTABLISHED
Novelty:                   CANDIDATE
```

---

# Part XV — Research Integrity Gate

## 47. Requirements Before a Strong Contribution Claim

Before describing DARA-DT as a distinct research contribution, require:

```text
[ ] EXP-007 cross-dependency evaluation completed

[ ] Runtime contract / assumption baseline investigated

[ ] Global fidelity baseline strengthened

[ ] DARTER comparison maintained against current outputs

[ ] Decision-assurance literature reviewed

[ ] Decision-feasibility equivalence tested

[ ] At least one framework failure condition documented

[ ] Generalisation boundaries documented

[ ] Stronger comparative experiments completed

[ ] Closest prior work systematically reviewed

[ ] Contribution remains meaningful after generic AI/DT terminology is removed
```

---

# Part XVI — Supervisor-Facing Formulation

## 48. Current Safe Formulation

> **DARA-DT investigates whether physical–digital divergence can be
> conditioned on the dependencies and physical validity of individual
> AI-generated logistics decisions, and whether this information provides
> useful runtime-assurance evidence beyond global Digital Twin mismatch.**

This is currently preferable to claiming a novel framework.

---

## 49. Stronger Future Formulation

If EXP-007 and stronger baseline comparisons support the hypothesis:

> **The research develops and evaluates a decision-conditioned
> physical–digital divergence mechanism for runtime assurance across multiple
> autonomous logistics decision dependencies.**

A novelty claim would still require final systematic prior-work evaluation.

---

# Part XVII — Immediate Research Decisions

## 50. Decision 1 — Do Not Broaden

Do not introduce unrelated technologies simply to increase sophistication.

Avoid adding:

```text
LLMs
blockchain
multi-agent architecture
cybersecurity frameworks
complex sensor fusion
distributed infrastructure
```

unless required by a research question.

---

## 51. Decision 2 — Test Generalisation First

EXP-007 should test:

```text
Capacity
Operational Status
Location / Availability
```

with reliable evidence first.

This isolates dependency type.

---

## 52. Decision 3 — Add Stronger Comparator After EXP-007

If the mechanism survives cross-dependency testing, the next major scientific
challenge should compare it against:

```text
runtime contract / assumption monitoring
```

rather than creating another weak baseline.

---

## 53. Decision 4 — Keep Decision Risk Provisional

The conceptual chain currently includes:

```text
Evidence Reliability
        ↓
Decision Risk
        ↓
Runtime Assurance
```

but Decision Risk should not yet become a major subsystem.

It should be formalised only if experimental evidence demonstrates that
relevance, impact and evidence reliability require explicit combined risk
reasoning.

---

# Part XVIII — Final Novelty Position

## 54. What Is Established

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

---

## 55. What Remains Open

```text
Decision-conditioned physical–digital divergence
        → CANDIDATE

Divergence-caused decision validity change
        → CANDIDATE

Integrated divergence → dependency → impact → authority mechanism
        → CANDIDATE

Cross-dependency generalisation
        → UNTESTED

Added value over runtime contracts / assumptions
        → UNRESOLVED

Added value over global Twin trust/fidelity
        → PARTIALLY TESTED

Confirmed novelty
        → NOT ESTABLISHED
```

---

## 56. Current Research Decision

```text
CONTINUE
        ↓
Protect the research question, not the framework
        ↓
EXP-007 cross-dependency test
        ↓
Strong runtime-contract comparator
        ↓
Broader stress testing
        ↓
Systematic closest-work comparison
        ↓
Refine or reject candidate contribution from evidence
```

---

## 57. Final Position

The strongest current DARA-DT research proposition is not that Digital Twins
need runtime assurance, nor that autonomous decisions should be checked
before execution.

Those ideas already have substantial prior work.

The sharper unresolved proposition is:

> **Whether the discrepancy between physical and Digital Twin state contains
> additional assurance information when it is conditioned on the state
> dependencies and physical validity of the specific AI-generated decision
> seeking execution authority.**

This proposition is scientifically useful because it is falsifiable.

It can fail if:

```text
runtime contracts perform equivalently,
```

if:

```text
global Twin trust provides the same information,
```

or if:

```text
the mechanism does not generalise beyond capacity.
```

Those possibilities should be tested rather than excluded.

Accordingly, the current status is:

> **DARA-DT is a technically implemented and experimentally supported
> research hypothesis with a plausible candidate differentiator, but its
> novelty remains to be established through cross-dependency validation,
> stronger comparator experiments and systematic closest-prior-work
> analysis.**
