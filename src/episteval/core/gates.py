"""episteval.core.gates — Invariant epistemic gates across the 4 INFERNO levels."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Protocol
from episteval.core.models import (
    Claim,
    EpistemicLevel,
    GateResult,
    GateStatus,
    InferenceRegime,
    WarrantDimension,
)


class EpistemicGate(ABC):
    """Abstract protocol for an invariant epistemic gate."""

    @property
    @abstractmethod
    def gate_id(self) -> str:
        """Unique identifier for the gate."""
        ...

    @property
    @abstractmethod
    def level(self) -> EpistemicLevel:
        """INFERNO level associated with this gate."""
        ...

    @property
    @abstractmethod
    def dimension(self) -> WarrantDimension:
        """Evaluative dimension associated with this gate."""
        ...

    @abstractmethod
    def evaluate(self, claim: Claim) -> GateResult:
        """Evaluate the claim and return a GateResult."""
        ...


class ObservationGroundingGate(EpistemicGate):
    """Gate L1: Checks that the claim is grounded in inspectable primary artifacts."""

    @property
    def gate_id(self) -> str:
        return "L1_OBSERVATION_GROUNDING"

    @property
    def level(self) -> EpistemicLevel:
        return EpistemicLevel.L1_OBSERVATION

    @property
    def dimension(self) -> WarrantDimension:
        return WarrantDimension.EMPIRICAL_GROUNDING

    def evaluate(self, claim: Claim) -> GateResult:
        if not claim.sources:
            return GateResult(
                gate_id=self.gate_id,
                level=self.level,
                dimension=self.dimension,
                status=GateStatus.FAIL,
                score=10.0,
                summary="Claim has zero empirical sources or artifact grounding.",
                blockers=["MISSING_PRIMARY_SOURCES"],
            )

        if len(claim.sources) >= 2:
            return GateResult(
                gate_id=self.gate_id,
                level=self.level,
                dimension=self.dimension,
                status=GateStatus.PASS,
                score=90.0,
                summary=f"Strong empirical grounding across {len(claim.sources)} sources.",
            )

        return GateResult(
            gate_id=self.gate_id,
            level=self.level,
            dimension=self.dimension,
            status=GateStatus.PROVISIONAL_PASS,
            score=65.0,
            summary="Sparsely grounded in a single empirical source.",
            blockers=["SINGLE_SOURCE_VULNERABILITY"],
        )


class FormalizationStructureGate(EpistemicGate):
    """Gate L2: Checks that the claim's premises and categorical schema are formally stated."""

    @property
    def gate_id(self) -> str:
        return "L2_FORMALIZATION_STRUCTURE"

    @property
    def level(self) -> EpistemicLevel:
        return EpistemicLevel.L2_FORMALIZATION

    @property
    def dimension(self) -> WarrantDimension:
        return WarrantDimension.FORMAL_INFERENCE

    def evaluate(self, claim: Claim) -> GateResult:
        if not claim.premises:
            return GateResult(
                gate_id=self.gate_id,
                level=self.level,
                dimension=self.dimension,
                status=GateStatus.FAIL,
                score=20.0,
                summary="Claim asserts conclusions without explicit premises.",
                blockers=["MISSING_FORMAL_PREMISES"],
            )

        return GateResult(
            gate_id=self.gate_id,
            level=self.level,
            dimension=self.dimension,
            status=GateStatus.PASS,
            score=85.0,
            summary=f"Premises formally articulated ({len(claim.premises)} premises).",
        )


class InferentialMachineryGate(EpistemicGate):
    """Gate L3: Validates the derivation machinery under the claimed inference regime."""

    @property
    def gate_id(self) -> str:
        return "L3_INFERENCE_MACHINERY"

    @property
    def level(self) -> EpistemicLevel:
        return EpistemicLevel.L3_INFERENCE

    @property
    def dimension(self) -> WarrantDimension:
        return WarrantDimension.FORMAL_INFERENCE

    def evaluate(self, claim: Claim) -> GateResult:
        blockers = []
        score = 80.0

        if claim.regime == InferenceRegime.DEDUCTIVE:
            if not claim.premises:
                score = 0.0
                blockers.append("DEDUCTIVE_INVALIDITY_EMPTY_PREMISES")
            elif claim.known_defeaters:
                score = 15.0
                blockers.append("DEDUCTIVE_CONTRADICTED_BY_DEFEATERS")

        elif claim.regime == InferenceRegime.BAYESIAN:
            if claim.prior_credence is None:
                score = 30.0
                blockers.append("MISSING_PRIOR_CREDENCE")

        elif claim.regime == InferenceRegime.DEFEASIBLE:
            if len(claim.known_defeaters) > 2:
                score = 45.0
                blockers.append("OVERWHELMED_BY_UNRESOLVED_DEFEATERS")

        status = GateStatus.PASS if score >= 70.0 else (GateStatus.PROVISIONAL_PASS if score >= 50.0 else GateStatus.FAIL)

        return GateResult(
            gate_id=self.gate_id,
            level=self.level,
            dimension=self.dimension,
            status=status,
            score=score,
            summary=f"Inference under {claim.regime.value} regime evaluated.",
            blockers=blockers,
        )


class BoundaryFalsifiabilityGate(EpistemicGate):
    """Gate L4: Checks explicit boundary conditions and empirical failure criteria."""

    @property
    def gate_id(self) -> str:
        return "L4_BOUNDARY_FALSIFIABILITY"

    @property
    def level(self) -> EpistemicLevel:
        return EpistemicLevel.L4_BOUNDARY

    @property
    def dimension(self) -> WarrantDimension:
        return WarrantDimension.EPISTEMIC_MEDIATION

    def evaluate(self, claim: Claim) -> GateResult:
        if not claim.boundary_conditions:
            return GateResult(
                gate_id=self.gate_id,
                level=self.level,
                dimension=self.dimension,
                status=GateStatus.FAIL,
                score=25.0,
                summary="Universal claim asserting no boundary conditions or falsification criteria.",
                blockers=["UNBOUNDED_SCOPE_VACUOUS_FALSIFIABILITY"],
            )

        return GateResult(
            gate_id=self.gate_id,
            level=self.level,
            dimension=self.dimension,
            status=GateStatus.PASS,
            score=90.0,
            summary=f"Explicit boundary conditions specified ({len(claim.boundary_conditions)} boundaries).",
        )
