# Closest Prior Work and Research Differentiation

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Research Area:** Trustworthy Intelligent Systems  
**Application Domain:** Autonomous Logistics Systems  
**Document Status:** Living Novelty-Control Document  
**Last Research Position:** September 2026

---

## 1. Purpose

This document identifies research areas and systems that are closest to
DARA-DT.

Its purpose is not to claim novelty.

Its purpose is to continually test whether the proposed contribution is:

- already established;
- a direct adaptation of existing work;
- an incremental extension;
- a useful integration of existing mechanisms; or
- sufficiently differentiated to justify further investigation.

DARA-DT should not claim:

```text
"first"
"unique"
"no previous research"
"novel"
```

unless a systematic literature review provides sufficient evidence.

The current novelty status is:

> **Candidate contribution under investigation.**

---

## 2. DARA-DT Research Question

The central research question is:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

The developing mechanism is:

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

The research question must therefore be compared against work in several
overlapping fields rather than against Digital Twin literature alone.

---

# Part I — Closest Research Areas

## 3. Digital Twin Assurance

Digital Twin assurance is an established and rapidly developing research and
industrial-practice area.

Relevant concerns include:

- model fidelity;
- data quality;
- model validation;
- operational trustworthiness;
- uncertainty;
- synchronisation;
- lifecycle assurance;
- runtime monitoring; and
- assurance evidence.

DARA-DT therefore does **not** treat Digital Twin assurance itself as a new
research concept.

The relevant question is narrower:

> How should a detected mismatch between physical and digital state affect
> the authority of a specific AI-generated operational decision?

---

## 4. DNV-RP-A204

DNV-RP-A204 provides a structured recommended practice for assurance of
Digital Twins.

Its scope includes:

- Digital Twin quality;
- trustworthiness;
- risks associated with relying on Twin information;
- integration and deployment;
- operation;
- maintenance; and
- lifecycle assurance.

This work is highly relevant because DARA-DT also concerns the risk of acting
on Digital Twin information.

### Relationship to DARA-DT

DNV-RP-A204 establishes that:

```text
Digital Twin information must be trustworthy enough for its intended use.
```

DARA-DT investigates a more specific experimental question:

```text
When physical and Twin state diverge,
does that divergence affect the specific AI decision about to execute,
and should autonomous authority change as a result?
```

This should currently be treated as a possible complementary operational
mechanism rather than as a replacement for Digital Twin assurance standards.

---

## 5. Continuous Runtime Digital Twin Assurance

A particularly close body of work concerns continuous runtime assurance.

This significantly reduces the defensibility of any broad claim such as:

> "Existing Digital Twin assurance is static."

That statement is no longer supportable as a general characterisation.

Contemporary work explicitly investigates continuous assurance.

---

## 6. DARTER

The Alan Turing Institute's DARTER project — Digital Twin Assurance via
Runtime Trust and Evidence Reporting — is especially close to the DARA-DT
research area.

DARTER investigates continuous assurance for safety-critical Digital Twins.

Its architecture includes concerns such as:

- verification of incoming operational data;
- runtime model-performance evaluation;
- validated performance thresholds;
- structured assurance evidence;
- operational design-domain monitoring;
- distribution drift;
- continuous updating of assurance cases; and
- runtime trustworthiness.

Its primary experimental application is air traffic management, while the
methods are intended to be reusable across other sectors.

Transportation and logistics are explicitly relevant transfer domains.

### Novelty Threat

DARTER creates a **high novelty threat** to any claim that DARA-DT introduces:

```text
runtime Digital Twin assurance
continuous Digital Twin assurance
runtime evidence for Digital Twin assurance
runtime monitoring of Digital Twin trustworthiness
adaptive trust in Digital Twins
```

Those ideas are already represented in current work.

---

## 7. DARA-DT vs DARTER

The current candidate distinction is not:

```text
static assurance
vs
runtime assurance
```

because DARTER already operates at runtime.

Instead, DARA-DT investigates whether assurance can be linked directly to
the dependencies and physical validity of an individual autonomous decision.

The distinction under investigation is approximately:

```text
DARTER-type question:

Can this Digital Twin and its predictions continue to be trusted within
their validated operational domain?
```

versus:

```text
DARA-DT question:

Given a specific AI-generated decision,
does the current physical–digital divergence affect a state variable on
which that decision depends, and does the divergence change whether the
decision remains physically valid?
```

This distinction is promising but **not yet sufficient to establish
novelty**.

Further literature comparison is required.

---

# Part II — Runtime Assurance

## 8. Runtime Assurance as an Existing Field

Runtime assurance predates DARA-DT.

Existing approaches include concepts such as:

- safety monitors;
- runtime verification;
- operational envelopes;
- safety filters;
- fallback controllers;
- runtime assumption monitoring;
- Simplex-style architectures;
- safety cages;
- reachability-based protection;
- adaptive assurance; and
- runtime certification evidence.

DARA-DT must therefore avoid claiming that regulating autonomous authority at
runtime is itself new.

---

## 9. Runtime Assumption Monitoring

Runtime assumption monitoring is especially important to the novelty
assessment.

Such approaches monitor whether assumptions made during system design or
assurance remain valid during operation.

Conceptually:

```text
Assumption
        ↓
Runtime Observation
        ↓
Assumption Still Valid?
        ↓
Continue / Intervene
```

This is close to DARA-DT because a decision dependency can potentially be
interpreted as an operational assumption.

Example:

```text
Decision:
assign vehicle_01 to order_01

Implicit assumption:
vehicle_01 has sufficient capacity
```

DARA-DT may then detect:

```text
Twin capacity = 10
Physical capacity = 4
Demand = 5
```

and determine that the decision's capacity assumption no longer holds.

This creates a serious conceptual overlap.

---

## 10. Critical Novelty Question

One of the most important questions for the project is therefore:

> **Is decision-relevant divergence fundamentally different from runtime
> assumption monitoring, or is it a Digital Twin-specific implementation of
> the same principle?**

This question must remain visible throughout the research.

A weak answer would significantly reduce the novelty claim.

A strong answer would require evidence that DARA-DT introduces additional
decision-specific reasoning not adequately captured by existing assumption
monitoring.

---

# Part III — Physical–Digital Divergence

## 11. Divergence Detection Is Not Novel by Itself

Digital Twin research already investigates:

- model fidelity;
- synchronisation;
- state-estimation error;
- physical–digital consistency;
- drift;
- data quality;
- model discrepancy; and
- Twin updating.

Therefore:

```text
Physical State ≠ Digital Twin State
```

is not itself a research contribution.

Likewise, calculating:

```text
|physical value - Twin value|
```

is not sufficient novelty.

---

## 12. Candidate DARA-DT Distinction

The candidate contribution begins when divergence is interpreted relative to
a specific decision.

Let:

\[
Dep(d_t)
\]

represent the dependencies of decision \(d_t\).

Let:

\[
D_t
\]

represent detected physical–digital divergence.

Then:

\[
D_t^{rel}(d_t) = Dep(d_t) \cap D_t
\]

represents divergence affecting the current decision.

The candidate distinction is:

```text
Global Twin Fidelity
        ↓
How accurate is the Twin overall?

versus

Decision-Relevant Divergence
        ↓
Is the Twin wrong about something this decision depends on?
```

EXP-001 to EXP-003 provide controlled implementation evidence for this
mechanism.

They do not establish its originality.

---

# Part IV — Decision Impact

## 13. Relevance Is Not Enough

EXP-004 demonstrates that decision relevance does not necessarily imply
decision invalidity.

Example:

```text
Twin capacity     = 10
Physical capacity = 9
Demand            = 5
```

Capacity is relevant.

Divergence exists.

But:

```text
9 >= 5
```

so the assignment remains feasible.

This motivates another layer:

```text
Decision Impact / Validity
```

---

## 14. Decision-Specific Validity

DARA-DT therefore investigates:

```text
Does this divergence merely affect a dependency,
or does it invalidate this particular decision?
```

For a capacity-dependent decision:

\[
M = C_{physical} - q
\]

provides a controlled validity margin.

EXP-005 demonstrates that equal divergence magnitude can have different
decision consequences.

Example:

```text
Twin = 10
Physical = 7
Divergence = 3
```

With:

```text
Demand = 5
```

the decision remains valid.

With:

```text
Demand = 8
```

the decision becomes invalid.

This is stronger than global divergence magnitude.

However, constraint-aware decision validation is itself not automatically
novel.

The research question is whether its explicit integration with
physical–digital divergence and runtime authority creates a differentiated
assurance mechanism.

---

# Part V — Evidence Reliability

## 15. Runtime Evidence Is Another Existing Research Area

Evidence quality, sensor reliability, data quality and uncertainty are
established research topics.

DARA-DT therefore should not claim that recognising unreliable runtime
evidence is novel.

EXP-006 instead investigates a narrower issue:

> What happens to decision-impact-aware runtime assurance when the evidence
> used to estimate physical reality is imperfect?

---

## 16. EXP-006 Novelty Implication

EXP-006 establishes the architecture:

```text
Physical Ground Truth
        ≠
Runtime Evidence
        ≠
Digital Twin State
```

This is methodologically important.

However, the separation itself should not currently be presented as a novel
theoretical contribution.

Its value is that it prevents the DARA-DT evaluation from assuming that
runtime evidence always equals physical truth.

---

# Part VI — Adaptive Autonomous Authority

## 17. Adaptive Authority Is Not Novel by Itself

Existing autonomous-system assurance research already considers:

- switching controllers;
- fallback behaviour;
- degraded autonomy;
- operational envelopes;
- human intervention;
- runtime safety filters; and
- dynamic restriction of autonomous behaviour.

Therefore:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
```

should not be presented as a novel concept.

The candidate contribution concerns **what evidence causes authority to
change**.

---

## 18. Candidate Authority Logic

DARA-DT investigates authority regulation based on the chain:

```text
Physical–Digital Divergence
        ↓
Decision Dependency
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
```

The research question is whether this chain provides useful decision-specific
assurance beyond existing global monitoring or assumption-based approaches.

---

# Part VII — Logistics Digital Twins

## 19. Logistics Is Not an Empty Research Domain

Digital Twins are already widely investigated in:

- supply chains;
- transport;
- warehouses;
- fleet management;
- manufacturing logistics;
- route optimisation; and
- resilient operations.

AI-driven and autonomous Digital Twin systems are also increasingly studied.

Therefore DARA-DT should not claim novelty simply because it applies AI and
Digital Twins to logistics.

---

## 20. Why Logistics Remains Valuable

Logistics provides a useful experimental domain because decisions depend on
dynamic physical state.

Examples include:

```text
vehicle location
capacity
availability
operational status
traffic
inventory
order demand
```

These dependencies can become inconsistent with their Digital Twin
representation.

This makes logistics a useful testbed for studying:

```text
physical–digital divergence
        ↓
decision consequence
        ↓
runtime autonomous authority
```

The application domain is therefore experimentally meaningful even if it is
not itself novel.

---

# Part VIII — Closest-Work Comparison

## 21. Current Comparison Matrix

| Research Area | Already Established | DARA-DT Question | Novelty Threat |
|---|---|---|---|
| Digital Twin assurance | Twin quality, trustworthiness, lifecycle assurance | Can divergence regulate individual AI decisions? | High |
| Continuous DT assurance | Runtime monitoring, evidence, drift, trust | Can assurance become decision-dependency-specific? | High |
| Runtime assurance | Monitor/intervene/fallback architectures | Can physical–digital divergence drive decision-level authority? | High |
| Runtime assumption monitoring | Monitor operational assumptions | Is decision-relevant divergence distinct from monitored assumptions? | High |
| DT fidelity/divergence | State mismatch, synchronisation, fidelity | Does the mismatch matter to this decision? | High |
| AI uncertainty | Confidence and uncertainty estimates | What if AI is confident but Twin state is wrong? | High |
| Decision validation | Constraint and feasibility checking | Can divergence be mapped to decision-specific validity? | Moderate–High |
| Adaptive autonomy | Restrict/defer/fallback authority | What evidence should trigger authority change? | High |
| Logistics Digital Twins | Logistics modelling and optimisation | How should divergence affect autonomous logistics decisions? | High |
| Compound stress testing | Robustness under multiple failures | Can assurance remain selective under combined divergence? | Moderate |
| Decision-relevant divergence | Dependency-specific mismatch | Is this already captured by assumption monitoring or decision assurance? | Unresolved |

The final row currently represents the most important unresolved novelty
question.

---

# Part IX — Candidate Contribution

## 22. Current Candidate Contribution

The strongest defensible candidate contribution is:

> **A decision-specific runtime-assurance mechanism that maps
> physical–digital divergence to the dependencies and physical validity of an
> AI-generated logistics decision, and experimentally evaluates whether that
> information improves runtime intervention decisions.**

This remains a candidate contribution.

It is not yet a confirmed novelty claim.

---

## 23. More Formal Candidate

For decision \(d_t\):

\[
Dep(d_t)
\]

defines decision dependencies.

Detected divergence is:

\[
D_t
\]

Decision-relevant divergence is:

\[
D_t^{rel}(d_t)=Dep(d_t)\cap D_t
\]

A decision-impact function can then be represented conceptually as:

\[
I(d_t,D_t^{rel},E_t)
\]

where \(E_t\) represents runtime evidence.

The assurance mechanism becomes conceptually:

\[
A_t =
\pi(d_t,D_t^{rel},I,E_t)
\]

where \(A_t\) controls autonomous authority.

The research contribution would not be the mathematical notation itself.

The contribution would need to arise from:

- the operationalisation;
- experimental differentiation from relevant baselines;
- demonstrated usefulness;
- generalisation;
- and evidence that the mechanism is not already established in prior work.

---

# Part X — Novelty Kill Test

## 24. Strong Novelty Kill Condition

The novelty case would be substantially weakened if prior work is found that
already combines:

1. a Digital Twin of a physical operational system;
2. explicit physical–digital divergence detection;
3. explicit dependencies of an individual AI-generated decision;
4. runtime matching of divergence to those dependencies;
5. decision-specific consequence or validity evaluation;
6. runtime intervention based on that evaluation;
7. adaptive regulation of autonomous authority;
8. evaluation under multiple divergence conditions; and
9. controlled evaluation in dynamic logistics or a directly transferable
   operational domain.

If a mature system already performs this complete chain, DARA-DT would need
to identify a narrower contribution.

---

## 25. Partial Overlap Does Not Establish Novelty

Conversely, finding separate papers for:

```text
divergence detection
runtime assurance
decision dependencies
evidence quality
adaptive autonomy
logistics Digital Twins
```

does not automatically mean their integration is novel.

Research novelty cannot be established simply by combining known components.

The integration must solve a meaningful unresolved problem and demonstrate
new knowledge.

---

# Part XI — Experimental Evidence Required

## 26. What EXP-001 to EXP-006 Establish

The current experiments provide evidence about the mechanism.

They show, within controlled conditions, that:

```text
divergence count
        ↓
can be misleading

decision relevance
        ↓
improves discrimination in early controlled scenarios

relevance alone
        ↓
can over-intervene

decision impact
        ↓
adds physical-validity information

imperfect evidence
        ↓
can undermine impact reasoning
```

These findings strengthen the research problem.

They do not establish novelty.

---

## 27. Why EXP-007 Is Important to the Novelty Case

The strongest later experiments remain concentrated on vehicle capacity.

This creates a serious alternative explanation:

> DARA-DT may currently be a sophisticated capacity-validity mechanism rather
> than a general divergence-aware assurance framework.

EXP-007 should therefore test:

```text
Capacity
Operational Status
Location / Availability
```

under a common decision-relevance and impact framework.

If the mechanism generalises, the research case becomes stronger.

If it does not, the result establishes an important boundary condition.

---

# Part XII — Current Research Position

## 28. What Can Be Said

The repository can currently state that DARA-DT:

- investigates decision-specific physical–digital divergence;
- explicitly models decision dependencies;
- distinguishes global from decision-relevant divergence;
- distinguishes relevance from physical decision impact;
- evaluates assurance behaviour against independent physical ground truth;
- investigates imperfect runtime evidence;
- compares multiple assurance strategies; and
- progressively tests the limitations of its own assumptions.

---

## 29. What Should Not Yet Be Said

The repository should not currently state that DARA-DT:

- is the first divergence-aware Digital Twin assurance framework;
- is the first runtime-assurance framework for Digital Twins;
- uniquely links physical and digital systems;
- solves Digital Twin trustworthiness;
- is safer than existing runtime-assurance systems;
- generally outperforms existing approaches;
- has been validated for autonomous logistics generally;
- provides formal safety guarantees; or
- has confirmed research novelty.

---

# Part XIII — Research-Gap Statement

## 30. Current Working Gap

A cautious working research gap is:

> **Current Digital Twin assurance and runtime-assurance research provides
> increasingly sophisticated mechanisms for monitoring model performance,
> data quality, operational envelopes, assumptions and trustworthiness at
> runtime. However, an unresolved question for this project is how
> physical–digital divergence should be interpreted relative to the
> dependencies and physical validity of a specific AI-generated operational
> decision, and whether this decision-specific information can improve the
> regulation of autonomous authority in dynamic logistics systems.**

This is a research question under investigation.

It should not be converted into a definitive literature-gap claim until the
literature review is sufficiently systematic.

---

# Part XIV — Literature Search Priorities

## 31. Highest-Priority Search Areas

The literature review should now prioritise combinations of:

```text
"digital twin" AND "runtime assurance"

"digital twin" AND "runtime monitoring" AND decision

"digital twin" AND "decision assurance"

"digital twin" AND "decision validity"

"digital twin" AND "physical digital divergence"

"digital twin" AND "model discrepancy" AND autonomous

"runtime assumption monitoring" AND autonomous systems

"decision dependency" AND runtime assurance

"decision-specific assurance"

"adaptive autonomy" AND digital twin

"digital twin" AND "operational design domain"

"digital twin" AND logistics AND assurance
```

The objective is to attack the candidate contribution rather than merely
collect supportive literature.

---

## 32. Search Decision Rule

For every close paper or project, record:

```text
What problem does it solve?
What does it monitor?
At what level does it reason?
Does it model individual decision dependencies?
Does it compare physical and Twin state?
Does it evaluate decision consequence?
Does it change runtime authority?
What evidence does it use?
What domain is evaluated?
What remains unresolved?
```

This structure should feed directly into:

```text
literature_matrix.md
novelty_evidence_matrix.md
```

---

# Part XV — Current Verdict

## 33. Novelty Status

Current status:

```text
Runtime assurance                    HIGH prior-work overlap
Digital Twin assurance               HIGH prior-work overlap
Physical–digital divergence          HIGH prior-work overlap
Adaptive autonomous authority        HIGH prior-work overlap
Logistics Digital Twins              HIGH prior-work overlap
Decision impact / validity            MODERATE–HIGH overlap
Evidence reliability                 HIGH prior-work overlap
Decision-relevant divergence         UNRESOLVED
Integrated decision-specific chain   UNRESOLVED
```

Therefore:

> **DARA-DT should continue as a research hypothesis, but its novelty case
> must remain under active challenge.**

---

## 34. Conclusion

The closest prior work shows that DARA-DT sits within an active and
competitive research area.

Runtime assurance, continuous Digital Twin assurance, model fidelity,
runtime evidence, assumption monitoring and adaptive autonomy already have
substantial prior work.

The defensible research direction is therefore narrower.

DARA-DT investigates whether physical–digital divergence can be evaluated
relative to the dependencies and physical validity of the specific
AI-generated decision about to execute, and whether that information provides
useful evidence for regulating autonomous authority.

The current experimental programme provides evidence that this question is
worth investigating.

It does not yet establish that the resulting mechanism is novel.

The next requirements are:

```text
1. continue aggressive closest-prior-work search
2. test cross-dependency generalisation
3. compare against stronger assurance baselines
4. identify conditions where DARA-DT fails
5. refine the contribution only after those tests
```

That evidence-first approach provides a stronger foundation for a PhD
proposal than prematurely claiming novelty.
