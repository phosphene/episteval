"""episteval.profiles.base — Abstract base protocol for domain-specific evaluation profiles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict
from episteval.core.models import Claim, EvaluationVerdict
from episteval.core.matrix import InfernoMatrix


class DomainProfile(ABC):
    """Abstract protocol for domain-specific calibration weights and gates."""

    @property
    @abstractmethod
    def profile_id(self) -> str:
        """Unique identifier for the domain profile."""
        ...

    @property
    @abstractmethod
    def weights(self) -> Dict[str, float]:
        """Weight distribution across evaluated gates."""
        ...

    def evaluate(self, claim: Claim) -> EvaluationVerdict:
        """Evaluate a claim under this domain profile."""
        matrix = InfernoMatrix()
        return matrix.evaluate(claim, weights=self.weights)
