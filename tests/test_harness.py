from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from lantora_eval.adapters import ReferenceAdapter
from lantora_eval.registry import TaskValidationError, load_tasks
from lantora_eval.runner import run_evaluation


ROOT = Path(__file__).resolve().parents[1]


class HarnessTests(unittest.TestCase):
    def test_example_tasks_pass(self) -> None:
        tasks = load_tasks(ROOT / "evaluations" / "tasks")
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            manifest, results = run_evaluation(tasks, ReferenceAdapter(), output, seed=17)
            self.assertEqual(len(results), 3)
            self.assertTrue(all(item["score"]["matched"] for item in results))
            self.assertEqual(manifest["task_count"], 3)
            self.assertEqual({path.name for path in output.iterdir()}, {"manifest.json", "results.json", "report.md"})

    def test_same_seed_produces_same_output_hashes(self) -> None:
        tasks = load_tasks(ROOT / "evaluations" / "tasks")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            _, first = run_evaluation(tasks, ReferenceAdapter(), base / "first", seed=7)
            _, second = run_evaluation(tasks, ReferenceAdapter(), base / "second", seed=7)
        self.assertEqual(
            [item["output_sha256"] for item in first],
            [item["output_sha256"] for item in second],
        )
        self.assertEqual([item["score"] for item in first], [item["score"] for item in second])

    def test_invalid_task_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.json"
            path.write_text(json.dumps({"task_id": "incomplete"}), encoding="utf-8")
            with self.assertRaises(TaskValidationError):
                load_tasks(Path(temporary))

    def test_existing_bundle_is_not_overwritten(self) -> None:
        tasks = load_tasks(ROOT / "evaluations" / "tasks")
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            run_evaluation(tasks, ReferenceAdapter(), output, seed=0)
            with self.assertRaises(FileExistsError):
                run_evaluation(tasks, ReferenceAdapter(), output, seed=0)


if __name__ == "__main__":
    unittest.main()

