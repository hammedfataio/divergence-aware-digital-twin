# Experiment 004 — Divergence Severity and Decision Validity

**Project:** DARA-DT — Divergence-Aware Runtime Assurance for Digital Twins  
**Experiment:** EXP-004  
**Status:** Completed — Controlled Proof-of-Concept  
**Research Stage:** Decision-Relevant Divergence → Decision Impact  
**Domain:** Autonomous Logistics Digital Twin

---

## 1. Purpose

Previous DARA-DT experiments established that the amount of physical–digital
divergence alone is insufficient for determining whether an autonomous
AI-generated decision should be interrupted.

A Digital Twin may contain substantial divergence that is unrelated to the
decision currently being executed. Conversely, a comparatively small
divergence may affect a variable on which the decision directly depends.

This motivated decision-relevance analysis.

EXP-004 investigates the next question:

> Is decision relevance alone sufficient to determine whether autonomous
> execution should be permitted?

The experiment evaluates progressively increasing divergence in a
decision-relevant vehicle-capacity variable and observes when that divergence
actually changes the physical validity of the AI-generated decision.

---

## 2. Research Question

> How does the severity of physical–digital divergence interact with
> decision relevance in determining whether an autonomous logistics
> decision remains physically valid?

The experiment specifically examines whether:

1. all decision-relevant divergence requires intervention;
2. divergence magnitude alone is sufficient for intervention;
3. a decision-validity boundary can be observed; and
4. decision relevance must be combined with decision impact in the
   runtime-assurance process.

---

## 3. Experimental Hypothesis

The experiment tests the following hypothesis:

> Decision relevance is necessary for targeted runtime assurance, but
> relevance alone is insufficient to determine whether an autonomous
> action should be restricted.

A divergence may affect a variable used by a decision while remaining too
small to invalidate that decision.

The critical issue is therefore not only whether divergence is relevant, but
whether it materially changes the validity of the proposed action.

---

## 4. Controlled Scenario

A single vehicle and a single order are used to isolate the effect of
capacity divergence.

The Digital Twin initially represents:

| Variable | Twin State |
|---|---:|
| Vehicle capacity | 10 |
| Order demand | 5 |
| Vehicle status | Operational |
| Vehicle availability | Available |

The AI controller generates its assignment using the Digital Twin.

After synchronization, the physical vehicle capacity is modified while the
Digital Twin retains the synchronized capacity of 10.

This creates controlled physical–digital divergence.

All other relevant variables are held constant.

---

## 5. Severity Conditions

Seven controlled conditions are evaluated.

| Condition | Twin Capacity | Physical Capacity | Order Demand | Divergence Magnitude | Physical Decision Validity |
|---|---:|---:|---:|---:|---|
| S0 | 10 | 10 | 5 | 0 | Valid |
| S1 | 10 | 9 | 5 | 1 | Valid |
| S2 | 10 | 7 | 5 | 3 | Valid |
| S3 | 10 | 6 | 5 | 4 | Valid |
| S4 | 10 | 5 | 5 | 5 | Valid |
| S5 | 10 | 4 | 5 | 6 | Invalid |
| S6 | 10 | 2 | 5 | 8 | Invalid |

The critical transition occurs between **S4** and **S5**.

At S4:

```text
physical capacity = order demand
5 = 5
