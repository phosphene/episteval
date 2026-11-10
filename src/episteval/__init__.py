"""episteval — Epistemic evaluation across modality, monotonicity, and credence."""

from episteval.core.models import (
    Claim,
    EpistemicLevel,
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

__version__ = "0.1.0"
__all__ = [
    "Claim",
    "EpistemicLevel",
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
