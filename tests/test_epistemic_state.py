"""tests for EpistemicState dual-faceted numeric data model and structural provenance."""

import pytest
from episteval.core.models import Claim, EpistemicState, EpistemicTier, InferenceRegime
from episteval.core.matrix import EpistemicMatrix


def test_epistemic_state_numeric_projection():
    state = EpistemicState(
        claim_id="claim-101",
        warrant_score=0.88,
        tier=EpistemicTier.T1,
        regime=InferenceRegime.BAYESIAN,
        is_warranted=True,
        summary="High epistemic warrant",
        premises=["Premise A", "Premise B"],
        sources=["source:1"],
        boundary_conditions=["Condition C"],
        derivation_ast={"root": "BAYES_UPDATE", "likelihood": 4.5},
    )

    # Float casting
    assert float(state) == 0.88

    # Bool truthiness
    assert bool(state) is True
    if not state:
        pytest.fail("State should evaluate to truthy when warranted")

    # Int casting
    assert int(state) == 0

    # Comparison dunders with floats
    assert state == 0.88
    assert state > 0.80
    assert state >= 0.88
    assert state < 0.95
    assert state <= 0.88

    # Arithmetic dunders
    assert round(state + 0.1, 2) == 0.98
    assert round(0.1 + state, 2) == 0.98
    assert round(state - 0.08, 2) == 0.80
    assert round(1.0 - state, 2) == 0.12
    assert round(state * 2, 2) == 1.76
    assert round(2 * state, 2) == 1.76
    assert round(state / 2, 2) == 0.44


def test_epistemic_state_sorting_and_filtering():
    s1 = EpistemicState(claim_id="low", warrant_score=0.40, tier=EpistemicTier.T3, regime=InferenceRegime.DEFEASIBLE, is_warranted=False, summary="Low")
    s2 = EpistemicState(claim_id="mid", warrant_score=0.72, tier=EpistemicTier.T2, regime=InferenceRegime.DEFEASIBLE, is_warranted=True, summary="Mid")
    s3 = EpistemicState(claim_id="high", warrant_score=0.91, tier=EpistemicTier.T1, regime=InferenceRegime.BAYESIAN, is_warranted=True, summary="High")

    # Native Python sorting using < operator
    ranked = sorted([s2, s1, s3])
    assert [s.claim_id for s in ranked] == ["low", "mid", "high"]

    # Filter by threshold directly against numeric literal
    passing = [s for s in [s1, s2, s3] if s >= 0.70]
    assert [s.claim_id for s in passing] == ["mid", "high"]


def test_verdict_to_epistemic_state_projection():
    matrix = EpistemicMatrix()
    claim = Claim(
        claim_id="spatial-1",
        statement="Spatial dispersal distance scales inversely with trait correlation",
        regime=InferenceRegime.BAYESIAN,
        prior_credence=0.5,
        sources=["doi:10.1038/nature12345", "doi:10.1126/science.67890"],
        premises=["Distance impedes diffusion", "Observed dissimilarity increases with distance"],
        boundary_conditions=["Contiguous continental biomes"],
    )

    verdict = matrix.evaluate(claim)
    state = verdict.to_epistemic_state(claim)

    assert isinstance(state, EpistemicState)
    assert state.claim_id == "spatial-1"
    assert state.is_warranted is True
    assert state.tier == EpistemicTier.T1
    assert state >= 0.80

    # Verify structural provenance axis
    graph = state.derivation_graph
    assert graph["claim_id"] == "spatial-1"
    assert graph["tier"] == "T1"
    assert len(graph["premises"]) == 2
    assert len(graph["sources"]) == 2
    assert len(graph["ast"]["gates"]) == 4
