"""tests for episteval.core.matrix and domain profiles"""

import pytest
from episteval.core.models import Claim, EpistemicTier, InferenceRegime
from episteval.core.matrix import InfernoMatrix
from episteval.profiles.comparative import ComparativeHistoricalProfile


def test_inferno_matrix_lexicographic_gating():
    matrix = InfernoMatrix()

    # Strong claim that passes all gates
    strong_claim = Claim(
        claim_id="strong-1",
        statement="Spatial isolation-by-distance correlates with folklore dissimilarity",
        regime=InferenceRegime.BAYESIAN,
        prior_credence=0.5,
        sources=["berezkin_2015_matrix", "thuillard_2018_trames"],
        premises=["Geographic friction impedes oral transmission", "Pairwise great-circle distance proxy"],
        boundary_conditions=["Does not account for maritime navigation conduits", "Restricted to pre-industrial traditions"],
    )
    v_strong = matrix.evaluate(strong_claim)
    assert v_strong.is_warranted is True
    assert v_strong.tier == EpistemicTier.T1
    assert v_strong.composite_score >= 80.0

    # Claim failing observation and boundary conditions
    weak_claim = Claim(
        claim_id="weak-1",
        statement="Universal monomyth timeline across all humanity",
        regime=InferenceRegime.DEDUCTIVE,
        premises=[],  # fails formalization
        sources=[],   # fails grounding
        boundary_conditions=[], # fails boundary
    )
    v_weak = matrix.evaluate(weak_claim)
    assert v_weak.is_warranted is False
    assert v_weak.tier == EpistemicTier.T3
    assert len(v_weak.diagnostics) >= 2


def test_comparative_historical_profile():
    profile = ComparativeHistoricalProfile()

    claim = Claim(
        claim_id="comp-1",
        statement="Megafaunal celestial pursuit star clock",
        sources=["swanton_1909_recension"],
        premises=["Bear constellation alignment in boreal winter"],
        boundary_conditions=["Sub-arctic and boreal biomes only"],
    )
    verdict = profile.evaluate(claim)
    # 1 source is PROVISIONAL_PASS, so composite tier is T2
    assert verdict.tier == EpistemicTier.T2
    assert verdict.is_warranted is True
