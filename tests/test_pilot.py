from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from lantora_eval.artifacts import sha256
from lantora_eval.pilot.adapters import PilotHeuristicAdapter, PilotRandomAdapter
from lantora_eval.pilot.generators import generate_suite, validate_suite, write_suite
from lantora_eval.pilot.study import run_seed_study
from lantora_eval.pilot.rendering import render_task
from lantora_eval.registry import load_tasks
from lantora_eval.runner import run_evaluation
from lantora_eval.scoring import score
from lantora_eval.statistics import grouped_summary, wilson_interval


class GoldProbeAdapter:
    name = "gold-probe"
    version = "test"

    def configuration(self):
        return {}

    def run(self, task, *, seed):
        from lantora_eval.models import AdapterResponse

        del seed
        return AdapterResponse(output=task.expected, steps=1)


class PilotGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tasks = generate_suite(seed=13001, items_per_condition=4)

    def test_all_families_and_conditions_are_balanced(self) -> None:
        counts = {}
        for task in self.tasks:
            key = (task.family, task.condition)
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(len(counts), 9)
        self.assertEqual(set(counts.values()), {4})

    def test_generation_is_deterministic(self) -> None:
        again = generate_suite(seed=13001, items_per_condition=4)
        self.assertEqual(
            [sha256(task.input) for task in self.tasks],
            [sha256(task.input) for task in again],
        )
        self.assertEqual(
            [sha256(task.expected) for task in self.tasks],
            [sha256(task.expected) for task in again],
        )

    def test_generated_tasks_round_trip_through_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "suite"
            manifest = write_suite(self.tasks, root, seed=13001)
            loaded = load_tasks(root / "tasks")
        self.assertEqual(manifest["task_count"], 36)
        self.assertEqual([task.task_id for task in loaded], sorted(task.task_id for task in self.tasks))

    def test_ambiguous_reasoning_task_is_rejected(self) -> None:
        task = next(task for task in self.tasks if task.family == "abstract-reasoning")
        bad = replace(task, input={"demonstrations": [], "query": task.input["query"]})
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            validate_suite([bad])

    def test_imbalanced_learning_task_is_rejected(self) -> None:
        task = next(task for task in self.tasks if task.family == "learning-transfer")
        label = task.input["demonstrations"][0]["label"]
        demos = [item for item in task.input["demonstrations"] if item["label"] == label]
        bad = replace(task, input={**task.input, "demonstrations": demos})
        with self.assertRaisesRegex(ValueError, "imbalanced"):
            validate_suite([bad])

    def test_unsatisfiable_plan_is_rejected(self) -> None:
        task = next(task for task in self.tasks if task.family == "planning")
        first, second = task.input["nodes"][:2]
        bad = replace(task, input={**task.input, "before": [[first, second], [second, first]]})
        with self.assertRaisesRegex(ValueError, "unsatisfiable"):
            validate_suite([bad])

    def test_planning_scorer_accepts_alternative_valid_plan(self) -> None:
        task = next(task for task in self.tasks if task.family == "planning")
        result = score(task, task.expected)
        self.assertTrue(result["matched"])
        self.assertEqual(result["violations"], [])

    def test_candidate_rendering_excludes_gold_and_metadata(self) -> None:
        rendered = render_task(self.tasks[0])
        self.assertNotIn("expected", rendered)
        self.assertNotIn("metadata", rendered)
        self.assertIn("input", rendered)


class PilotReportingTests(unittest.TestCase):
    def test_untrusted_adapter_cannot_read_gold_answer(self) -> None:
        task = next(
            task
            for task in generate_suite(seed=13001, items_per_condition=1)
            if task.expected is not None
        )
        with tempfile.TemporaryDirectory() as temporary:
            _, results = run_evaluation(
                [task], GoldProbeAdapter(), Path(temporary) / "run", seed=0
            )
        self.assertIsNone(results[0]["output"])
        self.assertFalse(results[0]["score"]["matched"])

    def test_wilson_interval_known_boundary(self) -> None:
        low, high = wilson_interval(10, 10)
        self.assertAlmostEqual(low, 0.722467, places=5)
        self.assertAlmostEqual(high, 1.0)

    def test_heuristic_baseline_and_reports(self) -> None:
        tasks = generate_suite(seed=13002, items_per_condition=2)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            manifest, results = run_evaluation(tasks, PilotHeuristicAdapter(), output, seed=17)
            report = (output / "report.md").read_text(encoding="utf-8")
        self.assertTrue(all(item["score"]["matched"] for item in results))
        self.assertEqual(len(manifest["grouped_statistics"]), 9)
        self.assertEqual(len(manifest["transfer_differences"]), 3)
        self.assertIn("No composite AGI score", report)
        self.assertIn("Control-to-transfer differences", report)

    def test_random_baseline_is_reproducible(self) -> None:
        tasks = generate_suite(seed=13003, items_per_condition=2)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, first = run_evaluation(tasks, PilotRandomAdapter(), root / "first", seed=99)
            _, second = run_evaluation(tasks, PilotRandomAdapter(), root / "second", seed=99)
        self.assertEqual(
            [item["output_sha256"] for item in first],
            [item["output_sha256"] for item in second],
        )

    def test_outcomes_are_counted_separately(self) -> None:
        results = [
            {"family": "x", "condition": "control", "score": {"matched": True, "outcome": "correct"}},
            {"family": "x", "condition": "control", "score": {"matched": False, "outcome": "abstained"}},
        ]
        summary = grouped_summary(results)[0]
        self.assertEqual(summary["outcomes"], {"abstained": 1, "correct": 1})

    def test_five_seed_study_reports_variation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            summary = run_seed_study(
                seeds=[13001, 13002, 13003, 13004, 13005],
                items_per_condition=1,
                adapter=PilotRandomAdapter(),
                output=Path(temporary) / "study",
            )
        self.assertEqual(len(summary["runs"]), 5)
        self.assertEqual(len(summary["seed_variation"]), 9)
        self.assertTrue(all(item["seed_count"] == 5 for item in summary["seed_variation"]))


if __name__ == "__main__":
    unittest.main()
