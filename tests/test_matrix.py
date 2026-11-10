"""tests for episteval.core.matrix"""

import pytest
from episteval.core.models import Claim, EpistemicTier, InferenceRegime
from episteval.core.matrix import EpistemicMatrix
from episteval.profiles.comparative import ComparativeHistoricalProfile


def test_epistemic_matrix_lexicographic_gating():
    matrix = EpistemicMatrix()

    # Valid fully warranted claim
    strong_claim = Claim(
        claim_id="strong-1",
        statement="Spatial dispersal distance scales inversely with trait correlation",
        regime=InferenceRegime.DEDUCTIVE,
        sources=["doi:10.1038/nature12345", "doi:10.1126/science.67890"],
        premises=[
            "Dispersal barrier restricts gene and cultural flow",
            "Observed variance increases with geographical distance",
        ],
        boundary_conditions=["Contiguous continental biomes"],
    )
    verdict = matrix.evaluate(strong_claim)
    assert verdict.is_warranted is True
    assert verdict.tier == EpistemicTier.T1
    assert verdict.composite_score >= 80.0
    assert len(verdict.passed_gates) == 4
    assert len(verdict.failed_gates) == 0

    # Weak claim failing multiple gates
    weak_claim = Claim(
        claim_id="weak-1",
        statement="Universal teleological law governs all cosmic complexity",
        regime=InferenceRegime.DEDUCTIVE,
        premises=[],  # fails formalization
        sources=[],   # fails grounding
        boundary_conditions=[],  # fails boundary
    )
    v_weak = matrix.evaluate(weak_claim)
    assert v_weak.is_warranted is False
    assert v_weak.tier == EpistemicTier.T3
    assert len(v_weak.diagnostics) >= 2


def test_comparative_historical_profile():
    profile = ComparativeHistoricalProfile()

    claim = Claim(
        claim_id="comp-1",
        statement="Glacial retreat timing correlates with sediment varve chronology",
        sources=["doi:10.1130/G12345.1"],
        premises=["Varve layer thickness indicates annual summer ablation rate"],
        boundary_conditions=["Periglacial lacustrine basins"],
    )
    verdict = profile.evaluate(claim)
    # 1 source is PROVISIONAL_PASS, so composite tier is T2
    assert verdict.tier == EpistemicTier.T2
    assert verdict.is_warranted is True
