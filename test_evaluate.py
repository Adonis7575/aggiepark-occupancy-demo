import unittest

from decisions import occupancy_label
from evaluate import evaluate


class OccupancyEvaluationTests(unittest.TestCase):
    def test_unknown_does_not_count_as_open(self):
        cases = [("occupied", 0.42), ("occupied", 0.84), ("empty", 0.15)]
        self.assertEqual(evaluate(cases, 0)["false_opening_rate"], 0.5)
        result = evaluate(cases, 0.15)
        self.assertEqual(result["false_opening_rate"], 0)
        self.assertEqual(result["coverage"], 2 / 3)
        self.assertEqual(result["accepted_accuracy"], 1)
        self.assertEqual(result["matrix"]["occupied"]["unknown"], 1)

    def test_invalid_scores_defer(self):
        self.assertEqual(occupancy_label(float("nan")), "unknown")
        self.assertEqual(occupancy_label(-1), "unknown")

    def test_binary_and_band_boundaries(self):
        self.assertEqual(occupancy_label(0.5, 0), "occupied")
        self.assertEqual(occupancy_label(0.5), "unknown")
        self.assertEqual(occupancy_label(0.35), "empty")
        self.assertEqual(occupancy_label(0.65), "occupied")

    def test_undefined_metrics_are_explicit(self):
        result = evaluate([("empty", 0.5)], 0.15)
        self.assertEqual(result["coverage"], 0)
        self.assertIsNone(result["accepted_accuracy"])
        self.assertIsNone(result["false_opening_rate"])
