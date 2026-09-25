# Experiment 001 — Decision-Relevance B-vs-C Pilot

**Project:** Divergence-Aware Runtime Assurance for AI-Driven Digital Twins  
**Experiment:** EXP-001  
**Status:** Preliminary controlled pilot completed  
**Execution:** Automated through GitHub Actions

---

## 1. Objective

This pilot evaluates whether decision relevance provides useful information
beyond the mere presence of physical–digital divergence.

The experiment compares three assurance strategies:

1. **No Assurance (B0)** — autonomous execution is allowed without checking
   Digital Twin divergence.

2. **Global Divergence (B1)** — intervention occurs whenever any divergence
   is detected.

3. **DARA-DT** — intervention depends on whether detected divergence affects
   state variables required by the current decision.

This experiment is a controlled proof-of-concept and is not intended to
establish general effectiveness.

---

## 2. Experimental Conditions

### Condition B — Decision-Irrelevant Divergence

The Digital Twin contains two physical–digital mismatches affecting vehicles
that are not used by the current logistics decision.

The selected vehicle remains physically valid.

Therefore, the independent physical-state evaluator determines that
intervention is not required.

**Observed divergence count:** 2

---

### Condition C — Decision-Relevant Divergence

The selected vehicle experiences a physical breakdown after Digital Twin
synchronisation.

The Digital Twin remains stale and continues to represent the vehicle as
available and operational.

The controller therefore selects a vehicle that is no longer physically
capable of executing the decision.

The independent physical-state evaluator determines that intervention is
required.

**Observed divergence count:** 2

---

## 3. Observed Results

| Condition | No Assurance | Global Divergence | DARA-DT |
|---|---|---|---|
| B — decision-irrelevant divergence | Correct non-intervention | False intervention | Correct non-intervention |
| C — decision-relevant divergence | Missed intervention | True intervention | True intervention |

---

## 4. Interpretation

In Condition B, the global-divergence strategy intervened even though the
detected mismatches were unrelated to the current decision.

DARA-DT identified that the divergence did not affect the state dependencies
of the selected decision and therefore allowed execution.

In Condition C, the physical state of the selected vehicle changed while the
Digital Twin remained stale.

The no-assurance strategy allowed the invalid decision to proceed.

Both the global-divergence strategy and DARA-DT intervened.

Within these controlled cases, the result demonstrates that decision
relevance can distinguish between divergence that affects a current decision
and divergence that does not.

---

## 5. Important Experimental Detail

Both pilot conditions currently contain two detected divergences.

The present experiment therefore isolates **decision relevance while holding
the divergence count equal**.

Although the internal scenario labels retain the original
`HIGH_DIVERGENCE_LOW_RELEVANCE` and `LOW_DIVERGENCE_HIGH_RELEVANCE`
terminology, this pilot should not be interpreted as a quantitative
high-versus-low divergence comparison.

A later experiment will vary divergence magnitude, count, and severity
independently.

---

## 6. What This Pilot Supports

The pilot provides preliminary executable evidence that:

- physical–digital divergence can be detected at runtime;
- divergence can be mapped to the dependencies of a specific decision;
- physically invalid decisions can be labelled independently of the
  assurance mechanism;
- global divergence monitoring can generate unnecessary intervention when
  divergence is unrelated to the current decision;
- decision-relevant divergence can avoid that intervention in the controlled
  Condition B example;
- decision-relevant divergence can still trigger intervention when stale
  Digital Twin state invalidates the selected decision in Condition C.

---

## 7. What This Pilot Does Not Establish

This experiment does not establish:

- general superiority of DARA-DT;
- statistical significance;
- robustness across logistics environments;
- performance under multiple divergence severity levels;
- effectiveness under distribution shift;
- effectiveness under compound divergence;
- performance with learned AI controllers;
- real-world operational effectiveness.

These claims require subsequent experiments.

---

## 8. Reproducibility

The pilot is executed automatically using:

```text
uv run python -m dara_dt.experiments.run_pilot
