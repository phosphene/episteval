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
        statement="Circumpolar hunt distribution",
        sources=["urn:cts:phosphene:swanton.1909", "urn:cts:phosphene:boas.1916"],
    )
    res_grounded = gate.evaluate(c_grounded)
    assert res_grounded.status == GateStatus.PASS
    assert res_grounded.score >= 80.0


def test_formalization_structure_gate():
    gate = FormalizationStructureGate()

    # No premises
    c_noprem = Claim(claim_id="c3", statement="Conclusion without premise")
    res_noprem = gate.evaluate(c_noprem)
    assert res_noprem.status == GateStatus.FAIL

    # Stated premises
    c_prem = Claim(
        claim_id="c4",
        statement="Conclusion",
        premises=["P1: If distance increases, dissimilarity increases", "P2: Distance observed > 5000km"],
    )
    res_prem = gate.evaluate(c_prem)
    assert res_prem.status == GateStatus.PASS


def test_deductive_machinery_defeater():
    gate = InferentialMachineryGate()

    # Deductive claim with contradictory defeaters
    c_ded = Claim(
        claim_id="c5",
        statement="X is strictly true",
        regime=InferenceRegime.DEDUCTIVE,
        premises=["P1: All A are B", "P2: x is A"],
        known_defeaters=["Observation: x is not B"],
    )
    res_ded = gate.evaluate(c_ded)
    assert res_ded.status == GateStatus.FAIL
    assert "DEDUCTIVE_CONTRADICTED_BY_DEFEATERS" in res_ded.blockers


def test_boundary_falsifiability_gate():
    gate = BoundaryFalsifiabilityGate()

    c_unbounded = Claim(claim_id="c6", statement="Universal myth archetype holds everywhere")
    res_unbounded = gate.evaluate(c_unbounded)
    assert res_unbounded.status == GateStatus.FAIL

    c_bounded = Claim(
        claim_id="c7",
        statement="Circumpolar distribution holds only above 50N",
        boundary_conditions=["Latitude >= 50 degrees N", "Terrestrial megafauna presence required"],
    )
    res_bounded = gate.evaluate(c_bounded)
    assert res_bounded.status == GateStatus.PASS
