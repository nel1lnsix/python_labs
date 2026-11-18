"""Регрессии проверки и бенчмарка ЛР7. Запуск: python -m src.lab07.test_cases."""
import contextlib
from copy import deepcopy
import csv
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from src.lab07 import bench, check
from src.lab07.sorting import bubble_sort

ROOT = Path(__file__).resolve().parents[2]


class Lab07Tests(unittest.TestCase):
    def test_required_check_functions_are_callable(self):
        for name in ("check_sorting", "check_search", "check_two_sum"):
            with self.subTest(function=name):
                self.assertTrue(callable(getattr(check, name, None)), name)
        if callable(getattr(check, "check_sorting", None)):
            self.assertIsNone(check.check_sorting(bubble_sort, trials=3))
            self.assertIsNone(check.check_search())
            self.assertIsNone(check.check_two_sum(trials=3))

    def test_repeated_check_does_not_accumulate_global_cases(self):
        original = check.PAIR_EDGES.copy()
        with contextlib.redirect_stdout(io.StringIO()):
            check.main()
            check.main()
        self.assertEqual(check.PAIR_EDGES, original)

    def test_sort_checker_reports_bad_algorithm_and_input(self):
        def wrong_sort(nums):
            return nums.copy()

        checker = getattr(check, "check_sorting", None)
        self.assertTrue(callable(checker), "Нет check_sorting")
        with self.assertRaises(AssertionError) as failure:
            checker(wrong_sort, trials=0)
        self.assertIn("wrong_sort", str(failure.exception))
        self.assertIn("2", str(failure.exception))
        self.assertIn("1", str(failure.exception))

    def test_bad_algorithm_cannot_change_fixed_cases(self):
        def mutating_sort(nums):
            nums.append(42)
            return sorted(nums)

        original = deepcopy(check.SORT_EDGES)
        with self.assertRaises(AssertionError):
            check.check_sorting(mutating_sort, trials=0)
        self.assertEqual(check.SORT_EDGES, original)

    def test_quick_benchmark_prints_header_and_preparation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "bench.csv"
            result = subprocess.run(
                [sys.executable, "-X", "utf8", "-m", "src.lab07.bench", "--quick",
                 "--output", str(target)], cwd=ROOT, capture_output=True,
                text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("task", result.stdout.splitlines()[0])
            self.assertIn("search_prepare", result.stdout)
            with target.open(encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream)
                self.assertEqual(reader.fieldnames, ["task", "n", "impl", "seconds"])
                rows = list(reader)
            self.assertEqual(len(rows), 15)
            self.assertTrue(any(row["task"] == "search_10" for row in rows))

    def test_large_sort_limit_is_real_and_small_sort_completes(self):
        limited = getattr(bench, "measure_limited", None)
        self.assertTrue(callable(limited), "Нет ограниченного запуска")
        seconds = limited(bubble_sort, [3, 1, 2], timeout=10)
        self.assertIsInstance(seconds, float)
        self.assertGreaterEqual(seconds, 0)
        result = limited(bubble_sort, list(range(5000, 0, -1)), timeout=0.01)
        self.assertEqual(result, ">0.01s")


if __name__ == "__main__":
    unittest.main(verbosity=2)
