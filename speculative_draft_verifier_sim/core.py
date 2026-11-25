"""Core analytical and trace-driven simulator for speculative decoding."""
from typing import Any, Dict, List


class SpeculativeSimulator:
    """Evaluates expected tokens/step and wall-clock speedup for speculative decoding."""

    def __init__(self, draft_cost: float = 0.08, target_cost: float = 1.0):
        if draft_cost <= 0 or target_cost <= 0:
            raise ValueError("Costs must be positive")
        self.draft_cost = draft_cost
        self.target_cost = target_cost

    def expected_accepted_tokens(self, alpha: float, gamma: int) -> float:
        if not (0.0 <= alpha <= 1.0):
            raise ValueError("alpha must be in [0, 1]")
        if gamma < 1:
            raise ValueError("gamma must be >= 1")
        if alpha == 1.0:
            return float(gamma + 1)
        # Expected tokens produced per verification step: (1 - alpha^(gamma+1)) / (1 - alpha)
        return (1.0 - (alpha ** (gamma + 1))) / (1.0 - alpha)

    def speedup(self, alpha: float, gamma: int) -> float:
        exp_toks = self.expected_accepted_tokens(alpha, gamma)
        step_cost = (gamma * self.draft_cost) + self.target_cost
        baseline_cost = exp_toks * self.target_cost
        return baseline_cost / step_cost

    def recommend_gamma(self, acceptance_prob: float, max_gamma: int = 12) -> Dict[str, Any]:
        curve: List[Dict[str, Any]] = []
        best = None
        for g in range(1, max_gamma + 1):
            sp = self.speedup(acceptance_prob, g)
            entry = {
                "gamma": g,
                "expected_tokens": round(self.expected_accepted_tokens(acceptance_prob, g), 3),
                "speedup": round(sp, 3),
            }
            curve.append(entry)
            if best is None or sp > best["speedup"]:
                best = entry
        return {"optimal_gamma": best["gamma"], "peak_speedup": best["speedup"], "curve": curve}
