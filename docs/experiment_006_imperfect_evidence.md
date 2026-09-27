# Experiment 006 — Decision-Impact Assurance Under Imperfect Runtime Evidence

**Project:** Divergence-Aware Runtime Assurance for Digital Twins (DARA-DT)  
**Experiment:** EXP-006  
**Status:** Experimental Design  
**Research Stage:** Robustness of Decision-Impact Reasoning

---

## 1. Motivation

EXP-005 demonstrated that decision-impact-aware assurance can distinguish
between divergences that merely affect a decision dependency and divergences
that materially invalidate the proposed decision.

However, EXP-005 relied on a strong assumption:

> The runtime evidence used to estimate decision impact accurately represented
> the physical system state.

Real Digital Twin systems cannot always make this assumption.

Runtime observations may be:

- noisy;
- delayed;
- stale;
- missing;
- incomplete; or
- uncertain.

An assurance mechanism that works only when physical state is observed
perfectly would have limited value in real autonomous systems.

EXP-006 therefore deliberately weakens the runtime-evidence assumption.

---

## 2. Research Question

> How robust is decision-impact-aware runtime assurance when the evidence used
> to estimate physical–digital divergence and decision impact is imperfect?

---

## 3. Experimental Hypothesis

The working hypothesis is:

> Explicit representation of runtime-evidence quality will allow the assurance
> mechanism to distinguish confident decision-impact estimates from uncertain
> ones and regulate autonomous authority accordingly.

This hypothesis is provisional and must be tested experimentally.

---

## 4. Core Experimental Principle

EXP-006 separates three quantities that must not be conflated:

### Physical Ground Truth

The actual state of the simulated logistics system.

This information is available to the experimental evaluator.

### Digital Twin State

The state representation used by the autonomous decision controller.

This state may differ from physical reality.

### Runtime Evidence

The observation available to the assurance mechanism.

Runtime evidence may itself be inaccurate, delayed, missing, or uncertain.

Therefore:

**Physical Ground Truth ≠ Runtime Evidence ≠ Digital Twin State**

This separation is central to EXP-006.

---

## 5. Why This Matters

Consider a vehicle with:

- Twin capacity = `10`
- Physical capacity = `6`
- Order demand = `8`

The proposed assignment is physically invalid.

In EXP-005, the assurance mechanism could receive runtime evidence indicating
capacity `6` and correctly identify the decision as invalidating.

EXP-006 asks what happens if the runtime evidence instead reports:

- `6` — accurate evidence;
- `7` — noisy but still decision-invalidating;
- `8` — apparent boundary;
- `9` — incorrectly appears valid;
- no value — missing evidence; or
- an old value of `10` — stale evidence.

The physical ground truth remains unchanged.

Only the evidence available to the assurance mechanism changes.

---

## 6. Evidence Conditions

EXP-006 will introduce controlled evidence-quality conditions.

### E0 — Accurate Evidence

Runtime evidence matches physical ground truth.

Purpose:

Establish the EXP-005 reference condition.

### E1 — Small Observation Error

Runtime evidence differs slightly from physical state but does not change the
estimated validity classification.

Purpose:

Test tolerance to minor measurement error.

### E2 — Boundary-Shifting Error

Runtime evidence moves the estimated state onto the decision boundary.

Purpose:

Test behaviour when evidence uncertainty changes the apparent safety margin.

### E3 — Validity-Flipping Error

Runtime evidence incorrectly makes an invalid physical decision appear valid,
or a valid decision appear invalid.

Purpose:

Test whether evidence error can reverse the assurance decision.

### E4 — Delayed Evidence

The assurance mechanism receives a previously correct observation that no
longer represents the current physical state.

Purpose:

Test sensitivity to observation age.

### E5 — Missing Evidence

The required runtime observation is unavailable.

Purpose:

Test explicit uncertainty handling.

### E6 — Conflicting Evidence

Two runtime observations provide inconsistent information about the same
decision dependency.

Purpose:

Test whether conflicting evidence can be represented without silently choosing
one observation.

---

## 7. Evidence Model

Runtime evidence should be extended beyond a simple observed value.

A conceptual evidence representation is:

```text
Evidence
├── dependency
├── observed_value
├── source
├── timestamp
├── age
├── confidence
└── availability
