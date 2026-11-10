"""episteval.core.models — Core models for epistemic evaluation."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class EpistemicTier(str, Enum):
    """Certified warrant tier."""
    T1 = "T1"  # High warrant / robust under counterfactual perturbation (WCI >= 80)
    T2 = "T2"  # Provisional warrant / valid with methodological caveats (55 <= WCI < 80)
    T3 = "T3"  # Defeated or ungrounded warrant (WCI < 55)


class GateStatus(str, Enum):
    """Evaluation status for an epistemic gate."""
    PASS = "PASS"
    PROVISIONAL_PASS = "PROVISIONAL_PASS"
    FAIL = "FAIL"


class InferenceRegime(str, Enum):
    """Inference regime governing claim derivation."""
    DEDUCTIVE = "deductive"          # Strict monotonic entailment (P |- Q)
    DEFEASIBLE = "defeasible"        # Non-monotonic warrant subject to defeaters (P ~ Q)
    BAYESIAN = "bayesian"            # Probabilistic credence calibration P(H|E)
    COUNTERFACTUAL = "counterfactual"# Modal stability across accessible worlds


class EpistemicLevel(str, Enum):
    """The four invariant INFERNO epistemic levels."""
    L1_OBSERVATION = "L1_observation"          # Grounding in primary empirical artifacts
    L2_FORMALIZATION = "L2_formalization"      # Structural typing, relations, and schemas
    L3_INFERENCE = "L3_inference"              # Explicit inferential/derivation machinery
    L4_BOUNDARY = "L4_boundary"                # Boundary conditions and falsifiability


class WarrantDimension(str, Enum):
    """The three invariant dimensions evaluated at each epistemic level."""
    EMPIRICAL_GROUNDING = "empirical_grounding" # Grounding / evidence density
    FORMAL_INFERENCE = "formal_inference"       # Soundness, deduction, internal consistency
    EPISTEMIC_MEDIATION = "epistemic_mediation" # Acknowledged limits, boundary conditions, caveats


class GateResult(BaseModel):
    """Result of evaluating a single epistemic gate."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    gate_id: str
    level: EpistemicLevel
    dimension: WarrantDimension
    status: GateStatus
    score: float = Field(..., ge=0.0, le=100.0, description="Calibrated score 0-100")
    summary: str
    blockers: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Claim(BaseModel):
    """An asserted proposition subjected to epistemic evaluation."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    claim_id: str
    statement: str
    regime: InferenceRegime = InferenceRegime.DEFEASIBLE
    premises: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    boundary_conditions: List[str] = Field(default_factory=list)
    known_defeaters: List[str] = Field(default_factory=list)
    prior_credence: Optional[float] = Field(None, ge=0.0, le=1.0)


class EvaluationVerdict(BaseModel):
    """Final arbitration verdict across all evaluated gates."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    claim_id: str
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: EpistemicTier
    regime: InferenceRegime
    gate_results: List[GateResult]
    passed_gates: List[str]
    failed_gates: List[str]
    is_warranted: bool
    summary: str
    diagnostics: List[str] = Field(default_factory=list)
