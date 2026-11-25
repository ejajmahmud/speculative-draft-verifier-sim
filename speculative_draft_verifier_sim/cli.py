"""CLI for Speculative Draft Verifier Sim."""
import argparse
import json
from .core import SpeculativeSimulator


def main():
    parser = argparse.ArgumentParser(description="Speculative Draft Verifier Sim CLI")
    parser.add_argument("--alpha", type=float, default=0.8, help="Per-token draft acceptance probability")
    parser.add_argument("--max-gamma", type=int, default=10, help="Maximum lookahead gamma")
    args = parser.parse_args()

    sim = SpeculativeSimulator()
    print(json.dumps(sim.recommend_gamma(args.alpha, max_gamma=args.max_gamma), indent=2))


if __name__ == "__main__":
    main()
