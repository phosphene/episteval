"""episteval.core.models — Core models for epistemic evaluation."""

from __future__ import annotations

import math
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


class EpistemicState(BaseModel):
    """Dual-faceted epistemic evaluation artifact.

    Combines Python numeric data model projection with complete
    derivation hypergraph provenance and regime semantics.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    claim_id: str
    warrant_score: float = Field(..., ge=0.0, le=1.0, description="Calibrated scalar warrant [0.0, 1.0]")
    tier: EpistemicTier
    regime: InferenceRegime
    is_warranted: bool
    summary: str
    premises: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    boundary_conditions: List[str] = Field(default_factory=list)
    defeaters: List[str] = Field(default_factory=list)
    diagnostics: List[str] = Field(default_factory=list)
    derivation_ast: Dict[str, Any] = Field(default_factory=dict, description="Structural AST / derivation hypergraph")

    # --- Scalar Projection Axis: Numeric Data Model ---

    def __float__(self) -> float:
        """Projects directly to calibrated scalar warrant [0.0, 1.0]."""
        return float(self.warrant_score)

    def __bool__(self) -> bool:
        """Evaluates truthiness based on certified epistemic warrant."""
        return bool(self.is_warranted)

    def __int__(self) -> int:
        return int(self.warrant_score)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EpistemicState):
            return super().__eq__(other)
        if isinstance(other, (int, float)):
            return math.isclose(self.warrant_score, float(other), rel_tol=1e-9, abs_tol=1e-9)
        return False

    def __lt__(self, other: Any) -> bool:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score < val

    def __le__(self, other: Any) -> bool:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score <= val

    def __gt__(self, other: Any) -> bool:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score > val

    def __ge__(self, other: Any) -> bool:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score >= val

    def __add__(self, other: Any) -> float:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score + val

    def __radd__(self, other: Any) -> float:
        return self.__add__(other)

    def __sub__(self, other: Any) -> float:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score - val

    def __rsub__(self, other: Any) -> float:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return val - self.warrant_score

    def __mul__(self, other: Any) -> float:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score * val

    def __rmul__(self, other: Any) -> float:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> float:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return self.warrant_score / val

    def __rtruediv__(self, other: Any) -> float:
        val = float(other) if isinstance(other, (int, float, EpistemicState)) else NotImplemented
        if val is NotImplemented:
            return NotImplemented
        return val / self.warrant_score

    # --- Structural Provenance Axis ---

    @property
    def derivation_graph(self) -> Dict[str, Any]:
        """Returns the full inferential topology and premise dependency chain."""
        return {
            "claim_id": self.claim_id,
            "regime": self.regime.value,
            "tier": self.tier.value,
            "warrant_score": self.warrant_score,
            "is_warranted": self.is_warranted,
            "summary": self.summary,
            "premises": self.premises,
            "sources": self.sources,
            "boundary_conditions": self.boundary_conditions,
            "defeaters": self.defeaters,
            "diagnostics": self.diagnostics,
            "ast": self.derivation_ast,
        }


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

    def to_epistemic_state(self, claim: Optional[Claim] = None) -> EpistemicState:
        """Projects this verdict into a dual-faceted EpistemicState artifact."""
        warrant_scalar = round(self.composite_score / 100.0, 4)
        premises = list(claim.premises) if claim else []
        sources = list(claim.sources) if claim else []
        boundary = list(claim.boundary_conditions) if claim else []
        defeaters = list(claim.known_defeaters) if claim else []

        ast: Dict[str, Any] = {
            "regime": self.regime.value,
            "composite_score": self.composite_score,
            "tier": self.tier.value,
            "gates": [
                {
                    "gate_id": g.gate_id,
                    "level": g.level.value,
                    "dimension": g.dimension.value,
                    "status": g.status.value,
                    "score": g.score,
                    "blockers": g.blockers,
                }
                for g in self.gate_results
            ],
        }

        return EpistemicState(
            claim_id=self.claim_id,
            warrant_score=warrant_scalar,
            tier=self.tier,
            regime=self.regime,
            is_warranted=self.is_warranted,
            summary=self.summary,
            premises=premises,
            sources=sources,
            boundary_conditions=boundary,
            defeaters=defeaters,
            diagnostics=list(self.diagnostics),
            derivation_ast=ast,
        )
