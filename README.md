# episteval

[![CI](https://github.com/phosphene/episteval/actions/workflows/ci.yml/badge.svg)](https://github.com/phosphene/episteval/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/episteval.svg)](https://pypi.org/project/episteval/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Epistemic evaluation across modality, monotonicity, and credence.**

`episteval` operationalizes formal epistemology and epistemic warrant auditing into modern automated evaluation harnesses. Rather than evaluating whether a claim matches a static string or ground-truth label, `episteval` arbitrates whether an agent, model, or research claim possesses a **demonstrable warrant trail** across formal inference regimes.

---

## Key Features

1. **Shift from Accuracy to Warranted Assertibility:**
   * Audits justification trails across formal and defeasible inference regimes.
   * Lexicographic gating prevents cosmetic eloquence from masking ungrounded assertions.

2. **Pluralism Across Inference Regimes:**
   * **Deductive Monotonicity:** Verifies strict entailment ($P \vdash Q$) and flags contradictory defeaters.
   * **Defeasible Warrant:** Tracks premise vulnerability and non-monotonic defeat ($P \sim Q$).
   * **Subjective Bayesian Credence:** Calibrates degrees of belief ($P(H \mid E)$) against explicit priors.
   * **Modal Accessibility:** Tests whether an inferential claim survives counterfactual perturbations across accessible domains.

3. **The Invariant INFERNO Evaluation Matrix:**
   * **$L_1$ Observation Grounding:** Anchors claims in inspectable primary artifacts and recensions.
   * **$L_2$ Formalization & Schema:** Requires explicit, typed premises and structured relations.
   * **$L_3$ Inferential Machinery:** Evaluates the derivation apparatus under the claimed regime.
   * **$L_4$ Boundary Conditions:** Enforces explicit scope boundaries and empirical failure criteria.

4. **Pluggable Domain Profiles:**
   * Includes calibrated profiles for **Comparative Historical & Evolutionary Sciences** (elevating primary recension depth, spatial controls, and strict null models) and **Synthetic Reasoning** (evaluating agentic LLM planning traces).

---

## Installation

```bash
pip install episteval
```

Or with development tooling:

```bash
pip install "episteval[dev]"
```

---

## Quickstart

### 1. Python API

```python
from episteval import Claim, InfernoMatrix, InferenceRegime

# Define a candidate proposition
claim = Claim(
    claim_id="prop-spatial-ibd",
    statement="Spatial Isolation-by-Distance explains folklore trait dissimilarity.",
    regime=InferenceRegime.BAYESIAN,
    prior_credence=0.5,
    sources=["urn:cts:phosphene:swanton.1909", "urn:cts:phosphene:boas.1916"],
    premises=[
        "Geographic distance impedes continuous oral diffusion.",
        "Observed pairwise dissimilarity scales monotonically with distance."
    ],
    boundary_conditions=[
        "Terrestrial continental zones; excludes maritime trade archipelagos."
    ]
)

# Arbitrate through the invariant INFERNO matrix
matrix = InfernoMatrix()
verdict = matrix.evaluate(claim)

print(f"Tier: {verdict.tier.value}")            # T1
print(f"Composite Score: {verdict.composite_score}/100")
print(f"Warranted: {verdict.is_warranted}")      # True
```

### 2. Command-Line Interface

Inspect and evaluate claim JSON files directly:

```bash
episteval check claim.json --profile comparative
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
