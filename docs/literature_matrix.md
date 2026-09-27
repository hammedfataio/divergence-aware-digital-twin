# DARA-DT Literature Evidence Matrix

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Framework:** DARA-DT  
**Research Identity:** Trustworthy Intelligent Systems  
**Application Domain:** Autonomous Logistics Systems  
**Document Status:** Living Literature Review  
**Literature Position:** September 2026

---

## 1. Purpose

This document maps the literature surrounding DARA-DT to:

- the central research question;
- supporting research questions;
- implemented experiments;
- competing approaches;
- novelty threats;
- unresolved research questions; and
- future experimental requirements.

This is not intended to be a generic bibliography.

The purpose is to determine whether the developing DARA-DT contribution
survives comparison with existing research.

The central research question is:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

---

## 2. Evidence Discipline

Literature is classified according to what it establishes for the project.

Each source should answer some combination of:

```text
What problem does the work address?

What does it monitor?

Does it compare physical and digital state?

Does it reason about an individual decision?

Does it represent decision dependencies?

Does it evaluate decision consequence or validity?

Does it regulate runtime authority?

What evidence does it use?

What domain does it evaluate?

What remains unresolved?
```

The matrix must distinguish:

```text
Prior work exists
```

from:

```text
Prior work solves the DARA-DT research question
```

These are not equivalent.

---

# Part I — Research Themes

## 3. Theme A — Digital Twin Assurance

### Representative Work

**DNV-RP-A204 — Assurance of Digital Twins**

DNV provides a systematic recommended practice for developing and assuring
Digital Twins.

Relevant concerns include:

- Digital Twin quality;
- trustworthiness;
- organisational maturity;
- risks associated with relying on Twin information;
- integration and deployment;
- operation;
- maintenance; and
- lifecycle assurance.

### Relevance to DARA-DT

This literature establishes that Digital Twin trustworthiness and the risks
of acting on Twin information are already recognised assurance problems.

Therefore DARA-DT cannot claim:

```text
Digital Twins require assurance
```

as a novel contribution.

### DARA-DT Question

The narrower question is:

> When the Twin differs from physical reality, does the mismatch affect the
> specific AI-generated decision currently seeking execution authority?

### Novelty Threat

**HIGH**

---

## 4. Theme B — Continuous Runtime Digital Twin Assurance

### Representative Work

**DARTER — Digital Twin Assurance via Runtime Trust and Evidence Reporting**

The Alan Turing Institute's DARTER project investigates continuous assurance
for safety-critical Digital Twins.

Its work includes:

- runtime data-quality verification;
- model-performance evaluation;
- validated thresholds;
- operational-domain monitoring;
- distribution-drift detection;
- automated assurance evidence;
- continuously updated assurance cases; and
- runtime trustworthiness.

Air traffic management is the primary testbed, while the methodology is
intended to transfer to additional safety-critical sectors.

### Relevance to DARA-DT

DARTER directly challenges any claim that:

```text
Digital Twin assurance is mainly static
```

or that:

```text
DARA-DT introduces runtime Digital Twin assurance.
```

Continuous Digital Twin assurance is already an active research direction.

### Candidate Difference

DARTER primarily asks whether:

```text
the Twin, data and predictions remain trustworthy
within validated operational conditions
```

DARA-DT investigates whether:

```text
a particular physical–digital mismatch affects a dependency
of the specific AI decision about to execute
```

and subsequently whether:

```text
that mismatch changes the decision's physical validity.
```

### Novelty Threat

**VERY HIGH**

### Research Requirement

DARA-DT must demonstrate that decision-specific divergence reasoning provides
information not already captured by global Twin trust or operational-domain
monitoring.

---

## 5. Theme C — Logistics Digital Twins

### Representative Literature

Recent systematic reviews investigate Digital Twins for real-time
decision-making in:

- supply chains;
- transport;
- warehouse systems;
- fleet operations; and
- logistics optimisation.

The literature demonstrates that Digital Twins are increasingly used to
support operational decision-making.

### Relevance to DARA-DT

This establishes that:

```text
Digital Twin + Logistics
```

is not novel.

Likewise:

```text
Digital Twin + Real-Time Decision-Making
```

is already an active research area.

### Research Opportunity

The relevant DARA-DT question concerns what happens when:

```text
the Digital Twin is sufficiently wrong
about state required by an autonomous decision.
```

### Novelty Threat

**HIGH**

---

## 6. Theme D — AI-Enhanced Logistics Digital Twins

### Representative Literature

Recent reviews describe integration of:

- AI;
- Digital Twins;
- IoT;
- optimisation;
- computer vision;
- reinforcement learning;
- robotics; and
- automated logistics systems.

Warehouse Digital Twins increasingly support:

- path planning;
- task allocation;
- inventory management;
- storage assignment;
- prediction; and
- optimisation.

### Relevance to DARA-DT

This establishes that:

```text
AI + Digital Twin + Logistics
```

cannot constitute the project's novelty claim.

### Research Opportunity

DARA-DT focuses instead on:

```text
AI decision authority when the Twin's representation
of physical reality becomes unreliable.
```

### Novelty Threat

**HIGH**

---

## 7. Theme E — Autonomous and Agentic AI with Digital Twins

### Representative Literature

Recent 2026 systematic work examines autonomous and agentic AI integrated
with Digital Twins in transportation and smart logistics.

The literature identifies increasing interest in systems capable of:

- selecting actions;
- coordinating decisions;
- initiating operational actions;
- interacting with Digital Twins; and
- operating with different levels of human oversight.

Operational validation remains an important challenge.

### Relevance to DARA-DT

This literature directly overlaps with the project's broader autonomous
logistics context.

Therefore DARA-DT cannot claim that autonomous decision-making connected to
Digital Twins is itself new.

### DARA-DT Question

The narrower question becomes:

> What runtime evidence should determine whether autonomous decision authority
> should continue when the Twin diverges from physical reality?

### Novelty Threat

**VERY HIGH**

---

# Part II — Physical–Digital Consistency

## 8. Theme F — Digital Twin Fidelity

Digital Twin fidelity concerns how accurately the digital representation
reflects its physical counterpart.

Relevant concepts include:

- state accuracy;
- model accuracy;
- synchronisation;
- prediction quality;
- behavioural consistency; and
- model validity.

### Relevance

DARA-DT depends on physical–digital consistency.

However:

```text
measuring Twin fidelity
```

is not itself the contribution.

### Candidate Difference

DARA-DT asks:

```text
Does this fidelity problem matter to this particular decision?
```

rather than only:

```text
How inaccurate is the Twin?
```

### Novelty Threat

**HIGH**

---

## 9. Theme G — Synchronisation and Staleness

Digital Twins depend on synchronisation between physical and digital state.

Research already considers:

- update frequency;
- stale information;
- communication delay;
- near-real-time synchronisation;
- asynchronous updates; and
- adaptive synchronisation.

### Relevance

Temporal divergence is therefore not a novel problem.

### DARA-DT Question

The relevant question is:

> Does stale information invalidate a dependency of the current decision?

### Novelty Threat

**HIGH**

---

## 10. Theme H — Physical–Digital Divergence

Physical–digital mismatch appears in multiple forms across the Digital Twin
literature.

These include:

```text
state error
model discrepancy
synchronisation error
drift
fidelity loss
behavioural mismatch
data inconsistency
```

### Relevance

DARA-DT therefore does not claim the discovery of physical–digital
divergence.

### Candidate Difference

The project operationalises divergence as an input to decision-specific
runtime assurance.

Conceptually:

\[
D_t = \{s_i : s_i^{physical} \neq s_i^{twin}\}
\]

followed by:

\[
D_t^{rel}(d_t)=Dep(d_t)\cap D_t
\]

### Novelty Threat

**HIGH for divergence detection**

**UNRESOLVED for decision-specific divergence**

---

# Part III — Runtime Assurance

## 11. Theme I — Runtime Assurance

Runtime assurance is an established field.

Relevant mechanisms include:

- runtime monitors;
- safety filters;
- supervisory controllers;
- fallback mechanisms;
- Simplex architectures;
- operational envelopes;
- runtime verification; and
- adaptive control authority.

### Relevance

DARA-DT therefore cannot claim:

```text
runtime intervention
```

or:

```text
runtime regulation of autonomy
```

as novel by themselves.

### Candidate Difference

The project investigates whether physical–digital divergence can provide
decision-specific evidence for such intervention.

### Novelty Threat

**VERY HIGH**

---

## 12. Theme J — Runtime Assumption Monitoring

Runtime assumption monitoring is one of the closest conceptual areas.

A system may depend on assumptions such as:

```text
sensor accuracy
environmental conditions
component availability
resource capability
```

Runtime monitoring can determine whether those assumptions continue to hold.

### Relationship to DARA-DT

Consider:

```text
Decision:
assign vehicle V1 to order O1

Decision dependency:
capacity(V1) >= demand(O1)
```

DARA-DT observes:

```text
Twin capacity = 10
Physical capacity = 4
Demand = 5
```

The decision dependency has effectively become invalid.

This can resemble runtime assumption monitoring.

### Critical Research Question

> **Is decision-relevant physical–digital divergence fundamentally different
> from runtime assumption monitoring?**

This is currently one of the strongest novelty threats.

### Novelty Threat

**VERY HIGH**

---

# Part IV — Decision-Level Reasoning

## 13. Theme K — Decision Dependencies

Autonomous decisions depend on particular state variables.

DARA-DT represents this as:

\[
Dep(d_t)
\]

The research uses these dependencies to determine whether detected divergence
affects the current decision.

### Example

```text
Decision:
assign vehicle_01

Dependencies:
capacity
availability
operational status
location
```

A mismatch affecting:

```text
vehicle_09
```

may be irrelevant to this decision.

### Research Question

> Does explicit dependency matching provide useful assurance information
> beyond system-level Twin fidelity?

### Novelty Status

**UNRESOLVED**

This is one of the project's most important literature-search areas.

---

## 14. Theme L — Decision-Relevant Divergence

The DARA-DT mechanism defines:

\[
D_t^{rel}(d_t)=Dep(d_t)\cap D_t
\]

This distinguishes:

```text
The Twin is wrong
```

from:

```text
The Twin is wrong about something this decision depends on.
```

### Experimental Connection

This mechanism is investigated through:

```text
EXP-001
EXP-002
EXP-003
```

### Current Evidence

The controlled experiments demonstrate that global divergence can produce
unnecessary intervention when the mismatch is unrelated to the decision.

### Novelty Status

**UNRESOLVED / CANDIDATE**

Experimental usefulness does not establish originality.

---

## 15. Theme M — Decision Impact and Validity

EXP-004 demonstrates that relevance is insufficient.

Example:

```text
Twin capacity     = 10
Physical capacity = 9
Demand            = 5
```

The capacity mismatch is relevant but the assignment remains valid.

Therefore DARA-DT introduces:

```text
Decision Impact / Physical Validity
```

### Formal Example

\[
M=C_{physical}-q
\]

where \(M\) represents the physical validity margin.

### Experimental Connection

```text
EXP-004
EXP-005
```

### Novelty Threat

Constraint checking and decision feasibility are established concepts.

The unresolved question is whether combining them with runtime
physical–digital divergence creates a useful assurance mechanism.

### Novelty Status

**MODERATE–HIGH THREAT**

---

# Part V — AI Uncertainty

## 16. Theme N — AI Confidence and Uncertainty

AI trustworthiness literature extensively investigates:

- predictive confidence;
- uncertainty estimation;
- calibration;
- out-of-distribution detection;
- epistemic uncertainty; and
- aleatoric uncertainty.

### Relationship to DARA-DT

AI uncertainty and Twin divergence are different failure dimensions.

An AI system may be highly confident given its input while the input itself
is based on stale or incorrect Twin state.

Conceptually:

```text
AI confidence = high
```

does not guarantee:

```text
Digital Twin state = physical reality
```

### Research Opportunity

Future experiments may compare:

```text
AI uncertainty
```

with:

```text
physical–digital divergence
```

and:

```text
decision-specific impact.
```

### Novelty Threat

**HIGH**

AI uncertainty itself is not a DARA-DT contribution.

---

# Part VI — Evidence Reliability

## 17. Theme O — Runtime Evidence Quality

Assurance systems depend on operational evidence.

Relevant research areas include:

- sensor reliability;
- data quality;
- provenance;
- stale observations;
- conflicting observations;
- missing data; and
- uncertainty.

### DARA-DT Connection

EXP-006 explicitly separates:

```text
Physical Ground Truth
        ≠
Runtime Evidence
        ≠
Digital Twin State
```

### Experimental Result

The controlled experiment demonstrates that apparently usable but incorrect
evidence can produce:

```text
missed intervention
```

while pessimistic evidence can produce:

```text
false intervention.
```

### Novelty Status

**HIGH prior-work overlap**

The methodological integration remains useful but should not be presented as
the invention of evidence-quality reasoning.

---

# Part VII — Adaptive Autonomy

## 18. Theme P — Authority Regulation

Existing autonomous-system architectures already use actions conceptually
similar to:

```text
ALLOW
RESTRICT
DEFER
FALLBACK
```

Examples include:

- safety controllers;
- fallback systems;
- human escalation;
- degraded autonomy; and
- operational-envelope enforcement.

### DARA-DT Difference Under Investigation

The project asks whether authority should depend on:

```text
decision-relevant physical–digital divergence
+
decision impact
+
runtime evidence
```

rather than simply:

```text
system-level alarm
```

### Novelty Threat

**HIGH**

---

# Part VIII — Literature-to-Experiment Mapping

## 19. Experimental Evidence Matrix

| Experiment | Literature Problem Tested | Main Question | Literature Threat |
|---|---|---|---|
| EXP-001 | Global divergence vs decision significance | Can equal divergence counts have different decision relevance? | Fidelity monitoring |
| EXP-002 | Global intervention vs decision-specific intervention | Does relevance improve selectivity? | Runtime assurance |
| EXP-003 | Dependency-aware divergence | Can mismatch be mapped to decision dependencies? | Assumption monitoring |
| EXP-004 | Relevance vs physical validity | Does relevant divergence always require intervention? | Constraint validation |
| EXP-005 | Decision impact | Can consequence reasoning improve intervention decisions? | Decision assurance |
| EXP-006 | Imperfect evidence | How does evidence degradation affect impact-aware assurance? | Data/evidence quality |
| EXP-007 | Cross-dependency generalisation | Does the mechanism generalise beyond capacity? | Generality / abstraction |

---

# Part IX — Literature-to-RQ Mapping

## 20. Central Research Question

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

Relevant literature families:

```text
Digital Twin fidelity
Digital Twin assurance
Runtime assurance
Autonomous logistics
Decision assurance
Evidence reliability
Adaptive autonomy
```

---

## 21. RQ1 — Detection and Relevance

> **Which runtime signals and dependency relationships most effectively
> identify decision-relevant divergence between a logistics system and its
> Digital Twin?**

Relevant literature:

```text
Digital Twin fidelity
synchronisation
state estimation
runtime monitoring
decision dependencies
runtime assumption monitoring
```

Experimental mapping:

```text
EXP-001
EXP-002
EXP-003
```

---

## 22. RQ2 — Impact

> **How do different forms, magnitudes and combinations of physical–digital
> divergence affect the reliability of AI-generated logistics decisions?**

Relevant literature:

```text
model discrepancy
decision feasibility
constraint validation
uncertainty
robust optimisation
Digital Twin integrity
```

Experimental mapping:

```text
EXP-004
EXP-005
EXP-006
EXP-007
```

---

## 23. RQ3 — Runtime Assurance

> **Can divergence-aware runtime assurance reduce inappropriate autonomous
> actions under disruption while maintaining acceptable logistics performance
> and autonomy availability?**

Relevant literature:

```text
runtime assurance
adaptive autonomy
operational envelopes
fallback systems
assurance cases
continuous Digital Twin assurance
```

Experimental mapping:

```text
EXP-002
EXP-004
EXP-005
EXP-006
future system-level experiments
```

---

# Part X — Key Literature Matrix

## 24. Current Evidence Matrix

| Literature Stream | What Prior Work Establishes | DARA-DT Relevance | Remaining Question | Threat |
|---|---|---|---|---|
| Digital Twin assurance | Twin trustworthiness requires systematic assurance | Establishes assurance context | Can assurance become decision-specific? | High |
| DARTER / continuous assurance | Runtime data, model and domain monitoring can support continuous assurance | Very close architecture | Does decision dependency add distinct information? | Very High |
| Logistics DTs | Twins support real-time logistics decisions | Establishes application domain | What happens when Twin state is wrong? | High |
| Autonomous AI + DT | Autonomous decisions increasingly interact with Twins | Establishes autonomy context | How should authority respond to divergence? | Very High |
| DT fidelity | Physical/digital consistency matters | Basis for divergence | Does global fidelity predict decision validity? | High |
| Synchronisation | Stale state is a known DT problem | Temporal divergence | When does staleness matter to a decision? | High |
| Runtime assurance | Runtime monitors can intervene | Basis for authority control | What should trigger intervention? | Very High |
| Assumption monitoring | Operational assumptions can be monitored | Conceptually close to dependencies | Is DARA-DT more than assumption monitoring? | Very High |
| Decision feasibility | Constraints determine decision validity | Supports impact reasoning | Can divergence drive runtime validity reasoning? | Moderate–High |
| AI uncertainty | AI confidence can be estimated | Alternative trust signal | What if model confidence and Twin fidelity disagree? | High |
| Evidence quality | Runtime observations can be unreliable | Directly relevant to EXP-006 | How should evidence reliability affect authority? | High |
| Adaptive autonomy | Authority can be restricted or transferred | Supports action model | Can divergence provide better authority evidence? | High |
| Decision-relevant divergence | Decision-specific mismatch | Core candidate contribution | Already established elsewhere? | Unresolved |
| Cross-dependency assurance | Same mechanism across state dependencies | Needed for generalisation | Does DARA-DT survive beyond capacity? | Unresolved |

---

# Part XI — Most Important Novelty Threats

## 25. Threat 1 — DARTER

DARTER substantially occupies:

```text
continuous Digital Twin assurance
runtime trust
live evidence
drift detection
operational-domain monitoring
```

DARA-DT must therefore demonstrate a narrower distinction.

---

## 26. Threat 2 — Runtime Assumption Monitoring

Decision dependencies may simply represent operational assumptions.

If existing assumption-monitoring approaches already perform equivalent
decision-specific reasoning, DARA-DT's candidate contribution must be
refined.

---

## 27. Threat 3 — Decision Feasibility

Decision-impact reasoning may reduce to conventional constraint checking.

DARA-DT must demonstrate why:

```text
physical–digital divergence
+
decision dependency
+
runtime validity
```

provides additional assurance value.

---

## 28. Threat 4 — Capacity Overfitting

Current later experiments are dominated by:

```text
vehicle capacity
```

The mechanism may therefore appear more general than the evidence supports.

This is why EXP-007 is necessary.

---

# Part XII — Evidence Gaps

## 29. Gap A — Decision-Specific Divergence

The literature search must continue to investigate whether existing work
explicitly performs:

```text
physical–digital mismatch
        ↓
specific decision dependency
        ↓
decision consequence
        ↓
runtime authority
```

This remains the strongest candidate gap.

---

## 30. Gap B — Cross-Dependency Generalisation

Evidence is required across:

```text
capacity
operational status
location / availability
```

A mechanism that works only for capacity cannot support a broad framework
claim.

---

## 31. Gap C — Divergence × AI Uncertainty

Future research may investigate cases such as:

```text
Low AI uncertainty + High relevant divergence

High AI uncertainty + Low relevant divergence

High AI uncertainty + High relevant divergence
```

This could determine whether the two signals provide complementary assurance
information.

It should not distract from cross-dependency validation first.

---

## 32. Gap D — Compound Divergence

Operational systems may experience multiple simultaneous mismatches.

Later experiments should test whether the mechanism remains selective under:

```text
temporal
+
state
+
operational
```

divergence.

---

## 33. Gap E — Operational Performance

Current experiments focus primarily on assurance outcomes.

Broader research must eventually determine whether intervention improves
system behaviour without unacceptable degradation in:

- service rate;
- lateness;
- cost;
- utilisation;
- decision latency; and
- autonomy availability.

---

# Part XIII — Literature Search Strategy

## 34. Priority Search Strings

Future literature searches should prioritise:

```text
"digital twin" AND "decision dependency"

"digital twin" AND "decision-specific assurance"

"digital twin" AND "decision validity"

"digital twin" AND "runtime assurance"

"digital twin" AND "runtime monitoring" AND autonomy

"digital twin" AND "physical digital divergence"

"digital twin" AND "model discrepancy" AND decision

"runtime assumption monitoring" AND autonomous systems

"decision dependency" AND runtime assurance

"decision assurance" AND digital twin

"adaptive autonomy" AND digital twin

"digital twin" AND logistics AND assurance

"digital twin" AND logistics AND trustworthiness
```

The objective is to locate work that could invalidate the proposed research
gap.

---

## 35. Literature Inclusion Priorities

Priority should be given to:

1. peer-reviewed journal papers;
2. peer-reviewed conference papers;
3. recognised standards and recommended practices;
4. major research-institute projects;
5. systematic reviews;
6. authoritative government or standards publications.

Preprints can be useful for identifying emerging research but should be
labelled appropriately.

---

# Part XIV — Literature Evidence Rules

## 36. Rule 1 — Do Not Search Only for Support

The literature review must actively search for work that makes DARA-DT less
novel.

This reduces confirmation bias.

---

## 37. Rule 2 — Separate Similarity from Equivalence

A paper discussing:

```text
runtime monitoring
```

is not automatically equivalent to:

```text
decision-specific divergence-aware assurance.
```

Likewise, different terminology may describe essentially the same mechanism.

Both possibilities must be investigated.

---

## 38. Rule 3 — Do Not Infer Absence

Failure to find a paper does not prove:

```text
no prior work exists.
```

Therefore statements such as:

```text
"No previous research..."
```

should be avoided unless supported by a sufficiently systematic review.

---

## 39. Rule 4 — Experiments Do Not Establish Novelty

A successful experimental result establishes:

```text
behaviour within the experimental conditions
```

not:

```text
research originality.
```

Novelty requires literature comparison.

---

# Part XV — Current Literature Position

## 40. High-Confidence Conclusions

Current literature strongly supports the following:

```text
Digital Twin assurance already exists.

Continuous runtime Digital Twin assurance already exists.

Runtime assurance already exists.

Runtime assumption monitoring already exists.

AI-enabled logistics Digital Twins already exist.

Autonomous AI + Digital Twin logistics research already exists.

Physical–digital fidelity is already an established concern.

Evidence quality is already an established concern.

Adaptive authority is already an established concern.
```

Therefore none of these individually constitutes the DARA-DT contribution.

---

## 41. Unresolved Questions

The following remain under investigation:

```text
Does existing work explicitly map physical–digital divergence
to dependencies of an individual AI decision?

Does existing work quantify whether that divergence changes
the physical validity of that decision?

Does existing work use that decision-specific impact to regulate
autonomous authority?

Is this fundamentally different from runtime assumption monitoring?

Does the mechanism generalise across multiple logistics dependencies?
```

These questions should drive the next literature searches and experiments.

---

# Part XVI — Current Candidate Research Gap

## 42. Working Gap Statement

The current cautious research-gap statement is:

> **Digital Twin assurance and runtime-assurance research increasingly
> provide mechanisms for monitoring model performance, data quality,
> operational envelopes, assumptions and trustworthiness during operation.
> An unresolved question for DARA-DT is how physical–digital divergence
> should be interpreted relative to the dependencies and physical validity
> of a specific AI-generated operational decision, and whether this
> decision-specific information provides useful evidence for regulating
> autonomous authority in dynamic logistics systems.**

This statement is intentionally framed as an unresolved question.

It should not yet be converted into a definitive novelty claim.

---

# Part XVII — Connection to Experimental Programme

## 43. Literature → Experiment Chain

```text
DT fidelity literature
        ↓
EXP-001 / EXP-002
Global divergence vs decision significance
        ↓
Runtime assumption monitoring
        ↓
EXP-003
Decision dependency and relevance
        ↓
Decision feasibility literature
        ↓
EXP-004 / EXP-005
Decision impact and validity
        ↓
Evidence-quality literature
        ↓
EXP-006
Imperfect runtime evidence
        ↓
Generality challenge
        ↓
EXP-007
Cross-dependency validation
```

The literature and experiments should therefore evolve together.

---

# Part XVIII — Current Research Position

## 44. Candidate Contribution

The current candidate contribution remains:

> **A decision-specific runtime-assurance mechanism that maps
> physical–digital divergence to the dependencies and physical validity of
> an AI-generated logistics decision, and experimentally evaluates whether
> that information improves runtime intervention decisions.**

Status:

```text
CANDIDATE
NOT CONFIRMED NOVELTY
```

---

## 45. Immediate Literature Priority

Before making a strong novelty claim, the highest-priority literature task is
to attack the intersection:

```text
Digital Twin
        +
Physical–Digital Divergence
        +
Decision Dependencies
        +
Runtime Decision Validity
        +
Autonomous Authority
```

If prior work already implements this chain, the contribution must be
refined.

If systematic searching continues to show only partial implementations, the
case for the research gap becomes stronger.

---

## 46. Conclusion

The literature does not support a broad claim that DARA-DT introduces:

```text
Digital Twin assurance
runtime assurance
autonomous logistics
physical–digital divergence
evidence monitoring
adaptive autonomy
```

These areas are already established.

The potentially differentiating question is narrower:

> **When a Digital Twin diverges from physical reality, can that divergence
> be mapped to the dependencies and physical validity of the specific
> AI-generated decision about to execute, and can this information improve
> runtime regulation of autonomous authority?**

The current experimental programme provides a structured way to investigate
that question.

The novelty case remains deliberately open until stronger literature and
cross-dependency evidence are available.
