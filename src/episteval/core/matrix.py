"""episteval.core.matrix — 4-Level x 3-Dimension INFERNO Evaluation Matrix."""

from __future__ import annotations

from typing import Dict, List, Optional
from episteval.core.models import (
    Claim,
    EpistemicLevel,
    EpistemicTier,
    EvaluationVerdict,
    GateResult,
    GateStatus,
    WarrantDimension,
)
from episteval.core.gates import (
    BoundaryFalsifiabilityGate,
    EpistemicGate,
    FormalizationStructureGate,
    InferentialMachineryGate,
    ObservationGroundingGate,
)


class InfernoMatrix:
    """The invariant INFERNO arbitration matrix.

    Evaluates a claim across the 4 epistemic levels and resolves its warrant tier.
    """

    def __init__(self, gates: Optional[List[EpistemicGate]] = None):
        self.gates: List[EpistemicGate] = gates or [
            ObservationGroundingGate(),
            FormalizationStructureGate(),
            InferentialMachineryGate(),
            BoundaryFalsifiabilityGate(),
        ]

    def evaluate(self, claim: Claim, weights: Optional[Dict[str, float]] = None) -> EvaluationVerdict:
        """Run all invariant gates and arbitrate the claim's warrant tier."""
        gate_results: List[GateResult] = []
        passed_gates: List[str] = []
        failed_gates: List[str] = []
        diagnostics: List[str] = []

        total_weight = 0.0
        weighted_sum = 0.0

        default_weights = {
            "L1_OBSERVATION_GROUNDING": 0.25,
            "L2_FORMALIZATION_STRUCTURE": 0.25,
            "L3_INFERENCE_MACHINERY": 0.25,
            "L4_BOUNDARY_FALSIFIABILITY": 0.25,
        }
        effective_weights = weights or default_weights

        for gate in self.gates:
            res = gate.evaluate(claim)
            gate_results.append(res)

            w = effective_weights.get(res.gate_id, 0.25)
            total_weight += w
            weighted_sum += res.score * w

            if res.status == GateStatus.PASS:
                passed_gates.append(res.gate_id)
            else:
                failed_gates.append(res.gate_id)
                for blocker in res.blockers:
                    diagnostics.append(f"[{res.gate_id}] {blocker}")

        composite_score = round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0

        # Lexicographic Gating: L1 or L4 failure caps composite tier at T2/T3
        has_l1_fail = any(r.level == EpistemicLevel.L1_OBSERVATION and r.status == GateStatus.FAIL for r in gate_results)
        has_l4_fail = any(r.level == EpistemicLevel.L4_BOUNDARY and r.status == GateStatus.FAIL for r in gate_results)

        if has_l1_fail or has_l4_fail or composite_score < 55.0:
            tier = EpistemicTier.T3
            is_warranted = False
        elif composite_score >= 80.0 and not failed_gates:
            tier = EpistemicTier.T1
            is_warranted = True
        else:
            tier = EpistemicTier.T2
            is_warranted = True

        summary = (
            f"Warranted at tier {tier.value} with composite score {composite_score}/100."
            if is_warranted
            else f"Defeated (Tier T3, {composite_score}/100) due to unpassed epistemic gates."
        )

        return EvaluationVerdict(
            claim_id=claim.claim_id,
            composite_score=composite_score,
            tier=tier,
            regime=claim.regime,
            gate_results=gate_results,
            passed_gates=passed_gates,
            failed_gates=failed_gates,
            is_warranted=is_warranted,
            summary=summary,
            diagnostics=diagnostics,
        )
