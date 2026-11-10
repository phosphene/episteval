---
uri: phosphene.tooling/episteval
owner: edphos
status: active
license: MIT
updated: 2026-11-10
---

# `episteval` — Epistemic Evaluation across Modality, Monotonicity, and Credence

[![CI](https://github.com/phosphene/episteval/actions/workflows/ci.yml/badge.svg)](https://github.com/phosphene/episteval/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/episteval.svg)](https://pypi.org/project/episteval/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)

`episteval` operationalizes formal epistemology, hypothetico-deductive verification, and epistemic warrant auditing into automated evaluation harnesses. The engine evaluates candidate assertions, scientific propositions, and synthetic agent reasoning traces through a **demonstrable warrant trail** across formal inference regimes.

---

## 1. Architectural Foundations: The Dual-Faceted Object Model

A central challenge in automated epistemic evaluation is reconciling two complementary computational needs:
1. **Ergonomic Consumption:** Downstream pipelines (ranking algorithms, loss functions, optimizer loops, scikit-learn suites, PyTorch tensors) require calibrated continuous scalar scores between $0.0$ and $1.0$.
2. **Formal Provenance:** Scientific audits, peer review, and safety gates require an inspectable derivation hypergraph, premise dependency chain, and axiomatic regime envelope.

`episteval` resolves this tension through a polymorphic, dual-faceted object model: **`EpistemicState`**.

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

### The Scalar Projection Axis
`EpistemicState` implements Python's numeric data model (`__float__`, `__bool__`, comparison, and arithmetic dunders). Downstream code treats the evaluation directly as a calibrated metric between $0.0$ and $1.0$, enabling straightforward thresholding, sorting, argmax selections, or integration into numerical scoring suites.

### The Structural Provenance Axis
Simultaneously, `EpistemicState` preserves the underlying justification topology. It exposes defeating conditions, premise sensitivities, modal operators, and the formal derivation AST, retaining the complete axiomatic system that generated the score.

---

## 2. Invariant Epistemic Matrix

`episteval` evaluates claims across four invariant levels and three evaluative dimensions:

| Epistemic Level | Evaluative Focus | Verification Invariant |
|---|---|---|
| **$L_1$ Observation Grounding** | Primary Artifacts & Data | Grounding density; inspectable source citations and empirical logs |
| **$L_2$ Formalization & Schema** | Structured Premises & Typing | Explicit typed premises, predicates, and formal relational schemas |
| **$L_3$ Inferential Machinery** | Derivation Apparatus | Deductive validity, Bayesian updating, or defeasible warrant |
| **$L_4$ Boundary Conditions** | Scope & Falsifiability | Explicit domain boundaries, counterfactual resilience, and null models |

### Multi-Regime Pluralism
- **Deductive Monotonicity:** Verifies strict entailment ($P \vdash Q$) and flags contradictory defeaters (following Braithwaite's hypothetico-deductive canon).
- **Defeasible Warrant:** Tracks premise vulnerability and non-monotonic defeat ($P \sim Q$).
- **Subjective Bayesian Credence:** Calibrates degrees of belief ($P(H \mid E)$) against explicit priors and likelihood ratios.
- **Modal Accessibility:** Tests whether an inferential claim survives counterfactual perturbations across accessible domains.

---

## 3. Installation

Install via `pip`:

```bash
pip install episteval
```

Or with development tooling:

```bash
pip install "episteval[dev]"
```

---

## 4. Usage

### Python API

```python
from episteval import Claim, EpistemicMatrix, InferenceRegime

# Define a candidate proposition
claim = Claim(
    claim_id="prop-keplerian-orbit",
    statement="Radial velocity measurements match Keplerian orbital parameters.",
    regime=InferenceRegime.BAYESIAN,
    prior_credence=0.5,
    sources=["doi:10.1086/123456", "arxiv:2301.00001"],
    premises=[
        "Gravitational potential governs stellar radial velocity curve.",
        "Observed Doppler shift exhibits periodic sinusoidal perturbation."
    ],
    boundary_conditions=[
        "Single-star binary systems; excludes unresolved stellar clusters."
    ]
)

# Arbitrate through the invariant epistemic matrix
matrix = EpistemicMatrix()
verdict = matrix.evaluate(claim)
state = verdict.to_epistemic_state(claim)

# 1. Scalar Projection Axis: Direct numeric consumption
print(f"Scalar warrant: {float(state):.2f}")       # 0.88
print(f"Passes quality threshold: {state >= 0.8}")   # True
if state:
    print("Claim is certified warranted.")

# 2. Structural Provenance Axis: Inspectable derivation graph
graph = state.derivation_graph
print(f"Tier: {graph['tier']}")                   # T1
print(f"Premises: {len(graph['premises'])}")
print(f"AST Root: {graph['ast']}")
```

### Command-Line Interface

Inspect and evaluate claims directly from JSON files:

```bash
episteval check claim.json --profile synthetic
```

---

## 5. Epistemic Knowledge Base (Wiki)

`episteval` maintains a canonical public reference wiki documenting the theoretical and historical foundations of automated scientific explanation and inference:
- [Methodological Foundations: Braithwaite's Hypothetico-Deductive Apparatus](wiki/foundations/braithwaite-hypothetico-deductive.md)
- [Testability, Generalization, and Non-Instantial Hypotheses: Wisdom's Canon](wiki/foundations/wisdom-testability-framework.md)
- [The Epistemic Matrix: Lexicographic Gating and Warrant Levels](wiki/concepts/lexicographic-gating.md)

---

## 6. License

MIT
