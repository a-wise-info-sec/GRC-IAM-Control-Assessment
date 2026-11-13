"""Edge cases that prevent overly optimistic assessment conclusions."""
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from check_terminations import classify, assess  # noqa: E402


class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.start = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)

    def test_on_time_at_boundary(self):
        result, _ = classify(self.start, self.start + timedelta(hours=24), "DISABLED")
        self.assertEqual(result, "PASS")

    def test_late_by_one_second(self):
        result, _ = classify(self.start, self.start + timedelta(hours=24, seconds=1), "DISABLED")
        self.assertEqual(result, "LATE")

    def test_disabled_snapshot_without_event_is_not_pass(self):
        result, _ = classify(self.start, None, "DISABLED")
        self.assertEqual(result, "INSUFFICIENT_EVIDENCE")

    def test_active_after_termination(self):
        result, _ = classify(self.start, None, "ACTIVE")
        self.assertEqual(result, "ACTIVE")

    def test_conflicting_event_and_snapshot(self):
        result, _ = classify(self.start, self.start + timedelta(hours=2), "ACTIVE")
        self.assertEqual(result, "CONFLICTING_EVIDENCE")

    def test_premature_event_is_review_required(self):
        result, _ = classify(self.start, self.start - timedelta(hours=2), "DISABLED")
        self.assertEqual(result, "REVIEW_REQUIRED")

    def test_full_dataset(self):
        rows = assess()
        self.assertEqual(len(rows), 12)
        from collections import Counter
        self.assertEqual(Counter(row["result"] for row in rows), {
            "PASS": 8, "LATE": 2, "ACTIVE": 1, "INSUFFICIENT_EVIDENCE": 1
        })


if __name__ == "__main__":
    unittest.main()
