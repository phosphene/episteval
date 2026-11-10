"""episteval — Epistemic evaluation across modality, monotonicity, and credence."""

from __future__ import annotations

from episteval.core.models import (
    Claim,
    EpistemicLevel,
    EpistemicState,
    EpistemicTier,
    EvaluationVerdict,
    GateResult,
    GateStatus,
    InferenceRegime,
    WarrantDimension,
)
from episteval.core.gates import (
    BoundaryFalsifiabilityGate,
    EpistemicGate,
    FormalizationStructureGate,
    InferentialMachineryGate,
    ObservationGroundingGate,
)
from episteval.core.matrix import InfernoMatrix
from episteval.profiles.base import DomainProfile
from episteval.profiles.comparative import ComparativeHistoricalProfile
from episteval.profiles.synthetic import SyntheticReasoningProfile

__version__ = "0.2.0"
__all__ = [
    "Claim",
    "EpistemicLevel",
    "EpistemicState",
    "EpistemicTier",
    "EvaluationVerdict",
    "GateResult",
    "GateStatus",
    "InferenceRegime",
    "WarrantDimension",
    "EpistemicGate",
    "ObservationGroundingGate",
    "FormalizationStructureGate",
    "InferentialMachineryGate",
    "BoundaryFalsifiabilityGate",
    "InfernoMatrix",
    "DomainProfile",
    "ComparativeHistoricalProfile",
    "SyntheticReasoningProfile",
]
