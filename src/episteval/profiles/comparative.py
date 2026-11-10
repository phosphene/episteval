"""episteval.profiles.comparative — Domain profile for Comparative Historical and Deep Time Sciences."""

from __future__ import annotations

from typing import Dict
from episteval.profiles.base import DomainProfile


class ComparativeHistoricalProfile(DomainProfile):
    """Calibrated profile for historical, phylogenetic, and evolutionary narrative claims.

    Elevates empirical observation and boundary falsifiability while heavily punishing
    unbounded universal claims or ungrounded speculative sequences.
    """

    @property
    def profile_id(self) -> str:
        return "comparative_historical"

    @property
    def weights(self) -> Dict[str, float]:
        return {
            "L1_OBSERVATION_GROUNDING": 0.35,  # Philological anchor / primary text depth
            "L2_FORMALIZATION_STRUCTURE": 0.15,
            "L3_INFERENCE_MACHINERY": 0.20,
            "L4_BOUNDARY_FALSIFIABILITY": 0.30,  # Strict null models and spatial controls
        }
