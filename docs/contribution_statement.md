# DARA-DT — Evidence-Supported Research Contribution

**Project:** Divergence-Aware Runtime Assurance for Digital Twins  
**Research Area:** Trustworthy Intelligent Systems  
**Experimental Domain:** Autonomous Logistics Digital Twins  
**Experimental Programme:** EXP-001 to EXP-010  
**Status:** CONTRIBUTION FROZEN AFTER EXP-010

---

# 1. Purpose

This document defines the evidence-supported research contribution of DARA-DT
after completion of the ten-experiment programme.

It provides the canonical contribution statement for:

- the repository README;
- research documentation;
- PhD proposals;
- supervisor communication;
- academic CV descriptions;
- research demonstrations; and
- future publications.

The contribution defined here is intentionally bounded by the experimental
evidence.

---

# 2. Research Problem

AI-driven Digital Twins can make or support autonomous operational decisions
using representations of physical systems.

However, the physical system can change faster than its Digital Twin is
updated.

This creates physical–digital divergence:

\[
\delta_t = P_t - T_t
\]

where:

- \(P_t\) represents the physical system state; and
- \(T_t\) represents the Digital Twin state.

The existence of divergence creates an assurance problem.

An AI decision may be logically correct relative to the Digital Twin while
being inappropriate relative to physical reality.

---

# 3. Example

Consider an autonomous logistics system.

The physical system contains:

```text
Vehicle A
status = failed
```

while the Digital Twin contains:

```text
Vehicle A
status = operational
```

An AI controller using only the Twin may assign an urgent delivery to
Vehicle A.

The AI decision may be internally consistent with its input.

The problem is that the input no longer accurately represents physical
reality.

The runtime-assurance question is therefore not simply:

```text
Is the AI confident?
```

or:

```text
Does divergence exist?
```

It is:

> **Does the physical–digital divergence affect the validity of the autonomous
> decision that is about to execute?**

---

# 4. Central Research Question

The project investigates:

> **How can physical–digital divergence be quantified at runtime and used to
> regulate autonomous AI decision-making in dynamic logistics Digital Twins?**

---

# 5. Research Reasoning Chain

The completed experiments support the following reasoning structure:

```text
Physical System
        ↓
Digital Twin
        ↓
Physical–Digital Divergence
        ↓
Decision Dependencies
        ↓
Decision Relevance
        ↓
Decision Impact / Validity
        ↓
Runtime Evidence Reliability
        ↓
Cross-Decision Dependencies
        ↓
Runtime Assurance
        ↓
Autonomous Authority
```

The framework additionally represents:

```text
Divergence Origin
        ↓
Affected Dependency
        ↓
Propagation Path
        ↓
Affected Decision
```

---

# 6. Experimental Programme

The contribution is supported by ten controlled experiments:

```text
EXP-001
B-vs-C Pilot
        ↓
EXP-002
Controlled Policy Comparison
        ↓
EXP-003
Decision Relevance
        ↓
EXP-004
Divergence Severity
        ↓
EXP-005
Decision Impact
        ↓
EXP-006
Imperfect Evidence
        ↓
EXP-007
Cross-Dependency Generalisation
        ↓
EXP-008
Imperfect-Evidence Contract Comparison
        ↓
EXP-009
Decision-Relevant Evidence Uncertainty
        ↓
EXP-010
Divergence Propagation
```

The programme progressively strengthened the competing assurance mechanisms
rather than comparing DARA-DT only with weak baselines.

---

# 7. Finding 1 — Divergence Alone Is Insufficient

EXP-001 and EXP-002 demonstrated that physical–digital divergence may exist
without affecting the pending autonomous decision.

Therefore:

```text
Divergence Exists
≠
Intervention Required
```

Global divergence monitoring can therefore be unnecessarily conservative.

---

# 8. Finding 2 — Decision Relevance Matters

EXP-001–EXP-003 demonstrated that divergence should be interpreted relative to
the dependencies of the pending decision.

Formally:

\[
D_t^{rel}(d_t)
=
Dep(d_t) \cap D_t
\]

This distinguishes:

```text
all detected divergence
```

from:

```text
divergence affecting the current decision
```

---

# 9. Finding 3 — Relevance Is Not Validity

EXP-004 demonstrated:

\[
Decision\ Relevance
\neq
Decision\ Invalidity
\]

A variable may be relevant to a decision while the magnitude or consequence
of its divergence remains insufficient to invalidate that decision.

This requires reasoning beyond simple dependency intersection.

---

# 10. Finding 4 — Decision Impact Matters

EXP-005 introduced decision-impact reasoning.

Instead of asking only:

```text
Does the decision depend on this variable?
```

the assurance mechanism asks:

```text
Does the observed divergence make
the pending decision invalid?
```

Within the controlled EXP-005 matrix, decision-impact reasoning improved
selectivity while maintaining full recall.

---

# 11. Finding 5 — Truth, Twin and Evidence Must Be Separated

EXP-006 established an important methodological distinction:

```text
Physical Ground Truth
        ≠
Digital Twin State
        ≠
Runtime Evidence
```

Physical ground truth describes what is actually true.

Digital Twin state describes what the computational representation currently
believes.

Runtime evidence describes what the assurance mechanism can observe at the
time of decision.

Conflating these layers can produce unrealistic assurance evaluations.

---

# 12. Finding 6 — Evidence Reliability Matters

Runtime evidence may be:

```text
AVAILABLE

STALE

MISSING

CONFLICTING
```

EXP-006–EXP-009 demonstrated that evidence quality changes assurance
behaviour.

The framework therefore treats evidence reliability as a first-class
assurance concern.

---

# 13. Finding 7 — Global Uncertainty Can Be Too Conservative

EXP-008 and EXP-009 demonstrated that reacting globally to imperfect evidence
can substantially restrict autonomous authority.

Decision-conditioned reasoning provides a more selective alternative by
considering whether uncertain evidence is actually associated with the
pending decision.

---

# 14. Finding 8 — Local Contracts Can Be Insufficient

EXP-010 introduced a multi-stage decision chain.

The local runtime contract produced:

```text
True Interventions
=
8

False Interventions
=
3

Missed Interventions
=
11

Correct Non-Interventions
=
8

Accuracy
=
0.533

Recall
=
0.421

Missed-Intervention Rate
=
0.579
```

This demonstrates that immediate local checks can miss invalidation caused by
cross-decision, cross-entity or shared-resource dependencies.

---

# 15. Finding 9 — Cross-Dependency Reasoning Matters

The strong composed runtime contract in EXP-010 represented:

```text
direct dependencies

cross-decision dependencies

cross-entity dependencies

shared-resource dependencies

upstream assumptions
```

It achieved:

```text
Accuracy
=
0.900

Recall
=
1.000

Missed-Intervention Rate
=
0.000
```

This supports the importance of dependency-aware assurance in the tested
multi-stage logistics scenarios.

---

# 16. Finding 10 — Divergence Can Propagate

EXP-010 contained:

```text
24 divergent conditions

12 propagating conditions

12 non-propagating divergent conditions

6 compound propagation conditions
```

The framework successfully represented the distinction between:

```text
upstream divergence that affects
the downstream decision
```

and:

```text
upstream divergence that does not affect
the downstream decision
```

Therefore physical–digital divergence can be modelled as a decision-dependent
propagation phenomenon within the experimental framework.

---

# 17. Strongest Falsification Result

The strongest proposed DARA-DT differentiation was tested in EXP-010.

The comparison was:

```text
P3
Dependency-Aware Composed Runtime Contract

vs

P4
Propagation-Aware DARA-DT
```

Both mechanisms received equivalent observable evidence and access to the
pre-registered decision dependencies.

The results were:

| Metric | P3 | P4 |
|---|---:|---:|
| True Interventions | 19 | 19 |
| False Interventions | 3 | 3 |
| Missed Interventions | 0 | 0 |
| Correct Non-Interventions | 8 | 8 |
| Accuracy | 0.900 | 0.900 |
| Precision | 0.864 | 0.864 |
| Recall | 1.000 | 1.000 |
| False-Intervention Rate | 0.273 | 0.273 |
| Missed-Intervention Rate | 0.000 | 0.000 |
| Autonomy Availability | 0.267 | 0.267 |

Additionally:

```text
Authority Matches
=
30 / 30

Outcome Matches
=
30 / 30
```

---

# 18. Meaning of the EXP-010 Result

EXP-010 does not demonstrate that DARA-DT is superior to a strong
dependency-aware composed runtime contract.

Instead, it demonstrates that:

> **Once the strong runtime contract receives equivalent observable evidence
> and dependency knowledge, explicit divergence-propagation provenance does
> not provide additional binary intervention or authority-selection
> performance in the tested multi-stage decision structures.**

This is a central result of the project.

---

# 19. Hypothesis Outcome

The final EXP-010 hypotheses are recorded as:

```text
H1
Local-Contract Limitation
=
SUPPORTED WITHIN THE FROZEN MATRIX
```

```text
H2
Strong DARA-DT Differentiation
=
NOT SUPPORTED
```

```text
H0
Runtime-Contract Equivalence
=
NOT REJECTED
```

H0 is not claimed to be universally proven.

The result is bounded to the evaluated experimental structures.

---

# 20. Evidence-Supported Contribution

The canonical contribution statement is:

> **DARA-DT provides a controlled experimental framework for investigating how
> physical–digital divergence, decision dependencies, decision validity,
> runtime evidence quality and multi-stage propagation interact in runtime
> assurance for AI-driven logistics Digital Twins. Across the evaluated
> experiments, decision-sensitive dependency reasoning improves assurance
> relative to coarse global monitoring and limited local checking. However,
> when a strong dependency-aware composed runtime contract receives equivalent
> observable evidence and dependency knowledge, explicit
> divergence-propagation provenance does not provide additional binary
> intervention or authority-selection performance in the tested multi-stage
> decision structures.**

This is the canonical research contribution unless new evidence justifies its
revision.

---

# 21. Methodological Contribution

A second defensible contribution is methodological.

The experimental framework explicitly separates:

```text
Physical Ground Truth

Digital Twin State

Runtime Evidence

AI Decision

Decision Dependencies

Detected Divergence

Decision Impact

Propagation

Assurance Decision

Authority State

Evaluation Outcome
```

This separation supports controlled evaluation without providing runtime
policies with privileged access to evaluator-only ground truth.

---

# 22. Comparative Contribution

The project also demonstrates the importance of progressively stronger
comparators.

The sequence evolved from:

```text
No Assurance
        ↓
Global Divergence
        ↓
Decision Relevance
        ↓
Decision Impact
        ↓
Runtime Contract
        ↓
Uncertainty-Aware Contract
        ↓
Dependency-Aware Composed Contract
```

This progression prevented an apparent advantage over weak baselines from
being treated as sufficient evidence of a unique assurance mechanism.

---

# 23. Falsification-Oriented Contribution

The project explicitly retained negative and equivalence results.

The experimental programme therefore demonstrates a research process based on:

```text
Hypothesis
        ↓
Controlled Experiment
        ↓
Strong Comparator
        ↓
Kill Test
        ↓
Result
        ↓
Claim Revision
```

rather than:

```text
Preferred Claim
        ↓
Experiment Designed to Confirm Claim
```

This is an important part of the research methodology.

---

# 24. What Is Not Claimed

DARA-DT does not currently claim:

```text
universal superiority over runtime contracts

superior binary intervention accuracy over P3

superior authority selection over P3

unique ability to model decision dependencies

unique ability to model divergence propagation

operational safety certification

real-world logistics validation

universal runtime-contract equivalence

proven diagnostic superiority

proven explanation superiority

proven auditability superiority
```

These claims exceed the current evidence.

---

# 25. Remaining Research Opportunity

The completed experiments leave a narrower unresolved question:

> **What measurable assurance value, if any, does explicit physical–digital
> divergence provenance provide once a strong dependency-aware runtime
> contract already represents the decision-relevant operational constraints?**

Potential dimensions include:

```text
root-cause localisation

diagnostic accuracy

explanation quality

recovery reasoning

auditability

operator understanding

assurance-case evidence
```

These dimensions were not established by EXP-001–EXP-010.

---

# 26. Why Provenance May Still Matter

Two assurance mechanisms can reach the same authority decision:

```text
DEFER
```

while providing different reasoning information.

A contract may report:

```text
Recovery resource requirement not satisfied.
```

A provenance-aware mechanism may report:

```text
Vehicle A physically failed after the upstream assignment.

The Digital Twin still represented Vehicle A as operational.

This mismatch changed the recovery-resource requirement.

The changed requirement invalidated the pending downstream assignment.
```

Both may select the same authority state.

The second explanation may potentially provide greater diagnostic or
assurance value.

That potential value requires separate evaluation.

---

# 27. Research Identity

The project should be positioned under the broader research identity:

> **Trustworthy Intelligent Systems**

with particular interests in:

```text
Artificial Intelligence

Digital Twins

Runtime Assurance

Autonomous Decision-Making

Uncertainty and Reliability

Decision Dependencies

Reinforcement Learning
```

Autonomous logistics is the current experimental domain.

It should not define the entire research identity.

---

# 28. Supervisor-Facing Position

The project demonstrates capability to:

- formulate a research problem;
- review competing approaches;
- build an experimental system;
- formalise decision dependencies;
- implement runtime assurance mechanisms;
- construct controlled benchmarks;
- define falsification criteria;
- compare increasingly strong baselines;
- preserve negative results;
- interpret evidence conservatively; and
- identify the next research question.

The project should therefore be presented as:

> **a research foundation and evidence-generating prototype**

rather than:

> **a completed proof of a universally superior assurance algorithm.**

---

# 29. PhD Proposal Position

A PhD proposal can build from the completed work by asking:

> **When and how does explicit physical–digital divergence provenance provide
> measurable assurance value beyond dependency-aware runtime constraint
> satisfaction in autonomous Digital Twin systems operating under uncertainty?**

Potential future investigation can examine:

```text
explanation

diagnosis

recovery

human oversight

assurance evidence

dynamic uncertainty

large-scale operational environments
```

without rewriting the completed EXP-001–EXP-010 evidence.

---

# 30. Demonstrator Position

The research demonstrator should expose:

```text
Physical State
        ↓
Digital Twin State
        ↓
Divergence
        ↓
AI Decision
        ↓
Decision Dependencies
        ↓
Runtime Evidence
        ↓
Decision Validity
        ↓
Propagation
        ↓
Assurance Policy
        ↓
Authority
        ↓
Outcome
```

It should support side-by-side inspection of strong comparator and DARA-DT
behaviour.

Where the mechanisms agree, that agreement should remain visible.

---

# 31. Final Contribution Boundary

The project supports:

```text
Decision-sensitive divergence reasoning
=
SUPPORTED
```

```text
Decision-impact / validity reasoning
=
SUPPORTED
```

```text
Truth–Twin–Evidence separation
=
SUPPORTED
```

```text
Evidence-aware assurance
=
SUPPORTED
```

```text
Cross-dependency reasoning
=
SUPPORTED WITHIN THE CONTROLLED MATRIX
```

```text
Divergence propagation representation
=
SUPPORTED
```

```text
DARA-DT superiority over strong composed contracts
=
NOT SUPPORTED
```

```text
Additional provenance-based diagnostic value
=
NOT YET EVALUATED
```

```text
Universal runtime-contract equivalence
=
NOT CLAIMED
```

---

# 32. Canonical Short Contribution

For short descriptions:

> **DARA-DT is a reproducible research framework for investigating how
> physical–digital divergence affects autonomous AI decisions through decision
> dependencies, validity, runtime evidence and multi-stage propagation in
> logistics Digital Twins.**

---

# 33. Canonical Extended Contribution

For research proposals and academic documentation:

> **DARA-DT investigates runtime assurance for autonomous AI systems whose
> decisions depend on Digital Twin representations that may diverge from
> physical reality. Through ten controlled experiments, the framework
> separates physical ground truth, Twin state, runtime evidence, decision
> dependencies, decision validity and autonomous authority. The results show
> that decision-sensitive and cross-dependency reasoning improve assurance
> relative to coarse global monitoring and limited local checking. However,
> the strongest experiment also demonstrates that an equal-evidence,
> dependency-aware composed runtime contract can reproduce DARA-DT's binary
> intervention and authority-selection behaviour in the tested multi-stage
> scenarios, narrowing the remaining research question toward the measurable
> explanatory, diagnostic, recovery and assurance-evidence value of explicit
> divergence provenance.**

---

# 34. Final Status

```text
Experimental Programme
=
10 / 10 COMPLETE

Results Consolidation
=
COMPLETE

Novelty Evidence Audit
=
COMPLETE

Closest Prior Work Audit
=
COMPLETE

Evidence-Supported Contribution
=
FROZEN
```

The next project stage is:

```text
Supervisor-Facing README
        ↓
Research Demonstrator / API
        ↓
Deployment
        ↓
PhD Proposal
        ↓
Supervisor Outreach
```

No future project artifact should claim stronger experimental evidence than
the contribution defined in this document unless new research provides that
evidence.
