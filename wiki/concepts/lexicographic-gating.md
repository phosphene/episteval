---
uri: episteval/wiki/concepts/lexicographic-gating
title: Lexicographic Gating and Non-Compensatory Epistemic Evaluation
author: Phosphene Platform Team
status: living
updated: 2026-11-10
license: MIT
---

# Lexicographic Gating and Non-Compensatory Evaluation

In traditional automated evaluation frameworks (e.g. typical benchmark metrics or naive weighted sums), scores are compensatory: a catastrophic failure in primary grounding or logical consistency can be masked by an artificially high score in surface presentation or fluency.

`episteval` prohibits compensatory error masking through **non-compensatory lexicographic gating**.

---

## 1. The Four Invariant Epistemic Levels

Epistemic warrant is evaluated across four invariant, hierarchically ordered levels:

```
  ┌─────────────────────────────────────────────────────────────┐
  │ Level 1: Observation Grounding (L1)                         │
  │ Primary artifacts, empirical datasets, and source recensions│
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Pass / Provisional
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ Level 2: Formalization & Schema (L2)                        │
  │ Explicitly typed premises, predicates, and ontologies       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Pass / Provisional
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ Level 3: Inferential Machinery (L3)                         │
  │ Entailment validity, Bayesian priors, or defeasible warrant │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ Pass / Provisional
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ Level 4: Boundary Falsifiability (L4)                       │
  │ Operational limits, counterfactual scope, and null models   │
  └─────────────────────────────────────────────────────────────┘
```

1. **$L_1$ Observation Grounding:** Does the claim anchor directly in inspectable empirical data or primary sources?
2. **$L_2$ Formalization & Schema:** Are premises, concepts, and relationships explicitly typed rather than expressed as ambiguous rhetoric?
3. **$L_3$ Inferential Machinery:** Does the deduction hold under its declared inference regime (monotonic deductive, defeasible non-monotonic, Bayesian credence)?
4. **$L_4$ Boundary Conditions:** Are operational domain constraints, falsifiability limits, and null models explicitly defined?

---

## 2. Non-Compensatory Mechanics

Under lexicographic ordering:
- A failure (`FAIL`) at $L_1$ or $L_2$ terminates the warrant derivation. No amount of elaborate mathematical deduction ($L_3$) or speculative boundary tuning ($L_4$) can compensate for absent empirical grounding or invalid formalization.
- The overall certified warrant tier is bounded by the minimum level passed:

$$\text{Tier}(\mathcal{C}) = f\left(\min_{i} \text{Status}(L_i)\right)$$

### Warrant Tiers
- **$T_1$ (High Warrant):** Certified passing all four levels ($L_1$ through $L_4$) with composite score $\ge 80.0$. Robust under counterfactual perturbation and severe scrutiny.
- **$T_2$ (Provisional Warrant):** Passes core grounding and formalization with provisional status ($55.0 \le \text{Score} < 80.0$). Valid within explicitly stated caveats.
- **$T_3$ (Defeated / Ungrounded Warrant):** Fails one or more foundational levels ($\text{Score} < 55.0$). Unwarranted for scientific adoption.

---

## 3. Mathematical Realization in `EpistemicMatrix`

The arbitration matrix evaluates a candidate claim $\mathcal{C}$ by dispatching an array of deterministic gates:

$$\mathcal{S} = \sum_{k} w_k \cdot s_k(\mathcal{C})$$

Subject to the hard constraint:

$$\text{is\_warranted} = \text{True} \iff \forall g \in \mathcal{G}_{\text{core}}, \, \text{Status}(g) \neq \text{FAIL}$$

If any core gate reports `FAIL`, the composite score is clamped, certified tier is forced to $T_3$, and diagnostics report the exact blocking conditions.

---

## References

- Sen, A. K. (1970). *Collective Choice and Social Welfare*. San Francisco: Holden-Day.
- Fishburn, P. C. (1974). "Lexicographic orders, utilities and decision rules: A survey". *Management Science*, 20(11), 1442–1471.
- Braithwaite, R. B. (1953). *Scientific Explanation*. Cambridge University Press.
