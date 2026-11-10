"""tests for episteval.core.gates"""

import pytest
from episteval.core.models import Claim, GateStatus, InferenceRegime
from episteval.core.gates import (
    ObservationGroundingGate,
    FormalizationStructureGate,
    InferentialMachineryGate,
    BoundaryFalsifiabilityGate,
)


def test_observation_grounding_gate():
    gate = ObservationGroundingGate()

    # Ungrounded claim
    c_empty = Claim(claim_id="c1", statement="Something exists")
    res_empty = gate.evaluate(c_empty)
    assert res_empty.status == GateStatus.FAIL
    assert "MISSING_PRIMARY_SOURCES" in res_empty.blockers

    # Fully grounded claim
    c_grounded = Claim(
        claim_id="c2",
        statement="Measured radial velocity matches Keplerian orbital mechanics",
        sources=["doi:10.1086/123456", "arxiv:2301.00001"],
    )
    res_grounded = gate.evaluate(c_grounded)
    assert res_grounded.status == GateStatus.PASS
    assert res_grounded.score == 90.0

    # Sparsely grounded claim
    c_sparse = Claim(
        claim_id="c2b",
        statement="Preliminary measurement report",
        sources=["doi:10.1086/123456"],
    )
    res_sparse = gate.evaluate(c_sparse)
    assert res_sparse.status == GateStatus.PROVISIONAL_PASS
    assert "SINGLE_SOURCE_VULNERABILITY" in res_sparse.blockers


def test_formalization_structure_gate():
    gate = FormalizationStructureGate()

    c_unstructured = Claim(claim_id="c3", statement="Speculative sequence")
    res_unstructured = gate.evaluate(c_unstructured)
    assert res_unstructured.status == GateStatus.FAIL
    assert "MISSING_FORMAL_PREMISES" in res_unstructured.blockers

    c_structured = Claim(
        claim_id="c4",
        statement="Gravitational acceleration is uniform at sea level",
        premises=["P1: Mass of Earth is constant", "P2: Distance to center of mass is uniform"],
    )
    res_structured = gate.evaluate(c_structured)
    assert res_structured.status == GateStatus.PASS
    assert res_structured.score == 85.0


def test_inferential_machinery_gate():
    gate = InferentialMachineryGate()

    # Deductive with known defeater -> FAIL
    c_defeated = Claim(
        claim_id="c5",
        statement="All organisms require sunlight",
        regime=InferenceRegime.DEDUCTIVE,
        premises=["Known autotrophs utilize photosynthesis"],
        known_defeaters=["Chemosynthetic hydrothermal vent biotas"],
    )
    res_defeated = gate.evaluate(c_defeated)
    assert res_defeated.status == GateStatus.FAIL
    assert "DEDUCTIVE_CONTRADICTED_BY_DEFEATERS" in res_defeated.blockers

    # Defeasible with defeater -> PASS (if <= 2 defeaters)
    c_defeasible = Claim(
        claim_id="c5b",
        statement="Avian species possess powered flight",
        regime=InferenceRegime.DEFEASIBLE,
        premises=["Flight morphology observed across primary clades"],
        known_defeaters=["Ratites exhibit secondary flight loss"],
    )
    res_defeasible = gate.evaluate(c_defeasible)
    assert res_defeasible.status == GateStatus.PASS
    assert res_defeasible.score == 80.0

    # Bayesian with missing prior -> PROVISIONAL_PASS
    c_bayes_no_prior = Claim(
        claim_id="c5c",
        statement="Planetary transit probability",
        regime=InferenceRegime.BAYESIAN,
        premises=["Transit dip observed in lightcurve"],
    )
    res_bayes = gate.evaluate(c_bayes_no_prior)
    assert res_bayes.status == GateStatus.FAIL
    assert "MISSING_PRIOR_CREDENCE" in res_bayes.blockers


def test_boundary_falsifiability_gate():
    gate = BoundaryFalsifiabilityGate()

    # Unbounded claim
    c_unbounded = Claim(claim_id="c6", statement="Physical constant invariant across all possible universes")
    res_unbounded = gate.evaluate(c_unbounded)
    assert res_unbounded.status == GateStatus.FAIL
    assert "UNBOUNDED_SCOPE_VACUOUS_FALSIFIABILITY" in res_unbounded.blockers

    # Bounded claim
    c_bounded = Claim(
        claim_id="c7",
        statement="Superconductivity manifests below critical temperature threshold",
        boundary_conditions=["Temperature <= Tc", "Ambient pressure ambient atmospheric"],
    )
    res_bounded = gate.evaluate(c_bounded)
    assert res_bounded.status == GateStatus.PASS
    assert res_bounded.score == 90.0
