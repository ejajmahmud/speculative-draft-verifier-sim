"""Tests for Speculative Draft Verifier Sim."""
import unittest
from speculative_draft_verifier_sim.core import SpeculativeSimulator


class TestSpeculativeSimulator(unittest.TestCase):
    def test_high_acceptance_yields_strong_speedup(self):
        sim = SpeculativeSimulator(draft_cost=0.05, target_cost=1.0)
        res = sim.recommend_gamma(acceptance_prob=0.85, max_gamma=10)
        self.assertGreater(res["peak_speedup"], 2.0)
        self.assertGreaterEqual(res["optimal_gamma"], 4)

    def test_low_acceptance_prefers_small_gamma(self):
        sim = SpeculativeSimulator(draft_cost=0.2, target_cost=1.0)
        res = sim.recommend_gamma(acceptance_prob=0.2, max_gamma=8)
        self.assertEqual(res["optimal_gamma"], 1)

    def test_invalid_alpha_raises(self):
        with self.assertRaises(ValueError):
            SpeculativeSimulator().expected_accepted_tokens(1.5, 4)
