# Experiment 009 — Decision-Relevant vs Decision-Irrelevant Evidence Uncertainty

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-009  
**Status:** Pre-Registered — Not Yet Executed  
**Research Stage:** Decision-conditioned evidence uncertainty and autonomy preservation

---

## 1. Motivation

EXP-008 evaluated runtime assurance when evidence associated with the pending
AI decision was reliable, stale, missing, or conflicting.

The strongest evidence-quality-aware policies were:

- Uncertainty-Aware Runtime Contract;
- DARA-DT Evidence-Aware Assurance.

Across the 24 EXP-008 conditions, both policies produced identical binary
assurance outcomes:

- 12 true interventions;
- 9 false interventions;
- 0 missed interventions;
- 3 correct non-interventions;
- 100% intervention recall;
- 12.5% autonomy availability.

The result demonstrated that conservative handling of uncertain evidence can
prevent unsafe autonomous execution.

However, it also demonstrated a substantial autonomy cost.

EXP-008 did not isolate an important part of the DARA-DT hypothesis:

> Whether evidence uncertainty should affect autonomous authority when the
> uncertain evidence is unrelated to the dependencies of the specific
> AI-generated decision being evaluated.

EXP-009 is designed specifically to test this question.

---

## 2. Primary Research Question

> **Can decision-conditioned runtime assurance distinguish
> decision-relevant evidence uncertainty from decision-irrelevant evidence
> uncertainty and thereby preserve autonomous authority without increasing
> missed unsafe interventions?**

---

## 3. Secondary Research Questions

EXP-009 investigates:

1. whether generic evidence-quality monitoring over-intervenes when uncertainty
   exists outside the dependencies of the pending decision;

2. whether decision-conditioned assurance can ignore irrelevant uncertainty
   while remaining conservative about relevant uncertainty;

3. whether this behaviour generalises across capacity, operational status, and
   location / availability dependencies;

4. whether improved autonomy can be achieved without increasing missed
   interventions;

5. whether the additional dependency information used by DARA-DT provides
   measurable assurance value beyond a simpler uncertainty-aware mechanism.

---

## 4. Central Hypothesis

The experiment tests the following hypothesis:

> Evidence uncertainty should influence autonomous authority only when the
> uncertain evidence affects a dependency required by the specific
> AI-generated decision.

For a decision \(d_t\), let:

\[
Dep(d_t)
\]

represent the state dependencies required by the decision.

Let:

\[
U_t
\]

represent runtime evidence whose quality is uncertain.

Decision-relevant uncertain evidence is:

\[
U_t^{rel}(d_t) = U_t \cap Dep(d_t)
\]

Decision-irrelevant uncertain evidence is:

\[
U_t^{irr}(d_t) = U_t \setminus Dep(d_t)
\]

The experimental question is whether distinguishing these sets improves the
runtime assurance trade-off.

---

## 5. Core Experimental Principle

EXP-009 separates:

\[
Physical\ Ground\ Truth
\]

from:

\[
Digital\ Twin\ State
\]

from:

\[
Runtime\ Evidence
\]

and additionally separates runtime evidence into:

\[
Decision\text{-}Relevant\ Evidence
\]

and:

\[
Decision\text{-}Irrelevant\ Evidence
\]

Physical ground truth remains evaluator-only information.

No runtime policy may use physical ground truth to determine its authority
decision.

---

## 6. Illustrative Example

Consider an AI decision:

> Assign Vehicle 2 to Order 7.

Suppose this decision depends on:

- Vehicle 2 capacity;
- Vehicle 2 operational status;
- Vehicle 2 availability;
- Vehicle 2 dispatch location;
- Order 7 demand and state.

Now suppose evidence about Vehicle 8 becomes stale.

The system contains uncertain evidence, but the uncertain evidence does not
affect a dependency of the Vehicle 2 assignment.

A global evidence-quality mechanism may react to the uncertainty simply because
uncertain evidence exists.

A decision-conditioned mechanism should be capable of determining that the
Vehicle 8 evidence is irrelevant to the Vehicle 2 decision.

EXP-009 tests this distinction directly.

---

## 7. Dependency Families

The experiment retains the three dependency families used in EXP-007 and
EXP-008.

### 7.1 Capacity

The selected vehicle must have sufficient capacity for the assigned order.

### 7.2 Operational Status

The selected vehicle must remain operational.

### 7.3 Location / Availability

The selected vehicle must remain available and within the permitted dispatch
location.

This preserves continuity with the preceding experiments.

---

## 8. Evidence Quality Conditions

EXP-009 focuses on the imperfect-evidence states already established by
EXP-008:

- stale;
- missing;
- conflicting.

Reliable evidence is retained as a control condition where necessary.

The critical new experimental variable is not merely evidence quality.

It is:

\[
Evidence\ Relevance
\]

with two principal states:

- decision-relevant;
- decision-irrelevant.

---

## 9. Experimental Factors

The controlled experiment varies four factors.

### Factor A — Dependency Family

- Capacity
- Operational Status
- Location / Availability

### Factor B — Evidence Quality

- Reliable
- Stale
- Missing
- Conflicting

### Factor C — Evidence Relevance

- Relevant to the pending decision
- Irrelevant to the pending decision

### Factor D — Physical Decision Validity

- Physically valid
- Physically invalid

The experiment will use a balanced controlled subset sufficient to isolate the
effect of evidence relevance without unnecessarily expanding the experimental
matrix.

The final condition matrix must be frozen before implementation.

---

## 10. Required Paired Conditions

The design must contain paired conditions where evidence quality is held
constant and only decision relevance changes.

For example:

### Pair A — Irrelevant Stale Evidence

Physical decision:

\[
VALID
\]

Evidence:

\[
STALE
\]

Evidence relevance:

\[
IRRELEVANT
\]

Expected research question:

> Should unrelated stale evidence remove autonomous authority from an otherwise
> valid decision?

---

### Pair B — Relevant Stale Evidence

Physical decision:

\[
VALID
\]

Evidence:

\[
STALE
\]

Evidence relevance:

\[
RELEVANT
\]

Expected research question:

> Should stale evidence concerning a required decision dependency cause
> conservative authority reduction?

---

### Pair C — Irrelevant Missing Evidence

Physical decision:

\[
VALID
\]

Evidence:

\[
MISSING
\]

Evidence relevance:

\[
IRRELEVANT
\]

---

### Pair D — Relevant Missing Evidence

Physical decision:

\[
VALID
\]

Evidence:

\[
MISSING
\]

Evidence relevance:

\[
RELEVANT
\]

---

### Pair E — Irrelevant Conflicting Evidence

Physical decision:

\[
VALID
\]

Evidence:

\[
CONFLICTING
\]

Evidence relevance:

\[
IRRELEVANT
\]

---

### Pair F — Relevant Conflicting Evidence

Physical decision:

\[
VALID
\]

Evidence:

\[
CONFLICTING
\]

Evidence relevance:

\[
RELEVANT
\]

These pairs directly test whether relevance changes runtime authority while
holding evidence quality constant.

---

## 11. Unsafe-Decision Controls

Autonomy preservation alone is insufficient evidence of improved assurance.

EXP-009 must therefore include physically invalid decisions.

These conditions test whether a policy that ignores irrelevant uncertainty
still intervenes when the actual decision becomes unsafe.

The experiment must contain cases where:

\[
Physical\ Decision = INVALID
\]

and decision-relevant evidence indicates or fails to resolve the unsafe state.

This prevents an apparently high-autonomy policy from appearing successful
simply because it allows more decisions.

---

## 12. Comparator Policies

EXP-009 must compare at least four policies.

### P0 — No Assurance

Always permits autonomous execution.

Purpose:

- maximum-autonomy reference;
- unsafe baseline.

---

### P1 — Global Evidence-Uncertainty Policy

Reduces autonomous authority whenever uncertain runtime evidence exists,
regardless of whether that evidence affects the current decision.

Purpose:

- tests the cost of treating all system uncertainty as decision relevant.

This comparator must receive the same runtime evidence as DARA-DT.

---

### P2 — Uncertainty-Aware Runtime Contract

Evaluates decision requirements and explicitly handles evidence quality.

The policy must be given only the information justified by its defined
interface.

It must not be artificially weakened to favour DARA-DT.

Purpose:

- strongest simpler comparator;
- continuation of EXP-008 Kill Test E.

---

### P3 — DARA-DT Decision-Conditioned Assurance

Evaluates uncertain evidence relative to the dependencies of the specific
AI-generated decision.

Conceptually:

\[
U_t^{rel}(d_t)=U_t\cap Dep(d_t)
\]

Decision-irrelevant uncertain evidence should not automatically remove
autonomous authority.

Decision-relevant uncertain evidence may trigger:

- restriction;
- deferral;
- fallback;

depending on the evidence and decision-validity mechanism.

---

## 13. Fairness Constraint

All runtime policies must receive equivalent observable runtime information.

No policy may receive:

- physical ground truth;
- evaluator labels;
- future state;
- hidden scenario identifiers;
- information derived from the expected experimental outcome.

Differences between policies must arise from their assurance logic rather than
unequal access to evidence.

---

## 14. Independent Ground Truth

Physical decision validity remains determined independently.

For every condition:

\[
GroundTruth(d_t,P_t)
\]

determines whether intervention was actually required.

Runtime policies must not call this evaluator during authority selection.

Ground truth is used only after the policy decision to classify the outcome.

---

## 15. Primary Outcome Categories

Each assurance decision is classified as:

- True Intervention (TI)
- False Intervention (FI)
- Missed Intervention (MI)
- Correct Non-Intervention (CNI)

These remain consistent with EXP-005 through EXP-008.

---

## 16. Primary Metrics

The experiment will report:

### Safety Metrics

- True Interventions
- Missed Interventions
- Intervention Recall
- Missed-Intervention Rate

### Over-Intervention Metrics

- False Interventions
- False-Intervention Rate
- Precision

### Autonomy Metrics

- Autonomy Availability
- ALLOW frequency
- RESTRICT frequency
- DEFER frequency
- FALLBACK frequency

### Overall Metric

- Accuracy

---

## 17. Key Comparative Metric

The central comparison is not accuracy alone.

EXP-009 tests the trade-off:

\[
Safety
\leftrightarrow
Autonomy\ Availability
\]

A policy that obtains zero missed interventions by deferring every uncertain
case does not necessarily provide useful decision-conditioned assurance.

The experiment therefore asks whether DARA-DT can preserve additional autonomy
specifically in decision-irrelevant uncertainty conditions without increasing
missed unsafe interventions.

---

## 18. Expected Diagnostic Pattern

The following pattern would be consistent with the decision-conditioning
hypothesis.

For a physically valid decision with irrelevant uncertain evidence:

\[
DARA\text{-}DT \rightarrow ALLOW
\]

while a global uncertainty mechanism may produce:

\[
GlobalUncertainty \rightarrow DEFER
\]

For a physically valid decision with relevant uncertain evidence:

\[
DARA\text{-}DT \rightarrow DEFER
\]

may remain appropriate.

For a physically invalid decision:

\[
DARA\text{-}DT \rightarrow INTERVENTION
\]

should remain required when the available runtime information justifies that
authority reduction.

These are diagnostic expectations, not experimental results.

---

## 19. Falsification Criteria

EXP-009 is explicitly falsification-oriented.

### Kill Test A — No Autonomy Advantage

If DARA-DT and the strongest uncertainty-aware comparator have equivalent
autonomy availability while maintaining equivalent safety, the claim that
decision conditioning improves autonomy preservation is not supported.

---

### Kill Test B — Safety Degradation

If DARA-DT preserves additional autonomy but increases missed interventions,
the additional autonomy cannot be interpreted as an assurance improvement.

---

### Kill Test C — Runtime Contract Equivalence

If an ordinary uncertainty-aware runtime contract can ignore irrelevant
evidence and achieve the same safety/autonomy trade-off using less mechanism
complexity, the stronger DARA-DT contribution claim is weakened.

---

### Kill Test D — Capacity-Only Effect

If the proposed benefit occurs only for capacity and does not reproduce for
status or location / availability, the framework-level generalisation claim
must be narrowed.

---

### Kill Test E — Evidence Privilege

If DARA-DT requires evidence unavailable to the comparator in order to achieve
better results, the comparison is not valid.

The experiment must therefore ensure evidence parity.

---

### Kill Test F — Trivial Entity Filtering

If the apparent benefit of DARA-DT can be reproduced simply by filtering
runtime evidence by selected entity identifier without requiring meaningful
decision-dependency reasoning, the contribution must be described as a simpler
filtering mechanism rather than a general decision-conditioned assurance
framework.

This kill test is particularly important.

---

## 20. Critical Novelty Test

EXP-009 is not intended merely to show that irrelevant data can be ignored.

The stronger question is:

> Does dependency-aware conditioning provide useful assurance information that
> cannot be reduced to trivial entity filtering or an ordinary
> uncertainty-aware runtime contract?

This distinction is necessary for evaluating the candidate DARA-DT
contribution.

---

## 21. Required Ablation

The experiment should include or enable comparison between:

\[
Global\ Uncertainty
\]

\[
Entity\text{-}Filtered\ Uncertainty
\]

\[
Decision\text{-}Dependency\text{-}Conditioned\ Uncertainty
\]

This ablation is important because:

\[
SelectedEntity \neq CompleteDecisionDependency
\]

A logistics decision may depend on multiple entities and variables.

For example:

> Assign Vehicle 2 to Order 7

depends not only on Vehicle 2 identity but potentially on:

- vehicle capacity;
- vehicle status;
- vehicle availability;
- vehicle location;
- order demand;
- order state;
- operational constraints.

Therefore a meaningful decision-conditioned mechanism should reason about
dependencies rather than merely the selected vehicle identifier.

---

## 22. Success Criterion

EXP-009 would provide evidence supporting the usefulness of decision
conditioning only if DARA-DT demonstrates a better safety–autonomy trade-off
under the controlled matrix.

A particularly informative pattern would be:

1. zero or no additional missed interventions relative to the strongest
   comparator;

2. fewer false interventions under decision-irrelevant uncertainty;

3. greater autonomy availability;

4. preservation of conservative behaviour when uncertainty affects a required
   decision dependency;

5. replication across more than one dependency family.

Even if these conditions occur, the result would constitute controlled
experimental evidence rather than proof of general superiority.

---

## 23. Negative Result Interpretation

A negative result is scientifically acceptable.

If the uncertainty-aware contract or entity-filtered baseline matches DARA-DT,
the project should report that result directly.

Possible resulting conclusions could include:

- decision conditioning provides no measurable advantage in the tested matrix;
- simple entity filtering explains the apparent benefit;
- ordinary runtime contracts are sufficient for the tested logistics
  decisions;
- DARA-DT requires a narrower contribution claim;
- additional complexity is not justified by the observed assurance benefit.

The experiment must not be modified retrospectively to force a favourable
DARA-DT result.

---

## 24. Relationship to Previous Experiments

The experimental progression is:

### EXP-004

Established that decision relevance alone is insufficient.

### EXP-005

Introduced decision-specific impact and physical-validity boundaries.

### EXP-006

Introduced imperfect runtime evidence.

### EXP-007

Generalised impact reasoning across capacity, status, and
location / availability, while exposing equivalence with a simpler runtime
contract under reliable evidence.

### EXP-008

Compared assurance under stale, missing, and conflicting evidence.

DARA-DT and the uncertainty-aware runtime contract achieved identical binary
performance:

\[
TI=12,\ FI=9,\ MI=0,\ CNI=3
\]

with:

\[
Autonomy=0.125
\]

### EXP-009

Tests whether decision conditioning can reduce unnecessary intervention when
uncertain evidence exists outside the dependencies of the pending AI decision.

---

## 25. Contribution Decision After EXP-009

After EXP-009, the candidate contribution must be reassessed.

Possible outcomes include:

### Outcome A — Decision Conditioning Adds Value

If DARA-DT preserves autonomy without reducing safety and survives the entity
filter and runtime-contract baselines, the experimental evidence for
decision-conditioned runtime assurance becomes stronger.

### Outcome B — Simple Filtering Is Sufficient

If entity filtering reproduces the result, the contribution must be narrowed.

### Outcome C — Runtime Contracts Are Sufficient

If an uncertainty-aware contract matches DARA-DT, superiority claims must be
rejected.

### Outcome D — Safety–Autonomy Trade-Off Remains Unresolved

If autonomy improvements introduce missed interventions, additional mechanism
development may be required before making a contribution claim.

---

## 26. Implementation Freeze Rule

Before implementation begins, the following must be frozen:

- condition matrix;
- dependency families;
- evidence-quality states;
- relevance labels;
- physical-validity labels;
- comparator definitions;
- ground-truth mechanism;
- metrics;
- falsification criteria.

Once experimental execution begins, these elements must not be changed in
response to observed results.

Any additional hypothesis arising after execution must be tested in a separate
experiment.

---

## 27. Current Status

EXP-009 is currently:

**PRE-REGISTERED — NOT EXECUTED**

No experimental results are claimed in this document.

No performance advantage is assumed.

The experiment exists specifically to test whether the candidate
decision-conditioning contribution survives stronger comparison and
falsification.

---

## 28. Pre-Registered Research Question

The final pre-registered question is:

> **Can decision-conditioned runtime assurance distinguish
> decision-relevant from decision-irrelevant evidence uncertainty in dynamic
> logistics Digital Twins, preserving autonomous authority without increasing
> missed unsafe interventions relative to simpler uncertainty-aware assurance
> mechanisms?**

This question will remain fixed for EXP-009.
