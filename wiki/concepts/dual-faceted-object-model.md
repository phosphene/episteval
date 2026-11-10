---
uri: episteval/wiki/concepts/dual-faceted-object-model
title: The Dual-Faceted Object Model: Ergonomic Numeric Projection and Formal Provenance
author: Phosphene Platform Team
status: living
updated: 2026-11-10
license: MIT
---

# The Dual-Faceted Object Model

A central design requirement in `episteval` is bridging the gap between two competing computational paradigms:
1. **Continuous Numerical Optimization:** Machine learning pipelines, loss functions, ranking models, and statistical suites require lightweight scalar metrics $\in [0.0, 1.0]$.
2. **Discrete Scientific Provenance:** Peer review, safety audits, and automated epistemics require full access to the underlying derivation hypergraph, premise dependency chain, and boundary constraints.

`episteval` resolves this dilemma through a unified, polymorphic data structure: **`EpistemicState`**.

---

## 1. The Dual Computational Axes

`EpistemicState` operates simultaneously along two complementary axes:

```
                        ┌───────────────────────────────────────┐
                        │            EpistemicState             │
                        └───────────────────┬───────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
  ┌───────────────────────────────────┐           ┌───────────────────────────────────┐
  │      Scalar Projection Axis       │           │    Structural Provenance Axis     │
  │  Implements Python Numeric Model  │           │  Preserves Inferential Hypergraph │
  ├───────────────────────────────────┤           ├───────────────────────────────────┤
  │ - float(state) -> [0.0, 1.0]      │           │ - state.derivation_graph          │
  │ - bool(state)  -> is_warranted    │           │ - state.premises (dependency chain│
  │ - Operator dunders: <, <=, >, >=  │           │ - state.boundary_conditions       │
  │ - Arithmetic: +, -, *, /          │           │ - state.defeaters & sensitivities │
  │ - Direct numpy/scipy sort & filter│           │ - state.derivation_ast (Formal AST│
  └───────────────────────────────────┘           └───────────────────────────────────┘
```

---

## 2. The Scalar Projection Axis

To enable seamless integration with scientific Python tools (e.g. `numpy`, `scipy`, `scikit-learn`, `PyTorch`), `EpistemicState` implements the Python numeric data model:

```python
# Direct float evaluation
score = float(state)  # 0.88

# Boolean warrant gate
if state:
    deploy_model()

# Direct comparison against numerical thresholds
if state >= 0.80:
    archive_warranted_finding()

# Native list sorting by warrant score
ranked_hypotheses = sorted(candidate_states, reverse=True)
```

By overloading comparison dunders (`__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__`) and arithmetic dunders (`__add__`, `__sub__`, `__mul__`, `__truediv__`), downstream code treats `EpistemicState` as a continuous score without unpacking or discarding object identity.

---

## 3. The Structural Provenance Axis

While the scalar projection supplies continuous values, the structural axis guarantees complete scientific provenance:

```python
graph = state.derivation_graph

# Inspectable inferential topology
print(graph["regime"])              # e.g. "bayesian", "deductive", "defeasible"
print(graph["tier"])                # "T1", "T2", "T3"
print(graph["premises"])            # Full premise dependency chain
print(graph["sources"])             # Grounding primary sources and recensions
print(graph["boundary_conditions"]) # Domain scope and falsifiability limits
print(graph["defeaters"])           # Tracked defeaters and sensitivity conditions
print(graph["ast"])                 # Abstract syntax tree of gate evaluation
```

The derivation AST preserves:
- Individual gate evaluations across $L_1$ to $L_4$.
- Specific blocker tokens raised during arbitration.
- Underlying prior and likelihood ratios when evaluating Bayesian claims.

---

## 4. Architectural Invariants

1. **Axiomatic Immutability:** `EpistemicState` is frozen (`frozen=True`) with forbidden extra attributes (`extra="forbid"`), preventing runtime state corruption or attribute drift.
2. **Equivalence Consistency:** Comparison with floating-point values uses standard relative and absolute tolerances ($10^{-9}$), ensuring stable numerical comparisons in machine learning loops.
3. **Information Losslessness:** The transformation from `EvaluationVerdict` to `EpistemicState` is strictly monotonic; no gate result, diagnostic string, or premise dependency is discarded.
