"""episteval.cli — Command-line interface for epistemic evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from episteval.core.models import Claim, InferenceRegime
from episteval.core.matrix import EpistemicMatrix
from episteval.profiles.comparative import ComparativeHistoricalProfile
from episteval.profiles.synthetic import SyntheticReasoningProfile


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="episteval",
        description="Epistemic evaluation across modality, monotonicity, and credence.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Evaluate a claim JSON file against epistemic evaluation gates.")
    check_parser.add_argument("file", type=Path, help="Path to claim JSON file")
    check_parser.add_argument(
        "--profile",
        choices=["invariant", "comparative", "synthetic"],
        default="invariant",
        help="Domain calibration profile to use (default: invariant)",
    )

    args = parser.parse_args()

    if args.command == "check":
        if not args.file.exists():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)

        try:
            data = json.loads(args.file.read_text(encoding="utf-8"))
            claim = Claim.model_validate(data)
        except Exception as e:
            print(f"Error parsing claim file: {e}", file=sys.stderr)
            sys.exit(1)

        if args.profile == "comparative":
            profile = ComparativeHistoricalProfile()
            verdict = profile.evaluate(claim)
        elif args.profile == "synthetic":
            profile = SyntheticReasoningProfile()
            verdict = profile.evaluate(claim)
        else:
            matrix = EpistemicMatrix()
            verdict = matrix.evaluate(claim)

        print("\n" + "=" * 60)
        print(f"EPISTEVAL VERDICT: {verdict.claim_id}")
        print("=" * 60)
        print(f"Tier:            {verdict.tier.value}")
        print(f"Composite Score: {verdict.composite_score}/100")
        print(f"Warranted:       {'YES' if verdict.is_warranted else 'NO'}")
        print(f"Regime:          {verdict.regime.value}")
        print(f"Summary:         {verdict.summary}")
        print("-" * 60)
        print("Gate Outcomes:")
        for res in verdict.gate_results:
            status_icon = "✔" if res.status.value == "PASS" else ("~" if res.status.value == "PROVISIONAL_PASS" else "✘")
            print(f"  [{status_icon}] {res.gate_id:<28} : {res.status.value:<16} ({res.score:5.1f}/100)")
        if verdict.diagnostics:
            print("-" * 60)
            print("Diagnostics / Blockers:")
            for d in verdict.diagnostics:
                print(f"  • {d}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
