"""episteval.profiles.synthetic — Domain profile for Synthetic and Automated Reasoning (LLMs / Agents)."""

from __future__ import annotations

from typing import Dict
from episteval.profiles.base import DomainProfile


class SyntheticReasoningProfile(DomainProfile):
    """Calibrated profile for generative models and synthetic reasoning traces.

    Focuses heavily on premise-conclusion deduction and counterfactual boundary resilience.
    """

    @property
    def profile_id(self) -> str:
        return "synthetic_reasoning"

    @property
    def weights(self) -> Dict[str, float]:
        return {
            "L1_OBSERVATION_GROUNDING": 0.20,
            "L2_FORMALIZATION_STRUCTURE": 0.30,
            "L3_INFERENCE_MACHINERY": 0.35,
            "L4_BOUNDARY_FALSIFIABILITY": 0.15,
        }
